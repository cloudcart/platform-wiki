---
type: api-resource
resource_path: /api/v2/order-fulfillment
http_methods: [POST, DELETE]
related_entity: order
related_features: [orders-shipping-waybill, orders-history, orders-notify-customer]
aliases: ["Order fulfillment API side effects", "order-fulfillment POST cascade", "mark fulfilled cascade", "order-fulfillment DELETE teardown", "void waybill API", "fulfillment payment auto-capture", "order-fulfillment 422 cases", "courier void on delete"]
tags: [api, json-api-v2, orders, fulfillment, waybill]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Order Fulfillment API — side effects & failure modes

> Part of [[api-order-fulfillment]]. See the hub for the other aspects (attributes & querying, examples & testing).

## Purpose

This aspect documents what happens **after** a write to the `order-fulfillment` resource. A single POST cascades through more than a dozen platform events — inventory decrement, invoice / receipt number generation, customer email, webhooks, and (on supporting gateways) a real money-movement payment capture. A DELETE runs the inverse teardown and flips the parent order's status. **Integrators must read this before wiring a back-office ERP to this endpoint** — the cascade matches the admin-panel **Save waybill** click, not a quiet metadata write.

## Endpoint

The side effects fire from `POST /api/v2/order-fulfillment` (the create / "mark shipped" call) and `DELETE /api/v2/order-fulfillment/{id}` (the void). PATCH amends tracking fields with no cascade beyond firing `order.updated`. POST guards are on the hub [[api-order-fulfillment]]; writable attributes are on [[api-order-fulfillment-attributes]]. Base URL, auth, headers: see [[json-api-v2]].

## Attributes

The cascade is driven by the writable attributes on [[api-order-fulfillment-attributes]] — the tracking URL / number, the two dates, plus the required `order` relationship. The auto-computed line-item list determines which inventory rows decrement. `date_fulfilled` and `shipping_provider` are read-only, set by the platform during the cascade.

## Relationships

The POST cascade touches relationships indirectly: it links the order's `products` line items to the new fulfillment, triggers inventory events against those lines, and schedules a discount-usage recompute against the order's `discounts` — all downstream effects of the single `order` relationship (see [[api-order-fulfillment-attributes]]).

## Filtering & sorting

Not applicable to writes. The collection-read filter / sort reference lives on [[api-order-fulfillment-attributes]].

## Side effects

A successful **POST** runs the **same fulfillment pipeline as the admin-panel Save waybill click** — see [[orders-shipping-waybill]] for the merchant-flow equivalent and [[order-processing-pipeline]] for the broader lifecycle context.

**Synchronous (during the POST request):**

1. **Validates** the order has a shipping provider, has non-digital products, is not archived, and is not already fulfilled — POST returns 422 with the localised error otherwise.
2. **Creates the fulfillment row** with the provided tracking URL / number / dates plus the auto-computed product list. The insert is wrapped in a 5-attempt retry to absorb race conditions on concurrent shipment events.
3. **Updates `order.status_fulfillment`** → `fulfilled`.
4. **Links the order's line items** to the new fulfillment (`order_products.order_fulfillment_id`).
5. **Decrements inventory** for the line items — stock comes out of warehouses per [[inventory-tracking]] (the timing follows the order's existing decrement state — see [[inventory-decrement-timing]]; the async chain is on [[background-queue-inventory]]).
6. **Generates the order's invoice number** (sequential per the merchant's invoice numbering settings — see [[orders-invoice]]).
7. **Generates the order's receipt number** (separate sequence).
8. **Writes an [[orders-history]] entry** — `fulfillmentAdd` with the payload and product IDs. The audit trail records `namespace = "api2"` → surfaced as **"API"** as the actor (the single platform-wide audit log; see [[json-api-v2]]).
9. **Records an order-status-history row** for the `not_fulfilled` → `fulfilled` transition.
10. **Dispatches a customer-income-update event** for analytics / reporting.
11. **Auto-captures payment authorization** — if the order's payment provider supports `captureAutomaticAuthorization` (e.g. Stripe with manual capture) AND the order has an outstanding authorize amount, the gateway is called to capture the authorized funds. **This is a real money movement.** See [[orders-payment-capture]].

**Asynchronous (post-commit):**

12. **Runs the order's webhook hooks** — `order.updated` fires to every subscribed endpoint in [[settings-hooks]]; status-specific hooks may also fire per subscription.
13. **Schedules a discount-usage recompute** with a 10-second delay on the order-events queue — recomputes the discount-usage counter on [[discount]] for any discounts on the order.
14. **Sends the customer fulfillment notification email** IF the per-order `notify_customer` flag is true AND the store-wide notification toggle is on (see [[orders-notify-customer]]).

