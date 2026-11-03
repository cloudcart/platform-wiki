---
type: feature
nav_path: "Orders → Subscriptions → Settings"
route_name: apps.membership.settings
route_path: /admin/orders/subscriptions/settings
aliases: ["Membership settings", "Subscriptions settings", "Subscription configuration", "Настройки на абонаменти", "Настройки на членство"]
tags: [administration, membership, orders, subscriptions]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 6
---
# Subscriptions settings (Membership app)

## Purpose

The **Settings** sub-screen for the Membership app — where the merchant configures how customer-side memberships work on the storefront: which products unlock subscriptions, how many days each tier provides, and the messaging shown when a customer's subscription expires.

This is owned by the Membership app and is only available after the app is installed ([[orders-subscriptions]] for install).

## Where to find it

Sidebar → **Orders** → **Subscriptions** → **Settings** tab.

## What the merchant can do here

The Settings tab is a thin wrapper over the platform's shared app-settings panel — it shows the Membership app's own settings rows (whatever the app declares via its config schema) PLUS the standard app chrome:

- The active/inactive status row + activation toggle.
- A **+ Create new** button (top-right) — same Add Subscription modal as the Memberships overview tab (see [[orders-subscriptions]]).
- A nav row with two tabs: *Memberships* (the list) and *Settings* (this screen).
- The app's settings rows (currently empty for stores on the default Membership template — the per-product page mapping lives on the product editor, NOT here).
- A **Save changes** bar at the bottom (when any setting becomes dirty).

## Settings & fields

The Membership app currently ships WITHOUT any settings fields on this screen — it's a placeholder slot that the shared app shell renders for every installed app. The actual per-product membership configuration (which pages a product unlocks, how many days each unlock grants) is set on the product editor in [[products-products]] under the product's pages tab (`ProductPages` association).

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Active / Inactive** status toggle | Activates / deactivates the Membership app | Active when installed | When deactivated, the auto-create-on-paid logic stops running. |
| **+ Create new** button | Opens the Add Subscription modal (manual VIP creation) | — | Same modal as on the Memberships tab. |

Per-product `days` value (set on each linked page in the product editor) — see [[orders-subscriptions]] for the auto-create logic that consumes this value.

## Business rules

### Settings live in the app's namespace

Settings written here are stored under the Membership app's namespace and migrate with the app. Uninstalling the app removes them.

### Status taxonomy

Membership subscriptions on the customer side use three states (all DERIVED from the single `expired` date column — there is no stored status field):

- **Active** — `expired` is in the future. Badge: green *Active*.
- **Inactive** — `expired` is in the past. Badge: grey *Inactive*. (Renders as *Disabled* in the status filter dropdown.)
- **Unlimited** — `expired` is NULL. Renders *"Unlimited"* in the date column. The Status badge for these rows shows **Active** (the controller's `format` returns `is_active = true` when `expired` is NULL).

The status filter ONLY accepts Active / Disabled values — unlimited rows are silently excluded from both buckets when the filter is applied.

## Related

- [[orders-subscriptions]] — the parent overview screen / install entry.
- [[orders]] — parent module.
- [[apps]] — where the Membership app can be installed/uninstalled.

## How it works (verified against backend)

### Configuration is on the PRODUCT — not in this settings screen

Hidden architecture: the actual "what pages does this product unlock?" mapping is configured PER PRODUCT on the product editor (via [[products-products]]). Each product has a `ProductPages` relationship listing pages with a `days` value (int). The "Settings" tab here is for global app preferences; tier/duration is product-level.

So to add a new membership tier, the merchant edits the relevant DIGITAL product → links it to one or more pages → sets `days` per page. Not in this settings tab.

### Membership products MUST be digital

Hidden rule: the auto-create logic on order paid status only iterates products with `digital = 'yes'`. If a merchant ties pages to a non-digital product, NO subscription is created on purchase. This is silent — no error, no warning. The merchant must set the product's `digital` flag in [[products-products]].

### `days = 0` on the product-page link → UNLIMITED subscription

If a `ProductPages` row has `days = 0` (or NULL), the membership created on purchase has `expired = NULL` → unlimited / lifetime access. The merchant uses this for "lifetime membership" products.

### No "max active subscriptions per customer" cap

There's no per-customer subscription limit. A customer can buy multiple membership products and stack subscriptions for the same page (extending the expiry each time).

### No renewal flow at the storefront

The Membership app doesn't auto-charge for renewal. When a subscription expires, the customer simply loses access — to renew, they purchase the membership product again on the storefront. This is purchase-driven, not subscription-billed.

### No notifications on expiry — segment-driven instead

There's no built-in "your subscription expires soon" email. To drive expiry communication, the merchant uses [[customers-custom-groups]] with the `MembershipExpiration` condition (configurable: "expires in N days") → builds a campaign via [[marketing-campaigns]]. No expiry email is hard-wired.

### App-namespace migration

Membership settings + records use the app's own tables (`@apps_memberships`). Uninstalling the Membership app drops these and clears the data — so the merchant loses ALL active customer subscriptions on uninstall. There's no archive / export-on-uninstall step.

## Open questions

(none — full per-field configuration is the Membership app's responsibility; this screen is a thin wrapper that the app populates. A dedicated Membership-app page documents the full storefront experience.)
