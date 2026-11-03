---
type: concept
nav_path: "Concept → Headless storefronts → Limits"
aliases: ["Storefront API limits", "Storefront API rate limits", "THROTTLED", "Too many requests", "Per-visitor limit", "List caps", "X-Request-Id", "Лимити на Storefront API", "Твърде много заявки", "Ограничения на Storefront API"]
tags: [nitrogen, headless, storefront-api, limits, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

> Part of [[headless-storefront]].

# Headless — Storefront API limits

## Definition

The limits a storefront built on `/api/sf` has to design around: how often one visitor may submit each form, how long a list one call may send, and how large a page of results may be. A limit past its value answers with a user error or a stated cut, not a failed request.

## Scope

Covered:

- Per-visitor limits, and the `THROTTLED` answer.
- List caps with their refusals.
- Page sizes.
- The return flow's code, and `X-Request-Id`.

Not covered:

- Hosting and account caps (storefronts, variables, deployment tokens) — see [[headless-nitrogen-overview]].
- The merchant's own cart limits and the 50-line rule — see [[headless-cart-rules]].

## Contrasts

- **A per-visitor limit vs a merchant's limit** — the first is the platform's and the same on every store. The second, such as `cart_max_products`, is set in [[settings-cart]].
- **Refused vs cut** — most lists past their cap refuse the call. A few fields answer null or read only the first entries, as noted below.

## Where it applies

### Who counts as one visitor

A visitor is the request's IP address. A storefront that calls the API from the browser needs nothing more.

A storefront that renders on its own server must send the shopper's address, or all its shoppers count as one visitor: the header `X-Storefront-Buyer-IP`, sent with the private token. Without the private token that header is ignored. See [[headless-storefront-api]].

### Per-visitor limits

A minute's allowance per store, per form and per visitor. Each form counts apart.

| Operation | Per minute |
|---|---|
| `contactFormSubmit`, `subscribeFormSubmit`, `productReviewCreate`, `productReviewAnswerCreate`, `productBackInStockSubscribe`, `gdprRequestCreate`, `fastOrderSubmit` | 10 |
| `customerLoginCodeSend`, `customerLoginCodeVerify`, `customerCreate`, `returnRequestStart` | 10 |
| `cloudCartPayExpressSubmit`, `cloudCartPayExpressCartSettle` | 10 |
| `articleCommentCreate` | 5 |
| `cartCustomizationFileUpload` | 20 |
| `subscribeFormViewed`, `cartOfferViewed`, `cartOfferDismissed` | 30 each |
| `cloudCartPayExpressQuote` | 30 |

Past the limit the answer is a user error with the code `THROTTLED` and the store's text: en *"Too many requests. Please try again in a couple of minutes"*, bg *"Твърде много заявки. Моля, опитайте отново след няколко минути"*. For `cartOfferViewed` and `cartOfferDismissed`, `counted` is also false, and nothing reaches the merchant's statistics.

A storefront's design should expect this on a shared address, such as an office or a mobile network, and keep what the buyer typed so they can send it again.

### List caps

100 entries in one list. Past it:

| List | Refusal |
|---|---|
| `lines` of `cartCreate`, `cartLinesAdd`, `cartLinesUpdate` | *"At most 100 lines can be sent in one call."* |
| `lineIds` of `cartLinesRemove` | *"At most 100 line ids can be sent in one call."* |
| A line's customizations, in `cartBundleAdd` too | *"At most 100 customizations can be answered on one line."* |
| Policy ids of a form, the account and the checkout | *"Every accepted policy id must be a Policy id, at most 100 of them."* (at the checkout: *"Every accepted consent id…"*) |
| `acceptedConsentIds` of `fastOrderSubmit` | *"At most 100 consent ids can be sent."* |
| `filters` of a listing | *"At most 100 filters can be sent."* |
| `nodes(ids:)` | *"At most 100 ids can be sent."* |

Answered without a refusal:

- `vendors(ids:)` reads the first 100.
- `quantityTierPrice(lines:)` answers null past 100 lines.
- `OfferHistoryInput` reads up to 100 entries of each list and skips the rest (see [[headless-offers]]).

### Page sizes

A connection takes `first` or `last`, at most 100; with neither, 25. Every connection pages both ways, except `relatedProducts`, which is forward only.

| Field | Default | At most |
|---|---|---|
| `relatedProducts(first:)` | 25 | 100 |
| `Product.reviews` | 10 | 50 |
| `Customer.orders` | 25 | 100 |
| `recentlyViewedProducts(first:)` | 8 | 30 |
| `productRecommendations` | | 10, no cursor |

Other size rules:

- `productComparison` compares the first three ids.
- A subscribe form's text answer takes 2000 characters.
- A review takes a title up to 200 characters, a comment up to 1000, an author name up to 200 (see [[apps-product-review-settings]]).
- A cart attribute's key takes 245 characters (see [[headless-cart-rules]]).

### Codes the buyer types

- **Sign-in code:** see [[headless-customer-accounts]].
- **Return flow** (`returnRequestStart`, `returnRequestVerify`, `returnRequestFlow(token)`): the code expires after ten minutes, and five failed attempts discard the flow. Keep only the token between requests and read the flow with `returnRequestFlow`: it answers `AWAITING_CODE` or `VERIFIED`, or null for an unknown or expired token. Reading counts no attempt and sends no code. `returnRequestResendCode` asks the customer to wait between resends. See [[storefront-withdrawal]].

### `X-Request-Id`

Every `/api/sf` response carries a UUID in `X-Request-Id`, the same one in the platform's logs. Quote it when reporting a failed call. A client's own value is replaced. The JSON-API v2 does not send this header (see [[json-api-headers-envelope]]).

## Related

- [[headless-storefront]] — hub.
- [[headless-storefront-api]] — endpoint, headers and tokens.
- [[headless-cart-rules]] — what cart mutations refuse.
- [[headless-offers]] — offer counting and history.
- [[headless-customer-accounts]] — the sign-in code.
- [[settings-cart]] — the merchant's own cart limits.

## Open Questions

_None._
