---
type: feature
nav_path: "Design → Themes → Purchase flow"
route_name: admin.templates.purchase
route_path: /admin/storefront/templates/purchase/{mapping}
aliases: ["Buy theme", "Theme purchase", "Paid theme checkout", "Theme subscription purchase"]
tags: [design, themes, templates, purchase, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Themes — Paid theme purchase flow

> Part of [[design-themes]]. See the hub for related aspects (catalogue, install, unpaid-middleware, switch-effects, plan-gates, edge-cases).

## Purpose

Paid themes are sold as **site subscriptions** — independent of the merchant's plan subscription. This aspect documents the buy flow from the **Buy `<price>`** button on a paid theme card through checkout completion and the auto-install that follows successful payment.

## Where to find it

Triggered from a paid (not-yet-purchased) theme card on `/admin/storefront/templates` — see [[design-themes-catalogue]].

| Action | Route name | Path | Method |
|--------|------------|------|--------|
| Open purchase page | `admin.templates.purchase` | `/admin/storefront/templates/purchase/{mapping}` | GET |
| Add theme to cart and start checkout | (paid theme buy) | `/admin/storefront/templates/purchase/{mapping}` | POST |

## What the merchant can do here

On the **purchase page** for a paid theme:

- See the theme's full description, screenshot, and headline price (VAT-inclusive amount displayed; an explicit VAT-notice label is shown below).
- Click **Buy** — POSTs to the same URL, which initialises the cart with this theme as the only item and redirects to `/admin/checkout` to complete payment.

## What the merchant cannot do here

- Cannot **install a paid theme** without buying it first — the install action on a paid-not-yet-purchased theme silently redirects to this purchase page.
- Cannot **return / refund** a purchased theme through this screen — paid themes are stored as subscriptions; refunds are handled outside the theme picker.
- Cannot keep **other cart items** when buying a theme — the cart is cleared when adding the theme.

## Settings & fields

### Buy form action

| Action | Trigger | Result |
|--------|---------|--------|
| **Buy** | Click "Buy `<price>`" on a paid-not-yet-purchased theme card | Opens the theme's purchase page. |
| **Buy** (on the purchase page) | Submit the buy form | Clears the cart, adds this theme to the cart, redirects to `/admin/checkout`. |

## Business rules

### Paid theme purchase flow — end to end

1. The merchant clicks **Buy** on the theme card → routes to `admin.templates.purchase/{mapping}` (a one-item purchase page showing the theme screenshot + headline price + VAT notice).
2. The merchant clicks **Buy** on the purchase page → POSTs to the same URL, which **clears the cart** and re-initialises it with this theme as the only item, then redirects to `/admin/checkout`.
3. The merchant completes payment on the checkout (standard CloudCart payment flow — see [[details-billing]] / [[details-billing]]).
4. After successful payment, the site is redirected to `admin.templates.change/{mapping}` for this theme, which installs it as the active theme and clears the `unpaid_template` flag — see [[design-themes-install]].

### The cart is **cleared** when adding a theme

Any other items the merchant had in their cart (apps, plan upgrades, services) are removed in favour of just the theme purchase. The merchant has to re-add other items if they wanted a combined purchase.

### Purchase page redirects away if already paid

If the theme is already paid for (`is_paid = true`), the purchase page redirects back to the themes list — there is no separate "already owned" state on this page.

### `redirectAfterPay` puts the install URL in the SESSION, not a DB column

After a paid theme is fully paid for, the platform reads `session('redirect_after_install')` to route the merchant straight into the install endpoint. The theme record's `redirectAfterPay` hook stamps that session key with `route('admin.templates.change', $mapping)` AND clears `unpaid_template` to 0. Standard CloudCart checkout's post-success handler consumes that session key.

### Theme as a subscription

Paid themes are modelled as **site subscriptions** (in the same table as plan subscriptions). The `is_paid` check is: does a subscription row exist for `site_id` + `model_type = 'theme'` + `mapping` AND is it paid?

Subscriptions can later be cancelled / refunded through the billing surface, but that does **not** auto-uninstall the theme — the storefront keeps rendering with the theme until the merchant manually installs a different one.

### Demo user purchase is short-circuited

The demo account does NOT actually go through checkout when buying a paid theme — see [[design-themes-edge-cases]].

### Unpaid theme locks the admin

If checkout is abandoned mid-purchase and the site ends up with `unpaid_template` set, every admin route (except a small allowed-route allowlist) is redirected to checkout for the unpaid theme. See [[design-themes-unpaid-middleware]] for the full mechanic.

## Related

- [[design-themes]] — hub.
- [[design-themes-catalogue]] — where the Buy button lives.
- [[design-themes-install]] — the post-payment install step.
- [[design-themes-unpaid-middleware]] — what happens if checkout stalls.
- [[details-billing]] — billing context for paid-theme purchases.
- [[details-billing]] — invoices for theme purchases.
- [[subscriptions]] — current subscription view (paid themes appear as subscription items).

## Open questions

- 📡 **Trial-store paid-theme buying.** Trial stores see paid themes as buyable; the purchase flow is unblocked. GraphQL-resolvable: query the merchant's plan / trial state to determine whether this store is on a trial plan.
