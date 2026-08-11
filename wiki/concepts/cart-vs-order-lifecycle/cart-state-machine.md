---
type: concept
nav_path: "Concept → Cart vs Order lifecycle → Cart state machine"
aliases: ["Cart state machine", "Cart lifecycle states", "Active cart", "Cart identity states", "Anonymous cart", "Subscriber-identified cart", "Cart auto-touch", "Cart TTL", "Cart bot sentinel", "Жизнен цикъл на количка"]
tags: [cart, order, lifecycle, state-machine, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[cart-vs-order-lifecycle]]. See the hub for the other aspects (order state machine, handoff, abandonment, restore).

# Cart state machine

## Definition

A **[[cart|Cart]]** is the pre-purchase, fully-mutable record of what a customer has selected on the storefront. It is created when the first product is added, lives in the customer's browser session (persisted server-side with a session token / customer ID), and can be freely modified — add / remove / edit quantities, apply / remove discount codes, pick shipping, pick payment — without committing anything irrevocable.

A cart progresses through six internal states (Active, Abandoned, Recovered, Converted, Lost, Soft-deleted). Only **Abandoned** and **Recovered** carts are visible to the merchant (via [[orders-abandoned]]); Active and Lost have no admin-side surface. Active exits either on the customer's **Place order** click (→ Converted, see [[cart-to-order-handoff]]) or when `updated_at` ages past the abandoned threshold (→ Abandoned, see [[cart-abandonment]]).

## Scope

Covered: cart data shape (line items, customer association, token, shipping / payment, address, discounts, Cart Rules, attribution); the six internal cart states + transitions; the four identity states (anonymous, UUID-tracked, subscriber-identified, logged-in); cart auto-touch (10-min refresh) and the cart `key` bot sentinel; cart-record TTL (7 days) and post-Order soft-delete cascade; login / logout cart-merge gated by `merge_cart` on [[settings-cart]]; cart-side webhooks (`cart.created`, `cart.updated`).

Not covered here: the Place-order snapshot moment (see [[cart-to-order-handoff]]); order statuses after creation (see [[order-state-machine]]); abandoned threshold + recovery email pipeline (see [[cart-abandonment]]); restore-link semantics (see [[cart-restore]]).

## Contrasts

- **Cart vs Order**: a Cart is pre-purchase, fully mutable, customer-side. An [[order|Order]] is post-purchase, status-gated, merchant-side. See [[order-state-machine]].
- **Cart vs [[cart-rule|Cart Rule]]**: a Cart holds the customer's selection. A Cart Rule is a marketing rule that fires AFTER discounts at submit — it doesn't live on the Cart.
- **Anonymous vs identified cart**: an Anonymous cart has no `user_id`, no `subscriber_id`, no email channel — cannot receive abandoned-cart recovery. A Subscriber-identified or Logged-in cart has an addressable email — eligible (see [[cart-abandonment]]).
- **Active vs Recovered**: both have a recent `updated_at`. Recovered means the customer returned via a restore link — the cart keeps the `restore_source` attribution that flags the resulting order `abandoned = 1`. See [[cart-restore]].

## Where it applies

**Cart data shape.** The cart holds line items (product / variant + quantity + per-line price + per-line discount + selected options), customer association (`user_id`, `subscriber_id`, or NULL), a secret session token `key` for restore links + cross-device identification, pre-selected shipping (provider + type + courier-specific fields) and payment provider, shipping / billing address, applied discounts + matching Cart Rules, `updated_at` (drives the abandoned-cart detector), and attribution (campaign ID, UTM source, referrer).

The cart is **not visible** in the primary [[orders]] list — only placed orders appear there. The merchant sees carts indirectly via [[orders-abandoned]] (abandoned past the threshold) and [[analytics-abandoned-carts]] / [[analytics-abandoned-checkout]] (funnel analytics); when the customer eventually places an order, the order's `cart_id` points back.

**The six cart states.**

| State | What it means | Where merchant sees |
|-------|---------------|---------------------|
| **Active** | Customer browsing / editing; `updated_at` recent (< threshold). | NOT visible (live session). |
| **Abandoned** | ≥1 item, `updated_at` past threshold, no order placed, customer identifiable. | [[orders-abandoned]] list. |
| **Recovered** | Customer clicked the restore link from a recovery email; cart Active again. | [[orders-abandoned]] history (with `date_sent`). |
| **Converted** | An order was placed against this cart; still stored but not modifiable. If the cart is later deleted, the order's `cart_id` is auto-set to NULL. | NOT in [[orders-abandoned]]; the order is in [[orders]]. |
| **Lost** | Abandoned, recovery sent (or never qualified), aged out without conversion. | Eventually auto-deleted. |
| **Soft-deleted** | Manually deleted from [[orders-abandoned]] by the merchant. | Removed from the list. |

