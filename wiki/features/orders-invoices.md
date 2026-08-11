---
type: feature
nav_path: "Invoices"
route_name: admin.invoices.list
route_path: /admin/invoices
aliases: ["Invoices", "Invoice list", "All invoices", "Cross-order invoices", "Списък с фактури", "Всички фактури", "Изтегли фактури", "Експорт на фактури"]
tags: [orders, invoices, list, accounting]
plan_gates: ["invoices"]
created: 2026-05-21
updated: 2026-07-29
source_count: 7
---
# Invoices (cross-order list)

## Purpose

The merchant's **cross-order invoice list** — a separate top-level page (NOT under [[orders]]) that shows ONLY orders which have a generated invoice number. Used for accounting workflows: filtering by date / customer / invoice number / credit-note presence, then **downloading** the matching invoices as a PDF bundle or **exporting** them as a CSV register (tax filing, quarterly reports, feeding an external accounting system).

The list is distinct from the per-order Invoice action in [[orders-invoice]]: that action downloads ONE invoice; this page lists MANY and supports bulk download / export. It is **consumption-only** — invoice numbers are issued per-order on [[orders-details]], never from here.

This is a hub page. The detail lives in four aspect pages (see **Sub-pages** below). The Assistant should drill into the aspect that matches the question rather than read all four.

## Where to find it

Sidebar → **Invoices** (when invoicing is enabled).

Route: `/admin/invoices`. Method: GET (initial render) / POST (AJAX grid load).

## What the merchant can do here

- **Scan invoice-generating orders** in a sortable table, open any order, and download a single invoice (or credit-note) PDF per row — see [[orders-invoices-list-table]].
- **Filter** — in the **filter panel** (the filter row), not a top-of-page picker — by **date** (order placement date), **customer**, or **credit-note** presence, plus an **order / invoice number** search box — see [[orders-invoices-list-filters]].
- **Download** the invoices as a PDF bundle, or **Export** them as a CSV register — both run asynchronously and are 2FA-gated. **Current limitation:** these buttons cover **all** invoiced orders — the applied filter scopes the on-screen list but is **not** applied to the download / export — see [[orders-invoices-list-bulk]].
- **Verify with a one-time code** before any bulk action runs (when 2FA is active) — see [[orders-invoices-list-verification]].

The merchant CANNOT generate, edit, re-issue, or void an invoice here, and cannot filter by status — those are per-order actions on [[orders-details]] / [[orders-invoice]], or live on the [[orders]] list.

## Sub-pages (in this cluster)

- [[orders-invoices-list-table]] — the six list columns, default sort, and the per-row invoice + credit-note download buttons.
- [[orders-invoices-list-filters]] — the filter panel (date / credit-note / customer) + the order/invoice-number search box, and the fact the **date filter is by order placement date** (no invoice-issue-date filter).
- [[orders-invoices-list-verification]] — the shared 2FA modal that guards the three bulk actions; when it appears and its three outcomes.
- [[orders-invoices-list-bulk]] — the **Download** / **Export** header buttons, the async threshold + chunking, and the scope behaviour (they currently cover all invoiced orders regardless of the applied filter).

## Settings & fields

The detailed field tables (columns, sortable keys, filter operators, async chunk limits) live on the aspect pages. Hub-level controls:

- **Page gate** — the whole page is gated on the store's `invoicing` setting (see Business rules) AND the `invoices` plan feature (see Plan gates).
- **Header** — two buttons, **Download** (PDF bundle) and **Export** (CSV). There is **NO** date-range picker in the header — the date and other filters live in the **filter panel** ([[orders-invoices-list-filters]]). **These buttons currently download / export ALL invoiced orders regardless of the applied filter** (the filter scopes only the on-screen list) — detail on [[orders-invoices-list-bulk]].

### Empty state

When the store has zero orders (and thus zero invoices), the page shows a *"No invoices yet"* heading, a help paragraph, and a *"Need help getting started?"* help-link box pointing at the support URL.

## Business rules

### Page gated on the `invoicing` setting

The first line of the template checks `setting('invoicing', 'yes') != 'no'`. When invoicing is disabled (`invoicing = no` in [[settings-invoicing]]), the list / grid is NOT rendered — instead the template's `{else}` branch shows a help box reading *"Invoicing functionality is turned off"* with a support-URL link. The merchant does NOT see a blank page, and the sidebar entry likely doesn't appear at all.

### Setting vs plan gate are two separate gates

The store-wide `invoicing` setting is a merchant toggle (controls whether invoicing fires at all). The `invoices` plan feature is a separate access gate that sits ABOVE the setting — even with `invoicing = yes`, the page is hidden when the plan lacks `invoices` (see Plan gates).

### Invoice data is read from orders, not a separate table

The list joins to the orders table and returns only orders with a non-null `invoice_number`. There is no standalone invoice record — corrections require editing the underlying order. Detail on [[orders-invoices-list-table]].

### Bulk operations are async and queued

Download and Export enqueue background jobs (a small set may return inline; a large set is queued — see [[orders-invoices-list-bulk]]); status appears in [[settings-queue-view]]. Large jobs deliver the file by email rather than an immediate browser download.

### Permission

Standard orders / invoicing permission scope.

## Plan gates

This feature is gated by the following plan-features (see [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `invoices` | Access gate (URL `invoices`) | The `/admin/invoices` route is registered under `restrict.access` in the platform code. When the merchant's plan lacks the `invoices` feature, the plan middleware intercepts the request and redirects to [[plan-features]] for upsell BEFORE the list controller runs. The sidebar entry for **Invoices** is hidden in that case. |

When the gate is hit, the merchant is redirected to [[plan-features]] for the per-feature upsell. `invoices` is a boolean access gate — it requires a plan that includes the feature; it does NOT extend via feature packs ([[plan-vs-feature-pack]]). NOTE: this is DISTINCT from the store-wide `invoicing` setting in [[settings-invoicing]] — that's a merchant toggle that controls whether invoicing fires at all. The plan gate sits above the setting.

## Related

- [[invoicing-and-accounting]] — invoicing & accounting concept hub.
- [[orders]] — parent orders list (the source of the invoice data).
- [[orders-details]] — where individual invoices are generated.
- [[orders-invoice]] — per-order Invoice download flow.
- [[orders-credit]] — credit-note flow (the Credit Note filter cross-references this).
- [[orders-invoices-download]] — the bulk PDF-bundle download in detail.
- [[orders-invoices-export]] — the bulk CSV export in detail.
- [[settings-invoicing]] — invoicing app activation + template config.
- [[settings-queue-view]] — async job status for bulk download / export.
- [[apps]] — external invoicing apps (Szamlazz / FGO / SmartBill / etc.) that generate the invoices.
- [[order]] — entity page.
- [[order-processing-pipeline]] — when invoice numbers are issued (status change + fulfillment, idempotent).

## Open questions

None.
