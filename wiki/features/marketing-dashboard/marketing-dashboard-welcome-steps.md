---
type: feature
nav_path: "Marketing → Dashboard → Welcome & setup steps"
route_name: marketing-dashboard
route_path: /admin/marketing-new/dashboard
aliases: ["Marketing setup checklist", "5-step setup", "Welcome card", "Marketing onboarding steps", "Setup Complete badge", "Стъпки за настройка", "Маркетинг приветствие"]
tags: [marketing, dashboard, onboarding, setup, checklist]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-dashboard]]. See the hub for the other aspects (overview KPIs, channel performance, quick-launch tiles, campaigns & products, RFM & discounts, data freshness).

# Dashboard — Welcome & setup steps

## Purpose

The **Welcome / Steps row** is the first thing the merchant sees at the top of the Marketing Suite. It welcomes new merchants with a help video, orients them with an explanatory paragraph, and walks them through the **5-step setup checklist** that wires up the third-party integrations the rest of the dashboard depends on (Google Analytics, Google Ads, Search Console, the messaging Channels, Facebook Pixel). Once all 5 steps are ticked, the row collapses to a compact greeting card — the checklist disappears so it doesn't take up dashboard real-estate forever.

## Where to find it

Sidebar → **Marketing** → **Marketing suite** — top row of the dashboard.

## What the merchant can do here

- **Watch the welcome video** — embedded YouTube help video (`https://www.youtube-nocookie.com/embed/OMblbmqJJdQ` — modest-branding mode, no-cookie variant) on the left of the welcome card.
- **Open the help centre** — a **Help center** ghost button in the welcome card links to `https://help.cloudcart.com/bg/support/solutions/77000208335`.
- **Tick a single setup step as complete** — clicking the green-bordered circular checkbox on a pending step opens an inline confirm popover labelled *"Mark task as complete?"* with a primary **Complete** button.
- **Jump to a step's target route** — clicking a pending step's label OR the arrow-right icon on the right edge of the row navigates into that step's settings screen.
- **Mark all 5 steps complete at once** — a **Mark all complete** ghost button at the bottom of the card bulk-flips every step to `true` via a single request. A spinner replaces the icon while the request is in flight.
- **Recognise completed steps at a glance** — completed steps show a filled green circle (`#25CF8B`) with a white checkmark plus a green **Setup Complete** badge; their labels become plain text (no longer clickable).

## Settings & fields

### The 5-step setup checklist

| Key | Step | Target route |
|-----|------|--------------|
| `google_analytics` | Google Analytics | `apps.google_analytics.settings` |
| `google_adds` | Google Ads | `apps.google_dynamic.settings` |
| `google_search_console` | Google Search Console | `/admin/apps/google_search_console/settings` (legacy path) |
| `channels` | MC Channels (SMS, Viber, Email, Webpush) | `campaigns-channels` |
| `facebook_pixel` | Facebook Pixel | `apps.facebook.settings` |

Each step is a boolean. The status set is persisted server-side via `POST /admin/api/core/marketing/steps-statuses-update` and read via `GET /steps-statuses`.

### Layout modes

The welcome card has two layout modes driven by checklist completion:

- **Pre-completion** — full-width left tile (`min-h-[215px]`) with the video on the left and a side column carrying the heading, an explanatory paragraph (*"Grow your online business with a full suite of solutions for building high converting Upsales and Cross sales, Customer reviews, Email, Webpush, Viber and SMS marketing automations."*), and the **Help center** ghost button. The checklist card sits to the right (7/12 column).
- **Post-completion** — when `Object.values(steps).every(v => v)` is true, the checklist row vanishes and the welcome card collapses to a compact `min-w-[240px] cc:h-[135px]` greeting. Only the welcome card remains.

### Progress bar

The checklist card carries a `CcProgressBar` (variant=success) showing **{completed} of {total} completed** progress at the top of the card.

## Business rules

### The checklist is a guide, not a gate

The merchant can use **Mark all complete** to declare the setup done **without actually configuring those steps**. The server only stores a boolean per step; there is no validation that the underlying app is actually installed or configured. This is intentional — the checklist is a *guide*, not a gate. The rest of the dashboard works regardless of checklist state.

### Local mirror prevents the video from re-flashing

Completing the checklist also writes `marketing_steps_completed=true` to the browser's `localStorage`. This ensures that when the merchant refreshes the page on a slow connection, the dashboard doesn't briefly flash the full welcome video before the server's `/steps-statuses` response arrives. The localStorage flag is a UX optimisation — the server-side state is the source of truth.

### Per-step click → confirm popover, not a direct toggle

Clicking the pending checkbox does NOT mark the step done immediately. It opens an inline confirm popover (CcDeleteComponent-styled) reading *"Mark task as complete?"* with a primary **Complete** button. The merchant must explicitly confirm. This prevents accidental clicks while scrolling from declaring setup done.

### Pending labels link, completed labels don't

A pending step's label is a clickable link that navigates to the step's target route (so the merchant can go finish the integration). Once the step is complete, the label becomes plain text — there is no longer a reason to "go set it up". This means a merchant cannot use the checklist as a quick-navigator to revisit the integration settings; for that they use the sidebar.

### Persistence is per-store, not per-administrator

The checklist boolean set is stored per **site**, not per admin user. If two administrators share the store, both see the same completion state. There is no per-user "dismiss" of the welcome card.

## How it works

The row reads the checklist state from `GET /admin/api/core/marketing/steps-statuses` on dashboard mount. Per-step click writes a single-key update to `POST /admin/api/core/marketing/steps-statuses-update`. The **Mark all complete** action sends one request with all five keys set to `true` (verify). The setup-checklist data lives in the campaigns app's settings — not in a dedicated table.

The checklist values are **not** consumed by any other module on the dashboard — they don't gate visibility, don't drive metrics, and don't influence the data-freshness collector. They exist purely to nudge the merchant through onboarding.

## Recommended merchant use

- **Day 1 — new store** — work through every step in order; clicking the label takes the merchant straight into the integration's settings page.
- **Returning merchant who finished setup elsewhere** — use **Mark all complete** to clear the checklist and collapse the row.
- **Re-onboarding after a channel disconnect** — there is no "untick" affordance, so a merchant who disconnects Google Analytics will still see the step as complete. To re-walk the merchant through it, support points them to the sidebar app pages directly.

## Related

- [[marketing-dashboard]] — hub.
- [[marketing-channels]] — Channels page; target of the MC Channels step.
- [[apps-google-analytics]] — Google Analytics integration; target of step 1.
- [[apps-google-dynamic]] — Google Ads integration; target of step 2.
- [[apps-facebook-pixel]] — Facebook Pixel integration; target of step 5.

## Open questions

No outstanding questions.
