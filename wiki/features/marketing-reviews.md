---
type: feature
nav_path: "Apps → Product Reviews → Reviews"
route_name: apps.product_review.reviews
route_path: /admin/apps/product_review/reviews
aliases: ["Reviews moderation", "Review queue", "Product reviews list", "Reviews list", "Pending reviews", "Модериране на ревюта", "Ревюта", "Списък с ревюта"]
tags: [marketing, apps, reviews, moderation, ratings]
plan_gates: ["product_reviews_added_rating"]
created: 2026-05-23
updated: 2026-06-10
source_count: 9
---
# Reviews (Moderation Queue) — hub

## Purpose

The **Reviews** tab inside the Product Reviews app is the merchant's single inbox for every customer review submitted across all products. From here the merchant approves new reviews (so they appear on the storefront product page), hides reviews that don't meet the store's quality bar, deletes spam or abusive entries, and reads any customer replies that other shoppers posted to existing reviews. The list reflects the result of the moderation policy set on the [[apps-product-review]] **Settings** tab — depending on that policy reviews arrive here either as Pending (waiting for the merchant's explicit Publish click) or already Published.

This is the operational counterpart to [[customers-details-reviews]] — that screen shows one customer's reviews in their profile; this screen shows the whole store's review feed in one place, so the merchant can clear the moderation queue in one sitting rather than profile-by-profile.

This page is a **hub** — the full surface is split across seven aspect pages (see below). The Assistant should drill into the aspect that matches the question, not read every page.

## Where to find it

Sidebar → **Apps** → **Product Reviews** (after install) → **Reviews** tab.

The route is `/admin/apps/product_review/reviews`. The page is rendered by the Vue component `ApplicationsProductReviewReviewsPage` inside the `ApplicationsProductReviewMainPage` shell (subdomain: `ProductReview`).

The tab strip on this app is: **Overview**, **Settings**, **Reviews** (this page), **Questions** (only when Q&A is enabled per [[apps-product-review]] settings — see [[marketing-reviews-questions-tab]]).

## What the merchant can do here

- Moderate every storefront review and its replies in one place (Publish / Hide / Delete, bulk or per-row).
- Filter and search the queue, deep-link to a filtered view, and bulk-act on selections.
- Read each review in full via a read-only detail modal.
- Moderate threaded replies (Approve / Delete) per review.
- Manually add a review on behalf of a customer (backfill / migration).
- Configure the *arrival policy* and *reply policy* from [[apps-product-review]] Settings — those decisions drive what lands here in what state.

Drill into the relevant aspect below for the full mechanics.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice:

- [[marketing-reviews-moderation-queue]] — the table itself: columns, sort, filters, free-text search, bulk Publish / Hide / Delete, status states (`is_approved`), permission, what the merchant CANNOT do here.
- [[marketing-reviews-modals]] — the three modals: read-only Detail (rating + comment), Answers (per-reply card layout), Add new review (fields + locale-tolerant `created_at` handling + `CcHelpBox` plan-cap banner).
- [[marketing-reviews-arrival-flows]] — the three settings (`accept_review`, `approved_answers`, `accept_star`) that decide whether a storefront submission lands Pending vs Published; defaults if Settings is never opened.
- [[marketing-reviews-submission-rules]] — storefront-side validation: field caps (200/200/1000 chars + min rating 1), `added_reviews_conditions = 'all' | 'buyer'`, the `max_days` window (1-365, default 7), duplicate-review protection (one per customer per product), subscriber-link flow, no photo/video, no profanity filter.
- [[marketing-reviews-replies]] — threaded answers: `accept_answers` / `accept_answer_condition` / `approved_answers` for replies, independence from parent approval, no customer notification on merchant reply, cascade-delete from parent.
- [[marketing-reviews-plan-cap]] — the `product_reviews_added_rating` plan-feature: numeric / restricted by default (`restrict.defaults = 1`), checked on BOTH admin Add new review AND storefront submission, extendable via feature pack, in-modal unlock CTA.
- [[marketing-reviews-questions-tab]] — the conditional Q&A tab as a second instance of the same UI components, `type="question"` prop, separate backend endpoints, shared plan-cap and arrival policy.

## Settings & fields

The hub itself has no settings. Each aspect documents its own controls:

- Table mechanics (columns, sort, filters, bulk actions, status states) → [[marketing-reviews-moderation-queue]].
- Modal shells and Add new review form fields → [[marketing-reviews-modals]].
- Arrival-policy settings (`accept_review`, `approved_answers`, `accept_star`) → [[marketing-reviews-arrival-flows]].
- Submission validation, `added_reviews_conditions`, `max_days` → [[marketing-reviews-submission-rules]].
- Reply settings (`accept_answers`, `accept_answer_condition`) → [[marketing-reviews-replies]].
- Plan-feature mapping (`product_reviews_added_rating`) → [[marketing-reviews-plan-cap]].
- Q&A tab visibility (`question` setting flag) → [[marketing-reviews-questions-tab]].

## Business rules

Cross-cutting rules that span aspects:

- **Status change recomputes the product summary immediately.** Every Publish / Hide / Delete (review OR reply) updates the affected product's aggregate rating + total review count. The storefront product page's "X stars (Y reviews)" headline reflects the moderation decision on the next page load — no cache TTL. See [[marketing-reviews-moderation-queue]].
- **Delete is irreversible and cascades.** Per-row trash and bulk Delete both hard-delete the row and cascade to threaded replies. There is no soft-delete fallback. See [[marketing-reviews-moderation-queue]] and [[marketing-reviews-replies]].
- **Manual-add always publishes.** The Add new review modal hard-codes `is_approved = 1` server-side, bypassing the arrival-flow policy. See [[marketing-reviews-modals]] and [[marketing-reviews-arrival-flows]].
- **Plan-cap rejects, not Pendings.** When over the `product_reviews_added_rating` quota, submissions are blocked outright and never reach the queue in any state. See [[marketing-reviews-plan-cap]].
- **`approved_answers` is overloaded.** The same setting key gates *review auto-approval by star rating* AND *reply `is_approved` on creation* — two distinct behaviours on the same key. See [[marketing-reviews-arrival-flows]] and [[marketing-reviews-replies]].
- **Segment integration survives reinstall.** Uninstall + reinstall of [[apps-product-review]] reactivates any [[marketing-segments]] referencing `product_review.` keys. See [[marketing-reviews-submission-rules]].

## Related

- [[apps-product-review]] — parent app: settings, install, Q&A, broader review policy controls.
- [[customers-details-reviews]] — per-customer view of the same review data.
- [[marketing]] — Marketing pillar (the Product Reviews app surfaces under the Marketing sidebar group).
- [[products-products]] — products that get reviewed.
- [[marketing-segments]] — segment conditions on review activity.
- [[marketing-campaigns]] — subscriber-link review-solicitation flow.
- [[settings-admin-notifications]] — "New review added" admin email notification.
- [[settings-staff]] — per-role permissions for the moderation queue.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — plan-feature mechanics.
- [[customer]] — Customer entity (`customer_id` on the review row).
- [[product]] — Product entity (`product_id` on the review row).
- [[order]] — Order entity (`order_id` on the review row for verified-buyer reviews).
- [[subscriber]] — Subscriber entity (`subscriber_id` on email-triggered review submissions).

## Plan gates

This feature is gated by `product_reviews_added_rating` — see [[marketing-reviews-plan-cap]] for the full mapping (numeric, restricted by default, checked on both admin and storefront paths, extendable via feature pack).

## Open questions

Distributed to the aspect pages.
