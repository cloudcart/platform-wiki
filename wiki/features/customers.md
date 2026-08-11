---
type: feature
nav_path: "Customers"
route_name: customers-list.new
route_path: /admin/customers-new
aliases: ["Customers", "Customer list", "Customer database", "Клиенти", "Купувачи", "Списък с клиенти"]
tags: [customers, list, core, hub]
plan_gates: ["customers", "total_customers"]
created: 2026-05-21
updated: 2026-06-10
source_count: 13
---

# Customers

## Purpose

The merchant's **customer list** — every account that has ordered from the store, signed up for newsletters, or been added manually. Each row aggregates a customer's identity, contact, lifetime stats (completed orders count + revenue), marketing-consent flag, active/banned status, and quick inline toggles. Clicking a row opens the **Customer details** page ([[customers-details]]).

The page header provides three primary actions: **Export customers**, **Import**, and **+ Add customer**.

This hub is split into focused aspects — read the one that matches the question, not all of them.

## Sub-pages (in this cluster)

- [[customers-list-view]] — list table columns, sort, header actions (Export / Import / + Add customer), per-row inline toggles (Marketing, Active), sign-in-as-customer icon, and what the merchant CANNOT do from this view.
- [[customers-filters]] — the filter set (Active, Banned, Accept marketing, Customer tag, Customer groups, Country, State).
- [[customers-bulk-actions]] — Ban customer/s, Remove ban, Change customer's group, Change password (bulk reset), Delete — including which handlers are stubs in the modern Vue build vs wired in legacy.
- [[customers-create-modal]] — the **+ Add customer** / edit side-panel: every field, v-model, validation, save behaviour, custom-fields rendering, `focusNote` / `noteOnly` opening modifiers, and the guest→registered auto-merge on email match.
- [[customers-ban]] — ban modal (required reason), per-customer ban from the detail-page header, `banned` + `date_banned` + `banned_reason` semantics, unban-clears-both rule.
- [[customers-flags]] — the three independent customer flags (Active, Banned, Accept marketing), inline toggles save immediately, login-side effects of `active = false`, marketing-toggle and tag-change segment-recompute side effects.
- [[customers-lifetime-kpis]] — denormalised lifetime totals on the customer record (`income`, `completed_orders`, `orders_total`, `orders_total_price`, `last_order_date`), queued recompute on order lifecycle, EUR conversion at 1.95583, CloudCart-staff backfill commands, password-reset link 1-hour validity, deletion cascade.

## Where to find it

Sidebar → **Customers**. The breadcrumb reads "Customers". The route is `/admin/customers-new` (modern Vue). The header icon is the user-group icon.

## What the merchant can do here

- See and filter every customer in the store — see [[customers-list-view]] + [[customers-filters]].
- Bulk-ban, bulk-unban, bulk-reassign groups, bulk-reset passwords, bulk-delete — see [[customers-bulk-actions]].
- Add a single customer manually — see [[customers-create-modal]].
- Toggle Marketing and Active for one row inline — see [[customers-flags]].
- Drill into a single customer — see [[customers-details]].
- Sign in as the customer on the storefront — see [[customers-sign-in]].
- Bulk-import customers from CSV — see [[customers-import]].
- Export the customer list to CSV — see [[customers-export]].

## Settings & fields

This is a hub — per-aspect pages carry the field tables. Quick map:

- List columns (Name, Completed orders, Revenue, Added, Status, Marketing, Active) → [[customers-list-view]].
- Filter set → [[customers-filters]].
- Create / Edit modal fields → [[customers-create-modal]].
- Ban-reason field → [[customers-ban]].

## Business rules

This is a hub — the cross-cutting business rules live on the aspect pages. Three rules every consumer of this cluster must know:

- **Three independent flags.** `Active`, `Banned`, and `Accept marketing` do NOT cascade — banning doesn't auto-deactivate, deactivating doesn't auto-clear marketing consent. See [[customers-flags]].
- **Modern bulk handlers are partly stubbed.** In the modern Vue listing, bulk Ban / bulk Change-group / bulk Change-password handlers are `console.log` stubs in the current build — until they ship, real bulk operations run from the legacy `/admin/old-customers` list. The per-customer Ban / Delete on the detail page ARE wired. See [[customers-bulk-actions]] for the full status table.
- **Hard delete + `isEmpty` protection.** Deleted customers cannot be recovered from the UI; the `isEmpty` check refuses deletion of customers with orders. See [[customers-lifetime-kpis]] for the cascade.

