---
type: feature
nav_path: "Apps → Withdraw from contract → Settings"
route_name: apps.aftercare.settings
route_path: /admin/apps/aftercare
aliases: ["Aftercare settings", "Aftercare setup", "withdrawal wizard", "aftercare onboarding", "withdrawal_window_days", "floating button withdrawal", "terms page", "return policy page", "aftercare 4-step wizard"]
tags: [apps, aftercare, settings, setup, orders, withdrawal]
plan_gates: ["aftercare_pro"]
created: 2026-07-24
updated: 2026-07-24
source_count: 1
---

> Part of [[apps-aftercare]]. See the hub for the other aspects (compliance, admin inbox, free-vs-Pro, storefront flow).

# Aftercare — setup & settings

## Purpose

The onboarding wizard and every setting: the storefront button, the Terms / Return-policy pages, the withdrawal window, and the notification channels.

## Where to find it

Sidebar → Apps → **Withdraw from contract** → Settings (`apps.aftercare.settings`), presented as a **4-step wizard**: **Install · Confirm the data · Set the rules · Activate**. `onboarding_step` tracks the furthest step the merchant has reached (step 1 = install done). The Settings tab shares one interface with the [[aftercare-withdrawals-admin|Withdrawals inbox]].

## What the merchant can do here

- Walk the 4-step wizard to go live: confirm store data, designate the Terms / Return-policy pages, set the rules, and activate.
- Enable and style the storefront button (or rely on a menu link), or — on Pro — point it at a custom page.
- Set the withdrawal window (≥ 14 days) and the notification channels.

## Settings & fields

| Field | Notes |
|---|---|
| `floating_button_enabled` | Show the storefront floating button (off by default — if left off, add the menu link instead). |
| `button_text` | Button label (≤ 255 chars); empty → the official translated Art. 11a wording is used. |
| `floating_position` | `left` / `right`. |
| `font_size` / `text_color` / `background_color` | Button styling. |
| `terms_page_id` / `return_policy_page_id` | The store CMS pages ([[page]]) shown as the withdrawal Terms / Return policy the customer must accept. |
| `withdrawal_window_days` | The withdrawal window in days — **required, 14–365** (14 = EU minimum). The clock starts on delivery — see [[aftercare-compliance]]. |
| `notify_email` | Customer email notifications — **locked on** (the Art. 11a acknowledgement must always send). |
| `auto_create_return` *(Pro)* | On each new withdrawal, auto-create a matching PENDING core order-return (on by default for Pro). |
| `use_custom_page` / `custom_page_id` *(Pro)* | Point the storefront button / menu link at one of your own CMS pages (carrying the withdrawal widget) instead of `/withdrawal`. |
| `notify_viber` *(Pro)* | Viber notification on withdrawal events. |
| `voucher_bonus_enabled` / `voucher_bonus_percent` *(Pro)* | A store-credit voucher (with a bonus %) as a refund alternative — **declared but not yet operational** in this release. |

## Business rules

- The window (`withdrawal_window_days`) is **required** and bounded **14–365** — 14 is the EU minimum and cannot be undercut (see [[aftercare-compliance]]).
- `notify_email` is **locked on** — the acknowledgement of receipt must always send; the toggle is forced on and `accepted`-validated.
- The Pro settings (`auto_create_return`, `use_custom_page`, `notify_viber`, `voucher_bonus_*`) stay disabled behind a "paid service / Buy here" prompt without the `aftercare_pro` plan feature — see [[aftercare-free-vs-pro]].

## Related

- [[apps-aftercare]] — hub.
- [[aftercare-compliance]] — why the window minimum is 14 days and starts on delivery.
- [[aftercare-free-vs-pro]] — the Pro-gated settings.
- [[storefront-withdrawal]] — where the button + Terms / Return-policy pages appear to the customer.
- [[page]] — the CMS pages designated as Terms / Return policy.

## Open questions

None.
