---
type: feature
nav_path: "Products → Missing products"
route_name: products-missing
route_path: /admin/products/missing-product
aliases: ["Missing products", "Back in stock subscribers", "Expected products", "Очаквани продукти", "Уведоми ме за наличност"]
tags: [products, missing, subscribers, restock, insights]
plan_gates: []
created: 2026-05-21
updated: 2026-11-09
source_count: 8
---
# Missing products

## Purpose

A read-only **insight page** showing products with **back-in-stock subscribers** — customers who clicked the "Notify me when in stock" button on a product whose status was set to "Show as subscribe for quantity" (see [[products-statuses]]). Each row shows how many subscribers are waiting, the current stock, and what action to take: a queue of **unmet demand** for **restock priority**. Notification is NOT automatic; see the two button states below.

## Where to find it

Sidebar → Products → **Missing products**. Route `/admin/products/missing-product`.

## What the merchant can do here

- See all products with **at least one subscriber** waiting for restock, in a paginated table (columns under Settings & fields).
- Filter, search, and sort (by name, quantity, or subscribers count) via the standard table controls.
- Click the per-row action button — see the two states below.

### What the merchant CANNOT do here
- See the subscribers on this page itself: the **Subscribers** button opens them in [[marketing-subscribers]].
- Reset / clear subscriber lists — they clear when the campaign is sent.

### Action button — two states, NO modal on this page

The per-row Actions column renders the same button used on [[products-favorite-products]]. No modal opens — both states are navigations, and which one shows depends on the Variant's current stock:

- **Variant quantity 0 / NULL (out of stock)** — ghost button *"Subscribers ({count})"* opens `/admin/subscribers?filters[subscribe_for_missing_product]={variant_id}` in a new tab — the merchant lands in [[marketing-subscribers]] filtered to that variant's pending subscribers. No inline popover.
- **Variant quantity > 0, or NULL = unlimited (restocked)** — primary button *"Create a campaign ({count})"* opens the new-campaign dialog; choosing a Regular campaign creates a draft with that variant's back-in-stock segment already picked (an existing one is reused, otherwise a One-time segment is created). Nothing is sent automatically (see Business rules).

## Settings & fields

### List columns

| Column | Notes |
|--------|-------|
| **Name** | Product name + thumbnail. Click navigates to the product editor in [[products-products]]. |
| **Quantity** | Current stock. For a missing product this is typically 0 or below the merchant's threshold. |
| **Subscribers** | Count of distinct customers waiting for restock notification. |
| **(actions)** | Per-row action button — two states described above. |

## Business rules

### Subscribers are collected automatically when products show the subscribe button

When a product's status falls into the "Show as subscribe for quantity" rule (from [[products-statuses]]), the storefront shows a "Notify me when in stock" button; the visitor leaves an email (guests included) and appears in the count here. The form opens as a popup, or as its own page when its URL is opened directly; there is no inline variant ([[storefront-notifications]]).

### Back-in-stock dispatch is merchant-triggered via a campaign (NOT automatic)

This is the single biggest gotcha on this page. When a subscribed Variant's stock rises above zero (or the merchant changes its tracking so the Variant becomes always-in-stock), the row flips its action button to **"Create a campaign"**. The merchant must click it and finish the campaign to send the back-in-stock email. There is NO background job that auto-detects "stock just became positive, fire emails" — the platform only marks the subscribers as eligible; the send is a deliberate marketing action through the segments + campaigns funnel. If the merchant restocks but never launches the campaign, the subscribers stay queued indefinitely. The "automatic email" workflow in older docs is incorrect.

To notify on every restock without a click, build an **Automated** campaign (trigger *Gets in segment*) on an Automated segment with the condition *"Subscribed for product availability, and which are already available"*. Automated segments are re-evaluated every 5 minutes ([[segments-rebuild-mechanics]]), so each restocked variant's subscribers then get the message.

Once a campaign sends, the platform records each subscriber-notification pair in `subscriber_notifications_send` — and the page's `doesntHave('notifications')` filter excludes those rows. So after the campaign, the row drops off the page.

### Signups are verified; marketing consent depends on the popup

A back-in-stock signup stores the email as **verified**, with no confirmation email. **Marketing consent** is set only when the GDPR app is active and the visitor ticks its marketing consent in the popup; otherwise a new address is stored without it (an address the store already had keeps its consent). Campaigns skip an address without marketing consent (log *"Not accepts marketing"*), and the back-in-stock campaign is no exception.

### Message content

The message is the campaign's own, on whichever channel the campaign uses. There is no back-in-stock notification template among the [[marketing-omnichannel-mails-list|Email notifications]].

## Related

- [[products]] — parent hub.
- [[products-products]] — clicking a product name navigates to its editor.
- [[products-favorite-products]] — sibling insight page; tracks customer wishlist items (distinct from restock subscribers).
- [[products-statuses]] — the "Show as subscribe for quantity" status rule is what enables the back-in-stock subscribe button on the storefront.
- [[products-inventory]] — restocking happens here; a positive quantity makes the row campaign-eligible.
- [[customer]] — subscribers can be registered customers OR guests.
- [[product]] — entity page.

## How it works (verified against backend)

### Subscriptions are variant-specific

Per the `subscribe_for_missing_product` table fields (`subscriber_id`, `product_id`, `variant_id`): each subscription is tied to a SPECIFIC variant, not the product as a whole. A customer subscribing to "Red Large" is tracked separately from "Blue Small" — when the merchant restocks "Red Large" but "Blue Small" stays at 0, only the Red-Large subscribers become campaign-eligible.

### Subscribers are merged with the Subscribers table

Each subscription belongs to a general Subscriber — a registered customer or a guest who only left an email.

### Page list rule: subscribers grouped per Variant, not per Product

The grid is grouped by `variant_id` — so a Product with two out-of-stock Variants that both have subscribers appears as **two rows**, not one. The Name column adds the Parameter labels (`Colour: Red / Size: Large`) as a subtitle so the merchant can distinguish them.

### Variant `quantity = NULL` reads as infinite stock (∞)

If a Variant's quantity is NULL (the storefront treats this as unlimited stock — common for digital goods with `tracking = no`), the Quantity column renders the infinity symbol `∞`. A NULL-quantity row is also treated as "restocked", so the action button flips to "Create a campaign" — once tracking is turned off on a Variant, any pending subscribers immediately become campaign-eligible.

### A hidden product still notifies its subscribers

Visibility and availability notifications are independent: a hidden, in-stock product still fills its back-in-stock segment ([[segments-conditions]]).

### Product / Variant deletion silently clears subscribers

Deleting a Product or a specific Variant **purges all pending subscriptions for that record**, without a warning. To preserve the demand record for future planning, deactivate instead of delete.

### Re-subscription resets the notification flag

When an already-notified subscriber clicks "Notify me when in stock" again (e.g. they got the email, didn't buy, the product ran out again), the platform deletes their prior `subscriber_notifications_send` row — so they re-enter the waiting queue on the same record. Only `updated_at` is bumped on re-subscribe.

### What this page does NOT do

- It does NOT include subscriber-less out-of-stock products. Only Variants with at least one outstanding subscriber appear.
- It does NOT restock: change `quantity` in [[products-inventory]].

## Open questions
