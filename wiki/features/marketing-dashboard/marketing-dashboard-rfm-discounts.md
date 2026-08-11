---
type: feature
nav_path: "Marketing → Dashboard → RFM & Discounts"
route_name: marketing-dashboard
route_path: /admin/marketing-new/dashboard
aliases: ["RFM Analysis dashboard", "BumpCart performance", "Cart rules performance dashboard", "Product Reviews row", "RFM heatmap", "RFM upsell overlay", "Recency Frequency Monetary", "Преглед на отзиви"]
tags: [marketing, dashboard, rfm, bumpcart, cart-rules, reviews, segmentation]
plan_gates: ["rfm_analysis"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-dashboard]]. See the hub for the other aspects (welcome & steps, overview KPIs, channel performance, quick-launch tiles, campaigns & products, data freshness).

# Dashboard — RFM, Discounts & Reviews

## Purpose

The bottom of the Marketing Suite holds three less-frequently-checked modules grouped together because they all read from the 6-hour snapshot rather than live data: the **Discounts performance row** (BumpCart + Cart Rules tabs), the **RFM Analysis row** (a Recency-Frequency-Monetary heatmap of the subscriber base), and the **Product Reviews row** (recent customer reviews when the Product Review app is installed). These are quarterly / strategic surfaces driving the high-leverage decisions: which customer segment to re-engage, whether the BumpCart upsell is working, what reviewers are saying.

## Where to find it

Sidebar → **Marketing** → **Marketing suite** — Discounts performance sits below the Products row; RFM Analysis sits below it; Product Reviews sits at the bottom (when the Product Review app is installed).

## What the merchant can do here

