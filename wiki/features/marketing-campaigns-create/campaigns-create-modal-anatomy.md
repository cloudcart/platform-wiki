---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → Modal anatomy"
route_name: campaigns-create
route_path: /admin/marketing-new/campaigns/create/:type(regular|automated)
aliases: ["Create campaign modal", "New campaign picker layout", "Campaign type picker tabs", "Custom Automation card", "Create campaign modal anatomy"]
tags: [marketing, campaigns, create]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Create campaign — modal anatomy

> Part of [[marketing-campaigns-create]]. See the hub for related aspects (Regular vs Automated, predefined clone, draft business rules).

## Purpose

This aspect documents the **modern Vue picker** the merchant actually sees — the `MarketingCampaignsCreateModal` popup: its shell, the two tabs, the Regular card, the Automated three-area layout, the predefined grid, the modal loader / meta query, and the per-card loading states. It is the layout-and-interaction reference for the [[marketing-campaigns-create|Create campaign]] flow.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click **+ Create campaign** in the top-right of any tab. The picker opens as a modal overlay, not a separate page.

## What the merchant can do here

- Toggle between the **Regular** and **Automated** tabs (client-side, no AJAX).
- On Regular: click the single **Create campaign** button.
- On Automated: click **Create campaign** in the *Custom Automation* card, OR click **Create campaign** on any card in the predefined best-practices grid.
- Close via X, backdrop click, or Escape.

## Settings & fields

### Modal-level behaviour

This is a `CcPopup` of size `lg` titled *"Create new campaign"*; the body is a two-tab segmented control (`MarketingCampaignsModalTabs`).

| Property | Value |
|----------|-------|
| Title | *"Create new campaign"* |
| Size | `lg` |
| Closes on backdrop click | Yes |
| Closes on Escape | Yes |
| Auto-closes on route change to `campaigns-create` / `campaigns-edit` | Yes — `watch(route.name)` in `useCampaigns` |

### Two tabs

| Tab id | Label | Body component | Default-active when… |
|--------|-------|----------------|----------------------|
| `regular` | *"Regular"* | `MarketingCampaignsRegularTemplate` | Set by header **+ Create campaign** click (`activeModalTab.value = 'regular'`) |
| `automated` | *"Automated"* | `MarketingCampaignsAutomatedTemplate` | Set when arriving from contexts that explicitly prefer automated |

Switching tabs is purely client-side via `<component:is="activeTabComponent">` — no AJAX fetch, the predefined catalog was already loaded by the modal-open meta query.

### Regular tab — fields and buttons

| Element | Value / behaviour |
|---------|-------------------|
| Icon | `fa-light fa-calendar-day` in a soft-purple rounded square |
| Heading | *"Create regular campaign"* |
| Subtitle | *"Keep your subscribers engaged by sharing your latest news, promoting a line of products or announcing an event"* |
| **Create campaign** button | Variant `primary`; on click: `POST /admin/api/core/marketing/campaigns` with body `{type: 'regular', title: null, active: 2}`. On success the router navigates to `campaigns-edit/regular/{id}`. On error: toast *"Error creating campaign"*. The button shows a loading spinner during the request. |

### Automated tab — three areas

1. **Section label:** *"Start from scratch"* (medium weight, top).
2. **Custom Automation card** (white box with grey border):
   - `fa-light fa-bolt` icon in a soft-purple rounded square
   - Title *"Custom Automation"* (semibold)
   - Subtitle *"Create your own automation. You can start from scratch defining your own ideas"*
   - **Create campaign** button (primary). Calls `POST /admin/api/core/marketing/campaigns` with `{type: 'automated', title: null, active: 2}` and navigates to `campaigns-edit/automated/{id}` on success. Loading spinner during request.
3. **Predefined catalog** (renders only when `predefinedCampaigns.length > 0`):
   - Section label *"Or choose one of our predefined best practices"*
   - Loader spinner while the meta query is in flight
   - 3-column responsive grid (`grid-cols-1 lg:grid-cols-3 md:grid-cols-2`), each card showing: title + description + a purple **Create campaign** link
   - Card click calls `GET /admin/api/core/marketing/campaigns/create/automated/{predefined_id}` (the `createFromPredefined` mutation) — full clone behaviour on [[campaigns-create-predefined-clone]].

### Modal-loader and meta query

When the modal opens for the first time (or when `data.value` is null), `getTabsAndTemplates` runs:

1. Sets `modalLoader = true` → the body is replaced with a centered `CcLoader` while loading.
2. Refetches `GET /admin/api/core/marketing/campaigns/create` (`apiMarketingCampaigns.meta.useQuery`).
3. The response contains a list of campaign types with their predefined-template catalogs; the Automated tab unpacks `data.find(item => item.type === 'automated').predefined` to render its grid.
4. Sets `modalLoader = false` and the body renders.

If the meta fetch fails, a toast *"Error loading campaigns"* surfaces and the body stays empty.

## Business rules

### Per-card loading state

When the merchant clicks **Create campaign** on a predefined card, the button enters a per-card loading state (opacity-60 + pointer-events-none on **that card only** — other cards remain clickable). The Regular and Custom-Automation buttons are bound to a separate `isCreating` ref.

### Cross-modal disabling

A single `creatingPredefinedId` ref tracks which predefined card the merchant is creating from. While set, that card's link is disabled. The Custom Automation button uses the separate `isCreating` ref. These two states do NOT cross-disable each other — the merchant can theoretically click Custom Automation while a predefined card is loading.

### Tab switch never writes data

Switching between Regular and Automated is UI-only; nothing is persisted until a **Create campaign** button is clicked. See [[campaigns-create-draft-business-rules]].

## Related

- [[marketing-campaigns-create]] — hub.
- [[marketing-campaigns-edit]] — the editor the modal navigates to on success.
- [[campaign]] — Campaign entity created on submit.

## Open questions

None.
