---
type: feature
nav_path: "Marketing → Channels → Email notifications → Toggles & gating"
route_name: marketing-mails-list
route_path: /admin/marketing/omnichannel/mails/list
aliases: ["customer_email_notifications", "Send notifications to customers", "Per-mail Active flag", "Forced-on mail labels", "Customer notification kill switch", "Имейл известия глобален превключвател"]
tags: [marketing, omnichannel, email, notifications, gating, toggles]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[marketing-omnichannel-mails-list]]. See the hub for related aspects (mail labels, editor modal, variables, abandoned-cart, customisation limits).

# Email notifications — toggles & gating

## Purpose

Two layers of on/off control gate every customer-mail send. This page documents the **global "Send notifications to customers" toggle**, the **per-mail Active flag**, the **locked** (forced-on) mails, and the exact send-gate point in the pipeline.

## Where to find it

The global toggle sits in the page header at `/admin/marketing/omnichannel/mails/list`, labelled **"Send notifications to customers"** (BG **"Изпращай известия до клиенти"**).

The per-mail Active flag is the **Active** switch column of the same list; on a locked mail the switch is disabled and stays on.

## What the merchant can do here

- Toggle the global switch ON/OFF in the page header (single click).
- Switch one mail off or on with its **Active** switch (not on locked mails).

## Settings & fields

### Page-level toggle

| Field | Setting key | Default | Effect when OFF |
|-------|-------------|---------|-----------------|
| **Send notifications to customers** | `customer_email_notifications` | `yes` | Meant to stop customer email notifications; in the code it applies only where a send asks for it (see *Business rules*) |

Persisted via `POST /admin/api/core/marketing/customer-mails-settings` with body `{customer_email_notifications: true/false}`. The backend translates the boolean to the string `'yes'` / `'no'` in the central platform settings table (one row per `(site_id, parameter)`). Other workers / queues pick up the new value on their next setting fetch.

### Per-mail Active flag

| Field | Source | Default | Effect when 0 |
|---|---|---|---|
| the platform code | One integer column on the `Mail` row | `1` | Skips ONLY that label's sends — other labels still fire |

### Forced-on labels (cannot be disabled via per-mail Active)

A mail is **locked** when its on/off cannot be changed: it always sends, whatever its Active flag and the global switch say. On the customer list the Aftercare acknowledgement of receipt is locked. The three labels below are merchant-alert mails, locked on [[settings-admin-notifications]]. The customer **two-factor code** email (`cc2fa_email`, used by the withdrawal form) is not locked: switched off, it sends nothing. Which other customer mails are locked is stored per store (verify).

| Label | Why forced-on |
|---|---|
| `email_confirmation` | Account-creation flow depends on the verification link |
| `two_factor_action` | 2FA action notifications |
| `alert_notification` | Critical platform alerts |

Locked mails ignore the global switch as well.

## Business rules

### Two layers of gating at send time

Every transactional mail dispatch checks **both**:

1. Global `customer_email_notifications == 'yes'` (store-wide) — but only for a send that asks for this check.
2. Per-mail the platform code (per-label), **except** for locked mails, which bypass both checks.

Both checks sit in the customer-notification helper. In the code the global check is off unless a send turns it on: the two-factor code email and the Aftercare emails do not, so the switch does not stop them, and no other customer email was found turning it on; only the wallet-expiry reminder reads the switch itself. What the switch stops in practice is therefore narrower than its label (verify on a store).

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
- **Keep the two-factor code email on** — the withdrawal form and the checkout login code depend on it.

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
