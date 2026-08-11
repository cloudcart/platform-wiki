---
type: feature
nav_path: "Design → Modules → Engagement → Request review (request_review)"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/{request_review_instance}
aliases: ["Request review module", "request_review module", "Review request module", "Leave a review module", "Модул покана за ревю"]
tags: [design, modules, engagement, product-review, request-review, page-builder]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Engagement module — request_review (Request review CTA)

> Part of [[design-modules-engagement]]. See the category page for the other engagement modules.

## Purpose

`request_review` is the **page-builder block** that renders a **call-to-action carousel** asking the LOGGED-IN customer to submit reviews for products they've recently purchased. Each slide shows a product the customer can rate, a 5-star picker, and a *"Write a review"* button that opens the review-submission flow from the [[apps-product-review]] app.

The block is **the inverse** of [[design-module-product-review]] — `product_review` displays existing reviews to social-proof the storefront, while `request_review` solicits NEW reviews from past buyers. Both blocks depend on the Product Review app.

## Where to find it

This is a **page-builder block** — it appears in the **Add module** picker when the merchant is editing a **Dynamic** page in [[marketing-landing-pages]]. Common placements:

- Post-purchase thank-you / order-confirmation landing page.
- Dedicated `/my-account/reviews` landing page.
- A standalone review-collection campaign target reachable from a post-purchase email.

The block does NOT appear on the **Design → Modules** tab list; it is page-builder-only.

## What the merchant can do here

- Edit the **title** (headline above the carousel).
- Edit the **description** (body copy under the headline).
- Toggle slider mode (`enable_slider`) — usually ON because the carousel cycles through multiple review-target products.
- Pick how many cards per row (`per_row`) for the rare static-grid layout.
- Pick an **accent colour** (`color`) for the title + description text.
- Enable / disable the block.
- Save / Reset / Cancel.

## Settings & fields

| Field | Type | Validation | Default | What it controls |
|-------|------|------------|---------|------------------|
| `enabled` | toggle | (bool) | `true` | Master on/off |
| `enable_slider` | toggle | (bool) | `true` | Carousel mode (typical) vs static grid |
| `title` | text | `char:0,100` | empty | Headline above the carousel (e.g., *"Leave us a review!"*; Bulgarian default copy reads *"Покана за оставяне на ревю"*) |
| `description` | text | `char:0,500` | empty | Body copy under the headline |
| `color` | color picker | (free-form) | `#bab1b1` | Accent colour for the title + description text |
| `per_row` | number | `int:1,12` | `3` | Cards per row (for static-grid mode) |

The block has fewer settings than [[design-module-product-review]] because the review-target product list is computed at request time — the merchant doesn't filter it. The block pulls the LOGGED-IN customer's recent purchase history.

## Theme dependencies

- Requires the **Product Review** app ([[apps-product-review]]) — both installed AND enabled. When either is false, the block doesn't register in the page-builder palette AND the storefront renders nothing.
- Requires the shopper to be **logged in**. Anonymous visitors see nothing.
- Requires the logged-in customer to have at least one product available to review. Otherwise the block renders nothing.
- Uses the `simple-rating` JS plugin for the unrated-stars display.

## Business rules

### Visibility rule chain

The storefront block renders only when ALL of the following are true:

1. `enabled = true` (module setting).
2. The Product Review app is installed AND enabled.
3. The visitor is signed in as a customer.
4. The customer has at least one product available to review.

If any of these fails, the block renders nothing — no fallback message, no empty state.

### Review-target product source

The carousel shows the customer's **purchased products that the customer has not already reviewed**, drawn from the [[apps-product-review]] app. Already-reviewed products are excluded. (verify) the exact look-back window — likely tied to the app's order-fulfillment status filter.

### Per-slide "Write a review" CTA

Each slide includes a 5-star picker (unrated, decorative) and a *"Write a review"* button (translation key the platform code) that links to the Product Review app's create-review flow for that product. Clicking opens an AJAX panel with the full review-submission form.

### `color` styling

The `color` value is applied inline to both the title and description text. Useful for matching the block to a brand palette on a custom landing page.

### `enable_slider = false`

When the slider is off, the cards are rendered as a static row with `per_row` cards across. Useful when there's just one or two products to review.

### Carousel options (data-attrs)

The carousel uses theme-shipped slider JS with these data attributes: `data-items=1`, `data-interval=3000`, `data-pause=true`, `data-dots=true`, `data-nav=true`, `data-autoplay=false`, `data-cycle=false`. These are NOT exposed to the merchant via settings — the carousel cycles only on manual click. Because `data-items=1` is fixed, the slider always shows ONE slide at a time; the `per_row` setting only affects the static-grid layout (`enable_slider = false`).

There is no way to filter the review-target list — the customer sees ALL of their unreviewed purchases regardless of date or category, so for high-volume buyers the carousel can be long.

### No anonymous CTA

There is no "create-an-account-to-review" flow on this block. If a shopper arrives at a landing page with this block embedded and is not logged in, they see nothing. Merchants who want to drive reviews from non-customers should use a Mailchimp / subscriber campaign that includes a "Log in to review" link in the email.

### Reset behaviour

Reset restores: `enabled=true`, `enable_slider=true`, `title=''`, `description=''`, `color='#bab1b1'`, `per_row='3'`.

### No merchant-side visibility hint

The block renders nothing when the customer has no eligible products to review, so it is invisible to most visitors — and there is no merchant-side indicator that this is the case.

## Related

- [[design-modules-engagement]] — hub.
- [[apps-product-review]] — installs the Product Review app; provides the review-target data + the review-creation flow.
- [[design-module-product-review]] — sibling; displays existing reviews as social proof.
- [[marketing-landing-pages]] — Dynamic pages use the page-builder, which exposes this block.
- [[marketing-campaigns]] — pair this block with a post-purchase email that links shoppers to a landing page containing `request_review`.
- [[design-themes]] — theme provides the visual styling for the carousel.

## Open questions

- 📡 **Review-target lookup window.** The carousel shows purchased-but-unreviewed products. (verify) the look-back window and whether it filters by fulfillment status. GraphQL-resolvable: query the Product Review app's review-target output for a given customer.
- 📡 **Customer purchase history.** The block reads from the merchant's order data. GraphQL-resolvable: query orders / line items for a customer.
- ⏸️ **Hard-coded carousel `data-items=1`.** Means slider always shows one slide. (verify) whether this is intentional or a future-multi-slide candidate.
- ⏸️ **Anonymous fallback.** No login CTA when the visitor is not signed in. (verify) whether a future enhancement adds a "Sign in to leave a review" prompt.
