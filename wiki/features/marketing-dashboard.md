---
type: feature
nav_path: "Marketing → Dashboard"
route_name: marketing-dashboard
route_path: /admin/marketing-new/dashboard
aliases: ["Marketing Suite", "Marketing Suite Dashboard", "Marketing dashboard", "Маркетингова сюита", "Маркетингов дашборд"]
tags: [marketing, dashboard, kpi, analytics]
plan_gates: ["rfm_analysis"]
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---

# Dashboard

## Purpose

The **Marketing Suite Dashboard** is the merchant's command center for all marketing activity — the single screen that answers *"How is my marketing actually doing?"* across every channel and every campaign at once. It welcomes the merchant with a setup checklist, shows period-over-period KPIs (orders, AOV, customers, accepting-marketing subscribers, customer value, open / click / conversion rates, marketing-driven sales and revenue), surfaces a per-channel performance breakdown for **Email / SMS / Viber / Web push**, lists the top-revenue and most-recent campaigns, highlights favourite and "back-in-stock-expected" products, summarises **BumpCart** and **Cart rule** discount performance, and presents an **RFM (Recency-Frequency-Monetary) analysis** of the subscriber base. Quick-launch tiles at the top let the merchant jump into "New Campaign", "New Segment", "New Popup", "New Discount", or the legacy Cross-Sell screen without leaving the dashboard.

This is the **landing page** of the new Vue-based Marketing area — opening "Marketing → Marketing suite" in the sidebar lands the merchant here.

## Where to find it

Sidebar → **Marketing** → **Marketing suite**.

The route is `/admin/marketing-new/dashboard`. The parent `marketing` route (`/admin/marketing-new`) redirects here by default.

## What the merchant can do here

The dashboard is a top-to-bottom stack of module rows: welcome + setup checklist, two-tier KPI grid, per-channel breakdown, quick-launch tiles, campaigns + products tables, then the RFM heatmap + discounts performance + reviews. Each row is documented in its own aspect page (see below) — the Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[marketing-dashboard-welcome-steps]] — the welcome card, embedded help video, 5-step setup checklist (Google Analytics / Google Ads / Search Console / MC Channels / Facebook Pixel), per-step confirm popover, "Mark all complete" bulk action.
- [[marketing-dashboard-overview-kpis]] — Overview row (Orders, AOV, Customers, Accepting marketing, Customer value), Marketing-results row (Open rate, Click rate, Conversion rate, Marketing sales, Revenue), shared date-range picker, compare-period / compare-year deltas.
- [[marketing-dashboard-channel-performance]] — per-channel cards (Sent / Delivered / Revenue) for Email / Viber / SMS / Web push, own range-picker independent of the Overview, channel-activation CTA when inactive.
- [[marketing-dashboard-quick-launch]] — the 5 "Marketing activities" tiles (New Campaign, New Segment, New Popup, New Discount, Cross-Sell) and their modal-or-redirect targets.
- [[marketing-dashboard-campaigns-products]] — Campaigns row tabs (Top / Recent), Favorite & Expected products tabs, the restock modal that lets the merchant lift `total_quantity = 0` rows in-place.
- [[marketing-dashboard-rfm-discounts]] — RFM 90-day heatmap (plan-gated), BumpCart performance tab, Cart Rules performance tab, recent Product Reviews summary.
- [[marketing-dashboard-data-freshness]] — what's live vs scheduled (the 6-hour collector job, the `dashboard` table, the disabled-site skip rules), the cache TTLs per module, the "All time" → "last year" backend cap, plan gating, moderator permissions.

## Settings & fields

This hub page does not own settings directly — every visible control lives inside one of the aspect rows. The cross-row controls are:

- **Date-range picker** (component `MarketingDashboardRangePicker`) — drives the Overview + Marketing-results rows. See [[marketing-dashboard-overview-kpis]].
- **Compare selector** (none / `period` / `year`) — drives the deltas on the Marketing-results tiles. See [[marketing-dashboard-overview-kpis]].
- **Channel-performance range picker** — separate range-picker on the channel-performance row header, so the merchant can compare channel KPIs across a different window. See [[marketing-dashboard-channel-performance]].

