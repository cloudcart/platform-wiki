---
type: entity
nav_path: "Entity → Cart → Merge, bots & step reset"
aliases: ["Cart merge on login", "merge_cart", "Cart merged message", "Bot cart sentinel", "Crawler cart key", "Cart step reset", "Bounced to shipping step", "Сливане на количка при вход"]
tags: [entity, orders, cart, checkout, login, bots]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[cart]]. See the hub for the other aspects (data model, lifecycle, stock & pricing, recovery).

# Cart — Merge, bots & step reset

## Identity

This page covers three operational behaviours of the Cart entity that produce visible (sometimes confusing) merchant-facing symptoms: **merge-cart-on-login** (what happens to a guest cart when the customer signs in), the **bot / crawler sentinel key** (why crawler traffic doesn't pollute the abandoned-cart list), and the **checkout `step` reset** (why a customer who edits the cart mid-checkout gets bounced back to the shipping step). All three are platform behaviours the merchant does not directly trigger but may need explained from a support ticket.

## Aliases

- **Merge cart on login** (`merge_cart` setting) — combining a guest cart into the logged-in customer's saved cart.
- **"Your cart has been merged."** — the storefront message shown after a login-merge.
- **Bot sentinel key** — the hard-coded cart `key` assigned to bot / crawler requests.
- **Step reset** — `step` reverting to `authorize` on cart-modifying operations.

## Key Attributes

### Merge cart on login (sums quantities for the same variant)

When a logged-out customer with an anonymous cart logs in, the platform can merge that anonymous cart into the customer's existing logged-in cart (if any). Same-variant duplicates are merged by **summing quantities** (the existing line's quantity is incremented by the guest-cart item's quantity) — NOT replaced. Discount codes from the guest cart are preserved; the platform shows the message *"Your cart has been merged."* on the next page render.

Merge behaviour is governed by the `merge_cart` setting on [[settings-cart]] (default ON). Without the merge, the customer's anonymous cart is discarded on login and only the saved cart survives.

### Bot / crawler carts get a sentinel key

When the cart is loaded from a request the platform identifies as a bot / crawler, the cart's `key` is set to a hard-coded sentinel string (`the_client_is_a_bot_and_does_not_have_permission_to_access_this_page_please_contact_site_support`) instead of a random token. This prevents bot crawlers from accumulating real cart rows that would otherwise spam the abandoned-cart list. The sentinel cart never matches the abandoned filter; crawler-induced cart traffic does not appear anywhere in the admin UI.

### Checkout step resets on cart-modifying operations

The cart tracks the last checkout `step` the customer reached (`authorize`, `shippingAddress`, `billingAddress` — see [[cart-entity-model]]). When the cart is modified by certain operations (bulk cart update, shipping change, address change), the platform may reset `step` back to `authorize` (the start of checkout) — this clears the customer's pre-selected shipping method and shipping address.

The visible symptom for merchants is: a customer who edited the cart mid-checkout finds themselves bounced back to the shipping step instead of resuming at the payment step. This is expected behaviour — a cart edit can invalidate the previously-chosen shipping option, so the platform forces re-selection.

## Where it appears

- [[settings-cart]] — the `merge_cart` toggle (default ON).
- [[checkout-flow]] — where the `step` reset bounces the customer; where the merge message renders.
- [[storefront-cart]] — the cart drawer / page affected by a login-merge.
- [[orders-abandoned]] — the list that the bot sentinel keeps clean.
- [[customer]] — the logged-in customer whose saved cart receives the merge.

## Related

- [[cart]] — hub.
- [[customer]] — the account a guest cart merges into on login.
- [[settings-cart]] — the `merge_cart` setting.
- [[checkout-flow]] — the step machine that resets on cart edits.
- [[cart-vs-order-lifecycle]] — the cart-state context for these operations.

## Open Questions

None.
