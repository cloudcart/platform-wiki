---
type: entity
nav_path: "Entity → Segment → Attributes schema"
aliases: ["Segment attributes", "Segment name vs title", "Segment processing flag", "Segment inactive_errors", "Segment channel", "Segment soft-delete", "Segment membership link", "Полета на сегмент"]
tags: [entity, marketing, segments, attributes]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[segment]]. See the hub for the other aspects (types, lifecycle, membership, relationships, API access).

# Segment — Attributes schema

## Identity

This page is the field-level reference for a [[segment|Segment]] — every attribute the merchant configures plus the underlying fields that drive the segment list, the rebuild placeholder, and the auto-disable behaviour. It also documents the segment-membership link, which is where the actual membership and the manual / resend flags live.

## Aliases

- **Name** vs **Title** — two distinct fields; the displayed label is `title` if set, else the auto-summary `name`.
- **Processing flag** — the `processing` flag that drives the "currently being filtered" placeholder.
- **Membership link** — the many-to-many association between [[subscriber|Subscriber]] and Segment that holds each membership row.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| `name` | Merchant-given label | Auto-generated from `conditions_formatted` if the merchant doesn't override (e.g., "Subscribed in last 30 days AND ordered from Shoes"). Editable. Shown in the segment list and in the Campaign target picker. |
| `type` | `regular` / `automated` | **One-time** (`regular`) — the merchant clicks Generate to evaluate; membership stays frozen until the next manual regenerate. **Automated** — the platform continuously re-evaluates on every qualifying subscriber-side event. See [[segment-entity-types-onetime-automated]]. |
| `conditions` | The rule tree | A nested set of filter conditions composed with AND (OR disabled in the current UI). Each condition is a `<field> <operator> <value>` triple (e.g., "Country equals Bulgaria", "Total spent greater than 100", "Last order date in last 30 days"). |
| `conditions_formatted` | Auto-summary text | Human-readable rendering of the rule tree shown in the segment list, e.g., "Country = Bulgaria AND Total spent > 100 BGN". Re-computed whenever conditions change. |
| `subscribers_count` | Cached subscriber count | The size of the current membership. Updated by the rebuild pipeline; the merchant clicks this number to open the [[marketing-segments-subscribers|Subscribers in this segment]] view. |
| `last_generated_at` | When the rule was last evaluated | For One-time segments — the timestamp of the last Generate click. For Automated segments — the timestamp of the last full rebuild. |
| `active` | yes / no | On/Off switch. Inactive segments stop being recalculated and cannot be picked as a campaign target. Existing campaigns referencing an Inactive segment still see the frozen membership — see [[segment-entity-lifecycle]]. |
| `campaigns_count` | Cached campaign-attached count | How many campaigns use this segment as a target. When > 0, the merchant cannot delete the segment until those campaigns are detached or deleted — see [[segment-entity-relationships]]. |
| `title` | Optional merchant-given rename | Separate field from `name`. Set ONLY through the Rename action on the segment list (PUT `/segments/:id/rename`). The display name on the list = `title` if set, else `name` (the auto-summary). Editing conditions overwrites `name` but does NOT touch `title`. |
| `processing` | flag (0/1) | Set to `1` during save and rebuild; the list shows the *"Your subscribers are currently being filtered, please check again later"* placeholder while `processing = 1`. Cleared to `0` when the rebuild finishes. |
| `last_execute` | timestamp | When the rebuild last completed (success or failure). Drives the "Last generated at" value shown on the list. The field is named `last_execute` internally even though the UI label reads "Last generated at". |
| `inactive_errors` | list of error strings (nullable) | Populated when the segment self-disables due to a broken condition (e.g. an uninstalled app's contributed condition). Each entry is a human-readable error string. The platform exposes a formatted version, `inactive_errors_formatted`, which joins them onto separate lines and wraps them with the localised disabled-segment message. |
| `channel` | text | Always `'cloudcart'` on segments created through the platform; the platform forces this at creation. Other channels existed historically; the modern segment is always channel=`cloudcart`. |
| `deleted_at` | timestamp (nullable) | Soft delete. Deleting from the list sets `deleted_at`; the record stays in storage. Only on a force-delete (not exposed in the UI) is the record purged and its membership-change history emptied. |

### The segment-membership link

The membership is a many-to-many association between [[subscriber|Subscriber]] and Segment, keyed by subscriber and segment. Each membership row carries:

- **`manual`** (0/1) — `1` if hand-added by the merchant, `0` if rule-matched. Drives the immune-from-rebuild behaviour on [[segment-entity-membership]].
- **`resend`** (0/1) — `1` if the subscriber should be re-sent the current campaign (set by campaign retry / resend flows); the rebuild reads this when deciding whether to skip already-attached subscribers.
- **`created_at` / `updated_at`** — membership-row timestamps; `updated_at` is what the segment uses to find the most recently-touched membership.

### Auto-generated names

When the merchant doesn't supply a name, the platform synthesises one from `conditions_formatted` — e.g., a Segment with rule "Country = Bulgaria AND Total spent > 100" becomes named "Country = Bulgaria AND Total spent > 100". The merchant can override at any time via Rename (which writes `title`, leaving `name` as the auto-summary).

### Cached counts are not live-computed

`subscribers_count` and `campaigns_count` are cached on the Segment, not computed on every page load. They update during rebuilds and when campaigns are attached or detached. The merchant clicks the count to expand the actual rows — see [[segment-entity-relationships]].

## Where it appears

- [[marketing-segments]] — the master list; renders `name`/`title`, `subscribers_count`, `campaigns_count`, the `active` toggle, and the `processing` placeholder.
- [[marketing-segments-editor]] — authors `conditions` and recomputes `conditions_formatted`.
- [[marketing-segments-subscribers]] — reads the segment-membership rows (`manual` / `resend`).
- [[api-segments]] — exposes a subset of these fields read-only (rule tree + `processing` + `inactive_errors` + `deleted_at` are hidden) — see [[segment-entity-api-access]].

## Related

- [[segment]] — hub.
- [[subscriber]] — the other side of the membership link; membership rows.
- [[campaign]] — drives `campaigns_count`; sets `resend` on the membership row.
- [[marketing-segments]] — the list that renders these fields.

## Open Questions

No outstanding questions.
