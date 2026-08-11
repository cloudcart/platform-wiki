---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Conversion attribution"
route_name: campaigns-statistics
route_path: /admin/marketing-new/campaigns/statistics/:id
aliases: ["Conversion attribution", "Campaign revenue attribution", "Last-touch attribution", "cc_campaign_id", "cc_campaign_action_id", "revenue_statuses"]
tags: [marketing, campaigns, statistics, attribution, revenue]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics]]. See the hub for the other aspects (KPI cards, channel breakdown, step table, aggregation, logs modal).

# Campaign statistics — conversion attribution

## Purpose

The conversion-rate KPI and the Turnover numbers on the Campaign statistics page only make sense once the merchant understands **how an order gets credited to a campaign**. This page documents the attribution model: the `orders_meta` keys that link orders to campaigns and steps, the session-based last-touch window, and the revenue-status filter that decides which attributed orders actually count toward revenue.

## Where to find it

Attribution is not a screen — it is the logic behind the Conversion-rate KPI ([[campaigns-stats-kpi-cards]]), the campaign Turnover card, the per-step Orders / Turnover columns ([[campaigns-stats-step-table]]), and the attributed-orders list ([[marketing-campaigns-statistics-full]]). This page is the reference the merchant consults when a campaign's revenue number looks too high, too low, or unexpected.

## What the merchant can do here

This is a reference page — no merchant actions specific to "attribution" itself. What the merchant DOES with this knowledge:

- **Interpret the conversion / revenue numbers correctly** — knowing it is last-touch, session-scoped attribution.
- **Understand why a cancelled order drops out of revenue** but a refunded subscriber stays attributed.
- **Configure which order statuses count** as revenue via the `revenue_statuses` setting in the Segments app.

## Settings & fields

- **`cc_campaign_id`** — the per-campaign attribution key. An order is attributed to a campaign when it has an `orders_meta` row with `parameter='cc_campaign_id'` and `value=<campaign_id>`. This drives the campaign's `orders_count` (conversion rate) and the headline Turnover card.
- **`cc_campaign_action_id`** — the per-step attribution key. Written alongside `cc_campaign_id`, it lets the per-step table identify WHICH step's link led to the order. Per-step Orders / Turnover use an `orders_meta` join on this key — see [[campaigns-stats-step-table]].
- **`revenue_statuses`** — the order statuses that count toward revenue. Configured in [[marketing-segments]] (the Segments app). Default: `paid`, `completed`, `fulfilled`, `pending`. Orders in `cancelled` / `refunded` / other non-revenue statuses are excluded from the revenue math.

## Business rules

- **Last-touch, session-scoped.** Attribution metadata is written when the customer clicks a tracked link, lands on the storefront with the campaign-tracking cookie, and places an order within the attribution window — the customer's session. Once the cookie expires (or the customer clears cookies), subsequent orders are not attributed. The campaign whose link was clicked **most recently** before the order gets the credit — this is closer to last-touch than first-touch attribution.
- **Both keys are written together.** `cc_campaign_id` and `cc_campaign_action_id` are recorded in the same write, so an order rolls up to both its step's per-step row AND the campaign's headline Turnover card simultaneously.
- **Cancellation disqualifies the order without removing the metadata.** Only orders in a configured revenue status count toward the conversion / revenue figures. A cancellation simply drops the order from the revenue math — the `orders_meta` attribution row stays in place, so if the order later returns to a revenue status it counts again.
- **The metadata survives a campaign delete.** Because attribution lives on `orders_meta` (on the order, not the campaign), it persists even after the campaign is soft-deleted. This is why the revenue list ([[marketing-campaigns-statistics-full]]) still works for a deleted campaign even though the stats route itself returns 404 — see [[campaigns-stats-aggregation]].

## How it works

The campaign-level `orders_count` is computed by joining the campaign's subscribers' orders against `orders_meta` rows where `parameter='cc_campaign_id'` AND `value=<campaign_id>`, filtered to the configured `revenue_statuses`. The per-step revenue uses a separate `orders_meta` join with `parameter='cc_campaign_action_id'` AND `value IN (<step ids>)`. The click-time snapshot that writes these metadata rows is documented in detail on [[marketing-campaigns-statistics-full]], which also explains why there is no double-counting between the per-campaign Turnover card and the per-order revenue list.

## Related

- [[marketing-campaigns-statistics]] — hub.
- [[campaigns-stats-kpi-cards]] — the Conversion-rate KPI + Turnover card driven by attribution.
- [[campaigns-stats-step-table]] — per-step Orders / Turnover keyed on `cc_campaign_action_id`.
- [[marketing-campaigns-statistics-full]] — the attributed-orders list + click-time attribution snapshot.
- [[marketing-segments]] — the `revenue_statuses` setting (Segments app).
- [[campaigns-stats-aggregation]] — why deleted campaigns still have a revenue list.

## Open questions

No outstanding questions.
