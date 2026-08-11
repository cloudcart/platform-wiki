---
type: feature
nav_path: "Apps → Up/Cross-Sell"
route_name: apps.up_cross_sell.settings
route_path: /admin/apps/up_cross_sell
aliases: ["Up Cross Sell", "Up Cross Up Sell", "Upsell", "Cross-sell", "UpCrossUpSell", "Upsell/Cross-sell", "no enable disable button", "app has no active toggle"]
tags: [apps, marketing, upsell, cross-sell, conversion]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# Up/Cross-Sell

## Purpose

**Up/Cross-Sell** integration — enables the **Marketing → Cross Sell** feature on the storefront. Lets the merchant configure conditional product recommendations shown to customers:

- **Cross-sell**: "Customers also bought" or "Frequently bought together" — products shown alongside the current product.
- **Upsell**: "Consider this higher-tier alternative" — premium / larger / better product variants suggested.

The app is mainly an **installation gateway** — once installed, it opens `/admin/marketing-new/cross-sell` where the merchant manages the actual rules in the Vue Cross-Sell & UpSell manager.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be switched off is an individual **offer** — every Cross-Sell / UpSell offer has its own per-row Active toggle, see [[marketing-cross-sell-list]].

## Where to find it

Sidebar → Apps → install → **Up/Cross-Sell**. The route is `/admin/apps/up_cross_sell`. On install, the merchant is taken to `/admin/marketing-new/cross-sell` (the management UI).

The management UI is the Vue **Cross-Sell & UpSell** module — its screens are documented on:
- [[marketing-cross-sell-list]] — the offer list.
- [[cross-sell-offer-form]] — create / edit an offer.
- [[marketing-up-sell-diagram]] — the visual diagram editor (shared by Cross-Sell and UpSell).

## What the merchant can do here

### Install gateway
On click in the App Store, the platform:
1. Installs the Up/Cross-Sell app.
2. Takes the merchant to `/admin/marketing-new/cross-sell` (the management UI).

### Actual management (in `/admin/marketing-new/cross-sell`)
The merchant configures:
- **Cross-sell rules**: when product X is viewed / added to cart, show products Y / Z as suggestions.
- **Upsell rules**: when product X is viewed / added to cart, show higher-tier alternative product W.
- Filtering rules (by category, vendor, tag, custom conditions).
- Bulk rule operations.

Behavior is similar in spirit to [[apps-cart-rules]] (trigger + action) but specifically for product-recommendation surfacing rather than discount application.

### What the merchant CANNOT do here
- Configure rules from THIS apps page — it's a redirect/gateway only.
- Use this without installing the app first.
- **Deactivate the app while keeping it installed** — there is **no on/off toggle**: install = active, uninstall = inactive.

## Settings & fields

The actual settings live in the Vue Cross-Sell & UpSell manager at `/admin/marketing-new/cross-sell`. The offer fields are documented on [[marketing-cross-sell]] (hub) and [[cross-sell-offer-form]].

## Business rules

### Install gateway model

This app is essentially a gateway that:
1. Marks the app as installed.
2. Opens the Cross-Sell & UpSell manager at `/admin/marketing-new/cross-sell`.

The actual functionality lives in the Marketing module, not in the App's own code.

**The app has no active/inactive toggle of its own.** Its only state is installed-or-not: **installed = active; not installed (removed) = inactive.** Unlike most apps, there is no separate "activate / deactivate the app" switch — installing it makes it active, removing it makes it inactive. (This is distinct from the per-offer **Active** toggle on individual cross-sell / upsell rules in [[marketing-cross-sell]], which activates / deactivates one offer, not the app.)

### Distinct from Cart Rules

| Feature | Purpose |
|---|---|
| [[apps-cart-rules]] | Conditional DISCOUNTS at cart/checkout. |
| **Up/Cross-Sell** | Conditional PRODUCT RECOMMENDATIONS surfaced on product pages / cart. |

Both are trigger-action systems but solve different conversion problems.

### Storefront placement

Cross-sell + upsell recommendations typically appear:
- Below the product description on product pages.
- In the cart / mini-cart panel ("Frequently bought together").
- On the order-confirmation page (post-purchase upsell).

Exact placement depends on the storefront theme template implementation.

### Permission
Standard apps permission scope.

## Related

