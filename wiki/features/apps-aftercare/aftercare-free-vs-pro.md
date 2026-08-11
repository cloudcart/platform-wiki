---
type: feature
nav_path: "Apps → Withdraw from contract → Free vs Pro"
route_name: ""
route_path: ""
aliases: ["Aftercare Pro", "aftercare_pro", "Aftercare free vs pro", "withdrawal webhooks", "auto_create_return", "voucher bonus", "block_resubmit", "aftercare deferred", "withdrawal card refund", "withdrawal countdown"]
tags: [apps, aftercare, plan-gates, pro, withdrawal]
plan_gates: ["aftercare_pro"]
created: 2026-07-24
updated: 2026-07-31
source_count: 1
---

> Part of [[apps-aftercare]]. See the hub for the other aspects (compliance, admin inbox, settings, storefront flow).

# Aftercare — free compliance core vs paid Pro

## Purpose

What every plan gets (the legal minimum) vs what the paid **`aftercare_pro`** feature adds — and which Pro options are declared in the data model but not yet operational.

## Where to find it

The `aftercare_pro` feature is bought from the plan / feature-pack prompt shown on the app's **Settings** wizard ([[aftercare-settings-setup]]); the Pro-only fields there stay disabled behind a "paid service / Buy here" box until it is active.

## What the merchant can do here

Decide whether the free compliance core is enough, or whether the Pro automation / retention extras are worth the feature pack — the split below is the whole decision.

## Settings & fields

The Pro-gated settings themselves (`auto_create_return`, `use_custom_page` / `custom_page_id`, `notify_viber`, `voucher_bonus_*`) are documented on [[aftercare-settings-setup]]; this page explains what each tier includes.

## Business rules

### At a glance — what is free vs paid

| Capability | Free (any plan) | Pro (`aftercare_pro`, paid) |
|---|---|---|
| Storefront withdrawal function (button / form, guest, email verification) | ✅ | ✅ |
| Acknowledgement email + terms snapshot + 14-day window | ✅ | ✅ |
| Admin inbox + `pending → returned / cancelled` lifecycle | ✅ | ✅ |
| `withdrawal` resolution + **bank** refund (recorded, paid out manually) | ✅ | ✅ |
| My-account withdrawal-history list | ✅ | ✅ |
| Auto-create a core order-return (`auto_create_return`) | ❌ | ✅ |
| Refund **to card** offered in the flow (via the core return) | ❌ | ✅ |
| **Viber** notifications (`notify_viber`) | ❌ | ✅ |
| **Custom-page** button (`use_custom_page`) | ❌ | ✅ |
| **Webhook** events | ❌ | ✅ |
| In-account **live countdown** + `/withdrawal/order` one-click shortcut | ❌ | ✅ |
| `block_resubmit` (lock lines after a cancel) | ❌ | ✅ |
| `cancel` resolution for a whole not-yet-shipped order | ❌ | ✅ |
| Store-credit **voucher** / **exchange** / **wallet** refunds | — declared, **not yet operational** — | |

`aftercare_pro` is a **paid plan feature**, sold as a monthly / yearly feature pack (bought from the app's Settings wizard — see [[aftercare-settings-setup]]). Without it, the Pro rows above stay disabled behind a "paid service / Buy here" prompt.

### Free compliance core (any plan)

The **free core** works on any plan — the legal minimum every EU store must offer:

- the storefront withdrawal button + form ([[storefront-withdrawal]]), **guest-accessible**, with email-code verification;
- the always-on **acknowledgement of receipt** and the **terms snapshot** ([[aftercare-compliance]]);
- the **14-day (or longer) window**, counted from delivery;
- the admin inbox with the `pending → returned / cancelled` lifecycle ([[aftercare-withdrawals-admin]]);
- the `withdrawal` resolution and **bank-transfer** refunds.

### Aftercare Pro (`aftercare_pro`)

Sold as a monthly / yearly feature pack. It adds:

- **`auto_create_return`** — every new withdrawal auto-creates a matching PENDING **core order-return** (for a committed order, once only), which then **drives the request's status** and carries the customer's refund choice into the store's normal returns / restock / refund flow. This is the biggest Pro behaviour — see [[aftercare-order-return-sync]].
- **Refund to card** — when the order was paid by a supporting online card gateway, the customer can pick a card refund instead of bank transfer. It is executed from the core return's refund button — **full or partial** — via the gateway; partial refunds are live for **Stripe / PayPal / Revolut / CloudCart Pay** (others are full-only or bank-only). Card is offered **per scope**: the option only shows on the scope the gateway supports. See [[aftercare-order-return-sync]].
- **`notify_viber`** — Viber messages on withdrawal events. Unlike email (2 status mails), Viber sends **three**: a `pending` *"request received"* message on creation (the Viber counterpart of the email acknowledgement, since there is no separate Viber acknowledgement) plus `returned` / `cancelled` on the status change — each a plain-text message with an inlined tracking link. Email stays the free, always-on channel.
- A **custom-page button** (`use_custom_page` / `custom_page_id`) — point the storefront button / menu link at one of your own pages carrying the withdrawal widget, instead of `/withdrawal`.
- **Webhook events** — `withdrawal.created` and `withdrawal.status_changed`, wired at `/settings/hooks` like any core event; the payload carries the order, customer, status, resolution, the refund choice, the withdrawn products (with VAT-aware totals), and the window dates.
- A **live withdrawal countdown + one-click CTA** on the logged-in customer's account (`/account/withdrawals`) and order pages, plus a **`/withdrawal/order/{hash}` shortcut** that — for the order's logged-in owner, while the window is open — **skips the order-lookup and email-verification** (the login already proves ownership) and drops them straight into the item picker. The standalone `/withdrawal` guest form (with verification) stays free.
- **`block_resubmit`** — after a request is `cancelled`, keep its lines locked so the customer cannot re-open a withdrawal for them (by default a cancel frees the lines for re-submission).
- The **`cancel`** resolution for whole, not-yet-shipped orders.

### Declared but not yet operational

These exist as data-model / setting placeholders but are not functional in this release — treat them as roadmap, not current behaviour:

- store-credit **vouchers** (including the `voucher_bonus_*` setting);
- **exchange** resolutions;
- **wallet** refunds;
- the **automated card-gateway** refund (Pro currently records the customer's card choice for the merchant to execute manually).

## Related

- [[apps-aftercare]] — hub.
- [[aftercare-withdrawals-admin]] — where the Pro resolution / refund options and `block_resubmit` appear.
- [[aftercare-settings-setup]] — the Pro-gated settings.
- [[plan-features]] / [[plan-gates]] — how the `aftercare_pro` feature is sold.

## Open questions

None.
