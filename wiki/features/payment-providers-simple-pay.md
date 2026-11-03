---
type: feature
nav_path: "Settings → Payment methods → SimplePay"
route_name: apps.simple_pay.settings
route_path: /admin/payment-providers/simple_pay, /admin/payment-providers/simple_pay/settings
aliases: ["SimplePay", "OTP SimplePay", "Simple Pay", "SimplePay Hungary", "SimplePay IPN URL", "SimplePay data transfer declaration", "Adattovábbítási nyilatkozat", "SimplePay Унгария", "Плащане със SimplePay", "Плащане с карта в Унгария"]
tags: [paymentproviders, payment-providers, simple-pay, otp, hungary, apple-pay, google-pay]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# OTP SimplePay

## Purpose

**OTP SimplePay** is the online payment service of the OTP Group in Hungary. The shopper is sent to SimplePay's payment page, pays by card, Apple Pay or Google Pay, and returns to the store. The app's own description: *"OTP SimplePay — accept card payments, Apple Pay and Google Pay on the SimplePay payment page (HUF, EUR, USD)."* (Bulgarian: *"OTP SimplePay — приемайте картови плащания, Apple Pay и Google Pay през платежната страница на SimplePay (HUF, EUR, USD)."*) It is offered to stores operating in Hungary. The merchant needs a SimplePay contract.

## Where to find it

Settings → **Payment methods** → **+ Add payment method** → **SimplePay**, listed for stores operating in Hungary. Address: `/admin/payment-providers/simple_pay` (overview) and `/admin/payment-providers/simple_pay/settings` (settings). The registration declares no plan gate.

## What the merchant can do here

- Choose **Test mode** or **Live mode**.
- Enter the account's currency, **Merchant ID** and **Secret key** for each mode.
- Copy the **IPN URL** into the SimplePay admin.
- Fill in the **Data transfer declaration** details.
- Show or hide the **SimplePay logo** in the store footer.
- Set the standard fields: logo, title and description, minimum and maximum order amount, discount.
- Refund a payment, fully or in part, from the order.

## Settings & fields

| Box → field | What it does | Default | Notes |
|---|---|---|---|
| **Live credentials** / **Test credentials** → **Account Currency** | The currency of the SimplePay account: HUF, EUR or USD. | HUF | Only the box of the selected mode is in use. |
| same → **Merchant ID**, **Secret key** | The account's credentials. | Empty | Found in the SimplePay merchant admin (secure.simplepay.hu; sandbox.simplepay.hu for test): **Partner** → the eye icon of the account → **Technical data**. No whitespace. |
| **IPN URL** | The address SimplePay sends each payment result to. Read-only, with **Copy**. | Filled in | Shown before the first save. |
| **Data transfer declaration** → **Company Name**, **Registered seat** | Shown to the shopper in the declaration at checkout, as in the SimplePay contract. | Company name from the store's settings; seat empty | Both required. |
| **SimplePay logo** → **Show the SimplePay logo in the store footer** (`show_logo`) | The logo and accepted cards in the footer. | On | The checkout box always shows the logo. |

Where to enter the IPN URL, in the sandbox admin and in the live admin: **Partner** → the eye icon of the account → **Technical data** (Technikai adatok) → **System notifications** (Rendszer értesítések) → **IPN URL** → **Save** (Mentés). The page warns: *"Without it, orders are updated only when the customer returns to the store or by the periodic status check."*

## Business rules

### One account per mode, orders converted

SimplePay issues a separate merchant account per currency, and a store uses one at a time per mode. An order in another currency is converted to the account's currency at the store's exchange rate at purchase. A partial refund uses the same rate. A HUF charge is rounded to whole forints.

### Checks on save and on activation

Saving checks the selected mode's account with SimplePay. When the account changed, it also starts and cancels a test payment to confirm the currency. Messages:

- *"Enter the Merchant ID and Secret key of your SimplePay account."*
- *"Enter both the Merchant ID and the Secret key of this account"*
- *"Invalid SimplePay merchant ID or secret key"*
- *"This SimplePay account is in HUF. Choose HUF as the account currency."* (the same for EUR and USD)
- *"This SimplePay account does not accept the selected currency."*
- *"Your store currency cannot be converted to the currency of your SimplePay account."*
- *"Enter your company name as in your SimplePay contract"*, *"Enter your registered seat as in your SimplePay contract"*

The **Active** switch is refused with *"Enter your SimplePay Merchant ID and Secret key before enabling this payment method."*, or with the message about the store currency.

### At checkout

The payment method's box shows the SimplePay logo, a note about the redirect, and the data transfer declaration, starting *"By starting the payment I accept the following data transfer declaration:"*. Starting the payment counts as accepting it; there is no checkbox. The wording is SimplePay's own and kept as it is: Hungarian on Hungarian storefronts, English on every other language.

The payment page opens in a window of **30 minutes**. There is no embedded form and no saved cards. Apple Pay and Google Pay run under the card method on SimplePay's page. Capture is one-step.

### What the shopper sees on returning

| Outcome | Text on the return page |
|---|---|
| Success | *"Successful transaction."* with the SimplePay transaction ID |
| Failure | *"Failed transaction."* with the ID and *"Please check if the details provided during the transaction are correct. If all of the details were provided correctly, please contact the bank that issued your card in order to investigate the cause of the rejection."* |
| Cancelled | *"You cancelled the payment"* |
| Timed out | *"You exceeded the maximum time available to start the transaction."* |

### How the payment status updates

The status arrives by SimplePay's notification to the IPN URL, the shopper's return, and a background check. The check starts 10 minutes after the redirect and repeats every 5 minutes; a payment still open at 3 hours is timed out. A return reporting success leaves the payment `pending` until the notification or the check confirms it. The order follows the rules on [[order-status-auto-transitions]].

| SimplePay status | Payment status |
|---|---|
| `INIT` | `requested` |
| `INPAYMENT`, `INFRAUD` | `pending` |
| `AUTHORIZED` | `authorized` |
| `FINISHED` | `completed` (`refunded` after a full refund) |
| `NOTAUTHORIZED` | `failed` |
| `CANCELLED`, `REVERSED` | `cancelled` |
| `TIMEOUT` | `timeouted` |

### Refunds

A full refund runs from the order's **Refund payment** button and refunds what is left after any earlier partial refunds ([[orders-payment-refund]]). A partial refund runs through an order return ([[orders-payment-refund-partial-refunds]]) and leaves the payment `completed`.

### Going live

The integration plan says SimplePay tests each merchant's shop individually (itsupport@simplepay.com, 5 to 8 business days), once the sandbox account and the IPN URL are in place (verify with SimplePay).

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — the payment methods list.
- [[multi-currency]] — the store's exchange rates used for the conversion.
- [[orders-payment-refund]] — full refunds.
- [[orders-payment-refund-partial-refunds]] — partial refunds.
- [[order-status-auto-transitions]] — how the order follows its payments.
- [[payment-status]] — payment statuses.

## Open questions

- The Bulgarian admin labels (production translation table).
