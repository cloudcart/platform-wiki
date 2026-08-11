---
type: feature
nav_path: "Apps → Private Store"
route_name: apps.private-store.overview
route_path: /admin/apps/private-store
aliases: ["Private Store", "B2B Store", "Login-required store", "Wholesale store", "Скрит магазин", "enable disable button", "app active toggle"]
tags: [apps, administration, b2b, access-control, storefront-mode]
plan_gates: ["private-store"]
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# Private Store (B2B / login-required mode)

## Purpose

**Private Store** integration — locks the entire storefront behind a login wall. Visitors who aren't logged in are redirected to a sign-in page (or a custom "request access" landing) instead of seeing products. Used by:

- **B2B / wholesale merchants** who don't want public price visibility — only registered B2B buyers see the catalog.
- **Members-only clubs** (e.g., warehouse-club models, professional-only stores).
- **Beta / preview stores** during pre-launch.
- **Reseller-only catalogs** (manufacturers selling exclusively to authorised dealers).

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it — a disabled app stops working while keeping its settings. The button is briefly absent while the screen is still loading its configuration; it appears once the settings arrive.

## Where to find it

Sidebar → Apps → install → **Private Store**. See [[apps-private-store-settings]] for configuration.

## What the merchant can do here

- Activate to enable storefront-wide login wall.
- Configure the **redirect page** — where unauthenticated visitors land (login page, request-access form, marketing landing, etc.).
- Configure registration / access-approval policy (auto-approve all registrations OR manual review).

### What the merchant CANNOT do here
- Apply Private Store selectively to PARTS of the catalog — it's all-or-nothing (entire storefront becomes private).
- Make products visible publicly while pricing is hidden — that's a separate flow (typically a "show price after login" pattern, not Private Store).

## Settings & fields

- **Redirect page** — where unauthenticated visitors land (login page, request-access form, or marketing landing). Cached for 1 hour, but saving the settings refreshes the cache immediately, so an edited redirect page takes effect right away.

## Business rules

### Entire storefront gated — login wall is all-or-nothing

Every storefront URL redirects to the configured page if the visitor is not logged in. The gated pages are: homepage, search, selections, showcase, vendors page + vendor view, tag pages, category list + view, blog list + view + article, content pages, feed, sitemap, bundle list + category, product view, compare.

Pages NOT gated (contact page, account pages, GDPR forms, login form itself) stay accessible — this is what lets the customer log in.

The login wall is skipped (bypassed) when: the current page is outside the gated list; the Private Store setting is absent; the "require registration" toggle is off (installed but not enforcing); or the URL matches the merchant's allowlist. The allowlist supports a mixed mode, so a public homepage + private catalog is a valid setup.

### Trade-off: SEO

Private Store kills public SEO — search engines can't crawl protected content. Merchants accept this for B2B exclusivity.

### Unconfirmed email forces redirect to account

If a logged-in customer's email is not confirmed AND the platform's unconfirmed-accounts policy is anything other than "none", the customer is sent to the My Account page to confirm their email before they can browse.

### Auto vs manual access approval

When the **registration approval** setting is ON, new registrations are created inactive — the merchant must approve each one before the customer can log in (true B2B gating). When OFF, new registrations are immediately active (sign-up just adds a friction step). Toggle in [[apps-private-store-settings]].

### Allowed-pages whitelist

The merchant can whitelist specific Pages (Privacy Policy, About Us, etc.) so they stay public while the rest of the store is gated. A separate toggle keeps the entire blog publicly visible.

### Binary access — no per-customer-group tiers

Gating only checks whether the visitor is logged in (and, if the email-confirmation policy is on, whether email is confirmed). There is no check against [[customers-custom-groups]]: once logged in, a customer sees the entire catalog regardless of group. For group-based visibility (VIP-only products, B2B-tier pricing), combine Private Store with [[customers-custom-groups]] and per-product / per-category group restrictions on the catalog itself.

### Standard registration form — no bespoke fields

There is no separate "request access" form; the customer fills the regular storefront registration form, and Private Store just flips the new customer's active flag based on the approval setting. The merchant CANNOT add bespoke fields ("company VAT", "tax ID", "wholesale license") without customising the theme or using a third-party customer-fields app.

### Approval workflow — no native queue or notification

There is no Private Store-specific pending queue, no "approve all" button, and no automatic notification when a customer lands in a pending state. Pending registrations appear in the standard [[customers]] list filtered by inactive; the merchant bulk-approves via multi-select + edit. Workaround for notifications: use [[apps-workflow]] to trigger an email on customer creation.

### Private Store vs Membership — different layers, combinable

Private Store gates ACCESS (can the customer browse the store at all?). Membership ([[apps-membership]]) gates SPECIFIC CONTENT (can the customer view specific pages/products?). They run independent gates and can be combined into a "B2B portal where members get even more" tier model.

### Redirect page must stay active

Only pages currently marked active are eligible as the redirect target. If the merchant archives the page set as the redirect destination, the platform falls back to the default login page (always accessible). So do not archive a page used as a Private Store landing page without first pointing the setting at another active page.

### Permission

Standard apps permission scope.

## Plan gates

This feature is gated by the `private-store` plan-feature (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `private-store` | Boolean (plan-level enable) | Whether the merchant can install the Private Store app + activate the storefront-wide login wall. |

`private-store` is access-shaped (boolean): lower plans get redirected to the per-feature upsell at [[plan-features]] or a plan-upgrade panel, and must upgrade (or use a pack that flips it on for the pack's duration). The app is included on Pro / Business / Enterprise tiers by default in most catalogs.

## Related

- [[apps]] — App Store.
- [[apps-private-store-settings]] — settings sub-page.
- [[customers]] — customer database (gated users).
- [[customers-custom-groups]] — group-based access typically combined.
- [[customer-group]] — entity page.
- [[apps-membership]] — sister storefront-mode app for paid membership.

## Open questions

