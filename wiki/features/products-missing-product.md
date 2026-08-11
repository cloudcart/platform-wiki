---
type: feature
nav_path: "Products → Missing products"
route_name: products-missing
route_path: /admin/products/missing-product
aliases: ["Missing products", "Back in stock subscribers", "Expected products", "Очаквани продукти", "Уведоми ме за наличност"]
tags: [products, missing, subscribers, restock, insights]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 7
---
# Missing products

## Purpose

A read-only **insight page** showing products with **back-in-stock subscribers** — customers who clicked the "Notify me when in stock" button on a product whose status was set to "Show as subscribe for quantity" (see [[products-statuses]]). Each row shows how many subscribers are waiting, the current stock, and what action to take. It is the merchant's queue of **unmet customer demand** — use it to spot **restock priority**, since many subscribers means confirmed buying intent. Notification is NOT automatic; see the two button states below.

## Where to find it

Sidebar → Products → **Missing products**. Route `/admin/products/missing-product`.

## What the merchant can do here

- See all products with **at least one subscriber** waiting for restock, in a paginated table (columns under Settings & fields).
- Filter, search, and sort (by name, quantity, or subscribers count) via the standard table controls.
- Click the per-row action button — see the two states below.

### What the merchant CANNOT do here
- See WHICH specific customers are subscribed (privacy-preserving aggregate only).
- Reset / clear subscriber lists — they clear when the campaign is sent.

### Action button — two states, NO modal on this page

The per-row Actions column renders the same button used on [[products-favorite-products]]. No modal opens — both states are navigations, and which one shows depends on the Variant's current stock:

- **Variant quantity 0 / NULL (out of stock)** — ghost button *"Subscribers ({count})"* opens `/admin/subscribers?filters[subscribe_for_missing_product]={variant_id}` in a new tab — the merchant lands in [[marketing-subscribers]] filtered to that variant's pending subscribers. No inline popover.
- **Variant quantity > 0, or NULL = unlimited (restocked)** — primary button *"Create a campaign ({count})"* navigates to `/admin/campaigns` to build the back-in-stock email campaign by hand. The email is NOT auto-dispatched (see Business rules).

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

When a product's status falls into the "Show as subscribe for quantity" rule (from [[products-statuses]]), customers see a "Notify me when in stock" button on the storefront product page. Clicking it requires them to enter their email — the email is added to the product's subscriber list and they appear in the count here. The subscriber need not be a registered customer; guests can subscribe just by providing an email.

### Back-in-stock dispatch is merchant-triggered via a campaign (NOT automatic)

This is the single biggest gotcha on this page. When a subscribed Variant's stock rises above zero (or the merchant changes its tracking so the Variant becomes always-in-stock), the row flips its action button to **"Create a campaign"**. The merchant must click it and finish the campaign to send the back-in-stock email. There is NO background job that auto-detects "stock just became positive, fire emails" — the platform only marks the subscribers as eligible; the send is a deliberate marketing action through the segments + campaigns funnel. If the merchant restocks but never launches the campaign, the subscribers stay queued indefinitely. The "automatic email" workflow in older docs is incorrect.

Once a campaign sends, the platform records each subscriber-notification pair in `subscriber_notifications_send` — and the page's `doesntHave('notifications')` filter excludes those rows. So after the campaign, the row drops off the page.

### Read-only customer privacy

The merchant sees the count but not the individual subscriber emails. This is by design — subscribers may include guests whose emails were collected without account creation, and exposing them would create privacy/GDPR risk. To target subscribers with broader marketing, the merchant uses the campaigns / segments feature, which queries subscriber relationships at scale without exposing individual identities.

### Email content

The back-in-stock email is templated through the platform's transactional email system, customised via the email-template feature (separate from this page).

### Permission

This page sits under the standard products permission scope. Viewing the list is purely read — it triggers no queue.

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

The `subscriber_id` foreign key points at the platform's general Subscribers entity — the same table that holds newsletter and abandoned-cart subscribers. A subscriber can be a registered customer OR a guest whose email was collected at the back-in-stock prompt without account creation.

### Updated_at acts as created_at

The table has no separate created_at column — `updated_at` holds the time the subscription was created (bumped only on re-subscribe), so it is effectively a creation timestamp.

### Page list rule: subscribers grouped per Variant, not per Product

The grid is grouped by `variant_id` — so a Product with two out-of-stock Variants that both have subscribers appears as **two rows**, not one. The Name column adds the Parameter labels (`Colour: Red / Size: Large`) as a subtitle so the merchant can distinguish them.

### Variant `quantity = NULL` reads as infinite stock (∞)

If a Variant's quantity is NULL (the storefront treats this as unlimited stock — common for digital goods with `tracking = no`), the Quantity column renders the infinity symbol `∞`. A NULL-quantity row is also treated as "restocked", so the action button flips to "Create a campaign" — once tracking is turned off on a Variant, any pending subscribers immediately become campaign-eligible.

### Hidden product / Variant deletion silently clears subscribers

Deleting a Product or a specific Variant cascades (`ON DELETE CASCADE`) and **purges all pending subscriptions for that record**. No notification, no warning — the row simply vanishes. To preserve the demand record for future planning, deactivate instead of delete.

### Re-subscription resets the notification flag

When an already-notified subscriber clicks "Notify me when in stock" again (e.g. they got the email, didn't buy, the product ran out again), the platform deletes their prior `subscriber_notifications_send` row — so they re-enter the waiting queue on the same record. Only `updated_at` is bumped on re-subscribe.

### What this page does NOT do

- It does NOT include subscriber-less out-of-stock products. Only Variants with at least one outstanding subscriber appear.
- It does NOT support restock from this screen — the merchant clicks the product name or goes to [[products-inventory]] to change `quantity`.

## Open questions
