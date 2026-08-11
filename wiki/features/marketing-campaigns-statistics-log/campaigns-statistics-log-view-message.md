---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Log → View message"
route_name: campaigns.statistics.log.view-message
route_path: /admin/campaigns/statistics/view-message/{log_id}
aliases: ["View sent message", "Rendered message body", "Per-recipient rendered HTML", "Email body preview", "SMS body preview", "Viber body preview", "Web Push body preview", "data.smsCount"]
tags: [marketing, campaigns, statistics, logs, render]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-log]]. See the hub for the other aspects (surfaces, status values, status archive, filters & table, side-effects, Email mapping, storage).

# Per-send log — View message (rendered body)

## Purpose

The View-message drill-down is the merchant's answer to *"what did the customer actually see?"*. Each log row has stored, alongside its metadata, the **fully rendered** message body — the HTML / text after every dynamic variable (customer name, discount code, dynamic-tag content, product list, etc.) was substituted at send time. Clicking the channel icon on a log row opens this stored body in a side-panel / modal. Crucially, the displayed body is what was **delivered**, not the template with unresolved placeholders — so the merchant sees the exact rendered output that landed in the recipient's inbox / SMS app / Viber chat / push notification.

## Where to find it

Inside the [[marketing-campaigns-statistics-log|per-send delivery log]] — click the channel icon in the first column of any row in the [[campaigns-statistics-log-filters-table|log table]]. In the modern Vue surface this opens a nested modal; in the legacy Smarty surface it opens the view-message side-panel at the dedicated route.

## What the merchant can do here

- **Read the exact body the recipient received** — Email HTML in an iframe, SMS text, Viber text + image, Web Push title + body + image.
- **Verify variable substitution** — confirm the customer's name, discount code, and dynamic-tag content all resolved correctly at send time.
- **Inspect the sender identity** — for Email, see the verified mailbox actually used as `from`.
- **Confirm sandbox mode** — sandbox-flagged rows render the body but make clear the send was redirected to the inspection URL, not the real recipient.

## Settings & fields

### Legacy view-message route

| Route name | Method | Route path | Purpose |
|------------|--------|------------|---------|
| `campaigns.statistics.log.view-message` | GET | `/admin/campaigns/statistics/view-message/{log_id}` | Open a side-panel rendering the message body of one log row. |

In the modern Vue surface, the equivalent is a nested modal (`MarketingChannelsLogsPreviewMessageModal`) opened from inside the parent logs modal — no separate URL. See [[campaigns-statistics-log-surfaces]] for the modal-chrome behaviour.

### Channel-specific render

The view-message endpoint dispatches to the registered channel's per-channel rendering:

| Channel | Render output | Panel chrome |
|---------|---------------|--------------|
| Email | Full rendered HTML — wrapped in a side-panel with class `wide` (full-width drawer), HTML rendered inside an iframe so the recipient's CSS is fully isolated from the admin chrome. | Wide drawer. |
| SMS | The message text body — plain text in a narrow panel. | Standard width. |
| Viber | The text body + the image (if any). | Standard width. |
| Web Push | Title + body + image (if any). | Standard width. |

If the channel isn't registered (legacy / discontinued channel), the endpoint falls back to the raw stored message text without channel-specific formatting.

### Channel-specific `data` extras

Each log row stores a `data` field carrying channel-specific extras that the view-message render uses:

- **Email**: `from` (the verified sender mailbox actually used), `subject`, `message_id` (Elastic Email message ID), HTML / plain content via the content relation.
- **SMS**: `smsCount` (number of 160-char chunks consumed), `provider` (msghub / nth), provider message ID.
- **Viber**: image URL, button URL, `provider_message_id`.
- **Web Push**: title, body, action URL, `endpoint_hash`.

The `from` is the **actual sending address** used — the merchant's verified Email domain's mailbox, not the channel-level default. So if the merchant has multiple verified senders, the merchant can see which one this particular send went out from.

### `messages_send` and SMS chunk counting

For non-SMS log rows, `messages_send` is hard-coded to 1. For SMS rows, the provider response carries a "this message used N chunks" count which is stored on the log as `data.smsCount`. The grid surfaces it as the `messages_send` column — so the merchant sees that a 350-char SMS consumed 3 chunks (3 SMS credits against the plan).

### Sandbox flag

Each log row also stores `sandbox` (0 or 1) and `sandbox_url`. When a channel is in sandbox mode (Sandbox URL set), sends are redirected to the merchant's chosen inspection URL instead of the real recipient. Sandbox log rows still appear in the log but are flagged `sandbox=1` and `sandbox_time` captures the timestamp.

## Business rules

- **The rendered message body lives in a SEPARATE document.** The actual HTML / text lives in a related `MarketingLogContent` document keyed by the log row's ID (relationship name: `content`). The list query fetches metadata only; only the View Message endpoint joins to the content doc. See [[campaigns-statistics-log-storage]].
- **The body is rendered ONCE at send time, then immutable.** Variables resolve against the recipient's data at send time and persist. Even if the customer's name changes later, the View-message panel still shows the name as it was at send.
- **Display is what the recipient saw.** The endpoint serves the stored body as-is — no re-rendering, no template re-evaluation.
- **Email HTML is iframed.** For email logs the panel opens with class `wide` and HTML renders inside an iframe to isolate the recipient's marketing CSS from the admin UI.
- **Sandbox logs render the body but with sandbox metadata visible.** When `sandbox=1`, the view-message panel still shows the rendered body (since the message WAS rendered, just redirected) but the row metadata makes clear this was an inspection-mode send.
- **Owner-scoped via `site_id`.** The view-message endpoint applies the same site-scoping as the list query — a forged `log_id` returns 404. See [[campaigns-statistics-log-storage]].
- **No re-send from the panel.** Read-only. The merchant cannot trigger a re-send from this view.
- **`execute_message` flag tints the channel icon red.** If the original send hit an exception, the channel icon is tinted red — signalling the merchant should click for the error context.

## How it works

The view-message endpoint loads the log row scoped to the current site, plus its `content` relation (the separate `MarketingLogContent` document holding the rendered body). The channel is looked up by the row's `channel` field; if registered, the endpoint delegates to the channel's per-channel render (Email returns HTML; SMS / Viber return text; Web Push returns the structured object). If the channel isn't registered, the endpoint falls back to the raw stored text in a generic panel.

For Email the rendered HTML is injected into the panel via an iframe to isolate CSS. For SMS / Viber the body renders as plain text in a standard side-panel. For Web Push the title + body + image lay out as a preview tile mimicking the OS-level notification appearance.

The stored body is served verbatim — no re-rendering, no template evaluation, no variable resolution. What's stored IS what was sent.

## Related

- [[marketing-campaigns-statistics-log]] — hub.
- [[campaigns-statistics-log-surfaces]] — the modal / side-panel chrome that wraps the rendered body.
- [[campaigns-statistics-log-storage]] — the projection / content-document split that makes the lazy-load work.
- [[campaigns-statistics-log-filters-table]] — the channel-icon drill-down that opens this view.
- [[marketing-channels-email]] — channel-level email log; same render path.
- [[marketing-channels-sms-msghub]] — MsgHub SMS log.
- [[marketing-channels-sms-nth]] — NTH SMS log.
- [[marketing-channels-viber]] — Viber log.
- [[marketing-channels-webpush]] — Web Push log.

## Open questions

None.
