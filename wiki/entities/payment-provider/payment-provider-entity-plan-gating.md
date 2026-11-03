---
type: entity
nav_path: "Entity → Payment Provider → Plan gating & currency"
aliases: ["Payment Provider plan gates", "authorize_payment feature", "Currency mismatch", "Per-plan provider restrictions", "Cross-currency conversion"]
tags: [entity, payments, payment-providers, plan-gates, currency, multi-currency]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Payment Provider — Plan gating & currency

> Part of [[payment-provider]]. See the hub for related aspects (attributes, credentials + modes, relationships, lifecycle, integration styles, side effects).

## Identity

How the merchant's subscription plan restricts what they can do with Payment Providers, and what happens when a provider's supported currency doesn't match the store's currency. Most providers are NOT plan-gated; the exceptions are documented here. Currency mismatches are NOT validated at save time — they fail at the gateway.

## Aliases

- **`authorize_payment` feature** — the canonical plan-feature gate.
- **Per-plan provider restrictions** — informal phrasing in merchant tickets.
- **Currency mismatch** / **Cross-currency conversion** — the BGN → EUR transition era questions.

## Key Attributes

### Plan-feature gating

Most providers are **NOT plan-gated**. The exceptions:

- **`authorize_payment` feature** — gates the manual-capture / authorize-then-capture mode on providers that support it (Borica Way4, Stripe with capture-later, Klarna pre-auth). The merchant on a plan without it sees the Authorization Mode field but the server rejects the save with *"Your plan does not support authorized payments."*
- **Some advanced providers** are restricted to higher-tier plans via per-provider plan-tier flags.
- **Save Customer Card** is NOT gated — any merchant on any plan can enable it (subject to the provider supporting tokenization).

See [[plan-gates]] for the full gating framework.

### Per-plan provider restrictions are NOT centralized

Per-plan provider restrictions are NOT centralized — each per-provider settings page checks its own plan-feature flag (e.g., `authorize_payment` on Borica Way4 / Stripe / Klarna for capture-later mode). Most providers have no plan gating; the merchant sees install errors only when activating a gated feature. There is no single "plan → allowed providers" matrix the merchant can consult.

### Currency mismatch fails at the gateway, not in admin

The platform does **NOT validate at save time** that a provider supports the store's current currency. If the merchant enables a BGN-only provider on an EUR store, the transaction fails at the gateway, not in the admin UI. The merchant only finds out when a customer's checkout fails.

After the Bulgarian BGN → EUR transition (per [[multi-currency]]), the platform's Convert action rewrites the provider's stored currency code; the gateway side must also be re-configured to accept EUR for end-to-end success. The two updates are NOT automatic — the merchant must do the gateway-portal reconfiguration manually.

### Cross-currency conversion is manual

There is **no automatic Convert path** for non-BGN → EUR (or other cross-currency switches). A Romanian merchant moving RON → EUR must reconfigure each provider's currency settings manually in [[settings-payment-providers]]. The platform does not bulk-update provider credentials when the store's currency changes.

### Operation-country gating in the Add Payment Method modal

The Add Payment Method modal on [[settings-payment-providers]] filters the catalogue by the merchant's **operation country** (set on [[settings-general]]). A merchant in Bulgaria sees the BG bank gateways + BG BNPL providers; a Romanian merchant sees EuPlatesc + MobilPay; a Greek merchant sees Cardlink. Global gateways (Stripe, PayPal, Braintree) appear regardless of country. This is the platform's pre-filtering — not a plan gate.

## Where it appears

- [[settings-payment-providers]] → Add Payment Method modal — country-filtered catalogue of available providers.
- Per-provider settings pages — the Authorization Mode field is hidden or save-rejected when the merchant's plan lacks `authorize_payment` (e.g., on [[payment-providers-borica-way4]], [[payment-providers-stripe]]).
- [[multi-currency]] — currency conversion behaviour during the BGN → EUR migration.
- [[settings-general]] — operation country setting that drives the Add Payment Method modal filter.

## Related

- [[payment-provider]] — hub.
- [[plan-gates]] — the platform's plan-feature framework.
- [[multi-currency]] — currency conversion and BGN → EUR transition.
- [[payment-provider-entity-attributes]] — the Authorization Mode and Currency Support fields gated here.
- [[payment-provider-entity-credentials-modes]] — Save-time validation that does NOT include currency checks.
- [[settings-general]] — operation country source.
- [[payment-providers-borica-way4]] / [[payment-providers-stripe]] — canonical examples of `authorize_payment`-gated providers.

## Open Questions

None.
