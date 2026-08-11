---
type: feature
nav_path: "Design → Themes → Unpaid-theme middleware"
route_name: admin.templates.list
route_path: /admin/storefront/templates
aliases: ["Unpaid theme", "unpaid_template flag", "Theme admin lock", "Unpaid template middleware"]
tags: [design, themes, templates, middleware, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Themes — Unpaid-theme middleware

> Part of [[design-themes]]. See the hub for related aspects (catalogue, install, purchase, switch-effects, plan-gates, edge-cases).

## Purpose

When a site has the `unpaid_template` flag set — typically because the merchant signed up with a paid theme during onboarding and skipped payment, or abandoned mid-checkout — a request-level middleware **locks the entire admin** to a small allowlist of routes until the merchant either pays for the theme OR switches to a free theme. This aspect documents the lock, the allowlist, the escape hatch, and the demo-user short-circuit.

## Where to find it

The middleware runs on **every admin request**. The merchant lands on the unpaid-theme checkout flow regardless of which admin URL they tried to open.

## What the merchant can do here

Only these routes remain reachable while `unpaid_template` is set:

- **Themes** (`admin.templates.*`) — so the merchant can switch back to a free theme.
- **Checkout** (`admin.checkout` and `admin.checkout.*`) — so the merchant can complete payment.
- **Login** (`admin.login`) — so the merchant can sign in.
- **Billing** (`admin.billing.*`) — so the merchant can manage billing.
- **2FA flows** (`admin.account.cc2fa` and `admin.account.cc2fa.*`, `admin.core.cc2fa.*`).

Every other admin request is **redirected to checkout** for the unpaid theme.

## What the merchant cannot do here

- Cannot use **any other admin screen** (products, orders, marketing, settings, etc.) until the flag is cleared.
- Cannot **dismiss** the lock — there is no "skip" or "remind me later" option.
- Cannot **bypass** via direct URL — the middleware checks every admin route.

## Settings & fields

This aspect has no merchant-editable fields. The lock state is the site-level `unpaid_template` flag (1 / 0).

## Business rules

### How the lock activates

`unpaid_template` is set when:

- A new site is created with a paid theme assigned but the trial-onboarding skipped payment.
- A theme purchase is initiated but checkout is abandoned before payment succeeds.

While the flag is set, the middleware runs on every admin request.

### Lock behaviour per request

If the current route is **not** in the allowed list (Themes / Checkout / Login / Billing / 2FA), the middleware:

1. Loads the unpaid theme record (`mapping` from the site).
2. Ensures the cart has the theme as an item — re-initialises the cart with the theme if not.
3. Redirects the request to checkout.

### Escape hatch — two paths

The merchant has two ways out:

1. **Pay for the theme** — complete checkout. After successful payment, the platform redirects to `admin.templates.change/{mapping}` which installs the theme and clears `unpaid_template`. See [[design-themes-purchase]] for the full payment flow.
2. **Switch to a free theme** — open Themes (the allowed route) and install any free theme. The install handler clears `unpaid_template` as part of its side-effects (see [[design-themes-install]]).

### Demo user is short-circuited

If the logged-in user is CloudCart's demo user (`demo.user_id` from config), the unpaid-theme middleware redirects to the `redirect_after_install` URL **without going through checkout**. The demo account does not actually pay or change anything on the site — see [[design-themes-edge-cases]].

### The flag is cleared in two ways

- Successful payment of the theme purchase (via `redirectAfterPay` → `admin.templates.change/{mapping}` → clears flag in the install transaction).
- Switching to a free theme via the Themes screen (the free-theme install also clears the flag).

## Related

- [[design-themes]] — hub.
- [[design-themes-purchase]] — the payment flow that clears the flag on success.
- [[design-themes-install]] — the install handler that also clears the flag when switching to a free theme.
- [[design]] — parent Design pillar; the same lock is mentioned in the mystore overview.

## Open questions

None.
