---
type: feature
nav_path: "Apps → Product Reviews → Moderation"
route_name: apps.product_review.reviews
route_path: /admin/apps/product_review
aliases: ["Review moderation", "Approve review", "Verified buyer", "Reviews tab", "Questions tab moderation", "Pending reviews", "Threshold auto-approval"]
tags: [apps, others, reviews, qa, moderation]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 7
---

> Part of [[apps-product-review]]. See the hub for the other aspects (settings, submission, Q&A, internals).

# Product Reviews — Moderation

## Purpose

This aspect covers what happens to a review (or question) AFTER it is submitted: the three moderation modes, the verified-buyer eligibility check, anonymous-review handling, the plan-cap that rejects new reviews, and the admin Reviews / Questions tabs where the merchant approves, hides, or deletes content.

## Where to find it

Sidebar → Apps → **Product Reviews** → **Reviews** tab (`apps.product_review.reviews`) for review moderation, and the **Questions** tab (`apps.product_review.questions`) for Q&A moderation.

## What the merchant can do here

### Reviews tab

- List of all reviews across products.
- Filter / search / moderate — Approve / Hide / Delete bulk actions (same workflow as [[customers-details-reviews]]).
- **Add new review** — a form with **Select product**, **Client** (any name, typed freely), date, rating, title and **Comment**; the review is published at once. Marked *Paid feature*: it needs the same plan feature as reviews in general (see the plan cap below). This is how a merchant adds a review on someone's behalf, under any name.
- **Answers** — a review's answers open in a window where each can be approved (**Approve answer**) or deleted. There is no reply box there.

### Questions tab

- List of all questions on products (when Q&A is enabled — see [[apps-product-review-qa]]).
- Same moderation workflow, plus adding a question from the admin.

### What the merchant CANNOT do here

- Edit an existing review's text or author name — only Approve / Hide / Delete.
- Reply from this screen — replies are written on the storefront, see below.
- Export reviews — there is no Export button on the Reviews tab; reviews cannot be exported to a file for external analysis.

## Settings & fields

Moderation behaviour is driven by the settings on [[apps-product-review-settings]] (`accept_review` / approve-before-publish, `approved_answers`, `accept_star`, `added_reviews_conditions`). The Reviews / Questions tabs themselves expose only the per-row Approve / Hide / Delete actions and the filter / search controls.

## Business rules

### Three moderation modes

1. **All reviews require approval** (`accept_review = ON`, `approved_answers = OFF`) — every review pending until merchant clicks Approve.
2. **Threshold-based auto-approval** (`accept_review = ON`, `approved_answers = ON`, `accept_star = 4`) — reviews ≥ 4 stars auto-publish; 1-3 stars pending.
3. **All reviews auto-published** (`accept_review = OFF`) — no moderation.

Threshold-based is the most popular setting — it balances speed (good reviews go up fast) and protection (bad reviews get screened).

### Replying as the merchant

Open the product page on the storefront in the same browser while signed in to the admin. With **Allow replies** (`accept_answers`) on, the admin can always answer, whatever "who can answer" is set to; with it off nobody can. The answer is signed with the name of a customer or remembered visitor signed in on that browser, otherwise with the admin's name. A review answer is published at once when `approved_answers` is on, otherwise it waits under **Answers**; a question answer is published at once. The reviewer is not notified. Integrations can also add answers through the Admin API.

### Verified-buyer enforcement

When `added_reviews_conditions = 'buyer'`:

- Only customers who PURCHASED the product can leave a review.
- The platform checks the customer's order history before accepting the submission.
- Anonymous users CANNOT leave reviews under this rule.

When set to `'all'`:

- Any logged-in customer can review any product (regardless of purchase history).
- Anonymous (guest) submissions are also accepted — see anonymous reviews below.

### Verified-buyer check: order status MUST be `paid` OR `completed` OR fulfilled

Each review can reference an `order_id`, and the verified-buyer check queries orders where:

- `status IN ['paid', 'completed']`, OR
- `status_fulfillment = 'fulfilled'`.

So "verified buyer" = the customer must have a paid / completed / fulfilled order containing this product. Orders in `pending`, `cancelled`, `failed`, `refunded`, etc. **do NOT count** for verified-buyer review eligibility.

### Anonymous reviews — guest submissions supported

The review row stores `user_name`, `user_email`, AND `customer_id` / `subscriber_id` as separate optional fields. When a guest submits a review (no logged-in customer), the platform stores their `user_name` + `user_email` directly on the review row. Logged-in customers' reviews carry `customer_id`. This means guest reviews ARE supported when `added_reviews_conditions = 'all'`.

### Reviews stored as written — no automatic translation

The review row stores `title`, `comment`, `user_name`, `user_email` only. There is no language column and no per-language variants. Each review displays exactly as the customer wrote it; on a multi-language storefront the customer sees reviews in whatever language past reviewers used.

### Plan-cap behaviour: new reviews are REJECTED with a message

The integration exposes the `product_reviews_added_rating` plan feature. The merchant's plan tier may cap how many reviews can be CREATED per period — higher plans accept more reviews. When the merchant's plan tier does not include `product_reviews_added_rating`, the create-review endpoint returns the error: *"To add a product review you need to purchase additional functionality."* The customer's submission is dropped — no queue, no pending state. The same gate applies to Q&A submissions.

This means **for high-review-volume stores, plan tier matters** — the merchant may need to upgrade if reviews are flowing in faster than the plan allows.

### Permission

Standard apps permission scope + per-feature permissions for moderation actions (verify in [[settings-staff]]).

## Related

- [[apps-product-review]] — hub.
- [[apps-product-review-settings]] — the settings that drive these moderation modes.
- [[customers-details-reviews]] — per-customer review moderation view (depends on this app being active).
- [[settings-staff]] — moderation-action permissions.

## Open questions

None — all previously-flagged questions resolved.
