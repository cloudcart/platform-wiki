---
type: feature
nav_path: "Customers → Customer details → Tab strip"
route_name: customers-details
route_path: /admin/customers/details/:id
aliases: ["Customer details tab strip", "Customer details sub-tabs", "Customer details navigation", "Customer wallet tab", "Портфейл на клиент"]
tags: [customers, profile, detail, navigation, wallet]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[customers-details]]. See the hub for the other aspects (identity card, ban flow, email verification, default address, delete).

# Customer details — Tab strip

## Purpose

The **sub-tab navigation** beneath the two-column overview area on the customer detail page. The tab strip routes the merchant between the detail sub-pages (Overview, Shipping addresses, Billing addresses, Orders, Products, Payments, Wallet, Reviews) without re-loading the customer record.

This aspect documents exactly which tabs appear, in what order and under which conditions.

## Where to find it

[[customers]] → click any row → opens `/admin/customers/details/:id`. The tab strip sits **below** the two-column area (identity card + default address card) and **above** the active tab's content.

A separate **header tab strip** at the top of the page holds *"Customers"* and *"Customer details"*. It is the level-1 navigation back to the parent list.

## What the merchant can do here

### The tabs, in order

| Tab | Route | What it shows |
|-----|-------|---------------|
| **Overview** | `customers-details-overview` | Order distribution and quick stats. See [[customers-details-overview]]. |
| **Shipping addresses** | `customers-shipping-addresses` | List + CRUD of saved shipping addresses. See [[customers-details-shipping-addresses]]. |
| **Billing addresses** | `customers-billing-addresses` | List + CRUD of billing addresses with B2B fields. See [[customers-details-billing-addresses]]. |
| **Orders** | `customers-orders` | Full order history for this customer. See [[customers-details-orders]]. |
| **Products** | `customers-products` | Every product the customer has bought. See [[customers-details-products]]. |
| **Payments** | `customers-payments` | Payment transaction history. See [[customers-details-payments]]. |
| **Wallet** | `customers-wallet` | Wallet balance, credits and **Add transaction**, at `/admin/customers/details/:id/wallet`. Shown for every customer outside the Guests group, even if the store never set up top-ups. See [[virtual-wallet-customers]]. |
| **Reviews** | `customers-reviews` | Reviews the customer has left, at `/admin/customers/details/:id/reviews`. Shown when the [[apps-product-review]] app is installed and active. See [[customers-details-reviews]]. |

## Settings & fields

The tab strip has no editable settings of its own. The Wallet tab follows the customer's group, and the Reviews tab follows the install + active state of the [[apps-product-review]] app.

## Business rules

### Tabs share one customer record

The page loads the customer once when it opens, and all tabs read that record, so moving between tabs does not re-fetch it.

Consequence: an edit made through the identity-card panel shows on every tab without a page reload. A change made elsewhere (e.g., the background update of the income KPIs) appears after a page reload.

The default-address card and each tab's list (orders, payments, addresses, etc.) fetch their own data independently.

### Reviews tab is conditional on the Product Review app

The Reviews tab appears only when the [[apps-product-review]] app is installed AND active. Uninstalling the app removes the tab, and opening its address then lands on Overview. A staff member without the `apps` permission does not see the tab.

### Permission gating

The Customers permission section controls access to the whole detail page (and therefore the tab strip). Per [[settings-staff]] restrictions, moderators may see only customers in specific groups depending on their permission grants.

## Related

- [[customers-details]] — hub.
- [[customers-details-overview]] — Overview tab.
- [[customers-details-shipping-addresses]] — Shipping addresses tab.
- [[customers-details-billing-addresses]] — Billing addresses tab.
- [[customers-details-orders]] — Orders history tab.
- [[customers-details-products]] — Products bought tab.
- [[customers-details-payments]] — Payments tab.
- [[virtual-wallet-customers]] — Wallet tab.
- [[customers-details-reviews]] — Reviews tab (conditional).
- [[apps-product-review]] — gates the Reviews tab.
- [[settings-staff]] — permission grants that gate access to the customer detail page.

## Open questions

None.
