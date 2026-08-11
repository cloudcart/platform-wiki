---
type: feature
nav_path: "Marketing → Channels → Email notifications → Customisation limits"
route_name: marketing-mails-list
route_path: /admin/marketing-new/omnichannel/mails/list
aliases: ["What merchants can customise in customer mails", "Customer mail customisation limits", "customer_email_notification_type", "plain vs html email", "Re-firing customer mails", "Per-locale customer mail templates", "Какво може и не може да се променя в имейл"]
tags: [marketing, omnichannel, email, notifications, customisation, locale, refire]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[marketing-omnichannel-mails-list]]. See the hub for related aspects (mail labels, editor modal, toggles & gating, variables, abandoned-cart).

# Email notifications — customisation limits

## Purpose

This page enumerates **what merchants CAN customise** per template, **what they CANNOT**, the per-locale rules, the rendering-format setting `customer_email_notification_type` (plain vs HTML), and the workflows for **re-firing** an already-sent transactional email on an existing order.

## Where to find it

Customisation is performed in the **template editor modal** (see [[omnichannel-mails-editor-modal]]) opened from the **Email notifications** list at `/admin/marketing-new/omnichannel/mails/list`.

Re-firing workflows live on [[orders-details]] and its sub-pages.

The rendering-format setting `customer_email_notification_type` is **not exposed in the modern Vue UI** — it survives as a backend flag (verify whether legacy admin still exposes it).

## What the merchant can do here

### Editable per template — exact list

For every mail label, the merchant can edit FOUR things in the editor modal:

1. **Name** — internal display name in the list (not visible to the customer).
2. **Subject** — email subject line (visible to the customer). Variables restricted to `allowed_subject_vars` for that label — see [[omnichannel-mails-variables]].
3. **HTML body** — rendered email content (visible to the customer). Variables restricted to `allowed_vars` for that label. Edited via the Unlayer visual designer. Both `template_json` (re-editable shape) and `message_html` (rendered HTML) are persisted.
4. **`template_json`** — implicit; saved together with `message_html` from the designer.

### NOT editable

The merchant CANNOT change:

