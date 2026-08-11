---
type: feature
nav_path: "Customers → Flags + inline toggles"
route_name: customers-list.new
route_path: /admin/customers-new
aliases: ["Customer flags", "Active flag", "Marketing flag", "Accept marketing", "Customer status flags", "Inline toggle customers", "active customer field", "banned customer field"]
tags: [customers, flags, active, banned, marketing, segments]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers]]. See the hub for the other aspects (list view, filters, bulk actions, create modal, ban flow, lifetime KPIs).

# Customers — Flags + inline toggles

## Purpose

The **three independent booleans** that determine a customer's effective state: `active`, `banned`, `accept_marketing`. This aspect covers the no-cascade rule between them, the inline-toggle save behaviour on the customer list, the login-side effects, the segment-recompute side effects of Marketing and Tag changes, and the Welcome-Email side effect on inactive→active activation.

## Where to find it

- Customer list ([[customers-list-view]]) → per-row **Marketing** and **Active** toggles.
- Customer list filter row → **Active** / **Banned** / **Accept marketing** filters — see [[customers-filters]].
- Customer detail page ([[customers-details]]) → identity-card + status badges.
- Banned flag is set / cleared via [[customers-ban]].

## What the merchant can do here

- Flip Marketing or Active for one row inline — saves immediately.
- Filter the list by any of the three flags — see [[customers-filters]].
- Set / clear Banned via the dedicated ban flow — see [[customers-ban]].

## Settings & fields

### The three flags — verified

| Flag | Meaning | Where set |
|------|---------|-----------|
| `active` (yes/no) | Storefront account enabled. When OFF, the customer cannot log in. | Inline toggle on list; field on Customer detail. |
| `banned` (yes/no) | Disciplinary lock. Banned customers cannot log in OR place orders. Requires a reason at ban time. | Ban modal — see [[customers-ban]]. |
| `accept_marketing` (yes/no) | Consent for newsletter and promotional emails. When OFF, the customer is excluded from marketing campaigns even if active. | Inline **Marketing** toggle on list; consent toggles at storefront / checkout. |

## Business rules

### Three flags are INDEPENDENT — no cascade

These flags do not cascade — verified:

- Banning does NOT auto-deactivate.
- Deactivating does NOT auto-clear marketing consent.
- Clearing marketing consent does NOT deactivate or ban.

A customer can be **active + not banned + opted out of marketing** (active shopper who doesn't want email), or **inactive + not banned + opted-in** (account disabled but still on the marketing list — the campaign send filters by `active` separately).

### Inline toggles save immediately

Toggling Marketing or Active on a row calls the action endpoint immediately — no batch / save-all. Success toast confirms; failure toast reverts the toggle.

### Active = inactive login throw — verified

When a deactivated customer (`active = false`) tries to log in at the storefront, login is rejected with the **`'sf.err.account.inactive'`** error (shown on the email field). So the merchant deactivating an account effectively blocks storefront login (but doesn't remove past orders or other historical data).

### Marketing toggle dispatches segment-recompute job — verified

Toggling Marketing for a customer queues a background task that updates the customer's Subscriber record (used by [[marketing-segments]] / campaigns) to reflect the new marketing-consent state. So flipping the flag here also flips them in/out of marketing-targeting segments.

### Tag changes dispatch segment-recompute job — verified

Adding/removing customer tags (inline or via bulk Tag action) propagates the tags to the matching Subscriber record (linked by `customer_id`). Segments that filter by customer tags see the change.

### Inactive → active activation triggers Welcome Email — verified

When the merchant toggles an inactive customer's Active flag from off → on (and `is_activated` was 0), the platform sends a Welcome Email to the customer using the password stored encrypted in the customer's meta data (if any). If the `unconfirmed_accounts_restrict` setting is not `'none'`, a Confirmation Link Email is also sent. The encrypted-password meta entry is then deleted.

This activation path matters for **manually-created customers**: when the merchant adds a customer with a password via [[customers-create-modal]] but the account is not yet activated, the password is stored encrypted in meta until first activation.

### Side effects summary

- **`customer.updated` webhook** fires on every flag flip — see [[settings-hooks]].
- **Marketing** flip → Subscriber record updated → segment re-evaluation.
- **Tag** add/remove → Subscriber tag propagation → segment re-evaluation.
- **Active off → on** activation → Welcome Email (+ Confirmation Link Email when `unconfirmed_accounts_restrict != 'none'`).
- **Banned on** → blocks login + order placement (see [[customers-ban]]).

### Permission

The inline toggles and the flag-bearing fields are all protected by the `customers` API permission — moderators without the grant cannot flip them. (verify whether finer-grained per-flag permissions exist)

## Related

- [[customers]] — hub.
- [[customers-list-view]] — the per-row toggles UI.
- [[customers-filters]] — the three independent flag filters.
- [[customers-ban]] — the `banned` flag specifically.
- [[customers-create-modal]] — manual create path that stores encrypted password until activation.
- [[customers-lifetime-kpis]] — recompute pipelines independent of flag changes.
- [[marketing-segments]] — recomputed when Marketing or tags change.
- [[settings-hooks]] — `customer.updated` webhook.
- [[settings-staff]] — moderator grants for the Customers section.

## Open questions

- Is there a per-flag permission grant beyond the umbrella `customers` API permission? (verify)
- Does flipping Active off send any email to the customer? (verify — activation off → on is documented; off direction is not)
