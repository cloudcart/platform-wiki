---
type: entity
nav_path: "Entity → Customer"
route_name: (none)
route_path: (none)
aliases: ["Customer", "Buyer", "Shopper", "Account holder", "Storefront account", "Клиент", "Купувач", "Потребител"]
tags: [entity, customers, core]
plan_gates: ["customers"]
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---

# Customer

## Identity

A **Customer** is a buyer of the merchant's store — either a **registered** account (someone who created a login with email + password) or a **guest** (someone who placed an order without creating an account). Every order has exactly one Customer attached; the platform creates a guest Customer record on the fly at checkout when the buyer does not log in.

The Customer carries identity (first name, last name, email, optional alternative phone), addresses (separate billing-address and shipping-address tables with multiple supported), marketing-consent flags, login credentials (registered only), assignment to a [[customer-group|Customer Group]] (loyalty / discount tier), and running lifetime totals (completed-orders count, lifetime revenue, last order date, income).

A Customer is **distinct from a [[subscriber|Subscriber]]**: a Customer has placed an order or registered for an account; a Subscriber is anyone who has opted in to receive marketing (newsletter signup, web-push acceptance, etc.) — see [[subscriber-vs-customer]]. The two overlap when a customer also opts in to marketing, but they are NOT the same record.

The customer count is plan-gated under the `customers` plan-feature key. The page where the merchant manages them is [[customers]]; the detail view is [[customers-details]] and its sub-tabs.

## Aliases

- **Customer** — the standard merchant-facing term across admin UI and storefront.
- **Buyer** / **Shopper** / **Account holder** — informal merchant phrasing.
- **Storefront account** — used when contrasting with admin / staff accounts.
- **Клиент** / **Купувач** / **Потребител** — Bulgarian terms used interchangeably.

## Key Attributes

The Customer is a multi-faceted record split across **six well-scoped aspects**. The AI Assistant should drill into the aspect that matches the question, not read every page.

