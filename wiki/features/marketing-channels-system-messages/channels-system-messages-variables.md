---
type: feature
nav_path: "Marketing → Channels → Channels setup → System messages → Variables"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["System message variables", "Merge tags", "Transactional variables", "Variables legend", "Add variable"]
tags: [marketing, channels, system-messages, variables, merge-tags]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-system-messages]]. See the hub for the other aspects (catalog, editor, validation, business rules, counters, AI assist).

# System messages — variables (merge tags)

## Purpose

The **Variables legend** is the set of merge tags the merchant can drop into a system-message template body. The platform substitutes them at send-time with the actual recipient's / order's data. The available tags depend on `(channel, is_campaign)` — system messages get the larger transactional set; the campaign editor on the same channel exposes a smaller marketing-oriented set.

## Where to find it

In the editor (see [[channels-system-messages-editor]]):

- **Add variable** dropdown — searchable, sits above the text field. Picks one tag and inserts it as a non-breakable pill at the caret.
- **Variables legend** card — sits below the editor as a 2-column grid; each variable name is a clickable link that copies it to clipboard.

## What the merchant can do here

- **Search and pick a variable** from the Add-variable dropdown — placeholder *"Search"*, group title *"Variables"*, empty text *"No variables found"*.
- **Insert it as a pill** into the active field at the caret position. The pill is non-breakable — the merchant can't accidentally split the tag.
- **Copy a variable to clipboard** by clicking it in the Variables legend below the editor.

## Settings & fields

The variables themselves are platform-defined — the merchant cannot add, rename, or remove a variable. The tables in the next two sections list the available set per channel + context.

## Available variables — system message context

### Viber + SMS (non-campaign / system message)

| Variable | Substituted value |
|----------|------------------|
| `{$customer_phone}` | Customer's phone number |
| `{$customer_first_name}` | First name |
| `{$customer_last_name}` | Last name |
| `{$customer_email}` | Email |
| `{$customer_address}` | Shipping/billing address (verify) |
| `{$order_status}` | Current order status label |
| `{$invoice_number}` | Invoice number (verify) |
| `{$invoice_date}` | Invoice date (verify) |
| `{$total}` | Order total |
| `{$shop_url}` | Store URL |
| `{$site_order_link}` | Link to the order's customer-facing details page |
| `{$reset_link}` | Password-reset link (only meaningful on `customer_forgot_password`) |

### Web Push (non-campaign / system message)

| Variable | Substituted value |
|----------|------------------|
| `{$customer_first_name}` | First name |
| `{$customer_last_name}` | Last name |
| `{$order_id}` | Order number |
| `{$order_status}` | Current order status label |
| `{$invoice_number}` | Invoice number (verify) |
| `{$invoice_date}` | Invoice date (verify) |
| `{$total}` | Order total |
| `{$shop_name}` | Store name |
| `{$expedition_date}` | Order expedition date (only meaningful on `order_status_fulfillment_change`) |
| `{$delivery_date}` | Expected delivery date (same event) |

### Campaign editor (different variable set)

The same channels expose a smaller variable set in campaign actions — subscriber details, shop URL, unsubscribe link — but typically NOT order details, since campaigns are blasts rather than transactional one-per-event sends. See [[marketing-campaigns]] for the campaign-side legend.

## Business rules

### Pills protect the tag from accidental edits

When the merchant clicks **Add variable**, the tag becomes a coloured non-breakable pill in the editor. The merchant can't split `{$customer_first_name}` into `{$customer_first_` + `_name}` by selecting part of it.

### Edit-modal returns webpush variable patterns for BOTH Viber and Web Push

Confirmed quirk: the single-message GET endpoint serves the same `campaigns.web_push.variables.patterns` config to both Viber and Web Push templates. The list and the editor draw from the same legend regardless of channel. Variables that don't apply (e.g., Web Push-only `{$expedition_date}` on a Viber template) would still appear in the dropdown — relying on the merchant to pick the right ones.

### Substitution happens at send-time, not preview-time

The live mobile-phone preview ([[channels-system-messages-editor]]) shows raw pills (`{$customer_first_name}`), NOT a sample subscriber's data. There is no "preview as recipient X" feature. The actual substitution runs when the platform dispatches the message in response to the event firing.

### Channel-scoped + event-context-aware

The Variables legend the merchant sees depends on `(channel, is_campaign)`. The "transactional" set (system messages) is broader — customer + order + payment details. The "marketing" set (campaigns) is narrower — subscriber + shop URL + unsubscribe link.

### Empty-state copy

When the searchable Add-variable dropdown matches no variables, the empty text is *"No variables found"*. Group title in the dropdown is *"Variables"*.

## Related

- [[marketing-channels-system-messages]] — hub.
- [[channels-system-messages-editor]] — the editor surface where Add variable and the legend live.
- [[channels-system-messages-catalog]] — which events expose which variables by default.
- [[marketing-campaigns]] — campaigns expose a different (smaller) variable set on the same channels.
- [[marketing-channels-viber]] — Viber-channel reference.
- [[marketing-channels-webpush]] — Web Push-channel reference.

## Open questions

- The `{$customer_address}`, `{$invoice_number}`, and `{$invoice_date}` substituted values are listed (verify) — confirm exact formatting against backend.
