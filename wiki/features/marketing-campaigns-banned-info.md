---
type: feature
nav_path: "Marketing → Campaigns → Banned info"
route_name: admin.api.campaigns.banned-info
route_path: /admin/api/core/marketing/campaigns/banned-info/{campaign}
aliases: ["Banned campaign info", "Campaign error reason", "Why is my campaign blocked", "Suspended campaign reason", "Защо е спряна кампанията", "Причина за блокирана кампания"]
tags: [marketing, campaigns, banned, anti-spam, suspension]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---
# Campaign banned info

## Purpose

The **Campaign banned info** surface is the merchant's **diagnostic** screen for a broken campaign — usually because the campaign references a channel that has been suspended (spam complaints, bounce rate, low open rate, or a manual CloudCart staff suspension), or because the campaign's trigger segment has been deactivated or deleted. It collects every reason the campaign is currently broken and presents them as plain-language alerts so the merchant knows what to fix. It is **read-only** — an explainer, not a configuration screen.

This page is a hub. It is split into five aspect pages — see **Sub-pages** below. The Assistant should drill into the one aspect that matches the question rather than reading every page.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → on the campaigns list, a broken campaign's title cell shows a red banned-reason indicator. There are **two parallel surfaces** depending on whether the merchant is on the legacy Smarty page or the modern Vue list — the full surface-by-surface breakdown (legacy side-panel vs the modern `CampaignsTableName` tooltip, the row fields aggregated, the alert-box styling, HTML rendering) is on [[campaigns-banned-surfaces]].

| Route name | Route path | Method |
|------------|------------|--------|
| `campaigns.banned-info` (legacy side-panel) | `/admin/campaigns/banned-info/{campaign_id}` | GET |
| `admin.api.campaigns.banned-info` (modern API) | `/admin/api/core/marketing/campaigns/banned-info/{campaign}` | GET |

Both surfaces consume the same backend `banned_reason` source — the difference is presentation only.

## What the merchant can do here

- See the **campaign's title** at the top of the panel.
- See **one or more red alert boxes** below the title — each box is a reason the campaign is currently broken.
- Close the panel and act on the reason (configure the missing channel, re-activate a suspended channel, restore a deleted segment).

That's it — the panel is read-only. There is no "Fix now" button; the merchant navigates to the appropriate channel / segment page themselves. The alert catalogue and how the reasons are assembled are documented on the aspect pages.

## Settings & fields

The banned-info surface is a viewer — **there are no merchant-editable fields here.** What it displays is computed on every open from the current state of each referenced channel and the trigger segment:

- The **per-channel `banned_reason`** (not installed, not configured, not active, suspended, plan-cap reached) — see [[campaigns-banned-channel-reasons]] for the full reason catalogue and the suspension thresholds.
- The **segment-side inactive errors** and the **"Missing channel type"** reason — see [[campaigns-banned-segment-reasons]].
- The **assembly + deduplication** of the combined list — see [[campaigns-banned-aggregation]].

## Business rules

The detailed rules live on the aspect pages. The headline rules:

- **This panel is the source of truth for "why won't my campaign send"** — its reasons map 1:1 to the activation pre-flight checks. See [[campaigns-banned-activation]].
- **Reasons are recomputed on every open** — not cached at the campaign level; reopen the panel after a fix to see the updated list. See [[campaigns-banned-aggregation]].
- **The list is deduplicated** — three Email steps surface the channel reason once, not three times. See [[campaigns-banned-aggregation]].
- **Suspensions only kick in after 500 sends** — reputation-based bans are gated by a minimum-send floor. See [[campaigns-banned-channel-reasons]].
- **Manual CloudCart deny overrides everything** — when staff set a manual deny, no other reason is computed. See [[campaigns-banned-channel-reasons]].

## Sub-pages (in this cluster)

- [[campaigns-banned-surfaces]] — the two surfaces (legacy Smarty side-panel vs modern `CampaignsTableName` Vue tooltip), the row fields aggregated, alert-box styling, and HTML-link rendering.
- [[campaigns-banned-aggregation]] — how the banned list is assembled (walk actions → channels → segment), deduplication, recompute-on-every-open, and the empty-list case.
- [[campaigns-banned-channel-reasons]] — the per-channel `banned_reason` catalogue + Email suspension thresholds, the 500-send floor, reputation short-circuit, manual unsuspend / deny, and plan-cap priority.
- [[campaigns-banned-segment-reasons]] — segment-inactive errors (localized text), soft-deleted segments, and the "Missing channel type" reason.
- [[campaigns-banned-activation]] — why this panel mirrors the status-toggle activation pre-flight checks and the fix workflow.

## Related

- [[marketing-campaigns]] — parent hub; the banned chip on the campaigns list opens this panel.
- [[marketing-campaigns-edit]] — campaign editor; channel-suspension also surfaces inline here.
- [[marketing-campaigns-draft]] — Inactive tab where channel-suspended campaigns land.
- [[marketing-channels]] — channel setup; the merchant fixes channel issues here.
- [[marketing-channels-email]] — Email reputation thresholds and suspension reasons.
- [[marketing-segments]] — segments; an inactive segment surfaces here.
- [[marketing-campaigns-policy]] — anti-spam policy (separate from channel suspension but also blocks campaigns).
- [[campaign]] — Campaign entity.
- [[channel]] — Channel entity (the source of `banned_reason`).
- [[segment]] — Segment entity.

## Open questions

No outstanding questions.
