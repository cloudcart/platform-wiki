---
type: feature
nav_path: "Orders → Order details → Shipping → Waybill"
route_name: admin.internal.waybill
route_path: /admin/orders/action/shipping/:order_id/waybill
aliases: ["Waybill", "Generate waybill", "Tracking number", "Shipping label", "Товарителница", "Издаване на товарителница", "Етикет за доставка"]
tags: [orders, shipping, waybill, courier, omniship, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---

# Shipping waybill (per order)

## Purpose

The merchant's flow for **generating, saving, removing, printing, and updating** a shipping waybill (товарителница / shipping label) on a specific order. This is the single most complex per-order action: it integrates with the configured courier (Econt, Speedy, Sameday, BoxNow, GLS, DPD, etc.) via the platform's OmniShip abstraction layer.

The action has **six possible operations** — generate, save, print, remove (void), update insurance, change payer side — each with cascading side effects (stock decrement, invoice generation, payment auto-capture, webhook fires, customer notification). The merchant sees a roughly consistent UI across couriers, but the underlying API calls vary substantially.

## Where to find it

From [[orders-details]] → **Shipping action row** in the order summary. The visible buttons depend on the order's fulfillment state:

| State | Visible buttons |
|-------|-----------------|
| **No waybill yet** (`status_fulfillment = not_fulfilled`, shipping provider set) | **Generate waybill** (opens form modal — see [[waybill-generate-flow]] / [[waybill-generic-modal]]). |
| **Waybill generated** | **Print PDF** (see [[waybill-print-pdf]]), **Remove waybill** (see [[waybill-remove-void]]). Also: **Change side** dropdown (see [[waybill-payer-side]]), **Update insurance** in-place edit. |

The action area is hidden when the order has no shipping provider OR all products are digital.

## Sub-routes (under `/orders/action/shipping/{order_id}/`)

| Route name | Method | Purpose |
|------------|--------|---------|
| `admin.internal.waybill` | GET | Open the waybill generation form. |
| (same route) | POST | Save the generated waybill. |
| `admin.internal.waybill-remove` | GET | Void the waybill on the courier + delete the fulfillment locally. |
| `admin.eur.waybill` | GET | EUR-currency variant — currently throws hard-block error after 2026-01-01 (see [[waybill-generic-modal]]). |
| `admin.internal.insurance` | POST | Update insurance amount on existing waybill. |
| `admin.internal.change-side` | POST | Change payer side (see [[waybill-payer-side]]). |
| `admin.internal.print_waybill` | GET | Render generic platform PDF (NOT the courier-formatted label — see [[waybill-print-pdf]]). |
| `admin.orders.shipping.change` | POST | Switch shipping provider on the order (pre-waybill). |

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[waybill-generate-flow]] — the courier-specific form, the Save commitment, the validation gauntlet, the cascading side effects (stock decrement, invoice, receipt, auto-capture, webhook, ERP exports).
- [[waybill-courier-specifics]] — per-courier table (Econt, Speedy, DPD-BG, BoxNow, Sameday, GLS, Cargus, DHL, etc.), Econt's exclusive billing-merge, Sameday's `company_name` from [[settings-general]], pickup-type-aware change-provider flow.
- [[waybill-payer-side]] — sender / recipient / other; the per-courier allowed-sides table; the filter rules that strip `PAYER_RECEIVER`; the 3-step default fallback (order meta → courier setting → first remaining in filtered list); the side-change cascade.
- [[waybill-remove-void]] — Remove flow; courier `cancelBillOfLading` swallowed errors; status recalculation rule (paid vs pending); fulfillment-returns cascade; automatic stock restore.
- [[waybill-print-pdf]] — generic platform PDF (the platform code) vs courier-formatted thermal label (per-courier app); when to use which.
- [[waybill-generic-modal]] — the minimal 4-field fallback form (`product/waybill.tpl`); the EUR-route hard-block message in Bulgarian after 2026-01-01; marketplace pickup banner; the code-disabled insurance toggle.
- [[waybill-api-fulfillment]] — JSON-API v2 path via [[api-order-fulfillment]]; same validation + same cascade as the UI; `api2`-namespaced history rows; integration patterns (WMS, [[apps-pick-and-pack]]).

