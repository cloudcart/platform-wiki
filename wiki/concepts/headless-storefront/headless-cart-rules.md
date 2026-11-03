---
type: concept
nav_path: "Concept → Headless storefronts → Cart rules"
aliases: ["Headless cart", "Storefront API cart rules", "CartWarning", "INPUT_IGNORED", "DISCOUNT_CODE_NOT_HONOURED", "MISSING_CUSTOMIZATION", "INVALID_QUANTITY", "cartCustomizationFileUpload", "cartLinesAdd", "cartLinesUpdate", "Правила на количката Nitrogen", "Количка Storefront API", "Качване на файл в количката"]
tags: [nitrogen, headless, storefront-api, cart, customizations, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

> Part of [[headless-storefront]].

# Headless — cart rules

## Definition

What the Storefront API's cart mutations refuse, what they warn about, and how they decide who the buyer is. The cart is the platform's, so its pricing and limits are the classic storefront's. Two lists answer every mutation: `userErrors` for what failed, `warnings` for what succeeded without applying something.

## Scope

Covered:

- Warnings, required and measured customizations, swaps, quantity, the 50-line rule, attributes, bundles.
- Uploading a customization's file.
- Who the buyer is, and discounts on the cart.

Not covered:

- Limits on lists and pages — see [[headless-storefront-limits]].
- Offers — see [[headless-offers]].
- Placing the order — see [[headless-checkout-submit]].

## Contrasts

- **`userErrors` vs `warnings`** — a user error means that input failed. A warning means the mutation completed, and tells what it did not apply. The client decides whether the buyer needs to know.
- **`cartLinesAdd` vs `cartBundleAdd`** — a bundle is a group, not a line: added whole, or not at all.

## Where it applies

### Warnings

`CartPayload`, `CartPaymentSessionPayload` and `CartSubmitPayload` carry `warnings`, each with `code`, `message`, `target` and `field`.

`INPUT_IGNORED` means something sent had no effect:

- a cart note, or the buyer's `countryCode`;
- on a signed-in cart: the e-mail, the names, and a phone differing from the customer's;
- line ids not on the cart, or attributes with an empty key;
- a credit plan or down payment with a non-credit method;
- `searchedAt` without `searchTerm`, or a delivery slot the service lacks;
- dropped customizations, or a cross-sell with no offer;
- parts of `cartCreate` not reached after a failure.

`DISCOUNT_CODE_NOT_HONOURED` means the cart dropped a code on its own: its conditions no longer hold, such as a quantity under its threshold, or a product with a discount the code may not be combined with was added. It names the cart, no field, once per code: *"The discount code {code} no longer applies to this cart, so it was removed."* `cartDiscountCodesUpdate` does not report what the buyer replaced.

### Customizations

`cartLinesAdd`, `cartCreate` and each `cartBundleAdd` item refuse the first unanswered required customization: the product's, its category path's, its vendor's or its smart collections'. The code is `MISSING_CUSTOMIZATION` and the message comes from the store's language: en *"Please choose:attribute."*, bg *"Не сте избрали:attribute."*. Not answers: a blank value, a list with a blank entry, an empty list. Without the Product Options app none is asked ([[apps-product-options-settings-new]]).

Measured types: `weight` and `length` take one number above zero; `square` takes exactly two, or both blank for no answer. Anything else refuses the line with `INVALID`.

### Swapping a line

`cartLinesUpdate` with `merchandiseId`:

- A variant of the same product swaps, keeping its answers.
- Onto another product: refused with `MISSING_CUSTOMIZATION` if that product's required ones are not among the line's answers, and with `INVALID` if the line answers one that product does not ask (*"This line has customizations of its own product, so it cannot be swapped onto another one: remove it and add the new one."*).
- A bundle's item: *"This line is part of a bundle, so its product is chosen with the bundle and cannot be swapped."*

### Quantity

- Below 1 on an add: `INVALID_QUANTITY` on that line (*"The quantity must be at least 1."*), and the other lines are added.
- A bundle below 1 is refused.
- `cartLinesUpdate` at 0 removes the line.
- A bundle's item, and a line fixed by an offer, keep their quantity: *"This line's quantity is set by its offer or bundle, so it cannot change; the line can be removed."*
- The merchant's `cart_max_products` and `cart_max_quantity` apply on an add and on a raised quantity ([[settings-cart-limits-and-decrement]]). Lowering is always allowed.

### The 50-line rule

The same as the classic storefront's: at 50 lines or more, no bundle goes in, and no new line of a variant the cart already holds (other customizations, an up-sell). Distinct variants are not capped by this rule. The message is en *"You have reached 50 cart items."*, bg *"Достигнахте лимит от 50 артикули в количката."*.

### Attributes and bundles

- **Attributes** are kept apart from the store's own data on the cart, so a key never changes pricing. A key over 245 characters is skipped with a warning.
- **Bundles** are added whole or not at all (*"This bundle has {n} products; {m} were chosen."*). A bundle's own variant is refused on `cartLinesAdd`, `cartCreate` and the `line` of `fastOrderSubmit`.

### A customization's file

For a `file` customization, the file goes first, the line second:

1. `cartCustomizationFileUpload(customizationId, file)`, sent as `multipart/form-data` by the GraphQL multipart request specification. The file is checked on its contents.
2. Send the returned `file.handle` as the customization's `value`.

`ProductCustomization.fileUpload` gives `maxFileSize` (bytes, 0 for no limit), `allowedExtensions` and `allowedMimeTypes`. These are the store's limits, the same for every file customization.

- The codes are `FILE_TOO_LARGE`, `FILE_TYPE_NOT_ALLOWED`, and `THROTTLED` past 20 uploads a minute per visitor.
- A handle is single use, bound to the store and the customization, and valid for 24 hours (`expiresAt`). An expired, used or foreign handle refuses the line with `INVALID`: upload again.
- A line with a file is checked for stock and limits before the file moves, so a refusal keeps the handle. A refused bundle discards its files and asks for them again.

### Who the buyer is

- A guest who types a registered customer's e-mail stays a guest. `cart.buyerIdentity.customer` is returned only to a request authenticated as that customer, so the guest does not see saved addresses. `email` still comes back.
- The account's custom fields and `alternative_phone` are written only by its authenticated owner: a token on this call, or a customer-bound request. A guest's own record is written.
- The order still attaches to that customer by e-mail at submit.

See [[headless-customer-accounts]].

### Discounts on the cart

`Cart.discountApplications` lists every discount applied, each once, with the sources `CODE`, `UPSELL`, `CROSS_SELL`, `BUNDLE`, `CART_RULE`, `PRODUCT`, `QUANTITY`, `ORDER_THRESHOLD`, `COUNTDOWN`, `PAYMENT_METHOD` and `SELLING_PLAN`. See [[discount-stacking]] for how they combine.

- A row of 0, such as a countdown whose pop-up was not shown, is skipped.
- Free shipping appears as a `SHIPPING_LINE` allocation of 100%.
- A cart discount keeps its order-summary key, matching `Cart.totals`.
- `endsAt` is the end of the discount's last day in the store's timezone, in UTC. `endDate` is deprecated.

## Related

- [[headless-storefront]] — hub.
- [[headless-storefront-limits]] — list caps and per-visitor limits.
- [[headless-offers]] — offers on the cart.
- [[headless-checkout-submit]] — from the cart to an order.
- [[headless-customer-accounts]] — the customer token.
- [[storefront-cart-actions]] — the classic storefront's cart.
- [[settings-cart-limits-and-decrement]] — the merchant's cart limits.

## Open Questions

_None._
