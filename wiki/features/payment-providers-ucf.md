---
type: feature
nav_path: "Payment Providers → UCF"
route_name: apps.ucf.settings
route_path: /admin/payment-providers/ucf
aliases: ["Ucf", "UCF", "UniCredit Consumer Financing", "UCF Bulbank email", "Bulgarian consumer credit legacy", "Email-based consumer credit"]
tags: [paymentproviders, payment-providers, ucf, bulgaria, credit, leasing, installments, unicredit, email-flow, legacy]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 1
---
# UCF

## Purpose

**UCF** is the **legacy email-request flow** for **UniCredit Consumer Financing** in Bulgaria — the older integration that predates [[payment-providers-smart-ucf|Smart UCF]]'s online API. When the customer picks UCF at checkout, the order is captured and an email is sent to UCF at `the provider's support address` with the customer's details, the cart, and the selected financing scheme. UCF staff process the application manually: they contact the customer, verify their identity, run underwriting, and confirm back to the merchant by email or phone. The order's payment status stays in pre-completion states until the merchant manually marks it Completed (after UCF approves) or Canceled / Failed (after UCF rejects).

This integration is **simpler than Smart UCF**: no online underwriting portal, no real-time status sync, no invoice upload — only the email + a manual scheme calculator on the CloudCart side. For new installations, [[payment-providers-smart-ucf|Smart UCF]] is the recommended path; this UCF provider is retained for merchants with existing email-flow agreements with UCF.

## Where to find it

Sidebar → **Payment Providers** → click **UCF**. The route is `/admin/payment-providers/ucf`; the provider key is `ucf`.

## What the merchant can do here

- **Install / Uninstall** the UCF payment method and **toggle Active** on / off in the header.
- **Configure the request email** — contact address and agreement number that go in the email UCF receives.
- **Configure the installment offer** — minimum price, min / max period, step interval, and monthly interest rate that drive the storefront calculator.
- **Override the customer-facing label** — logo, title, description on storefront checkout.

UCF has **no Test / Live mode** (it's email-only — there is no sandbox).

## Settings & fields

The page renders **one always-expanded card** titled *"UCF settings"*, with these fields stacked top-to-bottom:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Send email after completing an order** (`send_email_after_checkout`) | Whether the platform fires the request email after the customer places the order. | On | Switch. |
| **Email address** (`email`) | Where UCF receives the request emails. | `the provider's support address` | Required, valid email. Errors: "Email is required." / "Entered email is invalid." |
| **Agreement or Merchant ID** (`id`) | UCF-issued contract number — included in the request email subject. | Empty | Required. Error: "Number of agreement is required." |
| **Minimum order value** (`min_price`) | Hide UCF from checkout if order total is below this. | Empty | Required. Error: "Minimum price is required." Cannot be set below UCF's contractual floor (`provider.meta.min_price`). |
| **Minimum period** (`min`, months) | Minimum installment period offered to the customer. | Empty | Required. Error: "The minimum period is required." Bounded by `provider.meta.step`. |
| **Maximum period** (`max`, months) | Maximum installment period offered. | Empty | Required. Error: "Maximum period is required." Bounded by `provider.meta.step` ceiling. |
| **Step interval in months** (`step`) | Step between offered plan lengths (e.g., 3 → 3/6/9/12 months). | Empty | Required. Error: "The step interval is required." `min: 1`, `max: provider.meta.step.max`. |
| **Percentage per month** (`percentPerMonth`) | Monthly interest rate used in CloudCart's installment calculation. | `1.2` | Required. Error: "Percent per month is required". `min: 0`. |
| **Interest-free lease (in months)** (`free_leasing`) | Comma-separated list of months presented as 0%. Placeholder `3,6,18`. | Empty | Help: *"Here you can specify which months will be offered with free instalments by separating the values using commas (Example: 3,6,18)"*. |
| **Logo / Title / Description** | Standard storefront-label override. | Provider defaults | |

The server-provided `provider.meta` object carries the bounds, so even though the inputs are free-form numbers, the merchant cannot save a value below UCF's contractual floor or above the platform-permitted ceiling.

## Business rules

### Customer flow — calculator + email request, all manual

UCF is the simplest credit flow in CloudCart:

1. **At checkout** — the customer sees a financing calculator showing installment options computed locally from the merchant's settings (Min / Max months, Step, Percent per month, total order amount). Each plan row shows: months, monthly payment, total repayment.
2. **At order placement** — the platform creates a payment row with `provider=ucf` in a pending-credit state. The plan choice is stored.
3. **Email to UCF** — the platform sends an email to `the provider's support address` (or whatever the merchant configured) with the order ID, customer data, cart items, chosen plan. The subject typically includes the merchant's agreement number.
4. **UCF processes manually** — UCF staff contact the customer, verify identity (EGN, employment, income), and approve or reject.
5. **Merchant manually marks payment** — based on UCF's email or phone confirmation back, the merchant goes to the order page and marks the payment as Completed (approved) or Canceled / Failed (rejected).

There's **no API integration** — UCF doesn't talk to CloudCart at all in this flow. Everything is email + manual.

### Calculator math

The installment calculator on the storefront uses **simple multiplicative interest**:

```
monthly_payment = order_amount × (1 + percentPerMonth × months / 100) / months
total_repayment = monthly_payment × months
```

The default percent-per-month is 1.2; the merchant can override it in settings. (This is a simplified APR display — actual UCF underwriting may produce different rates based on customer profile.)

### Plan dropdown

The plan dropdown on the storefront is computed as:

```
months ∈ {min, min+step, min+2*step, ..., max}
```

E.g., min=3, max=24, step=3 → plans of 3, 6, 9, 12, 15, 18, 21, 24 months.

The merchant tunes this range to match what UCF will underwrite for their merchant agreement (different agreements allow different plan ranges).

### Refunds and gateway data

There's **no API integration**, so UCF stores no gateway response payload — the chosen plan (months, monthly payment) may be kept for audit, but nothing external. Refunds happen entirely off-platform between the merchant, UCF, and the customer; the merchant changes the order's payment status manually to reflect them.

### Plan-tier grouping

UCF is a credit-payment type — group "credit" rather than "regular" — reflected in the order's color class (`order-payment-color-credit`) and in storefront grouping.

### Request email

The email body uses the standard creditor-service email shared with other email-based credit providers (order details, customer block, scheme parameters, plan calculation); UCF inherits it without override. The subject is built from the translation key `leasing.email.subject` appended with the merchant's site name (`<subject> | <site name>`) and is rendered in the platform's default locale — unlike [[payment-providers-bnp|BNP's]] hard-coded Bulgarian subject, so a Romanian-locale store sends a Romanian subject.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where UCF is installed / uninstalled.
- [[payment-providers-smart-ucf]] — modern API-based UCF integration with online underwriting (recommended for new merchants).
- [[payment-providers-bnp]] — analogous email/eCom credit integration (BNP Paribas).
- [[payment-providers-fibank-bnpl]] — Fibank's BNPL consumer credit.
- [[payment-providers-dsk-bnpl]] — DSK's BNPL consumer credit.
- [[payment-provider]] — entity definition.
- [[payment-status]] — credit-flow status mapping.
- [[checkout-flow]] — concept page on the storefront checkout.

## Open questions

- ⏸️ Whether the default `1.2 %` per-month calculator-display rate still matches UCF's current advertised rate is a UCF-side commercial question. UCF's actual rate per customer is set by their underwriting, not by this field — the merchant typically tunes the value to match what UCF advertises today.
