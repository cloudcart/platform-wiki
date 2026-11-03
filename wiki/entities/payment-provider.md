---
type: entity
nav_path: "Entity → Payment Provider"
aliases: ["Payment Provider", "Payment gateway", "Payment method provider", "Payment integration", "Gateway", "PSP", "Платежен доставчик", "Платежен метод", "Платежен шлюз"]
tags: [entity, payments, payment-providers, integrations, settings]
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---

# Payment Provider

## Identity

A **Payment Provider** is a configured third-party payment gateway integration on the merchant's store — Stripe, iCard, Borica Way4, Mokka, MyPos, Paynetics, DSK Bank, CloudCart Pay, PayPal, Cash on Delivery, bank transfer, and 60+ more. Each provider, once installed and activated in [[settings-payment-providers]], appears at the storefront checkout as a payment-method option the customer can pick. CloudCart ships 72+ provider integrations covering Bulgarian bank gateways, BNPL (buy-now-pay-later) lenders, global card networks (Stripe, PayPal, Braintree, Authorize.Net), country-specific gateways (Cardlink GR, EuPlatesc / MobilPay RO, CIB Bank HU, NestPay TR), and offline / manual methods (COD, bank transfer, voucher).

A Payment Provider is the **configuration record** — one row per installed gateway per store — that carries the merchant's credentials, mode (live / test), activation state, customer-facing label, country / amount scoping, and per-provider operational flags. It is distinct from a [[payment-status]] (the *state* of the money on a specific order) and from a single payment record (one charge attempt against an order). The provider configuration is what the merchant edits in admin; the payment records and status enum are what get written each time a customer pays. See [[payment-provider-mechanism]] for the shared lifecycle every provider follows.

## Aliases

- **Payment Provider** — the canonical term in the admin UI and across the wiki.
- **Payment gateway** / **Gateway** — used interchangeably; the customer-facing word is often "payment method".
- **Payment method provider** — full phrase used in some legal / contract surfaces.
- **PSP** (Payment Service Provider) — industry term occasionally used in BNPL / bank documentation.
- **Платежен доставчик** / **Платежен метод** / **Платежен шлюз** — Bulgarian equivalents.

## Key Attributes

The Payment Provider entity is documented across seven aspect pages. The high-level shape is:

- **Identification** — provider code (`name`, e.g. `stripe`, `icard`, `borica_way4`, `mokka`, `cod`), storefront name, logo, description.
- **Mode + activation** — `live` / `test` toggle, Active yes / no, per-mode credential set.
- **Credentials** — per-provider field set; each field exists in two variants (`<name>` live, `test_<name>` test) and is stored AES-encrypted at rest.
- **Scoping** — `min_price` / `max_price`, allowed countries, currency support, sort order, allowed shipping methods, category restrictions, customer-group restrictions.
- **Customer incentives** — optional Discount (flat / percent / free-shipping) and Surcharge / fee (flat / percent) attached to picking this provider.
- **Operational flags** — Save Customer Card (per-mode), Authorization Mode (`auto-capture` / `authorize-then-capture`), 3DS enforcement, webhook callback URL.

See [[payment-provider-entity-attributes]] for the verbatim field catalogue with notes per provider family. See [[payment-provider-entity-credentials-modes]] for the live + test co-existence rule and the encryption-at-rest guarantee.

## Sub-pages (in this cluster)

This entity is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[payment-provider-entity-attributes]] — verbatim attribute catalogue (provider code, storefront name, logo, mode, active, scoping, discount / surcharge, auth mode, 3DS, webhook callback URL).
- [[payment-provider-entity-credentials-modes]] — live + test credentials co-existing on one row, the Mode toggle, save-time gateway validation, AES encryption at rest.
- [[payment-provider-entity-relationships]] — relationships to [[order]], [[cart]], [[payment-status]], [[shipping-provider]], [[category]], [[customer-group]], [[geo-zone]].
- [[payment-provider-entity-lifecycle]] — the seven merchant-controlled states (Available, Installed, Configured, Active, Suspended, Auto-deactivated, Uninstalled) + save-time transitions.
- [[payment-provider-entity-integration-styles]] — the three integration patterns (redirect, embedded SDK, API-only / manual) and the PCI-scope-out implication (card data never reaches CloudCart).
- [[payment-provider-entity-plan-gating]] — the `authorize_payment` plan-feature, per-provider plan restrictions, currency mismatch failing at the gateway not in admin.
- [[payment-provider-entity-side-effects]] — what fires when the merchant clicks Save: app-catalog upsert, provider cache invalidation, audit-log entries on install / uninstall, the auto-deactivation safety net.

