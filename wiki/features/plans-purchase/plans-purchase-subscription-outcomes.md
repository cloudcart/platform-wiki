---
type: feature
nav_path: "Profile → Choose plan → {Plan} → Purchase → Pay now → Outcome"
route_name: admin.checkout.confirm
route_path: /admin/checkout (confirm step)
aliases: ["Plan checkout confirm", "Plan subscription create", "Plan subscription update", "Per-item failure surface", "Plan re-purchase overwrite", "Резултат от чекаут", "Грешка при плащане на план", "Подновяване на абонамент"]
tags: [plans, purchase, checkout, subscription, lta, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plans-purchase]]. See the hub for the other aspects (billing cycle, recommended add-ons, plan detail view, checkout panel, business rules, discount codes).

# Plans purchase — subscription outcomes

## Purpose

The **confirm step** is the server-side endpoint behind *Pay now* on the Checkout side-panel. It validates prerequisites (invoice details + saved card), iterates the cart items independently (so item-level failures don't roll back successes), creates or updates subscription records (`MODE_CREATE` vs `MODE_UPDATE` for re-purchase), and — for LTA-bundle offers — routes through a separate contract-creation path. This page catalogues all the outcomes the merchant might see.

## Where to find it

Triggered by the *Pay now* button inside [[plans-purchase-checkout-panel]]. The HTTP endpoint is the standard admin `confirm` step at `/admin/checkout`. The merchant never navigates here directly — they only ever see the result rendered into the Checkout panel body.

## What the merchant can do here

This page is not a screen — it's the outcome catalogue. Use it when a merchant reports:

- *"It says 'Please enter your invoice details' but I already filled them in — why?"*
- *"My plan succeeded but my Mailchimp app failed — what now?"*
- *"I bought the same plan twice. Did I get charged twice?"*
- *"My LTA bundle didn't go through."*

## Settings & fields

(No fields — this page documents server-side outcomes, not a settings form. The merchant-visible surfaces are the Checkout panel toast/error banner and the per-item success card — both rendered by [[plans-purchase-checkout-panel]].)

## Business rules

### Checkout confirm requires invoice details + a card on file

The confirm step rejects the cart when either is missing:

- **No invoice details** → *"Please, enter your invoice details"* (HTTP 422) → the merchant is funnelled to [[billing-invoicing]].
- **No payment method** → *"Please, add payment method"* (HTTP 422) → the merchant is funnelled to [[billing-cards]].

The merchant CAN seed the cart on the PlanPanel without either, but they cannot complete the purchase until both exist. After fixing the missing piece, they return to checkout (the cart is still seeded).

### Cart `confirm` is destructive on success

When `confirm` succeeds, the cart is fully cleared before redirecting (`$cart->clear` — *(verify)*). The merchant's UTM session is also cleared. There's no "partial confirm" — every item in the cart is either successfully created as a subscription or surfaces in the response's `status[]` array with a per-item error message.

### Per-item failures are surfaced, not all-or-nothing

The confirm step iterates each cart item independently. If item 1 succeeds and item 2 fails (e.g. card declined for that one charge specifically), the response includes both outcomes:

```
status: [
  { success: true, item: 'Plan Pro — Yearly', error: null },
  { success: false, item: 'Mailchimp app', error: 'Card declined' },
]
```

The successful items become subscriptions; the failed ones do not. The merchant sees a partial-success state in the per-item card and can retry the failed items individually (re-enter the purchase flow with a clean cart and pick only the failed item).

### Existing subscription is reused on plan re-purchase

When the merchant re-buys their **current plan** (e.g. switching billing cycles), the confirm step finds the existing `plan_details` subscription and runs the platform code instead of `MODE_CREATE` — the same subscription record is updated in place (new billing cycle, new `next_billing_date`). The `unique_id` of the subscription is preserved.

The same overwrite logic applies to:

- **Apps** — matched by `model_id`.
- **Any item flagged `overwritable`** — matched by `mapping`.

This avoids duplicate subscription rows for the same logical product. See [[subscriptions]] for the subscription record model.

### LTA-bundle path uses a separate contract creator

When the cart includes an **LTA-bundle offer**, the confirm step routes through a separate `createLtaContract` path that creates an LTA contract record + renews it, generating subscriptions for each contract item. This path is only used for staff-onboarded LTA flows; regular self-serve merchants don't see it. See [[contracts]] for the LTA contract surface.

### LTA-contract cart-conflict check (422)

If the merchant has an active LTA contract AND adds a non-LTA item to the cart that conflicts with their contract terms (e.g. buying a plan when the contract covers one), the confirm step throws *"Your cart conflicts with your active contract"* (HTTP 422). This protects LTA merchants from accidentally double-paying for items already covered. See [[plans-purchase-business-rules]] for the LTA-override entry rule that prevents most merchants from reaching this state.

### Subscription created only on success — not on PlanPanel submit

The plan-detail subscription is **created when checkout succeeds**, not when the PlanPanel form is submitted. The PlanPanel only seeds a cart; the actual money movement + subscription creation happen on the confirm step. So a merchant who closes the browser between PlanPanel and Pay-now has not been charged and has no subscription.

### Success path triggers parent reload

When *Pay now* succeeds and the panel is closed, the parent screen reloads (`window.location.reload` after a 2.5-second delay) so the new plan / app / service / pack appears in the merchant's environment immediately — sidebar plan badge, app list, etc. See [[plans-purchase-checkout-panel]] for the in-panel confirmation card that renders before this reload.

### Status badges follow `status[].success`

The per-item card renders each cart line with a *Successful* / *Not successful* badge based on `status[].success`. Only `plan_details`-type items render the per-item list — for pure app/service purchases (no plan), the success card simply shows the success heading + email-receipt confirmation without the list.

### HTTP status reference

| Status | Meaning |
|--------|---------|
| 200 | All cart items processed (each may individually have succeeded or failed — check `status[]`). |
| 422 — *"Please, enter your invoice details"* | Invoice profile missing on the merchant. |
| 422 — *"Please, add payment method"* | No saved card on the merchant. |
| 422 — *"Your cart conflicts with your active contract"* | LTA-contract cart-conflict check tripped. |
| (Braintree returns `clientToken` in place of success) | 3DS challenge required — see [[plans-purchase-checkout-panel]]. |

## Related

- [[plans-purchase]] — hub.
- [[plans-purchase-checkout-panel]] — the Pay-now UI that surfaces these outcomes.
- [[plans-purchase-business-rules]] — the upstream LTA-override + cart-reset rules that prevent some 422s.
- [[subscriptions]] — the subscription records created on success (`plan_details`, `cloudcart_app`, `cloudcart_service` types).
- [[billing-invoicing]] — funnelled-to target on the *"invoice details"* 422.
- [[billing-cards]] — funnelled-to target on the *"payment method"* 422.
- [[contracts]] — LTA contract surface (the `createLtaContract` path).
- [[expired-subscription]] — adjacent state when the existing subscription is past-due before re-purchase.
- [[merchant-subscription-lifecycle]] — full lifecycle (states / renewal / retry / expiration / cancellation).

## Open questions

None.
