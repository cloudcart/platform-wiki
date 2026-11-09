---
type: feature
nav_path: "Apps → Product Reviews → Review requests by campaign"
route_name: apps.product_review.overview
route_path: /admin/apps/product_review
aliases: ["Leave a review link", "Review request campaign", "products_leave_feedback_url", "Order products feedback url", "Without product review", "Leave feedback segment", "Send link but not leave feedback for product", "Empty review button in campaign", "Линк за писане на отзиви на закупени продукти", "Без оставен отзив"]
tags: [apps, others, reviews, campaigns, segments, variables]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[apps-product-review]]. See the hub for the other aspects (settings, moderation, submission, Q&A, internals).

# Product Reviews — review requests by campaign

## Purpose

How a merchant asks buyers for reviews through a [[marketing-campaigns|campaign]]: the segment conditions the Product Reviews app adds, the campaign variable `{$products_leave_feedback_url}` (listed as "Order products feedback url"), what the link opens, and how the review window (`max_days`) applies to it.

## Where to find it

- **Segment conditions:** Marketing → Segments, condition group **Product Reviews** — shown only while the Product Reviews app is installed and active ([[segments-conditions]]).
- **Variable:** the campaign message editor's variables list ([[message-template-merge-tags]]).

## What the merchant can do here

A campaign is the **only** way the platform asks for reviews: it sends no automatic post-purchase review email. The `rate_orders_products` template in the customer email list is never sent ([[omnichannel-mails-labels]]).

- Build a segment of buyers who have not reviewed their order.
- Put `{$products_leave_feedback_url}` behind a button or link in the campaign message.
- Show the bought products with `{$triggered_products:N}`.

## Settings & fields

### The review conditions

| Condition (English label) | Matches | Offers the review link |
|---|---|---|
| Order → **Without product review** | Orders that are paid, completed or fulfilled and still have a product without a review from this subscriber, and for which no notification was sent yet. No operator or value. | Yes, plus `{$triggered_products:1}` |
| Subscriber → **Leave feedback** (with sub-conditions on rating, date, count, category, vendor) | Subscribers who left reviews | Yes, plus `{$triggered_products:1}` |
| Subscriber → **Is not leave feedback before/after period of time** | No review in, or before, the chosen period | Yes, plus `{$triggered_products:1}` |
| Subscriber → **Send link but not leave feedback for product** | Was sent a campaign notification in, or before, the period and left no review in it (verify) | No |

The Bulgarian admin labels come from the translations database; the server-side strings are "Без оставен отзив", "Оставил отзив за продукт" and "Изпратен линк, но не е оставил оценка за продукт" (verify on screen).

## Business rules

### The variable exists only with a review condition

`{$products_leave_feedback_url}` is offered in the variables list, and filled in at send time, **only when the campaign's segment contains one of the three review conditions above**. With any other segment (for example "has orders, last order shipped") it is not offered, and if it is in the message anyway, the send removes it like every unresolved variable: a button pointing to it gets an **empty link**. There is no variable holding a single product's URL; `{$triggered_products:N}` renders the first N matched products as blocks with name, image, price and a link to each product page.

### What the link opens

A storefront page listing the subscriber's bought products that have no review yet, from orders that are paid, completed or fulfilled, each with a review form; no sign-in is needed. When the segment's **Without product review** condition matched exactly one order for the subscriber, the page is limited to that order. A product drops off the list once reviewed; the link keeps working for the rest. Writing a review also clears the subscriber's "link sent" record.

### The review window applies, counted from the order date

A review sent from this page is refused once the order's creation date plus **Maximum period for leaving a review** (`max_days`, 1–365, default 7 — [[apps-product-review-settings]]) has passed, whichever "who may review" setting the store uses. The page still lists the product; the refusal comes on submit, with the message *"You have not purchased the product. Only users who have purchased the product can add reviews."* So a campaign sent later than `max_days` after the order brings refusals, and the window should be at least the campaign's delay.

## Related

- [[apps-product-review]] — hub.
- [[apps-product-review-settings]] — `max_days`.
- [[marketing-reviews-submission-rules]] — the other submission rules, including the product-page path.
- [[message-template-merge-tags]] — the campaign variables list.
- [[segments-conditions]] — segment condition catalogue.
- [[marketing-campaigns]] — campaigns.

## Open questions

- Exact Bulgarian labels of the review conditions and of the variable in the new admin (translations database).
- What exactly fills the record behind "Send link but not leave feedback for product" (verify).
