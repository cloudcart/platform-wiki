---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes"
route_name: discounts-code_pro-list
route_path: /admin/marketing-new/discounts/code-pro/:id
aliases: ["Code PRO export", "Export codes", "Download codes CSV", "Експорт на кодове", "Сваляне на кодове"]
tags: [marketing, discounts, code-pro, export, csv]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 3
---

# Code PRO codes export

## Purpose

The **Code PRO codes export** is a one-click CSV download of every code under a Code PRO discount — complete with its discount terms (conditions), date window, usage stats, region, customer-group restriction, and stacking flags. Click "Export" on the [[marketing-discounts-code-pro]] list, the platform streams a UTF-8 CSV directly to the browser, and the merchant gets a single spreadsheet they can:

- **Share with a marketing team** preparing a newsletter / SMS / Viber mailout.
- **Hand to a partner / affiliate** who needs the codes for their own audience (each row = one code with its terms).
- **Archive for accounting** showing which codes were generated, when, with what limits.
- **Re-import / audit** generated batches when the merchant runs many campaigns and needs a per-code history.
- **Verify** that the generator output matches the spec (especially after a [[marketing-discounts-code-pro-generator]] run).

The CSV is **always the entire active codes list** for the chosen Code PRO discount (no per-code filter in the URL) — the filter parameters the listing supports are not applied to the export. Filtering must happen in the merchant's spreadsheet tool after download.

## Where to find it

The Export action is **not its own page or route** — it is a toolbar anchor on the [[marketing-discounts-code-pro]] codes list (route `discounts-code_pro-list`). Click "Export" (the toolbar button labelled with a download icon and the word "Export", to the left of "Create Discount code" and "Generate codes"). The link points to `GET /admin/api/core/discounts/code-pro/{id}/export`, which returns a **streamed CSV response** (the download starts immediately and the page itself isn't replaced). For the full toolbar-anchor behaviour, the absence of any modal, and what the merchant can / cannot do, see [[code-pro-export-overview]].

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[code-pro-export-overview]] — the toolbar anchor (no modal, no format dropdown, no filter pane, no async job); the single direct GET link; what the merchant can and cannot do; the `discount-codes-pro.csv` filename.
- [[code-pro-export-columns]] — the fixed CSV column layout: 16 base columns + 8 columns × 5 condition slots = 56 columns per row; per-column sources; the fewer-than-5 / more-than-5 condition handling.
- [[code-pro-export-format]] — the file-format mechanics: UTF-8 BOM for Excel, leading-space code prefix, UTC ISO 8601 dates, streamed response, `set_time_limit(0)`, 500-per-chunk memory safety.
- [[code-pro-export-business-rules]] — no-filter scope, condition target-type normalisation, semicolon-joined multi-record names, permission scope, and the decoupled (un-gated) plan position.

## What the merchant can do here

- **Export the entire codes list** for the current Code PRO discount in one click.
- **Open the resulting CSV in any spreadsheet tool** (Excel, Google Sheets, LibreOffice Calc, Numbers) — the UTF-8 BOM ensures non-ASCII characters render correctly (see [[code-pro-export-format]]).
- **Sort, filter, slice, pivot** the data in the spreadsheet for marketing operations: which codes have never been used, which ones expire soonest, which belong to a specific influencer's customer group, etc.
- **Feed the codes into a third-party mailout system** (most accept CSV import with column-mapping).

The merchant cannot filter / choose columns / merge multiple discounts before download, and cannot re-import the CSV — see [[code-pro-export-overview]] for the full "cannot do" catalogue.

## Settings & fields

The output is a single fixed-shape file — there are no merchant-adjustable settings on the export itself. The file is named `discount-codes-pro.csv`, served as `text/csv` with a UTF-8 BOM. The column set is fixed (16 base + 56 total columns). See [[code-pro-export-format]] for filename / encoding / header detail and [[code-pro-export-columns]] for the full column reference.

## Business rules

- **One CSV per Code PRO discount, no filter scope** — the export ignores listing-level filters and always emits the full codes list. See [[code-pro-export-business-rules]].
- **Memory-safe + no timeout** — streamed in 500-code chunks with the PHP time limit disabled, so 50,000+ code exports finish without truncation. See [[code-pro-export-format]].
- **Condition "type" carries the target type, not the discount mechanic** — normalised to `all_products` / `order_over` / `free_shipping` / the setting name. See [[code-pro-export-business-rules]].
- **Permission** — inherits the parent Code PRO discount's scope; the standard `marketing.discounts` permission is required.
- **Not separately plan-gated** — any merchant with `discount-code-pro` access can export, regardless of the `discount-code-pro-generator` value (generator and exporter are decoupled). See [[code-pro-export-business-rules]].

## Related

- [[marketing-discounts-code-pro]] — parent list (the "Export" button lives here).
- [[marketing-discounts-code-pro-generator]] — the engine that produces codes; the export is the natural follow-up.
- [[marketing-discounts]] — parent feature.
- [[marketing-discounts-codes]] — Container codes' standard table-export (different surface, not this engine).
- [[discount]] — entity page for the parent Code PRO discount.
- [[discount-code]] — entity page for each exported code.
- [[customers-custom-groups]] — customer-group names referenced in the export (per-code restrictions).
- [[geo-zone]] — geo zone names referenced in the export (per-code restrictions).
- [[products-smart-collections]] — collection names referenced in `Condition i selection`.
- [[products-vendors]] — vendor names referenced in `Condition i vendor`.
- [[products-categories]] — category names referenced in `Condition i category`.
- [[products-products]] — product names referenced in `Condition i product`.

## Open questions

No outstanding questions.
