---
type: feature
nav_path: "Payment Providers → Borica Way4 → Save card & Wallets"
route_name: apps.borica_way4.overview
route_path: /admin/payment-providers/borica_way4
aliases: ["Borica Save customer card", "Borica MERCH_TOKEN_ID", "Borica tokenisation", "Borica MERCH_TRAN_STATE", "Borica Google Pay", "Borica Apple Pay", "Borica MPay", "MPay BG", "Pay with token"]
tags: [paymentproviders, payment-providers, borica-way4, save-card, tokenisation, google-pay, apple-pay, mpay]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-borica-way4]]. See the hub for related aspects (setup/CSR, settings, payment lifecycle, authorize/capture, refund/sync).

# Borica Way4 — Save card & Wallets (Google Pay / Apple Pay)

## Purpose

This aspect documents the two opt-in "card-experience" features the merchant can layer on top of plain Borica Way4 card payments:

1. **Save Customer Card** — Borica's `MERCH_TOKEN_ID` tokenisation. Signed-in customers see saved cards on subsequent checkouts and pay with one click (no Borica page redirect).
2. **Google Pay / Apple Pay** — the **MPay** wallet flow. Adds Google Pay / Apple Pay buttons next to the regular Pay-with-card button on storefront checkout; clicking one opens Borica's hosted page directly into the chosen wallet.

Both features are independent toggles on the same settings page and both must also be enabled by Borica on the terminal side — CloudCart cannot turn them on unilaterally.

## Where to find it

- **Save Customer Card** switch — Payment Providers → Borica Way4, the second of the four settings cards (`Save customer card settings`).
- **Enable Google Pay / Apple Pay** switch — Payment Providers → Borica Way4, the third card (`Google Pay / Apple Pay settings`).
- Both toggles are documented as fields in [[borica-way4-settings-fields]].
- The customer-facing **Cards on file** panel lives on [[customers-details-payments]].

## What the merchant can do here

- **Enable Save Customer Card** — signed-in customers can save their card after their first purchase and reuse it on subsequent purchases without re-entering details.
- **See saved cards per customer** — on the customer details page → Payments tab — see [[customers-details-payments]].
- **Let customers remove a saved card** — the storefront account panel exposes a remove action via `/site.payment.remove-card/borica_way4`.
- **Enable Google Pay / Apple Pay** — adds wallet buttons on storefront checkout that route through Borica's MPay surface.
- **Verify wallet activation on Borica's side** — the merchant must contact their bank / Borica to enable Google Pay / Apple Pay on the terminal too.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Save Customer Card** switch | Enables MERCH_TOKEN_ID tokenisation: returning signed-in customers see their saved card on checkout. | `no` | `yes` / `no` only. Triggers `MERCH_TRAN_STATE=S` on first purchase. Flipping this on also changes the **EGW_TERM_GROUP** value displayed in the fourth card from `SALE` to `SAVE_TOKEN` — see [[borica-way4-settings-fields]]. |
| **Enable Google Pay / Apple Pay** switch | Adds Google Pay + Apple Pay wallet buttons on storefront checkout (Borica's MPay flow). | `0` (off) | `1` / `0`. Borica must also enable this on the terminal side. |

## Business rules

### Save Customer Card — sign-in required

Tokenisation only applies when the buyer is a **signed-in (non-guest) customer**. Guest checkouts never trigger the token-save flow regardless of the toggle. The customer must also opt in implicitly by checking out while signed in — there is no separate "save my card?" checkbox at checkout. `(verify)`

### Save Customer Card — token flow (MERCH_TOKEN_ID)

The platform follows Borica's MERCH_TOKEN flow:

1. **First purchase** — the purchase request includes `MERCH_TRAN_STATE=S` (*Save* — request a card token after this transaction). The customer enters their card on Borica's page, completes 3DS, and on success Borica returns:
   - `MERCH_TOKEN_ID` — the opaque token to use for future charges.
   - `MERCH_TOKEN_EXP` — token expiry.
   - `MERCH_RN_ID` — a reference number Borica uses to look up the token server-side.
   - `CARD` — masked PAN for display.
   - `CARD_BRAND` — card scheme (Visa / Mastercard / etc.) for display.
2. **Platform stores** these on the customer-card record and on the customer's *Cards on file* panel. See [[customers-details-payments]].
3. **Subsequent purchases** — when the customer chooses Borica again at checkout, the platform calls Borica's pay-by-token endpoint server-to-server with `MERCH_TRAN_STATE=M` + the stored `MERCH_TOKEN_ID` + `MERCH_RN_ID`. The customer does not see Borica's page (depending on whether the issuer challenges 3DS).
4. **Customer-initiated removal** — the customer can delete a saved card via `/site.payment.remove-card/borica_way4` from the storefront's account panel.

### EGW_TERM_GROUP toggles with Save Customer Card

Flipping **Save Customer Card** ON also changes the **EGW_TERM_GROUP** value displayed in the fourth settings card from `SALE` to `SAVE_TOKEN`. The merchant must re-submit this new value to Borica when the bank registers (or updates) the terminal — otherwise the token-save call will be rejected by Borica with a TERM_GROUP mismatch. See [[borica-way4-settings-fields]].

### Save Customer Card vs Authorize — pick one

When both **Save Customer Card** is ON and **Authorization mode = Manual** (authorize), the runtime picks the **authorize** branch — the token-save call is skipped on the authorize transaction. The two flags can coexist in configuration but the merchant should pick one for clarity. Auto-capture + Save Customer Card is the most common pairing. See [[borica-way4-authorize-capture]].

### Google Pay / Apple Pay (MPay) flow

When **Enable Google Pay / Apple Pay** is on:

1. The storefront's payment-method block renders **three buttons** instead of one: card, Google Pay, Apple Pay.
2. Clicking a wallet button hits `/site.payment.borica-mode/<G|A|N>` — the chosen mode is stored in session.
3. The next purchase request adds an `MPAY` field with the chosen value:
   - `MPAY=G` — Google Pay.
   - `MPAY=A` — Apple Pay.
   - `MPAY=N` — regular card (no wallet).
4. Borica's hosted page opens directly into the chosen flow.

### Wallet activation requires Borica's terminal-side enablement

CloudCart cannot enable Google Pay / Apple Pay on the Borica side. The merchant must explicitly request wallet activation from their bank / Borica when registering the terminal. If the wallet button is shown on CloudCart but Borica has not activated it terminal-side, the transaction will fail at Borica's page.

### Apple Pay device / browser requirements

Apple Pay only renders on supported Apple devices in Safari (or on macOS desktop Safari with a paired iPhone). On other devices the Apple Pay button is hidden by the storefront automatically. `(verify)` — exact device-detection logic is handled by Borica's MPay surface, not CloudCart.

## Related

- [[payment-providers-borica-way4]] — hub.
- [[borica-way4-settings-fields]] — the two toggles + the EGW_TERM_GROUP display field.
- [[borica-way4-payment-lifecycle]] — base purchase flow that this aspect extends with `MERCH_TRAN_STATE=S` / `MPAY=G|A|N`.
- [[borica-way4-authorize-capture]] — interaction with Authorize mode (pick one).
- [[customers-details-payments]] — saved-card management for individual customers.
- [[checkout-flow]] — storefront checkout where the wallet buttons render.

## Open questions

- ⏸️ Whether the storefront exposes a *"save my card for next time?"* checkbox at checkout (vs always saving when the toggle is on for signed-in customers). `(verify)`
- ⏸️ Behaviour when a stored token's `MERCH_TOKEN_EXP` is past — does the platform proactively delete or just attempt the charge and let Borica fail it? `(verify)`
