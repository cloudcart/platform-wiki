---
type: feature
nav_path: "Invoices → Download"
route_name: admin.core.export
route_path: /admin/api/core/export-import/download_invoices
aliases: ["Download invoices", "Bulk invoice download", "Invoice PDF bundle", "Download all invoices", "Изтегляне на фактури", "Изтегли фактури"]
tags: [orders, invoices, download, pdf, zip, 2fa, async, accounting]
plan_gates: ["invoices"]
created: 2026-05-23
updated: 2026-07-29
source_count: 7
---
# Invoices bulk download

## Purpose

The **bulk PDF download** action on [[orders-invoices]] — packages multiple invoice PDFs into a single ZIP archive. Used by merchants doing periodic accounting (monthly / quarterly / annual filing), tax audits, or handover to an external accountant.

In the redesigned Invoices list this is a **single Download button** in the top-right header (calling the `download_invoices` action). There is **no** "Download all (X)" counter and **no** per-row selection. **Current limitation:** the button forwards the list's filter query, but `download_invoices` reads only the legacy `extra.ids` / `extra.dates` parameters — which the new UI no longer sends — so the bundle currently contains **every invoiced order regardless of the applied filter**; the filter scopes only the on-screen list (see [[invoices-download-scope]]).

This page is the **hub** for the bulk-download feature. Each slice is documented in its own aspect page below.

## Sub-pages (in this cluster)

- [[invoices-download-entry-points]] — the single **Download** button, the shared 2FA verification step, and the three response types (`zip` / `queue` / `error`) the frontend handles.
- [[invoices-download-scope]] — what goes into the bundle: currently all invoiced orders (the filter is **not** applied to the download); the filter panel + placement-date note; the empty-scope error.
- [[invoices-download-sync-async]] — the 10-invoice synchronous threshold, the 50-invoice async chunk size, email + alert delivery, bundle retention, and the failure behaviour.
- [[invoices-download-rendering]] — on-demand fresh PDF rendering, filename pattern, the Bulgarian-locale watermark, credit-note exclusion, the `invoicing = no` short-circuit, and bundle retention.
- [[invoices-download-permissions-plan]] — the `invoices.download` permission chain and the `invoices` plan access gate.

## Where to find it

From [[orders-invoices]]:
- **Download** — the top-right header button. There is no date-range picker beside it and no per-row selection. It currently bundles **all** invoiced orders — the applied filter narrows the on-screen list but **not** the bundle (see [[invoices-download-scope]]).

The button opens a 2FA verification step before the download proceeds (when 2FA is active on the admin). See [[invoices-download-entry-points]] for the modal and response handling.

## What the merchant can do here

- Download the invoiced orders as a single ZIP (**Download**) — note it currently covers **all** invoiced orders regardless of the applied filter. See [[invoices-download-scope]].
- Receive small bundles instantly in the browser, or large bundles by emailed link — see [[invoices-download-sync-async]].

### What the merchant CANNOT do here

- Download only specific page ranges of an invoice — invoices are fully-rendered PDFs, not page-selectable.
- Pick a different output format (CSV, XLSX, XML) — this action is PDF-only. For structured exports, see [[orders-invoices-export]].
- Skip 2FA — every bulk download goes through verification when 2FA email is active for the admin (see [[invoices-download-entry-points]]).
- Resume a failed async job — failures require re-running (see [[invoices-download-sync-async]]).
- Download invoices for orders without an invoice number — the list itself only shows invoiced orders.
- Customize the PDF layout / template from this action — the bundle uses the store's currently-configured invoice template (see [[settings-invoicing]] and [[invoices-download-rendering]]).

## Settings & fields

The configurable behaviour lives in the aspect pages:

- **Sync threshold + async chunk size** (10 sync / 50 per async chunk) — see [[invoices-download-sync-async]].
- **2FA code expiry windows** (60 min email / 2 min TOTP) — see [[invoices-download-entry-points]].
- **Permission mapping** (`orders` + `invoices.all` + `invoices.download`) — see [[invoices-download-permissions-plan]].
- **Download scope** (currently all invoiced orders — the filter is not applied to the bundle) — see [[invoices-download-scope]].

## Business rules

The cluster's load-bearing rules, each detailed in its aspect:

- **PDFs are generated fresh on demand, not stored** — re-downloading reflects the order's current state. See [[invoices-download-rendering]].
- **Async threshold is 10 invoices** — above it the bundle is chunked at 50 per batch and delivered by email + admin alert. See [[invoices-download-sync-async]].
- **Scope = all invoiced orders (the filter is not applied)** — the Download button forwards the list's filter query, but the action reads only the legacy `extra.ids` / `extra.dates` parameters the new UI no longer sends, so the bundle covers every invoiced order regardless of the on-screen filter. See [[invoices-download-scope]].
- **Empty scope returns a specific error** — *"No targeted orders nor all"*. See [[invoices-download-scope]].
- **Credit notes are NOT bundled** — only invoice PDFs. See [[invoices-download-rendering]] and [[orders-credit]].

## Plan gates

This feature is gated by the `invoices` plan-feature. The parent [[orders-invoices]] list page is itself gated on `invoices`, so when the plan lacks the feature the **Download** button is unreachable. Full mapping in [[invoices-download-permissions-plan]] (see also [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]]).

## Related

- [[orders-invoices]] — parent invoices list (the Download button lives here).
- [[orders-invoices-list-filters]] — the filter panel that defines the download scope.
- [[orders-invoices-list-verification]] — the shared 2FA step, documented as the list-level guard.
- [[orders-invoices-export]] — sibling CSV export of invoice metadata.
- [[orders-invoice]] — per-order single invoice PDF download.
- [[orders-export]] — orders export (CSV, different action).
- [[orders-credit]] — credit notes (separate flow from invoices).
- [[settings-invoicing]] — invoice template, numbering, store-wide invoicing toggle.
- [[settings-staff]] — `invoices.download` permission grant.
- [[settings-queue-view]] — async job status for large bundles.
- [[invoice]] — entity page.

## Open questions

(none — bundle scope, credit-note exclusion, and template-rendering behaviour all verified across the aspect pages.)
