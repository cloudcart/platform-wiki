---
type: concept
nav_path: "Concept → Multi-currency → Payment providers"
aliases: ["Currency-specific payment providers", "BGN-only providers", "Multi-currency providers", "Provider currency mismatch", "Provider currency code Convert", "Платежни доставчици и валута"]
tags: [finance, currency, payment-providers, gateways, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[multi-currency]]. See the hub for the other aspects (store currency model, price storage, order snapshot, FX rates, BGN → EUR transition, taxes & analytics).

# Multi-currency — payment providers

## Definition

Most payment providers are **currency-specific by design** — they only support certain processing currencies, determined by the merchant's contract on the provider's side. CloudCart configures each provider in [[settings-payment-providers]] with a per-provider currency code, but the platform **does NOT validate** that the provider supports the store's current currency before saving. A misconfigured provider (e.g., a BGN-only provider enabled on an EUR store) saves cleanly, then fails at the gateway when a customer tries to pay — not in the admin panel.

The BGN → EUR Convert action on [[apps-bgn2eur]] sweeps the **per-provider configured currency code** alongside the per-provider fee amount, flipping BGN to EUR for every provider whose admin-configured currency was BGN. For this to work end-to-end, the provider's merchant account must have ALSO been enabled for EUR on the provider's side — CloudCart cannot upgrade the provider account.

## Scope

Covered:

- Currency support patterns: BGN-only domestic providers, multi-currency international providers, country-specific banks.
- The per-provider configured currency code in CloudCart's admin.
- The absence of admin-side validation on the provider × store-currency pairing.
- How the BGN → EUR Convert action flips the per-provider configured currency code.
- Per-provider refund-currency constraints.

Not covered here:

- The order's frozen currency at creation — see [[multi-currency-order-snapshot]].
- The full Convert action field catalogue — see [[multi-currency-bgn-eur-transition]].
- FX rates for shipping-courier APIs (different pipeline) — see [[multi-currency-fx-rates]].
- Per-provider integration mechanics (auth, callbacks, webhook events) — see each provider's own page.

## Contrasts

- **BGN-only providers vs. multi-currency providers** — domestic Bulgarian providers (iCard, ePay, Borica, Paynetics, Wallet) historically configure BGN only. International providers (PayPal, Stripe, Adyen, Braintree) support many currencies but are constrained by the merchant's own account configuration on their side.
- **Provider's processing currency vs. store currency** — the platform stores the order in the store currency; the provider may settle in the same currency or in a related currency. The provider's settled currency is its own concern; CloudCart records the order's nominal currency.
- **Platform validation (absent) vs. gateway validation (present)** — CloudCart will save any provider × any currency combination. The provider's gateway rejects the request at runtime if the pairing is unsupported. There is no in-admin warning.
- **Per-provider configured currency code (Convert touches) vs. provider's underlying merchant account (Convert does NOT touch)** — Convert flips the BGN tag on the provider's CloudCart configuration; the provider's underlying merchant-account currency must be upgraded separately on the provider's side.

## Where it applies

### Currency support patterns

**Bulgarian domestic providers (typically BGN-only)**:

- iCard, ePay, Borica, Paynetics, Wallet.
- Historically configured with BGN as the sole processing currency.
- During the 2026 BGN → EUR transition, providers in this group have been adding EUR support on the provider side; merchants should confirm with each provider before relying on the post-Convert EUR flip.

**Multi-currency international providers**:

- PayPal, Stripe, Adyen, Braintree.
- Support many currencies, but the merchant's account configuration on the provider's side determines which currencies they can actually accept.
- A store can switch currency and continue using these providers IF the merchant's provider account is enabled for the new currency.

**Country-specific banks**:

- CIB Bank, BNP Paribas, Authorize.Net, EveryPay, DSK Bank, FiBank, MyPos, etc.
- Supported currencies match the country and the bank's product line.
- Cross-currency processing through these typically not supported.

### The per-provider configured currency code

In [[settings-payment-providers]], each enabled provider has a configured currency code on its provider-specific settings panel. This code is what the platform sends to the provider's API when a charge / refund / void is initiated. It is separate from the store-wide `currency` setting.

In practice, the per-provider currency code SHOULD match the store currency, but CloudCart does not enforce this. A merchant can:

- Set the store currency to EUR.
- Configure a provider with currency code BGN.
- Save without warning.
- Customer attempts to pay, gateway returns a "currency not supported" error.

The error surfaces only at the gateway; the admin panel gives no clue. Support tickets about "checkout fails for one payment method only after currency change" almost always trace back to a provider whose configured currency was not updated.

### The BGN → EUR Convert flips the provider currency code

The Convert action on [[apps-bgn2eur]] explicitly sweeps the per-provider configured currency code alongside the provider fee:

- Every provider configured with currency code `BGN` is flipped to `EUR`.
- The per-provider fee amount (if numeric) is divided by 1.95583.
- The provider's underlying merchant account must have been enabled for EUR on the provider's side — CloudCart cannot upgrade the provider account. If the merchant account is still BGN-only on the provider side, payment requests will fail at the gateway after Convert.

### Provider-side refund currency constraints

CloudCart does not support cross-currency refunds — see [[multi-currency-order-snapshot]]. Each provider further gates refunds:

- **Stripe** — refunds must be in the original capture currency.
- **Borica** — refunds in the original capture currency only.
- **Adyen** — same default; multi-currency-capable merchant accounts may differ.
- **iCard / ePay / Paynetics / Wallet / Borica** — refunds in original capture currency.
- **PayPal** — broader support, but each PayPal merchant account configuration determines what works.

For a Bulgarian store running Convert mid-life, a refund on a pre-Convert BGN order must be processed in BGN — which means the provider's merchant account on the provider side must continue to support BGN refunds for at least the cooling-off / chargeback window. Confirm with the provider before fully migrating to EUR-only.

### Practical support pattern

When a Bulgarian merchant reports "checkout works for one payment method but fails for another after switching to EUR", the diagnostic order is:

1. Check the per-provider configured currency code in [[settings-payment-providers]] — should be EUR if the store is on EUR.
2. Confirm with the provider that the merchant account on their side has been enabled for EUR.
3. Confirm the provider hasn't introduced new IBAN / settlement requirements for the EUR account.
4. Test a small EUR transaction end-to-end before rolling back.

For non-Bulgarian merchants changing currency, all of the above applies but without the Convert action's automated sweep — the merchant must manually update the per-provider currency code on each provider in [[settings-payment-providers]].

## Related

- [[multi-currency]] — hub.
- [[multi-currency-order-snapshot]] — refund currency rules at the order level.
- [[multi-currency-bgn-eur-transition]] — Convert action including provider currency code sweep.
- [[settings-payment-providers]] — per-provider configuration screen.
- [[orders-payment-refund]] — refund flow surfacing the order's frozen currency.

## Open Questions

- ⏸️ Confirm the exhaustive list of providers whose configured currency code is swept by the Convert action vs. providers that are skipped (if any). (verify)
