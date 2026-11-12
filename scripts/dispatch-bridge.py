#!/usr/bin/env python3
"""Push-triggered GitHub Actions dispatch bridge, NOT a build/deploy pipeline.

Only a newly added, uniquely named request in dispatch-requests/ can dispatch.
Never dispatch from a workflow-file edit or retry of an old bridge run.
"""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

# Template is inert until its *own* project explicitly enables a reviewed configuration.
CONFIG_PATH = Path(__file__).resolve().parent.parent / "dispatch-bridge.config.json"
CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
WORKFLOW_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+\.yml$")
if (not isinstance(CONFIG, dict) or
        set(CONFIG) != {"version", "enabled", "actions_repo", "php", "astro"}):
    raise RuntimeError("Invalid project dispatch bridge config")
if (CONFIG["version"] != 1 or type(CONFIG["enabled"]) is not bool or
        not isinstance(CONFIG["actions_repo"], str) or
        not REPO_PATTERN.fullmatch(CONFIG["actions_repo"])):
    raise RuntimeError("Unsupported dispatch config version or repository")
for name, fields in {
    "php": {"workflow", "source_repo", "source_branch", "ref", "inputs"},
    "astro": {"workflow", "source_repo", "source_branch", "event_type", "client_payload"},
}.items():
    value = CONFIG[name]
    if not isinstance(value, dict) or set(value) != fields:
        raise RuntimeError("Invalid " + name + " target config")
    if (not isinstance(value["source_repo"], str) or
            not REPO_PATTERN.fullmatch(value["source_repo"]) or
            not isinstance(value["workflow"], str) or
            not WORKFLOW_PATTERN.fullmatch(value["workflow"])):
        raise RuntimeError("Invalid source repository or workflow")
    if value["source_branch"] != "master":
        raise RuntimeError("Only master source branch is supported")
if (CONFIG["php"]["ref"] != "main" or
    CONFIG["php"]["inputs"] != {"confirm": "DEPLOY_PHP"} or
    CONFIG["astro"]["event_type"] != "wp_trigger_build" or
    not isinstance(CONFIG["astro"]["client_payload"], dict) or
    set(CONFIG["astro"]["client_payload"]) != {"site_domain"} or
    not isinstance(CONFIG["astro"]["client_payload"]["site_domain"], str)):
    raise RuntimeError("Invalid project production dispatch contract")
ACTIONS_REPO = CONFIG["actions_repo"]
TARGETS = {
    "workflow_dispatch": {
        **CONFIG["php"], "event": "workflow_dispatch",
        "max_seconds": 23 * 60,
    },
    "repository_dispatch": {
        **CONFIG["astro"], "event": "repository_dispatch",
        "max_seconds": 63 * 60,
    },
}
PATH_PATTERN = re.compile(r"^dispatch-requests/[0-9]{8}T[0-9]{6}Z-[a-z0-9-]{5,48}\.json$")
SHA_PATTERN = re.compile(r"^[a-f0-9]{40}$")
ACTIVE = {"queued", "in_progress", "pending", "waiting", "requested"}


class BridgeError(RuntimeError):
    pass


def valid_request(doc: object) -> dict:
    if not isinstance(doc, dict) or set(doc) != {"action", "source_sha", "reason", "request_id"} | ({"inputs", "ref", "workflow"} if doc.get("action") == "workflow_dispatch" else {"event_type", "client_payload"}):
        raise BridgeError("Request schema does not match the supported action")
    action = doc["action"]
    if action not in TARGETS or not isinstance(doc["request_id"], str):
        raise BridgeError("Unsupported dispatch action or request ID")
    if not re.fullmatch(r"[0-9]{8}T[0-9]{6}Z-[a-z0-9-]{5,48}", doc["request_id"]):
        raise BridgeError("Invalid request ID")
    if not isinstance(doc["reason"], str) or not (10 <= len(doc["reason"]) <= 160):
        raise BridgeError("A meaningful, short reason is required")
    if not isinstance(doc["source_sha"], str) or not SHA_PATTERN.fullmatch(doc["source_sha"]):
        raise BridgeError("An exact, 40-character source_sha is required")
    if action == "workflow_dispatch":
        if (doc["workflow"] != TARGETS[action]["workflow"] or
                doc["ref"] != TARGETS[action]["ref"] or
                doc["inputs"] != TARGETS[action]["inputs"]):
            raise BridgeError("PHP workflow, branch or confirmation does not match the release contract")
    else:
        if (doc["event_type"] != TARGETS[action]["event_type"] or
                doc["client_payload"] != TARGETS[action]["client_payload"]):
            raise BridgeError("Astro production event and site domain must match exactly")
    return doc


