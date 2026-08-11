---
type: feature
nav_path: "Settings → Payment methods → Installed providers list"
route_name: admin.payments
route_path: /admin/settings/payment_providers
aliases: ["Installed payment providers list", "Payment methods table", "Payment providers table", "Списък с инсталирани платежни методи"]
tags: [settings, payments, providers, list, navigation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-payment-providers]]. See the hub for related aspects (Add modal, filtering, activation, uninstall, credentials shell, record fields).

# Payment methods — Installed providers list

## Purpose

This aspect documents the main table on the Payment methods landing page — the list of every provider the merchant currently has installed, with click-through to each provider's dedicated configuration screen, an inline Status badge, a Remove button per row, and a "View more Payment methods" footer link to the App Store. The list is also the entry-point for the **+ Add payment method** modal (covered in [[settings-payment-providers-add-modal]]) and the activation toggle (covered in [[settings-payment-providers-activation]]).

## Where to find it

Sidebar → Settings → **Payment methods**. Route: `/admin/settings/payment_providers`. The page renders a single table directly under the header — there are no tabs and no sub-navigation; everything on this aspect is on one Vue page.

**Two URLs for the same screen:** `/admin/settings/payment_providers` (with underscore — legacy Settings-routes URL) AND `admin.payments` (modern canonical sidebar link) both resolve to this same Vue page. There is no `-new` modern counterpart — this IS the modern Vue page. The underscore URL is preserved for legacy bookmarks and the platform's protected-area routing regex.

## What the merchant can do here

- **See the list of installed payment methods** in a table — provider icon + name, "Installed" badge, optional "Recommended" / "Featured" badges (driven by active CloudCart marketing campaigns — see [[settings-payment-providers-filtering]]), active status, and a Remove button.
- **Click a provider's name (or anywhere on the row)** to navigate to its dedicated configuration screen. The destination route is `apps.<provider>.settings` (e.g., clicking CloudCart Pay opens [[payment-providers-cloudcart-pay-settings]]; clicking Borica Way4 opens [[payment-providers-borica-way4]]).
- **Toggle the Active status badge** on a provider — flips the row's Status between Active and Inactive without uninstalling. Full mechanics (including the activation guard) on [[settings-payment-providers-activation]].
- **Remove (uninstall) a provider** with the Remove button. Destructive — see [[settings-payment-providers-uninstall]].
- **Open the Add Payment Method modal** by clicking **+ Add payment method** in the top-right action slot — see [[settings-payment-providers-add-modal]].
- **Browse more providers in the App Store** by clicking **View more Payment methods** at the bottom of the table — opens the App Store filtered by Payment-methods category (route `apps.all` with `?category=13&filter=all`).

What the merchant CANNOT do from this table:

- Configure provider-specific settings inline — those live on each provider's own page.
- **Reorder providers** — there is no sort or drag control. The list order is fixed by the provider record's `sort_order` (set by the platform / by sequence of install). Merchants who want to "promote" a payment method visually at checkout do so via [[settings-cart]]'s "Choose a default payment provider" dropdown (which pre-selects it) or by re-installing providers — there's no drag-and-drop reorder on this page.
- **Filter or search** the installed-providers list — the table is hidden-pagination and shows everything installed in one view.

## Settings & fields

### Page header

| Element | What it shows | Notes |
|---------|---------------|-------|
| **Description line** | *"Add and configure payment methods for your clients"* | Page sub-header. |
| **+ Add payment method** button | Opens the install modal — see [[settings-payment-providers-add-modal]]. | Primary button in the top-right action slot. |

### Installed-providers table

| Column | Shows | Notes |
|--------|-------|-------|
| **Payment method** | Provider icon + name + status badges. | Click anywhere on the row navigates to `apps.<provider>.settings`. The display name comes from the provider's configured `title` (custom) or falls back to the provider's stock `name`. Shows two badges: "Installed" (always for installed rows) and "Recommended" (when an active marketing campaign promotes this provider — see [[settings-payment-providers-filtering]]). |
| **Status** | Active / Inactive badge. | Backed by the configuration's `active` flag (`yes`/`no` in storage, true/false in UI). Toggling described on [[settings-payment-providers-activation]]. |
| **(remove)** | Per-row Remove button. | Clicking calls the uninstall endpoint and removes the row optimistically. Destructive — see [[settings-payment-providers-uninstall]]. |

The table hides pagination — every installed provider is shown in a single page. A **View more Payment methods** footer link opens the App Store filtered to category 13 (Payment methods).

### Cog menu (per-row action menu)

On hover / focus, each installed row exposes:

- **Activate / Deactivate** — flips the Status badge (see [[settings-payment-providers-activation]] — the gateway can refuse with HTTP 422).
- **Settings** — same as clicking the row name; opens `apps.<provider>.settings`.
- **Uninstall** — destructive; deletes the provider configuration row (see [[settings-payment-providers-uninstall]]).

## Business rules

### Clicking a row navigates to provider-specific settings

Each row's name links to `apps.<provider>.settings` (e.g., `apps.cloudcart_pay.settings`, `apps.fibank_bnpl.settings`). These per-provider routes are defined elsewhere in the codebase by the per-provider Vue routers. The Add modal uses the same naming convention: `apps.<map>.settings`. **If the Vue router has no route by that exact name, the click is a no-op** — defensive guard against partial migrations between provider names.

### Hash deep-linking — `#add-payment` auto-opens the Add modal

If the URL contains `#add-payment`, the page automatically opens the Add Payment Method modal one second after mount, then clears the hash. Useful for "click here to add a payment method" call-to-action links elsewhere in the platform (e.g., dashboard widgets, onboarding checklists). Full modal behaviour on [[settings-payment-providers-add-modal]].

### One Vue page, two URLs

The legacy URL `/admin/settings/payment_providers` (with underscore) and the modern route name `admin.payments` both resolve to this Vue page. The platform routing layer expects the underscore URL in its protected-area regex; the modern route name is the canonical link from the sidebar.

### List feeds [[settings-cart]]'s default-payment-provider dropdown

The installed-providers list is consumed in two places:

- This page (installed providers list).
- [[settings-cart]] → Box: Payment and Shipping → "Choose a default payment provider" dropdown, AND Box: Payment methods → "Payment methods" multi-select for manual orders.

So installing, removing, or renaming a provider here immediately changes what the merchant sees as options in those Cart settings on next page load. The renaming is via `storefront_name` — see [[settings-payment-providers-record-fields]].

### No reorder, no search

There is no drag-and-drop reorder, sort header, or search box on this table. The merchant sees the list ordered by `sort_order` (assigned by the platform). For visual promotion at checkout, see the [[settings-cart]] default-payment-provider setting.

## Related

- [[settings-payment-providers]] — hub.
- [[settings-payment-providers-add-modal]] — the **+ Add payment method** modal opened from this list.
- [[settings-payment-providers-activation]] — the Status toggle on each row.
- [[settings-payment-providers-uninstall]] — the Remove button on each row.
- [[settings-payment-providers-filtering]] — what populates the list (operation country, soft-deleted apps, dev-only apps); what drives the Recommended / Featured badges.
- [[settings-payment-providers-record-fields]] — the `storefront_name`, `sort_order`, and `active` fields the table reads from.
- [[settings-cart]] — default-payment-provider dropdown that consumes this list.
- [[apps]] — App Store; "View more Payment methods" footer link target.
- [[payment-providers-cloudcart-pay-settings]] / [[payment-providers-borica-way4]] — example per-provider destinations of the click-through.

## Open questions

_None._
