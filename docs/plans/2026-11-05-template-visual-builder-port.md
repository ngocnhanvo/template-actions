# Visual Builder PSE -> Template source port — 2026-11-05

## Authorized result
Port the six feature groups already reviewed with owner: native Header menu editing; scoped Footer Info/Media/Table editing; flexible safe ESC Table text/HTML editing; exact row/field selection and mixed image/text protection; generic safe preview controls; editable/readonly/unsupported cues. Preserve Template public layout, menu structure/links and existing content. No PSE branding, table IDs, database, origins or fallback domain may be copied.

## Source / target and release
Target template-php/master bfd7037b454165dd2c558d2ab1894a903aa4e4b8, template-astro/master 131f0f21911cab696c818691c3c278da9c8865f3, template-actions/main 19ac73f51daa969476aff6b0ac2a86c0a1bb7962. PSE reference PHP 092068dff4e7e69b8f9e5f7022cf56507f20696e and Astro c5cd00625ac74d0b889726b5e9ccf1f5aeb32dc9. Source only in normal mode: no FTP, CMS changes or Astro build. Publish through source-commit-actions only, exact HEAD/path allowlists.

## Shared contracts
1. Keep PSE esc-builder/v1 route names and postMessage types for menu/footer/text adapters. Retain ticket, user, capability, nonce, version/hash, post-save readback and rollback. Existing template menu theme helpers esc_pse_* are present and shared; do not rename or rewrite theme plumbing.
2. Footer Info resolves the actual Page ACF product_lang (including configured non-vi/en languages), no silent cross-language write. Fields stay the native Info ACF fields. Frontend source annotations exist only in escBuilderPreview.
3. Footer assets are selected by explicit native ESC Table metadata component=FooterAssets (case-insensitive), under the existing public pub_ namespace. No pub_footer_assets_* hardcode. Exact six-column schema group,label,image,value,href,visible. Require a UNIQUE candidate in the requested language; no fallback across languages. TablePress default language contract: IDs with >=2 underscores ending _en -> en; all other IDs -> vi. No matching/ambiguous table => readonly/unavailable, never guessed. Existing native TablePress edit capability still required.
4. Expose and use the already returned table JSON component field. Frontend readFooterAssets(tables,language) uses the SAME selector, emits original rowIndex and retains hidden rows in Builder only so a hidden row can be shown again. Public rendering excludes invisible rows. Groups certification,responsible,credit match PSE; certification images are processed image objects with ALT, written only through native Insert Image.
5. Keep Template Footer layout/styles. Add only preview source tags to existing Info elements. Adapt preview DOM patching to explicit [data-esc-vb-footer-value] spans as well as PSE dd. Fix current Template linkbocongthuong -> actual WPInfo linkBocongthuong field for binding correctness. Optional FooterAssets component renders configured rows only; absent config leaves current Footer unchanged.
6. Menu components get preview-only native item IDs; retain Template native new-tab click handling and current public design. No copying PSE Header/Footer theme or menu content/order.

## Tasks / evidence
- [x] PHP port + standalone source/capability/version/mixed-cell/HTML/footer selector tests.
- [x] Astro port + source markers, portable assets helper, exact selection and safe controls; preserve existing public components.
- [ ] Offline PHP/Vitest/DOM/browser contracts in separate CI, never production build pipeline; compare independent reference fixtures and retain current target public layout.
- [x] Fresh code review, fix concrete issues, run full appropriate suites.
- [ ] Publish PHP then Astro through central source validation, verify SHAs, save final checkpoint and any deployment limits.

## Review corrections
- Verified rollback readback for Footer Info, BCT Media and native Menu; never claim restore when it failed.
- Keep exact PHP/Astro Footer schema/row limits and empty rows selectable privately.
- Preserve native Template slider arrows with preview-only control opt-in.
- Overlay one ticket-verified native Footer grid and bind row selection to its whole-table version; reject stale row order with 409.
- Keep existing public mixed-image transformation; protect mixed native cells at the write boundary.

## Validation boundary
Local: 73 Visual Builder Vitest cases and 8 Astro compiler transforms passed. Runtime PHP and complete Astro suites are validated on the exact central-runner checkout before source commits. Offline Chromium uses actual source guards with independent synthetic fixtures, no site requests or CMS writes. Logged-in live WordPress/ACF/TablePress integration and production rendering are a separate release check and are not claimed by source CI.
