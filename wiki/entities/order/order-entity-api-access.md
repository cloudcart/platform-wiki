---
type: entity
nav_path: "Entity → Order → Programmatic access (JSON-API v2)"
aliases: ["Order API", "JSON-API v2 orders", "Order PATCH", "Order fulfillment API", "api2 order writes", "Order sub-resources API"]
tags: [entity, orders, api, json-api-v2, programmatic]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[order]]. See the hub for the other aspects (identifiers, lifecycle, money, side-effects).

# Order — Programmatic access (JSON-API v2)

## Identity

The Order entity is exposed via **JSON-API v2** at `/api/v2/orders` — see [[api-orders]] for the canonical endpoint page. The API is **read + limited mutation**: integrations can read the full order graph (and most sub-resources via `?include=`), PATCH a small set of order-level attributes (`status`, `note_administrator`, `notify_customer`), and create / delete `order-fulfillment` records. They CANNOT create new orders, hard-delete orders, mutate addresses / line items / discounts, or trigger payment lifecycle actions (mark-paid / capture / cancel / refund / manual-confirm — admin-panel only).

The defining principle of the API is the **same-side-effects rule** — any allowed mutation runs through the EXACT same model pipeline as the admin-panel action that does the same thing. PATCHing `status` through the API runs `validateChangeStatus`, fires the same webhooks, writes the same [[orders-history]] row (tagged `api2` as the acting namespace), runs the same auto-promotion, the same stock effects, the same discount-uses counter increment, the same customer email. See [[json-api-v2]] for the side-effects principle in full.

## Aliases

- **`/api/v2/orders`** — the resource path.
- **`api2` acting namespace** — the audit-log Initiator value used when API mutations run.
- **PATCH order** / **PATCH status** — the dominant mutation path.
- **Order fulfillment API** — the only writable sub-resource (create + delete).

## Key Attributes

### Allowed operations

The API supports:

| Operation | Path | Effect |
|-----------|------|--------|
| READ | `GET /api/v2/orders` | List orders, with `filter[*]` + pagination per [[api-orders]]. |
| READ | `GET /api/v2/orders/{id}` | Read a single order with sub-resources via `?include=`. |
| MUTATE | `PATCH /api/v2/orders/{id}` | Update a small set of order-level attributes (see below). |
| MUTATE | `POST /api/v2/orders/{id}/relationships/fulfillment` | Create a fulfillment record (verify the exact path). |
| MUTATE | `DELETE /api/v2/orders/{id}/relationships/fulfillment` | Delete a fulfillment record (verify). |

### Forbidden operations

The API explicitly does **NOT** allow:

- **`POST /api/v2/orders`** — orders cannot be created via the API. Use storefront checkout or [[orders-add]] admin manual-order flow.
- **`DELETE /api/v2/orders/{id}`** — orders cannot be hard-deleted via the API. Use archive instead — see [[orders-archive]].
- **Payment lifecycle actions** — `mark-paid` / `capture` / `cancel` / `refund` / `manual-confirm` are all admin-panel only. The API does NOT have endpoints for these actions.
- **Sub-resource mutation** — addresses, line items, discounts are read-only via the API. The merchant must use the corresponding admin-panel feature to mutate them.

### Sub-resources (read-only via `?include=`)

The Order's sub-resources hang off `/api/v2/orders/{id}/relationships/{name}`. The full list lives on [[api-orders]]; the major ones:

- [[api-order-products]] — line items (read-only).
- [[api-order-payment]] — payment records (read-only).
- [[api-order-shipping]] — shipping data (read-only).
- [[api-order-discount]] — order-level discount (read-only).
- [[api-order-shipping-address]] — shipping address snapshot (read-only).
- [[api-order-billing-address]] — billing address snapshot (read-only).
- [[api-order-fulfillment]] — fulfillment records (**writable** — POST + DELETE).
- [[api-order-tax]] — tax breakdown (read-only).
- [[api-order-total]] — totals (read-only).
- [[api-order-modification]] — modifications (read-only — verify).

### PATCH-able attributes

The settable set is small. The verbatim list (verify against `api2/Modules/Orders/Order/Validators.php`):

| Attribute | Effect of writing |
|-----------|-------------------|
| `status` | Runs through `validateChangeStatus` (see [[order-entity-lifecycle]]) — gates apply. Fires the same webhooks + history rows as the admin pill. |
| `note_administrator` | Edits the internal-only admin note. Fires `order.updated`. |
| `notify_customer` | Toggles the per-order email-suppression flag. Fires `order.updated`. |

The verbatim list of API-settable order attributes is intentionally narrow — most order-level fields are read-only to integrations to avoid bypassing the admin's interactive flows (which run additional UI-side validation).

### `validateChangeStatus` runs on PATCH

