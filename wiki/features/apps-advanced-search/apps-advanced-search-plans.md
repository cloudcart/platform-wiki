---
type: feature
nav_path: "Apps → Aura Search → Settings → Plan & usage"
route_name: apps.advanced_search.settings
route_path: /admin/apps/advanced_search/settings?section=plan
aliases: ["Aura Search plans", "Aura Search price", "Advanced Search plan", "search quota", "monthly searches", "extra searches", "buy more searches", "Starter Growth Pro", "search limit reached", "switched to basic search", "Aura Search пакети", "лимит търсения", "месечни търсения", "допълнителни търсения", "премина към базово търсене"]
tags: [apps, search, billing, plans, quota]
plan_gates: ["advanced_search", "advanced_search_packs"]
created: 2026-09-23
updated: 2026-09-23
source_count: 6
---

# Aura Search — plans, the search quota, and running out

> Part of [[apps-advanced-search]]. See the hub for the other aspects (overview, searches, pins, vocabulary, AI, settings, indexing).

## Purpose

Aura Search is paid by the month and **metered**: each plan includes a number of storefront searches, and extra packs can be added on top. This aspect covers the plans, what counts as one search, and what the storefront does when the month's searches are used up.

## Where to find it

**Apps → Aura Search → Settings → Plan & usage** (`/admin/apps/advanced_search/settings?section=plan`). The same figures appear in the Settings tab's right-hand **Plan & usage** panel. Without a plan, a yellow notice with **Activate — choose a plan** also sits at the top of the Overview tab.

## What the merchant can do here

- **Activate** the app by choosing a plan (**Activate — choose a plan**).
- **Change plan** — move between Starter, Growth and Pro.
- **Buy more searches** — add extra monthly packs on top of the plan.
- Read **Plan**, **Additional packs**, **Total**, **Used** and **Left** for the current month.

## Settings & fields

### The three plans (pick one)

| Plan | Searches per month | Price per month |
|---|---|---|
| **Starter** | 5 000 | €9 |
| **Growth** | 15 000 | €19 |
| **Pro** | 40 000 | €39 |

Buying a plan **replaces** the one held before. There is no free plan.

### Extra search packs (stack)

| Pack | Price per month |
|---|---|
| 10 000 additional searches | €11 |
| 20 000 additional searches | €20 |
| 50 000 additional searches | €51 |
| 100 000 additional searches | €100 |
| 500 000 additional searches | €420 |
| 1 000 000 additional searches | €790 |

Packs **add up**: two 10 000 packs are 20 000 extra, and they stack on whichever plan is active. The panel lists each pack held with its count (e.g. *10 000 additional searches ×2 = +20 000*). These are the prices the purchase panel was set up with; the panel itself shows the price that applies at the moment of buying.

**Total** = the plan's searches + every pack. **Left** = Total − Used, never below zero. The count **resets at the start of each month**. Nothing carries over: the quota is a monthly allowance, not a balance, so searches left unused at the end of a month are not added to the next.

## Business rules

### 🔴 Enabling needs a plan; installing does not

Install, open and explore the app for free. Switching it **on** without a plan is refused and opens the plan picker instead; the Enable control itself is only shown once a plan is active. When the paid model was introduced, stores that had the app enabled but no plan were switched off, so a store that "used to have Advanced Search" and now shows it off simply has no plan yet.

Without an active app the storefront uses the **basic store search**.

### What counts as one search

A search is one request from the **instant results dropdown** under the storefront search box:

- It fires after **2 characters**, once the shopper pauses typing for **0.3 seconds**.
- A shopper who types a word slowly, pausing twice, spends **two** searches; typing it in one go spends one. Re-sending the same text does not count again.
- Requests from **bots and crawlers count too**. The meter is everything that reaches the dropdown, not only people.

**Not counted:** the full **`/search` results page**, a shopper pressing Enter to reach it, testing a search from the admin, and click reports. The Used figure is split in the panel into **Advanced Search** and **Advanced AI Semantic Search** requests, which together make up **Used**.

This is why a busy store can use a plan faster than its order count suggests. A search box used by many visitors, or hit by crawlers, is spending on every keystroke pause. [[apps-advanced-search-usage]] explains why this figure is larger than the **Searches** number on the Overview tab.

### 🔴 Running out downgrades the dropdown, not the app

When Used reaches Total:

- The **dropdown** falls back to keyword matching: **AI semantic search is left out of it**, and its requests stop being counted against the plan. Its other settings still apply — searched fields and weights, "all words must match", synonyms, pins.
- The app **stays enabled**. Nothing is switched off and no setting is lost.
- **Pinned products, synonyms and the full `/search` results page carry on** as before. The full page was never metered, so running out does not touch it.
- An admin alert is written, **once per month**: *"The Advanced Search monthly search limit (…) has been reached. Your storefront has switched to basic search. Buy more searches or wait for the next billing cycle to restore advanced search."*

The check is refreshed every few minutes, so buying a pack restores the full dropdown within about five minutes, not instantly. The start of the next month restores it on its own.

### A plan is a store subscription, not a one-off

Plans and packs renew monthly like any other paid service on the store; they are managed through the store's plan and billing ([[plan-gates]]).

## Related

- [[apps-advanced-search]] — hub.
- [[apps-advanced-search-usage]] — the three different "search" counts and why they differ.
- [[apps-advanced-search-settings]] — the Settings tab the plan panel sits in.
- [[plan-gates]] — how paid plan features and packs work.

## Open questions

(None currently outstanding for this page.)
