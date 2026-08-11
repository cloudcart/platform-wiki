---
type: feature
nav_path: "Orders → Details → Shipping"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Order shipping row", "Shipping action row", "Order fulfillment row", "Waybill", "Generate waybill", "Fulfill products", "Mark as unfulfilled", "Print label", "Insurance request", "Change side", "Shipping Hours expected delivery"]
tags: [orders, order-details, shipping, fulfillment, waybill, courier]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-details]]. See the hub for the other aspects (header, products, addresses, payment, history, actions, known issues).

# Order details — Shipping + Fulfillment

## Purpose

The **Shipping action row** in the main column of the order details page — surfaces the shipping provider, the **Fulfill products** button that generates the waybill, the **Print** action for the printed label, **Mark as unfulfilled**, change-side and insurance actions for couriers that support them, the per-line fulfilment badges, and the expected-delivery picker (for the Shipping Hours app). Courier-specific app rows (Glovo shop, Store Locations geo-zone) layer additional read-only metadata here.

This page documents the SECTION as it appears on order details. The full waybill flow + per-courier field catalogue is on [[orders-shipping-waybill]].

## Where to find it

Main column of `/admin/orders/details/<order_id>`, below the **Payment** row. It is hidden entirely for digital-only orders, and replaced by a warning when the shipping address is incomplete. **A draft order has no shipping (or payment) buttons** — they appear only once the draft is committed.

## What the merchant can do here

### Shipping row — there is only ONE row

There is no separate "Fulfillment row". Everything to do with dispatch lives in the single **Shipping** row:

- Shipping provider icon + name, and a **Change provider** dropdown (when allowed; a read-only provider name otherwise).
- **Fulfill products** primary button — generates the waybill and marks the order fulfilled.
- **Print** — the label PDF, shown once a waybill exists and the order is fulfilled.
- **Mark as unfulfilled** — the un-fulfil path (see below), shown only once the order IS fulfilled.
- Per-courier secondary buttons: **Change side** (receiver-pays vs sender-pays), **Request insurance**.
- Tracking number (plus the return waybill number, when one exists).
- Situational messages instead of the button: out-of-stock, outstanding card authorisation, or an open return (see below).

Per-line fulfilment state is shown as a **badge on each line of the products table**, not as a separate row — see Business rules.

### Mark as unfulfilled — the only un-fulfil path

Once the order is fulfilled, a red **Mark as unfulfilled** button appears in the Shipping row. It is the **only** way to take an order back out of the fulfilled state from the admin panel — no status-pill route, no bulk equivalent on the [[orders]] list — and it fires **immediately, with no confirmation dialog**. It drops the order's fulfillment record so the order returns to `not_fulfilled` and the waybill can be re-generated. It does **not** re-open line-item editing on an invoiced order — that block keys on the invoice, not on fulfilment ([[orders-details-known-issues]]).

### Fulfill products / waybill flow

The **Fulfill products** button is visible when ALL of the following are true:

- `quantity_enough` (stock is sufficient).
- The order is not already fulfilled.
- `allow_make_waybill_by_status` (status allows waybill generation).
- The order has **no pending return** (see below).
- Payment authorisation isn't blocking.

Clicking POSTs to the courier's `apps.<integration>.waybill` endpoint (integrated couriers) or `admin.internal.waybill` (non-integrated / manual couriers). The integration's response either:

- Generates the waybill silently + shows a **Print** button + tracking number, OR
- Opens an inline panel asking for waybill-specific fields (parcel count, weight, COD amount, insurance — varies per courier).

Full per-courier field catalogue: [[orders-shipping-waybill]].

### EUR-variant waybill (Bulgarian BGN→EUR transition)

The Bulgarian BGN→EUR transition routes orders in `BGN` currency through `admin.eur.waybill` instead of the standard route. This route is hard-coded to throw an error *"Orders in BGN cannot be shipped after 01.01.2026. Please convert the order to EUR."*

