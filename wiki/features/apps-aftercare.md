---
type: feature
nav_path: "Apps → Withdraw from contract"
route_name: apps.aftercare.overview
route_path: /admin/apps/aftercare
aliases: ["Withdraw from contract", "Withdrawal from contract", "Отказ от договора", "Отказ от договор", "Right of withdrawal", "EU withdrawal button", "Aftercare", "Aftercare Pro", "withdrawal request", "online withdrawal statement", "Directive 2023/2673", "electronic withdrawal function", "Article 11a", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, compliance, eu, withdrawal, returns, orders, beta]
plan_gates: ["aftercare_pro"]
created: 2026-06-24
updated: 2026-08-06
source_count: 2
---
# Withdraw from contract (Aftercare)

## Purpose

**Withdraw from contract** (app key `aftercare`; Bulgarian *"Отказ от договора"*) is the compliance app that gives a store the **electronic withdrawal function** required of online sellers to EU consumers by **Directive (EU) 2023/2673, Art. 11a** — in force from **19 June 2026**. It provides the prominent "withdraw from contract" button + form the law requires, an admin inbox to receive and resolve the requests, and the legal record (acknowledgement, audit trail, terms snapshot) the directive expects.

The **free core** covers the legal requirement in full; a paid **`aftercare_pro`** tier adds automation and retention extras — see [[aftercare-free-vs-pro]]. This is a navigation hub; each aspect below is on its own page.

> **On/off control appears only once the setup wizard is completed.** While onboarding is unfinished the settings tab is labelled **Onboarding** and the app screen shows no **Enable / Disable** button and no enabled / disabled indicator — a missing button is not a fault. Work through the remaining onboarding steps; the button appears once the last step is done.

## Where to find it

- **Install + configure:** Sidebar → Apps → install **Withdraw from contract**, then run the 4-step setup wizard — see [[aftercare-settings-setup]].
- **The requests inbox:** Sidebar → **Orders → Withdraw from contract** (`orders.aftercare.list`, `/admin/orders/aftercare`) — see [[aftercare-withdrawals-admin]].
- **On the storefront:** a floating button + optional menu link opening the withdrawal flow at `/withdrawal` — see [[storefront-withdrawal]].

## Sub-pages (in this cluster)

- [[aftercare-compliance]] — the legal basis (Directives 2023/2673 + 2011/83/EU), the **delivery-based** 14-day window, the exemptions the app does *not* model, and the evidence it captures (acknowledgement, terms snapshot, audit trail).
- [[aftercare-withdrawals-admin]] — the admin inbox: the withdrawals list / detail, the `pending → returned / cancelled` lifecycle, resolution types, refund method + scope, the credit-note relationship, and the emails the app sends.
- [[aftercare-settings-setup]] — the 4-step setup wizard and every setting: the withdrawal window, the Terms / Return-policy pages, the storefront button, and notification channels.
- [[aftercare-free-vs-pro]] — what the free compliance core covers vs what the paid `aftercare_pro` feature unlocks (and which Pro options are declared but not yet operational).
- [[aftercare-order-return-sync]] — (Pro) how `auto_create_return` mirrors a withdrawal into a core order-return that then drives its status, refund, and restock.
- [[aftercare-scenarios]] — worked return **cases + action sequences** (partial / whole-order / before-after delivery / refund routing / resubmission), the `allow_return` prerequisite, and what the app does **not** do (return shipping, credit note, restock on free).
- [[storefront-withdrawal]] — the customer-facing `/withdrawal` page: the step-by-step form, email verification, item picker, and tracking.

## What the merchant can do here

- Give customers a compliant, always-available way to start a withdrawal — see [[storefront-withdrawal]].
- Receive and resolve requests (`pending → returned / cancelled`) and record the refund — see [[aftercare-withdrawals-admin]].
- Configure the window, the Terms / Return-policy pages, and the button — see [[aftercare-settings-setup]].
- Meet the directive's evidence requirements automatically — see [[aftercare-compliance]].
- On Pro: auto-create core returns, refund to card, send Viber updates, a custom-page button, and webhooks — see [[aftercare-free-vs-pro]].

## Settings & fields

The full settings reference — the storefront button, the Terms / Return-policy pages, the withdrawal window (`withdrawal_window_days`), and the notification channels — lives on [[aftercare-settings-setup]]. The `aftercare_pro`-gated settings are catalogued on [[aftercare-free-vs-pro]].

## Business rules

- **Two things are legally locked and cannot be turned off**: guest access to the withdrawal function, and the email **acknowledgement of receipt** on every new request (both Art. 11a requirements). See [[aftercare-compliance]].
- **The window defaults to 14 days** (`withdrawal_window_days`) — the legal minimum; the merchant may extend (14–365) but not shorten it, and the clock starts on **delivery** — see [[aftercare-compliance]].
- **A reason is never mandatory** — the right of withdrawal needs no justification.
- Installing the app creates its per-site withdrawal tables and seeds the acknowledgement email template; uninstalling drops them.
- Newly released app (flagged **beta**), in the compliance / administration category alongside [[apps-n18-audit|Наредба Н-18 audit]] and the BGN→EUR tools.

## Related

- [[apps]] — App Store hub.
- [[orders]] — Orders admin area (where the inbox lives).
- [[orders-details]] — the order a withdrawal references; credit notes / refunds surface here.
- [[page]] — the CMS pages used as the withdrawal Terms / Return policy.
- [[plan-features]] / [[plan-gates]] — the `aftercare_pro` paid tier.
- [[apps-gdpr-overview]] — sibling EU-compliance app.

## Open questions

None — the deferred features (vouchers / exchange / wallet / automated card refund) are tracked on [[aftercare-free-vs-pro]].
