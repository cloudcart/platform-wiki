---
type: feature
nav_path: "Apps → Video Slider Module"
route_name: apps.video_slider_widget.overview
route_path: /admin/apps/video_slider_widget
aliases: ["Video Slider", "Video Slider Module", "Video carousel", "Video block", "enable disable button", "app active toggle"]
tags: [apps, marketing, content, landing-pages, plan-gated]
plan_gates: ["video_slider_widget"]
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# Video Slider Module

## Purpose

**Video Slider Module** — a landing-page module that displays a slider/carousel of videos (typically product demos, customer testimonials, marketing reels). When the module is enabled and the merchant adds it via the **Marketing → Pages** page builder, the storefront renders a video carousel that customers can browse / play inline.

Used by merchants who:
- Sell products that benefit from video demonstrations (fashion, cosmetics, electronics).
- Want to showcase customer testimonials on the homepage.
- Embed Instagram-Reels-style content on the storefront.

The app is **plan-gated** — paid feature.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so it can be switched off without uninstalling it. A disabled app stops working while keeping its settings.

## Where to find it

Sidebar → Apps → install → **Video Slider Module**. Two sub-pages:

| Sub-page | Route name |
|----------|------------|
| Overview | `apps.video_slider_widget.overview` |
| Settings | `apps.video_slider_widget.settings` |

## What the merchant can do here

### Settings tab

The settings page is a STATUS / GUIDANCE page (not configuration):

- **Active status indicator** — large icon + heading: "Video Slider app is active" (play icon, purple) OR "Video Slider app is not active" (pause icon, gray).
- **Guidance text**:
  - When ACTIVE: *"You can now add and configure the Video Slider module from any landing page in the page builder."* + link to `/admin/marketing/pages`.
  - When INACTIVE: *"Activate the app from the Overview tab to enable the Video Slider module across your landing pages."*
- **Action button**:
  - When ACTIVE: "Open landing pages" → routes to page builder.
  - When INACTIVE: "Enable Module" — activates from settings.
- **How to use the module** — instructional card explaining the workflow.

### Overview tab
Install / activate / deactivate. App description.

### Page builder integration
After activation, the merchant goes to **Marketing → Pages**, picks a landing page (or creates one), and **adds the Video Slider module block** from the page builder. The module block is configured INSIDE the page builder, not on this Settings page — fields like video URLs, autoplay, transition speed, etc.

### What the merchant CANNOT do here
- Configure individual videos / playlists on the app's Settings page — that's the page builder's job.
- Use without the corresponding plan feature (paid).

## Settings & fields

Per Manager:
- `getMigrationsPath` — DB migrations for the app's tables.
- `appInfo` — App Store metadata.
- `PLAN_FEATURE_MAPPING = 'video_slider_widget'` — paid feature key for plan-gating.

## Business rules

### Activation enables module BLOCK; page-builder configures per-page

This is a two-step model:
1. **App activation** = module block becomes AVAILABLE in the page builder.
2. **Per-page configuration** = the merchant ADDS the module block to specific landing pages and configures its content.

Each page can have its own video slider with different videos. So the merchant could run one slider on the homepage (brand testimonials) AND a different slider on a specific category (product demos).

### Plan-gated

The module requires a paid plan-feature subscription (`video_slider_widget`). Without it, the app may install but the module block in the page builder is locked / shows an upgrade prompt.

### Permission

Standard apps permission scope.

## How it works (verified against backend)

### What the module renders
From the app description: *"Display autoplaying videos with overlay text and call-to-action buttons in fully customizable slides."* Each slide carries:
- A video (which plays on the storefront).
- Overlay text (heading / sub-text positioned on top of the video).
- A call-to-action button (links to a product, category, page, or external URL).

The slides cycle as a carousel that customers can browse / play inline.

### Auto-install after subscription
When the merchant purchases the `video_slider_widget` plan feature pack, the app is **automatically installed and activated** by the platform's `postSubscription` hook — the merchant does not need to manually install after paying. The module block then becomes available in the storefront editor.

### Per-page configuration in the storefront editor
The Settings tab of the app itself only acts as a status / guidance page. Actual module setup happens in **Marketing → Pages** (the storefront editor) — the merchant adds a Video Slider module block to a specific page and configures the videos, overlays, and CTAs there. Each page can carry its own slider with different videos.

### Storefront editor link from Settings
- When the app is **active**, the Settings tab shows *"You can now add and configure the Video Slider module from any landing page in the page builder"* and an **Open landing pages** button that takes the merchant directly to `/admin/marketing/pages`.
- When the app is **inactive**, the Settings tab shows *"Activate the app from the Overview tab to enable the Video Slider module across your landing pages"* and an **Enable Module** button.

### `isConfigured` always returns true
The Manager's `isConfigured` returns `true` unconditionally — there are no required settings for the app itself. The module block becomes available the moment the app is active; configuration happens per-page in the page builder, not in the app's settings.

### postSubscription hook auto-installs + auto-activates
The Manager implements `MoreRecordsSubscription` — after the merchant purchases the `video_slider_widget` plan-feature pack, the platform calls `postSubscription` which checks if the app is already installed, installs it if needed, and immediately sets `active = 1`. So merchants paying for the plan feature don't need to manually install / activate from the App Store — the module is ready to use.

### No migrations table
`getMigrationsPath` returns `null` — the app does NOT create its own database tables. All module configuration lives inside the Pages module's existing storage (the page builder's content blocks JSON), keyed by page ID.

## Related

- [[apps]] — App Store.
- [[plan-gates]] — concept page on plan-based feature gating.

## Open questions

_None — all questions answered above._