The merchant uses the standard `admin.internal.waybill` route in all normal cases; the EUR route is essentially a deprecated alias whose only function is to surface the conversion-required error. The conversion itself is done via the **Convert to EUR** sidebar button (see [[orders-details-actions]]).

### Shipping-Hours expected-delivery panel

Visible only when the **Shipping Hours** app is installed AND the order has delivery dates AND `status_fulfillment != 'fulfilled'`. Triggered by the pencil icon next to the expected-delivery section in the Totals box. Opens a side-panel (medium) that lets the merchant pick a specific delivery date + time window. Route: `sitecp.order.shipping_hours.list`.

### Courier-specific app rows

When specific apps are installed and active, additional read-only or read-and-action rows appear:

| App | Row / Action |
|---|---|
| **Glovo** | Shipping row → location label (read-only — shows which Glovo shop fulfils this order, uses `glovo_shop_info` meta). |
| **Store Locations** | Shipping row → geo-zone label (read-only — uses `geo_zone_name` meta). |

## Settings & fields

The Shipping row reads from the order's shipping snapshot (provider + waybill tracking number + per-courier metadata). Provider capability flags decide which secondary buttons render (change-side, insurance, print).

The **Change provider** dropdown is gated by [[settings-shipping]] (installed + enabled couriers for the store).

## Business rules

### An OPEN RETURN replaces the Fulfill-products button

The most common *"why can't I generate the waybill?"* cause after out-of-stock. If the order has **any return still in `pending`**, the button is not rendered at all — in its place sits a yellow warning telling the merchant to complete or cancel the open returns first (otherwise the fiscal receipt and the cash-on-delivery amount would be wrong). One pending return is enough; `returned` / `cancelled` returns never block. Resolve it from the **Returns & exchanges** box in the sidebar and the button comes back on its own — see [[orders-details-returns]].

### Fulfill products hidden when stock is insufficient

