---
type: entity
nav_path: "Entity → Customer → Lifecycle"
aliases: ["Customer lifecycle", "Customer states", "Guest to registered", "Customer states transitions", "Customer deletion cascade"]
tags: [entity, customers, lifecycle, states]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customer]]. See the hub for the other aspects (attributes, status flags, relationships, auth + email, API + webhooks).

# Customer — Lifecycle

## Identity

The complete state machine a [[customer|Customer]] record can pass through — from guest creation at checkout, through pending-confirmation, active, inactive, banned, marketing-suppressed, all the way to hard-delete. Also documents the save-time transitions (email change, address default, guest-to-customer promotion) and the deletion cascade.

## Aliases

- **Customer states** — the six (+ deleted) named states a customer can occupy.
- **Customer lifecycle** — the transitions between them.
- **Guest-to-registered promotion** — the `convertGuestToCustomer` flow.

## Key Attributes

The seven named states:

| State | How to recognise | What it blocks |
|-------|------------------|----------------|
| **Guest** | `group_id = <guests-group-id>`, no password | No storefront login (no password). Subsequent guest orders with the same email typically attach to the same Guest record. |
| **Pending confirmation** | `email_confirmed = no`, registered (non-guest group) | Depending on `unconfirmed_accounts_restrict`, login or checkout may be restricted. See [[customer-entity-auth]]. |
| **Active** | `active = yes`, `banned = no` | Nothing — standard live state. Can log in, place orders, manage addresses, change password. |
| **Inactive** | `active = no` | Storefront login throws `'sf.err.account.inactive'`. Past orders remain intact. The merchant can re-enable by toggling `active = yes` (inline toggle on [[customers]]). |
| **Banned** | `banned = yes`, `banned_reason` filled, `date_banned` set | Login AND order placement. Detail page shows a red **Banned** chip. Storefront: `'sf.global.err.customer_banned'`. Admin: `'customer.err.user_banned'`. See [[customer-entity-status-flags]]. |
| **Marketing-suppressed** | `marketing = no` | Excluded from marketing campaign sends (newsletters, promo blasts). Does NOT block transactional emails (order confirmation, password reset, etc.). |
| **Deleted** | Record removed (hard delete) | All `Cart` rows (where `user_id = customer.id`) are cascade-deleted. `customer.deleted` webhook fires. **Orders survive but become orphaned** — the bulk-delete endpoint does NOT block when the customer has orders. |

The three operational flags — `active`, `banned`, `marketing` — are **independent** (see [[customer-entity-status-flags]]). Banning does NOT auto-deactivate, deactivating does NOT auto-clear marketing consent, and clearing marketing consent does NOT deactivate the account.

### Save-time transitions

- **Registered guest event** — when a customer is created with `group_id = <guests-group-id>`, the platform fires a special `RegisterGuest` event (distinct from the normal `Registered` event). Listeners use this to skip welcome emails for guests.
- **Email change** — modifying `email` flips `email_confirmed` back to `no`, stores the new value in `email_for_confirmation`, and triggers a new confirmation email. See [[customer-entity-auth]] for the full re-confirmation flow.
- **Address create / delete** — first-created address auto-becomes the default; deleting the default address requires picking a new default (or clears the default). See [[customer-entity-relationships]].
- **Ban / unban** — bulk ban and per-customer ban share the same path (accepts single ID or array). Unban clears `banned`, `banned_reason`, AND `date_banned` in one call. Ban preserves the reason for audit. **No history of past bans is retained** — only the most recent reason.

### Convert-guest-to-customer flow

When a guest places a second order and the storefront is configured for "Convert guests into members" ([[settings-cart]]), the platform calls `convertGuestToCustomer` which:

1. Moves the customer from the Guests group to the **Default group**.
2. Generates a random **8-char password**.
3. Marks the email as `confirmed`.
4. Optionally logs the customer in immediately and fires both `Login` and `CustomerCreated` events.

This is the **only path** that "promotes" a guest into a registered account. There is no manual "Promote guest to customer" admin action — it's tied to the second-order moment.

### Guest dedup at checkout

When a buyer checks out as a guest, the platform looks up an existing GUEST customer (scope `guest`) by email **first**:

- If a guest with the same email exists → that record is **reused** and the new order is attached to it.
- If only a REGISTERED customer has the email → a **NEW guest record** is created. The platform does NOT promote the registered account or attach the order to it.

So a buyer who has a registered account but proceeds as guest creates a **parallel guest record** with the same email; both records coexist until manual merge.

### `add` vs `addGuest` factory entry points

The platform exposes two factory entry points with different defaults:

- **`addGuest`** (used at checkout) — sets `group_id = <guests-group-id>`, forces `marketing = no`, `banned = no`, `imported = no`, and skips the welcome-email branch.
- **`add`** (used by the admin "Add customer" form on [[customers]]) — goes through full validation, group resolution, and triggers the welcome / confirmation emails per the store's `unconfirmed_accounts_restrict` setting.

Both fire `customer.created` (see [[customer-entity-api-and-webhooks]]).

### `isEmpty` protection against accidental deletion

The Customer has an `isEmpty` check that returns `true` only when the customer has **NO shipping addresses, NO billing addresses, AND NO orders**. Flows that respect this check refuse to delete non-empty customers. The merchant should **archive (deactivate) non-empty customers** rather than deleting them — historical order data orphans otherwise.

**Caveat**: the [[customers]] bulk-delete endpoint does NOT honour this check — see the deletion cascade row above. To preserve order history while preventing further customer activity, use **Ban** or **Deactivate** instead of Delete.

### Ban does NOT email the customer

A ban takes effect silently from the customer's perspective. There is **no automated email** or any other notification telling them the account was banned. The customer only discovers the ban when they next try to log in or place an order (the storefront returns a generic block message). Merchants who need to communicate the ban must email the customer separately.

### Guest customers — special-case lifecycle

Guests share most of the lifecycle but with carve-outs:

- Have **no password**; cannot log in.
- Are still subject to `banned`, but `active` toggles are irrelevant since there's no login.
- Can still receive **transactional** emails (order confirmation, etc.).
- Are excluded from many merchant-facing filters (e.g., the [[customers]] list typically filters out guests via the `customer` scope; guests are listed separately or under a guest filter).

## Where it appears

- [[customers]] — list view; bulk Ban / Deactivate / Delete actions; the Active toggle inline.
- [[customers-details]] / [[customers-details-overview]] — per-customer header shows the chips (Active / Inactive / Banned / Marketing-suppressed).
- [[checkout-flow]] — guest dedup and guest-to-customer promotion happen here.
- [[settings-cart]] — `unconfirmed_accounts_restrict` and "Convert guests into members" toggles drive lifecycle transitions.

## Related

- [[customer]] — hub.
- [[customer-entity-status-flags]] — the three independent flags.
- [[customer-entity-auth]] — email confirmation + password mechanics.
- [[settings-cart]] — the toggles that drive guest conversion and unconfirmed-account restriction.
- [[checkout-flow]] — guest dedup happens at checkout.

## Open Questions

- ⏸️ The precise rule for when a guest customer is "promoted" to a registered customer if the same email later registers — is the guest record merged with the new registered record, or do they stay separate?
