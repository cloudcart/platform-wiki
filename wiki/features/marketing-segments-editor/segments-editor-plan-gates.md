---
type: feature
nav_path: "Marketing → Segments → Editor → Plan gates"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segment editor plan gates", "Segment editor plan-limit banner", "Buy package banner", "segments plan feature", "subscribers plan feature", "subscribers-rfm plan feature"]
tags: [marketing, segments, editor, plan-gates, paywall]
plan_gates: ["segments", "subscribers", "subscribers-rfm"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-segments-editor]]. See the hub for the other aspects (modal layout, condition builder, operators-and-values, create popup, validation, save pipeline).

# Segment editor — plan gates

## Purpose

Three plan-feature mappings interact with the Segment editor: `segments` (numeric cap on Automated segments), `subscribers` (numeric cap on marketable subscribers — drives the red plan-limit banner), and `subscribers-rfm` (boolean — whether the RFM condition appears in the picker). This page documents each gate's effect on the editor's UI and on save behaviour. The wider plan-feature substrate is on [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]].

## Where to find it

The plan-feature interactions surface in two places:

- **Inside the editor modal** — the red plan-limit banner at the top of [[segments-editor-modal-layout]] when the store is at/over the `subscribers` cap.
- **In the precursor popup** — the **Automated (X of Y)** sub-card on [[segments-editor-create-popup]], which routes to the `PlanFeature` upsell modal at [[plan-features]] when at cap.

## What the merchant can do here

- **See the red plan-limit banner** at the top of the editor when at/over the `subscribers` cap (Automated only) — see [[segments-editor-modal-layout]].
- **Click Buy package** in the banner to open `/admin/plan/feature?mapping=subscribers` (the per-feature purchase modal at [[plan-features]]).
- **See the Automated (X of Y) counter** on the precursor popup — see [[segments-editor-create-popup]].
- **Be redirected to the upsell** when picking Automated at cap (the editor does not open; `PlanFeature` modal opens with `mapping=segments`).
- **Discover that the `subscriber.rfm` condition is not in the picker** on lower-tier plans (no inline upgrade prompt — the merchant must upgrade plan).

## Settings & fields

### The three plan-features

| Mapping | Shape | What it controls |
|---|---|---|
| `segments` | Numeric (max Automated segments) | Same store-wide Automated-segment cap as [[marketing-segments]]. The editor's "Create segment" → Automated path is blocked when at cap; the precursor popup shows *"Automated (X of Y)"* and clicking Automated opens the per-feature purchase modal at [[plan-features]] instead of the editor. One-time (`regular`) segments do NOT count toward the cap and can always be created. Verified via the meta endpoint's `getFeatures` returning `current` + `used` for the `segments` mapping. |
| `subscribers` | Numeric (max marketable subscribers) | When the store is at or over the `subscribers` cap, the editor renders a **red plan-limit banner** at the top with the localised *"You have reached your subscriber limit"* message + a **Buy package** button linking to `/admin/plan/feature?mapping=subscribers`. The banner is hidden for One-time segments (only Automated count toward the limit). After purchase, the meta query refetches and the banner clears. The cap also affects what the segment will MATCH — see the `subscribers.max_id` mechanism documented on [[marketing-segments]]. |
| `subscribers-rfm` | Boolean | Whether the `subscriber.rfm` condition is offered in the editor's condition picker. When off (default on lower-tier plans), the condition simply does not appear in the searchable dropdown — no inline upgrade prompt on the picker itself. The merchant must upgrade plan to use RFM-bucket targeting. |

When over cap, the merchant is redirected to the per-feature upsell at [[plan-features]]. Numeric gates (`segments`, `subscribers`) extend via packs ([[plan-vs-feature-pack]]); the boolean `subscribers-rfm` gate requires a plan upgrade.

**Note:** the meta-endpoint also filters condition modules by installed apps — that is an app-availability filter, **NOT** a plan gate. See [[segments-editor-validation]] for the meta endpoint behaviour.

### Plan-limit banner mechanics

The red banner shown at the top of [[segments-editor-modal-layout]]:

- Shows ONLY for Automated segments (`type !== 'regular'`). One-time segments don't count toward the segment limit; they don't trigger the banner.
- Disappears when the merchant has at least one Automated slot available (`used < current`).
- Contains the localised *"You have reached your subscriber limit"* copy with the substituted limit + total counts.
- Includes a **Buy package** button linking to `/admin/plan/feature?mapping=subscribers`.

The editor reads the merchant's `subscribers` plan-feature `used` and `current` counts from the meta endpoint (see [[segments-editor-validation]] for the 5-minute cache). After a successful purchase via the linked `/admin/plan/feature?mapping=subscribers` flow, the meta data refetches to clear the banner.

### Automated cap — precursor popup behaviour

The **Automated (X of Y)** sub-card in the precursor popup (see [[segments-editor-create-popup]]) shows the merchant's current Automated-segment count vs cap (from the `segments` plan feature's `used` / `current`). Two cases:

- **`used < current`** — clicking Automated closes the popup and opens the editor with an empty conditions tree and `type = 'automated'` in the Create payload.
- **`used >= current`** — clicking Automated does NOT open the editor. Instead it opens the **`PlanFeature` upsell modal** with `mapping=segments` (the standard per-feature purchase modal at [[plan-features]]). After successful payment the meta refetches and the editor opens with the unlocked Automated type.

The One-time card is never gated. AI-generate and Template flows always create One-time segments, so they are also never gated by `segments` (though they ARE gated by `subscribers` like all editor opens).

### `subscribers-rfm` — picker visibility

When the boolean is off, the `subscriber.rfm` condition does not appear in the searchable grouped dropdown at all — the meta endpoint omits it from the schema returned to that merchant. There is no inline upgrade prompt on the picker; the merchant simply does not see the condition.

When the boolean is on, the RFM condition appears in the **Subscriber** group of the picker and behaves like any other condition (operator + value vocabulary per [[segments-editor-operators-and-values]]).

## Business rules

- **Banner is type-aware.** Only Automated triggers the red banner; One-time saves never paywall on `subscribers`.
- **`segments` cap blocks the popup, not the editor.** A merchant at cap can still open the editor for Edit, save existing Automated segments, and create new One-time segments — only the Create-as-Automated path is gated.
- **Purchase clears the banner via meta refetch.** The meta query is invalidated after the `PlanFeature` purchase modal completes; the banner disappears automatically once the new counts arrive.
- **`subscribers-rfm` is binary** — there is no "RFM packs" extension; the merchant must move to a plan where the boolean is on.
- **Meta endpoint also filters by installed apps.** A condition whose owning app is uninstalled is omitted from the schema — this is an availability filter, not a plan gate (and not surfaced as a "buy package" prompt). The merchant installs the app to make the condition available.

## Related

- [[marketing-segments-editor]] — hub.
- [[segments-editor-modal-layout]] — where the red plan-limit banner renders.
- [[segments-editor-create-popup]] — the precursor popup where `segments` cap blocks the Automated sub-card.
- [[segments-editor-validation]] — meta endpoint that returns `used` + `current` and filters by installed apps.
- [[segments-editor-save-pipeline]] — meta refetch on save of an Automated segment.
- [[marketing-segments]] — `subscribers.max_id` mechanism that also affects what the segment MATCHES.
- [[plan-gates]] — plan-gate concept.
- [[plan-vs-feature-pack]] — numeric gates extend via packs.
- [[plan-features]] — the `PlanFeature` upsell modal opened when at cap.

## Open questions

No outstanding questions.
