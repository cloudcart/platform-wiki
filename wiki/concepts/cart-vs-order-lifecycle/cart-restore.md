---
type: concept
nav_path: "Concept → Cart vs Order lifecycle → Cart restore"
aliases: ["Cart restore", "Restore link", "Restore-link handler", "abandoned = 1", "restore_source", "Recovered cart", "Cart key token", "Възстановяване на количка", "Линк за връщане"]
tags: [cart, order, lifecycle, restore, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[cart-vs-order-lifecycle]]. See the hub for the other aspects (cart state machine, order state machine, handoff, abandonment).

# Cart restore

## Definition

A **restore link** is the per-cart unique URL embedded in an abandoned-cart recovery email (or messenger-bot message). When the customer clicks it, the restore-link handler validates the cart's secret `key` token, restores the cart's contents into a fresh storefront session, records the recovery source (`email` / `messenger-bot`) on the cart, and returns the customer to the checkout. If the customer then completes checkout, the resulting [[order|Order]] is marked `abandoned = 1` with `restore_source` set — this is the ONLY path that produces the recovery attribution flag (direct revisits without a click produce `abandoned = 0`; see [[cart-to-order-handoff]]).

The restore link is the customer-clicking complement to the merchant-sent recovery email described in [[cart-abandonment]]. The two together form the abandoned-cart recovery loop: detect → email → click → restore → convert.

## Scope

Covered:

- The cart `key` (secret session token) — what it does, why it's not regenerated, why bots get a sentinel value.
- The restore-link click handler: `key` validation, session restoration, `restore_source` attribution.
- The `abandoned = 1` order flag — set only by this handler, never retroactively.
- The two recovery sources: `email` and `messenger-bot`.
- Why a customer who returns directly (no click) produces an order with `abandoned = 0`.
- Effect on the [[orders|orders list]] *Recovered source* filter and the related analytics.

Not covered here:

- The Cart data shape + the six cart states — see [[cart-state-machine]].
- The 7 eligibility rules + the 3-min sweep + the per-period plan quota — see [[cart-abandonment]].
- The full Place-order pipeline that runs once the customer completes checkout from a restored cart — see [[cart-to-order-handoff]].
- The analytics / attribution surfaces for recovered conversions — see [[analytics-abandoned-carts]] / [[orders-abandoned]].

## Contrasts

- **Restore vs conversion**: every Recovery is a Conversion (an order is created), but not every Conversion is a Recovery. Recovery = customer arrived via restore-link click, so `abandoned = 1` + `restore_source` set. Conversion alone = any storefront submit, including a direct revisit to the same cart.
- **`abandoned = 1` flag vs Abandoned cart state**: confusingly close names. The cart STATE "Abandoned" (see [[cart-state-machine]]) means a cart that crossed the threshold. The ORDER flag `abandoned = 1` means the resulting order was placed via a restore-link click. A cart can be in the Abandoned state but still produce an `abandoned = 0` order if the customer revisits the storefront directly instead of clicking the email.
- **`restore_source = email` vs `messenger-bot`**: two delivery channels are surfaced. `email` is the standard abandoned-cart-recovery email (manually triggered by the merchant from [[orders-abandoned]]). `messenger-bot` is set when the customer arrives via a Messenger-bot conversation flow (the Facebook Messenger plug-in app, when installed and configured).
- **Cart `key` vs Order ID**: the `key` is a secret restore token tied to the cart row, valid until the cart is hard-deleted or the customer's `key` is regenerated. The order ID is the public-facing identifier of the placed order, present only after handoff.

## Where it applies

**The cart `key`.** The cart row holds a secret session token in the `key` field, used for restore links and cross-device identification (allowing a customer who opens the email on a different device to still pick up the same cart). The `key` is generated when the cart row is created and remains stable for the cart's life. Bots and crawlers, when they trigger cart creation, receive the sentinel `key` `the_client_is_a_bot_and_does_not_have_permission_to_access_this_page_please_contact_site_support` instead of a real random token (see [[cart-state-machine]]); this prevents crawled cart traffic from generating valid restore URLs.

**Restore-link click handler.** When the customer clicks the link:

1. The cart's `key` is validated against the URL parameter — invalid / unknown keys reject.
2. The cart's contents (line items, applied discounts, selected shipping / payment, address) are restored into a fresh storefront session.
3. The recovery source (`email` or `messenger-bot`) is recorded for attribution on the cart.
4. The customer is returned to the storefront at the cart / checkout step (depending on data completeness).
5. If the customer completes checkout from this point, the resulting order is marked `abandoned = 1` with `restore_source` set. The cart-to-order handoff runs the standard Place-order pipeline — see [[cart-to-order-handoff]].
6. If the customer doesn't return after restore, the cart stays Active (the click already moved `updated_at` forward); the abandoned-cart timer restarts from this point — see [[cart-abandonment]].

**The `abandoned = 1` flag is set only by this handler.** An abandoned cart that the customer revisits and submits directly (no restore link clicked, no email / Messenger source recorded) produces an order with `abandoned = 0`. The flag is NOT set retroactively. So direct-revisit submits are treated as normal placed orders with no recovery attribution and are excluded from the [[orders]] *Recovered source* filter. The implication for the merchant is that the recovery-conversion analytics will undercount any recovery where the customer arrived via memory, bookmark, or a fresh storefront visit — only the link-click path produces the attribution.

**Implications for the merchant view.**

- The merchant can filter [[orders]] by the *Recovered source* filter to see only `abandoned = 1` orders — these are the email / Messenger-driven recoveries.
- The [[analytics-abandoned-carts]] dashboard counts recovery-conversion rate against the `abandoned = 1` numerator, so the rate is the click-path rate only.
- Cart state transitions: after a successful restore, the cart goes Abandoned → Recovered (Active) → Converted (when the order is placed). See [[cart-state-machine]] for the transition diagram.

**Worked example — restore-link click completes the abandonment loop.**

(Picking up from the example in [[cart-abandonment]] at step 7.)

7. Customer clicks the link 30 minutes after receiving the email (so at 11:38 in the example). Cart's contents restore into a fresh session; `restore_source = email` is recorded on the cart. Customer continues checkout, submits at 11:40.
8. Order is created. `cart_id` points back to the original cart. `abandoned = 1`. `restore_source = email`. See [[cart-to-order-handoff]] for the full Place-order pipeline that runs here.
9. [[orders]] now shows the order. [[orders-abandoned]] no longer shows the cart (it's converted, not abandoned). See [[cart-state-machine]] for the Converted state.
10. The discount's `uses` counter increments when the order reaches `paid` status (assuming the customer was using a discount code) — see [[discount-stacking]].

## Related

- [[cart-vs-order-lifecycle]] — hub.
- [[cart-abandonment]] — the eligibility + sweep + email-send pipeline that precedes restore.
- [[cart-state-machine]] — the six cart states (Abandoned → Recovered → Converted).
- [[cart-to-order-handoff]] — Place-order pipeline that runs when the customer completes checkout from a restored cart; `abandoned = 1` set here.
- [[orders-abandoned]] — abandoned-cart admin list + Send restore link.
- [[orders]] — placed-orders list with *Recovered source* filter.
- [[analytics-abandoned-carts]] — recovery-conversion-rate dashboard.
- [[abandoned-cart-recovery]] — the cross-cutting recovery concept page.
- [[discount-stacking]] — discount usage counting on the resulting order.
- [[settings-hooks]] — `order.created` webhook fires on the resulting order.

## Open Questions

None.
