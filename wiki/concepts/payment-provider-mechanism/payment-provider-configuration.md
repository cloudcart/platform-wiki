---
type: concept
nav_path: "Concept → Payment provider mechanism → Configuration & activation"
aliases: ["Payment provider configuration", "Payment provider credentials", "Live and test credentials", "Payment provider activation flow", "Payment provider self-deactivation", "Конфигуриране на платежен доставчик"]
tags: [payments, payment-providers, configuration, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-provider-mechanism]]. See the hub for the other aspects (integration patterns, tokenization & 3DS, refunds, confirmation, checkout visibility).

# Payment provider — configuration & activation

## Definition

The **configuration & activation** aspect covers how a merchant installs a payment gateway in CloudCart, supplies credentials, validates them, and switches the provider Active so it appears at checkout. Every one of CloudCart's 72+ providers — Stripe, Borica Way4, iCard, Mokka, CloudCart Pay, COD, etc. — follows the same configuration shape: a small set of provider-specific fields, each duplicated for **live** and **test** mode, with a single Mode toggle to switch between them.

## Scope

Covered:

- The two-variant credential model (live + test) and `<field>` / `test_<field>` naming convention.
- The standard 6-step activation flow (install → configure → save → activate → method options → appears at checkout).
- Save-time validation against the gateway.
- Toggle-OFF vs uninstall (preserve vs destroy configuration).
- Self-deactivation when credentials become invalid at runtime.

Not covered here:

- How the customer's payment interaction is routed — see [[payment-provider-integration-patterns]].
- Where the provider then shows / doesn't show at checkout — see [[payment-provider-checkout-visibility]].
- Token storage of saved cards — see [[payment-provider-tokenization-3ds]].

## Contrasts

- **Live mode vs test mode** — the same provider record carries BOTH credential sets simultaneously; switching the Mode toggle re-routes every transaction to the corresponding gateway environment. The merchant never needs to clear keys to switch.
- **Toggle-OFF (Active = no) vs uninstall** — toggling Active off hides the provider from checkout but preserves credentials; the standard path for temporary suspension (gateway outage, key rotation). **Uninstall is destructive** — it deletes the configuration row, credentials, and schemes; the merchant must re-onboard from scratch.
- **Save-time credential validation vs runtime credential failure** — most providers validate on save by calling the gateway's API; bad keys are rejected inline. But a provider that was valid at save time can become invalid later (rotated at the gateway without an in-CloudCart update) — handled by runtime self-deactivation, not save validation.

## Where it applies

### Configuration screens

- [[settings-payment-providers]] — the merchant's central hub. The Add Payment Method modal lists every uninstalled provider available for the operation country + plan.
- Per-provider settings pages (one per gateway), typically titled "*Provider Name*". Examples: [[payment-providers-borica-way4]], [[payment-providers-icard]], [[payment-providers-stripe]], [[payment-providers-cloudcart-pay]], [[payment-providers-mokka]].

### The credential model

Field names use the pattern `<credential_name>` (live) and `test_<credential_name>` (test):

| Common provider-specific field | Examples |
|--------------------------------|----------|
| **Merchant / Store ID** | `merchant_id` / `test_merchant_id` (iCard), `store_id` / `store_test_id` (Mokka) |
| **API Secret / Private Key** | `secret_key` / `test_secret_key` (Stripe), `private_key` / `test_private_key` (iCard) |
| **Public Key / Certificate** | `publishable_key` / `test_publishable_key` (Stripe), `api_public_key` / `test_api_public_key` (iCard) |
| **Endpoint URL** | `store_endpoint` / `store_test_endpoint` (Mokka — country-specific URL) |
| **Terminal ID** | Specific to bank gateways (Borica Way4, e.g., `V1900145`) |
| **Key Index** | For providers supporting key rotation (iCard `key_index` / `key_index_resp`) |

The simplest providers (Mokka) need 3 fields × 2 modes = 6 inputs. The credential-heaviest providers (Borica Way4, iCard) need 6+ fields × 2 modes plus uploaded certificates. CloudCart Pay needs the fewest because the merchant onboards via a separate onboarding flow ([[payment-providers-cloudcart-pay-onboarding]]).

### The activation flow

The standard activation sequence is:

1. **Install** the provider from the Add Payment Method modal in [[settings-payment-providers]].
2. **Configure credentials** — paste the live + test credentials provided by the gateway during onboarding.
3. **Save** — the platform usually validates by calling the gateway's API with the credentials (Stripe verifies via `accounts.retrieve`, Borica Way4 verifies the certificate matches the private key, etc.). If the credentials are bad, the save is rejected with a provider-specific error inline on the relevant field.
4. **Activate** — toggle the Status switch to Active. For some providers (e.g., Borica Way4), activation is blocked in live mode until the live certificate is uploaded.
5. **Configure common payment-method options** — `storefront_name` (customer-facing label, may differ from internal `name`), logo override, `min_price` / `max_price` (per-provider order-amount range), optional discount when paying with this provider, sort order, allowed countries.
6. **The provider now appears at checkout** for matching carts — see [[payment-provider-checkout-visibility]] for the full filter chain.

### Self-deactivation on persistently invalid credentials

For providers with strict credential validation (Stripe is the canonical example), if the platform catches a credential-rejection error when initializing the gateway client mid-transaction, it:

1. Logs an admin notification.
2. Dispatches an alert to the bell-icon notification feed — see [[notification-delivery]].
3. **Automatically flips the provider's Active flag to OFF.**

The merchant must fix the keys and re-enable. This prevents customers from continuously hitting checkout errors when the merchant's keys have been rotated at the gateway without an in-CloudCart update. (verify) for non-Stripe providers — exact behaviour varies per integration.

## Related

- [[payment-provider-mechanism]] — hub.
- [[settings-payment-providers]] — the merchant's payment-methods hub.
- [[payment-provider]] — the entity carrying per-provider configuration rows.
- [[payment-providers]] — the navigation hub listing every provider page.
- [[notification-delivery]] — admin alerts fire on self-deactivation.
- [[plan-gates]] — operation-country + plan-tier gating of which providers appear in the Add Payment Method modal.

## Open Questions

- ⏸️ Exact list of providers that auto-deactivate on runtime credential failure (verify) — confirmed for Stripe; other strict-validation providers likely behave similarly but each integration's runtime handler may differ.