def new_request_from_push(before: str, after: str, run_attempt: str,
                          git=None, root: Path = Path(".")) -> dict | None:
    if run_attempt != "1":
        raise BridgeError("A rerun may re-dispatch: create a NEW approved request instead")
    if not SHA_PATTERN.fullmatch(before or "") or not SHA_PATTERN.fullmatch(after or ""):
        raise BridgeError("Push commit identities are required; refusing ambiguous events")
    if git is None:
        git = lambda args: subprocess.check_output(["git", *args], text=True)
    rows = git(["diff", "--name-status", "--no-renames", before, after]).splitlines()
    candidate_rows = [r for r in rows if r.split("\t", 1)[-1].startswith("dispatch-requests/")]
    if not candidate_rows:
        return None   # Genuine code/workflow changes should NEVER trigger a deploy.
    if len(rows) != 1 or len(candidate_rows) != 1:
        raise BridgeError("Dispatch must be a single, newly added request file, no other modifications")
    parts = candidate_rows[0].split("\t")
    if len(parts) != 2 or parts[0] != "A" or not PATH_PATTERN.fullmatch(parts[1]):
        raise BridgeError("Only a newly added, unique dispatch request is allowed")
    path = root / parts[1]
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 8192:
        raise BridgeError("Request must be a small regular JSON file")
    try:
        doc = valid_request(json.loads(path.read_text(encoding="utf-8")))
    except (ValueError, UnicodeError) as exc:
        raise BridgeError("Invalid JSON request") from exc
    if parts[1] != "dispatch-requests/" + doc["request_id"] + ".json":
        raise BridgeError("Request filename must equal request_id")
    return doc


class GitHub:
    def __init__(self, actions_token: str, source_token: str):
        if not actions_token or not source_token:
            raise BridgeError("Existing github.token and SOURCE_REPO_PAT are required")
        self.actions_token = actions_token
        self.source_token = source_token

    def api(self, method: str, path: str, *, data=None, source=False):
        token = self.source_token if source else self.actions_token
        payload = json.dumps(data, separators=(",", ":")).encode() if data is not None else None
        req = Request("https://api.github.com" + path, data=payload, method=method,
                      headers={
                          "Authorization": "Bearer " + token,
                          "Accept": "application/vnd.github+json",
                          "X-GitHub-Api-Version": "2022-11-28",
                          **({"Content-Type": "application/json"} if data is not None else {}),
                      })
        try:
            with urlopen(req, timeout=20) as resp:
                if resp.status == 204:
                    return None
                return json.load(resp)
        except HTTPError as exc:
            raise BridgeError(f"GitHub {method} {path.split('?')[0]} HTTP {exc.code}") from None
        except (URLError, TimeoutError, ValueError) as exc:
            raise BridgeError(f"GitHub {method} {path.split('?')[0]} transport failure: {type(exc).__name__}") from None

    def source_head(self, repo: str, branch: str = "master") -> str:
        return self.api("GET", f"/repos/{repo}/git/ref/heads/{quote(branch)}", source=True)["object"]["sha"]

    def runs(self, workflow: str):
        path = f"/repos/{ACTIONS_REPO}/actions/workflows/{quote(workflow)}/runs?per_page=50"
        return self.api("GET", path).get("workflow_runs", [])

    def run(self, run_id: int):
        return self.api("GET", f"/repos/{ACTIONS_REPO}/actions/runs/{run_id}")

    def run_jobs(self, run_id: int):
        return self.api("GET", f"/repos/{ACTIONS_REPO}/actions/runs/{run_id}/jobs?per_page=100")["jobs"]

    def post(self, doc: dict):
        if doc["action"] == "workflow_dispatch":
            return self.api("POST",
                f"/repos/{ACTIONS_REPO}/actions/workflows/{doc['workflow']}/dispatches",
                data={"ref": doc["ref"], "inputs": doc["inputs"]})
        return self.api("POST", f"/repos/{ACTIONS_REPO}/dispatches",
            data={"event_type": doc["event_type"],
                  "client_payload": doc["client_payload"]})


