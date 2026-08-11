---
type: feature
nav_path: "Marketing → Campaigns → Banned info → Surfaces"
route_name: campaigns.banned-info
route_path: /admin/campaigns/banned-info/{campaign_id}
aliases: ["Banned info surfaces", "Banned campaign side-panel", "Banned reason tooltip", "Campaign error icon", "Red exclamation triangle campaign"]
tags: [marketing, campaigns, banned, ui, tooltip]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Campaign banned info — surfaces

> Part of [[marketing-campaigns-banned-info]]. See the hub for the other aspects (aggregation, channel reasons, segment reasons, activation).

## Purpose

This page documents the **two parallel surfaces** the banned reasons appear on — the legacy Smarty side-panel and the modern Vue tooltip — and the visual treatment of each (the red error icon, the alert-box styling, and the HTML-link rendering). Both surfaces consume the same backend `banned_reason` source; the difference is purely presentation.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → on the campaigns list, a broken campaign's title cell shows a red banned-reason indicator. Which surface the merchant sees depends on whether the store is on the legacy Smarty campaign list or the modern Vue list.

## What the merchant can do here

| Surface | Trigger | Behaviour |
|---------|---------|-----------|
| **Legacy side-panel** (Smarty `campaigns.banned-info` route) | Click the banned chip in the legacy campaign-list row | Opens as a side-panel at `/admin/campaigns/banned-info/{campaign_id}` (GET). Lists ALL banned reasons as red alert boxes. |
| **Modern Vue tooltip** (`CampaignsTableName`) | Hover the red exclamation-triangle icon (`fa-light fa-exclamation-triangle`, color `#FC4F4E`) in front of a broken campaign's title | A `CcTooltip` displays the comma-joined banned-reason messages inline. No separate side-panel. |

In both cases the merchant can only **read** the reasons, then close the surface and navigate to the relevant channel or segment to act.

## Settings & fields

### Modern Vue tooltip — fields aggregated

In the modern Vue table, `hasError` is computed from the row's `banned` flag. When true, the campaign's title-icon slot renders the red triangle icon instead of the normal calendar / status-blob. The tooltip text aggregates messages from these row fields (deduplicated):

- `data.banned`
- `data.banned_reason`
- `data.inactive_errors`
- `data.error` / `data.errors`
- `data.status?.banned_reason`
- `data.segment?.inactive_errors`

Each field is parsed via `parseErrorValue` — strings stay as-is, JSON-encoded arrays expand, plain arrays flatten, objects walk recursively. The deduped list is joined with `, ` and shown as the tooltip text.

### Legacy side-panel — alert boxes

The side-panel renders the campaign title in the panel header (h3) and iterates the deduplicated reason list as red `.alert-danger` styled boxes — one box per reason.

## Business rules

### The chip is computed at row-serialization time

The chip is built into the campaign list row formatter — when the campaign row's serialization runs, it computes a `banned_reason` for each referenced channel and stamps it onto the row data. Opening the side-panel just shows the long-form version of what the chip is summarising. How that walk assembles the list is on [[campaigns-banned-aggregation]].

### Alert text supports HTML

The alerts are rendered with `nofilter` Smarty — a channel's `banned_reason` can include hyperlinks (e.g. to the channel's setup page, to the plan-upgrade flow, to the credit-purchase modal). So a "channel not configured" alert often looks like *"Channel **Email** is not configured. [Configure now]"* with the link going to [[marketing-channels-email]]. The plan-cap reason similarly embeds a buy-more-credits link — see [[campaigns-banned-channel-reasons]].

### Locale wrap on the list-row chip

The list-row banned chip and per-row formatter use a locale-wrapped variant of the reason text (`withLocale(site('language_cp'), ...)`) to ensure consistent localisation regardless of the request's locale context. The same data with HTML links is exposed to the side-panel; the "clear" chip variant uses a plain purchase-text string instead of the HTML link.

### Side-panel display only

The legacy view is only accessible via the side-panel — there's no full-page version. The URL `/admin/marketing-new/campaigns/banned-info/{id}` returns a panel template, not a full page. The panel has the standard close ("X") button at the top — clicking it returns the merchant to the campaigns list.

## How it works

Both surfaces ask the backend for the same combined, deduplicated reason list (see [[campaigns-banned-aggregation]]). The legacy surface renders it as multiple alert boxes; the modern surface flattens it into a single comma-joined tooltip string. Because the alert text is HTML-capable on the side-panel, embedded fix links render as clickable anchors; the tooltip shows them as plain joined text.

## Related

- [[marketing-campaigns-banned-info]] — hub.
- [[marketing-campaigns]] — campaigns list; both surfaces live on its rows.
- [[marketing-channels-email]] — a common target of the embedded "Configure now" fix link.
- [[campaign]] — Campaign entity (the row being serialized).

## Open questions

No outstanding questions.