- **The trigger event** — each label is hard-wired to a platform event (e.g., `order_add` always fires on order placement). To suppress the trigger entirely, use the per-mail Active flag or the global *Send notifications to customers* master switch (see [[omnichannel-mails-toggles-gating]]). For order status changes there is one shared `order_status_change` mail and no per-status toggle; the per-order `notify_customer` flag is the only per-order lever.
- **The recipient** — always the order's customer (or the cart's customer / subscriber for `abandoned_restore_link`). **No CC / BCC / fallback addressing.**
- **The sender** — always `site_email` from [[settings-general]] (or the channel's `from_email` for marketing channels).
- **The mail label / key** — adding new platform mail types is a code change. See [[omnichannel-mails-labels]].
- **The per-locale fallback chain** — the platform automatically renders the admin's current-locale `MailLanguage`, falling back to `config('app.fallback_locale')` if missing.

## Settings & fields

### Email body format — `customer_email_notification_type`

| Field | Setting key | Values | Default | Effect |
|---|---|---|---|---|
| **Email body format** | `customer_email_notification_type` | `plain` / `html` | `plain` | When `plain`, HTML tags are not rendered — recipients see literal `<table>…</table>` strings |

The default in `Setting::$defaults` is `plain`. The legacy notification admin page exposed the "HTML emails" tick which persists `html`; otherwise it stays `plain`. The modern Vue UI does **not** expose this setting. CloudCart's default templates assume **HTML rendering**, so almost every store wants this set to `html`.

Merchants who notice transactional emails arriving with un-rendered HTML tags (e.g., `<table>…</table>` literally visible) likely have this set to `plain` and need a developer to flip it to `html` via the legacy admin or API.

### Per-locale templates

Each `Mail` has one or more `MailLanguage` rows — one per language the store supports. The list shows the row matching `site('language')` (the admin's CP language). The platform code accessor returns the current-language template, **falling back to `config('app.fallback_locale')`** if the current-language row doesn't exist.

Editing a template only edits the currently-selected language version; switching admin language and re-opening edits a different `MailLanguage` row. There is no bulk-copy across locales in the Vue UI (verify).

## Business rules

### Templates are stored in the apps DB connection

`Mail` and its translations (`MailLanguage`) hold the editable HTML. Editing IS a SQL UPDATE on `MailLanguage` (subject, name, message_html, template_json) plus a `last_edited` timestamp bump on the parent `Mail` row.

### Re-firing transactional emails on an existing order

There is **NO generic "re-send order confirmation" button** in the Vue UI. The `order_add` mail fires only once at order creation. To re-send specific labels on a specific order, the merchant uses workflows on [[orders-details]]:

| Action | Workflow | Label re-fired |
|---|---|---|
| Re-apply a status change | [[orders-status-change]] (destination status's notification toggle ON in [[settings-statuses]]) | `order_status_change` |
| Send invoice | [[orders-invoice]] | `send_invoice` |
| Send receipt | [[orders-receipt]] | `send_invoice` (verify) |
| Send credit note | [[orders-credit]] | `send_credit_notify` |
| Send payment request | [[orders-payment-manual]] (draft / pending order) | `order_payment_add` |
| Send checkout-resume link | Draft-alert *Send as email* button on a draft order | `manual_order` (see [[orders-notify-customer]]) |

To re-send the original confirmation, the merchant must copy the order content into a manual email OR cancel + re-create the order (NOT recommended).

### Bulk-import of templates exists in `sitecp_bulk.php`

The `Mail` model is registered as a bulk-import target (`customer-mails` key in `sitecp_bulk.php`). This is wired for the **legacy bulk-import tooling** — not exposed on the modern Vue page — but means templates can be exported / imported in bulk by CloudCart staff or via an integration (verify current status).

### Anti-spam policy NOT required

Unlike campaigns and channels (see [[marketing-campaigns-policy]]), the Email notifications page is **NOT gated by the anti-spam policy**. These are transactional emails (explicit user-triggered or order-driven) — they don't fall under "marketing consent". The merchant can freely edit these templates on a fresh store.

### Permissions

API endpoints are gated by the marketing permission (verify exact permission key).

### Customer mails vs Campaign emails

These are platform-event mails; campaigns are merchant-authored marketing blasts via [[marketing-campaigns]] (subscriber-segment targeting, anti-spam policy, multi-channel). The Vue editor is **shared** between both surfaces — the difference is which prop (`customerMailId` vs `campaignId`) is set on open. See [[omnichannel-mails-editor-modal]].

### Recommended merchant use

- **Localise + brand the templates** via the Unlayer designer — replace default logo + colours with brand assets.
- **Don't disable order confirmations** — toggling OFF the global switch makes customers think their order failed; use only for testing.
- **Use `{$tracking_link}` / `{$tracking_code}` only if your shipping provider populates them** — empty otherwise.
- **Flip `customer_email_notification_type` to `html`** if templates use HTML tables and you see literal tag text in the inbox.

## Related

- [[marketing-omnichannel-mails-list]] — hub.
- [[omnichannel-mails-labels]] — the fixed event catalogue.
- [[omnichannel-mails-editor-modal]] — the editor used here.
- [[omnichannel-mails-variables]] — per-label allow-lists.
- [[omnichannel-mails-toggles-gating]] — global + per-mail Active gating.
- [[orders-details]] / [[orders-status-change]] / [[orders-invoice]] / [[orders-receipt]] / [[orders-credit]] / [[orders-payment-manual]] / [[orders-notify-customer]] — re-firing workflows.
- [[orders-notify-customer]] — the per-order `notify_customer` flag, the only per-order lever on the status-change mail.
- [[settings-general]] — `site_email` as the sender.
- [[marketing-campaigns]] / [[marketing-campaigns-policy]] — campaign contrast.
- [[email-template]] — Email template entity.

## Open questions

- 📡 **`customer_email_notification_type` surface today.** Whether the legacy admin still exposes the "HTML emails" tick or it's now config-only (verify).
- 📡 **Per-locale bulk operations.** Whether any Vue or API affordance exists to copy a template across all enabled locales (verify roadmap).
- 📡 **Receipt mail label.** Which `Mail` label drives [[orders-receipt]] sends — `send_invoice` or a separate label (verify).
