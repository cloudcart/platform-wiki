---
type: feature
nav_path: "Marketing → Dashboard → Campaigns & Products"
route_name: marketing-dashboard
route_path: /admin/marketing-new/dashboard
aliases: ["Top campaigns row", "Recent campaigns row", "Favorite products dashboard", "Expected products dashboard", "Restock modal dashboard", "Back-in-stock dashboard", "Маркетинг кампании топ", "Любими продукти", "Очаквани продукти"]
tags: [marketing, dashboard, campaigns, products, favorites, expected, restock]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-dashboard]]. See the hub for the other aspects (welcome & steps, overview KPIs, channel performance, quick-launch tiles, RFM & discounts, data freshness).

# Dashboard — Campaigns & Products

## Purpose

Two adjacent tabbed-table rows that surface **what the merchant should pay attention to**: a Campaigns row ranking campaigns by revenue / recency, and a Products row split between **Favorite** products (most-wishlisted) and **Expected** products (customers waiting on back-in-stock). The Products row is the only place on the dashboard where the merchant can take a corrective action without leaving — a **Restock modal** lets them lift an out-of-stock row's `total_quantity` in-place.

## Where to find it

Sidebar → **Marketing** → **Marketing suite** — the Campaigns row sits below the Quick-launch tiles; the Products row sits immediately below it.

## What the merchant can do here

- **Read the top-revenue campaigns** — Campaigns row → "Top Campaigns" tab, ranked by generated revenue in the selected period.
- **Read the most recent campaigns** — Campaigns row → "Recent Campaigns" tab, ordered by created/edited date.
- **Jump to a campaign's editor** — click any campaign title in either tab.
- **Start a new campaign from the row header** — a "+ Create campaign" link routes to `campaigns-active` with default listing query (this is the alternative entry-point to the New Campaign quick-launch tile — see [[marketing-dashboard-quick-launch]]).
- **Read the most-favourited products** — Products row → "Favorite" tab (heart icon).
- **Read the most-awaited products** — Products row → "Expected" tab (bell icon) — products customers subscribed to via "Notify me when available" forms while out of stock.
- **Restock an out-of-stock favourite or expected product** — click the row's action when `total_quantity = 0` to open the **Restock modal** + set a new quantity inline.

## Settings & fields

### Campaigns row tabs

| Tab | Source | Order |
|-----|--------|-------|
| Top Campaigns | `GET /campaigns-revenue` | Ranked by generated revenue in selected period |
| Recent Campaigns | `GET /campaigns-recent` | Most recently created / edited campaigns |

Each row shows campaign title, a status badge, and links to the campaign editor.

### Products row tabs

| Tab | Source | Icon | Description |
|-----|--------|------|-------------|
| Favorite | `GET /products-favorites` | heart | Products customers have favourited the most |
| Expected | `GET /products-expected` | bell | Products subscribed to via "Notify me when available" forms while out of stock |

Each tab summarises three KPI cards (count and revenue stats) above the table. The table lets the merchant restock a product directly via the Restock modal when `total_quantity = 0`.

### Restock modal (`MarketingDashboardProductsModalRestock`)

| Field | Default | Validation |
|-------|---------|------------|
| Quantity | (blank) | Numeric, minimum `0`; Save is disabled while blank |

Modal layout:

- **Headerless** — the title *"Update product quantity"* renders inside the body paired with a faint-grey times-X close icon.
- **Single field** — Quantity (numeric, min `0`).
- **Footer** — ghost **Cancel** + primary **Save**. Save is disabled until the field is non-null.
- **In-flight protection** — while the mutation is in flight, the close-X is dimmed and backdrop close is disabled; the merchant cannot dismiss mid-save.
- **Success toast** — *"Updated successfully"*. The modal closes and the row's `total_quantity` is updated inline (no full table reload) — the parent cache is patched keyed on the current `all_time` query.

## Business rules

### Campaigns row only counts active, non-archived campaigns

