---
type: concept
nav_path: "Concept → Payment provider mechanism → Checkout visibility"
aliases: ["Payment provider checkout visibility", "Payment provider filtering", "min_price max_price gating", "Currency support per provider", "authorize_payment plan gate", "Why payment provider missing at checkout", "Защо доставчикът не се показва на чекаута"]
tags: [payments, payment-providers, checkout, plan-gates, currency, concepts]
plan_gates: [authorize_payment]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-provider-mechanism]]. See the hub for the other aspects (configuration, integration patterns, tokenization & 3DS, refunds, confirmation).

# Payment provider — checkout visibility

## Definition

A payment provider being **Active** in [[settings-payment-providers]] is necessary but not sufficient for it to appear at checkout. Whether the customer actually SEES the provider as a payment-method row depends on a stack of filters: cart subtotal vs `min_price` / `max_price`, currency match, country allowlist, the selected shipping method's allowed-payments list, plan-feature gating (`authorize_payment` for manual-capture mode), and a few per-provider runtime checks. This aspect documents the full visibility chain — the canonical "why isn't my payment provider showing at checkout?" support topic.

## Scope

Covered:

- The full filter stack from "Active" to "customer sees the row".
- What the customer's payment-method row looks like (logo, storefront name, description, optional fee / discount).
- `min_price` / `max_price` gating.
- Currency support per provider class (BG bank gateways BGN-only, multi-currency globals, country-specific gateways, BNPL domestic-only).
- Plan-feature gating — the `authorize_payment` flag plus higher-tier-only providers.
- The BGN → EUR Convert action's effect on provider currency codes.

Not covered here:

- The credential / activation setup that makes the provider Active in the first place — see [[payment-provider-configuration]].
- The customer's experience AFTER they click the row (redirect / embedded / manual) — see [[payment-provider-integration-patterns]].
- The shipping side of the allowed-payments link — see [[shipping-provider-mechanism]].

## Contrasts

- **Provider-level activation vs provider-method visibility at checkout** — the Active toggle on [[settings-payment-providers]] turns the WHOLE provider on/off. Whether it APPEARS at checkout also depends on `min_price` / `max_price`, country availability, currency match, and the selected shipping method's allowed-payments list.
- **Inactive vs filtered out** — inactive providers are excluded entirely (the customer just doesn't see them, no greyed-out option). Filtered-out providers are also invisible to the customer but for a different reason — cart doesn't match the filter criteria. Both look the same to the customer; the merchant tells them apart in admin.
- **`authorize_payment` plan gate vs provider plan-gating** — `authorize_payment` is a feature gate on **the manual-capture flow** (a single mode on supported providers). Separately, **some providers themselves** (advanced BNPL) are restricted to higher plans.
- **Storefront currency match vs gateway-side currency configuration** — CloudCart does NOT validate at save time that the provider supports the store's currency. Misconfiguration fails at the gateway (live transaction), not in admin.

## Where it applies

### The full visibility filter stack

The customer sees a provider at checkout only if ALL of the following pass:

1. **Active = yes** in [[settings-payment-providers]].
2. **Cart subtotal within `min_price` / `max_price`** range configured per-provider.
3. **Currency match** — the cart's currency is in the provider's supported set.
4. **Country allowed** — the customer's billing/shipping country is on the provider's allowed-countries list.
5. **Selected shipping method allows this payment** — the shipping method has an allowed-payments list; this provider must be on it.
6. **Plan-gating passes** — for plan-gated providers / modes (see below).
7. **Runtime credential check passes** — strict-validation providers (Stripe) may self-deactivate at runtime if credentials are invalid; see [[payment-provider-configuration]].

### Customer's view at checkout

The customer sees the payment method as a row in the checkout's payment-method picker:

- **Logo** — the provider's logo (or the merchant's override).
- **Storefront name** — the merchant-configured label (`storefront_name`, e.g., "Pay with card" instead of internal `borica_way4`).
- **Description** — short text explaining the method.
- **Optional fee / discount** — if the merchant configured a discount or surcharge for this provider.

Inactive providers are excluded entirely — no greyed-out option, the customer just doesn't see them. See [[checkout-flow]] for the full payment-method picker UX.

### Currency support per provider class

| Provider class | Currency scope |
|---------------|----------------|
| **Bulgarian bank gateways** (Borica Way4, iCard, ePay) | Typically BGN or EUR (each terminal at the bank is provisioned for one currency at a time). |
| **Global card gateways** (Stripe, PayPal, Braintree, Authorize.Net) | 100+ currencies — the merchant's gateway account determines which subset is enabled. |
| **Country-specific bank gateways** (Cardlink GR, CIB Bank HU, EuPlatesc / MobilPay RO, NestPay TR) | One or two currencies, matching the country. |
| **BNPL providers** | Domestic-currency-only (Mokka BG = BGN; Mokka RO = RON; Mokka GR = EUR; Klarna by country; Iute by country). |

The platform does NOT validate that a provider supports the store's current currency at save time. If the merchant misconfigures (e.g., enables a BGN-only provider on an EUR store), the transaction fails at the gateway, not in the admin UI.

After the Bulgarian BGN → EUR transition (per [[multi-currency]]), the Convert action also rewrites the provider's configured currency code from BGN to EUR — but the **gateway side must also be configured to accept EUR** for the end-to-end flow to work.

### Plan-feature gating

Most providers themselves are NOT plan-gated — any merchant on any plan can install and activate them. The exceptions:

- **`authorize_payment` feature** ([[plan-gates]]) — gates the Manual capture / Authorize+Capture flow on providers that support it (Borica Way4, Stripe with capture-later, Klarna pre-auth). The merchant on a plan without this feature sees the Authorization Mode field but the server rejects the save with the literal error *"Your plan does not support authorized payments."*
- **Some advanced providers** are restricted to higher-tier plans via per-provider plan-tier flags (see each provider's page).
- **Save Customer Card** is **not** gated — any merchant can enable it on providers that support tokenization (see [[payment-provider-tokenization-3ds]]).

## Related

- [[payment-provider-mechanism]] — hub.
- [[payment-provider-configuration]] — what makes a provider Active in the first place.
- [[payment-provider-integration-patterns]] — what the customer experiences after they click the row.
- [[checkout-flow]] — the cart-to-order transition where the payment-method picker renders.
- [[settings-payment-providers]] — the Active toggle + `min_price` / `max_price` + allowed countries + storefront name + logo.
- [[shipping-provider-mechanism]] — the shipping method's allowed-payments list filters this list further.
- [[plan-gates]] — `authorize_payment` and per-provider plan-tier flags.
- [[multi-currency]] — BGN → EUR Convert action's effect on configured currency codes.
- [[payment-status]] — orthogonal — the status enum is unaffected by visibility filters.

## Open Questions

- ⏸️ Full per-provider list of which providers are plan-gated (verify) — confirmed `authorize_payment` mode gate; specific advanced-BNPL plan tiers documented on individual provider pages.