If `quantity_enough` returns false (i.e., the order's line items exceed current stock), the button is hidden and an out-of-stock message is shown instead. The merchant cannot generate a waybill for an order whose stock would go negative on decrement — see [[inventory-oversell]] for the clamping rule.

### Fulfill products hidden when authorization is outstanding

If the payment is in `authorized` state (capture hold) and the gateway requires capture-before-fulfilment, the button is hidden until the merchant captures the authorisation via [[orders-payment-capture]].

### Waybill EUR variant — hard error after 2026-01-01

For orders in `BGN` currency that hit the `admin.eur.waybill` route after 2026-01-01, the platform throws a hard error asking the merchant to convert the order to EUR first. The conversion button is in the sidebar (see [[orders-details-actions]]). This is part of the Bulgarian BGN→EUR transition — verified.

### Per-line fulfillment badge states

Each line in the products table carries a fulfillment badge with three possible states:

- **Not fulfilled** (red) — the line has not been dispatched yet.
- **Fulfilled** (green) — the line has a fulfillment record; clicking it opens the read-only popover (below).
- **Ready for pack** (blue) — a pack-prep state shown when the line's `terminal_for_pack` count matches the ordered quantity (set by the warehouse / terminal pack flow), i.e. the line is staged for packing but the waybill/fulfillment isn't generated yet.

### Per-product fulfillment popover — info only

Clicking the "fulfilled" badge on a line opens a small modal showing the fulfilment details for ONE specific line. It is a **read-only info modal** — there are no partial-fulfilment controls anywhere on the order detail page. Fulfilment is created only by **Fulfill products** (the whole shipment) and removed only by **Mark as unfulfilled**; there is **no "Mark as fulfilled" button and no "generate per-product fulfillments" action** on this screen. Merchants who need per-line dispatch use a warehouse app (see [[fulfillment-and-warehouse]]).

### Cancellation reverses fulfilment

When the merchant moves an order to a negative status (cancelled / refunded / failed / voided / chargebacked / disputed / timeouted) AND it was previously fulfilled, the platform automatically resets `status_fulfillment = not_fulfilled`. So cancelling a fulfilled order makes it appear "un-fulfilled" in the system. The waybill tracking number is preserved but the row marks the order as un-fulfilled. This is the automatic counterpart to the manual **Mark as unfulfilled** button.

### Being fulfilled changes what the status badge SAYS

While the order is fulfilled and its status is neither `completed` nor `cancelled`, the status badge on this page and in the [[orders]] list reads **Fulfilled** rather than the order's real status — a paid, dispatched order therefore shows *Fulfilled*, not *Paid*. See [[orders-details-header]].

### Mark as completed requires fulfilment

The **Mark as completed** action (in the header 3-dot menu) is gated on `status == paid` AND `status_fulfillment == fulfilled` — see [[orders-details-header]]. So the merchant can only mark as completed AFTER both the payment and the courier dispatch are confirmed.

### Shipping amount display — converted / original (multi-currency)

When the order was placed in a **currency different from the store currency**, or the order's stored total no longer matches the shipping's recorded amount, the Shipping row shows the figure **converted to the store currency** plus the **original total** in the order's currency — rather than a single number. So a EUR order in a BGN store (or an order whose total moved after the shipping amount was recorded) surfaces both the converted/current value and the original. See [[multi-currency-order-snapshot]] for the frozen order-currency amounts. (verify the exact divergence trigger.)

### What changing the shipping method actually does

Picking a different provider in the **Change provider** dropdown is not a label swap — in one transaction it:

- **re-quotes** shipping for the new provider (live carrier quote or rate-table lookup) and **recomputes the order totals**;
- **re-keys the shipping address to the new courier's integration** — so office / locker addresses bind to the new courier's network; a previously-chosen office / locker may need re-picking if the new courier doesn't recognise it;
- re-derives the **payer side** for the new provider (see [[order-pipeline-recalculation]]);
- writes a `shippingChange` history entry and fires an **`order.updated`** webhook.

On a **paid (recalc-locked) order** the shipping price is kept rather than re-quoted (the lock — see [[order-pipeline-recalculation]]), unless the change forces a re-quote. **Changing the payer side** (sender ↔ receiver) **does force a re-quote** — it bypasses the lock, because who-pays-shipping changes the collected amount; it re-syncs the courier and recomputes totals. Downstream, switching to a **local-pickup (marketplace)** method re-filters the payment dropdown (Cash on delivery is then hidden) — see [[orders-details-payment]].

### Waybill side effects

Waybill generation does the following:

- POSTs to the courier's API and stores the returned tracking number.
- Optionally writes COD amount + insurance metadata to the order.
- Failure surfaces an inline error in the panel — the order is NOT marked fulfilled.
- On success, the order's `status_fulfillment` may automatically flip to `fulfilled` (depends on courier).

See [[orders-shipping-waybill]] for the full per-courier catalogue.

## Related

- [[orders-details]] — hub.
- [[orders-shipping-waybill]] — canonical waybill flow + per-courier field catalogue.
- [[orders-payment-capture]] — capture-authorisation flow (gates Fulfill products when the payment is in `authorized` state).
- [[shipping]] — shipping integrations + capability flags.
- [[settings-shipping]] — courier catalogue.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-eushipment]] / [[apps-boxnow]] / [[apps-sameday]] — major couriers.
- [[apps-shipping-hours]] — expected-delivery date / time picker.
- [[apps-store-locations]] — geo-zone label on the row.
- [[apps-glovo]] — Glovo shop label on the row.
- [[inventory-oversell]] — why `quantity_enough` gates the Fulfill-products button.
- [[orders-details-returns]] — the open-return block on Fulfill products.
- [[orders-details-header]] — the "Fulfilled" status badge.
- [[fulfillment-and-warehouse]] — the fulfilment model + apps that do per-line dispatch.
- [[orders-details-actions]] — Convert-to-EUR sidebar button (used before BGN waybill).

## Open questions

None.
