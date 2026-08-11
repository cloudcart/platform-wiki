---
type: feature
nav_path: "Dashboard"
route_name: dashboard
route_path: /admin/
aliases: ["Dashboard", "Home", "Начален екран", "Табло"]
tags: [dashboard, home, onboarding]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 8
---
# Dashboard

## Purpose

The **Dashboard** is the merchant's home screen — the page that loads when they sign in or click the CloudCart logo. It is a stack of independent panels: the **onboarding checklist** (Setup your store — 9 steps), **quick stats** for the day, **headline charts** pulled from [[analytics]], the **Smart daily actions** recommendation widget ([[dashboard-smart-actions]]), and **promotional banners** (current offer, release notes, account-manager card, support card, CloudCart Capital financing, Backup).

The layout adapts to onboarding state:

- **Sandbox / onboarding incomplete** — top half is dominated by the onboarding checklist accordion; bottom half shows Support + Account Manager cards. Charts hidden.
- **Onboarding complete (Live store)** — top half shrinks to a greeting + offer; bottom half shows the full analytics charts + Statistics box + Backup banner.

Once the merchant completes ALL 9 steps, the **Switch to Full Dashboard** button appears; clicking it persists onboarding completion and the layout flips permanently.

## Where to find it

- The default route after login. URL `/admin/` (route `dashboard`).
- The CloudCart logo in the topbar always routes here.

## What the merchant can do here

### See greeting + offer (always)

- **Greeting** — *"Hello, {firstName}!"*.
- **Offer** card — current upgrade offer / promotion; dismissible.

### Walk the onboarding checklist (Sandbox / pre-Live stores)

The **Setup your store** card surfaces a 9-step checklist. Each step is an accordion row with an icon, a title (e.g., *"Add products to your store"*), a status indicator (orange dot if pending, green badge-check if complete), a description, a "Conditions for completing the tasks" bullet list, and a **primary CTA button** that routes to the screen where the step is completed. Skippable steps also show a **Skip this step** link that force-marks the step done; the SSL step shows a warning info-box when no domain is set yet (the merchant needs a domain first).

The 9 steps:

| Step key | Label | Skippable | CTA destination |
|---|---|---|---|
| `products` | Products add | NO | products-list#add-product |
| `payment` | Payment methods | NO | admin.payments#add-payment |
| `shipping` | Shipping methods | NO | admin.shippingProviders#add-shipping |
| `orders` | Orders checklist (3 test orders) | NO | opens storefront in new tab; falls back to /admin/orders |
| `gdpr` | GDPR install + pages | YES | apps.gdpr.settings |
| `domain` | Custom domain | YES | domains.settings#add-domain |
| `ssl` | Install SSL | YES | domains.settings#add-ssl (or #add-domain if no domain yet) |
| `plan` | Plan selection | NO | opens Plan-picker modal |
| `go_live` | Go live | NO | opens `Switching to Live Environment` confirm modal |

A progress bar at the top shows *"{processed} of {total} steps completed"* with a green progress fill.

### Switch to Full Dashboard (after all 9 complete)

When all steps are complete, the **Switch to Full Dashboard** button appears centered above the steps. Clicking it flips the layout to the full-data dashboard (statistics box + charts) and persists the choice. This is **irreversible per-store** — the onboarding checklist is gone for good once dismissed.

### Confirm Go Live (modal)

The `go_live` step opens the **Switching to Live Environment** confirmation modal:

- Body text: *"Please confirm that you want to move to the live environment. Note that this action is irreversible."*
- **Confirm** flips the store from Sandbox to Live and, on success, deletes all sandbox test data.
- On failure, the modal shows an inline error box *"Something went wrong, please try again later"*.
- If the merchant doesn't have an active plan AND the plan step is not done → opens the Plan picker first instead.

### View quick stats (Statistics panel — full dashboard only)

Four clickable counter tiles:

| Tile | Counter source | Click destination |
|---|---|---|
| **New orders** | Orders with `status IN (pending, paid) AND statusfulfillment = not_fulfilled` | filtered orders list |
| **Abandoned orders** | Active abandoned-cart count | `/admin/abandoned` |
| **Out of stock products** | Products with `quantity = 0 AND tracking = 1` | filtered products list |
| **Total customers** | All customers count | `/admin/customers/` |

If the merchant's plan disallows the Statistics panel feature, a yellow upgrade-plan banner is shown instead.

### View headline charts (full dashboard only)

Three live chart panels rendered from the [[analytics-pipeline]]:

- **Total Sales** — line chart.
- **Cart conversion funnel** — funnel chart.
- **Percentage of orders** — bar chart, distribution across statuses.

All three default to the last 30 days. The merchant can't change the range from the dashboard; for fine-grained control they go to [[analytics]].

### See Backup banner

The **Backup banner** advertises the [[backup]] feature when the store is on a plan that supports it but hasn't enabled it yet. Dismissible per session.

### Account-manager + Support cards

- **Account Manager** card — shows the assigned CSM with a **Book a meeting** button (only when the active plan has `csm_meetings: enabled`); a secondary card lists upcoming meetings.
- **Support** card — always shown post-onboarding. Quick links to help center + ticket. A **Support meeting** card appears only when the plan has `support_meetings: enabled`.
- **CloudCart Capital** card — financing offer banner.
- **Release** card — what's new / changelog highlights.

### Go-live trigger (corner overlay)

A persistent floating module in the page corner that triggers the Go-live flow when the merchant is ready — same flow as the `go_live` checklist step.

## Settings & fields

The dashboard itself has no configurable settings — visibility of panels is driven by:

- The store's onboarding state (each step's completion flag).
- The active plan's feature flags (`support_meetings`, `csm_meetings`).
- The sidebar navigation — the dashboard route must be visible; if not, only the greeting is rendered.

## Business rules

### Visibility gate via sidebar navigation + permission

The full dashboard body renders **only when** the dashboard route is visible in the sidebar navigation AND the merchant's role has the **Dashboard** (`dashboard`) permission grant from [[settings-staff]]. Owners always pass; a moderator without it sees only the greeting title. Each dashboard sub-module also calls into another pillar (orders, customers, products, marketing, reports) and re-checks that pillar's own permission — so a moderator with `dashboard` but not `orders` may see an empty Orders tile while another module renders normally.

### Stats counters only render when non-zero

The Statistics panel hides itself entirely when all four counters (new orders, abandoned, out-of-stock, customers) are zero — keeping the dashboard clean for empty / brand-new stores. If just one is non-zero, only those tiles render.

### Plan modal opens from inside the checklist

The Plan step's CTA opens the **Plan-picker modal** — the same modal used everywhere else when the merchant has to choose / upgrade a plan. On successful checkout the plan step is auto-marked complete.

## Related

- [[dashboard-smart-actions]] — the Smart daily actions recommendation widget on this page.
- [[dashboard-insights]] — the Insights (Executive Insights) overview at /admin/insights.
- [[analytics]] — full charts dashboard (the three boxes here are subset).
- [[analytics-pipeline]] — how chart data is computed end-to-end.
- [[account]] — the broader merchant onboarding flow (see also account/store wizard).
- [[products-products]] — destination of the Add Products CTA.
- [[settings-shipping]] — Shipping methods step.
- [[settings-payment-providers]] — Payment methods step.
- [[settings-domains]] — Domain + SSL steps.
- [[apps-gdpr-overview]] — GDPR step.
- [[backup]] — banner CTA.
- [[services]] — CSM / support meetings.

## Open questions

(none — verified against the dashboard, onboarding-progress, and statistics modules.)
