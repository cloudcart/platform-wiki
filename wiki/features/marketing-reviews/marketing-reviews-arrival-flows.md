---
type: feature
nav_path: "Apps → Product Reviews → Reviews → (arrival flows)"
route_name: apps.product_review.reviews
route_path: /admin/apps/product_review/reviews
aliases: ["Review arrival flows", "Auto-approve reviews", "Pending vs published on arrival", "accept_review", "approved_answers", "accept_star"]
tags: [marketing, apps, reviews, moderation, settings]
plan_gates: ["product_reviews_added_rating"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Reviews — Arrival flows (Pending vs Published on submission)

> Part of [[marketing-reviews]]. See the hub for related aspects (queue, modals, submission rules, replies, plan cap, Q&A tab).

## Purpose

When a customer submits a review on the storefront, it lands in the moderation queue in one of two states — Pending (`is_approved = 0`) or Published (`is_approved = 1`). Which state it arrives in is decided by **three settings** on the parent app's Settings tab. This page documents the three possible flows and what each one means for the merchant's daily workload.

For the *queue mechanics* (how the merchant operates on the result), see [[marketing-reviews-moderation-queue]]. For the *submission-side validation* (field caps, duplicate protection, verified-buyer mode), see [[marketing-reviews-submission-rules]].

## Where to find it

Sidebar → **Apps** → **Product Reviews** → **Settings** tab — the policy is controlled there. The *result* lands in **Apps → Product Reviews → Reviews** (the moderation queue).

## What the merchant can do here

- Choose between three review-arrival policies via the [[apps-product-review]] Settings tab.
- Inspect each review's `is_approved` state directly from the queue and Hide / Publish retroactively.

## Settings & fields

### The three settings that drive arrival state

All three live on [[apps-product-review]] Settings:

| Setting key | Values | Effect |
|---|---|---|
| `accept_review` | ON / OFF | Top-level gate: when OFF, all reviews auto-publish on submission. |
| `approved_answers` | ON / OFF | When ON, reviews auto-publish only if rating is ≥ `accept_star`. Otherwise they land Pending. **(Note on the name below.)** |
| `accept_star` | Integer 1–5 | The threshold rating used by `approved_answers`. Default `5` — only 5-star auto-publishes. |

Note on the setting key `approved_answers`: despite the name, this flag gates **review auto-approval based on star rating**, not merchant-reply approval. The validator pairs it with `accept_star` — the threshold rating. The UI label *"Automatically approve a review with a score above"* is the accurate description of behaviour.

### How a review lands here — three possible flows

The state a review lands in depends on those three settings (`accept_review`, `approved_answers`, `accept_star`):

1. **`accept_review = ON`, `approved_answers = OFF`** — every new review arrives as `is_approved = 0`. The merchant must explicitly Publish every one.
2. **`accept_review = ON`, `approved_answers = ON`, `accept_star = 4`** — reviews with rating ≥ 4 stars arrive as `is_approved = 1` (auto-published). Reviews with rating ≤ 3 stars arrive as `is_approved = 0` (pending).
3. **`accept_review = OFF`** — every review arrives as `is_approved = 1`. The queue still lists them; the merchant moderates retroactively by Hide / Delete.

Most stores run flow #2 — auto-publish positive reviews to keep momentum, screen low-rated ones manually.

### Default behaviour if Settings is never opened

If the merchant installs the app but never opens Settings, the defaults kick in:
- `added_reviews_conditions = 'all'` (anyone can review, no purchase needed) — see [[marketing-reviews-submission-rules]].
- `accept_star = 5` (only 5-star auto-publishes — so 1–4 stars require manual approval).
- `order_by = created_at` (newest first on the storefront).
- `max_days = 7` — the verified-buyer window. See [[marketing-reviews-submission-rules]].

The out-of-the-box behaviour is **intentionally restrictive** — low-rated reviews land in the moderation queue, never auto-published.

## Business rules

### Manual-add ALWAYS publishes, regardless of arrival policy

The Add new review modal (see [[marketing-reviews-modals]]) hard-codes `is_approved = 1` server-side. The three arrival flows apply only to storefront-submitted reviews. A merchant backfilling reviews manually bypasses the policy entirely.

### Replies inherit the arrival rule INDEPENDENTLY

Customer-posted replies to a review (threaded answers) use a parallel set of settings (`accept_answers`, `accept_answer_condition`) and inherit `is_approved = $approved_answers` on creation — that is, replies can auto-publish independently of the parent review's policy. The reply moderation flow is documented in [[marketing-reviews-replies]].

### Verified-buyer mode does NOT change arrival flow

Whether the store runs `added_reviews_conditions = 'all'` or `= 'buyer'`, the same three arrival flows apply once a submission passes validation. Verified-buyer mode is a *gate on who can submit*, not on whether the submission auto-publishes. See [[marketing-reviews-submission-rules]].

### Plan-cap exhaustion is BLOCKING, not Pending

When the store is over its `product_reviews_added_rating` quota, the submission is **rejected** outright — it does NOT land Pending. So Pending in the queue means "policy says you must review this", whereas a rejected submission never enters the queue at all. See [[marketing-reviews-plan-cap]].

## Related

- [[marketing-reviews]] — hub.
- [[apps-product-review]] — parent app where the policy is set.
- [[marketing-reviews-moderation-queue]] — what the merchant does with reviews after they arrive.
- [[marketing-reviews-submission-rules]] — what the storefront validates BEFORE the review reaches a flow.
- [[marketing-reviews-replies]] — the parallel arrival policy for replies.
- [[marketing-reviews-plan-cap]] — the quota that can block a submission outright.

## Open questions

- 📡 **Switching policy retroactively.** If the merchant flips `accept_review` from ON to OFF, do existing Pending reviews auto-publish, or do they remain Pending until manually published? (verify)
