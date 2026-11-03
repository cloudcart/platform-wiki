---
type: feature
nav_path: "Apps → Product Reviews → Internals"
route_name: apps.product_review.overview
route_path: /admin/apps/product_review
aliases: ["Product Review internals", "Review install hook", "Review lifecycle hooks", "Segment reactivation", "SumAndCountReviews", "Review aggregate recompute", "Review notification emails"]
tags: [apps, others, reviews, qa, internals, segments]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[apps-product-review]]. See the hub for the other aspects (settings, moderation, submission, Q&A).

# Product Reviews — Internals

## Purpose

This aspect documents the behind-the-scenes behaviour the merchant doesn't configure but should understand for support: what the install hook seeds (notification emails, segment reactivation), the per-review and per-question lifecycle side-effects (product-summary recompute, cache flush, cascading deletes), the eleven segment-condition managers the app registers, the aggregate-recompute command, and the absence of import / export paths.

## Where to find it

These behaviours are not surfaced as a screen. They fire automatically on install, on review / question CRUD, and on segment evaluation. Support agents reach this page when diagnosing *"my review counts are wrong"*, *"why did my segments reactivate"*, or *"can I import reviews from another platform"* tickets.

## What the merchant can do here

Nothing directly configurable — this is a reference for platform-internal behaviour. The merchant's touch points are the install / uninstall action ([[apps]]), the [[marketing-segments]] conditions this app contributes, and the [[settings-admin-notifications]] "New review added" event.

## Settings & fields

No merchant-facing fields. The notification email placeholders below (`{$shop_name}`, `{$product_name}`, `{$rating}`, `{$comment}`, `{$customer_name}`, `{$site_url}`) are the verbatim tokens seeded into the admin-notification template.

## Business rules

### Install hook re-activates dependent segments

On install (or re-install), the platform runs a one-shot query to find subscriber segments where `active = 0` AND `conditions LIKE '%product_review.%'`. It sets these back to `active = 1` AND `inactive_errors = null`. So **when the merchant uninstalls + reinstalls Product Review, any [[marketing-segments]] that were broken because they depend on review data automatically reactivate** — a thoughtful operational detail that prevents permanent segment breakage when the app is toggled.

### Install seeds admin-notification mails — in many languages

The install hook inserts admin-notification email templates for "New review added". The "New review added" template is seeded in English, Bulgarian, Romanian, Greek, Hungarian, German, Spanish, French, Italian, Macedonian (and Serbian / Albanian / Czech / Finnish / Polish per the lang dir). So **the admin notification reaches the operator in their localised language** when their admin UI is set to one of these. The mails fire when a new review is added (per [[settings-admin-notifications]] event subscription).

### Per-review and per-question lifecycle hooks

The Product Review and Q&A models each carry boot-time lifecycle hooks that drive storefront and admin behaviour:

**Review model:**

- **On `created`** — the product summary (review-count + average-rating cache on the Product row) is recomputed; if the reviewer is a tracked Subscriber on a `parent_id = null` (a customer-submitted review, not a merchant reply), any pending review-link-send row for that subscriber is deleted (so the "leave a review" email link isn't re-sent after they already reviewed).
- **On `updated`** — product summary is recomputed (so flipping `active` between hidden / shown updates the public rating immediately).
- **On `deleting`** — every child reply (`parent_id = <review_id>`) is hard-deleted first, then product summary is recomputed.
- **On `deleted`** — product summary recomputes a final time AFTER the row is gone, so the cached rating drops the removed review's stars.

**Question model:**

- **On `deleting`** — all answers (replies) for the question are deleted in the same pass.
- **On `saved` and `deleted`** — the cached product-list and product-detail payloads are flushed so the storefront re-fetches with the updated Q&A surface visible on the product page.

So a review or question CRUD operation is never a single-row write — every save / delete cascades to the product-summary recomputation and (for questions) the product-cache flush, and replies always cascade through their parent. Merchants who add many reviews in quick succession will see the per-product `total_reviews` and `average_rating` columns update transactionally on each save.

### 11 segment-condition managers registered

The Product Review app contributes ELEVEN segment-condition types for [[marketing-segments]]:

- CommentAverage / CommentCategory / CommentDate / CommentDateInterval / CommentLinkSend / CommentTimes / CommentVendor / Comment / LastComment / OrderWithoutComment / Rating / WithoutComment.

So merchants can build sophisticated segments like "customers with average rating ≥ 4 in the last 30 days who ordered from vendor X" — these only become available when Product Review is installed + active.

### Aggregate recompute: reactive per-save, plus a manual backfill command

Day-to-day, the platform doesn't need a batch recompute because each review save triggers an aggregate update on the product (see the lifecycle hooks above). For backfills / drift repair there is a `product-reviews:sum-and-count-reviews` console command that recomputes review aggregates (averages, counts) per product. **It is NOT scheduled** — it must be run manually OR by an external cron / orchestration. So if the per-product rating summary drifts (e.g., after a bulk import of historical reviews), the merchant needs CloudCart operator help to trigger this command — there is no admin button for it.

### No built-in import from external platforms

The integration exposes no CSV / Yotpo / Trustpilot import endpoint. Migrating reviews from another platform requires custom data entry — the only review-creation paths are the storefront submission form and the admin Reviews tab (one-at-a-time entry by the merchant). [[apps-yotpot]] is the alternative external review platform.

### No bulk CSV export

There is no Export button on the Reviews tab. Reviews are managed inside the admin (filter / search / approve / hide / delete) but cannot be exported to a file for external analysis.

## Related

- [[apps-product-review]] — hub.
- [[apps]] — App Store; install / uninstall triggers the segment reactivation + email seeding.
- [[marketing-segments]] — the 11 segment conditions this app contributes; segments reactivate on reinstall.
- [[settings-admin-notifications]] — "New review added" notification event.
- [[apps-yotpot]] — alternative review platform (external).

## Open questions

None — all previously-flagged questions resolved.
