---
type: concept
nav_path: "Concept → Payment provider mechanism → Tokenization & 3DS"
aliases: ["Card tokenization", "Saved cards", "Save Customer Card", "PCI-DSS scope", "3DS enforcement", "3-D Secure", "Card vault", "Запомняне на карта", "Тригер D-Secure"]
tags: [payments, payment-providers, security, 3ds, tokenization, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-provider-mechanism]]. See the hub for the other aspects (configuration, integration patterns, refunds, confirmation, checkout visibility).

# Payment provider — tokenization & 3DS

## Definition

Across all three integration patterns ([[payment-provider-integration-patterns]]), the constant is: **CloudCart never stores raw card numbers, expiry dates, or CVV codes**. The gateway-side vault holds the card; CloudCart stores only a token plus masked display metadata. **3-D Secure (3DS)** is the issuer-side authentication step layered on top — enforced at the card-network + provider level (not by CloudCart). This aspect covers both: what CloudCart keeps in its database for saved cards, and how 3DS challenges are routed.

## Scope

Covered:

- What CloudCart stores per saved card (token + masked metadata) and what it never stores (PAN, CVV, expiry).
- The "Save Customer Card" feature — guest vs signed-in handling.
- Removing a saved card from the storefront account panel.
- 3DS enforcement matrix: mandatory bank gateways vs issuer-driven globals vs N/A (offline + BNPL).
- 3DS metadata the platform sends with every card request.

Not covered here:

- The credential / activation setup that enables Save Customer Card per provider — see [[payment-provider-configuration]].
- The webhook / sync confirmation that completes a tokenized re-charge — see [[payment-provider-confirmation]].
- BNPL underwriting (a separate flow from 3DS, with its own ID + employment checks).

## Contrasts

- **PAN (raw card number) vs token** — CloudCart never sees the PAN; it holds only the gateway's token, which is meaningless outside that gateway's vault. Tokens are NOT portable across gateways.
- **Signed-in customer vs guest** — saved-card flow requires a logged-in account to attach the token to. **Guests cannot use saved-card flow** — they enter card details every time.
- **3DS mandatory vs 3DS issuer-driven** — on Bulgarian bank gateways (Borica Way4, iCard), 3DS 2.x is enforced on every Visa / Mastercard / Maestro / JCB transaction; the merchant cannot disable it. On global multi-currency gateways (Stripe, PayPal), the customer's bank decides whether to challenge or allow frictionless.
- **3DS vs BNPL underwriting** — BNPL providers run their own credit / employment / ID check flow instead of card 3DS; there's no 3DS challenge in a BNPL purchase.

## Where it applies

### What CloudCart stores

When the merchant enables "Save Customer Card" on supported providers (Stripe, Borica Way4, CloudCart Pay, and others) AND the customer is signed in, the gateway returns a token on first purchase. The platform stores against the customer's record:

- A **token** (the gateway's reference to the saved card, e.g., Stripe `pm_...`, Borica `MERCH_TOKEN_ID`, CloudCart Pay vault token).
- **Masked metadata** for display — card brand (Visa / Mastercard / Maestro / Amex / Diners / JCB), last 4 digits, expiry month/year, issuing country.

On subsequent purchases, the platform sends the token to the gateway and the gateway charges the saved card without re-prompting for card details. The customer can remove a saved card from the storefront's account panel.

For **guests**, saved-card flow is disabled — the customer enters card details every time because there's no logged-in account to attach the token to.

### 3DS enforcement matrix

3-D Secure (the issuer-side authentication step where the customer enters a one-time code from their bank's app) is enforced at the card-network and provider level. The merchant's experience:

| Provider class | 3DS behaviour |
|----------------|---------------|
| **Bulgarian bank gateways** (Borica Way4, iCard) | **Mandatory** on every Visa / Mastercard / Maestro / JCB transaction. 3DS 2.x. Merchant cannot disable. |
| **Multi-currency global gateways** (Stripe, PayPal) | **Issuer-driven** — the customer's bank decides whether to challenge or allow frictionless. Stripe handles the challenge UX transparently. |
| **Offline / manual** (COD, bank transfer, voucher) | **Not applicable** — no card interaction. |
| **BNPL providers** (Mokka, Klarna, Iute, DSK BNPL, FiBank BNPL, etc.) | **Not applicable** to 3DS — BNPL has its own underwriting flow (ID + employment checks). |

### 3DS metadata sent on every card request

The platform sends 3DS metadata on every card request to support frictionless challenges where the issuer chooses:

- Cardholder name.
- Billing address + shipping address.
- ASCII-only, character-limited per the 3DS 2.x protocol.

If the issuer challenges, the customer completes the challenge on the gateway's hosted page (Pattern 1) or via SDK-driven UI (Pattern 2). On success the gateway returns the result and the platform proceeds with the regular [[payment-provider-confirmation|webhook / sync flow]].

## Related

- [[payment-provider-mechanism]] — hub.
- [[payment-provider-configuration]] — where the merchant enables Save Customer Card per provider.
- [[payment-provider-integration-patterns]] — the three patterns that all use the same tokenization model.
- [[payment-provider-confirmation]] — what happens after a 3DS challenge succeeds / fails.
- [[customer]] — the entity that owns the saved-card tokens; guests have no record to attach to.
- [[payment-providers-stripe]] / [[payment-providers-borica-way4]] / [[payment-providers-cloudcart-pay]] — major Save-Customer-Card providers.

## Open Questions

- ⏸️ Full list of providers that support Save Customer Card (verify) — confirmed for Stripe, Borica Way4, CloudCart Pay; other providers' tokenization availability documented on individual provider pages.
