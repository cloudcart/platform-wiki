---
type: feature
nav_path: "Marketing → Dashboard → Quick-launch tiles"
route_name: marketing-dashboard
route_path: /admin/marketing-new/dashboard
aliases: ["Marketing activities row", "Quick-launch tiles", "New Campaign tile", "New Segment tile", "New Popup tile", "New Discount tile", "Cross-sell tile", "Маркетинг бързи действия"]
tags: [marketing, dashboard, quick-launch, modal, navigation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-dashboard]]. See the hub for the other aspects (welcome & steps, overview KPIs, channel performance, campaigns & products, RFM & discounts, data freshness).

# Dashboard — Quick-launch tiles

## Purpose

The **Marketing activities row** is the five-tile shortcut strip that lets the merchant **start** a new marketing activity from the dashboard without navigating away. Each tile is a "create" jump — straight into a modal builder, into an SPA route, or (for Cross-Sell only) into the legacy Smarty page. The row is the dashboard's answer to *"I want to set up a new X"* — it deliberately skips the list pages, which are reached via the sidebar dropdowns or the Campaigns row table.

## Where to find it

Sidebar → **Marketing** → **Marketing suite** — fourth row of the dashboard, directly below the Channel performance row.

## What the merchant can do here

Five tiles, left-to-right:

- **New Campaign** — opens a tabbed modal where the merchant picks Regular or Automated.
- **New Segment** — opens a two-step modal chain: type-chooser then editor.
- **New Popup** — SPA-navigates into the popup-form builder (no modal).
- **New Discount** — opens a modal listing discount-type tiles.
- **Cross-Sell** — full-URL navigation to the legacy Smarty Cross-Sell list.

## Settings & fields

### Tile → target mapping

| Tile | Target type | Target |
|------|-------------|--------|
| New Campaign | Modal | `MarketingCampaignsCreateModal` — tabbed (**Regular** / **Automated**), default tab `regular` |
| New Segment | Modal chain | `MarketingSegmentAddModal` (chooser) → `MarketingSegmentCreateOrEditModal` (editor) |
| New Popup | SPA navigation | route `subscribe-forms.form` |
| New Discount | Modal | `DiscountsCreateDiscountModal` — lists discount-type tiles; picking one navigates to that type's builder |
| Cross-Sell | Full-URL navigation | `ADMIN_CROSS_SELL_LIST_HREF` (legacy Smarty page) |

### New Segment — two-step modal chain

The New Segment flow is the only multi-step one on this row:

1. **`MarketingSegmentAddModal`** (chooser) — the merchant picks a **segment type** (`regular` or `automated trigger`) and optionally seeds the segment with **initial conditions**.
2. **`MarketingSegmentCreateOrEditModal`** (create) — opens automatically after the chooser closes; pre-filled with the `segmentType` + `initialConditions` the chooser collected.

The merchant can't reach step 2 without going through step 1 — there's no "skip to editor" affordance.

## Business rules

### Cross-Sell tile leaves the Vue dashboard

The **Cross-Sell** tile uses a full-URL navigation, NOT an SPA route — it leaves the Vue dashboard entirely and loads the legacy Smarty Cross-Sell list page. The back button works normally (browser history), but the Marketing dashboard state (date ranges, picked tabs) is lost on return because the page fully reloads. This is intentional — Cross-Sell hasn't been migrated to the new Marketing Suite yet.

### New Popup is the only tile that uses SPA navigation (no modal)

Four of the five tiles open a modal on top of the dashboard. The **New Popup** tile is the exception — it SPA-navigates into the popup-form builder route, leaving the dashboard. This is because popup forms have their own multi-tab editor that doesn't fit a modal. See [[marketing-subscribers-subscribe-forms]].

### Discount tile chains a second navigation

The **New Discount** modal lists discount-type tiles (flat / percent / shipping / fixed / quantity / countdown / code-pro / codes). Picking one closes the modal AND navigates to that discount's dedicated builder. So the merchant ends up on a different SPA route by the time they're done — they don't return to the dashboard automatically.

### Tile visibility is not plan-gated

All five tiles render unconditionally on the dashboard. Plan-gated affordances live inside the target builders (e.g., creating an Automated campaign may require a plan feature once the merchant is inside `MarketingCampaignsCreateModal`). The dashboard itself doesn't hide tiles based on plan.

### Tiles bypass list pages

The top "Marketing activities" tiles open creators directly — they're optimised for "I want to start a new X" workflows, **not** "I want to manage existing Xs". To browse and manage existing campaigns / segments / popups / discounts, the merchant uses the sidebar dropdowns or the Campaigns row table on [[marketing-dashboard-campaigns-products]].

### Moderator permissions can hide tiles

The marketing API permission gate applies — moderators without the broad **Marketing** permission OR the specific child permission for the target won't see the tile. For example, a moderator with only `marketing.discounts` will see the New Discount tile but not New Segment. Owners always see all five. Permissions are granted from [[settings-staff]] → Access permissions.

## How it works

The row is purely client-side — no API call is made on tile click until the underlying modal/route loads. Each tile dispatches:

- a Vue-Router `push` to the SPA target route (for New Campaign, New Segment, New Popup, New Discount), OR
- a full `window.location` assignment to `ADMIN_CROSS_SELL_LIST_HREF` (for Cross-Sell).

Modals are mounted into the dashboard's modal-stack overlay — the dashboard rows behind them stay alive but become non-interactive. Closing the modal returns the merchant to the dashboard with all module state preserved (date ranges, picked tabs, expanded sections).

## Recommended merchant use

- **Spin up a new campaign mid-review** — when the merchant spots a channel under-performing on [[marketing-dashboard-channel-performance]], the New Campaign tile is the fastest path to a corrective campaign.
- **Build an ad-hoc segment** — when the merchant wants to target a specific subscriber slice (e.g., "bought in the last 30 days but no email opens"), New Segment opens the chooser inline.
- **Quick discount during a Q4 push** — New Discount lets the merchant compose a flash discount without leaving the dashboard.

## Related

- [[marketing-dashboard]] — hub.
- [[marketing-campaigns-create]] — the Create-Campaign modal target.
- [[marketing-segments]] — the Segments list (target of the chooser+editor chain).
- [[marketing-subscribers-subscribe-forms]] — the popup-form builder (target of New Popup).
- [[marketing-discounts]] — the Discounts hub (target of New Discount).
- [[marketing-cross-sell]] — Cross-Sell legacy page (target of the Cross-Sell tile).
- [[settings-staff]] — moderator permissions that gate tile visibility.

## Open questions

No outstanding questions.