API PATCH of `status` goes **through the validate path**, NOT the direct programmatic `changeStatus` path. This means the same three guards apply (see [[order-entity-lifecycle]]):

- `completed` rejected unless `paid + status_fulfillment = fulfilled`.
- `cancelled` rejected if order is currently `paid` or `completed`.
- Any change on an archived order rejected.

So the API can NOT be used to bypass status-transition guards. Gateway-sync paths that legitimately need to overwrite use the **direct `changeStatus`** path, which is **internal-only** — not exposed via the JSON-API.

### Same side effects on mutation

Every allowed mutation runs through the same model pipeline as the admin-panel equivalent:

1. **Validation** — same Validators, same error strings.
2. **`validateChangeStatus` guards** (if status is changing).
3. **`saving` hook auto-promotion** — `paid + fulfilled + order_complete = 1` → `completed`.
4. **Banned-IP listener** (on order-create — but order-create isn't exposed; on status change, the listener doesn't re-check).
5. **Stock decrement / increment** — same `order_status_for_quantity_decrease` setting respected.
6. **Discount uses counter** — same `discounts_used_statuses` rule.
7. **Customer email** — same `notify_customer` gate, same [[settings-statuses]] per-status toggle.
8. **Webhook fan-out** — `order.created` (only on the original create), `order.updated` (on every PATCH), `order.deleted` (only on hard-delete, which isn't exposed via the API).
9. **History row** — written with `api2` as the acting namespace / Initiator. The merchant can see exactly which changes came from the API vs from the admin panel on [[orders-history]].

### Acting namespace = `api2` on history rows

Every API-driven mutation writes a row to [[orders-history]] with the **acting namespace** set to `api2`. The merchant sees this on the per-order history log and on [[products-change-log]] for stock changes resulting from API order PATCHes. This makes "an unknown system changed the order" tickets traceable — see the debugging-playbook patterns on [[inventory-debugging-playbook]] for the analogous stock-change case.

### Authentication + rate limit

The API uses [[settings-api-keys|PAT-token authentication]] — see [[pat-token]] for the token entity. Rate limits + auth model live on [[json-api-v2]].

### What a a support ticket ticket says when the API mutated an order

Common merchant-facing patterns:

- *"My order #1234 changed status but no one on the team touched it"* — check [[orders-history]] for the row with acting namespace `api2`. The Initiator + API key identify the integration.
- *"Stock dropped on Product X and no one updated it"* — same workflow via [[products-change-log]] — see [[inventory-debugging-playbook]] step 4.
- *"Customer says they got a shipment notification we didn't send"* — API fulfillment-create fires the same notification chain. Check [[api-order-fulfillment]] for who created the fulfillment row.

## Where it appears

- [[api-orders]] — the canonical JSON-API v2 endpoint page.
- [[api-order-products]] / [[api-order-payment]] / [[api-order-shipping]] / [[api-order-discount]] / [[api-order-shipping-address]] / [[api-order-billing-address]] / [[api-order-fulfillment]] / [[api-order-tax]] / [[api-order-total]] / [[api-order-modification]] — sub-resource endpoints.
- [[orders-history]] — audit log; rows from API mutations carry the `api2` acting namespace.
- [[settings-api-keys]] — PAT-token issuance (the API auth surface).
- [[settings-hooks]] — webhook subscribers (the same hooks fire for API mutations).
- [[json-api-v2]] — JSON-API v2 architecture, auth, rate-limit, side-effects principle.

## Related

- [[order]] — hub.
- [[order-entity-lifecycle]] — `validateChangeStatus` runs on PATCH.
- [[order-entity-side-effects]] — same side effects fire on API mutations.
- [[order-entity-money]] — payment-lifecycle actions are NOT exposed via the API.
- [[api-orders]] — canonical endpoint page.
- [[json-api-v2]] — API hub.
- [[settings-api-keys]] — PAT-token auth.
- [[pat-token]] — token entity.
- [[settings-hooks]] — webhook fan-out (same hooks as admin).
- [[order-status-entity-api-access]] — order-status-side API mechanics (the 6 settable + 5 gateway-only split lives there).
- [[inventory-debugging-playbook]] — debugging the `api2` Initiator pattern for stock changes.

## Open Questions

- The exact verbatim path for fulfillment create/delete: `/api/v2/orders/{id}/relationships/fulfillment` (verify against `api2/Modules/Orders/OrderFulfillment/Schema.php`).
- The verbatim list of PATCH-able attributes — current understanding is `status`, `note_administrator`, `notify_customer` (verify against `api2/Modules/Orders/Order/Validators.php`).
- Whether `order-modification` is read-only or has a write surface (verify).
- Whether the API can read archived orders by default or requires an explicit `filter[archived]` (verify against [[api-orders]]).