- **Read BumpCart performance** — Discounts row → "BumpCart" tab: impressions, conversions, revenue from the checkout-page bump-offer.
- **Read Cart Rules performance** — Discounts row → "Cart rules" tab: cumulative impact of all configured automatic cart-rule discounts (does NOT take a date range — it's a snapshot of current cart rules and their lifetime impact).
- **Scan the RFM heatmap** — RFM Analysis row: 90-day Recency / Frequency / Monetary segmentation of the subscriber base, plotted as a heatmap-style grid.
- **Read recent product reviews** — Product Reviews row: recent reviews summary when the Product Review app is installed.

## Settings & fields

### Discounts performance tabs

| Tab | Source | Range-aware? |
|-----|--------|--------------|
| BumpCart | `GET /bump-cart` | Yes — uses the dashboard's range |
| Cart rules | `GET /cart-rules` | **No** — clear-cut snapshot of current rules + cumulative impact |

The Cart rules tab is intentionally range-less because a cart rule's "performance" is its cumulative effect over its lifetime — slicing it by date hides setup decisions made before the picker window.

### RFM Analysis

| Aspect | Value |
|--------|-------|
| Window | 90 days |
| Source | `GET /rfm-analysis` |
| Plan gate | `cc_analytics.rfm` (or the RFM feature flag in subscriber settings — both must be ON to read live data) |
| Layout | Heatmap-style grid: Recency on one axis, Frequency on another, cell colour by Monetary value |

When plan-gated OFF, the section is blurred + overlaid with "RFM Analysis is not active" upsell text and a "View subscribers" link routing to [[marketing-subscribers]] where the merchant can enable subscription tracking.

### Product Reviews row

| Field | Source |
|-------|--------|
| Recent reviews | `GET /reviews` — last N reviews across all products |
| Star summary | aggregate from review records |

The row only renders when the `product_review` app is installed; otherwise the dashboard skips it entirely.

## Business rules

### RFM is blurred + upsold when plan-gated

When the merchant's plan doesn't include `cc_analytics.rfm` OR the RFM feature flag in the subscriber-tracking settings is off, the RFM section renders **visibly** (so the merchant knows the feature exists) but with the heatmap blurred and an "RFM Analysis is not active" overlay + CTA. The CTA links into [[marketing-subscribers]] where the merchant can enable subscription tracking — the prerequisite for RFM data to populate.

### BumpCart tab visibility depends on app install

The BumpCart performance tab renders when the BumpCart app is installed. Stores without BumpCart see only the Cart Rules tab in the Discounts row (verify whether the tab is hidden entirely or shows an empty-state with an install CTA).

### Cart Rules tab takes NO date range

Cart Rules performance is the only tab on the dashboard that ignores the date-range picker. The merchant cannot ask "how did my cart rules do last week" from this surface — only "what's the cumulative effect of my currently-configured rules". Cart rules are a configuration choice, not a campaign, so their impact is a stock measure not a flow measure.

### Product Reviews row depends on app install

The Product Reviews row only renders when the `product_review` app is installed. Uninstalled means no row at all — no placeholder, no install CTA.

### All four modules read from the 6-hour snapshot

RFM, BumpCart, Cart Rules, and Product Reviews are all collected by the MarketingDashboard scheduled job. A new review, a freshly configured cart rule, or a BumpCart impression burst won't appear until the next collector cycle (up to 6 h). Full rules on [[marketing-dashboard-data-freshness]].

### RFM data freshness — gated by subscriber-tracking

The RFM module additionally requires subscription tracking to be enabled on [[marketing-subscribers]] (otherwise the source subscriber-order joins never populate). After enabling tracking, RFM stays empty for at least one collector cycle (up to 6 h) before the first payload appears.

### Moderator permission to see RFM

Reading RFM requires the broad `marketing` permission OR the specific `marketing.subscribers` child permission. A moderator without either sees the row blurred even if the plan includes `cc_analytics.rfm`. Granted from [[settings-staff]].

## How it works

Each row queries its own endpoint under `/admin/api/core/marketing/`: `GET /bump-cart` (BumpCart), `GET /cart-rules` (Cart rules), `GET /rfm-analysis` + `GET /subscribers/settings` (RFM), `GET /reviews` (Reviews). All four read from the `dashboard` snapshot table written by the MarketingDashboard collector job. Collector workers run independently — a failed RFM collector doesn't block the BumpCart payload. See [[marketing-dashboard-data-freshness]] for the per-module collector breakdown.

The RFM heatmap is rendered client-side from the snapshot payload — no live aggregation. The "RFM Analysis is not active" overlay is purely visual; the underlying data field is still populated to avoid layout shift if the merchant activates the plan feature later.

## Recommended merchant use

- **Quarterly subscriber-base health check** — read RFM once a quarter; watch the high-Recency / high-Monetary cells (best customers) and the high-Frequency / low-Recency cells (churned regulars to win back).
- **Bump-offer optimisation** — read BumpCart impressions vs conversions monthly; if conversion rate drops below the merchant's threshold, re-edit the bump-offer copy.
- **Cart-rule audit** — open the Cart Rules tab when reviewing why margins look soft — see which automatic discounts are eating the most revenue.
- **Reputation pulse** — scan recent reviews weekly; low-star reviews on high-revenue products are urgent flags.

## Related

- [[marketing-dashboard]] — hub.
- [[marketing-dashboard-data-freshness]] — why all four modules can be up to 6 hours stale.
- [[marketing-subscribers]] — subscriber CRM; RFM module's CTA target + the page where subscription tracking is enabled.
- [[marketing-discounts]] — discount manager; BumpCart and Cart Rules are surfaced here in detail.
- [[apps-cart-rules]] — Cart Rules app (powers the Cart rules tab).
- [[apps-bumpcart]] — BumpCart app (powers the BumpCart tab).
- [[apps-product-review]] — Product Review app (powers the Reviews row).
- [[plan-gates]] — `cc_analytics.rfm` feature gate.
- [[settings-staff]] — moderator permissions.
- [[subscriber]] — Subscriber entity (RFM rows are subscribers).

## Open questions

- Confirm whether the BumpCart tab hides entirely or shows an empty-state when the BumpCart app is not installed.
