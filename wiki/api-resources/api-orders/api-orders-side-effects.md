---
type: api-resource
resource_path: /api/v2/orders
http_methods: [GET, PATCH]
related_entity: order
related_features: [orders-status-change, orders-history, orders-notify-customer]
aliases: ["Orders API side effects", "orders status PATCH cascade", "orders fulfill action", "order-status helper", "orders 405 blocked", "orders 422 cases", "orders invoice usn single write"]
tags: [api, json-api-v2, orders]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Orders API — side effects & failure modes

> Part of [[api-orders]]. See the hub for the other aspects (attributes & querying, examples & testing).

## Purpose

This aspect documents what happens **after** a write to the `orders` resource — the full status-transition cascade a PATCH fires, the single-write invoice / USN semantics, the `/fulfill` custom action, the read-only `/order-status` helper, and the complete 405 / 422 failure catalogue. Integrators must read this before driving status from an outside system: one PATCH can move real money, send customer emails, and correct stock.

## Endpoint

The side effects here fire from `PATCH /api/v2/orders/{id}` (and the `PATCH /api/v2/orders/{id}/fulfill` variant). The `GET /api/v2/order-status` helper is read-only and listed below. POST and DELETE are blocked (see *Side effects*). Base URL, auth, headers: see [[json-api-v2]].

## Attributes

The cascade is driven by the four writable attributes documented on [[api-orders-attributes]] — `status` (the transition trigger), `invoice_number` and `usn` (single-write, uniqueness-checked), and `invoice_date` (plain write). `status_fulfillment` is read-only here and only flips through the fulfillment path ([[api-order-fulfillment]]).

## Relationships

The status cascade touches several relationships indirectly: it cancels open `payment` authorization holds, schedules a discount-usage recompute against `discounts`, and triggers inventory events against the order's `products` lines. None of these are written by the PATCH payload directly — they are downstream effects. See [[api-orders-attributes]] for the relationship list.

## Filtering & sorting

Not applicable to writes. The `/order-status` helper accepts an optional `?filter[<key>]=<value>` to scope its flat list (e.g. by slug). The collection read filters live on [[api-orders-attributes]].

## Side effects

A successful **PATCH `/orders/{id}`** that changes `status` runs the **same status-transition pipeline as the admin-panel status pill** — there is no API-only fast path. See [[order-processing-pipeline]] for the full catalogue. The highlights:

- **Hard transition gates** — `completed` requires `paid + fulfilled`; `cancelled` blocked from `paid` or `completed`; `abandoned` only from `pending`; archived orders block every status change. Gate violations return 422 with the localised error message.
- **Auto-promotion** — when the store-level `order_complete` setting (default ON, see [[orders-details]]) is on, a `paid + fulfilled` order is auto-promoted to `completed` on the very next save, even when PATCH targets an unrelated field. Integrators should expect this.
- **Negative-status flip** — moving to `cancelled` / `voided` / `refunded` auto-cancels any open payment authorization hold (multi-gateway behaviour — see [[orders-payment-capture]] and [[payment-provider-mechanism]]) and resets `status_fulfillment` to `not_fulfilled`.
- **Stock movement** — status changes that cross the `paid` / `cancelled` boundary trigger inventory pipeline events (see [[inventory-decrement-timing]] for when stock drops, [[inventory-restock]] for the auto-return on cancel / refund / void, and [[background-queue-inventory]] for the async chain).
- **Discount-usage recompute** — every status change schedules a 10-second-delayed discount-usage recompute on the order-events queue (per [[discount]]).
- **Customer email** — when the configured "paid" / "shipped" / "fulfilled" / etc. status fires, the matching customer notification email goes out (subject to the per-order `notify_customer` flag and the store-wide notification toggle — see [[orders-notify-customer]]).
- **Webhooks** — `order.updated` fires on every PATCH; status-specific webhooks (`order.paid`, `order.cancelled`, etc.) fire per [[settings-hooks]] subscriptions.
- **Audit log** — the order's [[orders-history]] records `namespace = "api2"` for the actor — surfaced as **"API"** in the merchant's order-history view. This is **the** audit log on the platform: the only entity that captures who changed what at the API level with this fidelity.

