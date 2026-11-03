---
type: entity
aliases: ["Transactional email template", "Mail template", "Customer notification template", "Per-event email", "Транзакционен имейл шаблон"]
tags: [marketing, email, templates, transactional, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[email-template]]. See the hub for the other aspects (campaign authoring, merge variables, channel delivery).

# Email Template — transactional family

## Identity

A **transactional Email Template** is the per-event customer email the platform sends automatically when something happens to an order or account — Order confirmation, Order status changed, Abandoned cart restore link, Welcome, Password reset, Invoice attached, and so on. There is exactly **one transactional template per platform event**, and the set of events is **fixed in code**: the merchant CANNOT add new transactional template types, only edit the wording and layout of the ones CloudCart defines (the full set is roughly 30 labels).

Transactional templates are managed on [[marketing-omnichannel-mails-list]] (Sidebar → Marketing → Channels → Email notifications) but are edited in the same Unlayer drag-and-drop editor that campaign templates use — see [[email-template-campaign-authoring]] for the editor itself.

Each transactional template has a **per-event allowed-variable list** (e.g., `{$customer_first_name}`, `{$order_id}`, `{$tracking_link}`) that the platform substitutes against the actual recipient's data at send time. The full merge-tag mechanics live on [[email-template-variables]].

## Aliases

- **Transactional email template** — the canonical term for the per-event family.
- **Mail template** — alternative phrasing tied to this list (the underlying Vue model is literally `Mail` + `MailLanguage`).
- **Customer notification template** — phrasing on the Email-notifications screen.
- **Транзакционен имейл шаблон** — Bulgarian phrasing for this family.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Label** | n/a (platform-defined) | The event key — e.g., `welcome`, `order_add`, `order_status_change`, `abandoned_restore_link`, `send_invoice`, `password_change`. The full ~30-label set is fixed in code; merchants cannot add new ones. |
| **Name** (`name`) | Free-text | The label the merchant sees in the list (e.g., *"Order confirmation"*). Capped at `max:191` chars. |
| **Subject** (`subject`) | Free-text per-language | The email subject line. May reference merge variables from the allowed list (e.g., *"Order #{$order_id} confirmed"*). Some events have **required subject variables** (order-related events require `{$order_id}`). Capped at `max:191`. |
| **HTML body** (`message_html`) | Edited in the Unlayer editor | The rendered HTML the customer receives. Stored alongside `template_json` for re-editing. |
| **Active flag** (`active`) | Per-template (in the editor) | When `active = 0` AND the global `customer_email_notifications` setting is `yes`, this specific event's email is suppressed but others still fire. Independent of the page-level global on/off toggle. |
| **Language** (`MailLanguage` row) | Per language the store supports | Each transactional template has one row per active store language. The list shows the row matching the admin's CP language. Editing edits ONLY the currently-selected language version — switching language opens a different row. |
| **Last edited** (`last_edited`) | n/a (auto-bumped on save) | Drives the **Last edited** column on [[marketing-omnichannel-mails-list]]. |

Transactional templates are stored in the `mails` + `mails_language` tables.

### Master `customer_email_notifications` toggle silences EVERY customer-facing transactional email

When the global `customer_email_notifications` setting is set to `no`, the platform suppresses **every** customer-facing transactional email — including order confirmations, password reset, email confirmation, account-banned alerts, and every other event-driven send. The gate sits in the single shared notification helper used by all transactional sends. There is no opt-out path for individual events to bypass the master toggle in normal use — flipping it off effectively silences customer-facing transactional mail completely. To silence just one event, set that template's `active = 0` instead.

### Transactional sends bypass the campaign anti-spam policy

Transactional sends are NOT subject to [[marketing-campaigns-policy]] (the anti-spam gate applies to campaign sends only). A customer who has been removed from a campaign for an abuse complaint still receives transactional mail to the same address — unless the master `customer_email_notifications` toggle is off, or the address has been hard-bounced and suppressed at the channel level (see [[email-template-delivery]]).

## Where it appears

- [[marketing-omnichannel-mails-list]] — the master list of transactional Email Templates (Sidebar → Marketing → Channels → Email notifications). Includes the global *Send notifications to customers* on/off toggle.
- [[settings-invoicing]] — the `send_invoice` transactional template is emailed with each invoice PDF attachment.
- [[orders-invoice]] — the invoice-attached email uses the `send_invoice` template.
- [[checkout-flow]] — produces the order-related events that fire transactional templates.
- [[abandoned-cart-recovery]] — the concept that the `abandoned_restore_link` transactional template powers (the leaver receives it when they are a subscriber rather than a registered customer).

## Related

- [[email-template]] — hub.
- [[order]] — many transactional templates fire on Order events; they reference the order via merge variables — see [[email-template-variables]].
- [[customer]] — the recipient of most transactional templates.
- [[notification-delivery]] — the platform-wide notification pipeline that routes templates through the configured email channel.
- [[marketing-channels-email]] — the Email channel that actually delivers the rendered template.
- [[settings-invoicing]] — controls the invoice email that uses `send_invoice`.

## Open Questions

- ⏸️ The fallback behaviour when the merchant has not localised a transactional template for one of the store's active languages — does the customer see the fallback language version silently, or is there a UI hint?
