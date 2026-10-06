---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Settings → Save customer card"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["CloudCart Pay save card", "CloudCart Pay saved card", "CloudCart Pay save customer card", "CloudCart Pay stored card", "Manage saved cards", "Запазване на картата на клиента", "Управление на запазените карти", "Запазени карти CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, saved-cards]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, activation gate, checkout flow, express checkout, Apple Pay domain, refunds) and the six tabs.

# CloudCart Pay — saved card

## Purpose

The *Save customer card* setting: who can save a card, how a saved card is chosen and removed at checkout, how subscriptions use it, and why a saved card can disappear after the store changes its CloudCart Pay account. It is the page for "can my customers save their card?" and "why is a saved card gone?".

## Where to find it

Settings → Payment methods → CloudCart Pay → **Settings** tab → **Save customer card** box (Запазване на картата на клиента) → **Save Customer Card** switch. The behaviour happens on the storefront checkout (see [[cloudcart-pay-checkout-flow]]).

## What the merchant can do here

- **Turn card saving on or off** with one switch.
- **Let signed-in customers pay with a card they saved before**, and remove saved cards themselves.

## Settings & fields

| Field | What it does | Default | Notes |
|---|---|---|---|
| **Save Customer Card** | Lets signed-in customers save their card at checkout and reuse it later. | **On** | Box help text: *"Enable saving customer cards for future purchases"* (Разрешете запазването на картите на клиентите за бъдещи покупки). One switch for both environments. |

A store that has never saved this setting behaves as if it were on.

## Business rules

### Signed-in customers only

Saving works only for customers signed in to their account. A guest checkout never saves a card, whatever the switch says.

When the switch is on, the card form lets a signed-in customer save the card while paying. A card saved this way can also be charged later without the customer present, which is what subscription renewals need.

### Paying with and removing a saved card

The saved cards are kept by CloudCart Pay; the store keeps only the link to the customer. They are listed live at checkout.

- **Inline card form (default):** saved cards are offered inside the card form. Below it, **Manage saved cards** (Управление на запазените карти) opens the list of cards, each with **Delete**. After a card is deleted the form reloads without it.
- **Popup window:** the payment step shows the saved cards with the texts *"You can remove a saved card from this list at any time."* and *"The card to pay with is selected after clicking the complete order button."*, each card with **Delete**. The card itself is picked inside the popup.

Deleting asks for confirmation and removes the card at CloudCart Pay. A customer can delete only their own cards.

### Subscriptions always save the card

When the basket holds a product sold on a subscription (see [[apps-subscriptions]]), the card is saved even if **Save Customer Card** is off, because each renewal is charged to that card without the customer. The customer is not offered a choice in that case. CloudCart Pay can therefore back subscription plans.

A renewal is charged to the specific card used for the subscription. If that card is no longer on the customer's account, the renewal fails with *"The saved card for this subscription is no longer available."*

### After changing the CloudCart Pay account

Saved cards belong to the connected account they were saved under. If the store disconnects and links another account (see [[ccpay-onboarding-connect-disconnect]]), the earlier saved cards are no longer offered. At the customer's next checkout a fresh customer record is created on the new account, so checkout works without an error; the customer simply enters the card again.

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-settings]] — the Settings tab that holds the switch.
- [[cloudcart-pay-checkout-flow]] — inline and popup card forms.
- [[apps-subscriptions]] — subscriptions charged to the saved card.
- [[ccpay-onboarding-connect-disconnect]] — changing the connected account.
- [[customer]] — the customer record the saved card is linked to.

## Open questions

- Whether a customer can see or remove CloudCart Pay saved cards from their storefront account page as well as at checkout.
