# Template FTPS delta sync — 2026-11-05

## Approved scope and design
Port the existing PSE image/static delta transport into Template. Keep Template's dynamic WordPress/frontend destinations, signed protocol v2, SHA-256 verification, staging/rollback, sitemap Save revision and WordPress-controlled Astro build unchanged. Reuse only compiled public client images and HTML/CSS/JS/JSON with identical signed size/hash; server output, client/index.html and SEO metadata remain outside static reuse. Old PHP or unavailable supported inventory keeps full ZIP behavior; authentication/identity errors fail closed.

Baseline: template-actions/main 1c459a991259caf74fe56ed28b69a52a47b8c8de; template-php/master d572f477076d2e1f55e716d96e46c54877e3e232. Reference: PSE Actions main 1ef455411c4b3d345e1fbae3da7ef87224f6f1fd; PHP helper blob ff684cd872c208b8d5c8da9fc0e49edd8ac4d21a.

## Implementation plan
- [x] Port image/static PHP helper and standalone contracts; integrate inventory and restoration before activation.
- [x] Port packagers and signed inventory client; retain full ZIP fallback for older PHP.
- [x] Add 4 MiB FTPS socket buffer and overlap lftp preparation with Astro build, preserving error handling.
- [x] Update PHP release allowlist so the helper is installed before its caller; keep FTP deployment manual.
- [x] Run offline Python/PHP transport contracts and syntax checks; verify cross-language ZIP reconstruction.
- [x] Publish source through source-commit-actions with exact HEAD/path allowlists; verify remote SHAs and CI.

## Deployment boundary
Code mode normal. Source changes do not deploy PHP or build Astro. Until the PHP endpoint is explicitly deployed, the new Actions packager falls back to the existing full ZIP. Do not trigger production build for benchmarking. Next authorized PHP deployment must include template-image-delta.php before template-unzip.php, then a legitimate WordPress Build Website run can measure reuse and upload duration.

## Port corrections found by review
- Keep `client/images/**` exclusively in image delta, including JSON metadata; otherwise ordered image/static reconstruction can fail when the two inventories overlap. PHP inventory, restoration, packager and client validation use the same disjoint scopes.
- The combined bounded image/static inventory can exceed the upstream 1 MiB read cap. Read up to 4 MiB with explicit oversize failure instead of silently truncating valid JSON. File-count/path/size limits and authentication remain unchanged.
- Retain the PHP protocol's 1 MiB per-marker cap: both packagers measure serialized UTF-8 marker bytes and keep the full ZIP before deleting anything if the marker is too large.

## Status
CODE_READY / OFFLINE_CONTRACTS_PASS. Source updates are complete and verified; PHP FTP deployment and Astro production reuse/speed measurements are NOT_RUN.

- PHP: `ngocnhanvo/template-php@master`, commit `bfd7037b454165dd2c558d2ab1894a903aa4e4b8`.
- Actions implementation: `ngocnhanvo/template-actions@main`, commit `46694781d2370a523ca008ee9ec2787f453d916f`.
- PHP source validation [42014483112](https://github.com/ngocnhanvo/source-commit-actions/actions/runs/42014483112): PASS; PHP syntax, image/static contracts and remote SHA verified.
- Actions source validation [42014709451](https://github.com/ngocnhanvo/source-commit-actions/actions/runs/42014709451): PASS; workflow/shell/Python syntax and remote SHA verified.
- Cross-repo offline CI [42014745102](https://github.com/ngocnhanvo/template-actions/actions/runs/42014745102): PASS; 16 Python tests, both PHP standalone suites, real Python ZIP -> PHP restore, changed-image rejection and preservation of the live fixture. No skipped tests remotely.
- Independent review: PASS after correcting inherited scope/serialized-size issues documented above. No PSE source was modified.

## Next authorized action
In normal mode, obtain owner approval before uploading PHP. Deploy the helper before its endpoint, verify FTPS readback and the signed inventory. A later authorized WordPress Build Website run can measure TEMPLATE_IMAGE_DELTA / TEMPLATE_STATIC_DELTA and actual upload seconds/bytes. Until PHP deployment, the new workflow retains full-ZIP fallback. Do not rerun the already-passed offline contracts or build production solely for a benchmark.
