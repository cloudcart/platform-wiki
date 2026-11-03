---
type: feature
nav_path: "Marketing → Discounts → Countdown → Storefront popup + timer"
route_name: checkout.countdown_discount_popup
route_path: /checkout/countdown-discount-popup
aliases: ["Countdown popup", "Countdown timer module", "Checkout countdown", "Confetti popup", "Fireworks popup", "Parade popup"]
tags: [marketing, discounts, countdown, storefront, popup, timer]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-countdown]]. See the hub for the other aspects (editor, eligibility, single-instance rule, cart totals + stacking, programmatic access).

# Countdown discount — storefront popup + timer

## Purpose

This page documents the customer-facing side of the Countdown discount: the checkout-only popup modal, the celebration animation that plays once on first view, and the live ticking timer rendered in the checkout summary's totals area.

**The timer is checkout-only.** Older wiki phrasing claimed the same timer renders on category pages and product detail pages — that was incorrect. The Countdown timer is rendered ONLY in the checkout summary's totals area; category and product-detail pages do NOT show the countdown timer for this discount type. (The category / product-detail timer overlay seen on other discounts is driven by separate per-product fields like `timer_in_listing` / `timer_in_details` + `date_end`, NOT by Countdown's `countdown_minutes`.)

## Where to find it

The popup is served from the dedicated route `/checkout/countdown-discount-popup` (route name `checkout.countdown_discount_popup`). The storefront's checkout page fetches it as part of the cart-summary render when the customer first reaches the checkout flow. There is no admin URL — the merchant configures the modal content in the [[countdown-discount-editor]] and the storefront renders it from that data.

## What the customer sees here

- A modal pops once with the merchant's `countdown_description` HTML inside.
- The chosen `countdown_popup_effect` animation plays once (`confetti`, `fireworks`, or `school_pride`).
- After the modal closes, a totals-row in the checkout summary shows the Countdown discount line + a live ticking timer counting down to the per-session expiry.
- If the timer elapses before the customer places the order, the totals line silently vanishes on the next cart recompute.

## What the merchant can do here

- Author the popup body (`countdown_description`) in the HTML editor, choose the celebration animation (`countdown_popup_effect`), and set the per-session timer length (`countdown_minutes`) — all in [[countdown-discount-editor]].
- Preview the chosen animation inline in the admin via the **Preview** button before saving.
- Inspect the per-cart meta the popup writes (`countdown_popup_first_showing`, `countdown_discount_popup_was_shown`) through support tooling when troubleshooting "the timer didn't start" tickets `(verify)`.

The merchant CANNOT trigger the popup outside of the checkout flow, cannot make it re-fire on the same cart after the first view, and cannot combine it with the [[apps-fast-order]] one-click buy flow (which bypasses Countdown entirely).

## Settings & fields

### Popup endpoint behaviour

When the storefront's checkout page fetches `/checkout/countdown-discount-popup`:

1. Look up the cart's Countdown discount via `getCountdownDiscount` (already eligibility-filtered — see [[countdown-discount-eligibility]]).
2. If a Countdown is eligible AND `countdown_discount_popup_was_shown` is not yet set on the cart:
   - Set `countdown_discount_popup_was_shown = 1` on the cart meta.
   - Set `countdown_popup_first_showing = <UTC now>` on the cart meta.
   - Render the modal view with the merchant's `countdown_description` HTML + the chosen `countdown_popup_effect` animation.
3. If the popup was already shown for this cart, return null (no re-pop) — but the cart's `countdown_popup_first_showing` keeps governing when the timer expires.

So the timer starts the **first time** the customer's cart visits the popup endpoint — typically when they hit step 1 of the checkout flow.

### Animation effects (vue-rewards)

The chosen `countdown_popup_effect` plays via the vue-rewards confetti library:

