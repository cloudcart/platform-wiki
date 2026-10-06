---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Settings → Apple Pay domain"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["CloudCart Pay Apple Pay domain", "Apple Pay not showing", "Apple Pay domain registration", "Register domain Apple Pay", "Apple could not verify the domain", "Домейн за Apple Pay", "Apple Pay не се показва", "Регистриране на домейн"]
tags: [paymentproviders, payment-providers, cloudcart-pay, apple-pay, domains]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, activation gate, checkout flow, express checkout, refunds, saved card) and the six tabs.

# CloudCart Pay — Apple Pay domain

## Purpose

Apple Pay appears at checkout only on a store domain that is **registered for Apple Pay**. This page covers the **Apple Pay domain** card on the Settings tab, what its status means, how registration happens automatically or by hand, and why another provider's Apple Pay can block it. It is the page for "Apple Pay doesn't show on my store".

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
| Button | **Register domain** (Регистриране на домейн), or **Re-register** (Повторна регистрация) when already registered. | After a click the card shows the new status straight away. |

Error messages the button can show: *"No connected account"* and *"The store has no primary domain"*.

## Business rules

### "Registered" means usable by Apple Pay

The badge reads **Registered** only when the domain is switched on for the account and Apple Pay is active for it. A registration that was sent but rejected by Apple stays **Not registered**, with Apple's reason under it.

### Automatic registration

When a shopper starts a payment in the **popup** card form, the system checks whether the domain the shopper is on is registered and, if not, registers it in the background. It tries at most once an hour per domain and never holds up the payment. The inline card form (the default) does not trigger this check, so with inline checkout the **Register domain** button is the way to register.

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
- [[cloudcart-pay-express-checkout]] — Apple Pay on product pages.
- [[settings-domains]] — the store's domains.
- [[payment-providers-revolut]] — Revolut's Apple Pay, which takes precedence on the domain.
- [[payment-providers-paypal-acdc]] — PayPal advanced card payments' Apple Pay.

## Open questions

- Whether CloudCart registers every CloudCart Pay store's domain in bulk (an operator tool for this exists); with inline checkout the automatic check at payment time does not run.
