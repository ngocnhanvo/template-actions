# Template Visual Builder PSE port — 2026-11-05

Status: SOURCE_READY + OFFLINE_BROWSER_CONTRACT_PASS; not deployed.

Scope: six reusable feature groups requested by owner: native Header menu editing, Footer Info/Media/global ESC Table editing, flexible safe text/HTML fields, exact cell selection, safe native preview controls, and editability cues. Preserve Template public content, classes/menu layout, new-tab handling and existing public image transformation.

## Source and review
- PSE reference: psevn-php/master `092068dff4e7e69b8f9e5f7022cf56507f20696e`; psevn-astro/master `c5cd00625ac74d0b889726b5e9ccf1f5aeb32dc9`. Reference repositories were read only.
- Template PHP base `bfd7037b454165dd2c558d2ab1894a903aa4e4b8`; published `3b178876a0821f0e1c619528e462a8a3bf9de162`.
- Template Astro base `131f0f21911cab696c818691c3c278da9c8865f3`; published `0291d7d5640def31f9ee0d29328ed829fd44397b`.
- All target writes use source-commit-actions with exact base SHA and path allowlist. No bypass.
- Independent source review found no remaining Critical/Important issue after corrections to rollback verification, native carousel compatibility, exact Footer schema, empty rows, and private Footer snapshot/version freshness.

## Evidence
- PHP source gate [42057842728](https://github.com/ngocnhanvo/source-commit-actions/actions/runs/42057842728): PASS. All 26 changed PHP files passed php -l; 11 standalone test entrypoints passed, including generated inspector JavaScript syntax, ticket renewal, authorization, exact source/row/field, safe HTML/image preservation, optimistic versioning and rollback failure reporting. In-memory mocks only; no live CMS write.
- Local focused Astro suite: 73/73 PASS, 9 files. All 8 modified/new Astro components passed compiler transform; no app build.
- Full Astro gate [42058088150](https://github.com/ngocnhanvo/source-commit-actions/actions/runs/42058088150): PASS, 188 tests in 28 files. Source was published only after this completed.
- Template Actions QA source `53241f7289c1476c830e6e1f0b149738da91ce45`, published through central source gate [42058382617](https://github.com/ngocnhanvo/source-commit-actions/actions/runs/42058382617): PASS.
- Offline Chromium [42058416954](https://github.com/ngocnhanvo/template-actions/actions/runs/42058416954): PASS for desktop 1440x900 and mobile 390x844. Actual source Header/Footer/preview/editability guards, exact table+row+version selection, readonly paths and native controls passed. Asserted zero external/API requests, zero navigation and one tab. No site or WordPress login was used.
- Browser log recorded Astro `0291d7d5640def31f9ee0d29328ed829fd44397b` and PHP `3b178876a0821f0e1c619528e462a8a3bf9de162`, matching the intended published sources. Artifact `template-visual-builder-preview-contract` (ID 13430935071) contains four editable/readonly desktop/mobile screenshots plus result.json; expires 2027-02-03.
- 52 changed PHP/Astro file blobs were checked against the reviewed local sources; the original no-final-newline convention in getData.ts was retained. No additional source tests or deployments are pending under the authorized source-only scope. Do not rerun the successful gates or offline browser job without a new relevant change.
- PHP request v1 was an envelope only, never marked READY. v2 stopped before publishing on an obsolete static-config test assumption; v3 stopped on a missing generated fixture path. v4 is the successful request above. No source commit was made by failed requests.

## Deployment boundary
Chế độ code: normal. CODE/SOURCE validation is separate from live release. No PHP FTP upload, WordPress content edit, Astro build or deploy was authorized or performed. Live WordPress/ACF/TablePress hooks, real authenticated save/cancel flows and deployed UI parity remain release checks. Deploy the matching PHP/Astro halves together only with approval.

## Configuration
- Require the actual project ESC_VISUAL_BUILDER_ASTRO_URL; there is no copied PSE fallback domain.
- Global assets are optional and selected by native public pub_ ID + component=FooterAssets, exact language, exact six-column schema. Nothing creates/replaces Template customer content.
- Footer preview overlays one current, ticket-verified native grid and its whole-table version. Later native reorder/edit rejects selection with 409 rather than selecting a different row at the old index.
- Images in global Footer ESC Table remain native Insert Image; Info BCT uses an existing Media Library ID.

Previous FTPS optimization checkpoint is separate: docs/checkpoints/2026-11-05-template-ftps-delta.md. Do not redo its source/CI or assume its PHP deployment was approved.