Both Top and Recent tabs only consider campaigns matching the platform code — archived campaigns never appear here regardless of how much revenue they generated. See [[marketing-campaigns-archive]] for the full archive semantics.

### Restock modal only appears when `total_quantity = 0`

The restock action is row-conditional. For products still in stock there is **no** restock affordance. The entire Actions column is hidden from the table when **no row** has `total_quantity = 0` (the column is appended via spread-and-filter at render time), keeping the table compact when there's nothing to restock. The same Vue component renders the modal for both Favorite and Expected tabs — only the `type` prop and the cache target differ.

### Restock writes via the products mutation endpoint

The Save action POSTs to the products mutation API with `{ ids: [variant_id], action: 'set', quantity: <typed> }` — the same endpoint used by [[products-inventory]] for bulk quantity edits, just called with a single ID. Stock changes through this modal are logged in the parent product's [[products-change-log|Change log]] with the dashboard as the initiator (verify the exact label).

### Campaigns + Products rows are scheduled, not live

Both rows read pre-collected snapshots from the `dashboard` table, refreshed by the 6-hour MarketingDashboard collector job. A campaign that just generated revenue, or a product just favourited or subscribed-to, won't appear until the next cycle. Full rules on [[marketing-dashboard-data-freshness]].

### Expected products mirrors the dedicated subscribers page

The "Expected" tab is the dashboard's read-side view of the same back-in-stock subscription list that [[products-missing-product]] surfaces — both pull from the storefront's "Notify me when available" records. Restocking here triggers the same downstream notifications (low-stock alerts cleared, back-in-stock emails fired) as restocking on [[products-inventory]].

### "+ Create campaign" goes to the list, not a modal

The Campaigns row's "+ Create campaign" link routes to the campaigns list with a default query — it does NOT open the same modal as the New Campaign quick-launch tile on [[marketing-dashboard-quick-launch]]. Both lead to campaign creation eventually, through different surfaces.

## How it works

The Campaigns row queries `GET /admin/api/core/marketing/campaigns-revenue` and `/campaigns-recent`. The Products row queries `/products-favorites` and `/products-expected`. All four endpoints read from the `dashboard` snapshot table, NOT from a live join — so the numbers can be up to 6 hours stale.

The restock mutation queries the regular products write API (not the marketing dashboard API). On success, the dashboard patches its in-memory query cache for the affected tab using the row's variant ID — no full table reload.

## Recommended merchant use

- **Weekly campaign portfolio review** — scan Top Campaigns; if a campaign is silent for two consecutive reviews, archive it via [[marketing-campaigns-archive]].
- **Restock prioritisation** — open the Expected tab once a week; restock anything with a high subscriber count first.
- **Wishlist insight** — Favorite tab tells the merchant what their customers WANT to buy — high-favourite-count products with low inventory turnover signal price-sensitivity that a discount might unlock.

## Related

- [[marketing-dashboard]] — hub.
- [[marketing-dashboard-quick-launch]] — the New Campaign tile (alternative entry point to the "+ Create campaign" header link).
- [[marketing-dashboard-data-freshness]] — why these tables can be up to 6 hours behind.
- [[marketing-campaigns]] — Campaigns list — destination of campaign-title clicks.
- [[marketing-campaigns-archive]] — archived-campaign semantics; archived campaigns NEVER appear here.
- [[products-missing-product]] — the dedicated back-in-stock subscribers page (Expected tab's full surface).
- [[products-favorite-products]] — the dedicated wishlist-counts page (Favorite tab's full surface).
- [[products-inventory]] — bulk-quantity management; same mutation endpoint as the Restock modal.
- [[products-change-log]] — audit trail of stock changes (including ones from the Restock modal).
- [[campaign]] — Campaign entity.
- [[product]] — Product entity.

## Open questions

- Confirm the exact initiator label written to [[products-change-log]] when stock is updated via the Restock modal.