Transitions:

```
Active --[updated_at > threshold]--> Abandoned
Active --[customer clicks Place order]--> Converted (creates Order)

Abandoned --[merchant sends restore link]--> (email queued; cart stays in list)
Abandoned --[customer clicks restore link]--> Recovered (back to Active)
Abandoned --[customer never returns]--> Lost (auto-cleanup, eventually)

Recovered --[customer clicks Place order]--> Converted (Order, abandoned=1, restore_source set)
Recovered --[updated_at > threshold again]--> Abandoned (back to abandoned)
```

**Identity states.** A cart can be in four identity states, which determines which merchant-side surfaces show it:

| State | `user_id` | `subscriber_id` | Email known | Eligible for abandoned-cart recovery? | Shows in [[orders-abandoned]]? |
|-------|-----------|-----------------|-------------|---------------------------------------|-------------------------------|
| **Anonymous / guest** | NULL | NULL | NO | NO — no contact channel | NO |
| **UUID-tracked anonymous** | NULL | NULL, cookie UUID exists | NO | NO — UUID not addressable | NO |
| **Subscriber-identified** | NULL | set (newsletter, popup, etc.) | YES | YES — if Email channel subscribed + verified | YES |
| **Logged-in customer** | set | optional link | YES | YES — via account email | YES |

Anonymous → identified happens on login / register (`user_id` populated; cart-merge may run — below), on newsletter signup from a storefront popup / form (`subscriber_id` populated), or when the customer enters an email at the checkout shipping-address step (creates a subscriber if marketing consent is granted). UUID-tracked anonymous visitors (see [[subscriber-vs-customer]]) have a cookie UUID but no addressable email/phone — they cannot receive any email, including abandoned-cart recovery.

**Cart auto-touch — 10-minute refresh.** When a cart is loaded (page-view, AJAX) and its `updated_at` is older than **10 minutes** (platform `cart.autoupdate` config), the platform silently moves the timestamp forward. The abandoned threshold therefore measures meaningful activity, not idle revisits — a customer returning at the 55-minute mark resets `updated_at` to "now", pushing the abandoned trigger back another full interval.

**Cart `key` sentinel for bots.** On a crawler / bot request the platform issues a sentinel cart `key` of `the_client_is_a_bot_and_does_not_have_permission_to_access_this_page_please_contact_site_support` instead of a real random token. Bot crawlers don't accumulate real cart rows; this is invisible to merchants and explains why crawled traffic never appears in [[orders-abandoned]].

**Cart-record TTL — 7 days.** A cleanup job auto-deletes cart records whose `updated_at` is more than **7 days** old (hard-set by platform config, not exposed in [[settings-cart]]). A second pass soft-deletes carts that already produced an Order; a follow-up pass hard-deletes them, cascading child cart-item, shipping-quote, bundle, cross-sell, and option-storage rows away.

**Login / logout cart-merge — gated by `merge_cart`.** On login / register / social-login the merge fires if `merge_cart` on [[settings-cart]] is ON (default 1):

- **Anonymous → logged-in**: guest session cart and the customer's saved cart merge into ONE (items combined; saved-cart discount codes preserved); the old guest cart is deleted.
- **Logged-in A → logged-in B**: when A logs out and B logs in, the merge runs against B's saved cart + session cart. A's cart is NOT lost (stays on A's `user_id` row, reappears if A logs back in) — caution on shared browsers.
- **`merge_cart = 0`**: no item merging; session cart is re-associated to the new customer's `user_id`.

**Cart-side webhook events.** Fired via [[settings-hooks]]:

| Event | When |
|-------|------|
| `cart.created` | A new cart is created (first add to cart). |
| `cart.updated` | The cart is modified (item added / removed, quantity changed, etc.). |

Most merchants subscribe only to order events — `cart.*` traffic is high-volume and mainly useful for personalisation / abandoned-cart-bot integrations.

## Related

- [[cart-vs-order-lifecycle]] — hub.
- [[cart]] — Cart entity (data shape).
- [[cart-rule]] — Cart Rules; run AFTER discounts at submit.
- [[subscriber-vs-customer]] — UUID-tracked anonymous vs subscribers vs customers.
- [[customer]] — Customer entity; `user_id` association.
- [[settings-cart]] — `merge_cart`, `abandoned_remainder_interval`, cart caps.
- [[settings-hooks]] — `cart.*` webhook subscriptions.
- [[orders-abandoned]] — abandoned-cart admin list.
- [[analytics-abandoned-carts]] — abandoned-cart trends.
- [[analytics-abandoned-checkout]] — checkout funnel drop-off.

## Open Questions

None.
