#!/usr/bin/env python3
"""Read-only source contract checks for the WordPress-controlled build trigger."""
from pathlib import Path
import os

root = Path(os.environ.get("TEMPLATE_PHP_SOURCE", "source-php"))
trigger = (root / "wp-content/plugins/github-trigger/vcs-build-trigger.php").read_text(encoding="utf-8")
config = (root / "wp-content/mu-plugins/esc-github-trigger-config.php").read_text(encoding="utf-8")
assert "get_site_domain()" in trigger
assert "defined('VCS_GH_REPO')" in trigger
assert "wp_trigger_build" in trigger
assert "VCS_GH_ACTIONS_TOKEN" in trigger
assert "psevn-actions" not in trigger + config
assert "nghiencuukhoahoc" not in trigger + config
assert "define('VCS_GH_REPO'" not in config, "Routing must live in wp-config.php"
print("TEMPLATE_WORDPRESS_BUILD_TRIGGER=PASS; NO_BUILD=PASS")
