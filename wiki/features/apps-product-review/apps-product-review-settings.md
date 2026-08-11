---
type: feature
nav_path: "Apps → Product Reviews → Settings"
route_name: apps.product_review.settings
route_path: /admin/apps/product_review
aliases: ["Product Review settings", "Review policy settings", "Reviews configuration", "max_days", "accept_star", "added_reviews_conditions"]
tags: [apps, others, reviews, qa, settings, configuration]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[apps-product-review]]. See the hub for the other aspects (moderation, submission, Q&A, internals).

# Product Reviews — Settings

## Purpose

The Settings tab is the store-wide review-policy control panel. Every field here applies uniformly to every product in the catalog — there is no per-product review configuration. This is where the merchant decides who can review, whether reviews need approval, how long after purchase a review is allowed, whether replies and Questions & Answers are enabled, and how reviews are sorted on the storefront.

## Where to find it

Sidebar → Apps → install → **Product Reviews** → **Settings** tab (`apps.product_review.settings`).

## What the merchant can do here

- Toggle storefront display options (show rating on listing cards, hide rating when zero reviews, show only the aggregate average).
- Choose who can leave a review (all users vs verified buyers).
- Configure the moderation policy (approve-before-publish, threshold-based auto-approval) — see [[apps-product-review-moderation]] for the full moderation behaviour.
- Enable customer replies and choose who can answer.
- Set the post-purchase review time window (`max_days`).
- Enable the Questions & Answers feature and its moderation gate — see [[apps-product-review-qa]].

## Settings & fields

| Field | Type | Notes |
|-------|------|-------|
| **Show product list rating** | Switch | Display stars on category listing cards (vs only on product detail page). |
| **Hide rating if no reviews** | Switch | When product has zero reviews, hide the star module entirely (avoids "0 stars" misleading). |
| **Approve before publish** | Switch | When ON, reviews are Pending until merchant approves (default for spam protection). |
| **Add reviews from** (`added_reviews_conditions`) | Select | "All users" OR "Only purchased the product" — gates who CAN leave a review. |
| **Automatic approval of responses** | Switch | Auto-approve customer replies to existing reviews. |
| **Automatically approve a review with a score above** (`accept_star`) | Select (1-5 stars) | When `approved_answers` is ON: reviews ≥ this threshold auto-publish. (Useful for not slowing down 4-5 star reviews while still moderating 1-3 stars.) |
| **Show only overall product rating** | Switch | Hide individual reviews; show only the aggregated average. |
| **Allow replies** (`accept_answers`) | Switch | Customers can reply to existing reviews. |
| **Add answers from** (`accept_answer_condition`) | Select | When replies enabled: "All users" OR "Administrators" only. |
| **Sort feedback by** (`order_by`) | Select | "Date" (`created_at`) OR "Rating". |
| **Maximum period for leaving a review** (`max_days`) | Number | Days after purchase a customer can leave a review (1-365). |
| **Questions and Answers** (`question`) | Switch | Master toggle for the Q&A feature. |
| **Approve question before publishing** (`question_approved`) | Switch | When Q&A is ON: gate questions through moderation. |

### Dependent fields (conditional UI)

The `dependField` + `dependValue` pattern auto-hides irrelevant fields:

| Parent field | Child fields appear when |
|--------------|---------------------------|
| `approved_answers = ON` | `accept_star` (auto-approve threshold) |
| `accept_answers = ON` | `accept_answer_condition` (who can answer) |
| `question = ON` | `question_approved` (gate questions through moderation) |

## Business rules

### Default `added_reviews_conditions = 'all'`

Per the class constructor, `'added_reviews_conditions' => 'all'` is the default — anyone can leave reviews. The merchant explicitly switches to `'buyer'` (verified-purchase only) for stricter policy; the verified-buyer enforcement is detailed on [[apps-product-review-moderation]].

### Other install defaults

Beyond `added_reviews_conditions = 'all'` and `max_days = 7`, the platform seeds:

- `accept_star = 5` — when threshold auto-approval is later enabled, only PERFECT 5-star reviews auto-publish by default. The merchant typically loosens this to 4 to widen the auto-approval band.
- `accept_answer_condition = 'all'` — when replies are later enabled, anyone can answer by default. The merchant tightens to admin-only as needed.
- `order_by = 'created_at'` — newest first by default.

### Max-days range is 1-365

The settings validation enforces `max_days` — required, integer, min 1, max **365**. So the merchant can set the review window from 1 day (very tight) up to **365 days post-purchase** (a full year). Beyond 365 the setting is rejected. The default after install is **7 days** — the merchant typically extends to 30 / 60 / 90 days depending on product type. The time-window's effect on the storefront form is described in [[apps-product-review-submission]].

### `isConfigured` requires 4 always-required settings

The integration considers itself configured when `added_reviews_conditions`, `accept_star`, `order_by`, and `max_days` all have values. These are the minimum-required settings for the integration to function. Q&A toggles and reply settings are optional refinements.

### Settings save requires 5 fields (two conditional)

The save endpoint (POST only) enforces:

- `added_reviews_conditions` — required (the "who can review" select).
- `accept_star` — required only when `approved_answers = 1` (the threshold star rating).
- `accept_answer_condition` — required only when `accept_answers = 1` (the "who can answer" select).
- `order_by` — required (Date or Rating).
- `max_days` — required, integer, 1-365.

`accept_star` and `accept_answer_condition` are conditional-required (only fire when their parent toggle is on). `isConfigured` excludes `accept_answer_condition` because it's only relevant when replies are on.

### Settings are store-wide — no per-product override

All review settings (moderation, who-can-review, `max_days`, replies, Q&A) apply uniformly to every product. There is no per-product toggle to disable reviews on a specific item — to suppress reviews on adult / restricted products, the merchant must hide the storefront review module at the theme level.

## Related

- [[apps-product-review]] — hub.
- [[apps-product-review-moderation]] — how the who-can-review and approval settings translate into moderation behaviour.
- [[apps-product-review-qa]] — the Questions & Answers feature toggled here.
- [[settings-admin-notifications]] — "New review added" notification event.

## Open questions

None — all previously-flagged questions resolved.
