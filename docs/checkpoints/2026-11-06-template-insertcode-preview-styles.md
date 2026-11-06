# Template — ESC Table Insert Code preview styles (2026-11-06)

Status: SOURCE_READY + NATIVE_EDITOR_QA_PASS. Hosting unchanged. Code mode: normal.

## Cause and change

Both native Insert Code (`inc/tablepress/html.php`) and the context-menu
replacement builder (`inc/tablepress/wysiwyg.php`) emitted preview-only inline
styles on the wrapper and image. These styles became saved page HTML.

- Both builders now emit classes, table ID, one shortcode badge and intrinsic
  image dimensions, without `style` or `data-mce-style` attributes.
- Preview layout stays in TinyMCE `content_style`, including initially empty
  editors before the first insertion. Width fits the editor; height remains
  proportional to the image. Existing per-table aspect-ratio CSS is retained.
- The WordPress `content_save_pre` hook removes old preview style attributes
  with the real `WP_HTML_Tag_Processor`. It honors the slashed input/output
  contract using `wp_unslash`/`wp_slash`, returning the original input on a no-op.
  Unrelated editorial HTML/styles, literal script text, IDs, shortcodes and
  image dimensions are preserved. It does not rewrite existing database rows
  until those pages are normally saved after the PHP fix is deployed.

## Source and validation

- PHP `ngocnhanvo/template-php@master`: base
  `3b178876a0821f0e1c619528e462a8a3bf9de162`, published
  `baa1ed583e14b27c9cdc6278b6c5b66ba734f8b4`. Four reviewed file blobs match.
- PHP source gate [42227044039](https://github.com/ngocnhanvo/source-commit-actions/actions/runs/42227044039): PASS.
  Three changed PHP files pass `php -l`. Native Insert/Replace JS, actual
  WordPress HTML processor/formatting functions, slashed save round-trip,
  backslash/style preservation, idempotence and empty-editor CSS checks pass.
  The native Node regression was RED on the original inline-style output and
  GREEN after the fix. Tests use no DB or live WordPress session.
- Read-only independent review found no remaining Critical/Important issue.
- QA source `4978af61c3ec48dc405dc950589bfc5d22053833` extends the existing offline
  browser suite; no duplicate workflow or production build step was added.
- Final QA source gate [42229005290](https://github.com/ngocnhanvo/source-commit-actions/actions/runs/42229005290): PASS.
- Browser [42229033616](https://github.com/ngocnhanvo/template-actions/actions/runs/42229033616): PASS for desktop 1440x900 and mobile 390x844. It uses the actual shipped WordPress TinyMCE core, modern theme, noneditable plugin and lightgray skin. Both native preview builders retain exactly one shortcode, serialize/reload without preview style attributes, and fit a 300px editor with the correct image ratio. Visible iframe/image assertions and screenshots are included. Mobile screenshot was inspected and shows the preview and one badge correctly.
- Browser result records PHP `baa1ed583e14b27c9cdc6278b6c5b66ba734f8b4` and the unchanged Astro `0291d7d5640def31f9ee0d29328ed829fd44397b`. Artifact `template-visual-builder-preview-contract` ID 13507102616 contains screenshots/result.json; no credentials or real customer content.
- Initial browser fixture run 42227539884 failed because TinyMCE 4 could not bootstrap at an opaque about:blank URL. The corrected fixture serves a routed synthetic origin. Later visual review also required loading the actual native skin and asserting visible content; the final run above covers both. These were fixture corrections, not further PHP source changes.
- No live WordPress login/save or production rendering is claimed by these offline checks. Do not rerun passing gates/browser jobs without another relevant change.

## Release boundary

No PHP FTP upload, live content cleanup, Astro build or production deployment
was authorized or performed. This editor fix needs the two changed theme PHP
files on the Template WordPress host; it does not require an Astro build.
Existing live content gets preview styles removed on its next normal save.
Do not rerun the earlier completed Visual Builder port or its source gates.
