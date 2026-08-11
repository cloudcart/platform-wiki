---
type: feature
nav_path: "Marketing → Channels → Email notifications"
route_name: marketing-mails-list
route_path: /admin/marketing-new/omnichannel/mails/list
aliases: ["Email notifications", "Customer emails", "Transactional emails", "Customer mails", "Имейл известия", "Транзакционни имейли", "Имейли към клиенти"]
tags: [marketing, omnichannel, email, notifications, transactional]
plan_gates: ["change_email_notifications", "abandoned_orders"]
created: 2026-05-21
updated: 2026-06-10
source_count: 4
---

# Email notifications

## Purpose

The **Email notifications** screen is where the merchant edits the **transactional / system emails** that CloudCart sends to **customers** on platform events — *"Welcome"*, *"Order confirmation"*, *"Order status changed"*, *"Payment received"*, *"Abandoned cart restore link"*, *"Password reset"*, *"Email confirmation"*, *"Product back in stock"*, and many others. These are the **per-event customer-facing emails**, distinct from the **promotional campaigns** the merchant builds under [[marketing-campaigns]]: campaigns are merchant-authored marketing blasts targeting subscribers; mails are platform-authored event responses with merchant-customisable templates.

Per template, the merchant edits the **Name**, **Subject**, and **HTML body** with a per-label allow-list of variables (`{$customer_first_name}`, `{$order_id}`, `{$total}`, `{$tracking_link}`, etc.). A **global on/off switch** at the top silences the entire customer-notification system in one click. **Last edited** timestamps surface in the list.

This is one of two screens reached from **Channels** in the sidebar — its sibling is the channels-setup hub (Email / SMS / Viber / Web Push providers).

## Where to find it

Sidebar → **Marketing** → **Channels** → **Email notifications**.

Route: `/admin/marketing-new/omnichannel/mails/list`, component `MarketingMailsListPage`. The legacy sidebar link routes to `/admin/marketing/omnichannel/mails/list` — the modern Vue page lives under `/admin/marketing-new/...`.

The page header reads **"Email notifications"** (BG: **"Имейл известия"**) with an envelope icon.

## What the merchant can do here

- See the list of all transactional mail templates as a table with columns **Name**, **Subject**, **Last edited**. (List does not paginate — `:hide-pagination="true"`; roughly 20–30 entries.)
- Toggle the global switch **"Send notifications to customers"** in the page header — when OFF, no customer transactional emails are sent at all. See [[omnichannel-mails-toggles-gating]].
- Click a row's Name cell to open the **template editor modal** — see [[omnichannel-mails-editor-modal]] for the editor anatomy and Unlayer designer details.

## Settings & fields

| Field | Setting key | Default | Effect when OFF |
|-------|-------------|---------|-----------------|
| **Send notifications to customers** | `customer_email_notifications` | `yes` | Stops the platform from sending any customer transactional email — including security mail like password reset. See [[omnichannel-mails-toggles-gating]]. |

A second backend-only setting controls rendering format:

| Field | Setting key | Values | Default |
|-------|-------------|--------|---------|
| Email body format | `customer_email_notification_type` | `plain` / `html` | `plain` |

The default `plain` makes HTML templates render as literal tags in the recipient's inbox. Almost every store wants `html`. See [[omnichannel-mails-customisation-limits]].

Each row corresponds to one **mail label** (e.g., `order_add`, `abandoned_restore_link`, `welcome`). The full label catalogue + trigger events is on [[omnichannel-mails-labels]].

## Sub-pages (in this cluster)

This screen is split into 5 aspect pages — each well-scoped. The Assistant should drill into the aspect that matches the question, not read every page.

- [[omnichannel-mails-labels]] — the fixed catalogue of platform mail labels (`welcome`, `order_add`, `abandoned_restore_link`, etc.) and what triggers each.
- [[omnichannel-mails-editor-modal]] — the shared `CampaignEmailTemplateScratchModal` (Unlayer designer, variables legend, Send example, three-mode prop signature).
- [[omnichannel-mails-toggles-gating]] — global `customer_email_notifications` toggle + per-mail the platform code flag + three forced-on security labels (`email_confirmation`, `two_factor_action`, `alert_notification`).
- [[omnichannel-mails-variables]] — per-label `allowed_vars` / `allowed_subject_vars` / `required_subject_vars` allow-lists, server-side filtering, variable-insertion via the legend.
- [[omnichannel-mails-abandoned-cart]] — the `abandoned_restore_link` recovery subsystem; `AbandonedCartSend` job on the `system` queue; `abandoned_remainder` + `abandoned_remainder_interval` settings; `abandoned_orders` plan gate.
- [[omnichannel-mails-customisation-limits]] — what the merchant CAN / CANNOT edit; per-locale `MailLanguage` rows; `customer_email_notification_type` (plain vs HTML); re-firing workflows on existing orders.

## Business rules

