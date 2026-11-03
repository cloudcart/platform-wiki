---
type: feature
nav_path: "Apps → Image Health"
route_name: apps.image_health.overview
route_path: /admin/apps/image_health
aliases: ["Image Health", "Image Health app", "image_health", "Product image checker", "Image quality check", "Image score", "Google image requirements", "Meta image requirements", "Здраве на снимките", "Проверка на снимките", "Качество на снимките", "Оценка на снимките", "Снимки отхвърлени от Google"]
tags: [apps, products, images, ai, google-shopping, meta, credits]
plan_gates: ["image_health"]
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

# Image Health

> **No on/off control.** Installed is on, uninstalled is off. The app works inside the admin, and the storefront changes only when the merchant applies a fix to an image.

## Purpose

**Image Health** (Bulgarian **Здраве на снимките**) *"Checks every product image for quality and Google / Meta compliance, scores the catalog and tells you what to fix first."* One scan gives the store a score out of 100, lists the products whose images cost sales or get them rejected, and offers fixes the merchant approves.

## Where to find it

Sidebar → **Apps → Image Health**. Permission `apps`.

| Tab | Path | Route name |
|---|---|---|
| Overview | `/admin/apps/image_health` | `apps.image_health.overview` |
| **Health score** (the dashboard) | `/admin/apps/image_health/settings` | `apps.image_health.settings` |
| **Issues** | `/admin/apps/image_health/issues` | `apps.image_health.issues` |
| **Settings** | `/admin/apps/image_health/configuration` | `apps.image_health.configuration` |

The address of **Health score** ends in `settings`; the settings themselves are on the tab called **Settings**.

## Sub-pages (in this cluster)

- [[apps-image-health-checks]] — every check, its severity and rule, and the settings that switch them.
- [[apps-image-health-score]] — how the image, product and store scores are worked out; dismissing a problem.
- [[apps-image-health-credits]] — what a credit buys, the free 50, the packs, what locks without credits.
- [[apps-image-health-fixes]] — alt text, colour match, a better main image, white margins, JPEG conversion.

## What the merchant can do here

- Run **Scan catalog** / **Stop scan** on the Health score tab.
- Read the score, **Products by most serious problem** and **Most common problems**, both linking to the filtered Issues tab.
- Work through **Issues**: filter, open a product, dismiss a problem, apply a fix, or go to **Edit product** ([[products-editor]]).
- Buy or change a credit pack from the **Image credits** card.
- Set which checks run on the **Settings** tab.

## Settings & fields

All on the **Settings** tab, in the **Checks** box, listed on [[apps-image-health-checks]]. *"Changes apply from the next scan."*

## Business rules

### Plan and price

Free to install on any plan. Checks are metered in credits, plan feature `image_health`, with 50 free every month ([[apps-image-health-credits]]).

### A scan

- Walks products that are active and not draft.
- Two passes: technical over products (*"Scanning {processed} of {total} products…"*), then AI over images (*"AI check: {processed} of {total} images…"*), best sellers' main images first.
- One scan at a time: *"A scan is already running."* / *"Вече тече сканиране."*
- **Stop scan** during the AI pass still ends with a score, and images not reached wait for the next scan. During the technical pass it cancels the scan.
- A failed scan shows: *"The last scan did not finish. Start it again."*
- It runs in the background, so the merchant can leave the page. A large store takes a few minutes.

### Automatic re-check

With **Check new and changed images automatically** on, adding, replacing or deleting an image, changing its name, size or order, or linking it to a variant marks the product. About 10 minutes after the first change, one background refresh re-runs the technical checks for marked products only, then the AI for their new images while credits last. What is left waits for the next scan or refresh. A refresh waits while a full scan runs.

### Uninstalling

Nothing is deleted. Credits, results, dismissed problems, proposals and settings all come back on a reinstall. A running scan is closed as cancelled. A paid pack is deactivated, and the details trim to the free allowance ([[apps-image-health-credits]]).

## Related

- [[apps]] — App Store.
- [[products-editor]] — where images are replaced.
- [[apps-google-shopping]] — the source of the problems Google itself reports.
- [[plan-vs-feature-pack]] — plan features and feature packs.

## Open questions

- None.
