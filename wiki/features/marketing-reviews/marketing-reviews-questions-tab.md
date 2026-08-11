---
type: feature
nav_path: "Apps → Product Reviews → Questions and Answers"
route_name: apps.product_review.questions
route_path: /admin/apps/product_review/questions
aliases: ["Questions and Answers tab", "Q&A tab", "Product Q&A", "Въпроси и отговори", "Q&A moderation"]
tags: [marketing, apps, reviews, qa, moderation]
plan_gates: ["product_reviews_added_rating"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Reviews — Questions and Answers tab

> Part of [[marketing-reviews]]. See the hub for related aspects (queue, modals, arrival flows, submission rules, replies, plan cap).

## Purpose

The Product Reviews app exposes a second tab — **Questions and Answers** — that is **conditionally shown only when the settings flag `question === 1`** is set on the app's settings. This page documents how the Q&A tab is a *second instance of the same Reviews UI components*, what differs behaviourally between the two, and how it routes through separate backend stores. The Reviews tab itself is documented in [[marketing-reviews-moderation-queue]] and [[marketing-reviews-modals]].

## Where to find it

Sidebar → **Apps** → **Product Reviews** → **Questions** tab.

Route: `/admin/apps/product_review/questions`. The tab strip exposes two tabs:

- **Reviews** (`apps.product_review.reviews`) — always shown. See [[marketing-reviews-moderation-queue]].
- **Questions and Answers** (`apps.product_review.questions`) — only when `question === 1` in app settings. When the Q&A feature is off in [[apps-product-review]] Settings, the tab is hidden entirely.

So the Reviews app actually has FOUR routes the merchant navigates: Overview, Settings, Reviews, and (conditional) Q&A.

## What the merchant can do here

Functionally identical to [[marketing-reviews-moderation-queue]] — paginated table of submissions, per-row publish/hide/delete, bulk Publish / Hide / Delete, free-text search, filters, Answers modal for threaded replies, and an Add new question modal in place of the Add new review modal. The only behavioural differences are listed under Settings & fields below.

## Settings & fields

### Component reuse — `type="question"` prop switches behaviour

The Questions tab is a SECOND instance of the same Reviews UI components — `ApplicationsProductReviewReviewsQuestionsPage` reuses the SAME `ApplicationsProductReviewCreate`, `ApplicationsProductReviewRatingCommentModal`, and `ApplicationsProductReviewAnswersModal` components but with the `type="question"` prop. When the prop flips, behaviour changes:

| What changes | Reviews mode (`type="review"`) | Questions mode (`type="question"`) |
|---|---|---|
| Create modal title-field label | *"Review title"* | *"Question title"* |
| Rating star picker visibility | Shown (`v-show="type === 'review'"`) | **Hidden** — questions have no rating |
| API endpoints (create) | `createReview` | `createReviewQuestion` |
| API endpoints (delete answer) | `deleteReviewAnswer` | `deleteReviewQuestionAnswer` |
| API endpoints (approve answer) | `approveReviewAnswer` | `approveReviewQuestionAnswer` |
| Table mutator (after-write cache refresh) | `apiApplicationProductReview.reviews.useSetQueryData` | `apiApplicationProductReview.questions.useSetQueryData` |
| Add button label | *"+ Add new review"* | *"Add new question"* |
| Bulk action toast (publish) | *"Published successfully"* | *"Published successfully"* |
| Bulk action toast (hide) | *"The reviews was hidden successfully"* | *"The questions was hidden successfully"* (typo *"was hidden"* preserved from translation) |

### Tab visibility gate

The Questions tab appears in the tab strip ONLY when the app's `question` settings flag is `1`. The flag is controlled from **Apps → Product Reviews → Settings** ([[apps-product-review]]). Disabling Q&A in Settings hides the tab entirely; the route still resolves (so a bookmarked URL works) but there is no in-app affordance to reach it.

## Business rules

### Two separate backend stores

The Reviews tab and the Questions tab bind to **different backend stores** despite sharing components. A review and a question are NOT the same entity — they have separate index endpoints, separate create endpoints, and separate answer endpoints. Cross-contamination is impossible (a review cannot become a question or vice versa).

### Rating star picker is hidden, not optional

Questions do not have a rating field at all. The star picker is `v-show`-hidden via the `type` prop, and the submission validation does not require / enforce a rating. Sorting on a (non-existent) rating column is therefore not available on the Questions tab.

### Reply moderation works the same way

The Answers modal in Questions mode behaves identically to Reviews mode — same right-aligned slide-out shell, same per-card layout, same Approve / Delete actions. Only the underlying API calls differ. See [[marketing-reviews-modals]] for the modal shell and [[marketing-reviews-replies]] for the reply lifecycle.

### Q&A submission shares the SAME plan-cap

Both Reviews and Q&A submissions count against `product_reviews_added_rating` — there is no separate Q&A-specific plan-feature key. So a store at the cap loses BOTH manual Add new review and manual Add new question affordances at once. See [[marketing-reviews-plan-cap]].

### The "+ Add new" modal is shared

The create modal is the SAME `ApplicationsProductReviewCreate` component, just bound to different mutation endpoints via the `type` prop. The locale-tolerant `created_at` handling, the field validation, and the plan-cap `CcHelpBox` banner all apply equally — see [[marketing-reviews-modals]].

### Settings policy applies to BOTH tabs

The arrival-flow settings (`accept_review` and friends) and the reply settings (`accept_answers`, `accept_answer_condition`) on [[apps-product-review]] Settings govern BOTH reviews and questions — there's no separate policy for Q&A. See [[marketing-reviews-arrival-flows]] and [[marketing-reviews-replies]].

## Related

- [[marketing-reviews]] — hub.
- [[apps-product-review]] — parent app and the `question` settings flag that gates this tab.
- [[marketing-reviews-moderation-queue]] — the Reviews tab counterpart.
- [[marketing-reviews-modals]] — the shared create / detail / answers modal components.
- [[marketing-reviews-replies]] — the reply lifecycle (same mechanics in Q&A mode).
- [[marketing-reviews-plan-cap]] — the shared `product_reviews_added_rating` plan-cap.
- [[marketing-reviews-arrival-flows]] — the shared arrival-flow policies.

## Open questions

- 📡 **Q&A-specific arrival policy.** Is there any plan to introduce a `accept_question` flag separate from `accept_review`? Currently both share the review flag. (verify)
- 📡 **Toast typo fix.** The *"The questions was hidden successfully"* toast preserves a grammatical error from the translation source. (verify)
