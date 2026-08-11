---
type: feature
nav_path: "Marketing → Segments → Editor → Modal layout"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segment editor modal layout", "Segment editor regions", "Segment editor toolbar", "Segment editor header"]
tags: [marketing, segments, editor, modal]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-segments-editor]]. See the hub for the other aspects (condition builder, operators-and-values, create popup, validation, save pipeline, plan gates).

# Segment editor — modal layout

## Purpose

The Segment editor opens as a single large modal (size `xll`) on top of the [[marketing-segments]] list route. This page documents the modal's **shell** — its regions, its open / close behaviour, and the high-level "what can / cannot be done from here" before the merchant touches the condition tree itself. The condition-tree mechanics live in [[segments-editor-condition-builder]].

## Where to find it

From the [[marketing-segments]] list:

- **Create segment** (top-right) → opens the **Add segment** precursor popup first (see [[segments-editor-create-popup]]); picking a flow opens this modal.
- **Edit conditions** on any row → opens this modal pre-filled with that segment's conditions.
- Clicking the segment name in some places also opens it in Edit mode.

The route stays on `/admin/marketing-new/segments`. The modal pushes `?modal=create` or `?modal=edit&id=:id` (sometimes `?id=:id`) into the URL so the editor state survives refresh and back/forward. Closing the modal removes those query params and returns to the segment list.

The modal is large (size `xll`). Backdrop-click and Escape are **disabled** — the flags `no-close-on-backdrop` and `no-close-on-escape` are both true. The merchant must explicitly click Cancel or Save to close, so accidentally clicking off the modal does not lose the in-progress condition tree.

## Settings & fields

### Modal regions

| Region | What it does |
|--------|--------------|
| **Title** | "Create segment" (new) or "Edit segment" (existing). |
| **Plan-limit banner** | Red banner shown when the store is at/over the segment-feature limit. Contains the localised *"You have reached your subscriber limit"* message and a **Buy package** button linking to `/admin/plan/feature?mapping=subscribers`. Hidden for One-time segments (only Automated count toward the cap). See [[segments-editor-plan-gates]]. |
| **Conditions banner** | Info banner: *"All conditions have a logical AND"*. |
| **Header toolbar** (`SegmentHeader`) | Static label "Subscriber" on the left. (The original design called for a live summary line here — the code that renders it is **commented out** in the current build; the header always shows the literal word "Subscriber". An AND/OR toggle is **also commented out** in the same component — the segment engine still only supports AND at the top level.) On the right edge: a green **Add condition** link + plus-circle icon that emits `add-condition`. |
| **Conditions tree** | The actual condition rows — rendered as `SegmentConditionGroup` instances inside a `<ul class="cc-tree">` with vertical / horizontal connector lines. Empty-state placeholder: *"Add at least one condition to define your segment."*. See [[segments-editor-condition-builder]]. |
| **Footer** | Cancel + Save buttons. Save is disabled while a save request is in flight. |

The **summary line** above the conditions is an auto-generated human-readable name for the segment as currently configured (e.g., *"Subscribers who have spent more than 1500 in the last 180 days"*). For existing segments, this initially matches the backend-stored `conditions_formatted` until the merchant edits. As the merchant builds the tree, the derived `segmentSummary` recomputes in real time — on save it becomes the segment's display name (see [[segments-editor-save-pipeline]]).

## What the merchant can do here

- See the **conditions banner**: *"All conditions have a logical AND"*.
- See the **summary line** — auto-generated name from the current condition tree.
- Click **Add condition** (top-right of the toolbar) to add a new top-level condition row. A new empty row appears with the condition picker open and auto-scrolled into view.
- Pick a **condition type** from the searchable grouped dropdown — see [[segments-editor-operators-and-values]] for the operator + value vocabulary, and [[segments-editor-condition-builder]] for the row mechanics.
- **Add nested conditions** (green plus inside a condition row) — see [[segments-editor-condition-builder]].
- **Collapse / expand** a condition group (chevron at the row's left edge).
- **Remove** any row (trash icon — no confirmation inside the editor; final removal happens on Save).
- See **inline validation errors** under each field — surfaces backend validation by field key (e.g. *"You must select a specific records."* on a Product condition with no products picked). See [[segments-editor-validation]].
- **Save** — closes the modal, persists the conditions, refetches the segment list, toasts *"Segment created successfully."* / *"Segment updated successfully."*. See [[segments-editor-save-pipeline]].
- **Cancel** — discards the in-progress changes, resets the error store, returns to the segment list.
- **Buy package** — when at/over the plan's segment limit, the red plan-limit banner shows at the top with a Buy package button linking to `/admin/plan/feature?mapping=subscribers`.

## What the merchant cannot do here

- **Cannot rename the segment from the editor** — the display name comes from the auto-generated summary of conditions. To set a custom name, the merchant uses the separate **Rename** action on the [[marketing-segments]] list row (uses the `/admin/api/core/marketing/segments/:id/rename` endpoint with a `title` field — see [[segments-editor-save-pipeline]]).
- **Cannot change the segment type** from this modal — Type (One-time / Automated) is chosen on the **Add segment** popup ([[segments-editor-create-popup]]) and is immutable afterward. The editor does not expose a type toggle.
- **Cannot use OR at the top level** — the segment engine only composes top-level conditions with AND. (The internal data model supports an `or` separator and the editor renders an AND/OR toggle in source — but that toggle is commented out in the current UI; the segment always saves with AND.) For OR-like logic, the merchant creates a separate segment.
- **Cannot save with an empty tree** — at least one condition is required. The empty-tree placeholder reads *"Add at least one condition to define your segment."*. Backend validation message: *"You must have at least one row with conditions"*.
- **Cannot pick a condition that is not in the meta schema** — the condition picker is fed from the backend's available condition list (`/admin/api/core/marketing/segments/meta`), which already filters out app-provided conditions whose owning app is not installed/active. See [[segments-editor-validation]] for the meta-endpoint behaviour.
- **Cannot save with invalid combinations** — some conditions can only be combined with a whitelist of other conditions (e.g. `subscriber.missing_product`). Save returns the validation message and the modal stays open. See [[segments-editor-validation]].

## Business rules

- **Backdrop & Escape do not close the modal.** `no-close-on-backdrop` and `no-close-on-escape` are both true. This prevents accidental data loss when building deep condition trees.
- **Save is disabled while a save request is in flight.** Prevents double-submits.
- **Cancel and Close always reset the error store.** Re-opening the editor presents a clean slate (per the error-store behaviour documented in [[segments-editor-validation]]).
- **Modal size is `xll`.** The conditions tree can be large; the modal grows to accommodate it without horizontal scroll on common widths.

## Related

- [[marketing-segments-editor]] — hub.
- [[marketing-segments]] — parent list; the editor opens from here.
- [[segments-editor-create-popup]] — the precursor popup that runs before this modal opens in Create flow.
- [[segments-editor-condition-builder]] — the conditions-tree region's internals.
- [[segments-editor-validation]] — what surfaces inside the inline validation errors.
- [[segments-editor-save-pipeline]] — what happens on Save.
- [[segments-editor-plan-gates]] — when the plan-limit banner shows.

## Open questions

No outstanding questions.
