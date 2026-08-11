---
type: feature
nav_path: "Payment Providers → Smart UCF"
route_name: apps.smart_ucf.settings
route_path: /admin/payment-providers/smart_ucf
aliases: ["SmartUcf", "Smart UCF", "UniCredit Consumer Financing", "UCF online", "UCF Bulbank", "Bulgarian consumer credit", "Bulgarian installment"]
tags: [paymentproviders, payment-providers, smart-ucf, bulgaria, credit, leasing, installments, unicredit, redirect, invoicing]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 1
---
# Smart UCF

## Purpose

**Smart UCF** is the online installment-financing channel of **UniCredit Consumer Financing** (a UniCredit Bulbank subsidiary), used by Bulgarian merchants to offer **consumer-credit / installment plans** on retail purchases. When the customer picks Smart UCF at checkout, instead of charging a card the merchant sends a financing request to UCF; UCF underwrites the customer online (they are redirected to UCF's portal and fill in EGN + income + employment details), and on approval the order is paid in installments over 3–60 months.

Like [[payment-providers-bnp|BNP Paribas Personal Finance]], Smart UCF is a **credit-payment** provider, not a card gateway. The integration provides a **redirect** underwriting flow, **real-time status sync**, automatic **invoice upload**, and **promotional financing schemes** tied to product / category online-product-codes (`ucf_cop`).

Smart UCF is **Bulgarian-market-only** and uses BGN — all customer-facing copy is Bulgarian, and the underwriting terms map to Bulgarian consumer-credit regulations.

## Where to find it

Sidebar → **Payment Providers** → click **Smart UCF**.

The route is `/admin/payment-providers/smart_ucf`; the internal provider key is `smart_ucf`. Promotional-scheme configuration lives at a separate route, `admin.ucf.promo`.

## What the merchant can do here

- **Install / Uninstall** the method and **toggle Active** in the header.
- **Switch between Test and Live mode** — different UCF credentials per mode.
- **Enter UCF credentials** (`user`, `pass`) and a **minimum order price** below which UCF is hidden at checkout (default 75 BGN).
- **Set a Default online product code** (`default_cop`) — the COP fallback used when neither the product nor its category has a `ucf_cop` mapped.
- **Override the customer-facing label** (logo / title / description), set an **amount range** (min / max), and an optional **discount**.
- **Manage promotional financing schemes** at the linked promo page (month counts, interest rates, COP mappings) and **tag products / categories** with `ucf_cop` for correct underwriting routing.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** (`configuration.mode`) | Switches between UCF test and live endpoints. | `test` | `test` / `live`. |
| **Username** (field key `user`) | UCF-issued API username. | Empty | Required. Error: "Please, enter username". |
| **Password** (field key `pass`) | UCF-issued API password. | Empty | Required. Error: "Please, enter password" |
| **Min price** (field key `min_price`) | Hide UCF from checkout if order total is below this. | 75 BGN | Required. Error: "Minimum price is required" |
| **Default online product code** (field key `default_cop`) | Fallback COP used when product / category has no mapping. | Empty | See *Default COP fallback* below. |
| **Logo / Title / Description** | Standard storefront-label override. | Provider defaults | |
| **Min / Max amount** | Standard amount-range filter. | Empty | |
| **Discount** | Discount applied when customer picks Smart UCF. | None | |

## Business rules

### Customer flow — redirect + online underwriting

Smart UCF is a **hosted redirect** credit flow:

1. **At checkout** — the customer picks a financing scheme (month count, down payment) from the promo dropdown. CloudCart shows the monthly installment, APR (NIR), and total repayment in Bulgarian Lev.
2. **At order placement** — CloudCart creates a payment in Pending status and redirects the customer to UCF's underwriting portal with the order details (order number, customer name, phone, email, delivery address, online product code, total / initial / monthly price, installment count, items list).
3. **Customer underwrites on UCF's portal** — enters EGN, employer info, income, etc.
4. **UCF posts back** to `payments.return/smart_ucf` with the outcome; CloudCart syncs the final status (see below).

### Status mapping — `reqStatusCode` thresholds

UCF returns a numeric `reqStatusCode` for the application's underwriting progress, mapped to a CloudCart status by number range:

| `reqStatusCode` range | CloudCart status |
|-----------------------|------------------|
| > 65 | **Canceled** (`cancelled`) |
| 51–65 | **Completed** |
| ≤ 50 | **Pending** |

This threshold model (rather than a discrete enum) lets UCF add intermediate underwriting states without breaking the integration — each new code falls into one of the three buckets.

UCF's status API is the **source of truth**: both the customer return and a periodic background reconciliation query UCF directly and re-map via these thresholds, so the platform never relies on the return URL's parameters — making the flow robust to the customer closing the browser before redirect, return-URL tampering, and network failures. The reconciliation re-syncs Pending payments until terminal, and short-circuits on an already-Canceled payment so a final cancellation is never undone if UCF later reverts to "pending" internally.

### Invoice upload

UCF requires the invoice on file before the credit agreement is finalised. Once the order is fulfilled and an invoice is generated by the merchant's [[settings-invoicing]] integration, the platform automatically pushes the PDF to UCF with the order and invoice numbers. If UCF rejects it, the error is captured into `provider_data.providerStatus` for audit and the payment continues without a UI error.

### Pricing scheme management

The separate `admin.ucf.promo` page manages:

- **Online product codes (COPs)** — UCF's category-level financing-product identifiers; each product class (electronics, furniture, etc.) gets a COP from UCF.
- **Promotional schemes** — month counts (3, 6, 9, 12, 18, 24, 36, 48, 60), interest rates, down-payment requirements.
- **Per-product / per-category COP tagging** with `ucf_cop`.

### Default COP fallback

When the cart has no product / category with a `ucf_cop` mapped, the integration falls back to `default_cop`. If `default_cop` is also empty, the goods list becomes `['Not found']` — UCF rejects this, but the integration doesn't fail loudly, giving the merchant a chance to fix configuration without breaking checkout.

### Items metadata & shipping line

The cart's items are forwarded to UCF as a structured list — code (product ID), name, count, single price. Items with no ID (services, fees) have their amounts redistributed proportionally across items that do have IDs (so the total still matches), plus a **shipping line** named `"Доставка"` (Bulgarian for "Delivery") for the shipping amount.

### Plan-tier gating

Smart UCF is a credit-payment type — group `credit` rather than `regular`. This shows in the order's `order-payment-color-credit` colour class and storefront grouping.

### EGN entered on UCF's portal only

The redirect payload deliberately omits the customer's EGN — they enter it on UCF's portal, not on CloudCart. This is a privacy / regulatory choice: the EGN is sensitive personal data UCF wants entered through their own secured form.

### Fingerprint onboarding

The Settings page also shows a read-only **Smart UCF Fingerprint** — the platform's identifier UCF uses to know which CloudCart store is calling. The merchant gives this to UCF when onboarding; UCF whitelists it so the integration can connect.

## Related

- [[payment-providers]] — hub.
- [[settings-payment-providers]] — global list where Smart UCF is installed.
- [[payment-providers-ucf]] — older / simpler UCF integration using the email-request flow rather than the online API.
- [[payment-providers-bnp]] — analogous Bulgarian consumer-credit provider (BNP Paribas Personal Finance).
- [[payment-providers-fibank-bnpl]] — Bulgarian BNPL credit (Fibank).
- [[payment-providers-dsk-bnpl]] — Bulgarian BNPL credit (DSK).
- [[payment-provider]] — entity definition.
- [[payment-status]] — Pending / Completed / Canceled mapping.
- [[checkout-flow]] — storefront checkout concept.

## Open questions

- ⏸️ Whether UCF's current `reqStatusCode` enumeration still fits the mapping bands (`≤ 50 → Pending`, `51–65 → Completed`, `> 65 → Canceled`). Forward-compatible by design, but re-audit if UCF announces a code-range change.
