---
type: feature
nav_path: "Marketing → Campaigns → Subscribers"
route_name: subscribers.list
route_path: /admin/marketing-new/subscribers?filter[campaign]={campaign_id}
aliases: ["Campaign subscribers", "Campaign recipients", "Subscribers in this campaign", "Funnel members", "Получатели на кампания", "Абонати в кампания"]
tags: [marketing, campaigns, subscribers, recipients]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---
# Campaign subscribers

## Purpose

The **Campaign subscribers** page is the merchant's "who's in this funnel right now" view for a specific campaign. It lists every subscriber who has been enrolled in the campaign (regardless of where they are in its steps), shows their **progress** in the funnel (waiting / executing / completed / removed), how many times they've completed it (for repeating automated campaigns), what step they were last seen on, and their channel-subscribership status (Email/Phone/WebPush — and whether they accept marketing on each).

This is the merchant's go-to when they want to answer "did this customer get enrolled?", "are they at step 3 now?", "have they finished the welcome series yet?", "why didn't they get my email?" (channel-status diagnostics live here too). Unlike [[marketing-campaigns-statistics]] (which aggregates), this is a **per-subscriber list** — one row per enrolled subscriber, drilling into their personal journey through the campaign.

This cluster was split from a single page into a slim hub + four aspect pages because it covered four distinct concepts (the two surfaces, the column rendering, the progress model, and the enrolment data model). The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[campaigns-subscribers-surfaces]] — where to find it; the two parallel surfaces (legacy Smarty side-panel vs modern Vue redirect to the pre-filtered subscribers list); the two-request panel load.
- [[campaigns-subscribers-columns]] — the six columns and exactly how each renders (binary Progress badge, step-NUMBER-only Step badge, icon-only Times-completed counter, channel pills, locked sort, always-paginated).
- [[campaigns-subscribers-progress]] — the `subscriber_to_campaigns.progress` enum (`waiting`/`executing`/`completed`/`removed`/`paused`); why "enrolled" ≠ "received the message"; removed subscribers stay visible for audit.
- [[campaigns-subscribers-enrolment]] — the enrolment data model (the campaign-subscribers pivot); Regular vs Automated enrolment; repeating campaigns producing multiple rows per subscriber; Draft = empty; anti-spam / permission gates.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click any campaign row's **Subscribers (N)** button (the `subscribers_count` chip in the row). The button is disabled when the campaign has zero enrolled subscribers (`subscribers_count === 0`). There are two parallel surfaces (legacy side-panel and modern Vue redirect) — see [[campaigns-subscribers-surfaces]] for the full routing breakdown.

## What the merchant can do here

- See the **total enrolled count** for this campaign (mirrored from the `subscribers_count` chip in the parent list).
- See **per-subscriber progress** through the campaign — what step they're on, whether they've completed, whether they've been removed. See [[campaigns-subscribers-progress]].
- **Click a subscriber** to open their full [[marketing-subscribers|Subscriber profile]] (CRM record, channel history, order history).
- See **how many times** each subscriber has completed the campaign (for repeating automated campaigns) and the **date they were enrolled**.
- See the **channel status pills** per subscriber — Email, Phone, WebPush — with per-channel marketing/verified/bounced/unsubscribed flags. See [[campaigns-subscribers-columns]].
- **Paginate** the table. The list is **not** sortable from the UI — see [[campaigns-subscribers-columns]].

## Settings & fields

The page shows one row per enrolled subscriber across six columns (`name`, `channels_formatted`, `created_at_formatted`, `progress`, `times_completed`, `currently_step`) — every column's label and rendering is documented on [[campaigns-subscribers-columns]]. The per-subscriber funnel state is driven by the `subscriber_to_campaigns.progress` enum, documented on [[campaigns-subscribers-progress]]. If the campaign has zero enrolled subscribers, the page shows the empty state *"No records yet (Subscribers)"* with an illustration.

## Business rules

- **Enrolment ≠ "received the message".** A subscriber on this list may be waiting, may have been removed before any send, or may have received only some steps. To see who actually received a specific message, use [[marketing-campaigns-statistics-log]]. Full semantics on [[campaigns-subscribers-progress]].
- **Removed subscribers don't disappear** — the `remove_from_campaign` action flips progress to `removed` but keeps the pivot row, for auditability. See [[campaigns-subscribers-progress]].
- **Repeating campaigns can show the same subscriber multiple times** — each re-entry creates a fresh enrolment row. See [[campaigns-subscribers-enrolment]].
- **Draft campaigns have no enrolled subscribers** — enrolment fires only on activation. See [[campaigns-subscribers-enrolment]].
- **The list is always paginated and never sortable** from the UI. See [[campaigns-subscribers-columns]].
- **Anti-spam policy gate + standard campaign permission** apply to this route — see [[campaigns-subscribers-enrolment]].

## Related

- [[marketing-campaigns]] — parent hub; clicking the subscribers chip on a campaign row opens this page.
- [[marketing-campaigns-edit]] — campaign editor; the per-step setup is what enrols subscribers here.
- [[marketing-campaigns-statistics]] — campaign analytics; aggregates rather than per-subscriber.
- [[marketing-campaigns-statistics-log]] — per-send log (drilldown per (subscriber, step) delivery).
- [[marketing-subscribers]] — full subscriber CRM; clicking a name opens the profile.
- [[marketing-segments]] — segments; the trigger segment is what enrols subscribers into this list.
- [[campaign]] — Campaign entity.
- [[subscriber]] — Subscriber entity.

## Open questions

No outstanding questions.
