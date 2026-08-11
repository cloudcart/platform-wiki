---
type: feature
nav_path: "Marketing → Channels → Email notifications → Toggles & gating"
route_name: marketing-mails-list
route_path: /admin/marketing-new/omnichannel/mails/list
aliases: ["customer_email_notifications", "Send notifications to customers", "Per-mail Active flag", "Forced-on mail labels", "Customer notification kill switch", "Имейл известия глобален превключвател"]
tags: [marketing, omnichannel, email, notifications, gating, toggles]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-omnichannel-mails-list]]. See the hub for related aspects (mail labels, editor modal, variables, abandoned-cart, customisation limits).

# Email notifications — toggles & gating

## Purpose

Two layers of on/off control gate every customer-mail send. This page documents the **global "Send notifications to customers" toggle**, the **per-mail Active flag**, the three **forced-on** labels (security/auth critical), and the exact send-gate point in the pipeline.

## Where to find it

The global toggle sits in the page header at `/admin/marketing-new/omnichannel/mails/list`, labelled **"Send notifications to customers"** (BG **"Изпращай известия до клиенти"**).

The per-mail Active flag is **NOT** surfaced as a column on the modern Vue list — it's a legacy-admin field that survives on the `Mail` model.

## What the merchant can do here

- Toggle the global switch ON/OFF in the page header (single click).
- The list page does **not** expose the per-mail Active flag — to flip a specific event off without disabling everything, a developer or CloudCart staff must edit it in legacy admin (verify).

## Settings & fields

### Page-level toggle

| Field | Setting key | Default | Effect when OFF |
|-------|-------------|---------|-----------------|
| **Send notifications to customers** | `customer_email_notifications` | `yes` | Stops the platform from sending **any** customer email notification, including security-critical ones |

Persisted via `POST /admin/api/core/marketing/customer-mails-settings` with body `{customer_email_notifications: true/false}`. The backend translates the boolean to the string `'yes'` / `'no'` in the central platform settings table (one row per `(site_id, parameter)`). Other workers / queues pick up the new value on their next setting fetch.

### Per-mail Active flag

| Field | Source | Default | Effect when 0 |
|---|---|---|---|
| the platform code | One integer column on the `Mail` row | `1` | Skips ONLY that label's sends — other labels still fire |

### Forced-on labels (cannot be disabled via per-mail Active)

The labels `two_factor_action`, `email_confirmation`, and `alert_notification` are forced-on regardless of the per-mail Active flag. In the legacy admin notifications page they appear with `checked="checked" disabled="disabled"`. These are security / auth-critical:

| Label | Why forced-on |
|---|---|
| `email_confirmation` | Account-creation flow depends on the verification link |
| `two_factor_action` | 2FA action notifications |
| `alert_notification` | Critical platform alerts |

**The global toggle still suppresses these three labels.** Turning OFF the global switch is a complete kill switch — even forced-on security mail is blocked. Merchants should NEVER leave the global switch OFF in production: they will silently block their own customers from verifying email and completing 2FA flows.

## Business rules

### Two layers of gating at send time

Every transactional mail dispatch checks **both**:

1. Global `customer_email_notifications == 'yes'` (store-wide).
2. Per-mail the platform code (per-label), **except** for the three forced-on labels which bypass step 2.

Both checks happen inside `sendNotification` of the customer-notification helper — every label flows through this single helper, gated by an internal `check_notifications_enabled` flag (default `true`). There is no production code path that sets this flag to `false`, so the global switch really does block every customer-mail send including password reset (verify).

### The toggle is independent of campaigns

Campaign delivery (see [[marketing-campaigns]]) is governed by **Channels activation state** ([[marketing-channels-email]]) and the per-campaign Active flag — NOT by `customer_email_notifications`. Turning OFF the customer-mail toggle does NOT pause running campaigns; conversely, deactivating the Email channel does NOT block transactional mail. The two systems are wired independently.

### Surprise silent-event scenario

A merchant on the Vue page who turns ON the global switch may still find specific events silent. Why: a previous legacy-admin edit set the platform code for a label, and the modern Vue UI doesn't surface that flag. The diagnostic is: confirm in legacy admin (or via direct DB read) that the affected `(site_id, label)` row has `active = 1`.

### Holiday / migration use case

The intended use of the global toggle: temporary silence during data migration, testing, or holiday closures where the merchant doesn't want order-confirmation emails going out (e.g., orders accepted but fulfilment paused). Production stores should toggle this OFF only briefly.

### Setting persistence uses the singleton store-settings table

`POST.../customer-mails-settings` writes via `setting->set(['customer_email_notifications' => 'yes'/'no'])->save`. The in-memory cache refreshes for the current request only; other workers / queues read the new value on their next setting fetch. There can be a brief window where in-flight notifications still see the old value.

### Recommended use

- **Don't toggle OFF in production.** Customers think their order failed; password resets break.
- **Use the per-mail Active flag (legacy admin) for surgical silence** — e.g., disable `customer_newsletter_subscribe` confirmation if the merchant doesn't want subscribe confirmations.
- **The forced-on labels exist for a reason** — never try to suppress 2FA / email-confirmation; that would brick account flows.

## Related

- [[marketing-omnichannel-mails-list]] — hub.
- [[omnichannel-mails-labels]] — the catalogue of labels each toggle covers.
- [[settings-statuses]] — the order-status taxonomy. There is no per-status notification toggle; order-status mails are gated by the order's Notify-customer flag, the mail's own Active flag and the store-wide customer-email setting.
- [[settings-admin-notifications]] — analogue switches for merchant-facing notifications, not customer mails.
- [[notification-delivery]] — platform-wide outbound notification mechanism.
- [[marketing-channels-email]] — channel activation that gates campaign delivery (independent system).
- [[marketing-campaigns]] — campaign gating contrast.

## Open questions

- 📡 **Surfacing per-mail Active on the Vue list.** The legacy field is hidden from the modern UI — merchants cannot self-serve per-label silence. Whether a future Vue iteration will expose it (verify roadmap).
- 📡 **Cache invalidation across worker pools.** The exact propagation lag for `customer_email_notifications` flips across queue workers needs measurement (verify).