## What the merchant can do here

- **Generate waybill** — open the courier's form, review pre-fill, click Save to commit the dispatch.
- **Print PDF** — download the platform's generic dispatch summary; for the courier-formatted thermal label, use the courier's app.
- **Remove waybill** — void on courier side + restore local order state to `not_fulfilled`.
- **Update insurance** — change declared value on an active waybill (re-syncs courier).
- **Change side** — switch payer side from a dropdown (re-syncs courier; recalculates totals).
- **NOTE:** No bulk waybill generation, no in-place waybill amendment (must Remove then Generate again), no draft waybill state.

### What the merchant CANNOT do here

- Generate a waybill on an order with no shipping provider — must pick one first via Change shipping provider.
- Generate a waybill on a digital-only order — no physical shipment.
- Generate a waybill on an order with no shippable products.
- Save a waybill if the order's stock isn't reserved properly (variant-tracked, `tracked='no'`-overridden, `continue_selling='yes'`-overridden — see [[waybill-generate-flow]]).
- Generate an EUR-currency waybill for BGN orders **after 01.01.2026** — hard-block error: *"Поръчки в BGN не могат да се изпращат след 01.01.2026. Моля, конвертирайте поръчката в EUR."* See [[waybill-generic-modal]].

## Business rules (cluster-wide)

- **One waybill per order at a time.** To regenerate, Remove first via [[waybill-remove-void]].
- **Save is a courier-side commitment.** No draft state — Save IS the dispatch.
- **Fulfillment always decrements stock** regardless of the cart-decrement-timing setting on [[settings-cart]]. See [[inventory-decrement-timing]].
- **Remove always restocks** automatically via the per-line decrement-tracking flag. See [[inventory-restock]].
- **Pre-authorized payment auto-captures** on Save for gateways supporting `captureAutomaticAuthorization`. See [[orders-payment-capture]].
- **OmniShip layer** normalises the courier surface but each manager publishes its own `getWaybillSides`, `formatInsurance`, `getSupportType`.
- **Status recalculation on Remove** drops a completed order back to `paid` (or `pending` if COD hadn't been marked). See [[waybill-remove-void]].

## Settings & fields

The two waybill entry points and the EUR-route hard-block are documented on [[waybill-generic-modal]]. The validation gauntlet and pre-fill rules are on [[waybill-generate-flow]]. Per-courier field categories are on [[waybill-courier-specifics]]. Payer-side fields are on [[waybill-payer-side]].

## Related

- [[orders-details]] — parent screen (shipping action row).
- [[orders]] — list page where the merchant filters by fulfillment status.
- [[shipping]] — shipping provider configuration.
- [[settings-boxes]] — package dimensions used to populate the waybill.
- [[apps]] — courier apps (Econt, Speedy, BoxNow, Sameday, GLS, Cargus, Eurosender, Frisbo, etc.).
- [[settings-statuses]] — Fulfilled status + customer notification.
- [[settings-cart]] — stock decrement timing.
- [[settings-hooks]] — `order.updated` webhook.
- [[orders-sync-cod]] — COD payment sync flow (separate but related to waybills).
- [[orders-history]] — waybill events appear in the audit log (actions 27 / 28 / 47).
- [[orders-payment-mark-paid]] — for COD orders, used after the courier confirms COD payment.
- [[orders-payment-capture]] — fulfillment-add triggers auto-capture for two-phase payments.
- [[orders-products]] — line-item edits BLOCKED while a fulfillment exists.
- [[inventory-decrement-timing]] — fulfillment always decrements, regardless of cart setting.
- [[inventory-restock]] — symmetric re-credit flow on Remove.
- [[order-processing-pipeline]] — fulfillment-add and fulfillment-remove side-effects catalogued there.
- [[marketing-discounts-shipping]] — `has_free_shipping` flag affects Receiver-pays visibility (see [[waybill-payer-side]]).

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
