---
type: feature
nav_path: "Settings → Payment methods → tbi bank Romania"
route_name: apps.fusion_pay_ro.settings
route_path: /admin/payment-providers/fusion_pay_ro, /admin/payment-providers/fusion_pay_ro/settings
aliases: ["tbi bank Romania", "tbi Romania", "Fusion Pay Romania", "Fusion Pay RO", "TBI RO", "Plata in rate tbi", "tbi Румъния", "Fusion Pay Румъния", "Покупки на вноски в Румъния"]
tags: [paymentproviders, payment-providers, fusion-pay, tbi-bank, bnpl, installments, romania]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# tbi bank Romania (Fusion Pay)

## Purpose

**tbi bank Romania** is the buy-now-pay-later and installments method for stores in Romania. The shopper picks a plan at checkout, is sent to tbi's page, and makes the final choice and application there. The app's own description: *"tbi bank Fusion Pay — buy now, pay later and installments for stores in Romania (RON)."* (Bulgarian: *"tbi bank Fusion Pay — купи сега, плати по-късно и покупки на вноски за магазини в Румъния (RON)."*) It is separate from [[payment-providers-fusion-pay]], the method for Bulgaria: its own keys, and schemes returned ready by tbi with no category or promo mapping, no down payment and no tiers. Each merchant has their own contract with tbi.

## Where to find it

Settings → **Payment methods** → **+ Add payment method** → **tbi bank Romania**, listed for stores operating in Romania. Address: `/admin/payment-providers/fusion_pay_ro` (overview) and `/admin/payment-providers/fusion_pay_ro/settings` (settings).

## What the merchant can do here

- Choose **Test mode** or **Live mode**.
- Enter the keys issued by tbi for each mode.
- Limit the periods offered and the order amount range.
- Show or hide the installments card on the product page.
- Set the standard fields: logo, title and description.

## Settings & fields

| Box → field | What it does | Default | Notes |
|---|---|---|---|
| **Test / Live mode** | Which set of keys is used. | Test | |
| **tbi bank production credentials**, **tbi bank UAT (test) credentials** → **Reseller code**, **Reseller key**, **Encryption Key** | The keys from the agreement with tbi bank Romania. In test mode no real loans are created. | Empty | The set of the selected mode is required: *"Reseller code is required"*, *"Reseller key is required"*, *"Encryption key is required"*. |
| **Installment settings** → **Min period**, **Max period** | The periods offered, in months. | 3 and 60 | 3 to 60. Max must not be less than Min. |
| **Installment settings** → **Show the installments button on the product page** (`promo_button`) | The product page card. | On | |
| **Amount from**, **Amount to** | Order total for which the method is offered. | 100 and 65,000 RON | *"Amount from must be at least 100"*, *"Amount to must be at most 65000"*, *"Amount to must be greater than amount from"*. |

## Business rules

### Checks on save and on activation

Saving checks the selected mode's keys with tbi and pulls its schemes again, so a rate agreed with tbi shows at once. Wrong keys give *"Invalid reseller code or key"*. If tbi cannot be reached, the save goes through and the schemes are pulled on first use.

The **Active** switch is refused with:

- *"tbi bank Romania accepts payments in RON only. Change the store currency to RON to enable it."*
- *"Enter the tbi bank reseller code, reseller key and encryption key before enabling this payment method."*

Amounts are never converted: the method is offered only while the store's currency is RON and at least one scheme fits the order amount.

### On the storefront

- **Product page.** A card reading *"Pay in installments from … / month"* with **Details**, showing the cheapest eligible scheme (Bulgarian: *"Плати на вноски от … / месец"*, **Детайли**; Romanian texts are in the store's translations). **Details** opens every scheme.
- **Checkout.** Under **Buy on credit** ([[checkout-step-payment]]), a table of the schemes with period, NIR, installment and total, without an APR column, and a terms checkbox for tbi's general terms. The customer makes the final choice on tbi's page.
- **Schemes.** Refreshed daily at 00:05. If tbi cannot be reached, the last good list is used for up to 7 days.
- **Headless storefronts.** Credit plans are available through the Storefront API; see [[headless-storefront-api]].

### How the payment status updates

The shopper is redirected to tbi. The status is read when the shopper returns, and by a background check for each payment: every 5 minutes for 3 hours, hourly up to 48 hours, then every 6 hours. A payment still open after **14 days** is timed out.

| tbi reports | Payment status |
|---|---|
| Sent (*Comanda trimisa catre TBI*) | `requested` |
| In progress (*Comanda in derulare TBI*) | `pending` |
| Approved (*Plata TBI acceptata*) | `completed` |
| Cancelled or rejected (*Comanda anulata TBI*) | `cancelled` |

An unknown status changes nothing, and a final payment does not move back. The order follows the rules on [[order-status-auto-transitions]].

### Refunds

There is no refund from the admin. The integration plan gives the provider's support address as the address for refunds (verify with tbi).

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-fusion-pay]] — tbi for stores in Bulgaria.
- [[settings-payment-providers]] — the payment methods list.
- [[checkout-step-payment]] — the credit group at checkout.
- [[order-status-auto-transitions]] — how the order follows its payments.
- [[payment-status]] — payment statuses.

## Open questions

- The Bulgarian admin labels (production translation table).
