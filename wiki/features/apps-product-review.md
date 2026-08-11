---
type: feature
nav_path: "Apps → Product Reviews"
route_name: apps.product_review.overview
route_path: /admin/apps/product_review
aliases: ["Product Review", "Product Reviews", "Reviews + Q&A", "Customer reviews", "enable disable button", "app active toggle"]
tags: [apps, others, reviews, qa, moderation]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 6
---
# Product Reviews (CloudCart Reviews)

## Purpose

**Product Reviews** is the integration that adds **customer reviews** AND optionally **Questions & Answers** to the storefront's product detail pages. Customers see star ratings + written reviews from past buyers; they can leave their own (subject to merchant moderation rules) and ask questions that other customers / merchants can answer.

Used by virtually every consumer-facing CloudCart store — reviews are a primary conversion driver (social proof). The app drives both the per-customer review tab seen in [[customers-details-reviews]] AND the storefront product-page reviews module. This page is the hub; the detail lives in the five aspect sub-pages below.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so it can be switched off without uninstalling it. A disabled app stops working while keeping its settings.

## Where to find it

Sidebar → Apps → install → **Product Reviews**.

Four sub-pages in the admin UI:

| Admin sub-page | Route name | Documented in |
|----------------|------------|---------------|
| Overview | `apps.product_review.overview` | this hub |
| Settings | `apps.product_review.settings` | [[apps-product-review-settings]] |
| Reviews | `apps.product_review.reviews` | [[apps-product-review-moderation]] |
| Questions | `apps.product_review.questions` | [[apps-product-review-qa]] |

The Overview is the standard app overview — installation state + key metrics.

## Sub-pages (in this cluster)

- [[apps-product-review-settings]] — the store-wide Settings tab: every field, defaults, conditional UI, `isConfigured` and save-validation rules, `max_days` 1-365 range.
- [[apps-product-review-moderation]] — the three moderation modes, verified-buyer enforcement, anonymous reviews, plan-cap rejection, the Reviews / Questions admin tabs.
- [[apps-product-review-submission]] — the storefront review / reply / question form validation, the post-purchase time window, no photo uploads, reply-requires-email asymmetry.
- [[apps-product-review-qa]] — the opt-in Questions & Answers feature: toggle, question-create field set (no rating), moderation gate.
- [[apps-product-review-internals]] — install-hook segment reactivation + email seeding, per-review / per-question lifecycle hooks, the 11 segment-condition managers, the aggregate-recompute command, no import / export.

## What the merchant can do here

- Configure the store-wide review policy on the Settings tab — see [[apps-product-review-settings]].
- Moderate submitted reviews and questions (Approve / Hide / Delete) — see [[apps-product-review-moderation]].
- Enable the Questions & Answers feature — see [[apps-product-review-qa]].

### What the merchant CANNOT do here

- Edit the review's text — only Approve / Hide / Delete (see [[apps-product-review-moderation]]).
- Configure per-product review settings — settings are store-wide (see [[apps-product-review-settings]]).
- Migrate reviews from another platform automatically — no import path (see [[apps-product-review-internals]]).

## Settings & fields

The full field catalogue lives on [[apps-product-review-settings]]. The four always-required settings (`added_reviews_conditions`, `accept_star`, `order_by`, `max_days`) are what the integration's `isConfigured` checks. Q&A toggles and reply settings are optional refinements.

## Business rules

The detailed business rules are distributed across the aspect pages. The headline rules:

- **Who can review** is store-wide: "All users" or "Only purchased the product" (verified buyer). Verified-buyer eligibility requires a `paid` / `completed` / fulfilled order — see [[apps-product-review-moderation]].
- **Moderation** has three modes: approve-all, threshold auto-approval, or auto-publish — see [[apps-product-review-moderation]].
- **Plan gate** `product_reviews_added_rating` caps how many reviews / questions can be created; over-cap submissions are rejected with a message — see [[apps-product-review-moderation]].
- **Settings are store-wide** — no per-product override; suppress reviews on a specific product at the theme level — see [[apps-product-review-settings]].
- **Reviews are text-only** (no photo / video) and the post-purchase window is bounded by `max_days` (1-365, default 7) — see [[apps-product-review-submission]].
- **Install reactivates dependent segments** and seeds localised "New review added" admin emails — see [[apps-product-review-internals]].

## Related

- [[apps]] — App Store.
- [[customers-details-reviews]] — per-customer review moderation view (depends on this app being active).
- [[products-products]] — products that get reviewed.
- [[marketing-segments]] — segment conditions on review activity (11 condition managers).
- [[settings-admin-notifications]] — "New review added" notification.
- [[apps-yotpot]] — alternative review platform (external).

## Open questions

All previously-flagged questions resolved. See the aspect sub-pages.
