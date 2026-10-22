#!/usr/bin/env python3
"""Read-only deploy pipeline contract check, independent of a tenant or domain."""
from pathlib import Path

w = Path(".github/workflows/template-production-deploy.yml").read_text(encoding="utf-8")
php = Path("source-php/template-unzip.php").read_text(encoding="utf-8")
ready = Path("source-php/template-unzip-v2.ready").read_text(encoding="utf-8").strip()
seo = Path("source-astro/scripts/sync-seo-files.mjs").read_text(encoding="utf-8")
client = Path("scripts/template-remote-unzip.py").read_text(encoding="utf-8")
ftp = Path("scripts/template-resumable-ftp.sh").read_text(encoding="utf-8")
revision = Path("scripts/template-published-sitemap-revision.py").read_text(encoding="utf-8")
for value in ("repository_dispatch:", "types: [wp_trigger_build]", "ngocnhanvo/template-actions",
              "ngocnhanvo/template-astro", "ref: master", "pnpm run build-git",
              "scripts/template-remote-unzip.py verify", "scripts/template-remote-unzip.py unpack",
              "template-staging-build.json", "ASTRO_FTP_TARGET", "FTP_ASTRO_DIR"):
    assert value in w, "Missing controlled build contract: " + value
assert "\\n  workflow_dispatch:" not in w, "Build can only be initiated by WordPress"
for value in ("VCS_GH_ACTIONS_TOKEN", "get_site_domain", "template-astro.zip",
              "template-staging-build.json", "X_ESC_DEPLOY_TIMESTAMP", "X_ESC_DEPLOY_SIGNATURE"):
    assert value.lower() in php.lower(), "Missing signed deploy protection: " + value
assert "!defined('VCS_GH_REPO')" in php and "trim(VCS_GH_REPO) === ''" in php, "Deploy routing must be supplied by wp-config.php"
assert "VCS_GH_REPO !==" not in php, "Unzip endpoint must not bind to a repository name"
assert "hash_equals($expected, $signature)" in php and "get_site_domain" in php, "Do not weaken signing or destination checks"
assert ready == "TEMPLATE_ASTRO_UNZIP_PROTOCOL=2"
assert "/template-unzip.php" in client and "TEMPLATE_ASTRO_UNZIP_PROTOCOL=2" in client
assert "template-astro.zip" in ftp
assert "TEMPLATE_PUBLISHED_SITEMAP_REVISION" in revision
assert "TEMPLATE_PUBLISHED_SITEMAP_REVISION" in seo
assert ".template-sitemap-deploy-state.json" in seo
for body in (w,php,client,ftp,revision):
    for old in ("psevn-actions","psevn-astro","psevn-php","nghiencuukhoahoc.webnvn.com"):
        assert old not in body, old
# Guard the shared Agent against customer-branded responses and old server paths.
agent_root = Path("source-php/wp-content/mu-plugins/esc-agent/src")
for relative in (
    "Core/Planner.php",
    "Core/AgentSynthesisPrompt.php",
    "Core/ConversationIntentResolver.php",
    "Core/EscAgentLogger.php",
    "Skills/CompanySkill.php",
    "Skills/ProductSkill.php",
    "Skills/ProductDetailSkill.php",
    "Skills/ProductCompareSkill.php",
    "Skills/PromotionSkill.php",
    "Skills/PolicySkill.php",
):
    agent_source = (agent_root / relative).read_text(encoding="utf-8").lower()
    for forbidden in ("blue sea", "/home/xuongmunon", "nón/mũ bảo hiểm"):
        assert forbidden not in agent_source, "Customer-specific Agent dependency: " + relative

print("TEMPLATE_WP_CONTROLLED_DEPLOY_CONTRACT=PASS (no build or upload)")