def execute(doc: dict, gh: GitHub, *, sleeper=time.sleep) -> dict:
    doc = valid_request(doc)
    if not CONFIG["enabled"]:
        raise BridgeError("Template bridge is disabled; bind the project first")
    target = TARGETS[doc["action"]]
    current = gh.source_head(target["source_repo"], target["source_branch"])
    if current != doc["source_sha"]:
        raise BridgeError(f"Source master changed: expected {doc['source_sha']}, actual {current}; refusing wrong release")
    pre = gh.runs(target["workflow"])
    if any(r.get("status") in ACTIVE for r in pre):
        raise BridgeError("Target workflow is already active; do not dispatch duplicate")
    before_ids = {r["id"] for r in pre}
    started = dt.datetime.now(dt.timezone.utc)
    print(f"DISPATCH_PREFLIGHT=PASS action={doc['action']} source_sha={current}", flush=True)
    # POST only once. If response is lost, do NOT retry and risk double deployment.
    gh.post(doc)
    print("DISPATCH_REQUEST_ACCEPTED=YES (not yet deployment success)", flush=True)
    locked = None
    for _ in range(25):
        runs = gh.runs(target["workflow"])
        candidates = []
        for run in runs:
            if run.get("id") in before_ids or run.get("event") != target["event"]:
                continue
            created = dt.datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
            if created >= started - dt.timedelta(seconds=15):
                candidates.append(run)
        if len(candidates) > 1:
            raise BridgeError("Multiple matching runs: cannot safely correlate to dispatch")
        if len(candidates) == 1:
            locked = candidates[0]
            break
        sleeper(8)
    if not locked:
        raise BridgeError("Dispatch was accepted but a unique new run could not be located")
    run_id = locked["id"]
    print(f"DISPATCH_RUN_LOCKED={locked.get('html_url')} run_id={run_id}", flush=True)
    deadline = time.monotonic() + target["max_seconds"]
    while time.monotonic() < deadline:
        run = gh.run(run_id)
        if run.get("status") == "completed":
            break
        sleeper(15)
    else:
        raise BridgeError(f"Timed out waiting for run {run_id}")
    if run.get("conclusion") != "success":
        raise BridgeError(f"Production target run {run_id} ended {run.get('conclusion')}")
    jobs = gh.run_jobs(run_id)
    if not jobs or any(job.get("conclusion") != "success" for job in jobs):
        raise BridgeError(f"Run {run_id} has non-successful jobs")
    print(f"DISPATCH_TARGET_RUN=SUCCESS run_id={run_id}", flush=True)
    return {"action": doc["action"], "run_id": run_id, "url": run.get("html_url"),
            "source_sha": current, "target_jobs": [j["name"] for j in jobs],
            "status": "TARGET_RUN_SUCCESS_NOT_LIVE_QA"}


def configured_client_host(env_file: str) -> str:
    from urllib.parse import urlsplit
    values = []
    for line in env_file.splitlines():
        match = re.fullmatch(r'\s*(?:export\s+)?WC_URL_CLIENT\s*=\s*(.*?)\s*', line)
        if match:
            values.append(match.group(1).strip().strip("\"'"))
    if len(values) != 1:
        raise BridgeError("Expected exactly one WC_URL_CLIENT in ENV_FILE")
    url = urlsplit(values[0])
    if (url.scheme != "https" or not url.hostname or url.username or url.password or
            url.port not in (None, 443) or url.path not in ("", "/") or
            url.query or url.fragment):
        raise BridgeError("Invalid configured frontend HTTPS origin")
    return url.hostname


def main() -> int:
    before = os.environ.get("BEFORE_SHA", "")
    after = os.environ.get("GITHUB_SHA", "")
    try:
        if os.environ.get("GITHUB_REPOSITORY") != ACTIONS_REPO or os.environ.get("GITHUB_EVENT_NAME") != "push":
            raise BridgeError("Only push on the approved Actions repository is allowed")
        doc = new_request_from_push(before, after, os.environ.get("GITHUB_RUN_ATTEMPT", ""))
        if doc is None:
            print("NO_DISPATCH_REQUEST: workflow/script update only")
            return 0
        if not CONFIG["enabled"]:
            raise BridgeError("Template bridge not activated by reviewed project config")
        if doc["action"] == "repository_dispatch":
            expected_host = configured_client_host(os.environ.get("ENV_FILE", ""))
            if (doc["client_payload"]["site_domain"] != expected_host or
                    expected_host.endswith(".invalid")):
                raise BridgeError("Requested host disagrees with WC_URL_CLIENT")
        gh = GitHub(os.environ.get("GH_TOKEN", ""), os.environ.get("SOURCE_REPO_PAT", ""))
        result = execute(doc, gh)
        print(json.dumps(result, sort_keys=True))
        return 0
    except BridgeError as exc:
        print(f"DISPATCH_BRIDGE_FAIL={exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
