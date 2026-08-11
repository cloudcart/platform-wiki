---
type: feature
nav_path: "Apps → Product Reviews → (storefront submission validation)"
route_name: apps.product_review.reviews
route_path: /admin/apps/product_review/reviews
aliases: ["Review submission rules", "Verified-buyer mode", "max_days", "Review field caps", "Duplicate review protection", "added_reviews_conditions"]
tags: [marketing, apps, reviews, validation, storefront, verified-buyer]
plan_gates: ["product_reviews_added_rating"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Reviews — Submission rules (storefront-side validation)

> Part of [[marketing-reviews]]. See the hub for related aspects (queue, modals, arrival flows, replies, plan cap, Q&A tab).

## Purpose

This page documents every server-side rule that runs **before** a storefront-submitted review reaches the moderation queue: who is allowed to submit (verified-buyer mode), field length caps, duplicate-review protection, and the `max_days` window after order. For *what happens once a submission passes validation* (Pending vs Published), see [[marketing-reviews-arrival-flows]]. For the *plan-cap that can block any submission*, see [[marketing-reviews-plan-cap]].

## Where to find it

The rules themselves are enforced server-side on the storefront submission endpoint. The merchant controls them from **Apps → Product Reviews → Settings** (the `added_reviews_conditions` + `max_days` controls on [[apps-product-review]]).

## What the merchant can do here

- Restrict who can submit a review (anyone vs verified buyers only) via `added_reviews_conditions`.
- Cap how long after the order a customer has to leave a review via `max_days`.
- Inspect verified-buyer associations on the review row in the queue (via the linked `customer_id` / `order_id`, even though no visual badge is rendered — see [[marketing-reviews-moderation-queue]]).

## Settings & fields

### Field caps (storefront submission validation)

Server-side validation on customer-submitted reviews enforces:
- **Customer name** (`user_name`): required, max **200 chars**.
- **Title**: required, max **200 chars**.
- **Comment** (the review body): required, max **1000 chars** — so reviews cannot be longer than ~150 words. Stores that need longer reviews need a third-party app.
- **Rating**: required, numeric, minimum 1 (so 0-star reviews are blocked; the storefront UI shows 1–5 stars).
- **Product ID**: required, must be a valid integer.

There is NO minimum character count enforced on the comment field — a single-character comment ("ok") passes validation.

### `added_reviews_conditions` — who may submit

| Value | Effect |
|---|---|
| `'all'` (default) | Any storefront visitor can submit, including guests. Guest submissions write `user_name` + `user_email` directly on the review row (no customer relation). |
| `'buyer'` | Only customers who have a `paid` / `completed` / fulfilled order containing the reviewed product can submit. |

### Verified-buyer mode — `max_days` window enforced from order date

When `added_reviews_conditions = 'buyer'`, the storefront ALSO checks:
- The customer's email or ID matches a real order containing the product.
- The order's `date_added + max_days` has not yet passed.
- If an `order_id` is on the submission, the order's status must be `paid`, `completed`, or fulfilled.

`max_days` is the merchant-configured "Maximum days to leave a review" window. The validator caps it at **integer 1–365** (so the merchant cannot allow indefinite review windows, only up to one year). Default value if unset: **7 days** — meaning a fresh store using the default has a tight 1-week review window from order date.

### Order-attribution rules in verified-buyer mode

The submission writes the order's `id` and the matching `OrderProduct`'s `id` onto the review row (`order_id` + `order_product_id`). This is what enables [[marketing-segments]] conditions like *"customers who left a review on an order in segment X"* to work. Guest reviews and reviews from `added_reviews_conditions = 'all'` mode have these columns NULL.

### Storefront sort and filter controls

The storefront product page's review section honours these query params:
- `?order=rating` or `?order=date` (only these two are whitelisted; anything else falls through to the merchant's `order_by` setting).
- `?sort=asc` or `?sort=desc`.
- `?filter=N` (1-5) to show only N-star reviews.

These map to customer-facing dropdowns on the storefront. Server-side rejection of array-shaped sort/order params is explicit (defensive against scanner probes like `?sort[$eq]=asc`).

### Storefront pagination

The storefront's `getComments` endpoint paginates **10 reviews per page**. This is hard-coded, not a merchant setting. The "Load more" / pagination UI on the storefront drives off this fixed page size.

### Subscriber-link review submission has its own flow

When the merchant sends "Leave a review" links to subscribers (via a campaign with the review module — see [[marketing-campaigns]] and [[subscriber]]), the email contains an encrypted hash of `{subscriber_id, order_id}`. Submitting via that link uses a different endpoint that **doesn't require login** — and it deletes the link record on first submission, so the same email link only works once. Demo links (with `subscriber_id = 'demo-url'`) just load the 100 most recent orders' products as a preview, no real submission. This flow is used by campaign templates that solicit reviews after fulfilment.

## Business rules

### Duplicate-review protection — one per customer per product

When the storefront submits a review, the platform checks for an existing review on the same product matching either the same email OR (if logged in) the same customer ID — and rejects with `"is_added_review"` error if found. This means **one customer can only review one product once** — they cannot post a second review on the same product even after a follow-up purchase. Editing an existing review from the storefront is not supported; the customer would have to ask the merchant to delete the old one first (see [[marketing-reviews-moderation-queue]] — note that delete is a hard-delete that cascades to answers).

### Photo / video reviews — not supported in core

The platform's built-in review system is text-only with a rating + title + comment. There is no `image` / `video` / `attachment` field. Stores that want media-rich reviews use third-party review apps instead of CloudCart Reviews.

### Profanity filter — not built-in

There is no built-in word blacklist / language filter on the submission path. Every review reaches the queue as-is; profanity moderation is fully manual via the Hide / Delete actions in [[marketing-reviews-moderation-queue]]. Stores that need automated filtering either rely on the `accept_review` Pending policy (see [[marketing-reviews-arrival-flows]]) or integrate an external moderation service via the storefront review-submission API.

### Verified-buyer surfacing in the queue — partial

When `added_reviews_conditions = 'buyer'`, only customers with a matching order can submit, and the submission writes `customer_id` + `order_id` on the review row. However, **the moderation queue UI does not visually badge "verified buyer" reviews** — the merchant only sees the customer's name. The verified-purchase association exists in the data, but surfacing it in the queue is currently an open gap.

### Guest reviews carry name + email on the row

When `added_reviews_conditions = 'all'`, a guest (no logged-in customer) submission writes the typed name + email directly on the review row as `user_name` + `user_email`. The queue shows `user_name` in the Customer column. The customer relation is null in that case.

### Segment integration survives reinstall

When [[apps-product-review]] is uninstalled then reinstalled, the install hook reactivates any [[marketing-segments]] whose conditions reference `product_review.` keys. So segments built on review activity (e.g., *"customers who left a 5-star review"*) survive app reinstalls.

## Related

- [[marketing-reviews]] — hub.
- [[apps-product-review]] — parent app settings (`added_reviews_conditions`, `max_days`, `order_by`).
- [[marketing-reviews-arrival-flows]] — what happens after submission passes validation.
- [[marketing-reviews-plan-cap]] — the quota that runs alongside validation.
- [[marketing-segments]] — segment conditions on review activity (`customer_id` / `order_id`).
- [[marketing-campaigns]] — subscriber-link review-solicitation flow.
- [[subscriber]] — subscriber entity used by the link flow.
- [[order]] — order whose status / date drives verified-buyer eligibility.
- [[customer]] — customer entity (`customer_id` on the review row).

## Open questions

- 📡 **Two-language stores and `max_days`.** Does the `max_days` window honour the order's `paid_at` or `date_added` exactly? The two can differ for delayed-payment methods. (verify)
- 📡 **Re-review after refund.** If the order is refunded after the review is written, does the review stay published? (verify)