**Invoice / USN single-write.** A PATCH on `usn` runs a uniqueness check across all orders and writes the value; it can only be set once. A PATCH on `invoice_number` runs a uniqueness check, auto-stamps `invoice_date = now` if empty, and rejects subsequent writes. A PATCH on `invoice_date` writes immediately with no auto-recalculation.

**The `/fulfill` custom action.** A **PATCH `/orders/{id}/fulfill`** runs the validators (USN, invoice number, status) but the fulfillment cascade itself happens through [[api-order-fulfillment]] — that page documents the side-effect chain (inventory decrement, invoice / receipt number generation, history entry, payment auto-capture, async webhooks, customer email). It is the only "create-like" call on the orders resource.

**The `/order-status` helper.** A **GET `/api/v2/order-status`** has no side effects — it returns the merchant's configured order-status list (built-ins + custom) in a NON-JSON:API shape (`{data: [{id, name, slug, status_type}, ...]}`), useful for picker UIs that need the current set of valid status keys before PATCHing. Optional `?filter[<key>]=<value>` scopes the list.

**Blocked verbs.** `POST /orders` and `DELETE /orders/{id}` both return **405 Method Not Allowed** at the routing layer — order creation goes through storefront checkout or [[orders-add]]; cancellation goes through a status change and long-term cleanup through [[orders-archive]].

**Plan-feature gating:** none unique to `orders`. Standard JSON-API v2 plan checks apply (rate limit per plan — see [[platform-rate-limits]] — and 402 if the plan is expired or past-due).

**Common 422 cases:**

- `{"errors":[{"status":"422","source":{"pointer":"/data/attributes/status"},"detail":"Invalid status. You can use one of: pending, paid, fulfilled, ..."}]}` — invalid status key sent.
- `{"errors":[{"status":"422","source":{"pointer":"/data/attributes/status"},"detail":"<gate violation message>"}]}` — valid status but the transition gate blocks it.
- `{"errors":[{"status":"422","source":{"pointer":"/data/attributes/usn"},"detail":"You can set USN only once"}]}` — USN already set.
- `{"errors":[{"status":"422","source":{"pointer":"/data/attributes/usn"},"detail":"The usn has already been taken."}]}` — USN already used by another order.
- `{"errors":[{"status":"422","source":{"pointer":"/data/attributes/invoice_number"},"detail":"You can set invoice number only once."}]}` — invoice number already set.
- `{"errors":[{"status":"422","source":{"pointer":"/data/attributes/invoice_number"},"detail":"The invoice number has already been taken."}]}` — invoice number already used by another order.

## Equivalent UI

- [[orders-status-change]] — the status pill runs this exact cascade; the API PATCH has no fast path around it.
- [[orders-shipping-waybill]] — the admin **Save waybill** action is the UI counterpart of the `/fulfill` call.
- [[orders-history]] — the merchant-visible audit log where the `api2` ("API") actor entry lands.

## Related

- [[api-orders]] — hub.
- [[api-orders-attributes]] — the four writable attributes that drive this cascade.
- [[order-processing-pipeline]] — the full status-transition side-effect catalogue.
- [[order-status-workflow]] — transition rules + hard gates.
- [[api-order-fulfillment]] — the cascade behind `/fulfill`.
- [[inventory-decrement-timing]] — when a status change drops stock.
- [[inventory-restock]] — stock auto-return on cancel / refund / void.
- [[background-queue-inventory]] — async inventory + search-sync chain.
- [[orders-payment-capture]] / [[payment-provider-mechanism]] — payment-hold cancellation on negative status.
- [[orders-notify-customer]] — the per-order email gate.
- [[settings-hooks]] — `order.updated` + status-specific webhook subscriptions.
- [[orders-history]] — the `api2` audit entry.
- [[platform-rate-limits]] — per-plan rate limits / 402.
- [[discount]] — the 10-second discount-usage recompute.

## Open questions

- Document the exact stack of webhook events that fire when a single PATCH crosses multiple status boundaries (e.g. `pending → paid → fulfilled → completed` via the auto-promotion side effect — does each transition fire its own webhook, or only the final state?). `(verify)`
- Verify whether the order's `status_archive` JSON column (per [[order-status]] business rules) records the API actor identifier accurately for support investigations against PATCH-driven status changes. `(verify)`
