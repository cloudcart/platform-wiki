---
type: feature
nav_path: "Marketing → Segments → Editor → Validation"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segment editor validation", "Segment editor error store", "Segment condition manager validation", "Allowed combinations check", "Legacy key normalisation", "Meta endpoint cache"]
tags: [marketing, segments, editor, validation, error-handling]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-segments-editor]]. See the hub for the other aspects (modal layout, condition builder, operators-and-values, create popup, save pipeline, plan gates).

# Segment editor — validation

## Purpose

The Segment editor surfaces both **per-row validation** (key required, value required when the schema says so) and **cross-row validation** (allowed-combinations rules — e.g. `subscriber.missing_product` can only be combined with a whitelist of other conditions). This page documents the validation lifecycle, the error-store behaviour, the meta-endpoint that feeds the picker, and the legacy-key normalisation that runs when an existing segment opens for edit.

## Where to find it

Validation errors render inline next to the failing field (red text under the input). If there are multiple inline errors, the modal also scrolls to the first one. If a field-level error is present but no DOM error indicator can be rendered, the editor toasts the consolidated message. Cancel and Close always reset the error store.

## What the merchant can do here

- **Read inline validation messages** beneath any failing field (red text under the input).
- **Read the consolidated banner / toast** for cross-row errors (allowed-combinations check, empty-tree check) at the top of the modal.
- **Cancel** to wipe the error store; re-opening the editor presents a clean slate.
- **Resolve errors and retry Save** — the editor keeps the modal open while errors are present; the merchant fixes inputs and clicks Save again.

## Settings & fields

The validation aspect has no merchant-editable fields of its own — it inspects the conditions tree built on [[segments-editor-condition-builder]]. The data sources that drive validation:

- **Meta endpoint** — `/admin/api/core/marketing/segments/meta` (5-minute cache, no refetch-on-mount) returns the full condition schema keyed by `module_id` with `mapping`, `allow_value`, `value_kind`, `group`, `group_display`, `sub_conditions`. Forced through the `en` locale.
- **Scoped condition endpoint** — `/admin/api/core/marketing/segments/condition/:key` with a `parent` query param, used to disambiguate ambiguous keys (`product` under `view` vs under `subscriber`).
- **Stored conditions** — `/admin/api/core/marketing/segments/:id` (fresh on every modal open, `staleTime: 0`).
- **Error-store** — per-field map keyed by paths like `conditions.0.conditions.3.value`.

## Business rules

### One required top-level condition; at least one row in the tree

Save is blocked if the conditions array is empty. Backend validation messages (English):

- *"You must have at least one row with conditions"* (empty array)
- The empty-state placeholder in the modal reads *"Add at least one condition to define your segment."*

If the merchant tries to save with no conditions, the modal shows the validation error and stays open.

### Each row needs a condition key + (where applicable) operator + value

For conditions where `allow_value = true`:

- **Key** is required (validation: *"The condition key is required"* — field `conditions.<index>.key`).
- **Operator** must be one of the allowed operators for that condition's `value_kind` (see [[segments-editor-operators-and-values]]).
- **Value** is required when the schema says so — e.g. *"You must select a specific records."* on a product multi-select.

Field-level errors are surfaced inline next to the failing field. If multiple inline errors exist, the modal scrolls to the first one. When a field-level error cannot be rendered next to a DOM input, the editor falls back to a consolidated toast.

### Validation runs through the condition manager (allowed-combinations rules)

On save the backend runs the full condition tree through the segment's condition manager. Two checks happen at request time:

1. **`getIsDisabledByAllConditions`** — runs first; checks for inherent incompatibilities (e.g., `subscriber.missing_product` combined with disallowed conditions). Returns FALSE with the combined messages stored under `conditions.conditions_validate`. The merchant sees the message at the top of the modal. Verbatim error message: *"The condition ':condition' can only be combined with the following conditions: ':conditions'"*.
2. **`validate`** — when check 1 passes, recursively walks every nested condition row checking per-condition rules (e.g. customer ids must exist, percent values must be 0–100, date intervals must be positive integers). Errors are surfaced field-mapped (e.g. `conditions.0.conditions.3.value`) so the editor highlights the exact failing input.

