---
type: entity
nav_path: "Entity → Customer → API, webhooks & aggregate stats"
aliases: ["Customer API", "Customer webhooks", "Customer plan gate", "Customer income recalc", "Customer aggregate stats", "Customer validation errors", "Programmatic customer access"]
tags: [entity, customers, api, webhooks, plan-gates, aggregates]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customer]]. See the hub for the other aspects (attributes, lifecycle, status flags, relationships, auth + email).

# Customer — API, webhooks & aggregate stats

## Identity

The programmatic surface for the [[customer|Customer]] record — JSON-API v2 endpoints, lifecycle webhooks (`customer.created` / `customer.updated` / `customer.deleted` + the distinct `RegisterGuest` event), the `customers` plan-cap, the income-recalc aggregate-stats snapshot, the full validation-error catalogue, and the EUR / BGN currency-conversion rule.

## Aliases

- **Customer API** — JSON-API v2 programmatic CRUD.
- **Customer webhooks** — `customer.*` event subscriptions.
- **Customer plan gate** — the `customers` plan-feature key.
- **Aggregate stats** / **Income recalc** — `income`, `completed_orders`, `orders_total`, etc.

## Key Attributes

### Programmatic access via JSON-API v2

Customer records can be **read, created, updated, or deleted** via JSON-API v2 — see [[api-customers]] for endpoints, attributes (identity, three status flags, group_id, KPI snapshots, default-address pointers), and validation. Related resources:

- [[api-customer-groups]]
- [[api-customer-shipping-address]]
- [[api-customer-billing-address]]
- [[api-customer-tags]]

**Same side effects apply.** Creates / updates / deletes through JSON-API v2 fire the same lifecycle as admin-panel operations:

- `customer.created` / `customer.updated` / `customer.deleted` webhooks.
- Guest dedup at create-time on email match (see [[customer-entity-lifecycle]]).
- `email_for_confirmation` pending-state flow on email change (see [[customer-entity-auth]]).
- `RegisterGuest` distinct event for `group_id = guests`.
- `CustomerMarketingChange` segment recompute when `marketing` flips.
- `CustomerTagChange` propagation to Subscriber (verify).
- Income-KPI recalc on aggregate change.
- Cart cascade-delete + Subscriber removal on hard delete (orders are NOT deleted, they orphan).

**Same protection layer**:

- `customers` plan-cap enforced (exceeding the cap blocks new customer creation through the API).
- Email uniqueness within the store's customer table (per-scope: `customer` vs `guest` scopes).
- Password 3-20 chars; note 191-char cap; libphonenumber phone format check.
- Banned customers cannot place orders even if the order is created via API.

**Saved payment tokens** (`epay_one_touch`, `stripe`, `mypos`, `raiffeisen`, `borica_way4`) are NEVER exposed in API responses — same as admin export. See [[customer-entity-auth]].

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

### Webhooks fired by the Customer model

The Customer model fires three webhook events to [[settings-hooks]]:

| Event | When it fires | Notes |
|-------|---------------|-------|
| `customer.created` | After a customer is created (registered OR guest) | Both `add` and `addGuest` paths fire this. See [[customer-entity-lifecycle]]. |
| `customer.updated` | On save when fields change | Chatty; receivers should be idempotent. |
| `customer.deleted` | After hard-delete | Fires AFTER cascade (carts already wiped). |

There is a separate **`RegisterGuest`** event (distinct from `Registered`) for the guest-creation case to let listeners distinguish guest creation from full registration — used to skip welcome emails for guests.

### Plan gate — `customers` count

The plan-feature key **`customers`** caps the total customer count (registered + guest). When the merchant exceeds the cap, **NEW customer registration (and guest creation at checkout) is gated** by the plan-restriction layer. Existing customers continue to work. See [[plan-gates]].

This cap applies to both:

- Admin-panel "Add customer" via [[customers]].
- JSON-API v2 customer creation.
- Storefront registration.
- Guest-customer creation at checkout (this can break checkout when the cap is hit — surface to the merchant via the plan-upgrade prompt).

### Email is the unique identifier for registered customers

A registered customer (`group_id != guests-group-id`) is uniquely identified by **email**. The `existsByEmail` check prevents two registered customers with the same email.

**Guest customers with the same email CAN coexist** with a registered customer — the scopes `customer` and `guest` filter them apart. This is why a guest checkout from a buyer who also has a registered account creates a parallel record (see [[customer-entity-lifecycle]] for the dedup rule at checkout).

