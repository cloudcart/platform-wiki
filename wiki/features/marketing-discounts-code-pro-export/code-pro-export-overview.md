---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Export → Overview"
route_name: discounts-code_pro-list
route_path: /admin/marketing-new/discounts/code-pro/:id
aliases: ["Code PRO export button", "Export codes button", "Export toolbar anchor", "Бутон Експорт на кодове"]
tags: [marketing, discounts, code-pro, export, csv]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-code-pro-export]]. See the hub for the other aspects (columns, format, business rules).

# Code PRO export — overview & access

## Purpose

This aspect covers **how the Export action is surfaced** and **what the merchant can and cannot do with it**. The Code PRO codes export is a one-click CSV download of every code under a Code PRO discount. There is no configuration step — clicking the button immediately streams the full file to the browser.

## Where to find it

The Export action is **not its own page or route** — it is a toolbar anchor on the [[marketing-discounts-code-pro]] codes list (route `discounts-code_pro-list`). Click "Export" — the toolbar button labelled with a download icon and the word "Export", positioned to the left of "Create Discount code" and "Generate codes".

The link points to `GET /admin/api/core/discounts/code-pro/{id}/export`, which returns a **streamed CSV response** — the download starts immediately and the page itself isn't replaced. The output filename is **`discount-codes-pro.csv`** (served with the standard `Content-Disposition: attachment` header so the browser saves it rather than rendering it). See [[code-pro-export-format]] for the full header / encoding detail.

### No export modal — it's a single direct GET link

Unlike many other exports in the admin (Orders, Customers, Subscribers — all of which open a modal where the merchant picks columns / format / range), the Code PRO export is a **plain anchor** (`<a target="_blank">`) rendered in the codes-list toolbar. There is:

- **No "Format" dropdown** — CSV is the only output.
- **No filter pane** — the filters on the underlying codes list are NOT honoured (see [[code-pro-export-business-rules]]).
- **No date-range scoper.**
- **No async-job indicator, progress bar, or "email me the file" option.**

Clicking the button kicks off an immediate streamed download in a new tab — the merchant sees the browser's standard download UI, with no in-app feedback.

## What the merchant can do here

- **Export the entire codes list** for the current Code PRO discount in one click.
- **Open the resulting CSV in any spreadsheet tool** (Excel, Google Sheets, LibreOffice Calc, Numbers) — the UTF-8 BOM at the start ensures non-ASCII characters in names / values render correctly. See [[code-pro-export-format]].
- **Sort, filter, slice, pivot** the data in the spreadsheet for marketing operations: which codes have never been used, which ones expire soonest, which ones belong to a specific influencer's customer group, etc.
- **Feed the codes into a third-party mailout system** (most accept CSV import with column-mapping).

### What the merchant CANNOT do here

- **Filter the export before download** — the export ignores any UI-level filters the merchant has applied to the [[marketing-discounts-code-pro]] list. The CSV always contains the complete codes list for that discount. See [[code-pro-export-business-rules]].
- **Choose which columns to include** — the column set is fixed (16 base columns + 5 × 8 condition columns = 56 total columns). See [[code-pro-export-columns]].
- **Export multiple Code PRO discounts in one file** — each export is scoped to one discount. To get every Code PRO campaign in the store, the merchant runs the export per discount and merges the files manually.
- **Re-import the CSV via the admin UI** — the export is one-way (CSV out, not in). To re-create codes, use [[marketing-discounts-code-pro-generator]] or the per-code form.
- **Export Container codes via this engine** — this exporter is for Code PRO rows only. Container codes ([[marketing-discounts-codes]]) use the standard table-grid export of their listing.

## Settings & fields

There are no merchant-adjustable settings on the export — clicking the toolbar anchor is the entire interaction. The only "field" exposed is implicit in the URL: the discount `id` segment of `GET /admin/api/core/discounts/code-pro/{id}/export`, which scopes the export to one Code PRO discount. The file shape (filename, encoding, column set) is fixed and documented on [[code-pro-export-format]] and [[code-pro-export-columns]].

## Business rules

- The Export anchor is rendered only in the toolbar slot for the codes-list route — it is not reachable from any other Discounts screen.
- The export is **one-way** and **single-discount** by design (see "cannot do" above).
- Permission and plan-gating are inherited, not export-specific — see [[code-pro-export-business-rules]].

## Related

- [[marketing-discounts-code-pro-export]] — hub.
- [[marketing-discounts-code-pro]] — parent list where the Export button lives.
- [[marketing-discounts-code-pro-generator]] — produces the codes; export is the natural follow-up.
- [[marketing-discounts-codes]] — Container codes' standard table-export (different surface).
- [[marketing-discounts]] — parent feature.
- [[discount]] — entity page for the parent Code PRO discount.

## Open questions

No outstanding questions.