**Note on the courier dispatch.** Unlike the admin-panel waybill flow, this endpoint does **NOT** call the courier's API to create a dispatch. The admin flow pushes the shipment to the courier abstraction (Econt, Speedy, BoxNow, etc.), gets a tracking number back, then saves. API POST assumes the dispatch is **already booked elsewhere** (e.g. by the merchant's external ERP) — it records "this order is shipped, here's the tracking info" only.

A successful **DELETE** runs the corresponding teardown:

1. **Calls the courier's API to VOID the dispatch** if the order's `omniship_provider` is set AND it has a stored `bol_id` (courier-issued bill-of-lading ID). The courier may reject the void (e.g. Econt: *"Package already in transit"*); per the audit on [[orders-shipping-waybill]] this is **silently swallowed** — the local fulfillment row is removed regardless. **Integrators relying on automatic courier voids must validate manually with the courier dashboard.**
2. Removes order meta keys (`bol_id`, `pdf_url`, `glovo_shop_info`) from the order.
3. Deletes all fulfillment rows for the order.
4. Fires the fulfillment-removal hook → which **resets `order.status_fulfillment`** → `not_fulfilled` and **reverts the order's `status` to `paid` if the last payment is `completed`, otherwise to `pending`.** Integrators should expect the order's `status` to flip on DELETE.
5. Writes an [[orders-history]] entry for the removal (recorded with `namespace = "api2"` → "API").
6. Schedules another discount-usage recompute (10-second delay).
7. Runs hooks → `order.updated` webhook fires.

**Common 422 cases:**

- `{"errors":[{"status":"422","source":{"pointer":"/data/relationships/order"},"detail":"This order is already fulfilled."}]}` — POST on an order whose `status_fulfillment` is already `fulfilled`.
- `{"errors":[{"status":"422","source":{"pointer":"/data/relationships/order"},"detail":"The order field is required."}]}` — missing the `order` relationship on POST.
- `{"errors":[{"status":"422","source":{"pointer":"/data/attributes/shipping_tracking_url"},"detail":"The shipping tracking url format is invalid."}]}` — non-URL value sent for `shipping_tracking_url`.
- `{"errors":[{"status":"422","source":{"pointer":"/data/attributes/shipping_date_delivery"},"detail":"The shipping date delivery does not match the format Y-m-d."}]}` — malformed date.

Other [[order]] business rules — order archived, no shipping provider, no shippable (non-digital) products — block the underlying fulfillment-add call and surface as validation errors.

## Equivalent UI

- [[orders-shipping-waybill]] — the **Save** step runs this exact POST cascade; **Remove waybill** runs the DELETE teardown. The admin flow additionally calls the courier (Print PDF, Update insurance, Change payer side have no API counterpart).
- [[orders-history]] — the audit-trail entries (`fulfillmentAdd` / removal) produced by POST / DELETE, attributed to the `api2` ("API") actor.
- [[orders-notify-customer]] — the per-order email gate for step 14.

## Related

- [[api-order-fulfillment]] — hub.
- [[api-order-fulfillment-attributes]] — the writable attributes that drive this cascade.
- [[api-order-fulfillment-examples]] — worked POST / DELETE requests + the cascade-verification testing checklist.
- [[order-processing-pipeline]] — how fulfillment slots into the broader order lifecycle.
- [[inventory-tracking]] — the stock-decrement side effect.
- [[inventory-decrement-timing]] — when stock actually drops relative to the order's status.
- [[background-queue-inventory]] — async inventory + search-sync chain.
- [[orders-invoice]] — invoice number generation (one of the side effects).
- [[orders-payment-capture]] — payment-authorization capture (the real money movement).
- [[orders-notify-customer]] — customer email notification toggle.
- [[settings-hooks]] — webhook subscriptions fired post-commit.
- [[orders-history]] — the `api2` audit entries.
- [[discount]] — the 10-second discount-usage recompute.
- [[json-api-v2]] — API hub.

## Open questions

- Document the precise conditions the 5-attempt retry on the fulfillment insert is designed to absorb (likely race conditions on concurrent shipment events for the same order). `(verify)`
- Document whether the order-status revert on DELETE (paid → pending if no completed payment) writes a status-history entry attributed to `api2` correctly — useful for support investigations. `(verify)`
- Verify whether the courier-void failure on DELETE is logged anywhere visible to the merchant (currently appears silently swallowed per [[orders-shipping-waybill]] — confirm with support if there's any user-visible signal). `(verify)`
- Document the relationship between API POST and `omniship_provider` / `bol_id` order meta — the courier dispatch is NOT created by API POST, so a subsequent DELETE has nothing to void at the courier unless the merchant's external integration set `bol_id` independently. `(verify)`
