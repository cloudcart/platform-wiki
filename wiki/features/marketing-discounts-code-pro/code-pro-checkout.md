---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Checkout behaviour"
route_name: discounts-code_pro-edit
route_path: /admin/marketing/discounts/code-pro/:id/:codeId
aliases: ["Code PRO checkout", "Code PRO active scope", "Code PRO uses counter", "Code PRO replacement semantics", "Code PRO lookup"]
tags: [marketing, discounts, code-pro, checkout, redemption]
plan_gates: ["discount-code-pro"]
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[marketing-discounts-code-pro]]. See the hub for the other aspects (overview, form, fields, business rules, endpoints).

# Code PRO — checkout active-scope & uses counter

## Purpose

This page documents how a Code PRO code is **evaluated at checkout** — the active-scope filter, the case-insensitive lookup, the single-Code-PRO-per-cart replacement rule, and how the `uses` counter is recomputed via an async job. Use it when answering *"why is my customer getting 'invalid code' when the code looks valid?"*, *"can a customer use two Code PRO codes together?"*, or *"why is the Uses counter wrong / lagging?"*.

For admin-panel save behaviour see [[code-pro-business-rules]]. For the field-level definitions see [[code-pro-fields]].

## Where to find it

This behaviour applies on the storefront checkout flow whenever a customer types a code into the discount-code field. The active-scope evaluation runs server-side at the cart-discount-lookup step (see [[cart-vs-order-lifecycle]]). The `uses` counter is recounted when the order's status changes (see [[settings-statuses]]).

## What the merchant can do here

There is no admin-panel surface for this aspect — the rules are runtime behaviour. The merchant configures the inputs via [[code-pro-form]] / [[code-pro-fields]] and the checkout flow applies them.

## Settings & fields

The runtime active-scope check reads the following code-row fields (see [[code-pro-fields]] for the form keys):

- `active`.
- `date_start`, `date_end`.
- `max_uses`, `uses`.
- `customer_groups[]` (via the join table).
- `geo_zone_id`.

And the campaign's own `active` flag, dates and usage limit.

## Business rules

### Active-scope check at checkout

A Code PRO code passes the active-scope filter only when ALL of:

- The **parent discount** is `active = 1`, within its own dates and under its own usage limit.
- `active = 1` on the code row.
- `date_start <= today` (store timezone).
- `date_end >= today OR date_end IS NULL`.
- `max_uses > uses OR max_uses IS NULL`.
- Customer matches the code's `customer_groups` association (or the code has no group restriction, which means it accepts the cart's customer group or the guest group).
- Cart's shipping address falls within the code's `geo_zone_id` (or `geo_zone_id IS NULL` for "All regions").

Failing any check causes the code to be skipped — the customer sees a generic *"Invalid discount code"* message at checkout (the storefront does **not** distinguish between "expired", "exhausted", "region mismatch", or "group mismatch"). This is intentional: it avoids leaking campaign details to competitors / scrapers.

### Code lookup is case-insensitive

The cart's checkout flow matches the typed code against the stored value in a **case-insensitive** manner — the customer can type `summer25`, `Summer25`, or `SUMMER25` and they all match the same code row. The merchant doesn't need to advertise the code in a specific case; whatever case the customer types will work.

### Cart can hold ONE Code PRO code at a time (replacement semantics)

The customer's cart `discount_code` column holds **one** stand-alone code value (Code PRO or regular Promo). Typing a second code at checkout **replaces** the first — the platform does not stack two Code PRO codes simultaneously.

To combine several codes in one cart, the merchant must use Container codes ([[marketing-discounts-codes]]) where the cart's `discount_container_code` array stores multiple Container code strings.

This is the most-misstated runtime rule about Code PRO. Container codes (different table) can stack; Code PRO codes cannot.

### Per-customer cap (`maxused_user`)

The per-customer limit is compared with all of that customer's uses under the whole Code PRO campaign, not this code alone, in counted-status orders. When the limit is reached, the customer sees *"You have used this discount code the maximum number of times"* and the cart's discount-code field is cleared.

### Uses counter — incremented only on counted statuses, via async recompute

The `uses` column on each Code PRO code counts only orders that reach one of the store's **counted statuses** (default `paid`, `completed`, `fulfilled` — configurable via the `discounts_used_statuses` setting; see [[settings-statuses]]). Pending orders don't count yet; cancelled / refunded orders never count.

When the status of an order using a Code PRO code changes, the platform **recomputes** the `uses` counter — for both the per-code row and the parent Code PRO discount's aggregated count — at once, and again about 10 seconds later as a safety net.

The recompute counts **ALL counted-status orders, not a delta** — so the counter automatically self-corrects if an order later moves to / from a counted status (e.g., a cancel / refund causes the counter to decrement, freeing the code back up; a recovered cancellation re-counts the order). The counter on the per-code row is the source of truth at checkout, with `max_uses > uses` enforced in the active-scope query.

**Implication for support tickets**: a merchant complaining "the Uses counter shows N but I see N+1 orders" should look at the order statuses — orders not yet in a counted status won't count.

### Cancel / refund frees the code back up

When a previously-counted order moves OUT of a counted status (cancellation, refund, void, chargeback), the recompute decrements the `uses` counter. If the code was previously exhausted (`uses >= max_uses`), it becomes redeemable again automatically — **no admin action needed**.

This is symmetric with the [[inventory-restock]] flow on the stock side.

## How it works

The active-scope evaluation lives in the cart-discount-lookup pipeline. Each order-status change recounts `uses` at once and queues a second recount about 10 seconds later as a safety net.

The same active-scope rules apply whether the code comes from a customer typing into the cart UI or from a campaign template substituting `{triggered_dynamic_discount}` (see [[marketing-campaigns]]) — the lookup pipeline doesn't care about the entry surface.

## Related

- [[marketing-discounts-code-pro]] — hub.
- [[code-pro-fields]] — fields the active-scope check reads.
- [[code-pro-business-rules]] — admin-panel save flow that produces those fields.
- [[code-pro-overview]] — store-wide uniqueness on `discounts_code_pro.code`.
- [[marketing-discounts-codes]] — Container codes (the alternative for stacking multiple codes in one cart).
- [[settings-statuses]] — `discounts_used_statuses` setting drives the counted-status set.
- [[cart-vs-order-lifecycle]] — cart-stage vs order-stage handoff that the lookup runs in.
- [[marketing-campaigns]] — `{triggered_dynamic_discount}` replacement that issues dynamic Code PRO codes.
- [[marketing-segments]] — segment conditions referencing Code PRO usage.
- [[geo-zone]] — region restriction reads this entity.
- [[customers-custom-groups]] — customer-group restriction reads this entity.

## Open questions

No outstanding questions.