### Validation-error catalogue

The full set of validation errors customers can hit during admin or API create / edit:

| Error key | When it fires |
|-----------|---------------|
| `customer.err.email_required` | Email field empty. |
| `customer.err.email_taken` | Another customer already uses this email (case-sensitive comparison; `WHERE email = '...'`). |
| `customer.err.no_longer_exists` | The customer record being edited has been deleted concurrently (race condition). |
| `customer.err.note_max_chars_191` | Note exceeds 191 chars. |
| `customer.err.password_min_chars_3` | Password too short. |
| `customer.err.password_max_chars_20` | Password too long. |
| `customer.err.passwords_mismatch` | `password` and `password_repeat` differ. |
| `customer.err.invalid_old_password` | `password_old` doesn't match the current hash (storefront only). |
| `customer.err.user_banned` | Tried to place an order on a banned customer (admin-side). |
| `customer_group.err.choose` | `group_id` is missing or invalid. |
| `customer_group.err.no_longer_exists` | The group was deleted between form-load and submit. |

Storefront-specific runtime errors (not validation):

- `'sf.err.account.inactive'` — login attempt against `active = no` customer.
- `'sf.global.err.customer_banned'` — login or order placement against `banned = yes` customer.

See [[customer-entity-status-flags]] for the runtime errors.

### Aggregate stats — pre-computed snapshots

`income`, `completed_orders`, `orders_total`, `orders_total_price`, `last_order_date` are **pre-aggregated snapshots** updated by the income-recalculation service when orders change status. They are **NOT live-computed** on every read.

The recalc service updates:

- `income` — completed-orders sum.
- `completed_orders` — count of completed orders.
- `orders_total` — count of all orders (incl. cancelled).
- `orders_total_price` — sum of all order prices.
- `last_order_date` — most-recent completed-order date.
- `income_updated_at` — recalc timestamp.

It is **triggered on order status changes**, not on every customer-detail read. If the merchant deletes an order, these stats are refreshed accordingly.

### EUR / BGN currency-conversion in aggregates

When the store currency is **EUR**, the lifetime-revenue calculator converts BGN-denominated orders to EUR using the **fixed rate `1.95583` BGN/EUR** before summing. So a store that started in BGN and later switched to EUR will see **consistent EUR totals** across the customer's order history regardless of which currency the individual orders were placed in.

For BGN-store records (or other store currencies), **no conversion happens** — orders are summed in their stored `price_total` units.

### Deletion cascade — what survives

On hard-delete:

- All `Cart` rows where `user_id = customer.id` are deleted (cascade).
- Subscriber removal fires if applicable.
- `customer.deleted` webhook fires.
- **Orders survive but become orphaned** — the bulk-delete endpoint does NOT block when the customer has orders. The cascade only wipes carts; orders remain in the system with a now-dangling `customer_id` reference.

To preserve order history while preventing further customer activity, use **Ban** or **Deactivate** instead of Delete — see [[customer-entity-status-flags]].

## Where it appears

- [[api-customers]] — JSON-API v2 customer endpoint.
- [[api-customer-groups]] / [[api-customer-shipping-address]] / [[api-customer-billing-address]] / [[api-customer-tags]] — related API resources.
- [[settings-hooks]] — webhook subscription UI; lists the three `customer.*` events.
- [[plan-gates]] — the `customers` cap surfaces here.
- [[reports-customers]] — analytics chart consumes aggregate stats.
- [[customers-details-overview]] — surfaces aggregate stats per customer.

## Related

- [[customer]] — hub.
- [[customer-entity-lifecycle]] — `RegisterGuest` and add vs addGuest factories.
- [[customer-entity-status-flags]] — runtime errors `sf.err.account.inactive` / `sf.global.err.customer_banned`.
- [[customer-entity-auth]] — saved-payment-token exclusion from API.
- [[json-api-v2]] — authentication + rate limit + side-effects principle.
- [[plan-gates]] — `customers` plan-feature key.
- [[settings-hooks]] — webhook delivery.

## Open Questions

- ⏸️ What happens to the customer's `last_order_date` / `income` snapshot when the merchant manually changes an order's status retroactively — is the recalculation immediate or queued?
- ⏸️ Whether `CustomerTagChange` propagation to the Subscriber record is automatic or requires the customer-tag setting to be on (verify).
