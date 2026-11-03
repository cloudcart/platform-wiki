---
type: concept
nav_path: "Concept → Headless storefronts → Placing an order"
aliases: ["Headless checkout", "cartSubmitForCompletion", "cartCheckoutReadiness", "attemptToken", "paymentSessionId", "form_validation", "fastOrderSubmit", "checkoutUrl", "Плащане Nitrogen", "Поръчка през Storefront API", "Бърза поръчка API"]
tags: [nitrogen, headless, storefront-api, checkout, consents, fast-order, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

> Part of [[headless-storefront]].

# Headless — placing an order

## Definition

The three ways a Nitrogen storefront turns a buyer's choice into an order: sending the buyer to the store's web checkout with `Cart.checkoutUrl`, submitting the cart with `cartSubmitForCompletion`, or a one-product `fastOrderSubmit`. An order placed through the API behaves as one from the checkout: the pre-order and order-created events fire, so the merchant's new-order e-mail, the `order.created` webhook and the buyer's notices go out.

## Scope

Covered:

- The web checkout hand-off.
- `cartSubmitForCompletion`: consents, retries, how it can end.
- CloudCart Pay's embedded form, and its repeated `form_validation` event.
- Fast order through the API.

Not covered:

- What cart mutations refuse before this — see [[headless-cart-rules]].
- The classic checkout — see [[checkout-step-customer]].
- The types and fields, which introspection answers.

## Contrasts

- **`checkoutUrl` vs `cartSubmitForCompletion`** — the first leaves the whole checkout to the platform. The second keeps the buyer on the storefront, which then collects everything itself.
- **`cartSubmitForCompletion` vs `fastOrderSubmit`** — the first takes the buyer's cart. The second builds its own temporary cart for one product or bundle, leaves any cart the buyer has untouched, and places a cash-on-delivery order.

## Where it applies

### The web checkout hand-off

`Cart.checkoutUrl` is a link, `/checkout/adopt/{token}`, on the store's main host, so the checkout stays on one domain even when a domain is routed to the storefront. Read it when the buyer is about to go: it is valid for ten minutes.

For a request that runs as a signed-in customer, the link signs them in once. A reused link still hands over the cart, as a guest. A customer who can no longer sign in goes on as a guest too.

### `cartSubmitForCompletion`

Check `cartCheckoutReadiness` first: the submission refuses anything it reports as missing, and says which.

**Consents.** Pass the id of every consent the buyer accepted in `acceptedConsentIds`, from `cartCheckoutReadiness.consents`. Nothing else records that the buyer agreed.

- With the GDPR app, the policies follow its settings ([[apps-gdpr-policy-storefront]]).
- Without it, the store's checkout terms pages are required consents, listed by `policies(form: SUBMIT_PAYMENT)`. A submission or a fast order without them is refused.

**Retries.** `attemptToken` makes the call safe to retry: the same token returns the same order. Generate one per checkout attempt and reuse it when the call fails or times out.

**How it ends:**

| Status | Meaning |
|---|---|
| `COMPLETED` | The order exists and needs nothing more from the buyer. |
| `REQUIRES_REDIRECT` | The order exists, unpaid. Send the buyer to `redirectUrl`. Every card payment ends here, unless paid in the embedded form. |
| `REQUIRES_PAYMENT` | The order exists and the payment session is linked. Let the embedded form charge now. |
| `FAILED` | Nothing was created. See `userErrors`. |

### CloudCart Pay's embedded form

`cartPaymentSessionCreate` opens a session when the merchant has CloudCart Pay set to inline. When the buyer presses pay, call `cartSubmitForCompletion` with the session's id as `input.paymentSessionId`, and let the form charge only once the answer is `REQUIRES_PAYMENT`. The order then exists and owns the payment before any money moves, and completes when the payment succeeds, whether or not the buyer's page reports back. Read it with `orderStatus`.

A session that no longer matches the order, because the cart changed after it was opened, ends in `REQUIRES_REDIRECT` with a warning: open a new session and submit again with the same `attemptToken`, or send the buyer to `redirectUrl`. For any other payment method, `paymentSessionId` is ignored with a warning.

**Apple Pay and Google Pay: the repeated `form_validation` event.** A wallet tap reaches the storefront in the form's `form_validation` step. The form repeats that event every 2 seconds until it is answered, and gives up after about 10 seconds. `cartSubmitForCompletion` can take longer than one repeat, so:

- Submit on the first event for a wallet, once per tap.
- Ignore its repeats while that call is running, and answer once with the result.
- Do not answer a repeat with `failFormValidation`: the form then drops the tap with no error and no wallet sheet, and an answer that comes later is ignored.
- A repeat that starts another submit races the first.

The express buttons on product and cart pages are a separate flow: see [[headless-cloudcart-pay]].

### Fast order

`fastOrderSubmit(attemptToken, input)` places one product or bundle, cash on delivery, with no delivery method. See [[apps-fast-order]] for the merchant's side.

- Offer it only when `fastOrderSettings` is not null. It is null when the app is off or not configured, the plan has no checkout, or cash on delivery is unavailable.
- `input` takes `line` or `bundle`, one of them. A bundle's own variant is refused as a `line`.
- `email` is required from guests only. A signed-in customer orders under their account's e-mail, and an e-mail typed by anyone else never places the order into the account that has it.
- The same `attemptToken` returns the same order, and two concurrent submissions cannot place two.
- `userAgent` gives the store's analytics the buyer's device.
- A visitor may send it 10 times a minute.
- `FastOrderPayload.analyticsEventId` is the id to fire in the browser; a retry gets the same. See [[headless-analytics-consent]].

## Related

- [[headless-storefront]] — hub.
- [[headless-cart-rules]] — the cart before this.
- [[headless-analytics-consent]] — reporting the purchase.
- [[headless-storefront-limits]] — list caps and per-visitor limits.
- [[apps-gdpr-policy-storefront]] — the policies.
- [[apps-fast-order]] — Fast Order.
- [[headless-cloudcart-pay]] — CloudCart Pay's express buttons.

## Open Questions

_None._