| Effect | Stored value | Visual behaviour |
|--------|--------------|------------------|
| **Confetti** | `confetti` | Bidirectional burst from left + right edges of the screen — default celebration look. |
| **Fireworks** | `fireworks` | Sequential bursts at multiple positions on the canvas. |
| **Parade** | `school_pride` | Sustained red confetti stream from both sides; longest-lasting effect. |
| _None_ | `null` | The popup still shows, with no animation. |

Particle counts, angles, and intervals are frontend-rendering details that may evolve with theme updates `(verify)`; the merchant-facing surface is the visual category.

After the initial play the animation does not loop. The merchant can preview the effect inline in the admin form via the **Preview** button — see [[countdown-discount-editor]].

### Per-cart meta the popup writes

| Key | Set when | Used for |
|-----|----------|----------|
| `countdown_discount_popup_was_shown` | First popup view at the dedicated endpoint. | Suppresses re-pop on subsequent checkout visits. |
| `countdown_popup_first_showing` | First popup view. | Anchors the per-session timer (`first_show + countdown_minutes` = expiry). |

### Timer module at checkout

The cart-totals line for Countdown is keyed `discount.before.countdown.<discount_id>` and carries the timer's expiry timestamp (`popupFirstShowDate + countdown_minutes`) as its `value`. The storefront timer module reads this directly to know when to stop ticking.

Merchants don't see this metadata in the admin order view — it's used purely for the storefront countdown module.

## Business rules

### Per-session, not global clock

The `countdown_minutes` value defines how long the timer runs **from the moment each individual customer first sees the popup** at checkout. Two customers landing in checkout 30 minutes apart **each get the full `countdown_minutes` window** of urgency — not a shared deadline. This is the key behavioural difference from a calendar-based `date_end` (which expires at a single moment for all customers).

See [[countdown-discount-eligibility]] for the full per-cart validity check chain.

### Popup fires once per cart

Once the platform sets `countdown_discount_popup_was_shown = 1`, subsequent checkout visits don't re-fire the popup. The same `countdown_popup_first_showing` timestamp keeps defining when the timer expires.

### Survives navigation, resets on cookie clearing

The `countdown_popup_first_showing` is stored on the cart meta. As long as the customer keeps the same cart (same session / customer account), navigating away and returning doesn't reset the timer. But clearing cookies / logging out / starting a new cart resets the meta, and the timer restarts on the next checkout visit.

### Timer expiry is silent

When a customer's `countdown_minutes` window elapses without an order being placed, the platform does NOT auto-deactivate the parent discount or auto-delete the cart's `countdown_popup_first_showing` meta. The cart-time evaluation simply returns null (the totals line vanishes) until the customer clears their cart or the discount expires by `date_end`.

### FastOrder app bypasses the popup entirely

The [[apps-fast-order]] integration (one-page-checkout buy-now flows) explicitly excludes Countdown discounts from cart evaluation when the order is submitted through the fast-order route. The popup does not fire, the timer is not started, the per-cart `countdown_popup_first_showing` meta is not set. A merchant relying on Countdown urgency cannot combine it with a fast-order one-click buy flow — the customer following the fast-order path simply misses the countdown promotion.

### `disable_countdown_discount` cart-context suppression

An internal flag `disable_countdown_discount` on the cart instance suppresses Countdown for specific cart contexts (e.g., admin-edited orders, B2B flows). When set, `getCountdownDiscount` returns null regardless of qualifying conditions. This is normally not user-controlled — set by integration code paths `(verify)`.

## Related

- [[marketing-discounts-countdown]] — hub.
- [[countdown-discount-editor]] — where the merchant configures `countdown_description` + `countdown_popup_effect`.
- [[countdown-discount-eligibility]] — the validity check chain that decides whether the popup fires at all.
- [[countdown-discount-cart-totals]] — what the timer's totals line looks like at checkout.
- [[apps-fast-order]] — the integration that bypasses the popup.

## Open questions

- Confirm the cart-context contexts that set `disable_countdown_discount` (admin order edit, B2B carts, anything else?) `(verify)`.
