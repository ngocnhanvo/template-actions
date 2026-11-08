# ChatGPT — latest response

- Date: 2026-11-08 (Asia/Ho_Chi_Minh)
- Project: Template (`ngocnhanvo/template-astro`, `ngocnhanvo/template-php`)
- Scope: Aqua Visual Builder reusable Product management and nested ESC Table child tables inside parent cells
- Status: SOURCE_COMMITTED, SOURCE_GATE_TESTS_PASS, PRODUCTION_NOT_DEPLOYED

## Verified Template source commits

- `template-php/master` `86c9db4252dacaef485f747da237c0f95df4f538` — WooCommerce Product IDs managed only in ESC Table; attributes remain readonly.
- `template-php/master` `27bd8fe7adc08bcc8c5d7aafd2501a0b5f786eba` — Product picker, add/delete/reorder controls.
- `template-php/master` `06e346908ec40eb67a5a919243b7d13bb3072ffc` — remove hardcoded Sale currency fallback.
- `template-astro/master` `c7c3f87fe24cf1c196d26ea4da14baa80f07eea9` — safe Preview interaction guard and Product reference adapters.
- `template-php/master` `ccccada975b2e64945ce58582ec54d715ebf97cc` — bounded Page-owned nested shortcode-* ESC Table discovery and permission; source gate run 42491346637 PASS.
- `template-php/master` `024a9104cad189571025324c65087636191c88c7` — direct red/blue Product visual picking; fallback ID list only if Preview cannot match; source gate run 42491664580 PASS.
- `template-astro/master` `c67a593b99dff312e4bcfbff202871d0886dd191` — authenticated nested Page manifest data-only blocks; direct nested Product selection, add/delete/reorder, source-row tags; source gate run 42492142623 PASS.
- `template-astro/master` `4bf76861ef31a9108b5d1936b8cca38b482a22d7` — fix canonical sourceRow after insertion and notify nested track for pagination; five new nested Product jsdom regression tests; source gate run 42493054136 PASS.
- `template-php/master` `bf7d7b76f6df822359553fb6141a2684e0255278` — standalone PHP nested Page source graph regression: child/grandchild, cycle, isolation, unknown table, depth and 48-table cap; source gate run 42497357672 PASS.
- `template-php/master` `10a10ded0956837ce2d1ddb11b8d86f606eec5db` — keep preselected Product ID on entering visual sort and revalidate against authoritative WordPress rows; source gate run 42497631449 PASS.
- `template-astro/master` `bac0f9476c768c6ce2f8620a99120c43c20f75e0` — explicitly filtered Product tracks can reconcile a subset of ID references without weakening complete-grid validation; 3 Vitest cases; source gate run 42498714261 PASS.
- `template-astro/master` `aeee64c5e6f266b3475af3fa55ffd24828ed9da4` — refuse direct picking when selected Product card is filtered/hidden and reject malformed Product ID mappings; 2 jsdom tests; source gate run 42499865927 PASS.
- `template-astro/master` `f117b819880488432471eee3179c16e19a29172f` — use authoritative WooCommerce price, do not render fictional discount percentages on free/full-priced Product cards; jsdom regression; source gate run 42500089517 PASS.

## Constraints and next steps

- Aqua reference repositories were read-only; no client content, CSS or Home_03 layout copied. Actual project components displaying a child Product ESC Table must render the generic `data-esc-source-table`, `data-esc-builder-product-track`, `data-esc-builder-product-id`, and `data-esc-builder-product-card` mapping and template markup.
- Components showing a filtered subset must declare `data-esc-builder-product-partial="true"` on their Product track; complete grids remain strict by default. This is generic metadata, not an Aqua-specific style/ID.
- Source validation and Vitest PASS do not mean deployed website/browser QA PASS.
- Code mode normal: no FTP PHP upload or Astro production build/deploy authorized. A separate release approval is needed before production Visual Builder Chromium/Playwright, save/readback/reload, mouse/touch and rollback QA.
- Earlier PTSCPS commits 03ec40b, 7098260, 757424a remain intact.

**Chế độ code:** normal
**Cổng ghi source:** source-commit-actions (chưa có giá trị)
**Trạng thái:** PARTIAL — production deployment/browser acceptance pending
