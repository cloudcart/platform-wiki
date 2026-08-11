---
type: feature
nav_path: "Apps → Product Reviews → Questions & Answers"
route_name: apps.product_review.questions
route_path: /admin/apps/product_review
aliases: ["Questions and Answers", "Q&A", "Product questions", "CreateQuestionRequest", "Ask a question", "Question moderation"]
tags: [apps, others, reviews, qa, questions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[apps-product-review]]. See the hub for the other aspects (settings, moderation, submission, internals).

# Product Reviews — Questions & Answers

## Purpose

The Questions & Answers (Q&A) feature is the opt-in second half of the Product Reviews app. When enabled, the storefront product page gains a Questions tab where customers can ask product questions and other customers or administrators can answer. This page covers the Q&A toggle, the question-submission requirements (which differ from reviews), and the Q&A moderation gate.

## Where to find it

Enabled via the **Questions and Answers** (`question`) toggle on [[apps-product-review-settings]]. Questions are moderated on the **Questions** tab (`apps.product_review.questions`) — see [[apps-product-review-moderation]].

## What the merchant can do here

- Turn Q&A on / off store-wide via the `question` master toggle.
- Require questions to pass moderation before publishing via `question_approved`.
- Moderate submitted questions on the Questions tab (Approve / Hide / Delete — same workflow as reviews).

## Settings & fields

### Q&A toggles (on [[apps-product-review-settings]])

| Field | Type | Notes |
|-------|------|-------|
| **Questions and Answers** (`question`) | Switch | Master toggle for the Q&A feature. |
| **Approve question before publishing** (`question_approved`) | Switch | When Q&A is ON: gate questions through moderation. |

### Question-create validation (the request validator)

- `product_id` — required, integer.
- `user_name` — required, max 200 chars.
- `title` — required, max 200 chars.
- `comment` — required, max 1000 chars.

There is **NO `rating` field on a question** (questions are not rated). Otherwise the field set is identical to a review submission — contrast with the review and reply forms on [[apps-product-review-submission]].

## Business rules

### Conditional Q&A

The Q&A feature is opt-in via the `question` toggle. When ON:

- Customers see a Questions tab on product pages.
- They can ask new questions; other customers / admins can answer.
- Questions optionally require approval (`question_approved`).

### Plan-cap applies to Q&A too

The same `product_reviews_added_rating` plan gate that caps review creation applies to Q&A submissions — when the plan tier does not include the feature, the create endpoint rejects the submission with *"To add a product review you need to purchase additional functionality."* See [[apps-product-review-moderation]].

### Question lifecycle side-effects

The Question model carries boot-time lifecycle hooks (detailed on [[apps-product-review-internals]]):

- On `deleting` — all answers (replies) for the question are deleted in the same pass.
- On `saved` and `deleted` — the cached product-list and product-detail payloads are flushed so the storefront re-fetches with the updated Q&A surface visible on the product page.

## Related

- [[apps-product-review]] — hub.
- [[apps-product-review-settings]] — the `question` + `question_approved` toggles.
- [[apps-product-review-submission]] — review / reply form field sets (contrast with the question form).
- [[apps-product-review-moderation]] — the Questions tab moderation workflow.
- [[apps-product-review-internals]] — Question model lifecycle hooks + cache flush.

## Open questions

None — all previously-flagged questions resolved.
