---
type: feature
nav_path: "Orders → Order details → History → View-time enrichment"
route_name: admin.orders.history
route_path: /admin/orders/action/history/:order_id
aliases: ["Order history enrichment", "History view-time lookups", "History locale rendering", "History waybill join", "История — обогатяване"]
tags: [orders, history, audit, i18n, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-history]]. See the hub for the other aspects (timeline UI, action codes, record model, synthetic entries, acting party, API & triggers).

# Order history — view-time enrichment

## Purpose

Several history rows are stored with **keys / codes**, not finished text, and are resolved to their final display form **at view time** by looking up live data. This matters because it means a history row can read differently today than when it was written — the same stored data is rendered against the current locale, status taxonomy, app catalogue, and country list.

## Where to find it

All enrichment happens when the History panel on [[orders-details]] is rendered — see [[orders-history-timeline-ui]]. This page documents the lookups behind the displayed text.

## What the merchant can do here

Nothing directly. The practical consequence the merchant sees: descriptions appear in their own admin language, custom-status entries can change wording after a rename, and address-change diffs show full country names and waybill specifics — all without the stored row changing.

## Settings & fields

No editable settings. The enrichment lookups, in summary:

| Stored as | Resolved to (at view time) | Source |
|---|---|---|
| `message` translation key | Localised text | Admin's locale, key prefix `order.history.label.` |
| `message_data.app` reference | App friendly name | Apps catalogue |
| Custom-status KEY (code 53) | Status display name | Status taxonomy ([[settings-statuses]]) |
| Country ISO code (in address diffs) | Full country name | Batch country lookup |
| `log_id` on action 27 | Waybill details | Waybill log entry |

## Business rules

### Messages render via translation keys (locale-aware)

The `message` column stores a TRANSLATION KEY (e.g., `order_payment_paid`). At display time the platform translates it using the current admin's locale, prefixed with `order.history.label.`. So the same audit log renders in Bulgarian for a Bulgarian admin and in English for an English admin — the data layer is locale-agnostic.

### `message_data` app references render via the apps catalogue

If `message_data` contains an `app` reference, the platform looks up that app's friendly name at display time. A row stored as *"App was uninstalled"* with `app: speedy` renders live as *"Speedy was uninstalled"*.

### Custom status (code 53) renders the name from the live taxonomy

When the action is code 53 (custom status applied — see [[orders-history-action-codes]]), the platform stores the status KEY in `message` and looks up the status name from the merchant's [[settings-statuses]] taxonomy at view time:

- If the merchant **renames** a custom status later, all OLD history entries display the NEW name.
- If the merchant **deletes** the custom status, the entry shows the raw key string.

### Action 27 (fulfillment add) joins the waybill log

Action code 27 (`order_fulfillment_add`) has special handling: when `log_id` is present, the platform looks up the related waybill log entry and attaches it as a `waybill` attribute on the row, so the sub-template can render waybill specifics (tracking number, courier shipment ID, etc.). Other action codes do not get this enrichment even when they carry a `log_id`. See [[orders-shipping-waybill]] for the waybill itself.

### Country codes auto-resolved for address-change diffs

When a row's `message_data` contains a country code (in address-change before / after diffs), the platform collects all referenced country ISO codes and looks up their full names, so the template renders *"Bulgaria"* instead of *"BG"*. This is a **single batch lookup per page-load**, not a per-row query.

### Side effects

None — all enrichment is read-time only.

## Related

- [[orders-history]] — hub.
- [[orders-history-action-codes]] — code 53 (custom status) + action 27 (fulfillment) definitions.
- [[orders-history-record-model]] — the stored `message` / `message_data` / `log_id` fields enriched here.
- [[orders-history-timeline-ui]] — where the enriched text is displayed.
- [[settings-statuses]] — status taxonomy used for code-53 name lookup.
- [[orders-shipping-waybill]] — the waybill joined onto action-27 rows.

## Open questions

None.