## Business rules

These three rules cut across multiple rows and belong on the hub. The row-specific rules sit on each aspect.

### Two distinct money figures — Revenue vs Marketing sales

The dashboard surfaces TWO money figures across the Overview and per-channel rows:

- **Revenue** — total store revenue in the period (all orders, regardless of acquisition source).
- **Marketing sales** — revenue from orders attributed to marketing campaigns (via UTM parameters / campaign tracking IDs / abandoned-cart recovery / subscriber-to-campaign joins).

Marketing sales is the more important number for campaign ROI calculations. Revenue is shown for context (so the merchant can see what share of total revenue is marketing-driven).

### Quick-launch tiles bypass list pages

The top "Marketing activities" tiles open modals or jump to create routes directly — they're optimised for "I want to start a new X" workflows, not "I want to manage existing Xs". The list pages are reached through the sidebar dropdowns or the Campaigns row's table links. See [[marketing-dashboard-quick-launch]].

### Module freshness varies — some live, some up to 6 hours stale

Overview, Marketing-results, and Channel-performance read **live** with short caches (5 min / 1 h / 10 min). Everything else (RFM, BumpCart, Cart Rules, Favorites, Expected, Campaigns lists, Reviews) reads from a snapshot table refreshed by a **6-hour scheduled collector**. A merchant viewing the dashboard right after running a campaign will see the campaign in Overview within ~5 min but won't see it in the Campaigns row until the next collector cycle. The full rules live on [[marketing-dashboard-data-freshness]].

## How it works

The page is a thin wrapper assembling the rows in fixed order: steps → general overview → channel performance → quick-launch tiles → campaigns → products (favourites + expected) → discounts performance → RFM analysis → product reviews. Every row queries an endpoint under `/admin/api/core/marketing/`; the endpoint list is enumerated on [[marketing-dashboard-data-freshness]].

All marketing-area endpoints are gated by the `marketing` API permission OR the specific child permission for the underlying module (e.g., `marketing.subscribers` for RFM, `marketing.discounts` for cart-rules row). Administrators always pass; moderators must be granted the permission from [[settings-staff]] → Access permissions.

## Recommended merchant use

- **Daily / weekly health check** — open this page, scan the Overview deltas (see [[marketing-dashboard-overview-kpis]]), drill into any channel showing a sudden drop (see [[marketing-dashboard-channel-performance]]).
- **Onboarding** — work through the 5-step setup row to wire up tracking & messaging channels — see [[marketing-dashboard-welcome-steps]].
- **Campaign retrospectives** — set the Overview date range to the campaign window and look at Marketing sales / Conversion rate / Revenue deltas — see [[marketing-dashboard-overview-kpis]].
- **Subscriber-base health** — scroll to the RFM section once a quarter to spot churned high-value segments — see [[marketing-dashboard-rfm-discounts]].

## Related

- [[marketing]] — parent hub.
- [[marketing-campaigns]] — Campaigns list — opened by the Campaigns row table.
- [[marketing-campaigns-policy]] — gating policy that must be accepted before reaching Channels from this dashboard.
- [[marketing-omnichannel-mails-list]] — transactional email templates (separate from this dashboard's metrics).
- [[marketing-segments]] — segments — created via the "New Segment" tile.
- [[marketing-subscribers]] — subscriber CRM — RFM links here.
- [[marketing-subscribers-subscribe-forms]] — popup form creator — "New Popup" tile target.
- [[marketing-discounts]] — discount manager — "New Discount" tile target.
- [[marketing-cross-sell]] — Cross-sell / Upsell — quick-launch tile target.
- [[analytics-total-sales]] — the canonical revenue number (this dashboard surfaces a subset of analytics).
- [[campaign]] — Campaign entity.
- [[subscriber]] — Subscriber entity.
- [[segment]] — Segment entity.
- [[channel]] — Channel entity.
- [[notification-delivery]] — outbound message delivery internals.
- [[plan-gates]] — `cc_analytics.rfm`, `cc_analytics.allow_period_compare`, related plan limits.
- [[settings-staff]] — moderator permissions that gate dashboard module visibility.

## Open questions

No outstanding questions.
