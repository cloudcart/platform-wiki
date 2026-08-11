---
type: feature
nav_path: "Marketing → Campaigns → Subscribers → Surfaces"
route_name: subscribers.list
route_path: /admin/marketing-new/subscribers?filter[campaign]={campaign_id}
aliases: ["Campaign subscribers surfaces", "Campaign subscribers panel vs redirect", "Subscribers list filtered by campaign"]
tags: [marketing, campaigns, subscribers, recipients]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Campaign subscribers — surfaces

> Part of [[marketing-campaigns-subscribers]]. See the hub for the other aspects (columns, progress model, enrolment model).

## Purpose

This page documents **where the Campaign-subscribers list lives** and the **two parallel surfaces** the merchant can land on when they click into a campaign's subscriber population. Both surfaces show the same population (all subscribers enrolled in this campaign) but differ in column layout, available actions, and how the page is loaded.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click any campaign row's **Subscribers (N)** button (the `subscribers_count` chip in the row). The button is disabled if the campaign has zero enrolled subscribers (`subscribers_count === 0`).

There are **two parallel surfaces** depending on whether the merchant is on the legacy Smarty page or the modern Vue list:

| Surface | Route | Behaviour |
|---------|-------|-----------|
| **Legacy side-panel** (Smarty) | `campaigns.subscribers` → `/admin/campaigns/subscribers/{campaign_id}` (GET / POST) | Opens as a side-panel. Header shows the campaign's title. Body is a paginated table of enrolled subscribers (campaign-specific columns — see [[campaigns-subscribers-columns]]). |
| **Modern Vue redirect** (`CampaignsTableSubscribersLink`) | Click **(N) Subscribers** button on a campaign row → redirects to `subscribers.list` with `?filter[campaign]=<campaign_id>` | Routes to the main [[marketing-subscribers\|Subscribers list]] pre-filtered by this campaign. Merchant sees the **full subscribers list** with all its filters, bulk actions, and detail modal — but scoped to subscribers enrolled in this campaign. No separate side-panel; the merchant stays on the main subscribers UI. |

## What the merchant can do here

- Land on either the legacy side-panel or the modern pre-filtered subscribers list, depending on the surface.
- On the **legacy side-panel**: see campaign-specific columns (progress badge, currently-step, times-completed) — see [[campaigns-subscribers-columns]].
- On the **modern redirect**: see the standard subscribers-list columns (name, channels, country, subscribed, last-active, orders, turnover, accepts-marketing toggle) plus all the full-list filters and bulk actions — but **lose** the campaign-specific enrolment columns.
- On the modern redirect, recover the per-subscriber funnel state (progress, step) by clicking into the subscriber detail modal and inspecting the **Campaigns** sub-section.

## Settings & fields

The two surfaces show **the same population** but differ in column set:

- The **legacy side-panel** shows campaign-specific columns: progress badge, currently-step, times-completed. Full column rendering on [[campaigns-subscribers-columns]].
- The **modern redirect** shows the standard subscribers list columns (name, channels, country, subscribed, last-active, orders, turnover, accepts-marketing toggle) but loses the campaign-specific enrolment columns.

## Business rules

### The page opens twice on first load — panel chrome + grid

The `load` query param controls what comes back: `?load=1` returns the panel chrome (header + table head); the panel then makes a second request to the same URL (without `load`) to fetch the grid body. So opening the legacy panel triggers **two requests** to this endpoint — first GET, then POST.

### Same population, two layouts

Both surfaces resolve to the identical enrolled-subscriber population (the campaign-subscribers enrolment records — see [[campaigns-subscribers-enrolment]]). Choosing a surface only changes which columns and actions are available, never which subscribers are shown.

### Disabled button at zero enrolment

The **Subscribers (N)** button is disabled when `subscribers_count === 0`, so a merchant can't open an empty list for a Draft or never-launched campaign. The count itself is computed as part of the same lookup that loads each campaign, so the parent list doesn't fire a separate count query per campaign.

## Related

- [[marketing-campaigns-subscribers]] — hub.
- [[marketing-campaigns]] — parent hub; clicking the subscribers chip on a campaign row opens this surface.
- [[marketing-subscribers]] — the full Subscribers CRM list the modern redirect lands on.
- [[campaign]] — Campaign entity.
- [[subscriber]] — Subscriber entity.

## Open questions

No outstanding questions.
