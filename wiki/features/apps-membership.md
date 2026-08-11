---
type: feature
nav_path: "Apps → Membership"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Membership", "Customer Membership", "Paid membership", "Membership tiers", "Subscriptions", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, b2b, loyalty, membership]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# Membership (paid membership tiers)

## Purpose

**Membership** integration — adds **paid / earned membership tiers** to the storefront. Members get exclusive benefits (member pricing, exclusive products, early access to sales, free shipping) and access to gated Pages. Different from [[customers-custom-groups]] which is a basic taxonomy — Membership is a TRANSACTIONAL feature with time-bound validity, order-driven renewals, and page-level gated content.

Used for:
- Costco-style warehouse-club models (paid annual membership for access).
- Loyalty programs with tier requirements (Bronze / Silver / Gold based on spending).
- Subscription clubs (monthly fee for exclusive products).

Mechanically, there is **no separate "membership tier" entity** — the merchant builds tiers as differently-priced **digital products** linked to **Pages** with different validity periods. Buying the product grants a time-bound membership record. See [[apps-membership-purchase-flow]] for the full grant mechanics.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> Membership itself is per customer and is granted / revoked by order-status transitions — that is a customer's membership state, not an on/off switch for the app.

## Where to find it

Sidebar → Apps → install → **Membership**.

The Vue routes are intentionally pinned under `/admin/orders/subscriptions` (NOT `/admin/apps/membership`) because the integration was historically rolled out as an Orders → Subscriptions area before being merged into the Apps catalog. The two URLs:

- `/admin/orders/subscriptions` — Overview tab.
- `/admin/orders/subscriptions/settings` — Settings tab (a list of membership records + modals, not a settings form — see [[apps-membership-records-admin]]).

Both render through the standard `ApplicationSettings` wrapper. Old bookmarks for `/admin/apps/membership` and `/orders/subscriptions` redirect to these routes. **The legacy Subscriptions concept has been MERGED into Membership** — the old URL lands on the modern Membership UI.

## What the merchant can do here

- Define membership "tiers" as digital products linked to Pages with validity days.
- Set tier rules: paid (the customer buys the product) OR earned (lifetime-spend threshold).
- Configure member-exclusive products / categories and member-exclusive pricing.
- Gate specific Pages behind active membership (member-only catalog, forum, tutorials).
- View, create, extend, and delete individual membership records from the Settings tab.
- Track member status per customer.

### What the merchant CANNOT do here

- Run membership without [[customers]] (members are customers with membership records).
- Set up gift / family / multi-customer memberships — one record = one customer (see [[apps-membership-data-model]]).
- Get card-on-file auto-renew or expiry-reminder emails out of the box (see [[apps-membership-renewal-revocation]]).
- Generate a downloadable / scannable membership card or pass (see [[apps-membership-records-admin]]).

## Settings & fields

There is no form-level configuration screen. Configuration lives in two places:

- **The catalog** — the merchant marks a Product `digital = yes` and links it to one or more Pages with `days` of validity (see [[apps-membership-purchase-flow]]).
- **The Settings tab** — a table of every membership record plus a Create modal and an Extra Days modal (see [[apps-membership-records-admin]]).

The integration creates DB tables for membership records on install. Per-customer membership state is a simple time-bound record (see [[apps-membership-data-model]]).

## Business rules

### Paid vs earned tiers

| Type | Acquisition |
|------|-------------|
| **Paid** | Customer purchases the membership (a "Buy membership" digital product). |
| **Earned** | Customer hits a lifetime-spend threshold (e.g., 1000 BGN). |

The merchant configures which model applies per tier.

### Member-exclusive products

When a product is marked member-exclusive, non-members see "Login to view" / "Membership required" on the storefront. Members see normal pricing + the Buy button. Page visibility is gated by Membership, not by [[apps-private-store]] (which gates the whole storefront) — see [[apps-membership-renewal-revocation]] for the enforcement detail.

### Order-driven lifecycle

Membership is granted, extended, and revoked entirely by **order-status transitions** — there is no scheduled charge or scheduled job. Reaching `paid` / `completed` grants days; leaving those statuses subtracts them back. See [[apps-membership-renewal-revocation]].

### Permission

Standard apps permission scope.

## Sub-pages (in this cluster)

This feature is split into 5 aspect pages. Drill into the aspect that matches the question rather than reading every page.

- [[apps-membership-data-model]] — the 5-field membership record, relationships, lifetime (`expired = null`), one-customer-one-membership, no gift/family/multi-customer.
- [[apps-membership-purchase-flow]] — how a membership is granted by buying a `digital` product linked to Pages; multi-page → multiple records; quantity multiplies days; expiry stacking; the `add_days` order-meta audit trail.
- [[apps-membership-renewal-revocation]] — order-status-driven renewal + auto-revocation; custom statuses don't revoke; no grace period; no card-on-file auto-renew; no built-in expiry reminders; the subscriber-segment expiry condition; silent failure logging.
- [[apps-membership-records-admin]] — the Settings tab (table + filters), Create modal, Extra Days modal, page-gating enforcement, no bulk actions / exports, hidden +Additional-days for lifetime rows, no digital pass.
- [[apps-membership-api]] — the 5 internal API endpoints (list / create / add-extra-days / delete / install-uninstall) and the Manager surface.

## Related

- [[products-digital]] — membership tiers are built as digital `page` products (this app surfaces the Landing-pages mode).
- [[apps]] — App Store.
- [[customers]] — members are customers.
- [[customers-custom-groups]] — alternative simpler grouping (no tier validity / expiry).
- [[apps-private-store]] — alternative full-store-gating model.
- [[marketing-discounts]] — member-only discounts via discount targeting.
- [[marketing-subscribers]] — the membership-expiration segment condition for reminder emails.
- [[products-products]] — products can be tagged member-exclusive; digital products back the tiers.

## Open questions

None.
