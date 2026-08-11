---
type: feature
nav_path: "Dashboard → Smart daily actions"
route_name: admin.api.dashboard.smart-actions
route_path: /admin (Dashboard widget)
aliases: ["Smart daily actions", "Smart actions", "Dashboard recommendations", "Daily action recommendations", "smart_daily_actions", "do this next", "what to do today"]
tags: [dashboard, recommendations, marketing, plan-gated]
plan_gates: ["smart_daily_actions"]
created: 2026-06-18
updated: 2026-06-23
source_count: 2
---
# Smart daily actions (dashboard recommendations)

## Purpose

A Dashboard widget that surfaces **data-driven "do this next" recommendations** computed from the store's own recent activity — restock a sold-out bestseller, pause an underperforming campaign, recover abandoned carts, win back lapsed customers, and so on. Each card states *what* to do, *why* (the exact metric that triggered it), and the *expected effect*, with a one-click **Execute** (jumps to the right admin screen, context pre-filled) or **Dismiss**.

## Where to find it

The **Smart daily actions** widget on the admin **Dashboard** (Vue `SmartActions` component). It is backed by `GET admin.api.dashboard.smart-actions`; acting on a card posts to `admin.api.dashboard.smart-actions.act`; the history list is `admin.api.dashboard.smart-actions.history`.

## What the merchant can do here

- **See today's recommendations** — the top suggestions for the store right now.
- **Execute** a recommendation — routes to the relevant admin screen with context pre-filled (e.g. the campaign builder with the right segment, or the cross-sell settings).
- **Dismiss** a recommendation — it is hidden for the **rest of the day**; the same recommendation (`action_type` + `entity_id`) won't reappear until the next day.
- **Review history** (subscribed only) — the last 20 executed / dismissed actions.

## Plan gating

Gated by the `smart_daily_actions` plan-feature, enforced as a **hard daily cap on actions**:

- **Subscribed** → up to **3 actions per day**, plus the **history** view (last 20 entries).
- **Not subscribed** → **1 action per day** (a teaser to show the feature's value); the history endpoint returns empty.

The cap counts **both executed and dismissed** actions taken today: the widget surfaces only `dailyCap − (actions already taken today)` recommendations, and once the merchant has used up the day's quota it shows **nothing more until the next day** (the recommendations endpoint returns an empty list). So dismissing a card "spends" one of the day's slots just like executing it.

## The 11 recommendation types

Each type is computed from the store's data over a rolling window; a card appears only when its trigger condition is met (and it wasn't dismissed earlier the same day). Titles / reasons / effects below are the verbatim in-product copy.

| Type (`action_type`) | Triggers when (the "why") | Expected effect | Execute goes to |
|---|---|---|---|
| `restock` | *"Sold N units in the last 30 days but is now out of stock"* | *"+€X potential revenue"* | the product (restock) |
| `pause_campaign` | *"Sent to N subscribers but generated only N orders (R% conversion)"* | *"Save budget and reassign to better-performing campaigns"* | the campaign |
| `create_bundle` | *"Top-selling product with N units sold in the last 30 days"* | *"Bundles typically increase average order value by 15–20%"* | bundle creation |
| `follow_up_abandoned` | *"N customers left their cart in the last 7 days without completing the purchase"* | *"Recovery campaigns typically recover 5–15% of abandoned carts"* | `campaigns-create` (regular) |
| `activate_discount` | *"This discount generated N orders but is currently inactive or expired"* | *"Re-enabling a proven discount can quickly boost conversions"* | the discount |
| `send_winback` | *"N customers haven't placed an order in over 90 days"* | *"Win-back campaigns average 10–15% re-engagement rate"* | `campaigns-create` (regular) |
| `low_rating_product` | *"N reviews with an average rating of R — below the 3-star threshold"* | *"Addressing low-rated products reduces returns and improves store trust"* | the product |
| `upsell_opportunity` | *"Top seller with N units sold in 30 days but has no related products configured"* | *"Related products increase average order value by 10–20%"* | the product (related products) |
| `enable_cross_sell` | *"P% of your last-30-day orders contained a single product with no cross-sell configured"* | *"Cross-sell typically adds 1–3 extra items per order"* | `apps.up_cross_sell.settings` ([[apps-up-cross-sell]]) |
| `reactivate_segment` | *"This segment has had no campaign sent to it in the last 60 days"* | *"Targeted re-engagement campaigns typically yield 15–25% open rates"* | `campaigns-create` (regular), segment pre-filled |
| `price_drop_alert` | *"N views but zero orders in the last 30 days — price may be too high"* | *"A 10–15% price adjustment on high-traffic products can significantly lift conversion"* | the product (pricing) |

## Settings & fields

There are **no merchant-configurable settings** for this widget — recommendations are generated automatically from store data, and the only "knob" is whether the store's plan includes `smart_daily_actions` (which decides 1 vs 3 cards + history). The merchant cannot author recommendations, change thresholds, or pick which types appear.

Each action a merchant takes is stored in `smart_actions_history` with these fields:

| Field | Meaning |
|---|---|
| `action_type` | One of the 11 recommendation types (see table above). |
| `entity_id` | The product / campaign / segment / discount the recommendation is about. |
| `status` | `executed` (the merchant acted) or `dismissed` (hidden for the day). |
| `entity_title` | The human label shown on the card (e.g. the product name). |
| `expected_effect` | The projected-benefit string shown on the card. |
| `execute_route` | The admin route the Execute button opened. |

## Business rules

- **Recomputed on each load, within the daily cap.** Recommendations are recalculated every time the widget loads; anything dismissed earlier the same day is excluded, and the number shown is capped by the day's remaining action quota (see Plan gating). Once the quota is spent the list is empty for the rest of the day.
- **Acting is recorded (and counts toward the daily cap).** Execute / Dismiss posts to the act endpoint and writes a row to the `smart_actions_history` store (`action_type`, `entity_id`, `status` = `executed` / `dismissed`, `entity_title`, `expected_effect`, `execute_route`). Both `executed` and `dismissed` consume one of the day's action slots. The stored `entity_title` and `expected_effect` are truncated to 252 characters.
- **History is capped + gated.** The history view returns the latest **20** entries and only for subscribed stores; unsubscribed stores get an empty list.
- **Teaser on the free tier.** Without `smart_daily_actions` the widget still shows **one** recommendation per day — a deliberate nudge toward the paid feature.
- **Data-driven, not configurable.** The merchant cannot author custom recommendations or change the trigger thresholds — the 11 types and their windows (7 / 30 / 60 / 90 days) are platform-defined.

## Related

- [[dashboard]] — the admin dashboard that hosts the widget.
- [[dashboard-insights]] — the Insights (Executive Insights) overview; same `smart_daily_actions` plan-feature, the analytical companion to this widget.
- [[plan-gates]] / [[plan-features]] — the `smart_daily_actions` plan-feature.
- [[marketing-campaigns-create]] — the Execute target for the follow-up-abandoned, win-back, and reactivate-segment recommendations.
- [[apps-up-cross-sell]] — the Execute target for the enable-cross-sell recommendation.
- [[inventory-restock]] — the stock context behind the restock recommendation.
- [[marketing-discounts]] — the discount reactivated by the activate-discount recommendation.

## Open questions

- The exact admin routes the non-campaign Execute buttons open (product editor / bundle / discount screens) are derived per-recommendation from `execute_route`; the campaign + cross-sell targets are confirmed (`campaigns-create`, `apps.up_cross_sell.settings`).
