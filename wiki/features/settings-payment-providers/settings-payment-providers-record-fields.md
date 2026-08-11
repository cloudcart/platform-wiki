---
type: feature
nav_path: "Settings → Payment methods → Provider record fields, permissions, API"
route_name: admin.payments
route_path: /admin/settings/payment_providers
aliases: ["Payment provider record fields", "Payment provider min_price", "Storefront name override", "BNPL initial / installment", "Payment provider permission gate", "Payment providers API read-only"]
tags: [settings, payments, providers, record-fields, permissions, api]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-payment-providers]]. See the hub for related aspects (list, Add modal, filtering, activation, uninstall, credentials shell).

# Payment methods — Record fields, permissions, API

## Purpose

This aspect documents the **data shape** behind the Payment methods page — the 11 fields each provider configuration row carries — plus two cross-cutting concerns: the **`store.payment_providers` permission gate** that controls who can see / install / uninstall / toggle providers, and the **JSON-API v2 read-only surface** that lets integrations query installed providers without write access. Useful when merchants ask about per-provider thresholds, BNPL terms, customer-facing labels, or external integrations.

## Where to find it

The fields are exposed across several surfaces: the per-provider settings page (reached by clicking a row on [[settings-payment-providers-list]]) where most fields are editable; JSON-API v2 at `/api/v2/payment-providers` for read-only access (see [[api-payment-providers]]); and [[settings-staff]] → Access permissions where the `store.payment_providers` permission is granted to Moderators.

## What the merchant can do here

- Set a per-provider minimum-order-value (`min_price`) — e.g., "Bank transfer only on orders > 100 BGN".
- Override the customer-facing label (`storefront_name`) — e.g., internal "CloudCartPay" → storefront "Pay with card".
- Configure BNPL terms (`initial` + `installment`) — initial-payment % and installment count for BNPL providers.
- Grant `store.payment_providers` permission to a Moderator via [[settings-staff]] so subordinate staff can manage payment methods.
- Read installed providers programmatically via JSON-API v2 — list providers, check active state, see `storefront_name`, `min_price`, BNPL terms.

What the merchant CANNOT do here: edit `name` or `provider` (platform-managed identifiers); install / uninstall / activate / configure via the JSON-API (read-only — admin panel required); set `min_price` to a non-integer or negative value `(verify)`.

## Settings & fields

### Provider configuration record — 11 fields

Each provider's configuration carries these fields (stored as a per-provider configuration row tied to the underlying App):

