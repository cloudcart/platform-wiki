---
type: feature
nav_path: "Settings → Payment methods → Activate / Deactivate"
route_name: admin.payments
route_path: /admin/settings/payment_providers
aliases: ["Activate payment provider", "Deactivate payment provider", "Pause payment method", "Активирай платежен метод", "Деактивирай платежен метод", "Спри платежен метод временно", "Activation guard 422"]
tags: [settings, payments, providers, activation, audit-log]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-payment-providers]]. See the hub for related aspects (list, Add modal, filtering, uninstall, credentials shell, record fields).

# Payment methods — Activate / Deactivate

## Purpose

The Active / Inactive toggle on each installed provider row controls whether that provider is **shown to customers at checkout**. Toggling Inactive keeps the provider installed — its credentials, schemes, sort order, logo overrides are all preserved — but hides it from the storefront. This is the recommended path for **temporary suspension** (e.g., during a payment-gateway outage, or while the merchant rotates credentials); compare with full uninstall, which destroys the configuration (see [[settings-payment-providers-uninstall]]).

Activation is not always immediate: the underlying gateway can **refuse** activation with an HTTP 422 error and a merchant-facing reason. This is the "activation guard" — providers like CloudCart Pay block activation until KYC is complete, BNPL providers block until a scheme is configured, card processors block until API credentials pass a verification ping.

## Where to find it

