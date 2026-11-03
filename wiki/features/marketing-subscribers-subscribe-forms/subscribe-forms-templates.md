---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms → Templates"
route_name: ""
route_path: ""
aliases: ["Subscribe form templates", "Form template picker", "Modal popup template", "Bar template", "Panel template", "Sidebar template", "Fullscreen template", "Шаблони за форма"]
tags: [marketing, subscribers, forms, templates, popup, layout, storefront]
plan_gates: ["subscriber_forms"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-subscribers-subscribe-forms]]. See the hub for the other aspects (list view, builder, layout, triggers, fields, submission flow, GDPR consent, known issues).

# Subscribe forms — structural templates

## Purpose

When the merchant opens [[subscribe-forms-builder]] for a **new** form, the first thing shown is a *"Choose template"* (BG: *"Избери шаблон"*) selector. This is **NOT** a content library of pre-filled industry templates (Newsletter, Exit-intent discount, Pre-launch waitlist, Black Friday). It's a picker for the **structural visual shape** the form will use. Once picked, the template seeds the form's `layoutPosition` defaults; the merchant then writes their own copy / picks their own media / picks fields.

The same five templates are used by every form regardless of intent.

## Where to find it

Inside the form builder iframe (loaded from [[subscribe-forms-list]] → Add form). Surfaces only on first creation; existing forms can change `layoutPosition` directly via the position picker (see [[subscribe-forms-layout]]) without re-running the template chooser.

## What the merchant can do here

- Pick one of five structural templates: modal, bar, panel, sidebar, fullscreen.
- Continue into the builder with `layoutPosition.desktop` + `layoutPosition.mobile` seeded by the template's defaults.

The template choice is a **starting point**, not a constraint. The merchant can override `layoutPosition` afterwards.

## Settings & fields

### The five built-in templates (keys verbatim from the builder source)

| Template key | Visual shape | Default `layoutPosition` (desktop / mobile) |
|--------------|--------------|---------------------------------------------|
| **`modal`** | Centered popup over a darkened backdrop. | (centered modal — no `layoutPosition` needed; effectively `centerCenter`) |
| **`bar`** | Slim full-width bar pinned to top or bottom of the page. | `topFull` / `topFull` (default — also supports `bottomFull`). |
| **`panel`** | Compact rectangular panel anchored to a screen corner. | `bottomLeft` / `bottomCenter`. |
| **`sidebar`** | Tall vertical strip pinned to the left or right edge of the page. | `left` / `full` (mobile collapses to a full-width sheet). |
| **`fullscreen`** | Takes over the entire viewport (modal-like, full-screen). | `full` / `full`. |

## Business rules

### No content library

There is **NO library of pre-filled content templates** ("Black Friday discount", "Pre-launch waitlist", "VIP early-access"). The merchant picks the structural shape only; copy and media are blank by default.

### Template is a seed, not a lock

After the merchant picks a template, the form's `layoutPosition` can be reconfigured freely (e.g. starting from `modal` and then changing `layoutPosition.desktop` to `topRight` is allowed). The template choice does not persist as a hard constraint on subsequent edits — it just seeds the initial position values.

### Mobile fallback patterns

Two templates have mobile-specific defaults that differ from desktop:

- **`panel`** — mobile defaults to `bottomCenter` (full-width drawer at the bottom) instead of the desktop `bottomLeft` (corner).
- **`sidebar`** — mobile collapses to `full` (full-width sheet) because a tall side strip is impractical on narrow viewports.

This is the only structural concession to mobile in the builder — beyond `layoutPosition`, the merchant has to use the per-device `media` slots and per-device styles to differentiate mobile from desktop. See [[subscribe-forms-layout]] for the full 15-value position enum.

### Template choice does not affect display triggers

The trigger array (`startDisplaying`) is template-independent — see [[subscribe-forms-triggers]]. For example, a `bar` template can still be set to `exitIntent` even though it stays pinned to the viewport edge.

### Template choice does not affect embedded mode

The `embedded` flag is orthogonal to template — a merchant can set `embedded = true` regardless of which structural template they started from, and the form will render inline at the snippet's position rather than as a popup. (When `embedded = true`, the platform forces `startDisplaying = [{type: 'auto'}]` and clears the included-URLs list — see [[subscribe-forms-builder]].)

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[subscribe-forms-layout]] — the full `layoutPosition` enum (15 values, per device).
- [[subscribe-forms-triggers]] — display-trigger array (independent of template).
- [[subscribe-forms-builder]] — the visual editor that surfaces the template picker.

## Open questions

None.
