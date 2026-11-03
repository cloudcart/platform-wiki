---
type: feature
nav_path: "Profile → My subscriptions → Subscription → On-screen display"
route_name: admin.subscriptions.show
route_path: /admin/subscriptions/{unique_id}
aliases: ["Subscription detail screen", "Subscription info cards", "Subscription status badge", "Subscription detail fields", "Детайли на абонамент — екран"]
tags: [subscriptions, details, display, billing, account, modern-vue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions-detail]]. See the hub for the other aspects (cancel/renew endpoint behaviour, lifecycle side-effects).

# Subscription detail — on-screen display

## Purpose

The visible surface of the per-subscription view: the header, the three info cards, the status badge, and where the transactions table sits. This is what the merchant actually reads when they open one subscription to answer *"what is this, what does it cost, and when does it renew?"*. Everything here is **display-only** — no field on this screen is editable inline.

## Where to find it

[[subscriptions]] → click any row's ID/Name → opens `/admin/details/subscriptions/<unique_id>`. The breadcrumb reads **Subscriptions → `<unique_id>`**; the header title is `<unique_id> - <subscription name>`.

## What the merchant can do here

### Header

- **Icon** — varies by subscription type (gear for feature pack, grid for app, user-gear for service, star-calendar for plan). When the underlying model has a custom image (e.g. an app's logo), the image is shown instead.
- **Title** — `<unique_id> - <subscription name>`. Example: `66b3fa1abcd - Plan: Business — Year`.
- **Breadcrumb** — Subscriptions → `<unique_id>`.

### Info cards (3 columns)

**1) Details card** *(icon: circle-info)*

| Field | What it shows |
|-------|---------------|
| **Created at** | Datetime the subscription was first created (the original purchase moment), formatted in the store's `format.dateTime` locale setting. |
| **Type** | `Feature` / `Application` / `Service` / `Plan` / `Template`. |
| **Name** | The subscription's full descriptive name (e.g. *Algolia Search Pro*, *Plan: Business — 12 months*). |

**2) Pricing card** *(icon: file-invoice-dollar)*

| Field | What it shows |
|-------|---------------|
| **Price** | Per-cycle price in the subscription's currency. |
| **Billing period** | `once` / `month` / `year` / `2years` — or a literal month count for non-standard cycles. |
| **Value** | The subscription's quantitative value when applicable (e.g. for a "1000 extra products" feature pack the value is `1000`; for a 24-month contract the value is `24`). Renders ` - ` when null. |

**3) Next billing card** *(icon: calendar-day)*

| Field | What it shows |
|-------|---------------|
| **Next billing date** | When the next renewal will be attempted, formatted per the store's date format. Renders `-` when the subscription has no next billing date (one-time / fully expired). |
| **Next billing amount** | The amount that will be charged on next billing. |
| **Status** | A coloured badge — `Active` (green) / `Canceled` / `Past due` / `Expired`. |

### Transactions table (under the info cards)

Below the info cards is the full transactions table for this subscription — see [[subscriptions-transactions]] for the column-by-column documentation. On mobile, the table is preceded by a Tabs strip with one tab labeled **Transactions** (a vestige of a planned multi-tab layout — currently there's only one tab).

### What the merchant CANNOT do here

- Edit the subscription's price, billing period, value, or next billing amount inline. All fields are display-only. The platform also rejects any backend attempt to change `next_billing_amount` — see [[subscriptions-detail-cancel-renew]].
- Change the saved card associated with this subscription. The card on file lives in [[billing-cards]] and is used for ALL the merchant's subscriptions — there's no per-subscription card.
- Pause / suspend the subscription. The only off-switch is **Cancel** (from the list page or the cancel endpoint directly).
- Move the subscription to a different store. Subscriptions are bound to one `site_id` for their entire lifetime.

## Settings & fields

All fields on this page are read-only. The underlying entity exposes:

| Field | What it represents |
|-------|--------------------|
| `unique_id` | Short opaque ID — appears in the URL and the title. |
| `created_at` | Original purchase datetime. |
| `model_type` | `plan_details` / `cloudcart_app` / `cloudcart_feature` / `cloudcart_service` / `theme` — drives the icon and the Type label. |
| `name` | Derived from the linked model. |
| `price` / `price_formatted` | Per-cycle price. |
| `billing_period` | `once` / `month` / `year` / `2years` / literal months. |
| `value` | Numeric value (quantity / months) when the subscription is value-bearing. |
| `next_billing_date` | When the next renewal attempt is scheduled. |
| `next_billing_amount` | Amount of next charge. |
| `status` | `1` Active / `0` Canceled / `2` Past due / `3` Expired. |
| `failed_attempts` | Consecutive failed retries (visible on the list page, not on the detail page). |
| `lta_contract_id` | When set, indicates an LTA contract — surfaces a contract link on the legacy view. |

## Business rules

### Status colour coding

The status badge has only two visual states: `Active` (green / `cc-badge-status--active`) and "everything else" (red-tinged / `cc-tag-status--required`). Past due, Canceled, and Expired all render in the same red style — the badge's **text** is what distinguishes them.

### LTA contracts show a contract link on the legacy view

In the legacy Smarty subscription-details template, when `lta_contract_id` is set, the title gets an extra fragment: `<unique_id> / Contract: <contract_unique_id>`, where the contract ID is clickable to the contract show page. The modern Vue view does NOT surface this link — merchants on LTA contracts may need to use the legacy URL to navigate to their contract.

### Service-type subscriptions show the service description (legacy view only)

When `model_type == 'cloudcart_service'`, the legacy view renders the service's HTML description in a dedicated section below the details box. The modern Vue view doesn't show this — a small loss of context for Expert-Service subscriptions on the modern UI.

### Subscription `value` field — usage varies by type

- **Feature packs**: the pack's quantity (e.g. 1000 for "1000 extra products"). Renewal preserves the value unchanged.
- **Contracts**: the contract duration in months.
- **One-time services**: typically null.
- **Plans**: typically null (plan tier is in `model_id`).

### Detail page URL uses `unique_id`, not numeric ID

The URL path segment is the subscription's `unique_id` (a short generated token, e.g. `66b3fa1...`). The numeric ID is internal — never exposed. The same `unique_id` is the foreign key on transactions and invoices for this subscription.

## Related

- [[subscriptions-detail]] — hub.
- [[subscriptions]] — the parent list.
- [[subscriptions-transactions]] — the transaction history rendered below the info cards.
- [[billing-cards]] — saved card used for renewal (there's no per-subscription card).
- [[expired-subscription]] — the takeover screen when the Plan subscription expires fully.

## Open questions

(All resolved.)
