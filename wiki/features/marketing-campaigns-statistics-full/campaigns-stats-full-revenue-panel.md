---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Revenue panel"
route_name: campaigns.statistics.full.revenue
route_path: /admin/campaigns/statistics/full/revenue
aliases: ["Full revenue panel", "Per-campaign revenue panel", "Orders from campaign list", "Turnover side-panel", "Поръчки от кампания"]
tags: [marketing, campaigns, statistics, revenue, orders]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-full]]. See the hub for the other aspects (dashboard, attribution metadata, attribution mechanic, revenue statuses, order processing).

# Revenue side-panels (full + per-campaign)

## Purpose

The revenue side-panels list the actual orders the platform attributes to campaign clicks — one row per order, showing which campaign / step / channel was the last-touch credit. There are two variants:

- **Full revenue** (`campaigns.statistics.full.revenue`) — orders from ANY campaign. Opened from the Turnover card on [[campaigns-stats-full-dashboard]].
- **Per-campaign revenue** (`campaigns.statistics.revenue`) — orders for ONE campaign. Opened from the Turnover card on [[marketing-campaigns-statistics|per-campaign statistics]].

## Where to find it

Both are **legacy Smarty** side-panels (panel-class="wide"), reached by clicking the **Turnover** KPI card on the respective statistics page:

| Route name | Route path | Opened from |
|------------|------------|-------------|
| `campaigns.statistics.full.revenue` | `/admin/campaigns/statistics/full/revenue` | Turnover card on the full dashboard |
| `campaigns.statistics.revenue` | `/admin/campaigns/statistics/{id}/revenue` | Turnover card on per-campaign statistics |

Both are behind the campaign anti-spam policy gate; standard campaign permission applies.

## What the merchant can do here

Read the paginated table of attributed orders (header *"Turnover"*), and click an **Order** number to open that order's detail. The panels are read-only.

### Table columns (full revenue)

| Field | Label | Content |
|-------|-------|---------|
| `number` | Order | Order number (clickable — opens order detail). |
| `campaign` | Campaign | The campaign name attribution credits (`cc_campaign_name` from `orders_meta`). |
| `subscriber` | Subscriber | The customer/subscriber who placed the order. |
| `address` | Address | Shipping address summary. |
| `channel` | Channel | The campaign channel that drove the click (`cc_campaign_channel` from `orders_meta`). |
| `campaign_action_order` | Step | Step number (1-based, computed from `cc_campaign_action_order + 1`). |
| `date_added_formatted` | Date | Order date. |
| `status` | Status | Order status badge. |
| `price_total_formatted` | Total | Order total, money-formatted. |

### Per-campaign revenue variant

Same layout, filtered to one campaign — the table **drops the Campaign column** (every row is the same campaign). All other columns and behaviour are identical. The per-campaign lookup adds a `value=campaign.id` filter on the `orders_meta` query.

## Settings & fields

No settings on these panels. The set of statuses that qualify an order for inclusion is governed by [[campaigns-stats-full-revenue-statuses]]. The metadata that populates the Campaign / Channel / Step columns is documented in [[campaigns-stats-full-attribution-metadata]].

## Business rules

### N/A fallbacks

- **Channel column** — if the `cc_campaign_channel` meta row is missing (legacy orders pre-dating channel tracking, or some edge case), the cell shows the localised **"N/A"** placeholder. The order is still counted in revenue.
- **Campaign / channel attribution missing** — if the attribution metadata is absent for an order (e.g. the campaign was deleted before the view loaded), the cell falls back to **"N/A"**.

### Step number display is +1

`cc_campaign_action_order` is stored **0-based** in `orders_meta`. The panel displays it **+1** (1-based) so the merchant sees Step 1, Step 2, etc. — matching the campaign editor's 1-based step numbering.

### Soft-deleted campaigns still appear

If a campaign is soft-deleted but pre-delete orders attributed to it remain in the DB, those orders still appear on the full revenue list with the campaign name from the `cc_campaign_name` snapshot (captured at click time). The campaign link no longer resolves to a live campaign page, but the attribution data is preserved — see [[campaigns-stats-full-attribution-metadata]].

### Empty state vs zero data

Both panels distinguish two situations:

- **Never had any campaign orders** — renders the empty illustration *"No records yet (Turnover)"*.
- **Has orders, but the grid is loading them** — the grid wrapper is briefly hidden, then populated.

A **records-exist pre-check** runs before the grid query: it counts orders with the relevant `cc_campaign_id` meta (any campaign for the full panel; the specific campaign for the per-campaign panel). If zero, the controller skips the grid query and renders the panel with `records_exist=0` — the empty illustration shows and **no AJAX `__grid` call is issued**, saving a roundtrip on never-converted campaigns. Otherwise the grid loads; the dispatcher re-checks `data.custom_data.records < 1` after the AJAX load and toggles the empty state accordingly.

## Related

- [[marketing-campaigns-statistics-full]] — hub.
- [[campaigns-stats-full-dashboard]] — the dashboard whose Turnover card opens the full panel.
- [[marketing-campaigns-statistics]] — per-campaign statistics; opens the per-campaign panel.
- [[order]] — Order entity; each row is an order.
- [[orders-details]] — order detail opened by clicking the Order number.
- [[settings-statuses]] — order-status configuration.

## Open questions

No outstanding questions.
