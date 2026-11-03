---
type: concept
nav_path: "Concept → Headless storefronts → Offers"
aliases: ["Headless cross-sell", "Headless up-sell", "Storefront API offers", "upSellOffer", "crossSellOffer", "crossSellId", "upSellTriggerVariantId", "cartCrossSellApply", "cartOfferViewed", "cartOfferDismissed", "OfferHistoryInput", "Кръстосани продажби Nitrogen", "Допродажби витрина", "Оферти в количката"]
tags: [nitrogen, headless, storefront-api, cross-sell, up-sell, concepts]
plan_gates: ["cross_sells"]
created: 2026-11-03
updated: 2026-11-03
source_count: 3
---

> Part of [[headless-storefront]].

# Headless — cross-sell and up-sell offers

## Definition

The merchant's offers from the [[apps-up-cross-sell]] app reach a Nitrogen storefront through the Storefront API. The app's own code chooses and prices them, so an offer behaves as on the classic storefront. The merchant creates them only in the admin ([[marketing-cross-sell]], [[marketing-up-sell-list]]). The storefront shows them and takes them. With the app not active, every offer field answers null.

## Scope

Covered:

- Reading and taking an up-sell.
- Reading and taking a cross-sell, by its display.
- `offerHistory`, and why it decides whether an add can bring offers.
- Counting views and dismissals.

Not covered:

- Building offers — see [[marketing-cross-sell]] and [[marketing-up-sell-diagram]].
- The types and their fields, which introspection answers.
- Cart rules in general — see [[headless-cart-rules]].

## Contrasts

- **Up-sell vs cross-sell** — an up-sell proposes a better variant instead of the one being added. A cross-sell offers more products at the offer's price.
- **`POPUP` vs `ADD_TO_CART`** — a `POPUP` cross-sell is shown and the buyer picks; an `ADD_TO_CART` one puts its products into the cart for them.
- **Offers vs [[apps-cart-rules]]** — cart rules are applied by the cart itself. Offers appear only when the storefront asks for them and sends `offerHistory`.

## Where it applies

### `offerHistory` decides

The store picks an offer only for a mutation given `offerHistory`, even an empty one. Without it the add changes nothing else: mobile apps and older storefronts get the cart they asked for, with no surprise products. This applies to `cartCreate`, `cartLinesAdd` and, after a quantity change, `cartLinesUpdate`. The picked offer comes back as the payload's `crossSellOffer`.

`OfferHistoryInput` is what the buyer has seen and dismissed. The storefront keeps it, in a cookie for example, since the API keeps nothing per buyer. The merchant's view limit and dismissals count through it. Up to 100 entries of each list are read; offers no longer in the store are skipped.

### Up-sell

`upSellOffer(variantId, quantity, cartId)` is read **before** adding the variant, so the buyer can choose between the two. It answers null when:

- there is no up-sell, or the app is not active;
- the cart already holds the offer variant;
- the merchant has more than one active up-sell for that variant, since the store could price by either.

To take it, add the offer variant with `upSellTriggerVariantId` set to the trigger variant. Otherwise the line goes in at its own price with a warning. See [[upsell-list-storefront-firing]] for the classic storefront's flow.

### Cross-sell

`Cart.crossSellOffer(history)` is the offer on the cart page, and `CartPayload.crossSellOffer` the one after an add. Either is picked at random among those that apply, so two reads can differ: show the one read.

| Display | How it is taken |
|---|---|
| `POPUP` | The buyer picks products, each added with `crossSellId` set to the offer's id. |
| `ADD_TO_CART`, after an add | The mutation has already added its products. Show them if `showAddedProducts` says so. |
| `ADD_TO_CART`, on the cart page | `cartCrossSellApply(cartId, offerId, offerHistory)` adds them. |

`crossSellId` takes only `POPUP` offers of the add-to-cart and cart events. When the offer is not active, is not one the API shows, does not apply to the line, or the cart already holds this variant without it, the line is added at its own price with a warning. A checkout or after-order offer cannot be taken this way.

`cartCrossSellApply` adds nothing, with a warning, when the cart no longer meets the offer or all its products are already in the cart: *"This offer does not apply to the cart now, or the offer has nothing left to add, so nothing was added."*

An offer may lead to another: `nextIfAccepted` and `nextIfDeclined`.

### Counting views and dismissals

`cartOfferViewed` and `cartOfferDismissed` count in the merchant's statistics (see [[cross-sell-view-tracking]]). The storefront also adds the view or dismissal to its history.

- A visitor may count 30 of each a minute. Past that: `counted: false`, code `THROTTLED`, nothing counted.
- They take only offers the API shows: a cross-sell for the cart or an add, one another offer leads to, any up-sell. Any other is refused: *"No active offer has this id."*, code `INVALID`.
- Without the app: *"The store has no Up/Cross-sell app."*, code `APP_NOT_ACTIVE`.

### Lines of an offer

An offer's line follows the offer:

- **Fixed quantity.** A free gift from an offer, or an up-sell for a set quantity, may not change quantity (`CartLine.allowQuantityChange` is false). `cartLinesUpdate` refuses with `INVALID_QUANTITY`: *"This line's quantity is set by its offer or bundle, so it cannot change; the line can be removed."* Adding the same variant again is refused: *"The cart holds this variant through an offer that sets its quantity, so no more can be added to it."* Removing the line works.
- **Swapping the variant.** `cartLinesUpdate` with another `merchandiseId` takes the line out of the offers not made for it, at its own price, with a warning. This applies to an up-sell always, to a cross-sell the line came through always, and to a cross-sell the line triggers when its product changes.

A discount from an offer appears in `Cart.discountApplications` with the source `UPSELL` or `CROSS_SELL` (see [[headless-cart-rules]]).

## Related

- [[headless-storefront]] — hub.
- [[headless-cart-rules]] — warnings and refusals on cart mutations.
- [[headless-storefront-limits]] — the per-visitor limits.
- [[marketing-cross-sell]] — building cross-sell offers.
- [[marketing-up-sell-list]] — building up-sell offers.
- [[upsell-list-storefront-firing]] — the classic storefront's up-sell flow.
- [[cross-sell-vs-cart-rules]] — the engine compared with cart rules.
- [[apps-up-cross-sell]] — the app behind both.

## Open Questions

_None._