### Customer mails vs Campaign emails

The single biggest source of confusion in this area. Two separate systems, one shared editor component:

| | Customer Mails (this page) | Campaign Emails ([[marketing-campaigns]]) |
|---|----|----|
| Trigger | Platform event | Merchant-built campaign |
| Recipient | Specific customer | Subscriber segment |
| Channel routing | Always Email | Email / SMS / Viber / Web push |
| Setup gate | None — works out of the box | Anti-spam policy + channel activation |
| Templates | Fixed list of platform events | Free-form merchant-authored |
| Variables | Fixed allow-list per event | Includes dynamic-discount + segment variables |

The Vue editor (`CampaignEmailTemplateScratchModal`) is the same component for both — branches on whether `customerMailId` or `campaignId` is set.

### Two layers of gating apply at send time

1. The global `customer_email_notifications` setting (must be `'yes'`).
2. The per-mail the platform code row flag (must be `1`) — except for three forced-on security labels.

Both checks happen inside `sendNotification` in the customer-notification helper. The Vue UI surfaces only layer (1); layer (2) is a legacy-admin field. See [[omnichannel-mails-toggles-gating]] for the full mechanics.

### Anti-spam policy NOT required

These are transactional emails (user / order-triggered). Unlike campaigns ([[marketing-campaigns-policy]]), this page is NOT gated by anti-spam acceptance.

### Per-locale templates with fallback

Each `Mail` has one `MailLanguage` row per store language. Editing is per-locale; the platform falls back to `config('app.fallback_locale')` if the current locale row is missing. See [[omnichannel-mails-customisation-limits]].

### `last_edited` timestamp bumps on every save

`PUT /admin/api/core/marketing/customer-mails/{id}` updates the `MailLanguage` row + bumps the parent the platform code timestamp — that's what the list's **Last edited** column shows.

### Backend controller surface

The Vue page reads from these endpoints (verify):

- `GET.../customer-mails` → list rows `{id, label, name, subject, active, last_edited}`.
- `GET.../customer-mails-settings` → returns `{customer_email_notifications: boolean}`.
- `POST.../customer-mails-settings` → persists the global toggle.
- `GET.../customer-mails/{id}` → full template.
- `PUT.../customer-mails/{id}` → updates `MailLanguage` + bumps `last_edited`.
- `GET.../customer-mails/{id}/variables` → per-label allow-list for the editor legend.

## Recommended merchant use

- **Localise + brand the high-traffic templates first.** `order_add`, `order_status_change`, `abandoned_restore_link` — these are seen most.
- **Tune the abandoned-cart email.** Subject line drives open rate, which drives recovery revenue. See [[omnichannel-mails-abandoned-cart]].
- **Don't toggle OFF the global switch in production.** It silently blocks password reset and email confirmation.
- **Flip `customer_email_notification_type` to `html`** if templates use HTML tables and arrive with literal tag text.

## Related

- [[marketing]] — parent hub.
- [[marketing-campaigns]] — promotional campaigns (the merchant-authored counterpart).
- [[marketing-campaigns-policy]] — anti-spam policy that gates campaigns but NOT this page.
- [[marketing-dashboard]] — marketing analytics (covers campaign emails, not these transactional ones).
- [[order-status-workflow]] / [[orders-status-change]] — order-status transitions fire most of these mails.
- [[checkout-flow]] — `order_add` and `abandoned_restore_link` are dispatched here.
- [[cart-vs-order-lifecycle]] — abandoned-cart concept the recovery mail depends on.
- [[notification-delivery]] — platform-wide outbound notification mechanism.
- [[settings-statuses]] — order statuses that trigger `order_status_change`.
- [[settings-payment-providers]] — payment providers whose status changes trigger `order_payment_status_change`.
- [[settings-general]] — `site_email` as the default sender.
- [[email-template]] — Email template entity.
- [[customer]] — recipient entity.
- [[subscriber]] — recipient entity for abandoned-cart when not a customer.
- [[order]] — data source for order-related mails.
- [[cart]] — data source for abandoned-cart recovery.

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `change_email_notifications` | Access | Lower plans can see the list but cannot **edit** templates — the route `marketing/omnichannel/mails/edit/%` is gated. Defaults still send on lower plans; only customisation is blocked. |
| `abandoned_orders` | Access | Gates the **abandoned-cart recovery** subsystem at the `abandoned` route. The `AbandonedCartSend` job auto-destroys (`EXECUTE_DESTROY`) on plans without this feature. See [[omnichannel-mails-abandoned-cart]]. |

The global `customer_email_notifications` toggle is **independent** of these plan gates and acts as a master kill switch regardless of plan tier.

## Open questions

- 📡 **Abandoned-cart reminder settings location.** `abandoned_remainder` + `abandoned_remainder_interval` live under platform Settings, not on this Vue page. Exact admin route to verify. GraphQL-resolvable: query the merchant's settings for current values.
