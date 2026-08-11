---
type: feature
nav_path: "Settings → Payment methods"
route_name: admin.payments
route_path: /admin/settings/payment_providers
aliases: ["Payment methods", "Payment providers", "Payment gateways", "Платежни методи", "Начини за плащане"]
tags: [settings, payments, providers, integrations]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---

# Payment methods

## Purpose

The landing page for the store's payment methods. Lists every payment provider the merchant has installed (Cash on delivery, bank transfer, CloudCart Pay, DSK BNPL, FiBank BNPL, FusionPay, Iute, Klear, Stripe, PayPal, EasyPay, ePay, etc.), shows each one's name, icon, and active status, and lets the merchant install more providers, open a provider's dedicated configuration screen, deactivate a provider without uninstalling it, or fully uninstall a provider.

The page itself is a **thin index** — credentials, schemes, mappings, onboarding, transactions, and payouts for any given provider live on the provider's own page under `apps.<provider>.settings`. This hub catalogues the seven aspects this feature splits into; the Assistant should drill into the aspect that matches the merchant's question, not read every page.

## Where to find it

Sidebar → Settings → **Payment methods**.

The page's breadcrumb reads "Settings → Payment methods". The route is `/admin/settings/payment_providers`. The header icon is a credit card. The legacy URL `/admin/settings/payment_providers` (with underscore) and the modern route name `admin.payments` both resolve to the same Vue page — see [[settings-payment-providers-list]] for the two-URL detail.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice:

- [[settings-payment-providers-list]] — the installed-providers table, the per-row click navigation, the cog menu (Activate / Settings / Uninstall), the hidden-pagination one-page view, the `#add-payment` hash deep-link, the two-URL note, and the "View more Payment methods" App Store link.
- [[settings-payment-providers-add-modal]] — the **+ Add payment method** modal, the vertical scroll of provider cards, the `apps.<provider>.settings` navigation on click, the empty-state when everything is installed, and the auto-open behaviour on `#add-payment`.
- [[settings-payment-providers-filtering]] — what filters the list (operation country, soft-deleted apps, dev-only apps, plan-feature gating) and how the "Recommended" / "Featured" badges are driven by active CloudCart marketing campaigns.
- [[settings-payment-providers-activation]] — the Active/Inactive toggle, the **activation guard** (HTTP 422 — provider can refuse to activate until onboarding / credentials / compliance complete), the gateway's own `updateActive` cascade, and the `SiteEventLog` audit trail.
- [[settings-payment-providers-uninstall]] — the destructive Remove action; what configuration is lost (API credentials, schemes, logo, sort order); reinstall is from a clean slate; no soft-delete.
- [[settings-payment-providers-credentials-shell]] — the shared `SettingsFormPayments` 6-slot shell every provider page reuses (`logo`, `mode`, `amount`, `discount`, `description`, `auth`) and the per-gateway credentials index that catalogues what the merchant types for Stripe, myPOS, Klear, CloudCart Pay, BNPL, and the long tail of providers.
- [[settings-payment-providers-record-fields]] — the 11 fields each provider configuration carries (including `min_price` per-provider threshold, `storefront_name`, `initial`/`installment` for BNPL), the `store.payment_providers` permission gate, JSON-API v2 read-only programmatic access, and the [[settings-cart]] consumer.

## What the merchant can do here

The hub itself is navigation only — every concrete action lives on an aspect page. High-level actions, with their aspect:

- **See the installed payment-methods table** — see [[settings-payment-providers-list]].
- **Click a provider's name** to open its dedicated `apps.<provider>.settings` page — see [[settings-payment-providers-list]].
- **Install a new payment method** via the **+ Add payment method** modal — see [[settings-payment-providers-add-modal]].
- **Activate or deactivate** a provider without uninstalling it — see [[settings-payment-providers-activation]].
- **Uninstall** a provider (destructive — credentials and schemes are lost) — see [[settings-payment-providers-uninstall]].
- **Understand why a provider isn't showing in the Add modal** (operation country, plan, soft-deleted app, dev-only) — see [[settings-payment-providers-filtering]].
- **Find what credentials a given gateway needs** (Stripe Secret/Publishable keys, myPOS Configuration package, Borica certificate, Klear API keys, etc.) — see [[settings-payment-providers-credentials-shell]].
- **Set a per-provider minimum order amount** (`min_price`), customer-facing storefront label (`storefront_name`), or BNPL terms (`initial`/`installment`) — see [[settings-payment-providers-record-fields]].
- **Browse more payment methods** via the "View more Payment methods" footer link (App Store, category 13) — see [[settings-payment-providers-list]].

