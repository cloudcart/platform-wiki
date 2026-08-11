---
type: feature
nav_path: "Payment Providers → TBI"
route_name: apps.tbi.settings
route_path: /admin/payment-providers/tbi
aliases: ["TBI", "Tbi", "TBI legacy", "TBI lease", "ТБИ", "ТБИ Банк лизинг", "TBI installment legacy"]
tags: [paymentproviders, payment-providers, tbi, bnpl, installments, bulgaria, legacy]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# TBI

## Purpose

**TBI** is the legacy installment-loan payment method for TBI Bank in CloudCart — a pre-API, calculator-style integration that advertises installment plans on the storefront without a live API to TBI. The merchant enters their TBI agreement / merchant ID + contact email, picks a min / max number of months + a step interval and a flat monthly interest rate, and the storefront shows the customer a locally-calculated installment table. There is NO redirect-to-TBI checkout, NO real-time pricing call, NO automated status callback — when a customer picks TBI, the merchant follows up offline by email (the default address is `the provider's support address`).

This integration is superseded by the modern [[payment-providers-fusion-pay|Fusion Pay]] provider (real-time TBI API, redirect-to-TBI checkout, free-leasing schemes, button tiers). **New merchants should install Fusion Pay, not TBI.** The TBI provider remains in CloudCart only for stores that haven't migrated.

Period range is **3–60 months**, step is configurable (typically 3), default monthly rate **1.5%**. BGN / Bulgaria only — no multi-currency support.

## Where to find it

Sidebar → **Payment Providers** → click **TBI**. Route `/admin/payment-providers/tbi` (legacy route `settings/payment_providers/edit/tbi`). Settings is the only screen — no sub-tabs, and no test/live environment-mode separation (legacy single-environment provider).

## What the merchant can do here

- Install / Uninstall the payment method, and activate / deactivate via the header switch.
- Configure the installment calculator parameters (see Settings & fields).
- Toggle **Send email after completing an order** to auto-notify the contact email on every TBI order.
- Set a **Minimum order value** below which TBI is hidden on the storefront.
- List **Free instalments** — specific month counts that are interest-free (e.g. `3,6,18`).
- Edit the **Description** shown to the customer on the storefront after a TBI order completes.
- Standard payment-provider controls (Logo, Title, customer-facing description).

## Settings & fields

The fields are grouped into three rows: the TBI settings card, an **Interest free lease** row (free-instalment list + its title), and a **Checkout settings** row (the post-order description).

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Send email after completing an order** | Auto-emails the contact email on every TBI order completion. | OFF | Switch. |
| **Email address** | Contact email for TBI staff. | `the provider's support address` | Required: `Email is required.` Must be valid: `Email is not valid.` |
| **Agreement or Merchant ID** | TBI Bank-issued merchant / agreement number. Free text. | Empty | Required: `Number of agreement is required.` |
| **Minimum order value** | Order total below which TBI is hidden on the storefront. | Empty | Required: `Minimum price is required`. Number; min is the platform minimum. |
| **Minimum period (3 months)** | Lower bound (months) of the calculator. | 3 | Required: `The minimum period is required.` Range 3–60. |
| **Maximum period (60 months)** | Upper bound (months) of the calculator. | 60 | Required: `Maximum period is required.` Range 3–60. |
| **Step interval in months** | Increment between offered month counts. e.g. step 3 with min 3 / max 12 → customer sees 3, 6, 9, 12. | 3 | Required: `The step interval is required.` Number, min 1. |
| **Percentage per month** | Flat monthly interest rate fed into the local pricing module. | 1.5 | Required: `Percent per month is required.` Number, min 0. |
| **Free instalments** | Comma-separated month counts that are interest-free, e.g. `3,6,18` → those plans are calculated at 0%. | Empty | Free text. Help: "Here you can specify which months will be offered with free instalments by separating the values using commas(Example: 3,6,18)". |
| **Title for interest-free leases** | Heading shown above the 0% offers in the customer's pricing module. | Empty | Free text. |
| **Description** | Free-form text shown on the storefront in the post-order TBI message. | Empty | TinyMCE editor. |

## Business rules

### How TBI legacy works for the merchant

TBI is a "show-me-the-numbers" integration:

1. **Storefront** — the customer adds products to the cart and picks TBI as the payment method.
2. **Local pricing** — CloudCart computes installment plans locally from the merchant's min / max / step / monthly rate / free-instalments list. NO API call to TBI Bank.
3. **Customer picks a plan** in the storefront module.
4. **Order is placed** — the order goes into PENDING with TBI as the payment method.
5. **CloudCart emails the contact address** (if Send email after completing an order is ON).
6. **Merchant contacts the customer / TBI Bank** manually — this is the entire "approval" loop. There is no API-driven status update.

### Pricing — flat rate with free-instalments override

For each month `m` in `[min, max]` stepped by `step`: if `m` is in the free-instalments list the rate is 0% (interest-free); otherwise the flat **Percentage per month** (default 1.5%) applies. The local pricing module produces monthly payment, NIR, APR, and total repayment for each plan — those numbers appear in the customer's pricing module.

### Refund handling

Not automated. The merchant handles refunds out-of-band with TBI Bank.

### The follow-up email body

When Send email after completing an order is ON, the notification goes out as the **shared creditor-request template** (the same template used by [[payment-providers-ucf|UCF]], [[payment-providers-dsk-zero|DSK Zero]], and a BNP-specific variant). The body is a fixed Bulgarian-language text the merchant cannot customise from CloudCart; it states:

- A new leasing application has arrived from the store, naming the company (and EIK / BULSTAT if configured) and the merchant agreement / ID.
- The applicant's full name, EGN (Bulgarian personal ID), phone, email, and home address.
- The order timestamp, total amount, and a request to confirm or refuse the leasing.

The merchant name, recipient email, and agreement ID are pulled from the TBI settings.

### Legacy status

This is the legacy TBI provider; the modern replacement is [[payment-providers-fusion-pay|Fusion Pay]], which uses TBI's real API. **New merchants should NOT install TBI** — install Fusion Pay instead. For a merchant asking "how do I take TBI installment payments," the answer is: install Fusion Pay (this page is legacy reference only). CloudCart keeps TBI in the system for stores that haven't migrated.

### Plan-gating

TBI is listed in the plan features map but no specific gate is applied — it is available on all plans.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-fusion-pay]] — **modern replacement** for this provider (real TBI API). New merchants use this.
- [[payment-providers-tbi-bank]] — separate TBI integration for card-style payments via TBI Bank's gateway (different product, not the installment loan).
- [[payment-providers-dsk-bnpl]] — DSK Bank's BNPL with a similar real-time-API model (vs TBI's local-calculator model).

## Open questions

_None._
