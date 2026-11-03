---
type: feature
nav_path: "Apps → Deprecated"
route_name: apps.deprecated
route_path: /admin/apps/deprecated/:name
aliases: ["Deprecated apps", "Old apps", "Retired apps", "Apps deprecated"]
tags: [apps, deprecated]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# Apps → Deprecated

## Purpose

The **Deprecated apps** view surfaces apps that are no longer in active maintenance. A merchant who previously installed one of these apps can still access its existing data + configuration here (historical orders, settings, etc. remain visible) but should NOT install new ones — they've been replaced by modern alternatives OR retired entirely.

Used when:
- The merchant clicks an old App Store link that points at a deprecated app.
- The merchant navigates from a search result that returns a deprecated app.
- The merchant has historical data tied to a deprecated app and needs to view / extract it.

The `:name` URL parameter identifies which specific deprecated app's view to render.

## Where to find it

The route `/admin/apps/deprecated/:name` is reached via direct navigation OR via the App Store catalog when filtered to show deprecated entries (verify whether the catalog has a "show deprecated" toggle).

Route name: `apps.deprecated`. The view renders the standard `AppOverview` component with a deprecation banner / disabled install controls.

## What the merchant can do here

- **Read** the deprecated app's documentation (description, original purpose).
- **Access** historical data if the app was previously installed (settings, logs, configurations).
- **Migrate** — follow the suggested migration path to the modern replacement (typically linked in the deprecation notice).
- **Cannot install** — the install button is disabled / hidden.

### Current deprecated apps in the wiki

| Deprecated app | Recommended replacement |
|---|---|
| [[apps-drop-shipping]] | [[apps-suppliers]] + [[apps-xml-sync]] + [[apps-frisbo]] |
| [[apps-rapido]] | Regional active courier integrations (per market) |
| [[apps-berry]] | Regional active courier integrations (per market) |

### What the merchant CANNOT do here
- Install a deprecated app (install controls disabled).
- Reactivate an uninstalled deprecated app (recovery requires support).
- Receive bug fixes or new features for deprecated apps.

## Settings & fields

The view renders the standard `AppOverview` component but with the install action disabled and a deprecation banner explaining the recommended replacement.

## Business rules

### Read-only state

Deprecated apps preserve their historical data — orders, settings, logs are all readable. But they cannot be **changed** or **reinstalled**. The merchant's view is essentially read-only.

### Migration path documentation

Each deprecated app's wiki page documents the modern replacement. The merchant can click through to the new app, install it, and follow any migration steps.

### Support SLA

Deprecated apps have NO active support — issues are not investigated, bugs are not fixed, security patches are not applied. The platform may eventually delete the data entirely (verify retention policy).

### Permission
Standard apps permission scope.

## How it works (verified against backend)

### Page layout (per `Deprecated.vue`)

The deprecated-app view renders a centred panel:

| Section | Content |
|---|---|
| **App name (h3)** | The original app's display name. |
| **Category** | `Category: <app.category.name>` in purple — when the app belongs to a category. |
| **DEPRECATED badge** | Red pill in uppercase. |
| **"This app is no longer available."** (h5) | Headline message. |
| **Long-form note** | *"For more information or if you have any questions, please do not hesitate to contact our team. We will find the best solution for your business."* |
| **App icon** | Right-column rounded image with reduced opacity to signal "retired" state. |
| **Similar Apps swiper** | A `AppSwipe` row at the bottom labelled "Similar Apps" listing apps from the **same category** (excluding the current one), fetched via `GET /admin/api/core/applications`. Each card is clickable and routes to that app's overview/install. |

The "Contact us" button is present in the code but commented out — there is currently NO direct CTA on this page. The merchant is expected to use the global support module or the cards in the Similar Apps swiper.

### Catalog visibility
Deprecated apps are surfaced through the dedicated `/admin/apps/deprecated/:name` route, not the main App Store catalog. The standard App Store filters its results to active apps only, so merchants generally reach deprecated entries through old direct links, search results, or by navigating from their existing app data when a previously-installed app has been retired.

### Data retention
Deprecated apps preserve their historical data — orders, settings, logs are all readable. The merchant's view becomes effectively **read-only**: nothing can be changed, no new install can be performed, no reinstall is possible without support. The merchant can extract historical data from order records or analytics, but should NOT rely on these apps for live operations.

### Communication when an app is retired
When CloudCart retires an app that has active merchant users, the merchant typically learns through:
- A deprecation banner on the app's settings page directing them to the modern replacement.
- The "Recommended replacement" entry in this hub.

### Migration path documentation
Each deprecated app's wiki page documents the modern replacement to migrate to:
- **Drop Shipping** → [[apps-suppliers]] + [[apps-xml-sync]] + [[apps-frisbo]].
- **Rapido** / **Berry** → regional active courier integrations per market.

## Related

- [[apps]] — App Store hub.
- [[apps-drop-shipping]] — deprecated.
- [[apps-rapido]] — deprecated.
- [[apps-berry]] — deprecated.
- [[apps-json-import]] — internal-only (distinct from deprecated).

## Open questions

_None — all questions answered above._
