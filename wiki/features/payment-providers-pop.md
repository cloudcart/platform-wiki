---
type: feature
nav_path: "Payment Providers → Pay in store (Pop)"
route_name: apps.pop.settings
route_path: /admin/payment-providers/pop
aliases: ["Pop", "Pop.bg", "Pay in store", "Pay at point", "Pay in physical store", "Pickup payment", "Плащане в магазина", "Плащане на място"]
tags: [paymentproviders, payment-providers, pop, cash, offline, pickup, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# Pop (Pay in physical store)

## Purpose

A configuration screen for the **Pop** payment method — a generic "Pay in some of your physical stores" option for merchants who operate one or more physical retail locations and want to let the customer place an online order and then walk into the brick-and-mortar shop to pay (cash, card on the store's POS, voucher — anything the physical store accepts).

This is one of the simplest offline payment providers in CloudCart, alongside [[payment-providers-cod]] and [[payment-providers-voucher]]: no API credentials, no test mode, no webhook URL. The merchant just installs it and customers see "Pay in store" as a checkout option. The order is committed in the `pending` state and the merchant manually marks it Paid once the customer arrives and completes the in-person payment.

The label "Pop" is the internal provider key; the customer-facing label is whatever the merchant configures (the source default description is *"Your customers will be able to pay in some of your physical stores"*).

## Where to find it

Payment Providers → **Pop**. Provider key: `pop`. Route name `apps.pop.settings`, path `/admin/payment-providers/pop/settings`.

After installing from [[settings-payment-providers]] → "Add payment method".

## What the merchant can do here

- **Install / uninstall** from [[settings-payment-providers]].
- **Toggle active** — hide/show at checkout without uninstalling.
- **Customer-facing title** override (e.g., rename "Pop" → "Pay at our store" or "Плати в магазина").
- **Logo override**.
- **Set a per-provider discount / fee** ([[discount]]).
- **From / To availability window** (e.g., only during shop hours).
- **Set min / max order value** via `min_price`.

There are NO API credentials, NO test mode, NO description-text field (the settings panel for `pop` is a minimal payment-provider settings shell — only logo / amount / discount rows are exposed).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Title** | Customer-facing label at checkout. | "Pop" / locale equivalent | Free text. Stored on the payment-provider configuration's `title` field. |
| **Logo** | Custom image displayed next to the title at checkout. | Stock storefront icon | Optional upload. |
| **Discount type** | Adds a fee or grants a discount when Pop is the chosen method. | none | Percent / flat. See [[discount]]. |
| **From / To** | Time window during which Pop is offered at checkout. | always | Common pattern: enable only during shop opening hours. |
| **Min price** | Minimum order amount required to offer Pop. | 0 | Stored in cents. |
| **Active** | Master switch — hides/shows Pop at checkout. | active after install | Same toggle as [[settings-payment-providers]]. |

There is **no Description field** on this provider's edit form (unlike COD / Voucher which DO have a TinyMCE description field) — the Pop edit template renders only the title/logo, from-to, and discount shared partials.

## Business rules

### Pop is an "offline" payment

Same model as [[payment-providers-cod]]:

- Order is created in `pending` state immediately at checkout.
- No money flows through CloudCart at checkout time.
- Merchant manually marks the order Paid when the customer arrives and pays in person.
- Pop is NOT included in CloudCart's "online payment" group — settings like "reserve stock only after successful online payment" don't apply.

### Purchase is a no-op

On purchase, the platform simply sets the payment row's status to `requested` and returns without any redirect or external call. No HTTP call. No webhook. No external integration.

### No validation rules

No required fields. The merchant can install Pop, save it with default settings, and start accepting it immediately.

### Customer experience at checkout

The customer:
1. Picks Pop at checkout.
2. Submits the order.
3. Sees the order-success page with whatever description/instructions the merchant has put in store-side communications (e.g., the order-confirmation email, or the [[apps]] custom thank-you-page hooks).
4. Walks into the merchant's physical store with the order number and pays in person.
5. Merchant looks up the order and marks it Paid.

### No customer instructions on the order-success page (unlike COD / Voucher)

Pop does NOT have the same TinyMCE "Description" field that [[payment-providers-cod]] and [[payment-providers-voucher]] have — so the order-success page does NOT show a Pop-specific instructions block automatically. The merchant should either:

- Customize their order-confirmation email to include in-store payment instructions for Pop orders.
- Use a [[apps]] custom-page integration.
- Add the instructions to the customer-facing title itself (limited space).

### Refund

Refunds are not supported through CloudCart. To refund a Pop order: cancel the order in CloudCart and physically refund the cash/card payment in-store using the merchant's POS system.

### No periodic status sync

There is nothing to sync — no external system holds payment status. Status is driven entirely by the merchant's manual "Mark as paid" action ([[orders-payment-mark-paid]]).

### Permission

Configuring Pop requires the `store.payment_providers` permission section.

### Cache + side effects

Saving Pop settings updates the payment-provider configuration row. No queued jobs. No webhook deliveries.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-cod]] — similar offline cash flow (cash-to-courier instead of cash-in-store).
- [[payment-providers-voucher]] — similar offline flow for gift card / voucher redemption.
- [[settings-payment-providers]] — install/uninstall and the master Active toggle.
- [[orders-payment-mark-paid]] — manual "Mark as paid" for in-store payments.
- [[orders-payment-manual]] — manually add a payment row.
- [[discount]] — per-provider fee/discount.
- [[checkout-flow]] — how Pop appears in the checkout payment-method list.
- [[payment-providers]] — the `payments` row gets `provider=pop`, advances `requested → completed` only when the merchant marks it Paid.

## How it works (verified against backend)

### Purchase — minimal

The purchase step sets the payment status to `requested` and returns without any redirect or external call. No external API. No signature. No webhook.

### Validator

The configuration validator is empty — no rules, no messages. Nothing to validate.

### Source description

The English source description is *"Your customers will be able to pay in some of your physical stores"*. This is the description shown in the Add-payment-method modal for the Pop card; it's NOT shown to customers.

### Settings panel

The Pop settings panel is a thin wrapper around the shared payment-provider settings shell, exposing only logo, amount, and discount rows. No mode toggle, no credentials.

## Open questions

_None._

## Verified — multi-store handling

There is no per-location Pop variant. The provider is a single, store-wide row; a merchant with multiple physical locations cannot configure different Pop rows per store. To distinguish between locations, the merchant relies on the order's pickup-store choice in [[settings-cart]] / shipping setup.
