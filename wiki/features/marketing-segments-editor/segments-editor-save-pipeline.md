---
type: feature
nav_path: "Marketing → Segments → Editor → Save pipeline"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segment editor save", "Segment editor save pipeline", "Segment editor side effects", "Segment editor rename endpoint", "set_subscribers_to_single_segment", "Programmatic segments"]
tags: [marketing, segments, editor, save, side-effects, queue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-segments-editor]]. See the hub for the other aspects (modal layout, condition builder, operators-and-values, create popup, validation, plan gates).

# Segment editor — save pipeline

## Purpose

When the merchant clicks **Save**, the editor walks the in-memory condition tree, serialises it into the request payload, calls Create (POST) or Update (PUT), and the backend persists + dispatches downstream re-evaluation jobs + fires events. This page documents the payload-build step, the two endpoints, the immediate side effects, and why there is no JSON-API v2 write path. The validation that runs at request time is on [[segments-editor-validation]].

## Where to find it

The Save button lives in the editor modal's footer (see [[segments-editor-modal-layout]]). It is disabled while a save request is in flight.

## What the merchant can do here

- **Click Save** to persist the in-memory condition tree (Create POST or Update PUT) and trigger the immediate full-population rebuild.
- **Click Cancel** to discard in-progress changes (resets the error store, closes the modal, returns to the segment list).
- See the **success toast** — *"Segment created successfully."* or *"Segment updated successfully."* — and watch the segment row's spinner spin until the queue job completes.
- See the segment-list placeholder *"Your subscribers are currently being filtered, please check again later"* while large stores chunk the rebuild in 500-row batches.
- **Rename** an existing segment via the separate Rename action on the [[marketing-segments]] list row (uses `/admin/api/core/marketing/segments/:id/rename` with `{title}`).

## Settings & fields

The save aspect itself has no merchant-editable fields — it serialises the conditions tree built on [[segments-editor-condition-builder]] and the type chosen on [[segments-editor-create-popup]]. The save endpoints:

| Endpoint | Method | Path | Payload | Toast |
|---|---|---|---|---|
| Create | POST | `/admin/api/core/marketing/segments` | `{type: 'regular' \| 'automated', conditions: [...]}` | *"Segment created successfully."* |
| Update | PUT | `/admin/api/core/marketing/segments/:id` | `{conditions: [...]}` (type immutable) | *"Segment updated successfully."* |
| Rename | PUT | `/admin/api/core/marketing/segments/:id/rename` | `{title: 'new name'}` | (list toast) |

Both Create and Update return the full segment object with `conditions`, `conditions_formatted`, `processing`, and timestamps.

## Payload build

On Save the editor walks the in-memory tree and:

- **Normalises composite (`parent::child`) keys** to top-level wrappers with nested children (see [[segments-editor-condition-builder]]).
- **Strips undefined / empty values.**
- **For `date_interval` values**, only includes the value when the `interval` is a valid non-negative number.
- **For `date` values**, strips the time portion and emits `YYYY-MM-DD`.
- **For `channel.verified` conditions**, forces `value = 1` (the only valid value).
- **Recursively processes nested conditions.**

The resulting payload is sent to POST (Create) or PUT (Update).

For Automated segments, the Create call also refetches the meta query to update the plan-feature counters (see [[segments-editor-plan-gates]]). The backend requires conditions to be a non-empty array and each row's key to be a known condition key, then runs the full tree through request-time validation — see [[segments-editor-validation]] for the lifecycle.

### Performance — chunked re-evaluation on the queue

After Save, the subscriber population is re-evaluated against the new conditions on a background queue. For large stores this is **chunked in 500-row batches**. While the job runs, the [[marketing-segments]] list shows the placeholder *"Your subscribers are currently being filtered, please check again later"* on that segment's row, and the row's spinner spins. The **"Last generated at"** timestamp updates when the job completes; the [[marketing-segments-log]] records the additions/removals.

### Live summary while editing

As the merchant builds the tree, a derived summary recomputes in real time. It is shown in the toolbar above the conditions and becomes the segment's display name on save (stored as `conditions_formatted`). If the merchant doesn't change conditions in Edit mode, the summary stays equal to the originally-stored formatted name (no churn).

### Rename uses a separate endpoint

Renaming a segment hits `PUT /admin/api/core/marketing/segments/:id/rename` with `{title: 'new name'}` — this updates the `title` column (NOT `name`, the auto-summary). The editor never sets `title` itself; the segment's display falls back to `name` when `title` is empty. The Rename action is on the [[marketing-segments]] list row (per-row menu), not in this editor modal.

## Programmatic access

The segment editor has **no JSON-API v2 write path** — segments are exposed at [[api-segments]] as **read-only**. POST / PATCH / DELETE are not registered because the `conditions` rule tree is a deeply nested payload only the visual builder produces correctly. Reasons:

- The schema is fed from a meta endpoint that gates conditions by installed apps.
- Parent-scoped resolution for ambiguous keys (`product` under `view` vs under `subscriber`) requires the disambiguation logic on [[segments-editor-condition-builder]].
- Normalises composite `parent::child` keys.
- Runs each value through a per-condition validator that depends on store-specific context (customers exist, products exist, etc.).

The API deliberately hides `conditions` and `conditions_formatted` from response payloads for the same reason.

**Workaround for programmatic audiences.** Integrations that want to feed an audience from outside the platform create subscribers via [[api-subscribers]] + [[api-subscribers-tags]], then define an Automated segment in the admin panel with a tag-based rule. The tag becomes the integration contract; the rule tree stays in the visual builder.

See [[json-api-v2]] for authentication, rate limits, and the side-effects principle.

## Business rules

- **Save runs an immediate full-population rebuild.** Even One-time segments rebuild on save — no separate "Generate" click.
- **Save sets `processing = 1`, `active = 1`, `inactive_errors = null` atomically** — even if the merchant didn't touch active. It also sets `name` to the auto-generated `conditions_formatted` text.
- **A segment-created (new) or segment-updated (edit) event fires downstream** on every successful save, so any subscribed webhook is notified.
- **The rebuild job is single-flighted** per segment — back-to-back saves do not stack jobs.
- **The recurring 5-minute Automated sweep is registered on first save** and covers the segment going forward.
- **`processing` flips to 0 on job completion** — the segment list's 3-second polling shows the spinner until the flag clears.
- **Rename is a separate endpoint, separate column** — `title` vs `name`; display falls back to `name` (auto-summary) when `title` is empty.

## Related

- [[marketing-segments-editor]] — hub.
- [[segments-editor-modal-layout]] — the Save button + the toolbar summary line that becomes `conditions_formatted`.
- [[segments-editor-condition-builder]] — composite-key unwrap that the payload builder runs.
- [[segments-editor-validation]] — request-time validation that gates the persist step.
- [[segments-editor-create-popup]] — the type (`regular` / `automated`) that the Create payload carries.
- [[segments-editor-plan-gates]] — meta query refetch on Create of an Automated segment.
- [[marketing-segments]] — segment list polling + spinner + "Last generated at" timestamp.
- [[marketing-segments-log]] — audit trail of add/remove events from the rebuild job.
- [[marketing-segments-subscribers]] — the list of subscribers the rebuild populates.
- [[api-segments]] — read-only JSON-API v2 resource (no write path).
- [[api-subscribers]] / [[api-subscribers-tags]] — programmatic audience-feed workaround.
- [[json-api-v2]] — auth, rate limits, side-effects principle.

## Open questions

No outstanding questions.
