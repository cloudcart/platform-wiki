---
type: feature
nav_path: "Marketing → Channels → Channels setup → System messages → Event catalog"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["System messages event catalog", "Viber system events", "Web Push system events", "Transactional template catalog"]
tags: [marketing, channels, system-messages, transactional, viber, web-push]
plan_gates: ["viber_messages", "campaign.channel.web_push"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-system-messages]]. See the hub for the other aspects (editor, variables, validation, business rules, counters, AI assist).

# System messages — event catalog

## Purpose

The catalog of **per-event transactional templates** the platform fires when something happens in the store. Each channel that exposes System messages owns its own catalog — Viber has 7 templates, Web Push has 2. The merchant cannot add or remove templates; the list is fixed by the platform.

## Where to find it

Sidebar -> **Marketing** -> **Channels** -> **Channels setup** -> click the **Viber** or **Web Push** card -> click **System messages**. Modal title is built dynamically: *"System messages - {Channel Name}"*.

## Channel applicability

| Channel | System messages modal | Channel mapping key | Event templates |
|---------|----------------------|---------------------|------------------|
| **Viber** | Yes | `viber_message` | 7 templates |
| **Web Push** | Yes | `web_push` | 2 templates |
| **Email** | No (use [[marketing-omnichannel-mails-list]] instead) | — | — |
| **SMS MsgHub** | No (campaign-only) | — | — |
| **SMS NTH** | No at channels-page level (campaign-action context only) | `sms_nth_message` | — |

The button is hidden on cards that do not expose System messages.

## Viber system messages — events and default titles

| Event key | Title (en) | Title (bg) | Default body excerpt |
|-----------|------------|------------|----------------------|
| `customer_create` | "When customer is created" | "При регистрация на потребител" | *"Hello {\$customer_first_name}, Thank you for creating your {\$shop_url} account! Use your email address to login: {\$customer_email}"* |
| `customer_forgot_password` | "When customer requests new password" | "Когато потребител поиска нова парола" | *"...require a password change to {\$shop_url}, Upgrade your password here {\$reset_link}"* |
| `cash_on_delivery` | "When customer pay 'Cash on Delivery'" | "Когато клиент плати с 'Наложен платеж'" | *"Thank you for your order in {\$shop_url}! {\$customer_first_name}, your {\$order_id} order of {\$total} is registered. Order Details: {\$site_order_link}"* |
| `bank_wire_transfer` | "When customer pay 'Bank Wire Transfer'" | "Когато клиентът плати по 'Банков трансфер'" | Order-placed thanks + bank details + order link. |
| `credit_card` | "When customer pay with 'Credit Card'" | "Когато клиентът плати с 'Кредитна карта'" | Order-placed thanks + order link. |
| `order_status_change` | "When order status is changed" | "При промяна на статус на поръчка" | *"Hello {\$customer_first_name}, Order status in {\$shop_url} - order # {\$order_id} was changed to '{\$order_status}'. Details of the order: {\$site_order_link}"* |
| `order_status_fulfillment_change` | "When Order is 'Fulfilled'" | "Когато поръчката е 'Изпратена'" | *"Hello {\$customer_first_name}, your {\$shop_url} order {\$order_id} will be sent on {\$expedition_date}. It is expected to arrive on {\$delivery_date}. Details of the order: {\$site_order_link}"* |

## Web Push system messages — events and default fields

| Event key | Title (en) | Default title field | Default body field |
|-----------|------------|--------------------|--------------------|
| `order_status_change` | "When order status is changed" | *"Hello {\$customer_first_name}"* | *"Order # {\$order_id} was changed to '{\$order_status}'"* |
| `order_status_fulfillment_change` | "When Order is 'Fulfilled'" | *"Hello {\$customer_first_name}"* | *"Your order with {\$order_id} will be sent to {\$expedition_date}. She is expected to arrive at {\$delivery_date}"* |

## What the merchant can do here

- Browse the per-channel list with three columns: template label, send-count *"Send messages (**N**)"*, status switch.
- Toggle a template ON / OFF (see [[channels-system-messages-business-rules]] for switch semantics).
- Click the template label to open the editor (see [[channels-system-messages-editor]]).

## Settings & fields

The catalog is a fixed list — there are no merchant-settable fields at catalog level beyond the per-row status switch (covered under business rules below) and the read-only send-count column. Per-template content fields are covered on [[channels-system-messages-fields-validation]]; the variable legend each template exposes is on [[channels-system-messages-variables]].

## What the merchant cannot do

- **Cannot add new event templates.** The catalog of events is fixed (Viber: 7; Web Push: 2). Custom event triggers like *"Trigger when subscriber abandons cart"* must use campaigns instead.
- **Cannot delete templates.** Disabling = toggling OFF; the row stays in the list.
- **Cannot change the event the template is bound to.** *"When customer is created"* is permanently tied to the customer-registration event.
- **Cannot edit the internal `event` key** (e.g., `customer_create`, `order_status_change`). The merchant sees only the human-readable title.

## Business rules

### Per-event uniqueness

Each `(channel, language, event)` combination has exactly one template row. There is no "duplicate" or "A/B test" support; the merchant edits the single row's content. See [[channels-system-messages-business-rules]] for language-fallback handling.

### Channel must be installed + active to send

A template toggled ON, on a channel that is NOT installed or NOT active, will not send when its event fires. The platform short-circuits dispatch before reaching the template lookup. Install + activate the channel on [[marketing-channels]] first.

### Email is the parallel concept on a different surface

Email's transactional templates are NOT in this catalog. Email uses [[marketing-omnichannel-mails-list]] — same idea (per-event transactional content), different surface and editor.

## Related

- [[marketing-channels-system-messages]] — hub.
- [[marketing-channels]] — parent channels hub; where the merchant first picks Viber / Web Push.
- [[marketing-channels-viber]] — Viber channel reference. Owns the 7 Viber event templates listed above.
- [[marketing-channels-webpush]] — Web Push channel reference. Owns the 2 Web Push templates.
- [[marketing-omnichannel-mails-list]] — Email's parallel transactional catalog.
- [[marketing-channels-logs]] — channel logs; system-message sends appear here with Type = *"System message"* and the event label.

## Open questions

None.