- [[customer-entity-attributes]] — the full per-field schema (identity, status flags, addresses, aggregates, validation constraints, error keys, `customer_name_display` setting).
- [[customer-entity-lifecycle]] — the seven named states (Guest, Pending confirmation, Active, Inactive, Banned, Marketing-suppressed, Deleted), save-time transitions, `add` vs `addGuest` factory entry points, guest dedup at checkout, `convertGuestToCustomer` promotion, `isEmpty` deletion protection.
- [[customer-entity-status-flags]] — the three independent flags `active` / `banned` / `marketing` and how they gate login, ordering, marketing sends. Ban requires non-empty `banned_reason`; banning does NOT email the customer.
- [[customer-entity-relationships]] — orders, addresses (multi with one default per type), customer group (required), customer tags, subscriber segments, custom fields, favorites, social accounts, saved cards, carts. Plus the Customer ≠ Subscriber boundary.
- [[customer-entity-auth]] — password rules (3-20 chars; storefront requires `password_old`, admin doesn't), email-confirmation flow, `unconfirmed_accounts_restrict` (`none` / `checkout`), email-change re-confirmation handshake via `email_for_confirmation`, social-account linking, saved-payment tokens (`epay_one_touch`, `stripe`, `mypos`, `raiffeisen`, `borica_way4` — NEVER exposed in API).
- [[customer-entity-api-and-webhooks]] — JSON-API v2 endpoints, `customer.created` / `customer.updated` / `customer.deleted` webhooks + distinct `RegisterGuest` event, `customers` plan-cap, aggregate-stats recalc, EUR / BGN fixed-rate (`1.95583`) conversion in lifetime totals, full validation-error catalogue, deletion cascade (carts wiped, orders orphan).

## Why it matters to the merchant

The Customer record is where **identity, marketing consent, order history, and financial trust** intersect. Five high-impact behaviours the merchant should understand:

- **Customer ≠ Subscriber.** Same email may be both, but they are independent records with independent lifecycles. Disabling marketing on one does not disable the other. See [[subscriber-vs-customer]].
- **Three independent flags — no cascade.** Toggling Active off does NOT revoke marketing consent. Banning does NOT auto-deactivate. Each flag is set independently. See [[customer-entity-status-flags]].
- **Deletion orphans orders.** Hard-deleting a customer wipes carts but **leaves orders behind** with a dangling `customer_id`. To preserve order history while preventing further activity, use **Ban** or **Deactivate** — never Delete. See [[customer-entity-lifecycle]].
- **Guest dedup is per-scope.** A registered customer's email does NOT block a guest checkout with the same email — the two records coexist until manual merge. See [[customer-entity-lifecycle]].
- **Aggregates lag.** `income`, `completed_orders`, and `last_order_date` are pre-aggregated snapshots updated by the recalc service on order-status changes, not live-computed on every read. See [[customer-entity-api-and-webhooks]].

## Where it appears

- [[customers]] — the main customer list (search, filter, bulk actions, header create).
- [[customers-details]] — per-customer wrapper that hosts the sub-tabs.
- [[customers-details-overview]] — overview tab (identity, stats, notes).
- [[customers-details-orders]] — order-history sub-tab.
- [[customers-details-products]] — products bought sub-tab.
- [[customers-details-payments]] — payments sub-tab.
- [[customers-details-shipping-addresses]] / [[customers-details-billing-addresses]] — address management.
- [[customers-details-reviews]] — product reviews left by the customer.
- [[customers-sign-in]] — impersonation (log in as the customer).
- [[customers-change-password]] — set a specific new password (NOT a reset link).
- [[customers-custom-fields]] — custom-field definitions populated per customer.
- [[customers-custom-groups]] — customer-group (loyalty tier) definitions.
- [[customers-export]] / [[customers-import]] — bulk export / import.
- [[reports-customers]] — analytics + chart for customer registrations and revenue.

## Related

### Related entities

- [[customer-group]] — required group assignment per customer; drives discount tier.
- [[subscriber]] — marketing-consent record. Customers and Subscribers can share an email but are independent.
- [[segment]] — subscribers (and customers who are also subscribers) belong to segments.
- [[order]] — every Order belongs to one Customer.
- [[cart]] — abandoned + active carts owned by the customer.
- [[invoice]] / [[credit-note]] — financial documents tied to the customer's orders.
- [[product]] — customers favorite and buy products (see [[products-favorite-products]]).
- [[discount-code]] — discount codes can target specific customers / groups.
- [[webhook]] — `customer.*` event subscriptions.

### Cross-cutting concepts

- [[subscriber-vs-customer]] — the canonical distinction that confuses many merchants.
- [[checkout-flow]] — how a guest Customer is created at checkout vs how a registered Customer is recognised.
- [[notification-delivery]] — how customer-level and subscriber-channel consent layers gate marketing sends.
- [[plan-gates]] — the `customers` count cap.
- [[merchant-roles]] — moderator permissions for the Customers section.

### Settings & webhooks

- [[settings-hooks]] — `customer.created`, `customer.updated`, `customer.deleted` webhook events.
- [[settings-banned-ip]] — distinct concept from customer-account ban: order-IP-level rejection at order placement.
- [[settings-staff]] — moderator permission grants for accessing the Customers section.
- [[settings-cart]] — `customer_name_display`, `unconfirmed_accounts_restrict`, "Convert guests into members" toggles.
- [[json-api-v2]] — programmatic-access hub.

## Open Questions

Distributed to aspect pages. See:

- [[customer-entity-status-flags]] — precedence of `Customer.marketing` vs `SubscriberChannel.marketing`.
- [[customer-entity-lifecycle]] — guest-to-registered promotion when the same email later registers.
- [[customer-entity-api-and-webhooks]] — aggregate-recalc timing on retroactive order-status changes.