- [[apps]] — App Store hub.
- [[marketing-cross-sell]] — actual management UI (separate wiki page to be created).
- [[apps-cart-rules]] — sister conditional-rule engine (different scope — discounts vs recommendations).
- [[products-products]] — products tied together through Cross-Sell rules.
- [[products-smart-collections]] — collection-based product grouping.

## How it works (verified against backend)

### Up vs Cross — separate offer record types

Cross-Sell and Up-Sell are **two separate offer record types**, not one combined entity. The merchant creates Cross-Sell offers and Up-Sell offers separately, each with its own list view.

For the full management UI documentation, see [[marketing-cross-sell]].

### Redesigned navigation — separate Cross Sell and Up Sell sections (2026)

The management surface was reworked into **two distinct sections under Marketing**, each its own navigation group (both appear only once `up_cross_sell` is installed):

- **Cross Sell** — *List offers* (`marketing.cross_sell.offers`) + *Create new offer* (`marketing.cross_sell.create_offer`).
- **Up Sell** — *List offers* (`marketing.up_sell.offers`) + *Create new offer* (`marketing.up_sell.create_offer`).
- A shared **Settings** entry serving both.

The **Marketing dashboard** also shows promo bars — *"Try the new Cross Sell section"* / *"Try the new Up Sell section"* (*"We have redesigned the … section to make it easier for you"*) — pointing the merchant at the redesigned sections. The offer records themselves are unchanged; the redesign is about how Cross Sell and Up Sell are organised and reached.

### Triggers on two cart events: add-to-cart + quantity update
The app subscribes to TWO storefront events:
- `cart.add.post` — after the customer clicks Add to Cart.
- `cart.product.quantity.post` — after the customer changes a quantity in the cart.

Both events fire the same handler — so cross-sell prompts can appear both at initial-add AND at quantity-edit time. Default state for these subscriptions is **INACTIVE** (the merchant must activate them in [[settings-hooks]] for the cross-sell prompts to fire).

### `hasStatusChange = false` — order events not used
Cross-Sell does NOT listen to order-status changes. Cross-sell prompts only fire during the live cart flow, not after order placement.

### Two display modes: popup OR add_to_cart
Each cross-sell rule has a `display_type` set to either:
- **`popup`** — a modal overlay is rendered with the cross-sell offer (using `modal-dialog-crosssell` class). The default cart side-panel is disabled when this fires.
- **`add_to_cart`** — the cross-sell offer is automatically added to the cart inline (no modal). May still trigger a popup confirmation when an extra opt-in is required.

### "Hide cart products from suggestions" toggle
Each cross-sell rule has a `hide_cart_products` flag. When ON, the cross-sell engine filters out cart items that are themselves cross-sell TARGETS (so the customer doesn't see "Add product X" when X is already in their cart due to a previous cross-sell). The merchant uses this to avoid recommending things the customer already accepted.

### Random rule selection (when multiple match)
When multiple cross-sell rules match the current cart contents, the platform calls `inRandomOrder->first` — i.e., it randomly picks ONE rule to fire. There is no priority field, no sequential firing, and no "show two at once" mode. To favor specific rules, the merchant disables less-preferred ones.

### Cross-sell from existing order (re-order with same cross-sell)
The platform supports a "populate cart from order" flow — when the customer clicks a cross-sell link with `order_id` and `cross_sell` query parameters, the platform copies the original order's items into the new cart, then applies the cross-sell rule, then redirects to checkout. This is how the merchant builds "Re-order with X added" links from order-confirmation emails.

### Active cross-sells must pass three checks
Each cross-sell record is filtered through:
- `active` — the rule is enabled.
- `whereNotNo` — non-skip status.
- `whereAllowView` — the rule's view rules (e.g., customer-group visibility) allow the current visitor.

So even if a rule matches the cart contents, customer-group restrictions can still hide it (e.g., "VIP-only cross-sell" never appears to logged-out visitors).

### Errors silently logged
If a cross-sell rule query throws an exception, the platform logs it to its internal exception store and returns the original response unchanged — the cart action proceeds without showing the cross-sell. The customer never sees an error message; the merchant has to inspect the logs to find broken rules.

## Open questions

(none — this is a gateway/redirect page. Full management documentation lives in [[marketing-cross-sell]].)
