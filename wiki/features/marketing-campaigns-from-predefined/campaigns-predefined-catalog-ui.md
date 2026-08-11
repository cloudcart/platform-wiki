---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → From template → Catalog UI"
route_name: admin.api.campaigns.create
route_path: /admin/api/core/marketing/campaigns/create
aliases: ["Predefined campaign catalog", "Best practices grid", "Predefined card grid", "Шаблонни кампании — каталог"]
tags: [marketing, campaigns, predefined, templates, ui]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
> Part of [[marketing-campaigns-from-predefined]]. See the hub for the other aspects (clone flow, channel gate, segment & tags, curation).

# Predefined campaigns — the catalog UI

## Purpose

This page documents the **card grid** that renders the predefined-campaign catalog inside the **Automated** tab of the Create-campaign modal. It is the read-only browse surface — what the merchant sees, where its data comes from, how the cards are laid out, and what shows in the empty / loading states. The action a card triggers is documented in [[campaigns-predefined-clone-flow]].

## Where to find it

Sidebar → **Marketing** → **Campaigns** → **+ Create campaign** → **Automated** tab → the lower section, below the "Create your own automation" box.

The catalog renders as the lower section of the **Automated** tab inside the `MarketingCampaignsCreateModal` (see [[marketing-campaigns-create]] for the modal's full anatomy). There is no separate browsing route — the catalog is always embedded in the modal.

## What the merchant can do here

- **Browse** every predefined campaign available in the store's language as a grid of card tiles.
- **Read** each card's title and short description to decide which best-practice funnel fits the scenario.
- **Click Create campaign** on a card to clone it — handled in [[campaigns-predefined-clone-flow]].
- **Fall through to the manual path** — if no template fits, the "Create your own automation" box above the grid builds an empty Automated campaign instead.

## Settings & fields

### Source of the catalog

When the Create-campaign modal opens, `getTabsAndTemplates` calls `GET /admin/api/core/marketing/campaigns/create` (the `apiMarketingCampaigns.meta` query). The response is an array of campaign-type metadata blocks; the Automated tab unpacks:

```
metaData.find(item => item.type === 'automated').predefined
```

Each predefined item has at least `{id, title, description}`. The list is **server-pre-filtered** to exclude templates whose required channels are not configured on the store — see [[campaigns-predefined-channel-gate]].

### Layout

- **Section label** above the grid: *"Or choose one of our predefined best practices"* — only rendered when `predefinedCampaigns.length > 0`.
- **Grid:** `grid-cols-1 lg:grid-cols-3 md:grid-cols-2 gap-4` — responsive 3-column / 2-column / 1-column.
- **Loader:** a centered `CcLoader` shows while `isLoadingPredefined` is true (the meta query in flight).

### Card anatomy

Each card is a white-bg rounded box with a 1-px grey border, padded `p-4`, full-height flex column:

| Element | Content | Source |
|---------|---------|--------|
| Title (top) | base text-medium | `campaign.title` (translated) |
| Description (middle, `flex-1`) | small grey text | `campaign.description` (translated) |
| Action link (bottom) | purple **Create campaign** link | hits the clone endpoint via AJAX |

The cards are laid out in rows of 3; on smaller viewports each card stacks full-width. The action is an `<a>`, not a button — it carries `@click.prevent="handleCreateFromPredefined(campaign.id)"`. While that specific card is being created, the link gets `opacity-60 pointer-events-none`; other cards remain clickable.

### Empty state

If `predefinedCampaigns.length === 0` (e.g. the merchant's locale has no active templates AND the fallback locale also returns empty), the section label + grid are simply omitted. The "Create your own automation" card above remains the only option.

## Business rules

### Locale-aware browsing

The catalog respects the store's site language — it first looks for active templates matching the store's current language. If zero templates match, the platform falls back to the app's configured fallback locale — typically English. So a Bulgarian-language store with English-only catalog entries will see those English templates, and vice versa.

### Cards only render templates with a complete `data.campaign` payload

A predefined campaign is only valid if its JSON `data` blob contains a `campaign` key — otherwise the clone endpoint returns 404. CloudCart's curation flow ensures every active template ships with a complete payload (see [[campaigns-predefined-curation]]), but the protective check exists server-side: if the template lacks a `data.campaign` payload, the clone endpoint throws 404.

### Required channels are pre-filtered out of the grid

The modern `GET /admin/api/core/marketing/campaigns/create` endpoint that feeds this grid **already excludes** predefined campaigns whose required channels are missing on the store — so the merchant never sees a template they can't clone. The legacy sitecp picker did NOT pre-filter. Full mechanics in [[campaigns-predefined-channel-gate]].

## Related

- [[marketing-campaigns-from-predefined]] — hub.
- [[marketing-campaigns-create]] — parent picker; this grid is the lower half of its Automated tab.
- [[campaigns-predefined-clone-flow]] — what the **Create campaign** link triggers.
- [[campaigns-predefined-channel-gate]] — why some templates never appear in the grid.
- [[marketing-campaigns-edit]] — where the merchant lands after cloning.

## Open questions

None.
