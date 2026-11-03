---
type: feature
nav_path: "Apps → Product Reviews → Reviews → (plan-feature cap)"
route_name: apps.product_review.reviews
route_path: /admin/apps/product_review/reviews
aliases: ["product_reviews_added_rating", "Review plan cap", "Reviews quota", "Reviews paid feature", "Review feature pack"]
tags: [marketing, apps, reviews, plan-gates, billing]
plan_gates: ["product_reviews_added_rating"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Reviews — Plan-feature cap (`product_reviews_added_rating`)

> Part of [[marketing-reviews]]. See the hub for related aspects (queue, modals, arrival flows, submission rules, replies, Q&A tab).

## Purpose

The CloudCart Product Reviews app is gated by a single numeric plan-feature, `product_reviews_added_rating`. This page documents what the cap counts, where the check fires (admin manual-add AND storefront submission), what the merchant experiences when over the cap, and how to extend it (feature packs, plan upgrade). Other plan-gate semantics across the platform are documented in [[plan-gates]] and [[plan-vs-feature-pack]].

## Where to find it

The cap is invisible UI-wise — there is no progress bar showing "X of Y reviews used this month". The merchant becomes aware of it only when:
- They click **+ Add new review** in **Apps → Product Reviews → Reviews** and the modal opens with a *"Paid feature"* `CcHelpBox` banner on top — see [[marketing-reviews-modals]].
- A storefront customer's submission is rejected and the storefront falls through to a generic error.

## What the merchant can do here

- Buy a feature pack to extend the cap (`product_reviews_added_rating` is numeric / restricted by default — see [[plan-vs-feature-pack]]).
- Upgrade their plan tier to one that includes a higher cap.
- Click the unlock CTA inside the Add new review modal's `CcHelpBox` to enable the feature in-place — this fires `@finalize → handleEnableFeature(index)` and unlocks the form without a page reload. See [[marketing-reviews-modals]].

## Settings & fields

### The plan-feature mapping

| Mapping | Shape | What it controls |
|---|---|---|
| `product_reviews_added_rating` | Numeric (restricted by default) | Per-plan cap on the number of reviews the store may accept. Counted against the platform's product-review manager. Listed under `restrict.defaults` with value `1` — meaning **the feature is restricted out-of-the-box** on the default plan, and the store must upgrade or buy the feature pack to accept any reviews at all. Checked on BOTH paths: admin "Add new review" modal AND storefront customer-submission. Over-cap returns `status: 'error'` with toast *"To add a product review you need to purchase additional functionality."* Extendable via feature pack. |

### Where the check fires — both paths

- **Admin Add new review modal.** The endpoint `POST /admin/api/product_review/create` checks the cap server-side and returns `status: 'error'` with the *"To add a product review you need to purchase additional functionality."* toast when over.
- **Storefront customer submission.** The same plan check runs as part of the storefront submission validation pipeline. So a store can hit its monthly review quota and stop accepting NEW reviews from customers until the plan is upgraded or the quota resets.

### Restriction-by-default semantics

`product_reviews_added_rating` ships with `restrict.defaults = 1`, meaning the feature is **restricted out-of-the-box** on the default plan. A merchant installing Product Reviews on a fresh store will hit the cap on the very first review unless they're on a plan tier that includes the feature or they buy a feature pack. The defaults make the app effectively **opt-in via billing** rather than free-by-default.

## Business rules

### Plan-cap exhaustion REJECTS the submission — it does NOT land Pending

When the cap is exhausted, the submission is **blocked outright**. It never enters the moderation queue in any state — Pending, Published, or otherwise. This is distinct from the arrival flows documented in [[marketing-reviews-arrival-flows]], which are about *what state a submission lands in after passing the cap check*.

### Cap check runs on EVERY submission path

The same `product_reviews_added_rating` gate fires on:
- Admin manual-add via the Add new review modal.
- Storefront customer submission on the product page.
- Subscriber-link review submission (campaign-driven — see [[marketing-reviews-submission-rules]]). (verify)

The check is **path-agnostic** — there's no carve-out for any particular submission flow.

### Feature-pack-extendable

`product_reviews_added_rating` is a numeric gate, which means the merchant can extend it without changing plan tier via feature packs — see [[plan-vs-feature-pack]] for the mechanism. After a pack is purchased, the next submission proceeds normally.

### In-modal unlock vs. paid upgrade

The Add new review modal's `CcHelpBox` banner is the merchant's primary self-service unlock surface. Clicking the unlock CTA triggers `handleEnableFeature(index)` and mutates `application.features[index].current = true` LOCALLY so the form unlocks IN-PLACE without a page reload. For multi-feature stacks where several gates are pending, ONE help-box banner renders per pending feature.

The unlock CTA is the **same affordance** the platform uses across all plan-gated screens — it's not specific to Reviews.

### Reply submissions and the cap

`product_reviews_added_rating` is named for reviews, but the cap mechanism applies to the parent review-manager class. Whether *reply* creation also counts against the cap is implementation-detail-dependent. (verify)

### What the cap does NOT block

Reading existing reviews, moderating existing reviews (Publish / Hide / Delete in [[marketing-reviews-moderation-queue]]), and replying to existing reviews (where the reply itself is exempt — see Open questions) all proceed normally even when the cap is exhausted. Only **new review creation** is gated.

## Related

- [[marketing-reviews]] — hub.
- [[apps-product-review]] — parent app.
- [[marketing-reviews-modals]] — the in-modal `CcHelpBox` unlock banner.
- [[marketing-reviews-arrival-flows]] — contrast: arrival flows describe state AFTER the cap check passes.
- [[marketing-reviews-submission-rules]] — other validation that runs alongside the cap check.
- [[plan-gates]] — generic plan-gate documentation.
- [[plan-vs-feature-pack]] — how numeric gates are extended via packs.
- [[plan-features]] — the catalog of plan features.

## Open questions

- 📡 **Cap exhaustion UI on the storefront.** What does the customer see when their submission is rejected by the cap? Is the error message localised? (verify)
- 📡 **Reply creation counted against the cap?** Whether a reply (child row with `parent_id` set) also consumes a unit of the `product_reviews_added_rating` quota is unverified. (verify)
- 📡 **GraphQL resolvability.** GraphQL-resolvable: query the merchant's current plan + feature-pack stacks to read the `product_reviews_added_rating` cap and current consumption.
