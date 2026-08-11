---
type: feature
nav_path: "Orders → Order details → Shipping → Waybill → Generate"
route_name: admin.internal.waybill
route_path: /admin/orders/action/shipping/:order_id/waybill
aliases: ["Generate waybill", "Save waybill", "Издаване на товарителница", "Fulfill products", "Ship items"]
tags: [orders, shipping, waybill, courier, fulfillment]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-shipping-waybill]]. See the hub for other aspects (per-courier specifics, payer side, print PDF, remove/void, generic modal, API path).

# Waybill — generate & save flow

## Purpose

The action of opening a courier-specific waybill form on a given order, filling in package details (recipient, sender, weight, insurance, COD, payer side, service tier), and committing the dispatch to the courier. **Save is a courier-side commitment** — once the merchant clicks Save, the courier may begin pickup within hours.

## Where to find it

[[orders-details]] → Shipping action row → **Generate waybill** button. Button is visible when `status_fulfillment = not_fulfilled` AND a shipping provider is set AND at least one product is non-digital.

The button opens one of TWO forms — see [[waybill-generic-modal]] for the fallback minimal modal and the routing rule.

## What the merchant can do here

- Review and adjust pre-populated fields: recipient, sender, package weight / dimensions, declared value (insurance), COD amount, payer side (see [[waybill-payer-side]]), service tier, additional courier-specific fields (Econt office, BoxNow locker, Speedy depot — see [[waybill-courier-specifics]]).
- Click **Save** to commit. A draft cannot be kept on the platform — Save IS the dispatch.
- Click **Complete order** (alternative submit on the generic modal — `#fulfillComplete`) to save the waybill AND flip order status to `completed` in one click.

## Settings & fields

### Pre-filled values (from the order)

| Field | Source |
|-------|--------|
| Recipient | Order's shipping address. |
| Sender | Store config / sender-address profile. |
| Package weight / dimensions | Calculated from product weights + chosen shipping box per [[settings-boxes]]. |
| Declared value (insurance) | Sum of `order_price × quantity` across non-digital products only. Formatted via the provider's `formatInsurance`. Merchant can override. |
| COD amount | Order's invoice total when payment is COD; `0` otherwise. |
| Payer side | See [[waybill-payer-side]] (3-step fallback: order's `side` meta → courier's "Default payer side" setting → first key in filtered allowed list). |
| Products to ship | Only `digital = no` AND not already fulfilled. Digital products excluded entirely. |

### Validation gauntlet (on Save)

In order — first failure aborts:

- Order must not be archived: *"Cannot perform this operation on archived order"*.
- Order must have a shipping provider: *"Products cannot be fulfilled without a shipping method"*.
- At least one product to ship: *"Some of the products are no longer in the order"*.
- For variant-tracked products: variant stock must cover quantity UNLESS the order product has `tracked='no'` OR the product has `continue_selling='yes'`: *"There is not enough quantity"*.
- None of the products already in another fulfillment: *"Some of the products are already fulfilled"*.
- Shipping tracking URL max 255 chars (silently rejected if longer).

## Business rules

### One waybill per order at a time

The order has ONE fulfillment record at a time. To regenerate (wrong courier, wrong package weight), the merchant must Remove the existing waybill first — see [[waybill-remove-void]] — then Generate a new one.

### Save is a commitment, not a draft

Clicking Save creates the dispatch on the courier's system. The courier may already start picking up the package within hours. The platform exposes no "draft" or "preview" state.

### Cascading side effects on successful Save

All wrapped in one DB transaction:

- Order's `status_fulfillment` flips to `fulfilled`.
- **Stock decremented** for shipped products (regardless of cart settings — fulfillment ALWAYS decrements). See [[inventory-decrement-timing]].
- **Invoice number generated** if not already issued — see [[orders-invoice]].
- **Receipt number generated** if applicable — see [[orders-receipt]].
- **Pre-authorised payment auto-captured** if the payment provider supports `captureAutomaticAuthorization` AND there's a pending authorization. So for some gateways, Save waybill effectively settles payment. See [[orders-payment-capture]].
- Order status history entry: `not_fulfilled → fulfilled`.
- Customer income (lifetime spend) recalculated.
- Customer fulfillment-notification email sent if order `notify_customer = yes` (queued — see [[orders-notify-customer]]).
- `order.updated` webhook fires per [[settings-hooks]].
- Discount-usage sync queued with a 10-second delay — recomputes usage counts post-fulfillment. See [[marketing-discounts-codes]].
- All downstream app listeners trigger: ERP exports (Universum, Gensoft, Barsy, Versus), accounting (SmartBill, Szamlazz, FGo, Rkeeper), warehouse routing (StoreLocations, PickAndPack), analytics (segment-update for [[customers-custom-groups]], campaign triggers for [[marketing-campaigns]]).
- History row `order_fulfillment_add` (action 27) appears in [[orders-history]].

### No bulk waybill generation

Generation is strictly per-order. There is no bulk action on [[orders]] for generating waybills on selected orders. For multi-package dispatches, the merchant works order-by-order or uses the courier's own bulk-import tool.

### Re-generation requires void first

Once a fulfillment exists, editing the order's products / quantities / address is BLOCKED on the line items (see [[orders-products]]). To amend, the merchant must Remove via [[waybill-remove-void]], edit the order, then re-generate. The platform does not support in-place waybill amendment via the courier API.

### Form UI mechanics

- Generate waybill: `data-ajax-panel` opens a side-panel form.
- Save: `ajaxForm` submission.
- On error: the courier's error message surfaces as a toast; the order stays `not_fulfilled`.

### Marketplace-pickup providers do not open this form

When the active shipping provider's manager declares `SUPPORT_MARKETPLACE` (Amazon FBA, Frisbo, similar fulfillment-by-marketplace integrations), the Change Provider action diverts to `apps.shipping.changePickup` or `apps.{app_key}.changePickup`. The merchant does NOT generate a waybill on the platform side — the marketplace handles dispatch. See [[waybill-generic-modal]] for the marketplace banner that appears above the generic form.

## Related

- [[orders-shipping-waybill]] — hub.
- [[orders-details]] — parent screen (shipping action row).
- [[settings-boxes]] — package dimensions used to pre-fill.
- [[settings-statuses]] — Fulfilled status + customer notification gating.
- [[settings-hooks]] — `order.updated` webhook.
- [[orders-history]] — `order_fulfillment_add` audit entry.
- [[orders-payment-capture]] — auto-capture trigger on fulfillment.
- [[inventory-decrement-timing]] — fulfillment always decrements (regardless of cart setting).
- [[order-processing-pipeline]] — full status-transition pipeline with the fulfillment side-effects catalogued.

## Open questions

None.
