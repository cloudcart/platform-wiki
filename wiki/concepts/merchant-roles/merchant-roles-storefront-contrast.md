---
type: concept
nav_path: "Concept → Merchant roles → Storefront contrast (Customer / Subscriber)"
aliases: ["Customer vs Moderator", "Subscriber vs admin", "Storefront user is not admin", "Customer Service rep customer record", "Separate Customer record from Moderator"]
tags: [access, storefront, admin, contrast, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[merchant-roles]]. See the hub for the other aspects (owner, moderator, permissions tree, API access, force sign-out + 2FA, notifications + audit).

# Merchant roles — storefront contrast (Customer / Subscriber)

## Definition

CloudCart has four distinct "people" entities the merchant might confuse if they think of "roles" as a single dimension. **None of them overlap as records.** A Customer who also acts as a Moderator has TWO separate records in the system — one on [[customers]] and one on [[settings-staff]].

| Role | Side | Record location | Purpose |
|---|---|---|---|
| **Owner** | admin panel | [[settings-staff]] (unique `type=owner` row) | Root admin for the store. See [[merchant-roles-owner]]. |
| **Moderator** | admin panel | [[settings-staff]] (`type=moderator` rows) | Delegated staff with granular permissions. See [[merchant-roles-moderator]]. |
| **Customer** | storefront | [[customers]] | Has bought (or could buy) from the storefront. Storefront login + checkout. See [[customer]]. |
| **Subscriber** | storefront | [[marketing-subscribers]] | Has opted in to marketing communications. May or may not also be a Customer. See [[subscriber]] and [[subscriber-vs-customer]]. |

## Scope

What this page covers:

- The four distinct record types and which screen surfaces each.
- The "Customer who is also a Moderator" pattern — two separate records.
- Why the merchant's billing-customer (the merchant themselves) is the Owner, not a Customer.

Not covered here:

- The Customer / Subscriber duality itself — see [[subscriber-vs-customer]] (the dedicated concept page).
- The Owner / Moderator distinction — see [[merchant-roles-owner]] and [[merchant-roles-moderator]].
- API Keys / PATs (machine identities, not "people") — see [[merchant-roles-api-access]].
- Storefront-user authentication on the customer side — see [[customer]] and the storefront-side documentation.

## Contrasts

- **Customer vs Subscriber** — Customers are storefront users with a buy history (or potential to buy); Subscribers are a marketing audience who've opted in to communications. See [[subscriber-vs-customer]] for the dedicated concept page.
- **Customer vs Moderator** — Customers live on [[customers]] and have storefront credentials. Moderators live on [[settings-staff]] and have admin-panel credentials. **The same person acting in both capacities has TWO records.**
- **Subscriber vs Moderator** — A Subscriber is a marketing audience member, not an admin account. A merchant employee who also subscribes to the storefront's newsletter has a separate Subscriber record from their Moderator account.
- **Owner vs Customer (of their own store)** — the Owner is the merchant. If they buy from their own store as a test (or to claim a discount), the test order creates a Customer record. The Customer record is a storefront entity; the Owner record is an admin entity. They share no fields.

## Where it applies

### "Customer Service rep" who happens to be a Customer too

The merchant's Customer Service rep is a Moderator with permissions restricted to Orders + Customers. Suppose the same person also buys from the store personally:

- They have a **Moderator record** on [[settings-staff]] with username, granted permissions, optional 2FA.
- They have a **Customer record** on [[customers]] with their order history, addresses, wishlist, optional storefront login.
- The two records do NOT cross-reference each other. The system does not "know" they're the same human.
- The Moderator credentials log into the admin panel; the Customer credentials log into the storefront. Different cookies, different sessions, different password fields.

This is intentional — it lets the merchant change Moderator permissions (or revoke admin access entirely) without affecting the same human's ability to shop, and vice versa.

### A Subscriber who is NOT a Customer

A Subscriber who opted in via a popup but never bought is a [[marketing-subscribers|Subscriber]] record only. They have no [[customer|Customer]] record until they place an order. Conversely, a Customer who opted out of marketing is a Customer-only record. See [[subscriber-vs-customer]] for the full taxonomy.

Neither of these is an admin account.

### The Owner buying from their own store

If the Owner places a test order to verify the storefront flow, the system creates a **Customer record** for them on [[customers]]. The Customer record has the Owner's name and email, but it is NOT linked to the [[staff-member|Staff-Member]] record. The Owner is now visible in two places:

- [[settings-staff]] — as the `type=owner` row.
- [[customers]] — as a regular Customer with one order.

This duality is normal and expected. The Owner remains the only `type=owner` row regardless of how many Customer records they accumulate.

## Why this matters to the merchant

- **Don't conflate "the customer service person" with "a customer."** Granting Moderator permissions to a Customer does NOT happen automatically — the merchant has to create a separate Moderator account for them on [[settings-staff]].
- **Revoking storefront access does NOT revoke admin access.** Suspending a Customer record on [[customers]] does not touch any Moderator record. To revoke admin access, the merchant deletes the Moderator on [[settings-staff]] (see [[merchant-roles-moderator]]).
- **Subscriber opt-out has no admin-panel side effect.** A Subscriber unsubscribing affects only their marketing-opt-in flag; their Customer record (if any) and any Moderator record they hold are untouched.
- **The Owner's storefront orders are real Customer rows.** They count toward the store's Customer count, the orders count, the analytics, the LTA-contract turnover, etc. (verify) — the platform treats the Owner-as-buyer the same as any other Customer.

## Related

- [[merchant-roles]] — hub.
- [[merchant-roles-owner]] — Owner is an admin record, not a Customer.
- [[merchant-roles-moderator]] — Moderator is an admin record, separate from any Customer record the same human may hold.
- [[customer]] — Customer entity (storefront user).
- [[subscriber]] — Subscriber entity (marketing audience).
- [[subscriber-vs-customer]] — concept page on the storefront-user duality.
- [[customers]] — Customers list screen.
- [[marketing-subscribers]] — Subscribers list screen.
- [[settings-staff]] — Staff list (where Moderators live).
- [[staff-member]] — Staff-Member entity (Owner / Moderator record).

## Open Questions

None.
