---
type: entity
nav_path: "Entity → Customer → Status flags (Active / Banned / Marketing)"
aliases: ["Customer status flags", "Active flag", "Banned flag", "Marketing flag", "Customer ban", "Deactivate customer", "Three independent flags"]
tags: [entity, customers, status, flags, ban]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customer]]. See the hub for the other aspects (attributes, lifecycle, relationships, auth + email, API + webhooks).

# Customer — Status flags (Active / Banned / Marketing)

## Identity

The three booleans on every [[customer|Customer]] record that gate **storefront login**, **order placement**, and **marketing-campaign eligibility** — `active`, `banned`, `marketing`. They are **independent**: each must be set on its own. Banning does NOT auto-deactivate; deactivating does NOT auto-clear marketing consent; clearing marketing consent does NOT deactivate the account.

## Aliases

- **Active flag** (`active = yes/no`) — storefront login enabled.
- **Banned flag** (`banned = yes/no`) — disciplinary lock on login AND ordering.
- **Marketing flag** / **Accept marketing** (`marketing = yes/no`) — newsletter / promo consent.

## Key Attributes

| Flag | Field | Effect when `no` | Where the merchant toggles it |
|------|-------|------------------|------------------------------|
| Active | `active` | Storefront login throws `'sf.err.account.inactive'`. Past orders intact, account recoverable. | Inline toggle on [[customers]] list, also on [[customers-details]]. |
| Banned | `banned` (+ required `banned_reason` + `date_banned`) | Login throws `'sf.global.err.customer_banned'`; order placement throws `'customer.err.user_banned'`. | Ban modal on [[customers]] / [[customers-details]]; also bulk via [[customers-bulk-actions]] (verify). |
| Accept marketing | `marketing` | Customer excluded from marketing campaign sends entirely. Transactional emails still go through. | Inline / detail-page toggle; storefront preferences also let the customer flip this. |

### Three independent flags — no cascade

The customer's status is governed by these three booleans that do NOT cascade. When the merchant toggles Active off, marketing consent is NOT automatically revoked. When the merchant bans, Active is NOT automatically flipped. Each flag has to be set independently.

This is the single most-misunderstood rule about customer status — merchants frequently assume "banning" turns off marketing too. It does not.

### Banned is stricter than Inactive

| Action | `active = no` (Inactive) | `banned = yes` (Banned) |
|--------|--------------------------|-------------------------|
| Storefront login | ❌ blocked (`'sf.err.account.inactive'`) | ❌ blocked (`'sf.global.err.customer_banned'`) |
| Place order (storefront) | ✅ usually allowed (verify per checkout-as-guest path) | ❌ blocked |
| Place order (admin-side) | ✅ allowed | ❌ blocked (`'customer.err.user_banned'`) |
| Receive transactional emails | ✅ | ✅ (verify) |
| Be included in marketing sends | depends on `marketing` flag | depends on `marketing` flag (independent) |
| Past orders | preserved | preserved |
| Reason required | no | **yes** — `banned_reason` mandatory |

The merchant's intent for Ban: **keep the record (for audit) but lock all account activity**.

### Ban requires a non-empty reason

The Ban modal on [[customers]] has a required `banned_reason` textarea. The Confirm button stays disabled until the merchant types a reason. The reason is stored on the customer and shown on [[customers-details]]. Unbanning clears `banned`, `banned_reason`, AND `date_banned` in one call. There is no history of past bans — only the most recent reason is retained.

Banned customers' detail pages show a red **Banned** chip with the reason and date embedded in the login-error message: *"You have been banned: `<reason>` (since `<date>`)."*

### Deactivated accounts get a specific login error

When a customer with `active = no` tries to log in, the storefront throws the translation key `'sf.err.account.inactive'` as the error message. So merchants who want to **soft-disable** an account without banning can do this — orders remain intact and recoverable.

### Marketing consent is at customer-level AND subscriber-channel level

`Customer.marketing` is a single yes/no for the customer-record itself. The newer [[subscriber|Subscriber]] / SubscriberChannel model carries **per-channel consent** (Email, SMS, Viber, Web Push) for marketing.

When the merchant runs a campaign, **both layers gate delivery**:

- A customer with `marketing = no` is **excluded entirely**.
- A subscriber whose per-channel `SubscriberChannel.marketing = 0` is excluded from **that specific channel** even if the customer-level flag is `yes`.

See [[notification-delivery]] for the full precedence rules, and [[customer-entity-relationships]] for the Customer / Subscriber distinction.

### Bulk ban / unban behavior

The `changeBanned` path accepts a single ID or an array — bulk ban from the [[customers]] list and per-customer ban from [[customers-details]] share the same code path. Unban clears `banned`, `banned_reason`, and `date_banned` together; ban preserves the reason for audit.

### Banning does NOT email the customer

A ban takes effect **silently** from the customer's perspective. There is no automated email or any other notification telling them the account was banned. The customer only discovers the ban when they next try to log in or place an order. Merchants who need to communicate the ban must email the customer separately. See [[customer-entity-lifecycle]] for the broader lifecycle context.

## Where it appears

- [[customers]] — list view shows Active / Banned / Marketing chips; bulk Ban / Deactivate actions live here.
- [[customers-details]] / [[customers-details-overview]] — per-customer header with the chips; Ban modal opens from here.
- [[customers-ban]] — dedicated ban modal documentation (verify).
- [[customers-flags]] — list view's flag column behaviour (verify).
- Storefront preferences — the customer can flip `marketing` on the storefront account-settings page (see [[customer-account]]) (verify).

## Related

- [[customer]] — hub.
- [[customer-entity-lifecycle]] — the six named states.
- [[customer-entity-relationships]] — Customer-vs-Subscriber marketing consent precedence.
- [[settings-banned-ip]] — distinct concept: order-IP-level rejection happens at order placement time regardless of which customer placed the order.
- [[notification-delivery]] — how customer-level + subscriber-channel consent layers gate marketing sends.

## Open Questions

- ⏸️ Whether `marketing = no` at customer level overrides ALL per-channel SubscriberChannel consents, or only ones tied to the same email — the precedence rule when a customer-email matches a subscriber-email is not fully documented.
- ⏸️ Whether placing an order on the storefront is blocked for `active = no` customers, or only the *login* is blocked (the order could still go through as guest checkout) (verify).
