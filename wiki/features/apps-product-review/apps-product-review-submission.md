---
type: feature
nav_path: "Apps → Product Reviews → Submission"
route_name: apps.product_review.overview
route_path: /admin/apps/product_review
aliases: ["Review submission form", "Leave a review", "Review validation", "Reply to review", "CreateReviewRequest", "CreateAnswerRequest", "Review time window"]
tags: [apps, others, reviews, qa, storefront, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 7
---

> Part of [[apps-product-review]]. See the hub for the other aspects (settings, moderation, Q&A, internals).

# Product Reviews — Submission

## Purpose

This aspect covers the customer-facing submission side: what fields the storefront review form, reply form, and (for Q&A) question form accept and require, the time-window that controls when a review can be left after purchase, and the constraints customers run into (no photo / video uploads, asymmetric email requirement on replies).

## Where to find it

The submission forms render on the storefront product detail page (reviews module + Questions tab). The merchant configures the policies that govern them on [[apps-product-review-settings]]; the moderation of what gets submitted is on [[apps-product-review-moderation]].

## What the merchant can do here

The merchant does not fill in these forms — customers do. This page is the canonical reference for support agents diagnosing *"why was my review rejected"* / *"why can't I leave a review on this old order"* / *"why does the reply form ask for my email"* tickets.

## Settings & fields

### Review-create validation (the request validator)

- `product_id` — required, integer.
- `user_name` — required, max 200 chars.
- `rating` — required, numeric, min **1** (0-star reviews are rejected — review must be a positive 1-5).
- `title` — required, max 200 chars.
- `comment` — required, max 1000 chars.

**No email field is required for a review** — the customer can submit without leaving an email address.

### Review-answer / reply validation (the request validator)

- `user_name` — required, max 200 chars.
- `user_email` — required, max 200 chars.
- `comment` — required (no max).

## Business rules

### Time-window enforcement

The default `max_days` is 7. The setting (configured on [[apps-product-review-settings]], range 1-365) limits how many days after purchase a customer can leave a review. E.g., 30 days means customers have 30 days post-purchase to leave a review. Beyond this window the review form is hidden / disabled per the storefront templates.

### No photo / video uploads on reviews

The review-submit form accepts only `product_id`, `user_name`, `rating`, `title`, and `comment` (max 1000 chars). There is no file-upload field — customers cannot attach images or videos to their review. The merchant can show product imagery on the page, but the customer's review is text-only.

### Replying to a review demands an email address

the request validator requires `user_email`, whereas the initial review submission does NOT require an email. This is asymmetric and may surprise merchants (who'd expect symmetry between review-create and reply-create): a customer can leave a review with no email but must supply one to reply to an existing review.

### Which name is saved as the author

The typed name is not always the one saved:

1. **Signed-in customer** — the form shows no name or email field; the account's full name and email are used.
2. **Remembered visitor** — the store remembers a visitor on that browser after they sign in, place an order, subscribe, or open a link from one of the store's campaigns. If that record has a name, it is saved instead of the typed one.
3. Otherwise, the name typed in the form.

The platform does not prefill the guest name field. So when reviews from different people carry the same person's name, they were most likely sent from a browser that person had used to sign in, order or open a campaign link, for example the merchant testing their own store. Reviews from a campaign review link take the name of the subscriber the link was sent to ([[apps-product-review-campaign-link]]); answers follow the same order, then the signed-in admin's name.

### Which name the storefront shows

When the review is linked to a customer account, the storefront shows the account's **current** name, so renaming the customer renames their reviews; otherwise it shows the saved name. The avatar initials come from the same name. The merchant cannot edit an existing review's author name; a review under any name can be added from the admin ([[apps-product-review-moderation]]).

### Customer notification on merchant reply — none

When the merchant replies to a review (creating a `parent_id` reference), the created-hook on the review only triggers a product summary update — no customer-notification event fires. The merchant should NOT assume the customer is auto-notified when they reply; this is currently a silent operation.

## Related

- [[apps-product-review]] — hub.
- [[apps-product-review-settings]] — `max_days` time window and reply / answer policy.
- [[apps-product-review-moderation]] — what happens to the submission after it is accepted.
- [[apps-product-review-qa]] — the question-submission form (different field set).

## Open questions

None — all previously-flagged questions resolved.
