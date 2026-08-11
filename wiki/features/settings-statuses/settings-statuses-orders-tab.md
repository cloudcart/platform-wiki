---
type: feature
nav_path: "Settings → Statuses → Orders"
route_name: order-statuses
route_path: /admin/settings/statuses/order
aliases: ["Order statuses tab", "Orders status taxonomy", "Add custom order status", "Delete custom order status", "Статуси на поръчки"]
tags: [settings, statuses, orders]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-statuses]]. See the hub for the other taxonomies (shipping, payment) and the cross-cutting mechanics (rename, custom codes, delete protection, permissions).

# Statuses — Orders tab

## Purpose

The Orders tab of [[settings-statuses]] is the only one of the three taxonomies where the merchant can do more than rename — they can also **add new custom order statuses** and **delete custom ones** (provided no orders are currently attached to that status). This makes the Orders taxonomy extensible: the merchant can carve out workflow states the platform's 11 built-ins don't already cover (e.g., "Awaiting supplier", "Available in 3 days", "Quality check").

## Where to find it

Sidebar → Settings → **Statuses** → **Orders** tab (default tab — the page lands here when no tab segment is given in the URL). Route: `/admin/settings/statuses/order`.

## What the merchant can do here

- See all 11 built-in order statuses listed with their current merchant-facing labels.
- **Rename** any built-in status by typing a new name inline in the "New status name" column. A per-row **Save** button appears when the value differs from the saved value; the merchant clicks it to commit (no auto-save on blur / Enter — see Settings & fields below).
- **Add a new custom status** by clicking the **+ Add status** button in the page header — opens a modal with a single "Status name" field (placeholder: *"Example: Available in 3 days"*). The custom status appears immediately in the list with `custom: true` flag.
- **Delete a custom status** by clicking the trash icon in the Actions column. Built-in statuses cannot be deleted (no delete button is shown for them based on `custom` flag). See [[settings-statuses-delete-protection]] for the attached-orders gate.

What the merchant **cannot** do:

- Delete built-in statuses (no Delete button rendered for them; backend also rejects).
- Change the status CODE (e.g., turn `pending` into `awaiting_payment`) — only the display label can change. Status codes are wired throughout the platform's logic and remain stable. See [[settings-statuses-custom-codes]] for how a custom status's code is generated from its name.
- Reorder statuses — the table renders them in a fixed platform-defined order (built-ins first in their canonical sequence, then custom statuses appended in creation order).
- Set per-language labels here — the renamed value is a single string applying to every storefront language. For per-locale labels see [[settings-statuses-rename-mechanic]] and [[settings-translations]].

## Settings & fields

### Per-tab table

| Column | Shows | Editable? | Notes |
|--------|-------|-----------|-------|
| **Current status name** (`translation`) | The original translated label for the status code (from the platform's translation system, e.g., `order.status_<code>`). | No | Read-only display of what the platform calls this status before merchant overrides. |
| **New status name** (`new_name`) | The merchant's custom rename, or empty if unset. | Yes (inline) | A per-row Save button (shown only when the value differs from saved) commits via `PATCH /statuses/order/update` — no auto-save on blur. |
| **Actions** | Trash icon. | n/a | Shown only for custom statuses (`custom: true`). |

### Add-status modal (Orders only)

- **Size**: `lg`. **Title**: "Add status".
- **Body**: A single section with the heading *"Create new status"* above the `Status name` text input. Placeholder: *"Example: Available in 3 days"*.
- **Save button**: validates that `name` is non-empty (otherwise *"There is no name for the status."* is shown inline) and POSTs to `/statuses/order/create` with `name` in the body.
- **Defensive client check**: If the modal is invoked while the merchant is somehow on the Shipping or Payment tab (it should be hidden in those cases), the create handler short-circuits with toast *"Only order statuses can be created"* before any API call.
- **Backdrop close**: enabled. The merchant can dismiss by clicking outside or pressing Esc.
- **Reset on close**: name + errors are cleared every time the modal closes (so re-opening starts blank).
- **On success**: toast *"Successfully created"* and the new status is added to the table; on backend error, toast *"Error while creating the status"* and any field-level errors from the response bind back to the form.

### Inline rename UX

- Typing in a name shows the Save button on that row.
- Reverting back to the original name hides the Save button again — no accidental no-op saves.
- Clicking Save sends `PATCH /statuses/order/update` with `{ status: <code>, name: <new value> }`. Errors revert the local field to the previously-saved value.
- **No auto-save on blur or Enter** — the merchant must click the Save button explicitly. (Older notes hinted at "save on blur"; the actual implementation requires button click.)

### Delete UX

- The trash icon appears only on rows where `custom: true`.
- Clicking the trash icon opens a small inline confirmation popover — *"Are you sure?"* Yes / No.
- Confirming sends `DELETE /statuses/order/<status>` (the slug-code, not numeric id).
- Success → row is removed; toast *"Deleted successfully"*.
- Failure (orders attached) → toast with the backend error string *"This status has attached: `<N>`"* and the row stays. Full mechanics on [[settings-statuses-delete-protection]].

## Business rules

### The 11 built-in order statuses (in display order)

`authorized`, `pending`, `voided`, `timeouted`, `cancelled`, `failed`, `refunded`, `chargebacked`, `paid`, `completed`, `disputed`.

Custom statuses created by the merchant are appended after these 11 in the table, in creation order.

### Custom statuses are flagged `custom: true`

The API response marks each status with a `custom` boolean. The merchant-facing table doesn't surface this flag visually, but it drives the Delete-column visibility client-side and the delete eligibility server-side. Built-in statuses (`custom: false`) are protected from deletion regardless of attached-orders count.

### Saves are immediate; no draft

There is no "Save" button at the page level. Each rename or create is a separate API call (paginated table with inline-edit pattern). The merchant sees immediate save / error feedback per row.

### `status_draft` exists but is NOT in the 11 built-in order statuses

The canonical 11 do NOT include `draft`, yet the platform's translation file has a label `Чернова` for it. This suggests an additional internal "draft" state used somewhere (possibly admin-side order workflow). Worth tracking if a merchant mentions a "Draft" status they can't find in the admin. *(verify)*

### Default Bulgarian status labels (sample, for reference)

- `status_authorized` → "Оторизирано плащане"
- `status_paid` → "Платена"
- `status_pending` → "Изчакваща"
- `status_fulfilled` → "Изпратена" (shipping taxonomy — see [[settings-statuses-shipping-tab]])
- `status_draft` → "Чернова"

Many of the English-language defaults are EMPTY strings — Bulgarian is the primary localisation for status labels. English-locale stores often see the raw code or the merchant's custom rename. The rename overrides this default — see [[settings-statuses-rename-mechanic]].

## Related

- [[settings-statuses]] — hub.
- [[settings-statuses-rename-mechanic]] — what the rename actually stores and how it interacts with [[settings-translations]].
- [[settings-statuses-custom-codes]] — how a custom status NAME becomes an internal CODE; integration consequences.
- [[settings-statuses-delete-protection]] — the attached-orders count gate that blocks deleting a custom status in use.
- [[settings-statuses-permissions-validation]] — `settings.statuses` permission grant + server-side Form Request validation.
- [[order-status]] — entity page.
- [[order-status-workflow]] — how statuses transition on an order.
- [[orders-status-change]] — the order-side flow for changing a status.

## Open questions

- The presence of `status_draft` in the translation file but not in the 11 built-ins — is this a remnant of an older workflow, or an internal state surfaced elsewhere in the admin? *(verify)*
