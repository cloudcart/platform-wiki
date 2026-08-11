---
type: feature
nav_path: "Payment Providers → Klear → Settings"
route_name: apps.klear.settings
route_path: /admin/payment-providers/klear/settings
aliases: ["Klear Settings", "Klear Lending settings", "Настройки Klear", "Клиър настройки"]
tags: [paymentproviders, payment-providers, klear, bnpl, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---
# Settings

## Purpose

The Settings tab is the only configuration surface for Klear. It gathers the **public + private API keys** (separate sets for test and live), an optional **financing-program ID** (a special Klear partnership offer), a **checkout-rule** controlling how strictly that program applies, a **manual capture** toggle, and an optional **product-page promo button**. The 75 BGN minimum order amount is hard-enforced here. Klear is single-tab — no Promotions or Schemes tab; pricing schemes are fetched live from Klear's API at checkout.

## Where to find it

Sidebar → **Payment Providers** → **Klear** → **Settings** tab.

The route is `/admin/payment-providers/klear/settings`. The page renders the shared payment-provider settings shell with the `klear` provider key and these settings boxes: **Klear live settings** (or **Klear test settings**), **Klear financing program settings**, and **Klear promo button settings**.

## What the merchant can do here

- Flip the **Test mode switch** and enter the **Public Api Key** + **Private Api Key** for the active mode.
- Toggle **Manually confirm a payment** (`manual_capture`).
- Enter an optional **Financing program ID**, pick its **checkout rule** (`inclusive` / `exclusive`), and set the product-filter values.
- Toggle **Show button in product page** (`promo_button`).

## Settings & fields

### Credentials

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode switch** | Which credential set is active (`test` vs `live`). | test | Both sets saved at once. Drives which key pair is used at runtime. |
| **Public Api Key** (live or `_test`) | Klear-issued public key. Used as the HTTP Basic auth username. | Empty | Required in the active mode. Server message: `"Public key is required"`. |
| **Private Api Key** (live or `_test`) | Klear-issued private key. Used as the HTTP Basic auth password. | Empty | Required in the active mode. Server message: `"Private key is required"`. |

### Order amount range

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Amount from** | Minimum order total at which Klear shows on checkout. **Cannot be less than 75 BGN** (Klear's commercial minimum). | 7500 (cents = 75.00 BGN) | Required. Server message: `"Amount from must be greater than 75"`. |
| **Amount to** | Maximum order total. | None | Standard payment-provider field, no Klear-specific validation. |

### Manual capture

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Manually confirm a payment** (`manual_capture`) | When ON, Klear orders that come back as `authorized` stay in `Pending` — the merchant manually completes them from the order admin view. When OFF, they auto-complete on Klear's approval. | OFF | Switch (`trueValue: 1`, `falseValue: 0`). |

### Financing program

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Financing program ID** | Klear-issued ID for the merchant's partnership program (e.g., 0% on specific categories). | Empty | Optional. When empty, no filtering is applied — Klear returns its default catalog. |
| **Financing program checkout rule** | Decides how the product filter is enforced. | `exclusive` | Required. Server message: `"Financing program checkout rule is required"`. Dropdown: `exclusive` (default), `inclusive`. |
| **Product filter values** | Defines which products qualify for the financing program. | Empty | A two-part picker (see below). Picking `all` makes the program apply to every product, subject to the checkout rule. |

The **Product filter values** picker is the platform-wide "Products filter" UI (shared with discounts, smart collections, etc.): a **filter dropdown** (`all`, `product`, `vendor`, `tag`, `selection`, `category`) plus a value picker that adapts to the chosen type — so the program can be scoped to specific products, vendors, tags, smart collections, or categories.

### Promo button

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Show button in product page** (`promo_button`) | When ON, renders a Klear-branded "pay with Klear" button on each product detail page that opens a price-breakdown popover. | OFF | Switch (`trueValue: 1`, `falseValue: 0`). |
| **Button-style preview** (read-only) | A side-by-side preview of two Klear button designs, for reassurance only. | n/a | **No merchant-picked variant** — the storefront renders Klear's default button when `promo_button=1`. |

## Business rules

### Defaults applied on first install

When the provider is first installed, these initial values are seeded:

```
mode = test
discount_type = flat
promo_button = 0
financing_program_checkout_rule = exclusive
amount_from = 7500 (= 75 BGN × 100 cents)
```

The merchant starts in test mode with no API keys, no financing program, and the strict `exclusive` checkout rule.

### Auth + endpoints

HTTP Basic auth on every request: username = the active public key (`public_apikey` / `public_apikey_test`), password = the active private key (`private_apikey` / `private_apikey_test`), chosen by the `mode` flag. Client timeout **3 seconds**, no retries.

| Environment | Base URL |
|---|---|
| Live | `https://www.klearlending.com/api/` |
| Test | `https://klear-pre.azurewebsites.net/api/` |

### Payment lifecycle (BNPL installment loan, not a card charge)

1. **Pricing** — at the cart, the platform calls `GET /v1/pricing/{public_api_key}[/{financing_program}]?amount={total}`; Klear returns the installment schemes (interest-bearing and 0% variants).
2. **Checkout** — the customer picks a scheme + down-payment; the platform POSTs the order (line items, customer details, selected scheme, financing program if applicable) and gets back a redirect URL.
3. **Approval** — the customer completes the loan application on Klear's hosted page.
4. **Return** — Klear redirects back with a status; the platform re-queries Klear's transactions endpoint with the returned `checkout_token` + the internal payment ID. The authoritative status comes from that re-query, not the callback payload, so a forged callback URL cannot mark an unpaid order as completed.
5. **Capture** — if `manual_capture` is OFF AND Klear returned `authorized`, the platform captures immediately. Otherwise the payment stays `Pending` for manual completion.

### Status mapping

| Klear status | Mapped |
|---|---|
| `authorized`, `captured`, `confirmed` | `Completed` (or `Authorized` if manual-capture mode and not yet captured) |
| `declined`, `failed` | `Failed` |
| `canceled` | `Canceled` |
| `pending` | `Pending` |

### How checkout-rule filtering works at storefront

At pricing time each cart product is checked against the merchant's filter expression. The program is applied at pricing only (it decides which catalog of schemes the customer sees, never how the payment is captured):

- **Exclusive** (default, strict) — ALL cart products must match. One non-match → fall back to Klear's default catalog.
- **Inclusive** (loose) — ONE match applies the program to the whole basket. No match → fall back to the default catalog.

When the program ID is set and a match is found, the pricing URL gains the `/{financing_program}` suffix; otherwise it is omitted.

### 0% interest vs interest-bearing — separate display

When Klear's pricing endpoint returns mixed schemes, the platform separates them: interest-bearing variants into the main scheme group, 0% variants into a `free_leasing` sub-group below. The merchant doesn't configure this split.

### Refund — email only, NOT API

Klear refunds are NOT API-driven. The integration emails refund requests to a fixed inbox, **`the provider's support address`** — the merchant cannot change this address. Klear processes the refund manually and updates the platform status afterwards.

### Plan-gating, country + currency

Not plan-gated by CloudCart subscription tier. BGN only, Bulgaria only; both Klear API endpoints are Bulgaria-specific.

## Related

- [[payment-providers-klear]] — parent hub (overview tab + checkout-rule explainer).
- [[payment-providers]] — top-level Payment Providers area.
- [[payment-providers-iute-settings]] — Iute settings (similar API-key-pair pattern).
- [[payment-providers-fusion-pay-settings]] — TBI Bank settings; financing-program concept resembles TBI tiers with different semantics.

## Open questions

_None._
