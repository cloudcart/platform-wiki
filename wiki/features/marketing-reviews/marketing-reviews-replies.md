---
type: feature
nav_path: "Apps → Product Reviews → Reviews → (replies / answers)"
route_name: apps.product_review.reviews
route_path: /admin/apps/product_review/reviews
aliases: ["Review replies", "Threaded answers", "Reply moderation", "accept_answer_condition", "accept_answers", "approved_answers (replies)"]
tags: [marketing, apps, reviews, replies, moderation]
plan_gates: ["product_reviews_added_rating"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Reviews — Replies (threaded answers)

> Part of [[marketing-reviews]]. See the hub for related aspects (queue, modals, arrival flows, submission rules, plan cap, Q&A tab).

## Purpose

Customers (and merchants) can post **replies** to existing reviews — threaded answers that show under the parent review on the storefront product page. This page documents how those replies are stored, how the merchant moderates them, and the three independent settings that govern whether a reply auto-publishes, who may post one, and whether the reply feature is enabled at all.

For the *root review* lifecycle (single inbox, Publish / Hide / Delete), see [[marketing-reviews-moderation-queue]]. For the *answers modal UI* itself, see [[marketing-reviews-modals]].

## Where to find it

Sidebar → **Apps** → **Product Reviews** → **Reviews** tab → click the **speech-bubble icon with the count badge** on a row → the Answers modal opens listing every reply.

The reply-feature toggles live on **Apps → Product Reviews → Settings** ([[apps-product-review]]).

## What the merchant can do here

- See every reply (customer-to-review or merchant-to-review) under a given root review, listed inside the Answers modal.
- **Approve** a Pending reply (thumbs-up icon, shown only when `is_approved == 0`).
- **Delete** any reply (times-circle icon).

The merchant CANNOT, from this screen:
- Reply to a review as the merchant — no "Add merchant reply" textbox. See Business rules.
- Edit the reply text — only approve / delete.
- Mark a reply as "needs review" separate from "hidden".

## Settings & fields

### Three settings that drive reply behaviour

All three live on [[apps-product-review]] Settings:

| Setting key | Values | Effect |
|---|---|---|
| `accept_answers` | ON / OFF | Top-level gate for the reply feature. OFF disables replies entirely. |
| `accept_answer_condition` | `'all'` / `'admin'` | Who may submit a reply on the storefront. |
| `approved_answers` | ON / OFF | When a reply IS accepted, this controls `is_approved` on creation. |

### `accept_answer_condition` values

- `'all'` — any visitor can reply to a review **without being logged in**.
- `'admin'` — only admin / staff replies are accepted; storefront visitor reply attempts get rejected silently.

### `is_approved` on a reply

Replies inherit `is_approved = $approved_answers` on creation — meaning replies can be auto-published independent of the parent review's policy. The same `approved_answers` setting key is reused by the *review* arrival flow (see [[marketing-reviews-arrival-flows]]), but for replies it is the literal `is_approved` value rather than a star-rating gate.

### Per-reply actions inside the Answers modal

| Action | When shown | Endpoint family |
|---|---|---|
| **Approve answer** (thumbs-up icon) | Only when `answer.is_approved == 0` | `approveReviewAnswer` for reviews / `approveReviewQuestionAnswer` for Q&A |
| **Delete answer** (times-circle icon) | Always | `deleteReviewAnswer` for reviews / `deleteReviewQuestionAnswer` for Q&A |

Tooltips (verbatim): *"Approve answer"* / *"Change the status of the answer"* on the approve icon; *"Delete answer"* on the delete icon. The full modal shell is documented in [[marketing-reviews-modals]].

## Business rules

### Replies live in the same table with `parent_id` set

Replies are rows in the same backing table as root reviews, with `parent_id` pointing at the root review's `id`. The moderation-queue index query explicitly excludes `parent_id != null` rows so replies don't pollute the main table — see [[marketing-reviews-moderation-queue]]. They surface only through the Answers modal, which queries `parent_id = {reviewId}`.

### Reply approval flag is INDEPENDENT of the parent review's approval flag

The parent review and its replies are approved separately. Hiding the parent review **does not** auto-hide its replies; restoring the parent does **not** auto-publish its replies. Each reply tracks its own `is_approved` toggle.

### Merchant reply must be posted from the storefront or via API

The Answers modal has no "Add merchant reply" textbox. To respond to a review as the merchant, the merchant must either:
- Reply from the storefront product page **logged in as the staff account**, OR
- Use the `POST /api/product_review/create` endpoint with a `parent_id` referencing the root review.

There is no admin-panel affordance to draft a merchant reply directly.

### Customer is NOT notified when the merchant replies

When the merchant (or staff) replies to a review (creating a child review with `parent_id` set), the platform updates the product's review summary but **does not** trigger a customer notification email. The customer who wrote the original review will not get notified that the merchant replied — they only see it if they revisit the storefront product page.

### Delete cascades from parent to all replies

When a root review is hard-deleted (per-row trash or bulk Delete in [[marketing-reviews-moderation-queue]]), every reply with `parent_id` pointing at that review is also hard-deleted. There is no soft-delete fallback for replies either.

### Aggregate product summary recomputes on reply moderation

Like root reviews, every approve / delete on a reply recomputes the parent product's aggregate rating + total review count — though the practical effect on rating is minor (replies don't carry stars). The recomputation runs unconditionally on every moderation action.

## Related

- [[marketing-reviews]] — hub.
- [[apps-product-review]] — parent app settings (`accept_answers`, `accept_answer_condition`, `approved_answers`).
- [[marketing-reviews-modals]] — the Answers modal UI shell.
- [[marketing-reviews-moderation-queue]] — the root-review queue replies live underneath.
- [[marketing-reviews-arrival-flows]] — the parallel approval policy for root reviews; note the shared `approved_answers` key.
- [[marketing-reviews-questions-tab]] — the Q&A tab uses the same answer-moderation flow against a different store.

## Open questions

- 📡 **Notification opt-in for the customer.** Is there a planned setting to email the original reviewer when the merchant replies? (verify)
- 📡 **Reply edit window.** Can a customer edit their own reply within a grace period? (verify)
