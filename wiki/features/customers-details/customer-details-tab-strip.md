---
type: feature
nav_path: "Customers → Customer details → Tab strip"
route_name: customers-details.new
route_path: /admin/customers-new/details/:id
aliases: ["Customer details tab strip", "Customer details sub-tabs", "Customer details navigation"]
tags: [customers, profile, detail, navigation]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details]]. See the hub for the other aspects (identity card, ban flow, email verification, default address, delete).

# Customer details — Tab strip

## Purpose

The **sub-tab navigation** beneath the two-column overview area on the customer detail page. The tab strip routes the merchant between the seven possible detail sub-pages (Overview, Shipping addresses, Billing addresses, Orders, Products, Payments, Reviews) without re-loading the customer record — they all share the cached customer object via Vue's provide/inject.

This aspect documents exactly which tabs appear, in what order, under which conditions, and what the current build actually renders (vs the design specification).

## Where to find it

[[customers]] → click any row → opens `/admin/customers-new/details/:id`. The tab strip sits **below** the two-column area (identity card + default address card) and **above** the active tab's content.

A separate **header tab strip** (the `CcSettingsWrapper` tabs) renders a single *"Customers"* tab + (when on a detail route) an additional *"Customer details"* active tab — these are NOT the sub-tabs documented here; they're the level-1 navigation back to the parent list.

## What the merchant can do here

### Designed tab strip (7 tabs in spec)

| Tab | Route | What it shows |
|-----|-------|---------------|
| **Overview** | `customers-details-overview.new` | Order distribution and quick stats. See [[customers-details-overview]]. |
| **Shipping addresses** | `customers-shipping-addresses.new` | List + CRUD of saved shipping addresses. See [[customers-details-shipping-addresses]]. |
| **Billing addresses** | `customers-billing-addresses.new` | List + CRUD of billing addresses with B2B fields. See [[customers-details-billing-addresses]]. |
| **Orders** | `customers-orders.new` | Full order history for this customer. See [[customers-details-orders]]. |
| **Products** | `customers-products.new` | Every product the customer has bought. See [[customers-details-products]]. |
| **Payments** | `customers-payments.new` | Payment transaction history. See [[customers-details-payments]]. |
| **Reviews** | (conditional, when reviews app installed) | Reviews the customer has left. See [[customers-details-reviews]]. |

The Reviews tab is conditional — it only appears when the reviews app is installed and active.

### Modern build — 6 tabs verified

In the current modern build, the tab strip renders exactly these 6 tabs in this order (verified):

1. **Overview** → `customers-details-overview.new`
2. **Shipping addresses** → `customers-shipping-addresses.new`
3. **Billing addresses** → `customers-billing-addresses.new`
4. **Orders** → `customers-orders.new`
5. **Products** → `customers-products.new`
6. **Payments** → `customers-payments.new`

The **Reviews** tab is **currently NOT rendered** in the modern UI — the `isReviewsInstallAndActive` check is commented out as a TODO. So stores with the Reviews app installed still don't see the tab in the modern UI; they must visit the legacy `/admin/customers/details/:id` route to access historical customer reviews until the modern conditional is wired up.

## Settings & fields

The tab strip has no editable settings of its own. The presence / absence of the Reviews tab is governed entirely by the install + active state of the [[apps-product-review]] app (currently gated by an unfinished conditional — see above).

## Business rules

### Tabs share one cached customer record

All sub-tabs read the customer record from a single TanStack Query cache, populated when the merchant first opens the detail page. The cache is shared via Vue's provide/inject mechanism — sub-tab navigation does NOT re-fetch the customer object.

Consequence: a customer-record edit made via the identity-card modal updates the cache, so every sub-tab sees the new data on next render without a page reload. But changes made directly in the database (e.g., an external job updating the income KPIs) won't appear until the cache is invalidated — typically by a hard refresh or by navigating away and back to the list.

The exceptions are sub-tab-specific queries: the [[customer-details-default-address|default-address card]] has its own query keyed by customer ID + default_address_id, and each sub-tab fetches its own list data (orders, payments, addresses, etc.) independently.

### Reviews tab is conditional on the Product Review app

The Reviews sub-tab appears only when the [[apps-product-review]] app is installed AND active. The route's `isReviewsInstallAndActive` check gates the tab — uninstalling the app removes the tab from the navigation. Without the app, historical reviews on this customer (if any from a previous activation) are not viewable through this UI.

**Current-build gap**: the `isReviewsInstallAndActive` conditional in the modern detail page is commented out as a TODO, so even merchants who DO have the Reviews app installed see only 6 tabs in the modern UI. Workaround: visit the legacy `/admin/customers/details/:id` route to view historical customer reviews until the modern conditional is finished `(verify)`.

### Permission gating

The Customers permission section controls access to the whole detail page (and therefore the tab strip). Per [[settings-staff]] restrictions, moderators may see only customers in specific groups depending on their permission grants — but within an allowed customer, all 6 sub-tabs are visible (no per-tab permission split).

## Related

- [[customers-details]] — hub.
- [[customers-details-overview]] — Overview tab.
- [[customers-details-shipping-addresses]] — Shipping addresses tab.
- [[customers-details-billing-addresses]] — Billing addresses tab.
- [[customers-details-orders]] — Orders history tab.
- [[customers-details-products]] — Products bought tab.
- [[customers-details-payments]] — Payments tab.
- [[customers-details-reviews]] — Reviews tab (conditional).
- [[apps-product-review]] — gates the Reviews tab.
- [[settings-staff]] — permission grants that gate access to the customer detail page.

## Open questions

- Confirm whether the modern Reviews-tab conditional has been wired up since the TODO was noted `(verify)`.
