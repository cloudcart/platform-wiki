---
type: feature
nav_path: "Plan → Apps"
route_name: plan-apps
route_path: /admin/plan-apps
aliases: ["Plan apps", "Paid apps", "Apps catalog (plan)", "Apps tab", "Платени приложения", "Приложения за план"]
tags: [plans, plan-apps, apps, subscription-billing]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---
# Plan Apps

## Purpose

The **Apps** tab inside the Plan area is a search-enabled grid of every PAID CloudCart app the merchant can install. It is a curated subset of the full [[apps]] marketplace — filtered to *paid only*, so each card represents a subscription the merchant is billed for monthly / yearly. From here the merchant browses, searches by name / description, clicks into an app's overview / settings, or follows a link to cancel an already-installed paid app.

It sits alongside [[plans]], [[plan-features]], and [[plan-services]] as one of the four tabs in the Plan section; the same panel chrome (back button to dashboard, tab bar) wraps all four.

## Where to find it

- **Plan → Apps** tab in the Plan area's top-level tab bar (visible on `/admin/plans`, `/admin/plan-apps`, `/admin/plan-features`, `/admin/plan-services`).
- The Plan sidebar entry (owner-only) lands the merchant in this area; they click the **Apps** tab.

URL pattern: `/admin/plan-apps`.

## What the merchant can do here

### Browse paid apps in card form

Each app is rendered as a card showing its icon, localised name, short description (clipped with a *Show more* / *Show less* link when it overflows the card height), and an action button. The grid is ordered *recommended* first (alphabetical within the recommended group), then alphabetical for the rest.

### Search across the catalog

A search box at the top filters the visible cards by app name and description. The filter is purely client-side over the already-loaded list — no server round-trip per keystroke, case-insensitive substring across both fields. A **No results** placeholder shows when the filter yields zero matches (or when there are no paid apps for the merchant's country / catalog).

### Get / install a paid app

If the app is NOT installed, the card shows a **Get app** button linking to the app's overview page (`apps.{key}.overview`) — or its settings page (`apps.{key}.settings`) if no overview route is defined. From there the merchant goes through that app's standard install / trial / purchase flow. Apps that require a separate request use `/admin/apps/request/{key}` instead — the same flow as on the main [[apps]] marketplace.

### Cancel an installed paid app

If the app IS installed AND paid, the card shows a **Cancel** button (red ban icon) that links to [[subscriptions]] pre-filtered to that app's subscription. The merchant cancels from the subscriptions list — there is no inline uninstall / cancel action on this screen.

## What the merchant cannot do here

- **Install a free app** — the list is paid-only; free and ecosystem apps live on the main [[apps]] marketplace.
- **Filter installed vs uninstalled** — no such tab; the merchant scrolls / searches the unified list. The only distinction is the button label.
- **Cancel from this screen** — the Cancel button is a *link* to [[subscriptions]], not an inline action.
- **Install an app from a disallowed country** — apps whose country-limit filters exclude the merchant's invoicing / operation country are not shown.
- **See deprecated apps** — apps with `depricated_at` set are filtered out (unless already installed).

## Settings & fields

This is a browse / search screen — no editable fields. Per card the merchant sees:

| Field shown | What it represents |
|-------------|--------------------|
| **Icon** | App icon (small image) |
| **Name** | Localised app name |
| **Description** | Short description (or full description if short isn't set), truncated with *Show more* / *Show less* when it overflows |
| **Get app** button | Visible only when the app is NOT installed; routes to the app's overview / settings or request page |
| **Cancel** button | Visible only when the app IS installed and IS paid; routes to [[subscriptions]] filtered to that app's mapping |
| **Pricing** (text, when not installed) | Monthly or yearly price as published by CloudCart (e.g. *9.00 EUR / month*) |

## Business rules

### Paid-only filter

The catalog request passes `paid=1`, so only apps with a price are returned (the `is_paid` flag is true) — even installed free apps don't appear. To see / install / configure free apps, the merchant uses the standard [[apps]] catalog.

### Country / locale and deprecation filtering (server-side)

Before the cards render, the backend removes:
- Apps in dev mode (unless the environment is in development).
- Apps with a `depricated_at` value (deprecated).
- Apps whose country / operation-country limits exclude the merchant.

Already-installed apps stay visible regardless of these filters, so the merchant can still cancel an app they had before its retirement. Because country filtering is server-side, the client search box can never surface a paid app outside the merchant's country.

### Installed-app state is shared across screens

The **Installed** badge / button state on each card is computed from the merchant's installed-apps cache (active site-app records). The same cache backs the Plan area and the main [[apps]] marketplace, so installing an app on one screen is reflected on the others without a manual refresh.

### Get app button respects request-app and route presence

The *Get app* link is resolved per app:
1. If `request_app = 1` → `/admin/apps/request/{key}`.
2. Else prefer `apps.{key}.overview` (when registered and the app isn't installed); otherwise `apps.{key}.settings`.
3. If neither route exists, the button renders but stays inert.

For XML-feed apps (keys starting with `app.xml_feed.`), the route key uses the last segment only (e.g. `app.xml_feed.google` → `google`).

### Cancel routes to subscriptions, not to the app's settings

The **Cancel** action does NOT open an in-screen modal — it routes to [[subscriptions]] using the `subscriptions-list` route with a pre-applied `filters[mapping][]` filter for the app's key. The subscriptions list shows only that app's subscription, where the merchant runs the standard cancel flow (cancellation takes effect at the next billing date; existing app data is preserved per the subscription's cancellation rules). See [[subscriptions]].

### No trial flow on this screen

Even though many paid apps support trial periods (`trial_days > 0`), the trial decision happens on the destination app overview / settings page, not on this card grid. The merchant clicks *Get app*, lands on the app's own page, and chooses *Start trial* there. See [[apps]].

### Description fallback

Each card shows the short description when set, falling back to the full description. The fallback is purely cosmetic — only one of the two strings is ever shown, with *Show more* applied if it overflows.

## Related

- [[apps]] — the main marketplace catalog (free + paid + ecosystem); the plan-apps tab is a filtered subset.
- [[plans]] — pick-a-plan catalog.
- [[plan-features]] — buy additional quota on individual features.
- [[plan-services]] — recommended services tab.
- [[subscriptions]] — list of all CloudCart subscriptions; this is where Cancel takes the merchant.
- [[plan-gates]] — how plan-tier features gate visibility (some plans may restrict which apps appear).
- [[billing-cards]] — saved card that pays for app subscriptions.
- [[merchant-subscription-lifecycle]] — merchant-question hub: "how do I buy a paid app / what happens if I cancel an app subscription?".

## Open questions

(All resolved.)
