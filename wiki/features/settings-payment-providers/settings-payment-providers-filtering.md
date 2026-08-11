---
type: feature
nav_path: "Settings → Payment methods → Provider availability filtering"
route_name: admin.payments
route_path: /admin/settings/payment_providers
aliases: ["Why a payment provider is missing", "Provider availability", "Operation-country filter", "Recommended payment method badge", "Featured payment method badge", "Защо не виждам платежен метод"]
tags: [settings, payments, providers, filtering, plan-gates, marketing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-payment-providers]]. See the hub for related aspects (list, Add modal, activation, uninstall, credentials shell, record fields).

# Payment methods — Provider availability filtering

## Purpose

This aspect documents **what controls which payment providers a given store sees on the Payment methods page** — both in the installed-providers list ([[settings-payment-providers-list]]) and in the **+ Add payment method** modal ([[settings-payment-providers-add-modal]]). The backend's listing endpoint returns ALL providers (installed + available) with an `installed` boolean per row, but applies four filters before returning. It also surfaces "Recommended" / "Featured" badges driven by CloudCart's marketing campaigns. When a merchant asks *"Why don't I see payment provider X in my list?"*, this is the page that answers.

## Where to find it

The filters are not exposed to the merchant as UI controls — they happen server-side every time the page loads. The merchant experiences them as the **shape of the list** at Sidebar → Settings → **Payment methods** (route `/admin/settings/payment_providers`).

The two operator settings that influence what the merchant sees are on [[settings-general]] (operation country) and the merchant's subscription plan (plan-feature gating, edited by CloudCart support / billing).

## What the merchant can do here

There are no merchant-facing controls for the filters themselves — the filters are server-side and not configurable per merchant. Indirect actions the merchant can take to change what they see:

- **Change the store's operation country** via [[settings-general]] — exposes providers that target the new country and hides providers that don't (e.g., switching from Bulgaria to Romania changes the available BNPL gateways).
- **Upgrade or downgrade the store's plan** — unlocks or hides plan-gated providers.
- **Install a dev-only / internal app** (via a direct app install link from CloudCart support) — once installed, that provider stays visible on this page even though it's normally hidden.

## Settings & fields

This aspect has no merchant-editable fields on the Payment methods page itself. The four filters and the two marketing flags are properties of the **underlying App row** for each provider (managed by CloudCart, not the merchant).

| Filter / flag | Source | Effect |
|----------------|--------|--------|
| Operation country | App row's country-availability map | Provider hidden if the store's `operation_country` (from [[settings-general]]) is not in the App's supported countries. |
| Soft-deleted app | App row's deleted timestamp | Provider hidden entirely if CloudCart soft-deleted the underlying App from the catalog. |
| Dev-only flag | App row's dev/internal flag | Provider hidden from the Add modal unless this store has explicitly installed it. Installed dev apps remain visible. |
| Plan-feature gate | Plan / feature-provider mapping | Provider may be hidden or shown read-only depending on whether the store's plan includes the required feature. |
| `recommended` | Marketing model | Drives the **Recommended** badge on the row + Add-modal card. Active marketing entry only. |
| `featured` | Marketing model | Drives the **Featured** badge. Active marketing entry only. |

## Business rules

### Filter 1 — Operation country gates availability

The provider's underlying App must be available for the store's `operation_country` (configured in [[settings-general]]). Providers not available for that country are excluded entirely. So a **Bulgarian merchant won't see Romania-only providers** in either the installed list or the Add modal, and vice versa.

Switching `operation_country` on [[settings-general]] reshapes this list on next page load. A previously-installed provider whose country no longer matches will continue to appear in the installed list (its configuration row exists) but cannot be re-installed from the Add modal once removed — the merchant would first have to switch operation country back.

### Filter 2 — Soft-deleted apps drop out entirely

If the underlying App row is **soft-deleted** by CloudCart (the App's `deleted_at` is set — CloudCart removed it from the catalog), the provider is omitted entirely from both the installed list and the Add modal. This means a payment method that was previously available may silently disappear from this page if CloudCart deprecates its app — without uninstalling it from the merchant. The merchant should treat that as **"no longer offered"** rather than "broken".

This is a known operations consideration: when CloudCart support deprecates a gateway, existing merchants stop seeing the row on the Payment methods page, even though their underlying configuration row still exists in the database. Reactivation requires CloudCart support to restore the App row from soft-delete.

### Filter 3 — Dev-only apps are hidden unless installed

Provider apps marked as **dev/internal-only** are excluded from the Add modal for all stores, except if a particular store has explicitly installed them (typically via a direct support-issued install link). Keeps test / pilot integrations out of the general merchant catalog while letting developers and pilot merchants exercise them — a developer-installed app stays visible on the developer's store, but other merchants don't see it.

### Filter 4 — Plan-feature gating

Payment providers can be **plan-gated** via a feature-provider mapping (e.g., advanced providers locked behind higher plans). The store's subscription plan determines whether the provider appears in the Add modal at all. For installed providers on a plan that no longer includes the feature, the row may still appear but the provider's activation may be blocked — see [[settings-payment-providers-activation]] for how activation guard reports this.

### "Recommended" and "Featured" badges come from active marketing campaigns

Each provider's underlying App has a `recommended` and `featured` relation to the Marketing model. These badges appear only when there is an **active** marketing entry with a current activity period for the App. Effects:

- Which providers show as Recommended / Featured **changes over time** as CloudCart's marketing team configures campaigns.
- There is **no per-merchant setting** that controls which providers show the badge.
- The badge does **not** pin a provider to the top of the list — it just adds a visual marker. The actual list order is fixed by `sort_order` on the provider record. To "promote" a payment method visually at checkout, the merchant uses [[settings-cart]]'s "Choose a default payment provider" (which pre-selects it).

### Filters apply equally to installed and available providers

The four filters above apply to both halves of the page — what's listed as installed AND what's offered in the Add modal. So if a previously-installed provider's underlying app gets soft-deleted, the installed row disappears too (not just the Add modal card).

### JSON-API v2 does NOT apply these filters

The JSON-API v2 read endpoint returns ALL installed provider records — it does NOT apply the operation-country, soft-deleted, dev-only, or plan-feature filters that the UI applies. A provider record can be `active=true` in the API response but still hidden from checkout if the plan-feature or country filter excludes it. Consumers must treat the `active` flag as **necessary-but-not-sufficient** for checkout visibility. See [[settings-payment-providers-record-fields]] and [[api-payment-providers]].

## Related

- [[settings-payment-providers]] — hub.
- [[settings-payment-providers-list]] — the installed-providers table this filtering shapes.
- [[settings-payment-providers-add-modal]] — the Add modal this filtering shapes.
- [[settings-payment-providers-activation]] — plan-feature gating may also block activation post-install.
- [[settings-general]] — `operation_country` setting drives Filter 1.
- [[plan-gates]] — plan-feature mapping drives Filter 4.
- [[apps]] — the underlying App rows; soft-delete / dev-only flags drive Filters 2 and 3.
- [[api-payment-providers]] — JSON-API v2 does NOT apply these filters.
- [[settings-cart]] — default-payment-provider dropdown for visual promotion (separate from Recommended badge).

## Open questions

_None._
