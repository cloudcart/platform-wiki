---
type: feature
nav_path: "Marketing → Campaigns → Subscribers → Enrolment"
route_name: campaigns.subscribers
route_path: /admin/campaigns/subscribers/{campaign_id}
aliases: ["Campaign subscriber enrolment", "Campaign enrolment data source", "Regular vs Automated enrolment", "Repeating campaign enrolment", "Times completed counter"]
tags: [marketing, campaigns, subscribers, recipients]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Campaign subscribers — enrolment model

> Part of [[marketing-campaigns-subscribers]]. See the hub for the other aspects (surfaces, columns, progress model).

## Purpose

This page documents **how subscribers get onto the Campaign-subscribers list** — the enrolment data source (the campaign-subscribers enrolment records), how Regular vs Automated campaigns populate it differently, why a single subscriber can appear multiple times on a repeating campaign, and the gating rules (Draft = empty, anti-spam, permissions). A support agent answering "why is the same person listed three times?" or "why is my new campaign's subscriber list empty?" should land here.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → a campaign's **Subscribers (N)** button → the list of enrolled subscribers (see [[campaigns-subscribers-surfaces]] for the two surfaces).

## What the merchant can do here

- See exactly which subscribers are enrolled in this campaign and when (enrolment timestamp).
- Understand why the list grows over time for Automated campaigns vs being a single batch for Regular campaigns.
- Understand why a Draft campaign's list is empty.
- See repeat-completion counts for subscribers who re-enter a repeating campaign.

## Settings & fields

### Enrolment data source

The subscribers list reads from the campaign-subscribers enrolment records linked to each subscriber. Each enrolment record stores:

- `subscriber_id`
- `campaign_id`
- `progress` (the enum — see [[campaigns-subscribers-progress]])
- `times_completed`
- `created_at` (enrolment timestamp, shown as the **Added at** column)

Only subscribers actually enrolled in this campaign appear. Subscribers in the trigger segment but not yet enrolled (e.g., scheduled future enrolment) don't show until the platform enrols them.

### Times completed counter — applies to both Regular and Automated

The `times_completed` value on the enrolment record is incremented whenever a subscriber completes the campaign — regardless of campaign type. For a typical Regular campaign each subscriber completes once (`times_completed = 1`). For Automated campaigns with `repeat = true`, subscribers re-entering the trigger flow start a fresh enrolment row, and the counter on each enrolment increments to 1 on completion. The counter is not strictly an Automated-only concept. (Its icon-only rendering is documented on [[campaigns-subscribers-columns]].)

## Business rules

### Subscribers list works for both Regular and Automated

The route doesn't gate on campaign type — both Regular and Automated campaigns expose this list. For Regular campaigns the list is typically a single batch enrolled at start time; for Automated campaigns enrolments accrete over time as the trigger fires.

### Repeating campaigns can show the same subscriber multiple times

For automated campaigns with `repeat=true`, a subscriber who re-enters the trigger gets a **fresh enrolment record**. So the same subscriber can appear N times on this list, each row showing a different enrolment date and progress. This is by design, not a duplication bug.

### Pre-launch state

A campaign in Draft (`active=2`) has no enrolled subscribers — the list is empty, because enrolment only fires on activation. The merchant must launch the campaign to populate this list. (The **Subscribers (N)** button is also disabled at zero enrolment — see [[campaigns-subscribers-surfaces]].)

### Soft-deleted subscribers are excluded

The list uses the active subscriber pool — soft-deleted subscribers don't appear (deleted subscribers are filtered out).

### Pagination resilience — snap-back happens after the first query

When the merchant requests a page beyond the available data (e.g., they were on page 5, deleted a bunch of subscribers, and now there's only page 1), the platform silently snaps back to page 1 so the merchant never sees an empty page in error. The mechanism is a re-fetch: the first fetch returns nothing for the requested page, so when there are subscribers but the requested page is beyond page 1 and came back empty, the platform resets to page 1 and re-fetches against page 1. The cost of "snap back" is one extra round-trip — but the merchant always gets a populated page back.

### Subscribers count is computed alongside the campaign, not as a separate query

The `subscribers_count` shown in the panel header is counted as part of the same lookup that loads the campaign. So opening the panel doesn't trigger an extra count query.

### Anti-spam policy gate

Like every campaign endpoint, this route is gated by the campaign anti-spam policy gate — a merchant without policy acceptance can't open it.

### Permissions

Standard campaign permission applies.

## Related

- [[marketing-campaigns-subscribers]] — hub.
- [[campaigns-subscribers-surfaces]] — how the two surfaces present this enrolled population.
- [[campaigns-subscribers-progress]] — the per-enrolment progress state stored on each enrolment record.
- [[campaigns-subscribers-columns]] — the Added-at and Times-completed columns sourced from the enrolment records.
- [[marketing-campaigns-edit]] — campaign editor; the trigger / repeat settings that drive enrolment.
- [[marketing-segments]] — the trigger segment that enrols subscribers.
- [[marketing-subscribers]] — full subscriber CRM.
- [[campaign]] — Campaign entity.
- [[subscriber]] — Subscriber entity.

## Open questions

No outstanding questions.
