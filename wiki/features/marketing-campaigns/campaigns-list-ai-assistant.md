---
type: feature
nav_path: "Marketing → Campaigns → AI Assistant drawer"
route_name: campaigns
route_path: /admin/marketing-new/campaigns
aliases: ["AI Campaign Assistant", "Campaign suggestions drawer", "Seasonal suggestions", "Trending suggestions", "Behaviour suggestions"]
tags: [marketing, campaigns, ai, suggestions, drawer]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns]]. See the hub for the other aspects (tabs & filters, create modal, row actions, types & actions, rules, execution internals).

# Campaigns — AI Assistant drawer

## Purpose

The **AI Campaign Assistant** is a drawer that slides down from the top of the Campaigns list and surfaces machine-generated campaign suggestions based on the store's customer behaviour, seasonal calendar, and trending-product signals. Each suggestion can be created as a Draft campaign in one click, pre-filled with a title, description, channel, and example message body.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → **AI Assistant** button (cloudio-variant button with sparkles icon) in the page header. The drawer slides down with a 220 ms transition. It is **not** a modal — the table below stays visible and clickable.

## What the merchant can do here

- Browse three categories of suggestions: events / trending / behaviour.
- Click **Create** on any suggestion card to mint a Draft campaign pre-filled with that suggestion's metadata.
- Close the drawer via the **Hide assistant** link in the top-right corner.

## Settings & fields

### Drawer header

- Sparkles icon + heading *"AI Campaign Assistant"*
- Subtitle *"Smart campaign suggestions based on customer behaviour, season, trending products"*
- **Hide assistant** link in the top-right corner closes the drawer.

### Three suggestion tabs

Pill-shaped buttons with `bg-[#EDEEFA]`:

| Tab key | Icon | Source |
|---------|------|--------|
| `events` | calendar | Seasonal / event suggestions (Black Friday, Mother's Day, etc.) — falls back to static when the AI suggestions endpoint returns `fallback: true` |
| `trending` | chart-line-up | Trending products in the store |
| `behavior` | users | Customer-behaviour-derived suggestions (e.g., abandoned cart) |

Labels for each tab come from the `useSeasonalSuggestions` composable (verify) and may localise per merchant language.

### Suggestion card layout

While suggestions are loading the drawer shows **3 skeleton cards** with pulse animation (icon block, two text bars, two badge bars).

- Coloured gradient background based on `tone`:

  | `tone` value | Gradient colour |
  |--------------|-----------------|
  | `warm` | orange |
  | `cool` | blue |
  | `celebration` | pink |
  | `urgent` | red |
  | `eco` | green |

- Top row: tone-coloured emoji icon + small `dateRange` text.
- Title (medium weight) + 3-line-clamped description.
- Footer badges: `audienceTag` (purple) + one-or-more `channelTag` chips (cyan).
- Hover overlay: white semi-transparent backdrop with a single **Create** button.
- While a card is being created, the entire grid is `pointer-events-none` and the active card shows *"Creating campaign…"* text above its button.

## Business rules

### Create flow from a suggestion

1. Calls `POST /admin/api/core/marketing/campaigns/create-from-suggestion` with `{title, description, type, channel, exampleTitle, exampleBody, segment}`.
2. On success: navigates to `campaigns-edit/{type}/{newId}` — the new campaign is a Draft pre-filled with the suggestion's title, description, channel, and an example message body.
3. On error: per-card loading state clears; toast surfaces the error.

### Polling while AI job is computing

The AI suggestions query auto-refetches every 10 seconds while `data.fallback === true` (i.e., the background AI job is still computing). Once real data arrives, polling stops. (verify exact poll interval against current code.)

### Plan-feature modal on locked suggestions

When a suggestion requires a feature the merchant's plan doesn't include, clicking **Create** opens a **PlanFeature** modal (`type="plan_feature"`) instead of creating — the merchant must upgrade their plan first. The campaign-create POST does **not** fire in this case.

### Quota still applies

Suggestion-driven creates pass through the same plan-tier quota check as the regular **+ Create campaign** path — see [[campaigns-list-rules]].

## Related

- [[marketing-campaigns]] — hub.
- [[campaigns-list-create-modal]] — sibling create surface (manual + predefined paths).
- [[campaigns-list-rules]] — plan-feature gating + quota enforcement that applies to AI-suggested creates too.
- [[plan-gates]] — plan-feature keys that can lock a suggestion.

## Open questions

- Exact poll interval for the `fallback: true` re-fetch loop — currently documented as 10 seconds based on a UI observation. (verify)
- Whether the `useSeasonalSuggestions` composable localises tab labels or always uses English. (verify)
