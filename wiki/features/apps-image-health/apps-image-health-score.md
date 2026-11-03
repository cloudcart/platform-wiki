---
type: feature
nav_path: "Apps → Image Health → Health score"
route_name: apps.image_health.settings
route_path: /admin/apps/image_health/settings
aliases: ["Image Health score", "Health score", "Store image score", "Why did my image score change", "Dismiss image problem", "Оценка на снимките", "Как се смята оценката на снимките", "Скрий проблем със снимка"]
tags: [apps, products, images, score]
plan_gates: ["image_health"]
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

> Part of [[apps-image-health]]. See the hub for scans, the automatic re-check and uninstalling.

# Image Health — the score

## Purpose

How the number on the **Health score** tab is worked out, from one image to the whole store, and what moves it.

## Where to find it

**Apps → Image Health → Health score** (`/admin/apps/image_health/settings`), the **Image Health score** card. Each product's and image's score is on the **Issues** tab.

## What the merchant can do here

- Read the store score as `{score} / 100`, with *"{count} products scanned, {clean} without problems"* and *"Last scan: {date}"*.
- Read **Products by most serious problem** and **Most common problems** (top 5), both linking to the filtered Issues tab.
- Dismiss a problem that does not apply, or restore it, in the product's side panel.

Before the first scan the card says: *"Scan your catalog to see how healthy your product images are."*

## Settings & fields

No fields of its own. **Channels you sell on**, **Images a product should have** and **Checks to skip** ([[apps-image-health-checks]]) decide which problems exist to count.

## Business rules

### Penalties

| Severity | Penalty |
|---|---|
| Critical | 40 |
| High | 20 |
| Medium | 10 |
| Low | 3 |

### From image to store

| Level | How it is worked out |
|---|---|
| **Image** | 100 minus the penalties of its open problems, floor 0. |
| **Product** | Half the main image plus half the average of the others (all of it the main image when it is the only one), minus product-level penalties, floor 0. A product with no image scores 0. |
| **Store** | The average of the products, weighted by `1 + ln(1 + revenue)`. |

Revenue is the last 90 days, from paid and completed orders. The weighting lets a best seller's images count for more than a product nobody buys, without one product swamping the rest.

### The score always covers the whole catalog

The store score, the counts per severity and the most common problems are free, whatever the credits cover. They show how big the problem is before anything is paid for. An image's own score, problems and recommendations need a credit: [[apps-image-health-credits]].

### What moves the score

- **Dismissing a problem** changes the score at once, with no new scan. Restoring it does the same in reverse. Dismissed, a missing-image problem no longer holds the product at 0.
- **Replacing images on the product page** changes it after the next scan, or after the automatic re-check ([[apps-image-health]]).
- **Changing the settings** changes it from the next scan.
- **Applying a fix** re-checks the image ([[apps-image-health-fixes]]).

## Related

- [[apps-image-health]] — hub.
- [[apps-image-health-checks]] — what each problem is and its severity.
- [[apps-image-health-credits]] — what is free and what is locked.

## Open questions

None.
