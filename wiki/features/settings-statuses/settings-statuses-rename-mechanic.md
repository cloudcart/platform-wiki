---
type: feature
nav_path: "Settings → Statuses → (rename mechanic)"
route_name: statuses
route_path: /admin/settings/statuses
aliases: ["Status rename override", "Translation override", "Rename vs translation", "Clearing a rename", "Status label precedence"]
tags: [settings, statuses, translations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-statuses]]. See the hub for the three taxonomies (orders, shipping, payment) and the other cross-cutting mechanics (custom codes, delete protection, permissions).

# Statuses — rename mechanic

## Purpose

A merchant typing a value into the "New status name" column of [[settings-statuses]] is not editing an enum value — they are creating a **translation override**. This page documents how that override is stored, how it interacts with [[settings-translations]] (per-language labels), what happens when the field is cleared, and the practical merchant consequences for multi-language stores. This mechanic is identical across all three taxonomies (orders / shipping / payment) but is the most-misunderstood part of the page, so it gets its own aspect.

## Where to find it

The rename input is on every row of every tab on [[settings-statuses]] — "New status name" column. The behaviour documented here applies to all three taxonomies equally:

- [[settings-statuses-orders-tab]]
- [[settings-statuses-shipping-tab]]
- [[settings-statuses-payment-tab]]

## What the merchant can do here

- **Rename a built-in or custom status** by typing in the "New status name" field and clicking the per-row Save button.
- **Clear a rename** by emptying the "New status name" field and clicking Save — this deletes the override row entirely, restoring the platform's default translation.
- **Combine renames with [[settings-translations]]** to get per-language labels (see "Per-language labels" below).

What the merchant **cannot** do via the rename mechanic:

- Set different labels per storefront language from this page — the rename is a single string applied to every language. For per-locale labels see [[settings-translations]].
- Change the status CODE — only the display label. The code stays `pending`, `paid`, etc. forever; webhooks and integrations always see the code, never the renamed label.
- Have an empty rename "stick" — an empty value deletes the override row rather than storing an empty-string override. So you cannot use a blank rename to "hide" the platform's default label.

## Settings & fields

The "New status name" cell is a single text input (one per row) plus a hidden per-row Save button that becomes visible only when the field's value differs from the previously-saved value.

| Field | Notes |
|-------|-------|
| **status** | The status code being overridden (e.g., `pending`, `paid`, or the slug-generated code for a custom status). Sent as part of the PATCH payload, not editable in the UI. |
| **name** | The new label. Empty string is treated as "clear override" — the platform deletes the row rather than storing `""`. |
| **type** | The taxonomy (`order`, `shipping`, `payment`). Driven by the active tab; not user-editable. |

The PATCH endpoint is `PATCH /statuses/<type>/update`. Validation rules on [[settings-statuses-permissions-validation]].

## Business rules

### What the override actually stores

When the merchant fills "New status name" and saves, the platform stores a row with `(type=<order|shipping|payment>, status=<code>, name=<custom value>)`. The platform's status-rendering layer reads this row first; if it's missing, the platform falls back to the built-in translation key (`order.status_<code>`, `shipping.status_<code>`, `payment.status_<code>`).

So the override is a **set-aside** layer over the platform's default translations.

### Clearing a rename deletes the override row entirely

When the merchant clears the "New status name" field for a built-in status (e.g., for `pending`) and saves, the platform does NOT store an empty-string row — it **deletes the override row** for that `(type, status)` pair. The platform's status-rendering layer then falls back to the default translation (`order.status_pending`, etc.) on next read.

The practical effect: **clearing a rename and saving is reversible**. The merchant can re-enter a rename at any time and a new override row is created. No row → no history.

This also means a merchant cannot use a blank rename to make a status display as an empty string. To get a near-blank label, the merchant would have to type something like a single space and save — and even then the platform may trim leading / trailing whitespace at display time. *(verify)*

### Renaming doesn't affect the underlying code or integrations

Webhooks, API clients, exports, and any code referring to a status sees the unchanged `code` (e.g., `paid`, `completed`); only the human-facing label changes. This is the property that makes renaming safe — the merchant can rename freely without breaking gateway integrations, ERP exports, or [[settings-hooks]] subscribers.

### Per-language labels — rename vs translation precedence

For every status, the platform carries **two separate labels**:

- **The merchant's rename** (this page) — a **global** override that applies to every storefront language identically. Stored in the status-override table.
- **The platform's per-language translation** (the platform's translation files, separately overridable via [[settings-translations]] per locale) — varies per storefront language.

The precedence rule is: **the merchant's rename takes priority over the per-language translation**.

| Scenario | Status `pending` renders as |
|----------|------------------------------|
| No rename, BG storefront | `order.status_pending` → "Изчакваща" |
| No rename, EN storefront | `order.status_pending` (often empty in EN) → fallback or raw code |
| Rename = "Awaiting confirmation", BG storefront | "Awaiting confirmation" (rename wins, even though BG would have "Изчакваща") |
| Rename = "Awaiting confirmation", EN storefront | "Awaiting confirmation" |

### How to get true per-language labels

If the merchant wants `pending` to read as "Awaiting confirmation" in English and "Изчакваща" in Bulgarian, they must:

- **Leave the rename field blank** on [[settings-statuses]] (so the platform falls back to per-language translations), AND
- **Override the per-language translation key** (`order.status_pending`) per locale via [[settings-translations]].

If they rename here, the same English text will show in every storefront language, including Bulgarian — which is usually NOT what the merchant wants for a multilingual store.

### Custom statuses have NO platform translation fallback

Custom order statuses (created via [[settings-statuses-orders-tab]]) carry a slug code like `order-available-in-3-days`, but the platform has no translation file row for that code. The display falls back to the merchant's rename only — there is no per-language alternative.

To translate a custom status into multiple languages, the merchant must use [[settings-translations]] with a manually-added key (advanced workflow). Without that, the custom status displays the same text on every storefront language.

### Renaming a custom status does NOT change its code

If the merchant created "Available in 3 days" (code: `order-available-in-3-days`) and later renames it to "Coming next week", the code stays `order-available-in-3-days`. Webhooks and integrations that referenced the old code continue working. The label change is purely cosmetic. See [[settings-statuses-custom-codes]] for the full code-vs-name story.

## Related

- [[settings-statuses]] — hub.
- [[settings-statuses-orders-tab]] — orders tab; rename + add + delete.
- [[settings-statuses-shipping-tab]] — shipping tab; rename only.
- [[settings-statuses-payment-tab]] — payment tab; rename only.
- [[settings-statuses-custom-codes]] — how custom statuses get their codes (and why renaming a custom doesn't change its code).
- [[settings-translations]] — per-language translation overrides; the way to get truly per-locale status labels.
- [[settings-hooks]] — webhooks always send the unchanged status code; renames don't affect them.

## Open questions

- Whether the platform trims leading / trailing whitespace from rename values at display time — relevant if a merchant tries a single-space rename to hide a label. *(verify)*
