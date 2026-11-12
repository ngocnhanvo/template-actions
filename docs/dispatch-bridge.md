# GitHub-only Dispatch Bridge — Template reusable source

This **is not MCP** and does not replace a production deploy pipeline.
It is a control-plane workflow in each project's own `-actions` repository
using ordinary authenticated GitHub source commits from the existing ChatGPT
GitHub connector.

## Bootstrap in a new project

1. Inherit from `ngocnhanvo/template-actions@main` the files
   `.github/workflows/dispatch-bridge.yml`, `scripts/dispatch-bridge.py`,
   `scripts/test_dispatch_bridge.py`, `dispatch-bridge.config.json` and this guide.
   **Do not copy any request files from another project.**
2. Review the **actual** app source/action repo names and branches and the
   existing PHP and Astro workflow IDs. Edit all values in the project-owned
   `dispatch-bridge.config.json`, including the frontend site host.
   Set the config `actions_repo` to the exact destination repo. The sample
   `template.example.invalid` is deliberately inoperative.
3. Confirm the repo's Actions `main` branch, `SOURCE_REPO_PAT` and `ENV_FILE`
   secrets, and existing PHP/production workflows. The GitHub runner's
   `github.token` requires `actions:write` and `contents:write` for the
   dispatch job. No tokens are copied between repositories.
4. Keep `"enabled": false` during import, commit and verify offline tests pass.
   Once the mappings are approved, enable it in a **separate reviewed commit**
   and run test-only validation first. Do not combine config changes with a
   production request.
5. Only after the project's applicable authorization (`auto-build` for Astro)
   create a **new, unique request file in its own repo**, through the standard
   connected GitHub tool.

### PHP deployment request (workflow_dispatch)

```json
{
  "action": "workflow_dispatch",
  "request_id": "20261113T010000Z-approved-php-release",
  "source_sha": "<40-hex-current-php-master-sha>",
  "reason": "Deploy the reviewed WordPress PHP code to the approved production",
  "workflow": "<actual-project-php-release.yml>",
  "ref": "main",
  "inputs": { "confirm": "DEPLOY_PHP" }
}
```

### Astro deployment request (repository_dispatch)

```json
{
  "action": "repository_dispatch",
  "request_id": "20261113T020000Z-approved-astro-release",
  "source_sha": "<40-hex-current-astro-master-sha>",
  "reason": "Deploy the reviewed Astro build after PHP release succeeded",
  "event_type": "wp_trigger_build",
  "client_payload": { "site_domain": "<host-from-WC_URL_CLIENT>" }
}
```

The file name MUST be exactly
`dispatch-requests/<request_id>.json`.
Example timestamps and identifiers are illustrative; don't reuse them.
Every request is a real audited production action, not a dummy commit.

## Enforcement & acceptance

- A newly added, unique JSON request in a **single-file push** only; no
  workflow/script/config changes mixed with release requests
- `run_attempt=1`; do not rerun an old request/job to trigger another deployment
- Config explicit `enabled=true`, exact destination `GITHUB_REPOSITORY`
- Workflow ref/inputs, event/payload, repo and source SHA must match approved config
- On Astro dispatch, host must also match the HTTPS `WC_URL_CLIENT` parsed from
  existing `ENV_FILE` secret
- No active target run, record prior run IDs; POST exactly once and lock a unique
  target run; read status and job conclusions
- `DISPATCH_REQUEST_ACCEPTED` is NOT build PASS; target job success is
  not proof of signed activation or browser QA. Preserve existing target
  production provenance, rollback/locking, and live browser verification
- No arbitrary API endpoint, token sharing, or extra deploy workflow
- Source `master` may move between preflight and checkout: read target job
  provenance to verify **the exact** source SHA actually deployed.

The bridge is project-parameterized. Clone and verify the configuration using
the destination project's own credentials, exact workflow IDs and run logs.