## Where it appears

- [[settings-payment-providers]] — the central hub: every installed provider as a row, plus the Add Payment Method modal listing every available provider for the merchant's country / plan.
- [[payment-providers]] — the navigation hub listing every per-provider page.
- Per-provider settings pages — one page per gateway (72+ in total):
  - **Bulgarian bank gateways**: [[payment-providers-borica-way4]], [[payment-providers-icard]], [[payment-providers-dsk-bank]], [[payment-providers-cib-bank]].
  - **Bulgarian BNPL**: [[payment-providers-mokka]], [[payment-providers-dsk-bnpl]], [[payment-providers-fibank-bnpl]], [[payment-providers-iute]], [[payment-providers-klear]], [[payment-providers-tbi-bank]], [[payment-providers-fusion-pay]], [[payment-providers-plati-posle]].
  - **CloudCart's own gateway**: [[payment-providers-cloudcart-pay]] + onboarding / settings / payouts / transactions sub-pages.
  - **Global card gateways**: [[payment-providers-stripe]], [[payment-providers-paypal]], [[payment-providers-braintree]], [[payment-providers-authorize]], [[payment-providers-mollie]].
  - **Regional**: [[payment-providers-euplatesc]], [[payment-providers-mobilpay]], [[payment-providers-monri]], [[payment-providers-cardlink]], [[payment-providers-payu]], [[payment-providers-paysera]], [[payment-providers-everypay]].
  - **Offline**: [[payment-providers-cod]].
- [[orders-details]] — per-order edit hub; the payment row shows the current [[payment-status]] and exposes provider-specific actions (Refund, Capture, Sync, Mark Paid).
- [[orders-payment-mark-paid]] / [[orders-payment-capture]] / [[orders-payment-refund]] / [[orders-payment-manual]] — order-side payment actions.
- [[checkout-flow]] — where the customer picks one of the active providers.
- [[settings-statuses]] → Payment tab — merchant can rename payment-status labels (underlying enum unchanged).

## Related

### Related entities

- [[payment-status]] — the canonical enum every provider's response codes map into.
- [[order]] — every Order has a payment record associated with one Payment Provider.
- [[cart]] — the customer's in-progress checkout, carrying the picked provider before order creation.
- [[shipping-provider]] — sister entity; both are third-party integrations gated at checkout. A shipping method also carries an allowed-payments list that filters providers.
- [[category]] — categories can restrict which providers are offered for orders containing products in that category.
- [[customer-group]] — groups can restrict the available providers per loyalty tier.
- [[geo-zone]] — providers are scoped by allowed countries.

### Cross-cutting concepts

- [[payment-provider-mechanism]] — the shared lifecycle every provider follows (configure → activate → take customer through → confirm → refund / capture / sync).
- [[payment-provider-checkout-visibility]] — the filter chain that decides whether a provider appears at checkout.
- [[payment-provider-confirmation]] — webhook vs Sync confirmation styles.
- [[payment-provider-refunds]] — the three refund styles per provider.
- [[payment-provider-tokenization-3ds]] — saved cards + 3DS enforcement rules.
- [[checkout-flow]] — the cart-to-order transition where the provider is selected and the payment is initiated.
- [[multi-currency]] — currency conversion and the BGN → EUR transition that rewrites provider currency codes.
- [[plan-gates]] — the `authorize_payment` feature gate.
- [[notification-delivery]] — admin alerts fire when a provider self-deactivates on persistent credential failures.
- [[shipping-provider-mechanism]] — sister concept for shipping integrations.

### Settings & webhooks

- [[settings-payment-providers]] — the central provider hub.
- [[settings-statuses]] — the Payment tab lets the merchant rename payment-status labels (underlying enum unchanged).
- [[settings-hooks]] — payment-status changes trigger `order.updated` webhooks; some providers also fire their own internal events.

## Open Questions

No outstanding questions — all items resolved or removed.
