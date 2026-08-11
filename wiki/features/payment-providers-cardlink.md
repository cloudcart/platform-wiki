---
type: feature
nav_path: "Payment Providers → Cardlink"
route_name: apps.cardlink.settings
route_path: /admin/payment-providers/cardlink
aliases: ["Cardlink", "Cardlink One", "Alpha Bank Cardlink", "Worldline Cardlink", "Greek card gateway", "Greek card payments"]
tags: [paymentproviders, payment-providers, cardlink, greece, card, 3ds, redirect]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 2
---
# Cardlink

## Purpose

**Cardlink** is the dominant Greek card-acquiring network, operated by Worldline and partnered with Alpha Bank, Eurobank, and Nexi. CloudCart integrates the Cardlink ecommerce hosted-payment page so merchants based in Greece — or selling primarily to Greek customers — can accept Visa / Mastercard / Maestro charges in EUR. The customer is redirected from the storefront checkout to Cardlink's hosted payment page, completes 3D Secure (mandatory under PSD2 / Greek banking rules), and is bounced back to the store after authorisation.

The merchant signs a Cardlink ecommerce contract through their bank, picks a Cardlink-affiliated acquiring gateway (the Bank dropdown — typically Alpha Bank, Nexi/Eurobank, or another partner), and receives a **Merchant ID** and a **Digest Secret**. Those two values plus the chosen gateway and currency are pasted into the settings here.

## Where to find it

Sidebar → **Payment Providers** → click **Cardlink**.

The route is `/admin/payment-providers/cardlink`. The internal provider key is `cardlink`.

## What the merchant can do here

- **Install / Uninstall** the Cardlink payment method.
- **Toggle Active** on / off in the header.
- **Switch between Test and Live mode** — drives whether the integration hits Cardlink's sandbox or production endpoint.
- **Pick the acquiring gateway / bank** — Alpha Bank, Nexi/Eurobank, etc. — drives which Cardlink-affiliated bank URL the integration posts to.
- **Enter Merchant ID (MID)** and **Digest Secret** — both required for any transaction.
- **Pick the settlement currency** — EUR for the standard Greek-market contract.
- **Override the customer-facing label** — logo, title, description on storefront checkout.
- **Set an amount range** (min / max) and an optional **discount** for the method.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** (`configuration.mode`) | Switches between Cardlink test and production endpoints. | `test` | When the field is empty, the integration treats it as Test (test mode = "empty mode"). |
| **Currency** (`configuration.currency`) | Settlement currency — usually EUR for the Greek market. | Empty | Required. Error: "Currency is required." |
| **Merchant ID** (`configuration.mid`) | Merchant identifier issued by Cardlink / acquiring bank. | Empty | Required. Error: "Merchant ID is required." |
| **Digest Secret** (`configuration.secret`) | Shared secret used to sign every request and verify every response. | Empty | Required. Error: "Digest Secret is required." |
| **Bank** (`configuration.gateway`) | Picks the Cardlink-affiliated acquiring gateway (Alpha Bank, Nexi/Eurobank, etc.). | Empty | Required. Error: "Bank is required." |
| **Logo / Title / Description** | Standard storefront-label override. | Provider defaults | |
| **Min / Max amount** | Range filter for the method. | Empty | |
| **Discount** | Discount applied when customer picks Cardlink. | None | |

## Business rules

### Currency auto-conversion to configured currency

Cardlink only acquires in the **configured currency** (set per merchant contract — almost always EUR). When the customer's order is in another currency, the platform converts the payment amount before redirect — both `payment->amount` and `payment->currency` are updated and persisted; the customer sees the converted total on Cardlink's page.

### Customer flow — full redirect

Cardlink is a **hosted redirect** gateway with the standard EMV 3DSv2 challenge built into the bank's page:

1. At checkout the platform builds a Cardlink purchase request (payment amount in minor units, order number as description, return / cancel URLs both pointing at `/payments.return/cardlink`) signed with the merchant's Digest Secret, and the browser is auto-submitted to Cardlink's hosted page (or a test URL in non-live mode).
2. The customer enters card details on Cardlink's page and completes 3D Secure (Strong Customer Authentication mandated in Greece under PSD2).
3. Cardlink returns to `/payments.return/cardlink` with the result and digest.

The return identifies the payment by the `orderid` query parameter (the internal Payment ID set at redirect time). If `orderid` is missing or unknown, the platform returns "Bad Request".

### Status mapping

| Cardlink return signal | CloudCart status |
|------------------------|------------------|
| `isSuccessful=true` (digest verified, success code) | **Completed** |
| `isCancelled=true` | **Canceled** |
| Otherwise | **Failed** |

Note: Cardlink distinguishes "Cancelled" from "Failed" (e.g., customer abandoned vs. card declined). This is one of the few CloudCart payment integrations that maps to Canceled separately from Failed — see [[payment-status]] for the full status taxonomy.

### Billing data forwarded

The platform sends a structured `card` block with the customer's email and ISO country code. When the order has a billing address, the platform adds: `billingCity`, `billingPostcode`, `billingAddress1`, `billingPhone`. This enables Cardlink's risk-scoring and AVS checks.

### What the persisted log strips

After the return, the platform stores Cardlink's response in `provider_data` after stripping the `digest` field (since it's a sensitive verification artefact). The response message is also pinned as a top-level `message` key for quick reference.

### Refunds & sync

The Cardlink integration does **not** implement refund, sync, or capture flows — the only end-to-end method wired up is `purchase`. Calling any other action on the integration raises a "Method not supported by the gateway" error. Refunds for Cardlink payments are processed from the acquiring bank's merchant back-office portal, and the merchant marks the order's payment as Refunded in CloudCart manually.

### 3D Secure enforcement

3DSv2 / Strong Customer Authentication is enforced on Cardlink's page — the customer cannot bypass the challenge. CloudCart doesn't need to set 3DS flags itself; the bank's Cardlink instance handles it. The integration ships with Cardlink's 3DSv2 redirection technical reference for engineering use.

### Bank dropdown drives the endpoint

The `Bank` (`configuration.gateway`) setting selects which Cardlink-affiliated acquiring gateway the request is signed for. The dropdown has exactly three hardcoded options: **Nexi / Alpha Bank** (`nexi`), **Cardlink** (`cardlink`), and **Worldline** (`worldline`). Each partner has its own endpoint and digest expectations — picking the wrong bank causes a digest-mismatch rejection even when the MID + Digest Secret are correct. The merchant must pick the bank whose name is on their Cardlink contract; the live vs test endpoint is then chosen by the test-mode flag. (Compare with [[payment-providers-nestpay|NestPay]], where the same pattern exists for Turkish banks.)

### Installments

Cardlink supports installments for Greek cards, but these are negotiated outside CloudCart on the bank-portal side. CloudCart sends a single-purchase request; installment terms (if any) are arranged by the customer on Cardlink's hosted page or by the merchant in the bank back-office. There is no separate provider variant in CloudCart for installments.

### Plan-tier gating

None — Cardlink has no `plan_gates` declaration.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where Cardlink is installed / uninstalled.
- [[orders-payment-refund]] — generic refund button (Cardlink defers to bank back-office).
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Canceled / Failed mapping (Cardlink is one of the few integrations using Canceled).
- [[checkout-flow]] — concept page on the storefront checkout.
- [[multi-currency]] — context for the EUR auto-conversion behaviour.
- [[payment-providers-nestpay]] — same bank-dropdown pattern, Turkish equivalent.

## Open questions

(none)