If validation throws `ModuleNotExists` (a referenced condition module is uninstalled), the validator returns TRUE silently — the segment saves, but it will auto-disable on the first evaluation run (see [[marketing-segments]] → "Allowed-combinations check happens at evaluation time").

### Error-store behaviour

Validation errors from save are surfaced via the per-field `errorStore`:

- Condition-field errors (matching the pattern `conditions(.<n>.conditions)*.<n>.(key|operator|value)`) render inline next to the field.
- Non-field errors render as a top-of-modal banner / toast.
- The modal de-dupes consecutive identical error toasts (signature-keyed) to avoid spamming the merchant.
- Cancel and Close always reset the error store.

### Meta endpoint feeds the condition picker

The editor's condition picker is fed from the **meta endpoint** (`/admin/api/core/marketing/segments/meta`) which returns the full condition schema for the merchant's account — including only conditions whose owning module/app is installed and active. The schema is keyed by `module_id` (e.g. `marketing.segments.conditions.product`) with:

- `mapping` strings (e.g. `subscriber_product`)
- an `allow_value` flag
- a `value_kind` (`numeric`, `currency`, `date_interval`, `date`, etc. — see [[segments-editor-operators-and-values]])
- a `group` / `group_display` for the picker grouping
- nested `sub_conditions`

The response is built from a fresh `SubscribersSegment` instance and its condition manager (`getConditionManager->toArray`), forced through the `en` locale so the API surface is language-stable. Same path serves the per-condition `/condition/{key}` endpoint, with the parent-subtree disambiguation logic described in [[segments-editor-condition-builder]] (composite `parent::child` keys).

### Meta endpoint caching

- **5-minute cache** (`staleTime: 5 * 60 * 1000`) — refetch-on-mount is OFF, so opening the editor multiple times in 5 minutes does NOT re-hit the schema endpoint. After plan-feature purchases the meta query is invalidated explicitly so the picker reflects the unlocked conditions.
- The segment's stored conditions (`/admin/api/core/marketing/segments/:id`) are **fresh on every modal open** (`staleTime: 0`) — Edit-mode pre-fill always reads current data.

### Edit mode: pre-fill from server, normalise legacy keys

When opening for an existing segment, the editor:

1. Fetches the condition meta schema (`/admin/api/core/marketing/segments/meta`) — cached for 5 minutes.
2. Fetches the segment's stored conditions (`/admin/api/core/marketing/segments/:id`) — fresh.
3. Runs the stored conditions through a **key-normaliser** that promotes legacy short keys (`cart`, `product`) to full module ids (`marketing.segments.conditions.cart`, `marketing.segments.conditions.product`).
4. Applies **legacy rewrites** — e.g. the legacy `date_interval` child under `subscriber` is rewritten to `subscriber.last_active`.

The merchant doesn't see any of this — the editor just opens with the conditions correctly pre-filled. The same normaliser also runs on AI-generated output (see [[segments-editor-create-popup]]).

### Inline error auto-expand

If a nested condition has a validation error, its parent group auto-expands so the merchant can see the failing field (see [[segments-editor-condition-builder]] for the chevron's `collapsed` state).

### Composite-key validation

When a row uses a composite `parent::child` key (see [[segments-editor-condition-builder]]), the validator runs against the unwrapped form (top-level `view` with nested `product` child, not the literal the platform code). Errors come back keyed against the unwrapped path (e.g. `conditions.0.conditions.0.value` for the nested `product` row's value).

## Related

- [[marketing-segments-editor]] — hub.
- [[segments-editor-modal-layout]] — where inline + banner / toast errors render.
- [[segments-editor-condition-builder]] — composite-key disambiguation that this validation handles.
- [[segments-editor-operators-and-values]] — operator + value-control vocabulary the schema declares.
- [[segments-editor-create-popup]] — AI-generate flow uses the same condition manager for final validation.
- [[segments-editor-save-pipeline]] — where validated payloads are POSTed / PUT.
- [[marketing-segments]] — auto-disable on evaluation when `ModuleNotExists`.

## Open questions

No outstanding questions.
