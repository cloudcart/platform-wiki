---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Tax Invoices"
route_name: apps.cloudcart_pay.tax-invoices
route_path: /admin/payment-providers/cloudcart_pay/tax-invoices
aliases: ["CloudCart Pay tax invoices", "CloudCart Pay fee invoices", "CloudCart Pay invoices", "Download CloudCart Pay invoice", "Preparing PDF", "Фактури CloudCart Pay", "Данъчни фактури CloudCart Pay", "Фактура за таксите CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, invoices, fees]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 1
---
# CloudCart Pay — Tax Invoices

## Purpose

The **Tax Invoices** tab lists the tax invoices issued to the merchant's CloudCart Pay account for the CloudCart Pay fees, and lets the merchant download each one as a PDF for the accounts. Each row shows the invoice number, description, billing period, issue date, amount and whether the PDF is ready.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Tax Invoices** tab (between **Transactions** and **Payouts**). Address: `/admin/payment-providers/cloudcart_pay/tax-invoices`.

## What the merchant can do here

- **See the issued tax invoices**, newest first, 50 at a time.
- **Download** an invoice's PDF once it is ready.
- **Load More** older invoices.
- **Refresh** the list.

## Settings & fields

| Column | What it shows | Notes |
|---|---|---|
| **Number** | The invoice number. | |
| **Description** | The invoice's title or description. | "-" when empty. |
| **Period** | The billing period, e.g. "01.09.2026 - 30.09.2026". | Shows the last day included; a one-day period shows one date. |
| **Issue Date** | The date the invoice was issued (DD.MM.YYYY). | |
| **Amount** | The invoice total in its currency. | |
| **Status** | **Issued** (green) when the PDF can be downloaded; **Preparing PDF** (amber) while it is still being produced. | |
| **PDF** | **Download** with a PDF icon; opens in a new tab. | Shown only when the status is **Issued**. |

Buttons: **Refresh** at the top (when an account is connected) and **Load More** under the table while there are more invoices.

## Business rules

### Invoices for the fees

The invoices are issued for the fees CloudCart Pay charges on the account; the fee of each payment is on the [[payment-providers-cloudcart-pay-transactions|Transactions tab]], and the prices are in [[cloudcart-pay-pricing]]. Only issued invoices are listed.

### Issued first, PDF afterwards

An invoice is issued first and its PDF is produced afterwards. Until then the row reads **Preparing PDF** and has no download link; **Refresh** later shows it as **Issued** with **Download**.

### Download

Each click on **Download** fetches a fresh, short-lived link to the PDF through the admin panel, so it only works for someone signed in to the store's admin. If the PDF is not available, the merchant sees *"Tax invoice is not available for download"* or the reason returned.

### Empty and error states

- No invoices yet: *"No tax invoices yet."*
- No connected account: *"Please complete the onboarding process first."* (Моля, първо завършете процеса на регистрация.)
- The list could not be read: a red box with the reason.

### Same account and environment as the other tabs

The list is read live for this store's connected account in the environment the store charges in (test or live). After linking another account it shows that account's invoices ([[cloudcart-pay-account-model]]).

### Staff access

The tab is available only to staff whose role allows the store's payment methods settings ([[settings-staff]]).

## Related

- [[payment-providers-cloudcart-pay]] — CloudCart Pay hub.
- [[payment-providers-cloudcart-pay-transactions]] — the fee on each payment.
- [[cloudcart-pay-transactions-totals]] — **Total Fees** for a period.
- [[cloudcart-pay-pricing]] — what CloudCart Pay costs.
- [[cloudcart-pay-merchant-terms]] — the agreement the fees belong to.
- [[payment-providers-cloudcart-pay-payouts]] — payouts.

## Open questions

- How often invoices are issued (the period column suggests one per billing period; the period length is not set by CloudCart).
- Whether invoices are issued while the 0% transaction fee applies (until 31 December 2026).
- Bulgarian labels of this tab and its columns (not in the translation files read).