Sidebar → Settings → **Payment methods**. Each installed-providers row has a Status badge (Active / Inactive) — clicking it (or using the cog menu's Activate / Deactivate action) flips the state. The list itself is described on [[settings-payment-providers-list]].

## What the merchant can do here

- **Deactivate an installed provider** without uninstalling — clicks the Active badge or the cog menu's "Deactivate". The provider stays installed but is hidden from checkout. All credentials, schemes, mappings, and per-provider settings are preserved.
- **Reactivate** a previously paused provider — clicks the Inactive badge or the cog menu's "Activate". For providers that have already completed onboarding, this succeeds immediately without re-running the activation guard. For providers that never finished onboarding (or where compliance status has lapsed), the gateway may refuse — see the activation guard below.
- **See the activation-status change in the audit log** — every toggle writes a `SiteEventLog` entry (`TYPE_PAYMENT_ACTIVATED` on enable, `TYPE_PAYMENT_DEACTIVATED` on disable). The entry is visible via the site-event-log view (see [[orders-history]] and the Settings → activity log surface), not on the Payment methods page itself.

What the merchant CANNOT do here:

- Force-activate a provider whose gateway has refused with HTTP 422 — the merchant must resolve the underlying reason (complete KYC, add scheme, fix credentials) first.
- See the audit-log entries inline on the Payment methods page — they're recorded but only visible from the activity-log view.
- Schedule a future activation / deactivation — the toggle is immediate.

## Settings & fields

### Status badge / cog menu

| Control | Position | Action |
|---------|----------|--------|
| **Status badge** | Status column of each installed-provider row. | Click flips Active ↔ Inactive. Posts to the activity endpoint with the new state. |
| **Cog menu → Activate / Deactivate** | Per-row cog menu (hover / focus). | Same effect as clicking the badge — provided for accessibility / keyboard users. |

### Possible failure responses on activation

When the merchant tries to activate, the gateway can respond with HTTP 422 and a reason. The reason is shown as a merchant-facing toast. Common 422 reasons documented in the catalogue:

| Reason | Provider example | Resolution |
|--------|------------------|------------|
| Onboarding not complete | CloudCart Pay account not yet submitted / KYC pending | Complete the onboarding flow on [[payment-providers-cloudcart-pay-onboarding]]. |
| Scheme not configured | BNPL provider with no installments scheme | Configure schemes (e.g., [[payment-providers-dsk-bnpl-promotions]], [[payment-providers-dsk-zero-schemes]]). |
| Required credentials missing | API keys empty, MID unset, certificate not uploaded | Fill in credentials on the provider's settings page (e.g., [[payment-providers-borica-way4]]). |
| Compliance check failed | Processor reports account not yet approved | Wait for processor approval; retry later. |
| Credential verification ping failed | Card processor's verification call returned an error | Re-check the credentials; the gateway may have rotated keys. |

## Business rules

### Activation guard — provider can veto enabling

When the merchant flips the badge from Inactive to Active, the platform asks the **underlying payment gateway service** whether activation is allowed right now. The service can refuse with HTTP 422 + a merchant-facing reason — this is the "activation guard". It's how CloudCart Pay blocks activation until KYC is complete, BNPL providers block until a scheme is configured, and card processors block until credentials pass a verification ping. The merchant sees a 422 toast with the provider-specific reason; the row stays Inactive, no audit-log entry is written for the failed attempt.

**Reactivating an already-onboarded provider that was simply paused does NOT re-run the guard** — it succeeds immediately. The guard runs primarily on first-time activations and after a compliance flag is set by the gateway.

### Toggle cascades to the gateway integration

Beyond setting `active=yes/no` on the local configuration row, the toggle calls the gateway's own internal `updateActive(bool)` hook. For some gateways this triggers an outbound call to the provider's API (e.g., reactivating a paused subscription on the gateway side). For most providers it's a no-op.

The toggle is wrapped in a transaction so partial failures roll back the local `active` flag if the remote call fails. From the merchant's perspective: either both states change together, or neither does — there's no "local says active but gateway says paused" inconsistent intermediate state.

### Activity changes are written to the audit log

Each toggle writes a `SiteEventLog` entry — `TYPE_PAYMENT_ACTIVATED` on enable, `TYPE_PAYMENT_DEACTIVATED` on disable. The entry includes the actor (Administrator or Moderator — see [[merchant-roles]]), the provider, the direction, and the timestamp. So the merchant and CloudCart support can later see who flipped which provider on/off and when. **The audit trail is NOT visible on the Payment methods page** — only in the platform's activity-log view ([[orders-history]] and Settings → activity log).

### Inactive providers are hidden from checkout but NOT from manual orders

An Inactive provider is hidden from the customer at storefront checkout, but is still listed in [[settings-cart]]'s manual-orders Payment-methods multi-select (so the merchant can mark a fulfilment as paid via a paused gateway), and is still returned by [[api-payment-providers]] with `active=false`. "Hidden from checkout" is the only customer-visible effect.

### Active / Inactive vs Uninstall — pick the right path

Use **Deactivate** for temporary suspension (gateway outage, key rotation, scheme change) — all configuration preserved. Use **Uninstall** for permanent removal — destructive, see [[settings-payment-providers-uninstall]]. Both actions require `store.payment_providers` (see [[settings-payment-providers-record-fields]]).

### No cache flush, no queued jobs, no admin emails

Toggling activity does not flush the platform Settings cache, dispatch queued jobs, or fire admin notifications. Page state updates optimistically; downstream effects (checkout visibility, audit log) are immediate.

## Related

- [[settings-payment-providers]] — hub.
- [[settings-payment-providers-list]] — the row this toggle lives on.
- [[settings-payment-providers-uninstall]] — the destructive alternative.
- [[settings-payment-providers-record-fields]] — the `active` field this toggle flips; the `store.payment_providers` permission gate.
- [[settings-payment-providers-filtering]] — plan-feature gating may also block activation post-install.
- [[orders-history]] — site-event-log view where `TYPE_PAYMENT_ACTIVATED` / `TYPE_PAYMENT_DEACTIVATED` entries are visible.
- [[payment-providers-cloudcart-pay-onboarding]] — example of an onboarding flow the activation guard waits on.
- [[payment-providers-dsk-bnpl-promotions]] / [[payment-providers-dsk-zero-schemes]] — example BNPL scheme pages the activation guard waits on.
- [[payment-providers-borica-way4]] — example card processor whose credential ping the guard runs.
- [[settings-staff]] — `store.payment_providers` permission grant.
- [[merchant-roles]] — Administrator vs Moderator roles in the audit-log entry.

## Open questions

_None._