| Field | Purpose | Editable from |
|-------|---------|---------------|
| `name` | Provider identifier (internal — e.g., "CloudCartPay", "Borica Way4"). | Platform-managed; merchant cannot rename. |
| `provider` | Provider type / vendor identifier. | Platform-managed. |
| `map` | Provider config / mapping data — generic per-provider blob (e.g., scheme references, gateway-specific settings that don't fit other fields). | Per-provider settings page (varies). |
| `type` | Provider classification (card / bank / wallet / BNPL / cash / etc.). Used by checkout to group providers. | Platform-managed. |
| `active` | Active flag (`yes`/`no` in storage, true/false in UI). Whether the provider is shown at checkout. | Activation toggle on [[settings-payment-providers-list]]; full mechanics on [[settings-payment-providers-activation]]. |
| `storefront_name` | Customer-facing label (may differ from internal `name`). E.g., internal "CloudCartPay" → storefront "Pay with card". | Per-provider settings page → shared shell `description` slot (see [[settings-payment-providers-credentials-shell]]). |
| `min_price` | Minimum order value (in cents) to expose this provider at checkout. Filters out for small carts. | Per-provider settings page → shared shell `amount` slot. |
| `group` | Grouping for display ordering / categorisation at checkout. | Per-provider settings page (where exposed). |
| `initial` | **BNPL only** — initial-payment percentage at checkout. | Per-provider settings page (BNPL providers). |
| `installment` | **BNPL only** — number of installments. | Per-provider settings page (BNPL providers). |
| `payment_variant_id` | Reference to provider variant configuration. | Platform-managed; varies by provider. |

### Permission scope

| Permission | Scope |
|------------|-------|
| `store.payment_providers` | Required for **all** endpoints on the Payment methods page — list, install (Add modal), uninstall, toggle activity, edit per-provider settings. Granted from [[settings-staff]] → Access permissions. A Moderator without it cannot see or manage payment providers — they don't even see the Payment methods item in the sidebar. |

### JSON-API v2 surface

- **Endpoint:** `/api/v2/payment-providers` — see [[api-payment-providers]].
- **HTTP methods:** GET only. Read-only.
- **What's returned:** All installed provider records with their fields above.
- **What's NOT supported:** POST, PATCH, DELETE — install / uninstall / activation toggling / configuration edits all require admin-panel access.
- **Auth:** API key, see [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Business rules

### `min_price` is per-provider, not store-wide

Different providers can have different thresholds. A store can have "Bank transfer only on orders > 100 BGN" and simultaneously "BNPL only on orders > 50 BGN" without conflict.

### `storefront_name` decouples internal identity from customer label

The internal `name` is used in audit logs and integration debugging; `storefront_name` is what the customer sees at checkout. Renaming `storefront_name` does NOT affect the provider's identifier elsewhere — orders that completed using this provider still reference the internal `name`, and JSON-API v2 returns both. Useful for "Pay with card" / "Card payment" / "Bank card" — same gateway, different label per merchant taste.

### BNPL terms are per-provider, not per-promotion

The `initial` + `installment` fields on the provider record represent the **default BNPL terms** the provider quotes at checkout — they are NOT the per-promotion / per-scheme terms BNPL providers offer separately. Providers like DSK BNPL have a separate Schemes sub-tab (see [[payment-providers-dsk-bnpl-promotions]]) that lets the merchant configure multiple promotion tiers; those don't overwrite the base `initial` / `installment` on the provider record.

### JSON-API v2 quirk — does NOT apply UI filters

The JSON-API v2 returns ALL installed provider records, regardless of operation-country, soft-delete, dev-only, or plan-feature gating the UI applies (see [[settings-payment-providers-filtering]]). A provider record can be `active=true` in the data but still hidden from checkout if a UI filter excludes it. Consumers must treat `active` as **necessary-but-not-sufficient** for checkout visibility — to mirror what the storefront actually shows, integrations must additionally check operation country, plan, and underlying app status.

### The list also feeds [[settings-cart]]'s dropdowns

The installed-providers list is consumed in two places beyond this page:

- [[settings-cart]] → Box: Payment and Shipping → "Choose a default payment provider" dropdown.
- [[settings-cart]] → Box: Payment methods → "Payment methods" multi-select for manual orders.

So adding, removing, or renaming a provider here immediately changes what the merchant sees as options in those Cart settings on next page load. The renaming is the `storefront_name` field above.

### Saving fields does NOT flush the platform Settings cache

Provider configuration rows are NOT Setting rows. Editing `min_price`, `storefront_name`, BNPL terms, etc. does NOT flush the platform Settings cache, does NOT dispatch queued jobs, and does NOT fire admin notifications. Changes are effective on next page load (and next API call).

## Related

- [[settings-payment-providers]] — hub.
- [[settings-payment-providers-list]] — the table that surfaces the `active` and `storefront_name` fields.
- [[settings-payment-providers-credentials-shell]] — the shared shell whose `amount` / `description` slots map to `min_price` / `storefront_name`.
- [[settings-payment-providers-activation]] — the toggle that flips the `active` field.
- [[settings-payment-providers-uninstall]] — what destroys these fields.
- [[settings-payment-providers-filtering]] — UI filters NOT applied by the JSON-API.
- [[api-payment-providers]] — JSON-API v2 read endpoint.
- [[json-api-v2]] — API hub (auth, rate limit, side-effects principle).
- [[payment-provider]] — entity page describing the record shape.
- [[settings-cart]] — consumes the installed-providers list for default-payment-provider + manual-orders dropdowns.
- [[settings-staff]] — `store.payment_providers` permission grant.
- [[merchant-roles]] — Administrator vs Moderator scopes.
- [[payment-providers-dsk-bnpl-promotions]] — example BNPL Schemes (separate from base `initial` / `installment`).

## Open questions

- Confirm `min_price` validation rules (negative numbers, non-integer values). `(verify)`
