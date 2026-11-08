# ChatGPT — latest response

- Date: 2026-11-08 (Asia/Ho_Chi_Minh)
- Project: Template (`ngocnhanvo/template-astro`, `ngocnhanvo/template-php`)
- Scope: reusable Visual Builder improvements from PTSCPS
- Status: SOURCE_COMMITTED, PRODUCTION_NOT_DEPLOYED

## Verified source commits

1. `template-astro/master` `03ec40b10213e647fef6afe932d67c4bd2103cfc`: retained ESC Table `sourceRow` and `sourceType` through API expansion; transmitted rendered table version and section/description coordinates.
2. `template-php/master` `70982601448605c1f918b85ca9267142802c1204`: exact cell coordinate selection, verified native row, optimistic table version checks, and safe CTA link editors. The source gate ran PHP validation before committing.
3. `template-astro/master` `757424a16e822f8c032ff96f96230baff766d6af`: restored `home_02` first-row source selection and bound `home_01` gallery heading to section-title metadata.

## Boundaries and follow-up

- PTSCPS was read-only reference; no PTSCPS repository or CMS writes.
- Existing Template generic ESC API (`meta.api`) reused; do not copy PTSCPS-specific `home_05` news component, business content, CSS, static table mappings or locale allowlists.
- `normal` mode: no PHP FTP upload and no Astro production build were triggered. Source commits are not deployed QA.
- Production Visual Builder has not been tested against a deployed Template instance. For deployment use a separately authorized production release and Playwright Save/reload QA.
- Older request `20261108-template-api-config-02` was submitted in another conversation, but no commit for it was observed in `template-php/master` at this checkpoint. Avoid treating it as complete or resubmitting blindly.

**Chế độ code:** normal
**Cổng ghi source:** source-commit-actions (chưa có giá trị)