What the merchant CANNOT do here:

- Configure provider-specific settings on this page itself — those live on each provider's own page.
- Reorder providers — there are no sort/drag controls on this list.
- Filter or search the installed-providers list — the table shows everything installed in one view.

## Settings & fields

This hub does not expose any fields directly. Field-level documentation lives per aspect:

- **Installed-providers table columns** (Payment method, Status, remove) → [[settings-payment-providers-list]].
- **+ Add payment method modal** (provider cards, descriptions, Recommended / Featured badges, empty state) → [[settings-payment-providers-add-modal]].
- **Shared `SettingsFormPayments` shell rows** (logo, mode, amount, discount, description, auth) and per-gateway credential fields (Stripe / myPOS / Borica / CloudCart Pay / Klear / BNPL) → [[settings-payment-providers-credentials-shell]].
- **Provider configuration record fields** (11 columns: `name`, `provider`, `map`, `type`, `active`, `storefront_name`, `min_price`, `group`, `initial`, `installment`, `payment_variant_id`) → [[settings-payment-providers-record-fields]].

## Business rules

This hub does not own any business rules directly — each aspect documents the rules it owns. Pointers:

- **Provider visibility filters** (operation country, soft-deleted apps, dev-only apps, plan-feature gating, marketing-campaign badges) → [[settings-payment-providers-filtering]].
- **Activation can be vetoed by the gateway** (HTTP 422 — KYC / credentials / scheme not ready); audit log entries on every toggle → [[settings-payment-providers-activation]].
- **Uninstall is destructive** — credentials, schemes, sort order, logo overrides all lost on Remove → [[settings-payment-providers-uninstall]].
- **The installed-providers list also feeds [[settings-cart]]'s default-payment-provider dropdown and the manual-orders Payment methods multi-select** → [[settings-payment-providers-record-fields]].
- **All endpoints are permission-gated** by `store.payment_providers` (granted from [[settings-staff]]) → [[settings-payment-providers-record-fields]].
- **Programmatic read access via JSON-API v2** is read-only — install / uninstall / activation toggle / configuration edits all require the admin panel → [[settings-payment-providers-record-fields]] + [[api-payment-providers]].
- **Toggling activity, installing, or uninstalling does NOT flush the platform Settings cache** (these are not Setting rows — they're per-provider configuration rows tied to the App). No queued jobs are dispatched. No admin notifications fire → [[settings-payment-providers-activation]] + [[settings-payment-providers-uninstall]].

## Related

- [[checkout-step-payment]] — storefront-side payment step + the 8-stage filter pipeline that decides which providers reach checkout.

- [[payment-providers]] — the full provider directory (jump to any specific gateway's configuration page).
- [[settings]] — parent hub.
- [[settings-general]] — `operation_country` filters which providers are available; `currency` affects which providers can process the store's currency.
- [[settings-cart]] — defaults dropdown + manual-order payment methods consume the same provider list.
- [[settings-invoicing]] — invoice templates may reference the selected payment method.
- [[settings-statuses]] — payment statuses (`paid`, `pending`, etc.) are referenced by provider callbacks.
- [[settings-staff]] — `store.payment_providers` permission grant.
- [[apps]] — the App Store; "View more" footer link points here.
- [[api-payment-providers]] — JSON-API v2 read-only endpoint.
- [[payment-provider]] — entity page (provider record shape).
- [[payment-providers-cloudcart-pay]] — CloudCart's own payment provider hub.
- [[payment-providers-borica-way4]] — Borica Way4 hub (gold-standard BG card gateway).
- [[payment-providers-dsk-bnpl]], [[payment-providers-dsk-zero]], [[payment-providers-fibank-bnpl]], [[payment-providers-fusion-pay]], [[payment-providers-iute]], [[payment-providers-klear]] — per-provider configuration pages.
- [[checkout-flow]] — how the selected payment method is used at checkout.
- [[payment-provider-mechanism]] — the integration model behind every provider (configuration, checkout visibility, confirmation, refunds, tokenization / 3DS).
- [[multi-currency]] — the store currency determines which providers can process payments.
- [[merchant-roles]] — `store.payment_providers` permission gates access.

## Open questions

_None._
