---
type: feature
nav_path: "Orders → List → Export"
route_name: admin.orders
route_path: /admin/orders/list
aliases: ["Orders list export", "Async order export", "Order export queue", "Order export 2FA", "Export orders CSV", "Експорт на списък с поръчки"]
tags: [orders, list, export, async, background-job, two-factor, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[orders]]. See the hub for the other aspects (columns, filters, bulk actions, status taxonomy, default visibility, locking).

# Orders list — export

## Purpose

The **Export** header button on `/admin/orders` produces a CSV of the orders matching the current filter state. It is **confirmed with a two-factor code**, and it has **two outcomes** depending on how many orders are being exported: a small export downloads straight to the browser, a large one is queued and delivered later by email + the File manager.

For the per-order export of line-item products see [[orders-ordered-products-export]]; for the parent admin-panel export entry point see [[orders-export]].

## Where to find it

`/admin/orders` header → **Export** button (next to **+ Add order**). The button is absent on a store that has never taken an order (the whole header region is replaced by the empty state — see [[orders]]).

## What the merchant can do here

### Confirm with a two-factor code

Clicking **Export** does not start the download. It opens a confirmation modal asking for a **6-digit code**, because an order export is a bulk extraction of customer personal data:

- Admins with an authenticator app configured enter the **current TOTP code** — valid for about 2 minutes.
- Everyone else gets a **one-time code emailed** to their admin address — valid for 60 minutes.

Only after a valid code is submitted does the export run. A wrong or expired code returns a validation error and the merchant re-requests it. (If the store's 2FA-by-email functionality is switched off platform-side, the confirmation step degrades to a formality.)

### The two outcomes

| Number of orders in the result | What happens |
|---|---|
| **50 or fewer** | The file is generated inline and the browser downloads it immediately — no waiting, no email. |
| **More than 50** | The export is queued. The merchant gets a toast reading *"The export is being processed. You will receive an email with the download link."* and can navigate away. |

For the queued case, the finished file is zipped and delivered **twice**: as a **download link by email**, and as a file in the store's **File manager** (Settings → Files), where an in-admin notification links straight to it. If the email is missed or filtered, the File manager is the reliable place to look.

For very large stores the queued job walks the whole result set in batches of 500 rows. There is **no upper limit** on how many batches it will run — a 500 000-order export is slow, not truncated.

### What the export contains

One **row per product line**, not one row per order. Each row carries the order-level fields (number, dates, statuses, customer, addresses, payment, shipping, totals) **plus** that line's product name, variant options, SKU, barcode, quantity, vendor, weight, price, discounted price and category — with additional rows for per-line options. Order-level totals are printed only on the order's first row, so a spreadsheet sum of the total column does not double-count.

This means the Orders export **already covers line items**; the separate [[orders-ordered-products-export]] is a differently-shaped product-centric view, not the only way to get products.

## Settings & fields

The export has no merchant-configurable settings — no format picker, no field picker. The 50-order sync/async threshold and the 500-row batch size are platform constants.

## Business rules

### Filter state IS preserved into the export — including filters the merchant forgot

The export uses whatever filter state the list is currently carrying. Because that state is **remembered in the session** (see [[orders-list-filters]]), a merchant who filtered to *Status = Paid* yesterday, navigated away, and comes back today to export will silently export only paid orders. To export everything, clear the filter bar first.

### The export does NOT hide what the list hides

An important asymmetry. The list applies a silent default exclusion — cancelled, voided and archived orders are hidden until a filter is applied ([[orders-list-default-visibility]]). **The export does not.** Exporting from the default, unfiltered view returns **all** orders, including the cancelled, voided and archived ones that are not on screen.

So a merchant reconciling *"the list shows 42 orders but the export has 47 rows"* is not seeing a bug — the export is the complete set and the list is the filtered one. This also makes the export the quickest way to get a true count.

### Any filter you can apply on the list applies to the export

The export builds on the same query as the list, so filters carry over one-to-one — including the two filter combinations that silently misbehave (see [[orders-list-filters]]). A filter that is wrong on the list is wrong in the export too.

### Plan gates inherit from the parent Orders page

The export trigger is gated by the same plan-features as the list itself (`orders_amount`, `orders_revenue`, `users_traffic`). When a path gate is hit, the merchant cannot reach the Orders list — and therefore cannot trigger an export.

## Related

- [[orders]] — hub.
- [[orders-list-columns]] — Export button sits next to **+ Add order** in the header.
- [[orders-list-filters]] — filter state (session-persisted) that the export inherits.
- [[orders-list-default-visibility]] — the exclusion the list applies and the export does NOT.
- [[orders-export]] — parent export-tracking entry point + result download surface.
- [[orders-ordered-products-export]] — the product-centric sister export.
- [[settings-files]] — the File manager where a queued export lands.
- [[plan-features]] — upsell screen when a plan gate fires.

## Open questions

None.
