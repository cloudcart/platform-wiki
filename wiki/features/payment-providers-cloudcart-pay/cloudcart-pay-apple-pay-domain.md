---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Settings → Apple Pay domain"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["CloudCart Pay Apple Pay domain", "Apple Pay not showing", "Apple Pay domain registration", "Register domain Apple Pay", "Apple could not verify the domain", "Домейн за Apple Pay", "Apple Pay не се показва", "Регистриране на домейн"]
tags: [paymentproviders, payment-providers, cloudcart-pay, apple-pay, domains]
plan_gates: []
created: 2026-10-06
updated: 2026-11-03
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, activation gate, checkout flow, express checkout, refunds, saved card) and the six tabs.

# CloudCart Pay — Apple Pay domain

## Purpose

Apple Pay appears on the store only on a domain that Apple has **verified**. This page covers the **Apple Pay domain** card on the Settings tab, what its status means, how registration happens automatically or by hand, the lock on the **Apple Pay** switch, and why another provider's Apple Pay can block it. It is the page for "Apple Pay doesn't show on my store".

## Where to find it

Settings → Payment methods → CloudCart Pay → **Settings** tab → the **Apple Pay domain** card (Домейн за Apple Pay), below the connected account. The card appears once the store has a connected account.

## What the merchant can do here

- **See the store's domain** and whether it is registered for Apple Pay.
- **Read Apple's reason** when Apple rejected the domain.
- **Register the domain**, or **register it again**.

## Settings & fields

| Element | What it shows or does | Notes |
|---|---|---|
| Domain | The store's primary domain. | Taken from the store's domains — see [[settings-domains]]. |
| Status badge | **Registered** (Регистриран) or **Not registered** (Не е регистриран). | Read live each time the tab opens. |
| Message when not registered | *"Apple Pay will not be shown at checkout until the store domain is registered."* (Apple Pay няма да се показва при плащане, докато домейнът на магазина не бъде регистриран.) | Replaced by Apple's reason when Apple rejected the domain. |
| Apple's reason | *"Apple could not verify the domain:"* followed by Apple's explanation. | Shown when a registration was sent but Apple did not accept the domain. |
| Button | **Register domain** (Регистриране на домейн), or **Re-register** (Повторна регистрация) when already registered. | After a click the card shows the new status straight away. Disabled until the account is active. |
| Hint when the account is not active | *"The Apple Pay domain can be registered once your CloudCart Pay account is active. Complete the onboarding and wait for the account review to finish."* | Active means payments enabled on the account. A registration attempt on an inactive account is refused with the same hint. |

Error messages the button can show: *"No connected account"* and *"The store has no primary domain"*.

## Business rules

### "Registered" means usable by Apple Pay

The badge reads **Registered** only when the domain is switched on for the account and Apple Pay is active for it. A registration that was sent but rejected by Apple stays **Not registered**, with Apple's reason under it.

### Hidden until verified

On the inline card form, the popup and the express buttons, Apple Pay is left out while the domain is not verified, because the button would only fail after the shopper taps it. If the status cannot be read (provider unreachable), the button stays, so an outage does not hide a working wallet. The separate payment page does not depend on the store's domain ([[cloudcart-pay-hosted-page]]).

### Automatic registration

A storefront domain with no registration is registered on the way, at most once an hour per domain, without holding up the page. The button comes back on its own after Apple accepts, within about an hour.

### The Apple Pay switch is locked while not verified

While the domain is not verified, the **Apple Pay** switch in **Digital wallets** cannot be turned on if it is off. A switch already on, or never saved (which means on), can still be turned off, and other settings still save. If the status cannot be read, the change goes through. The message, under the switch and on a refused save: *"Apple Pay can be turned on once Apple has verified the store domain. Register it in the Apple Pay domain section."* The lock applies whichever card form display is chosen.

### The verification file is served automatically

Apple checks a verification file on the store's domain. CloudCart serves it on every storefront domain automatically, also while the store is in maintenance or expired. The merchant does not upload anything.

### One Apple Pay provider per domain

A domain can carry only one provider's Apple Pay verification file. When **Revolut** is active with its Apple Pay option on, its file is served; otherwise **PayPal** advanced card payments with Apple Pay on; only when neither is, CloudCart Pay's. A store that runs Apple Pay through one of those providers therefore cannot verify the same domain for CloudCart Pay at the same time. See [[payment-providers-revolut]] and [[payment-providers-paypal-acdc]].

### After changing the primary domain

Registration is for the primary domain shown on the card. After the store's primary domain changes, the card shows the new domain; if it reads **Not registered**, click **Register domain**.

### Apple Pay also needs the wallet switched on

The **Apple Pay** switch in the **Digital wallets** box must be on, and the shopper must use a device and browser that support Apple Pay. See [[payment-providers-cloudcart-pay-settings]].

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-settings]] — the Settings tab that holds this card.
- [[cloudcart-pay-checkout-flow]] — where Apple Pay appears at checkout.
- [[cloudcart-pay-express-checkout]] — Apple Pay express buttons.
- [[cloudcart-pay-hosted-page]] — the payment page, which needs no verification of the store domain.
- [[settings-domains]] — the store's domains.
- [[payment-providers-revolut]] — Revolut's Apple Pay, which takes precedence on the domain.
- [[payment-providers-paypal-acdc]] — PayPal advanced card payments' Apple Pay.

## Open questions

- Whether CloudCart registers every CloudCart Pay store's domain in bulk (an operator tool for this exists).
