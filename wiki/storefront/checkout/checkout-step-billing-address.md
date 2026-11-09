---
type: storefront-page
nav_path: "Storefront → Checkout → Billing address"
route_name: checkout.billing.address
route_path: /checkout/billing-address
themes_using: [all]
aliases: ["Checkout billing address", "Billing address step", "Invoice address at checkout", "Use different billing address", "Адрес за фактура", "Адрес за фактуриране", "Използвай друг адрес за фактура", "Желая фактура", "Получател Име", "Булстат/ЕИК или ЕГН", "ИН по ЗДДС", "МОЛ на фирма"]
tags: [storefront, checkout, billing, invoice, address, company]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[checkout]]. The shipping address above it is on [[checkout-step-shipping-address]].

# Checkout — Billing address

## Purpose

The checkout step that collects the address the invoice is made out to: the recipient, the company details and the address. It is separate from the delivery address. Whether it appears is set on [[settings-cart-checkout-fields]].

## URL & route

The step is a section of `/checkout`. It loads from `checkout.billing.address` (`/checkout/billing-address`) and is saved through `checkout.billing.address.submit`. Container: `.js-checkout-billing-address`.

## How it loads

Two settings in **Settings → Cart and checkout** decide it:

| Don't ask for billing address | Require billing address on checkout | At checkout |
|---|---|---|
| On | (hidden) | No billing step, ever. |
| Off | Required | The step always shows, with no checkbox. |
| Off (default) | Not required (default) | Below the delivery address, a checkbox **Use different billing address** / **Използвай друг адрес за фактура**. Ticking it opens the step. |

Both settings are off and Not required on a store that never changed them. A cart with digital products only, with nothing to ship, always gets the step unless **Don't ask for billing address** is on. A wallet top-up or gift card purchase never gets it.

A store's checkbox may read differently, for example "Желая фактура": the storefront wording can be renamed in [[settings-translations]].

## What the customer sees

Heading **Billing address** / **Адрес за фактура**.

**A guest, or a customer with no saved billing address,** gets one form:

| English | Bulgarian |
|---|---|
| First name receiver | Получател Име |
| Last name receiver | Получател Фамилия |
| Phone | Телефонен номер |
| Company name | Име на фирма |
| Company registration number | Булстат/ЕИК или ЕГН |
| Tax or VAT number | ИН по ЗДДС |
| Company owner | МОЛ на фирма |
| Enter your address or postcode | Въведете улица и град за доставка |
| Save and continue | Запази и продължи напред |

The address search field appears when the store has a Google Maps key and fills in the address fields. Without a key, the customer types Country (Държава), State (Област), City (Населено място), Address (Улица), Street number (Номер), additional address information and Postcode (Пощенски код).

**A signed-in customer with saved billing addresses** sees them as a list. Their default billing address is selected. Each address has an **Edit** / **Редактирай** link, and **Add new address** / **Добави нов адрес** opens the form.

## Storefront behaviour

- **Nothing is copied from the delivery address.** The form starts empty, and there is no "same as delivery" option. Leaving the checkbox unticked means the order has no billing address.
- **The company fields follow the Company info box** on [[settings-cart-checkout-fields]]: each is required, optional or hidden. All four are **Required** until the merchant changes them, so by default the step asks for company name, registration number, VAT number and company owner.
- **Saving** stores the address on the customer. A guest's billing address replaces the one saved before. The step then collapses to a summary with a change link.
- The address the store uses for fees and taxes is set separately (`invoicing_address`).

### Invoices without a billing address

**Issue an invoice only if a billing address is selected** is on by default ([[settings-invoicing-activation-modes]]). While it is on, an order without a billing address gets no invoice, automatically or by hand. That covers orders where the step was hidden and orders where the customer left the checkbox unticked. The merchant first adds a billing address on the order ([[orders-address-edit]]). With the switch off, such an order is invoiced to its delivery address.

## JavaScript behaviour

The checkbox toggles the step's container. The forms post through the shared checkout hooks; see [[checkout-page-javascript]].

## Customisations available to the merchant

- **Settings → Cart and checkout**: the two switches above, the Company info box, and the name and phone fields ([[settings-cart-checkout-fields]]).
- The storefront wording ([[settings-translations]]).
- The Admin GraphQL API reads the two switches as `hideBillingAddress` and `requireBillingAddress`, and the invoice switch as `billingInvoicing`.

## Theme variations

The step comes from the global checkout templates, so every theme shows the same form.

## Known issues / by-design vs bug

- **"The address is asked again"** when the customer wants an invoice: by design. The billing address is a second address, and nothing is filled in from delivery.
- **"Company fields required for a private customer"**: the default. The merchant sets each one to optional or hidden.
- **"No invoice for the order"**: the order has no billing address while the invoice switch is on.

## Related

- [[checkout]] — hub.
- [[checkout-step-shipping-address]] — the delivery address and the checkbox below it.
- [[settings-cart-checkout-fields]] — the switches and the company fields.
- [[settings-invoicing-activation-modes]] — the invoice switch.
- [[orders-address-edit]] — adding a billing address to an order.
- [[customer-addresses]] — the customer's saved addresses.
- [[settings-translations]] — renaming storefront wording.

## Open questions

- The Bulgarian labels of the two switches and of the invoice switch: the admin's translations are stored outside the code.