### Permission

This page requires the `customers` permission section. Per [[settings-staff]] restrictions, moderators may see only customers in specific groups depending on permission grants. Sub-features require additional grants: `customers.custom_fields` for [[customers-custom-fields]], `customers.customer_groups` for [[customers-custom-groups]]. All admin API endpoints under `/admin/api/core/customers` are protected by `hasApiPermission:customers` middleware. Moderators without the grant get 403.

### Side effects (cluster-wide)

- **`customer.created` / `customer.updated` / `customer.deleted` webhooks** fire on the respective changes — see [[settings-hooks]].
- **Marketing toggle** dispatches `CustomerMarketingChange` → Subscriber record updated → [[marketing-segments]] membership recomputed.
- **Tag changes** propagate to the matching Subscriber record (joined by `customer_id`).
- **Deletion cascade** — see [[customers-lifetime-kpis]] for the full list (cart deleted, Subscriber deleted async on `subscribers` queue, past orders preserved, `default_address_id` set NULL).

## Programmatic access

Customer records and groups can be read, created, updated, or deleted via **JSON-API v2** — see [[api-customers]] and [[api-customer-groups]]. Addresses and tags: [[api-customer-shipping-address]], [[api-customer-billing-address]], [[api-customer-tags]].

**Same side effects apply.** API writes fire the same lifecycle hooks as the admin save / inline toggles: `customer.*` webhooks, guest→registered auto-merge on email match, Subscriber removal, segment recompute, KPI denormalisation recompute, Welcome Email + Confirmation Link Email per `unconfirmed_accounts_restrict` on activation. Plan-gate `customers` count enforced. Bulk operations are admin-list features only.

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `customers` | Numeric (max customer records) | Per-plan customer-record cap. Enforced via the platform code on every customer create (admin Add Customer modal, storefront registration, JSON-API v2 POST). When the cap is reached, new creates return HTTP 402 and the merchant is redirected to `/admin/plan/feature/customers`. Existing customers continue to work; only NEW records are blocked. Add-on packs (+100 / +500 / +1000 customers) stack on top of the plan value via [[plan-features]]. |
| `total_customers` | Boolean (dashboard module gate) | Whether the Dashboard's customer-count statistic module shows the merchant a customer count or hides it behind an upgrade prompt. Independent of the `customers` numeric cap — info-only display gate, NOT a create restriction. |

When over cap, the merchant is redirected to the per-feature upsell at [[plan-features]]. The `customers` cap is the only gate that affects the merchant's ability to use the list itself; everything else on this page (filters, bulk actions, inline toggles) is permission-gated, not plan-gated. Import / Export header actions are gated separately by `customer_import` ([[customers-import]]) / `customer_export` ([[customers-export]]).

## Related

Aspects in this cluster — see Sub-pages above: [[customers-list-view]], [[customers-filters]], [[customers-bulk-actions]], [[customers-create-modal]], [[customers-ban]], [[customers-flags]], [[customers-lifetime-kpis]].

External pages:

- [[customers-details]] — per-customer detail page (opens when the merchant clicks a row).
- [[customers-details-overview]] / [[customers-details-orders]] / [[customers-details-shipping-addresses]] / [[customers-details-billing-addresses]] / [[customers-details-products]] / [[customers-details-payments]] / [[customers-details-reviews]] — detail sub-tabs.
- [[customers-custom-fields]] — custom checkout field definitions.
- [[customers-custom-groups]] — customer-group (loyalty tier) definitions.
- [[customers-sign-in]] — log in as the customer (impersonation).
- [[customers-change-password]] — set a specific password (NOT a reset link).
- [[customers-import]] / [[customers-export]] — bulk-IO flows (legacy).
- [[reports-customers]] — analytics + chart.
- [[customer]] / [[customer-group]] — entity pages.
- [[settings-hooks]] — `customer.*` webhook events.
- [[settings-banned-ip]] — distinct order-IP-level rejection.
- [[settings-staff]] — moderator permission grants.
- [[marketing-segments]] — recomputed when Marketing flag or tags change.
- [[subscriber-vs-customer]] — the customer-record vs marketing-subscriber distinction behind the Marketing flag, tag propagation, and segment recompute.
- [[notification-delivery]] — the Welcome / Confirmation-link / account email mechanism triggered on customer create + activation.
- [[plan-features]] — `customers` numeric cap + add-on packs.

## Open questions

None — all previously-flagged items distributed to sub-pages.
