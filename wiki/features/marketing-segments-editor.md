---
type: feature
nav_path: "Marketing → Segments → Editor"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segment editor", "Segment conditions editor", "Segment condition builder", "Edit segment", "Create segment", "Сегмент редактор", "Редактор на сегмент", "Условия за сегмент", "Конструктор на сегмент"]
tags: [marketing, segments, editor, condition-builder]
plan_gates: ["segments", "subscribers", "subscribers-rfm"]
created: 2026-05-23
updated: 2026-06-10
source_count: 7
---
# Segment editor

## Purpose

The **Segment editor** is the modal where the merchant builds (or modifies) the rule tree that defines who qualifies for a segment. It is the heart of [[marketing-segments]] — without conditions, a segment has no audience. The editor is a **tree-shaped condition builder**: each top-level row is one condition; conditions can have nested child conditions; the whole tree is evaluated with **logical AND** (the help banner at the top of the modal says exactly *"All conditions have a logical AND"*); a subscriber must match every row in the tree to be attached to the segment.

The editor opens both for **create** (new segment from scratch / AI prompt / template) and for **edit** (existing segment's conditions). For an existing segment the merchant can change conditions and the segment will re-evaluate the entire subscriber population on save. The segment's `name` is generated from the conditions (a human-readable summary like *"Subscribers who placed an order in the last 30 days"*) — there is no separate "name" field on this modal; the segment's title is the auto-generated summary the merchant sees on the [[marketing-segments]] list (renamed via a separate Rename modal — see [[segments-editor-save-pipeline]]).

## Where to find it

From the [[marketing-segments]] list:

- Click **Create segment** (top-right) — opens the **Add segment** popup first (choose One-time / Automated / AI / Template — see [[segments-editor-create-popup]]), then the editor opens for the chosen flow.
- Click **Edit conditions** on any segment row — opens the editor pre-filled with that segment's existing condition tree.
- Click directly on the segment name in some places — opens the editor in Edit mode.

The route stays on `/admin/marketing-new/segments`. The modal pushes `?modal=create` or `?modal=edit&id=:id` (or sometimes `?id=:id`) into the URL so the editor state survives refresh and back/forward. Closing the modal removes those query params and returns to the segment list.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[segments-editor-modal-layout]] — modal regions (title, plan-limit banner, conditions banner, header toolbar, conditions tree, footer); large `xll` size; `no-close-on-backdrop` / `no-close-on-escape` behaviour; what the merchant can / cannot do at a high level.
- [[segments-editor-condition-builder]] — `SegmentConditionGroup` mechanics; chevron collapse / expand; green-plus nesting; red-trash removal; composite `parent::child` key disambiguation; scroll-into-view on add; the `cc-tree` visual hierarchy.
- [[segments-editor-operators-and-values]] — operator vocabulary by `value_kind` (Default, Numeric, Date interval, Exact date, Text, Membership, Feedback rating, etc.); value-control vocabulary per condition (Channel, Date, Country, Customer, Products, Tag, UTM, Device type, Custom field, etc.).
- [[segments-editor-create-popup]] — the **Add segment** precursor popup (New from scratch / Generate with AI / Predefined template); 6 built-in templates; AI-generate prompt rules + `mini` model parameters.
- [[segments-editor-validation]] — required-row validation; `getIsDisabledByAllConditions` + recursive `validate`; field-mapped errors (`conditions.0.conditions.3.value`); legacy-key normalisation (`cart` → `marketing.segments.conditions.cart`); error-store + toast de-dup; meta-endpoint caching (5 min) + per-condition scoped schema.
- [[segments-editor-save-pipeline]] — Create POST + Update PUT endpoints; `set_subscribers_to_single_segment` queue dispatch + recurring task registration; `SegmentCreated` / `SegmentUpdated` events; transactional `processing = 1, active = 1` write; separate Rename endpoint.
- [[segments-editor-plan-gates]] — `segments` (Automated cap) + `subscribers` (red plan-limit banner + Buy package button → `/admin/plan/feature?mapping=subscribers`) + `subscribers-rfm` (boolean — whether `subscriber.rfm` shows in the picker).

## What the merchant can do here

At hub level, the editor lets the merchant declare an audience by building an AND-chain of conditions. The detailed action set is distributed across the aspect pages:

- Open the editor in Create mode via the precursor popup (scratch / AI / template) — see [[segments-editor-create-popup]].
- Open the editor in Edit mode (pre-filled with the segment's existing conditions) — see [[segments-editor-modal-layout]].
- Add / remove / nest / collapse condition rows — see [[segments-editor-condition-builder]].
- Pick an operator and enter a value per condition — see [[segments-editor-operators-and-values]].
- Save (Create POST or Update PUT) which immediately rebuilds the subscriber population — see [[segments-editor-save-pipeline]].
- Buy a package when at/over the plan-feature cap — see [[segments-editor-plan-gates]].

## Settings & fields

The hub does not own any unique fields. Each aspect documents the fields it owns:

- Modal regions + the **Add condition** toolbar control — [[segments-editor-modal-layout]].
- Condition row anatomy (key / operator / value / actions) + composite `parent::child` keys — [[segments-editor-condition-builder]].
- Operator vocabulary by `value_kind` + the full value-control table per condition — [[segments-editor-operators-and-values]].
- Precursor popup option cards + 6 built-in templates + AI-generate parameters — [[segments-editor-create-popup]].
- Meta endpoint shape (`module_id`, `mapping`, `allow_value`, `value_kind`, `group`, `sub_conditions`) + 5-minute cache — [[segments-editor-validation]].
- Create POST / Update PUT / Rename PUT endpoints + `set_subscribers_to_single_segment` queue job + `SegmentCreated` / `SegmentUpdated` events — [[segments-editor-save-pipeline]].
- Plan-feature mappings (`segments`, `subscribers`, `subscribers-rfm`) + Buy package button → `/admin/plan/feature?mapping=subscribers` — [[segments-editor-plan-gates]].

## Business rules

Hub-level invariants that touch every aspect (each aspect page documents its own detailed rules):

- **AND-only at the top level.** The help banner *"All conditions have a logical AND"* is the literal rule. For OR-like logic, the merchant creates a separate segment.
- **Type is immutable.** One-time / Automated is chosen on the precursor popup and cannot be changed afterward.
- **No JSON-API v2 write path.** Segments are read-only at [[api-segments]]; integrations feed audiences via tags on subscribers and define a tag-based Automated segment in the visual builder.
- **Save runs an immediate full-population rebuild** — even One-time segments rebuild on save via the `segments` queue. See [[segments-editor-save-pipeline]].
- **Plan-feature counts are type-aware.** Only Automated segments count toward the `segments` cap; the `subscribers` cap drives the red plan-limit banner only for Automated. See [[segments-editor-plan-gates]].

## Plan gates summary

Three plan-features interact with the editor (full mechanics on [[segments-editor-plan-gates]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `segments` | Numeric | Max Automated segments. Editor's "Automated" choice in the precursor popup is blocked at cap. |
| `subscribers` | Numeric | Red plan-limit banner with **Buy package** button → `/admin/plan/feature?mapping=subscribers` when the store is at/over the marketable-subscriber cap. Hidden for One-time. |
| `subscribers-rfm` | Boolean | Whether the `subscriber.rfm` condition appears in the searchable condition picker. |

Numeric gates extend via packs ([[plan-vs-feature-pack]]); the boolean `subscribers-rfm` requires a plan upgrade.

## Related

- [[marketing-segments]] — parent list; the editor saves here.
- [[marketing-segments-subscribers]] — sibling; shows WHO matches the conditions the editor builds.
- [[marketing-segments-log]] — sibling; audit trail of add/remove events triggered by the editor's save.
- [[marketing-subscribers]] — the subscriber population the editor's rules filter.
- [[marketing-subscribers-custom-fields]] — custom fields that show up as a condition value-control here.
- [[marketing-subscribers-subscribe-forms]] — produces subscribers + can be filtered via the `from_form` condition.
- [[marketing-campaigns]] — campaigns target the segments the editor produces.
- [[marketing-discounts]] — discounts can require a segment match (audience-targeted promotions).
- [[apps-cart-rules]] — shares the same condition *family / vocabulary* (customer-group, product, tag, amount, …), but the two systems have **separate** condition-manager implementations — Cart Rules matches via its own `CartRuleMatches` filters, Segments via `*ConditionManager` classes; they do not share manager classes.
- [[apps-product-review]] — contributes review-related conditions when installed.
- [[segment]] — entity page.
- [[api-segments]] — read-only JSON-API v2 resource (no write path).
- [[api-subscribers]] / [[api-subscribers-tags]] — programmatic audience-feed workaround.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — plan-feature substrate.

## Open questions

No outstanding questions.
