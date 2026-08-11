---
type: concept
nav_path: "Concept → Storefront known issues → Cart lifecycle"
aliases: ["Storefront cart lifecycle issues", "Cart merge issues", "Cart cookie lifetime", "Abandoned cart restore", "Thank-you page refresh"]
tags: [storefront, cart, checkout, abandoned-cart, issues]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[storefront-known-issues]]. See the hub for the other aspects (framework, inventory, discount codes, listing / search, display + customer, pending bugs).

# Storefront issues — cart lifecycle

## Definition

The cart-lifecycle entries cover behaviours around **how the cart persists between sessions and merges between identities** — the anonymous-to-logged-in handoff, the guest-cookie expiry window, the abandoned-cart restore semantic, and the thank-you-page refresh safety. Every entry below is **By design** and ultimately governed by [[checkout-flow]] and [[abandoned-cart-recovery]].

Four catalogue entries are in this group: anonymous cart merging into logged-in cart on sign-in, the 24-hour guest-cookie sliding lifetime, abandoned-cart restore merging items into the current cart (not replacing it), and the thank-you-page-refresh not re-charging.

## Scope

Covered:

- The four By-design entries that have generated support tickets around cart persistence + cart merge + thank-you page.
- Cross-reference to [[checkout-flow]] + [[abandoned-cart-recovery]] for the underlying model.

Not covered:

- Cart item-level changes (price recalculation, discount recalculation on cart-line update) — see [[cart-vs-order-lifecycle]].
- Checkout-step jumping by URL — see [[storefront-issue-pending-bugs]] entry 28.
- The cart drawer's cross-sell block — see [[storefront-issue-pending-bugs]] entry 24.

## Contrasts

- **Merge on sign-in vs drop on sign-in** — controlled by the **Merge cart** (`merge_cart`) setting in [[settings-cart]]. When ON, anonymous-cart lines are added to the logged-in cart at sign-in. When OFF, the anonymous cart is dropped silently — the customer sees only the cart attached to their account. Merchants who enable it expect "no surprise items"; merchants who disable it expect "carry-over". The same symptom looks like a bug to either side.
- **24-hour guest sliding lifetime vs permanent guest cart** — the guest-cart pointer cookie (`ccchc`) has a 24-hour sliding window, refreshed on every interaction. After 24h of inactivity the cookie expires and the visitor gets a new cart. This is intentional — long-lived guest carts inflate the database with abandoned junk + interfere with the abandoned-cart recovery flow.
- **Abandoned-cart restore: merge vs replace** — the recovery link does NOT substitute the customer's current cart; it **merges** the abandoned items into whatever cart the customer has at the time. Discount code + shipping address + billing address are also restored if the abandoned cart belonged to the same logged-in customer. Merchants sometimes report this as a bug ("the abandoned-cart link added items I didn't expect") — it is the documented behaviour.
- **Thank-you page refresh: idempotent vs double-charge** — refreshing the thank-you page does NOT re-charge the customer. The return URL is keyed by a payment hash; the payment record is single-use + already completed at the point the return page renders. Refreshing reloads the same hash; the payment provider does not re-charge a closed transaction.

## Where it applies

The four catalogue entries:

| # | Behaviour | Affected page(s) | Category | What to tell the merchant |
|---|---|---|---|---|
| 10 | Anonymous cart merges into the logged-in cart on sign-in (or doesn't, depending on the store) | Cart, checkout, customer login | By design | Controlled by the **Merge cart** (`merge_cart`) setting in [[settings-cart]]. When ON, anonymous-cart lines are added to the logged-in cart at sign-in. When OFF, the anonymous cart is dropped. See [[checkout-flow]]. |
| 11 | Cart disappears after 24 hours of inactivity for guest visitors | Cart, product detail | By design | The `ccchc` cookie that points at a guest cart has a **24-hour** sliding lifetime, refreshed on every interaction. After 24h of inactivity the cookie expires and the visitor gets a new cart. Logged-in customers' carts persist by Customer ID. See [[checkout-flow]]. |
| 12 | An abandoned-cart recovery link merges the abandoned items into the current cart (instead of replacing it) | Cart, checkout | By design | The recovery handler merges into the current cart row — items from the abandoned cart are added, not substituted. Discount code + shipping address + billing address are also restored if the abandoned cart belonged to the same logged-in customer. See [[abandoned-cart-recovery]]. |
| 13 | Refreshing the thank-you page does NOT re-charge the customer | Checkout return, order confirmation | By design | The return URL is keyed by `payment_hash` — the payment record is single-use + already-completed at the point the return page renders. Refreshing reloads the same hash; the payment provider doesn't re-charge a closed transaction. See [[checkout-flow]]. |

### Support-agent quick path

All four are **By design**. The agent's response template:

- *"My cart disappeared after a day"* → entry 11; point at the 24h cookie + the logged-in alternative.
- *"My customer signed in and their cart was wrong"* → entry 10; check the merchant's `merge_cart` setting.
- *"My abandoned-cart link added items the customer didn't want"* → entry 12; explain the merge semantic + the discount + address restore.
- *"My customer says they refreshed and got charged twice"* → entry 13; this CANNOT be a double-charge from refreshing — investigate the payment provider's logs (a separate failed retry, manual capture, or a duplicate order from the customer hitting Submit twice on the previous step).

## Related

- [[storefront-known-issues]] — hub.
- [[storefront-issue-framework]] — the four categories.
- [[checkout-flow]] — concept page that governs entries 10, 11, 13.
- [[abandoned-cart-recovery]] — concept page that governs entry 12.
- [[settings-cart]] — `merge_cart` setting.
- [[cart-vs-order-lifecycle]] — full lifecycle model.

## Open Questions

- What is the precise behaviour when a merchant disables the `merge_cart` setting AND a logged-in customer signs in with items in their anonymous cart — are those items dropped silently, or surfaced as a one-time prompt? (verify.)
- Does the 24-hour cookie lifetime carry over across devices, or is it strictly per-browser? (currently per-browser by virtue of being a cookie — verify if any cross-device handoff is possible via the account-restore flow.)
