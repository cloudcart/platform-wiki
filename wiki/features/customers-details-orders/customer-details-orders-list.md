---
type: feature
nav_path: "Customers → Customer details → Orders → List view"
route_name: customers-orders.new
route_path: /admin/customers-new/details/:id/orders
aliases: ["Customer order list", "Customer orders table", "Order history columns", "Order history actions column"]
tags: [customers, orders, history, list]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-orders]]. See the hub for the other aspects (filters, scoping).

# Customer orders — List view

## Purpose

The paginated table that renders one customer's order history — its eight columns, the fixed sort order, the icons-only Actions column, the status-badge colour mapping, and every click-through navigation. This aspect covers the **table itself and its read-only-by-design surface**. The filter bar is documented on [[customer-details-orders-filters]]; the server-side rules that decide which orders the table returns are on [[customer-details-orders-scoping]].

## Where to find it

From [[customers-details]] → **Orders** tab. The route is `/admin/customers-new/details/:id/orders`.

## What the merchant can do here

- See every order this customer has placed in a paginated table.
- Sort by Order ID descending (default — newest first) or by Date.
- Click an order to navigate to the order detail page in the orders feature (opens in a **new tab**).
- Click a tracking number in the Receiving column to open the courier's tracking page in a new tab.
- Read the customer-note / admin-note tooltips on the per-row Actions icons.

### What the merchant CANNOT do here

- View / edit / print a PDF invoice from a per-row action — those actions live only on the global order detail page, not in this column.
- Mutate any order from this tab — there is no Add / Edit / Delete modal, no confirmation dialog, and no inline action that changes data.

## Settings & fields

### Eight columns

| Column | Notes |
|--------|-------|
| **Order ID** | Sortable. Click → opens the order in the orders feature (opens in NEW TAB at `/admin/orders/details/<id>`). Renders as "Order #<id>" with tooltip. |
| **Address** | Shipping address summary — displays **city name** on first line + **country name** below it. (Not recipient name or street.) |
| **Date** | When the order was placed. Sortable. |
| **Fulfillment** | The shipping provider used (Econt / Speedy / etc.) — text only, not sortable. |
| **Receiving** | Expected delivery date (if courier returned an estimate) **PLUS clickable tracking number + tracking URL link** below. The tracking URL is either the courier's URL or falls back to a `track17.net` link. |
| **Status** | Order status badge (Paid / Pending / Completed / Cancelled / Refunded / etc.). |
| **Total price** | Order total with currency + **last payment provider name as a small badge underneath** (e.g., "Stripe" / "EasyPay"). |
| **Actions** | Only two icons: 1) message-dots icon shown when a **customer note** exists on the order (note shown in tooltip); 2) sticky-note icon shown when an **admin note** exists (note shown in tooltip). NOT view/edit/PDF actions — those are only on the order detail page itself. |

### Sort

Even though the column definitions mark Order ID and Date as sortable, the backend validates the sort field against only `id,date_added`. Any other column header is non-sortable, and the default sort is `id DESC`. See [[customer-details-orders-scoping]] for the full sort/pagination caps.

## Business rules

### Read-only by design

This tab is intentionally pure. There is **no Add / Edit / Delete modal, no confirmation dialog, no per-row inline action that mutates data**. Every per-row interaction either navigates away or shows a passive tooltip. To manage orders (bulk-edit, mark fulfilled, refund), the merchant uses the global Orders feature, which is the canonical management surface.

### Per-row Actions column (icons only, no menu)

The "Actions" column on the far right is intentionally minimal — it does NOT contain a hamburger / overflow menu. The icons shown depend on which notes are present:

| Icon | When visible | Behaviour |
|------|--------------|-----------|
| `fa-message-dots` (chat bubble) | Order has a non-empty `note_customer` field | Hover-tooltip displays the full customer-note text. Not clickable. |
| `fa-note-sticky` (sticky note) | Order has a non-empty `note_administrator` field | Hover-tooltip displays the full admin-note text. Not clickable. |

If neither note is present, the cell is **empty** (no icon, no placeholder). There is no view-PDF / print / refund action in this column.

### Click-through navigations (no modal — opens new tab/page)

- **Order ID column** ("Order #123" with tooltip-dotted text) → clicks open `/admin/orders/details/<id>` in a **new tab** (`target="_blank"`). No modal.
- **Receiving column** → when the order has both `tracking_url` and `tracking_number`, the tracking number renders as an external link with an arrow icon (`fa-arrow-up-right-from-square`) — clicks open the courier's tracking URL in a new tab.
- **Address column** displays read-only city-name + country-name (no link, no edit).
- **Total price column** displays the currency sign (from `serverSettings('currency.sign')`) + the numeric total, with the **payment-provider name as a small purple "update" badge** underneath when populated (e.g., "Stripe" / "EasyPay" / "Bank transfer"). The provider badge is NOT clickable.

### Status badge colour mapping

The Status column is a coloured badge — colour comes from the order's `status_key`:

- **Yellow** (`cc-tag-status--yellow`): pending, fulfilled, requested, disputed, held, initiated.
- **Green** (`cc-badge-status--active`): completed, paid.
- **Red** (`cc-tag-status--required`): refunded, cancelled, chargebacked, timeouted, voided, failed.
- **Grey** (`cc-tag-status--default`): anything else.

## Related

- [[customers-details-orders]] — hub.
- [[customers-details]] — parent details page.
- [[order]] — entity page; the order opened from the Order ID column.
- [[shipping]] — shipping providers shown in the Fulfillment column.
- [[settings-payment-providers]] — payment providers shown as the Total price badge.

## Open questions

None.
