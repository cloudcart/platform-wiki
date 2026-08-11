---
type: concept
nav_path: "Concept → Abandoned cart recovery → Attribution on recovered order"
aliases: ["Recovered order attribution", "abandoned = 1", "restore_source", "Recovered source filter", "Recovery banner", "Order was recovered through", "cart_id preservation"]
tags: [orders, cart, abandoned, recovery, attribution, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[abandoned-cart-recovery]]. See the hub for the other aspects (threshold, eligibility, restore link, channels, bulk send, plan quota).

# Abandoned cart — recovered-order attribution

## Definition

When the customer completes checkout from a restored cart, the resulting order carries flags that identify it as a recovery. The merchant observes recovery success via these flags — on [[orders-history]] as a banner on the order, on [[orders]] as a **Recovered source** filter, and on [[analytics-abandoned-carts]] / [[analytics-abandoned-checkout]] as aggregated metrics.

The recovered order goes through the **normal [[order-status-workflow]]** from `pending` onward — the recovery flag doesn't change the lifecycle, only the attribution.

## Scope

Covered:

- The four order fields stamped on recovery (`abandoned`, `restore_source`, `cart_id`, `campaign_id`).
- The [[orders-history]] banner — *"Order was recovered through `<source>`"*.
- The [[orders]] **Recovered source** filter.
- The link-only attribution rule — direct checkout submissions without clicking the link are NOT tagged.
- Where in analytics recovery performance shows up.

Not covered here:

- The link itself (URL format, click handler) — see [[abandoned-cart-restore-link]].
- The `<source>` value's relationship to delivery channel — see [[abandoned-cart-channels]].
- The full order-status lifecycle the recovered order then runs through — see [[order-status-workflow]] and [[order-processing-pipeline]].

## Contrasts

- **Recovered order vs normal order** — identical workflow and statuses. The only differences are the `abandoned = 1` flag and `restore_source` value on the recovered order, which drive the banner + filter. Lifecycle, fulfillment, payment, refunds — all identical.
- **Recovery attribution vs marketing-campaign attribution** — `restore_source` is the recovery channel (`email` / `messenger`); `campaign_id` is the marketing-campaign attribution (set if the customer's session had UTM / cookie data from a campaign). The two can co-exist on the same order — a campaign-driven visit can later turn into a recovery if the customer abandons and comes back via the link.
- **Link-recovery vs direct re-submission** — if the customer somehow bypasses the link and submits the cart directly (e.g. they typed in the storefront URL, found their cart still in the session, and checked out), the order does NOT get tagged `abandoned = 1`. The tag is set **only via the link path**.

## Where it applies

### Fields stamped on the recovered order

When the customer completes checkout from a restored cart, the resulting order carries:

- **`abandoned = 1`** — flag that this order came via the recovery path.
- **`restore_source`** = `email` or `messenger` — which channel delivered the link (see [[abandoned-cart-channels]]).
- **`cart_id`** = the original cart ID (preserved across the lifecycle).
- **`campaign_id`** — set if the customer's session had marketing-attribution data (UTM / cookie) at checkout time; independent of the `restore_source` value.

These fields are set during the restore handler's stamping step (see [[abandoned-cart-restore-link]]) on the active session cart and inherited by the order at checkout submission.

### Recovery banner on [[orders-history]]

The recovered order's audit log shows a banner: *"Order was recovered through `<source>`"* where `<source>` is the value of `restore_source` (`email` or `messenger`). This appears as one of the timeline events on the order's history view. (verify)

### Recovered source filter on [[orders]]

On the placed-orders list, the merchant can use the **Recovered source** filter to see only recovered orders. The filter options are typically:

- All orders (default — no filter).
- Recovered (any source).
- Recovered via email.
- Recovered via messenger.

(verify the exact filter options surfaced in the UI)

### Analytics surfaces

Recovery performance is aggregated in two places:

- **[[analytics-abandoned-carts]]** — abandoned-cart trend dashboard. Shows count of abandoned, count of recovered (`abandoned = 1` on orders), recovery rate, recovery revenue. Useful for tracking whether changes to the threshold (see [[abandoned-cart-threshold]]) or the recovery message body actually move the recovery rate.
- **[[analytics-abandoned-checkout]]** — checkout-funnel drop-off. Shows the step BEFORE order placement where customers exit. Different question — "where do customers drop?" rather than "how many recovered?".

### Cart cleanup after recovery vs drop-off

- **Recovered** — the original cart row is referenced by the new order's `cart_id`; the cart row stays in the database for audit but no longer appears in [[orders-abandoned]] (it's been converted, not abandoned anymore — the seven-check eligibility excludes carts with an order against them; see [[abandoned-cart-eligibility]]).
- **Not recovered** — the cart eventually ages out (the underlying session token expires; the cart row is auto-cleaned by background maintenance). The merchant can also bulk-delete from [[orders-abandoned]] at any time.
- **Manually deleted** — if the merchant clicks Delete on a cart in [[orders-abandoned]], the cart is soft-deleted and removed from the list.

### Direct re-submission edge case

A customer who has the abandoned cart in their browser session (or who typed the storefront URL and found their cart preserved) and checks out **without** clicking the restore link will produce an order with:

- `abandoned = 0` (no recovery flag).
- `restore_source = NULL`.
- `cart_id` = the same cart ID (still preserved).

This order is NOT shown under the Recovered source filter and does NOT show the recovery banner. From the merchant's analytics perspective, this is "natural conversion" rather than "recovery". This matters when interpreting recovery-rate metrics — they undercount "would-have-recovered" carts where the customer self-rescued without the email.

## Related

- [[abandoned-cart-recovery]] — hub.
- [[abandoned-cart-restore-link]] — where the link click stamps `abandoned = true` + `restore_source` onto the active session cart, which the order then inherits.
- [[abandoned-cart-channels]] — the delivery channel that determines whether `restore_source` is `email` or `messenger`.
- [[order]] — the order entity that carries `abandoned`, `restore_source`, `cart_id`, `campaign_id`.
- [[cart]] — the cart entity referenced via `cart_id`.
- [[orders]] — placed-orders list with the Recovered source filter.
- [[orders-history]] — per-order audit log; shows the recovery banner.
- [[order-status-workflow]] — the normal order-status lifecycle the recovered order then runs through.
- [[order-processing-pipeline]] — the full status-transition pipeline that handles the recovered order from `pending` onward.
- [[analytics-abandoned-carts]] — abandoned-cart trend analytics.
- [[analytics-abandoned-checkout]] — checkout-funnel drop-off analytics.

## Open Questions

- Confirm the exact options surfaced on the [[orders]] Recovered source filter (all / email / messenger?). (verify against the filter UI)
- Confirm the banner string format on [[orders-history]] for orders recovered via messenger. (verify)
