---
type: feature
nav_path: "Apps → Econt → Shipments"
route_name: apps.econt.shipments
route_path: /admin/shipping/econt/shipments
aliases: ["Econt shipments", "Econt waybills list", "Econt shipments return", "Товарителници Еконт", "Връщания Еконт"]
tags: [apps, shipping, courier, bulgaria, econt, shipments, labels, waybill]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-econt]]. See the hub for the other aspects (Settings, addresses, waybill mapping, pallet, COD / insurance, coverage / caches).

# Econt — Shipments + Shipments return tabs

## Purpose

The Shipments and Shipments return tabs list every Econt waybill the store has generated — Shipments for outbound parcels, Shipments return for return waybills. The merchant tracks status, opens a tracking link, and prints labels here (single-row print or bulk-select print). Both tabs use the SHARED `Shipments.vue` component (Shipping module). The ONLY difference between them: the return tab adds `filters[is_return_voucher] = 1` to the query.

## Where to find it

Sidebar → Apps → Econt → **Shipments** tab → `/admin/shipping/econt/shipments`.
Sidebar → Apps → Econt → **Shipments return** tab → `/admin/shipping/econt/shipments-return`.

Routes:
- `apps.econt.shipments`
- `apps.econt.shipments-return`

## What the merchant can do here

- Browse all generated outbound waybills (Shipments tab) or all return waybills (Shipments return tab).
- Filter by date with an operator-driven dropdown (Yesterday / Today / Tomorrow + `before / after / exactly / before or equals / after or equals`, custom date picker).
- Click the tracking link to open Econt's external tracking page.
- Print a single label from a row's print icon.
- Bulk-select rows and print labels in batch — A4 or A6, depending on the merchant's preset.
- Generate the actual return waybill per-order (Shipments return tab's own creation flow — same fields as outbound, with sender / recipient swapped; see [[econt-waybill-recipient-mapping]] for the recipient composition rules).

## Settings & fields

### Data table

Filtered to: shipping provider = econt, `status_fulfillment = fulfilled` (+ `filters[is_return_voucher] = 1` for the return tab).

Columns include: **Order ID**, **Date added**, **Shipping date**, **Tracking number**, **Status** (from Econt — Pending pickup / In transit / Delivered / Failed / Returned), **Total price**, **Payment provider** — plus a per-row print action.

### Date filter dropdown

Above the table. Options: Yesterday / Today / Tomorrow. Operators: `before / after / exactly / before or equals / after or equals` (custom date picker).

### Bulk actions — Print labels

Select multiple rows → **Print labels** triggers print logic:
- If `speedy_print_size` (the printer-paper-size setting) is set to a specific size (A4 / A6), the labels print in that size directly via `POST /admin/api/labels`.
- If size is `ALL` (or empty), opens **Print Format Select modal** (`PrintFormatSelectModal`) — two buttons: **A4** | **A6**. Picking one triggers the print, opens the resulting PDF in a new tab, then closes the modal.

The modal is also reachable from a single-row print icon when no format is preset.

## Business rules

### Return waybill is a separate sub-page with its own creation flow

Return shipments are managed under their own sub-page (Shipments → Return). The merchant generates a return waybill per order; the form has the same fields as an outbound waybill (recipient = the original sender; sender = the customer's address).

**Mutual-exclusion rule:** "Reject return" and "Return shipment" options cannot both be selected on the same waybill — the platform validates and surfaces the error.

### Printer size is store-wide

The `speedy_print_size` setting controls whether the bulk-print flow needs a format-picker modal. Despite the name, it applies to every OmniShip courier including Econt (it's a shared store-wide print-paper-size preference).

### Status comes from Econt

The Status column is Econt's lifecycle, not CloudCart's order status — *Pending pickup / In transit / Delivered / Failed / Returned*. CloudCart syncs it; do not confuse it with the order's `status_fulfillment` (which is `fulfilled` for every row on this table by construction).

### Labels print as PDFs in a new tab

The print flow opens the generated PDF in a new browser tab — labels are not auto-downloaded. The merchant uses their browser's print dialog from that tab.

## Related

- [[apps-econt]] — hub.
- [[orders-shipping-waybill]] — where the outbound waybill is generated per-order (the rows shown here are the outputs).
- [[econt-waybill-recipient-mapping]] — recipient block composition for outbound + return waybills (B2B billing-override).
- [[econt-cod-insurance]] — COD status row meaning for cash-on-delivery shipments.

## Open questions

None.
