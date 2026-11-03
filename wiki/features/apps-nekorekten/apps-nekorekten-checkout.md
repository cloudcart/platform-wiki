---
type: feature
nav_path: "Apps → Nekorekten → Settings → Orders → Cash on delivery at checkout"
route_name: apps.nekorekten.settings
route_path: /admin/apps/nekorekten/settings
aliases: ["Cash on delivery at checkout", "COD hidden for a customer", "cash on delivery missing for one customer", "Hide it from blocked and reported customers", "Hide it only from customers on my blocked list", "Always show it — only warn me on the order", "stop hiding cash on delivery", "наложен платеж не се показва", "скрит наложен платеж", "клиент не вижда наложен платеж", "Некоректен каса"]
tags: [apps, nekorekten, checkout, cod, payment-methods]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 6
---

# Nekorekten — Cash on delivery at checkout

> Part of [[apps-nekorekten]]. See the hub for the other aspects (settings, order check, lists, plan limits).

## Purpose

Whether a flagged buyer can still choose **Cash on delivery** (Наложен платеж) at checkout. Screening and hiding are two separate decisions: the order is checked and the verdict is shown either way, and this one setting decides what the verdict costs the buyer at checkout.

## Where to find it

**Apps → Nekorekten → Settings → Orders → Cash on delivery at checkout**. Its effect is on the storefront's payment step ([[checkout-step-payment]]).

## What the merchant can do here

- Hide cash on delivery from buyers who are blocked **or** reported on nekorekten.com (the default).
- Hide it only from buyers on the store's own blocked list.
- Never hide it, and rely on the warning on the order.

## Settings & fields

**Cash on delivery at checkout** (`cod_at_checkout`). Tooltip: *"Whether a flagged customer loses "Cash on delivery" at checkout. Orders are checked and the risk is shown on the order either way."*

| Option | Value | Who loses cash on delivery |
|---|---|---|
| **Hide it from blocked and reported customers** (default) | `hide_all` | Buyers on the blocked list, and buyers with **one or more** reports on nekorekten.com. |
| **Hide it only from customers on my blocked list** | `hide_blocked` | Only buyers on the blocked list. Reported buyers keep it; their orders still show **High risk**. |
| **Always show it — only warn me on the order** | `show` | Nobody. Blocked and reported buyers are only flagged on their orders. |

The field cannot be cleared. A store that never opened it behaves as **Hide it from blocked and reported customers**.

## Business rules

### Only cash on delivery is touched

The app removes the store's **Cash on delivery** method and nothing else. It acts last, after the platform's own rules (minimum order, category restrictions, courier support). If cash on delivery was not going to be offered anyway, the app does nothing. See [[payment-providers-cod]].

### When the buyer is checked

As soon as the shopper has given a phone or an e-mail, the payment step checks them. The phone is taken from the shipping address, or from the billing address when there is none. The check runs each time the payment step is redrawn — after an address or shipping change — and again when the order is placed. Before the shopper gives any contact, nothing is checked.

The buyer is judged in a fixed order — whitelist, blocked list, a lookup from the last 7 days, then nekorekten.com ([[apps-nekorekten]]). A whitelisted contact always keeps cash on delivery, even if it is also on the blocked list.

### Nothing to see for the shopper

Cash on delivery simply is not in the list of payment methods. There is no message and no explanation. If the method is submitted anyway — for example from a page opened before the check — the order is refused with a checkout error instead of being placed.

### An unanswered check never hides anything

A buyer who could not be checked is **Not checked**, and Not checked never loses cash on delivery under any option. That covers: no API key, a refused key, a spent plan, the app's per-minute limit, nekorekten.com being slow or unreachable, or any error inside the app. If the check itself fails, the shopper keeps every payment method.

### The blocked list works without an account

Hiding from blocked buyers needs no nekorekten.com key, only an **enabled** app. With no key, reports cannot be read, so under the default option only the blocked list has any effect.

### What it costs from the nekorekten.com plan

A buyer not on either list and not looked up in the last 7 days costs one lookup. That happens at the payment step, also for shoppers who never finish the order. The order check afterwards reuses that answer.

- **Hide it only from customers on my blocked list** still looks new buyers up, because the check is the same; it only ignores the answer when deciding.
- **Always show it** makes no lookups at checkout at all. The order check still spends lookups on new cash-on-delivery orders.

A first-time buyer's lookup happens while the payment step loads. The app waits up to **8 seconds** for nekorekten.com before giving up and leaving cash on delivery in place.

### A 7-day memory

A lookup is reused for 7 days. A buyer reported on nekorekten.com after being looked up keeps cash on delivery until the 7 days pass, unless the merchant presses **Check again** on one of their orders ([[apps-nekorekten-order-check]]), which refreshes the stored answer.

### What this setting does not affect

- **Automatic blocking by status** only decides who goes on the blocked list. **No automatic blocking** does not mean "hide from nobody" — that is **Always show it**.
- **Check every new cash-on-delivery order** is independent: switching it off stops the order verdicts, not the hiding.
- The **Fast Order** app's one-step form ([[apps-fast-order]]) places cash-on-delivery orders without going through this payment step, so a blocked or reported buyer can still order through it. That order is still checked afterwards.

### Counted in Activity

Each buyer checked at checkout is counted once per cart within an hour, and counted as blocked when cash on delivery was hidden — see [[apps-nekorekten-activity]]. Under **Always show it** nothing is counted.

## Related

- [[apps-nekorekten]] — hub.
- [[checkout-step-payment]] — the storefront step where the method disappears.
- [[payment-providers-cod]] — the Cash on delivery method itself.
- [[apps-nekorekten-blocklist]] — what puts a buyer on the blocked list.
- [[apps-nekorekten-whitelist]] — contacts that always keep cash on delivery.
- [[apps-nekorekten-quota]] — why a buyer may be Not checked.

## Open questions

- The exact wording of the checkout error a shopper gets when cash on delivery is refused at submit (verify on a live store).
