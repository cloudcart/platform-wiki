---
type: entity
nav_path: "Entity → Customer → Key attributes"
aliases: ["Customer attributes", "Customer fields", "Customer validation", "Customer record fields"]
tags: [entity, customers, attributes, validation]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customer]]. See the hub for the other aspects (lifecycle, status flags, relationships, auth + email, API + webhooks).

# Customer — Key attributes

## Identity

The full per-field schema for the [[customer|Customer]] record — every attribute the merchant configures or sees, with its purpose, defaults, and validation. This page is the reference the AI Assistant cites when a merchant asks *"What goes in field X?"* or *"Why is my customer save failing?"*.

## Aliases

- **Customer attributes** / **Customer fields** — the per-record field definitions.
- **Validation constraints** — the create / edit rules surfaced by `customer.err.*` translation keys.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| `first_name`, `last_name` | Customer's name | Both required at create. Displayed concatenated per the `customer_name_display` setting (default `{first_name} {last_name}`). |
| `email` | Email address | The primary identifier — uniquely identifies a registered customer. Required. Also the login username for storefront login. |
| `alternative_phone` | Backup phone | Optional. Distinct from address-level phone — used for admin-side contact. |
| `password` + `salt` | Storefront login credentials | Hashed; never exposed in API responses. Set on register; updated via [[customers-change-password]] (admin sets a specific value) or via the storefront's "Forgot password" / reset-link flow. See [[customer-entity-auth]]. |
| `group_id` | FK → [[customer-group]] | Required. Determines which customer-group discounts and pricing apply. The platform reserves a special "Guests" group ID for guest customers; everyone else is a `Registered` customer. |
| `active` | yes / no | Master account-enabled flag. When `no`, the storefront login throws the `'sf.err.account.inactive'` error and blocks login. Past orders remain intact. See [[customer-entity-status-flags]]. |
| `banned` | yes / no (stored 0/1) | Disciplinary lock. Banned customers cannot log in OR place orders (`'sf.global.err.customer_banned'` on storefront, `'customer.err.user_banned'` in admin contexts). |
| `banned_reason` | Free text | REQUIRED when banning — the Ban modal's Confirm button stays disabled until a reason is typed. Cleared automatically on unban. |
| `date_banned` | Datetime when banned | Set when banned, cleared on unban. |
| `marketing` | yes / no | Customer-level "accept marketing" consent. When `no`, the customer is excluded from marketing campaigns even if active. (Distinct from per-channel Subscriber consent — see [[customer-entity-relationships]].) |
| `newsletter` | yes / no | Legacy newsletter-opt-in flag — many places still write to it from form posts where `newsletter_subscribe` is present. Newer marketing model uses [[subscriber|Subscriber]] / SubscriberChannel records instead. |
| `email_confirmed` | yes / no | Whether the customer has verified their email via the confirmation link. When `no`, depending on `unconfirmed_accounts_restrict` (`none` / `checkout`), login or checkout may be restricted. See [[customer-entity-auth]]. |
| `email_confirm_code` | Token | One-time confirmation code emailed after registration. |
| `email_for_confirmation` | Pending email | When the customer changes their email, the new address is stored here pending verification. See [[customer-entity-auth]]. |
| `date_confirm_sent` | Datetime | When the confirmation email was last sent — used for resend rate-limiting. |
| `is_activated` | yes / no | Whether the activation completed end-to-end (used in social-account / magic-link flows). |
| `imported` | yes / no | Marker that the customer came in via Import (the [[customers-import]] flow). |
| `default_address_id` | FK → CustomerShippingAddress | The default shipping address shown at checkout. |
| `default_billing_address_id` | FK → CustomerBillingAddress | The default billing address. |
| `note` | Admin-only free text | Internal note about the customer — NEVER visible to the customer. Help text on the Create modal: *"This note will not be visible to customer"*. |
| `timezone_id` | FK to timezone | Customer's timezone. Used for time-sensitive display (e.g., order delivery windows). |
| `remember_token` | Persistent-login token | The "remember me" cookie value. |
| `income` | Lifetime revenue total | Aggregate sum of completed-orders prices. Updated by the income-recalculation service. See [[customer-entity-api-and-webhooks]]. |
| `completed_orders` | Count of completed orders | Running aggregate. |
| `orders_total` / `total_orders` | Total order count (all statuses) | Includes cancelled / abandoned. |
| `orders_total_price` | Sum of all order prices | All statuses included. |
| `last_order_date` | Most recent order timestamp | Used by RFM analysis and segmentation. |
| `income_updated_at` | When stats were last refreshed | Aggregate snapshot timing. |
| `epay_one_touch`, `stripe`, `mypos`, `raiffeisen`, `borica_way4` | Saved payment-method tokens | Per-provider saved-card / one-touch tokens. Empty for guest customers. NEVER exposed in API responses. See [[customer-entity-auth]]. |
| `date_added` | Created-at timestamp | Customer record creation time. The `created_at` column is renamed to `date_added` — this is the canonical CloudCart pattern for customer records. |
| `updated_at` | Last-modified timestamp | Updated on every save. |

## Validation constraints

At create / edit the platform enforces:

- `note` max **191 chars** — error key `customer.err.note_max_chars_191`.
- `password` min **3** / max **20** chars — error keys `customer.err.password_min_chars_3` / `customer.err.password_max_chars_20`.
- `password_old` required when changing password on the storefront (but NOT in admin) — errors *"Empty old password"* / *"Invalid old password"* / `customer.err.invalid_old_password`.
- `password_repeat` must match `password` when both are supplied — error `customer.err.passwords_mismatch`.
- `email` is validated for **format** AND **uniqueness** within scope — error `customer.err.email_taken` when the same email already belongs to another registered customer; `customer.err.email_required` when empty.
- `group_id` must be a valid existing group — errors `customer_group.err.choose` / `customer_group.err.no_longer_exists`.
- Phone numbers are checked against libphonenumber format.

The full validation-error key set is documented in [[customer-entity-api-and-webhooks]].

## Storefront name display

The setting `customer_name_display` (also referenced as `name_display_format`) controls how `first_name` / `last_name` are concatenated for display. The platform's `name_field` is `full_name_email` and surfaces all three (first, last, email) for search by ANY of them.

## Where it appears

- [[customers-details-overview]] — the overview tab renders all the identity, status, and aggregate-stats fields.
- [[customers]] — list view shows `first_name`, `last_name`, `email`, `group_id`, `active`, `banned`, `marketing`, `completed_orders`, `last_order_date`.
- [[customers-custom-fields]] — per-merchant custom fields layered on top of these built-in attributes (verify).
- [[customers-import]] — import maps CSV columns to these fields.
- [[customers-export]] — export emits these columns (saved payment tokens are excluded).

## Related

- [[customer]] — hub.
- [[customer-group]] — required group assignment.
- [[customers-change-password]] — admin path to change `password`.
- [[settings-cart]] — `customer_name_display` setting; `unconfirmed_accounts_restrict` setting referenced in `email_confirmed`.

## Open Questions

- ⏸️ Whether the `customer_name_display` setting key is exactly `customer_name_display` or `name_display_format` — both appear in code paths (verify).
