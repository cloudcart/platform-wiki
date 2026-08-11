---
type: feature
nav_path: "Apps → Product Reviews → Reviews → (modals)"
route_name: apps.product_review.reviews
route_path: /admin/apps/product_review/reviews
aliases: ["Review detail modal", "Review answers modal", "Add new review modal", "Review modals"]
tags: [marketing, apps, reviews, modals, ui]
plan_gates: ["product_reviews_added_rating"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Reviews — Modals (detail, answers, add new)

> Part of [[marketing-reviews]]. See the hub for related aspects (queue, arrival flows, submission rules, replies, plan cap, Q&A tab).

## Purpose

The Reviews page hosts THREE distinct modals, all driven from the same row but via different click targets. This aspect documents each modal — its shell, its body, what the merchant can do inside, and what they cannot. The table itself is documented in [[marketing-reviews-moderation-queue]].

## Where to find it

Sidebar → **Apps** → **Product Reviews** → **Reviews** tab. From a table row:

- Click the **Comment** text → opens the **Detail (rating + comment)** modal.
- Click the **speech-bubble icon** with the answer count badge → opens the **Answers** modal.
- Click **+ Add new review** above the table → opens the **Add new review** modal.

## What the merchant can do here

### Three modals — distinct surfaces

| Modal | Trigger | Purpose |
|---|---|---|
| **Detail (rating + comment)** | Click the Comment text or Status chip | Read the full review (title + stars + comment) — read-only |
| **Answers** | Click the speech-bubble icon with the answer count badge | Moderate threaded replies (approve / delete) |
| **Add new review** | Click "+ Add new review" button | Manually create a review on behalf of a customer |

None of the three modals lets the merchant edit a published review's text — only approve / hide / delete actions and answer moderation.

## Settings & fields

### Detail modal — exact UI shell (read-only)

A **right-aligned slide-out** modal (`class="modal-right"`, size `lg`):
- **Header**: review's `title` field rendered as raw HTML (so emoji + entity-encoded chars display correctly) + a ghost-variant **Close** button on the right side. No Edit or Delete affordance.
- **Body**: a single card containing `data.comment` rendered as raw HTML. Wrapper class: `edit-settings-modal-content cc:rounded-lg`.
- **No footer** — only the header Close button or backdrop click dismisses.

### Answers modal — per-reply card layout

Same right-aligned slide-out shell (`lg`, `modal-right`). On open, AJAX-fetches `GET /admin/api/product_review/{id}/answers` — until the fetch settles, the body shows a `<CcLoader/>` spinner. The body then lists EACH answer as its own `cc-card`:

| Card section | Content |
|---|---|
| Top labelled row | "User:" + `answer.user_name` (raw HTML), then "Date:" + `answer.created_at` |
| Reply body | `answer.comment` rendered as raw HTML in the middle of the card |
| `<hr/>` divider | Separates body from per-answer actions |
| Bottom action row | Left: thumbs-up icon with tooltip *"Approve answer"* / *"Change the status of the answer"* — **only shown when `answer.is_approved == 0`**. Right: times-circle icon with tooltip *"Delete answer"* |

Spinners replace the icon when the per-action mutation is in flight (`statusLoader` / `deleteLoader`). Closing the modal clears the answer list (`answers.value = []`) so re-opening always re-fetches fresh.

The reply lifecycle (approve, delete, who can post) is documented in [[marketing-reviews-replies]].

### Add new review modal — fields

Right-aligned slide-out (`modal-right`, size `lg`). Custom header carries:
- Left: title *"Create new"* (translated; the same create modal handles BOTH Reviews and Q&A — see [[marketing-reviews-questions-tab]]).
- Right: ghost **Cancel** + primary **Save** button. Save is disabled while `disabled` is true (per-feature gate not yet purchased — see [[marketing-reviews-plan-cap]]) or while the mutation is in flight (`submitLoader`).

| Field | Required | Notes |
|-------|----------|-------|
| **Select product** | Yes | Autocomplete (`/admin/api/core/products/search`). |
| **Client** (`user_name`) | Yes | Free-text customer display name. |
| **Select a date and time for the review** (`created_at`) | No | Optional override; default is `now` in store timezone. See `created_at` handling below. |
| **Select rating** | Yes | 1–5 stars. |
| **Enter a review title** (`title`) | Yes | HTML-escaped on save. |
| **Enter a review** (`comment`) | Yes | HTML-escaped on save. |

### `created_at` handling — locale-tolerant

- If the merchant leaves the field empty, the modal sets it to `moment(new Date).format(timeFormat)`.
- If the entered value contains `pm` / `am` (12-hour format), they are stripped and replaced with `:00`.
- If the merchant's date format does not include seconds (`ss`), the modal appends `:00` to the entered string.

The API always receives a fully-qualified timestamp regardless of the merchant's locale.

### Per-feature gate banner inside the Add new review modal

When the **`product_reviews_added_rating`** plan-feature is not currently available (e.g. quota exhausted), the modal shows a `CcHelpBox` banner at the top with `type="danger"` and label *"Paid feature"* + the underlying feature mapping + name. The fields below the banner are disabled until the merchant clicks the unlock CTA inside the help-box (which fires `@finalize → handleEnableFeature(index)` and mutates the local `application.features[index].current = true` so the form unlocks IN-PLACE without a page reload). If multiple required features are pending, ONE help-box banner is rendered per feature. Full plan-cap semantics: [[marketing-reviews-plan-cap]].

## Business rules

### Detail modal is read-only by design

There is no "Edit" affordance on the detail modal. To change a review the merchant must Delete it (and ask the customer to resubmit) — see [[marketing-reviews-submission-rules]] for the one-per-customer-per-product rule that complicates resubmission.

### Manual-add reviews always publish immediately

Reviews created through the Add new review modal post to `POST /admin/api/product_review/create`, and the controller hard-codes `is_approved = 1` on the new row — i.e., manually-added reviews are always **Published**, bypassing the normal moderation flow (see [[marketing-reviews-arrival-flows]]). Useful for backfilling historical reviews from another platform.

### Title and comment are HTML-escaped on save

The Add new review endpoint applies `htmlspecialchars` to both `title` and `comment`. The Detail modal then renders them as raw HTML, which displays escaped entities correctly (so `&lt;script&gt;` in the body renders literally as text, not as a tag).

### Reused for Q&A with a `type="question"` switch

The create modal, the detail modal, and the answers modal are ALL reused inside the Questions tab with the `type="question"` prop. Behavioural changes when the prop flips: title label changes, rating star picker hides, API endpoints switch. See [[marketing-reviews-questions-tab]].

## Related

- [[marketing-reviews]] — hub.
- [[apps-product-review]] — parent app and its settings.
- [[marketing-reviews-moderation-queue]] — the table that hosts these modals.
- [[marketing-reviews-replies]] — what the Answers modal moderates.
- [[marketing-reviews-plan-cap]] — the gate that disables the Add new review modal.
- [[marketing-reviews-questions-tab]] — how these same components are reused for Q&A.

## Open questions

- 📡 **Manual-add bypass of `product_reviews_added_rating` quota.** When the merchant manually adds a review while at the cap, does the backfill consume quota or is it exempt? (verify)
