# Template FTPS delta sync — 2026-11-05

## Approved scope and design
Port the existing PSE image/static delta transport into Template. Keep Template's dynamic WordPress/frontend destinations, signed protocol v2, SHA-256 verification, staging/rollback, sitemap Save revision and WordPress-controlled Astro build unchanged. Reuse only compiled public client images and HTML/CSS/JS/JSON with identical signed size/hash; server output, client/index.html and SEO metadata remain outside static reuse. Old PHP or unavailable supported inventory keeps full ZIP behavior; authentication/identity errors fail closed.

Baseline: template-actions/main 1c459a991259caf74fe56ed28b69a52a47b8c8de; template-php/master d572f477076d2e1f55e716d96e46c54877e3e232. Reference: PSE Actions main 1ef455411c4b3d345e1fbae3da7ef87224f6f1fd; PHP helper blob ff684cd872c208b8d5c8da9fc0e49edd8ac4d21a.

## Implementation plan
- [x] Port image/static PHP helper and standalone contracts; integrate inventory and restoration before activation.
- [x] Port packagers and signed inventory client; retain full ZIP fallback for older PHP.
- [x] Add 4 MiB FTPS socket buffer and overlap lftp preparation with Astro build, preserving error handling.
- [x] Update PHP release allowlist so the helper is installed before its caller; keep FTP deployment manual.
- [ ] Run offline Python/PHP transport contracts and syntax checks; verify cross-language ZIP reconstruction.
- [ ] Publish source through source-commit-actions with exact HEAD/path allowlists; verify remote SHAs and CI.

## Deployment boundary
Code mode normal. Source changes do not deploy PHP or build Astro. Until the PHP endpoint is explicitly deployed, the new Actions packager falls back to the existing full ZIP. Do not trigger production build for benchmarking. Next authorized PHP deployment must include template-image-delta.php before template-unzip.php, then a legitimate WordPress Build Website run can measure reuse and upload duration.

## Port corrections found by review
- Keep `client/images/**` exclusively in image delta, including JSON metadata; otherwise ordered image/static reconstruction can fail when the two inventories overlap. PHP inventory, restoration, packager and client validation use the same disjoint scopes.
- The combined bounded image/static inventory can exceed the upstream 1 MiB read cap. Read up to 4 MiB with explicit oversize failure instead of silently truncating valid JSON. File-count/path/size limits and authentication remain unchanged.
- Retain the PHP protocol's 1 MiB per-marker cap: both packagers measure serialized UTF-8 marker bytes and keep the full ZIP before deleting anything if the marker is too large.

## Status
CODE_READY; local 15 Python tests PASS, YAML/shell/diff checks PASS, independent code review PASS. PHP syntax and standalone image/static contracts PASS in source validation run 42014483112; cross-language validation runs in separate offline CI. FTP PHP and Astro production validation NOT_RUN.

PHP source validation request: `source-commit-actions/requests/20261105-template-pse-ftps-php-delta-01` (no deployment).
