---
type: storefront-page
route_name: site.restore.abandoned
route_path: /restore-abandoned/{code}/{source}/{discount_code?}
themes_using: [all]
tags: [storefront, abandoned-cart, recovery, marketing, discount]
created: 2026-06-08
updated: 2026-06-08
source_count: 4
---

# Restore-abandoned cart link

## Purpose

The landing URL the abandoned-cart recovery system emails to customers once their cart is classified as abandoned. Clicking the link **restores the abandoned cart into the customer's current session** (merging with any cart they already have), **optionally applies a recovery discount code**, **tags the restoration source** for attribution, and **redirects to `/cart`** so the customer continues checking out as if they'd never left.

This is the single mechanism behind every recovery touch — recovery emails (and SMS / push where configured) link here.

## URL & route

- **Route name**: `site.restore.abandoned`.
- **Route path**: `/restore-abandoned/{code}/{source}/{discount_code?}`.
- **Method**: GET. No middleware beyond the global storefront ones — the URL is intentionally open so a not-logged-in customer can still restore their cart.

URL parameters:

- **`{code}`** — the abandoned cart's recovery lookup key, generated when the cart is classified as abandoned ([[abandoned-cart-recovery]]).
- **`{source}`** — free-form attribution string for the recovery channel. Conventionally `email-1` / `email-2` / `email-3` (position in the sequence), `sms`, `push`, `recover-link` (manual). Stored on the cart as `restore_source`.
- **`{discount_code}`** (optional) — a code applied automatically for incentive campaigns ("Come back and get 10% off"); applied as a discount-code or a discount-container-code depending on which it matches.

## How it loads

The page has **no template** — it is pure redirect logic. Verified flow:

1. Look up the abandoned cart by `{code}`, then resolve the customer's current cart (creating one if needed). **If either can't be found** → redirect to a fresh empty `/cart/{newKey}` (the silent failure path — expired link, deleted cart, mistyped code).
2. In a single transaction:
   - Set `restore_source = {source}` and `abandoned = true` on the current cart (the `abandoned` flag marks it as restored-from-abandoned for analytics).
   - **If the abandoned cart is not already the current cart**, merge it in — items are coalesced (quantities summed for duplicate variants, unique items kept).
   - **If the abandoned cart belonged to a customer matching the current session's customer** and had a shipping type, restore its progress: re-apply its discount (if any); if the cart `has_shippable` and a shipping address existed, restore `shipping_type` + shipping address and set the step to `shippingAddress`; if `has_billing_address` and a billing address existed, restore it and set the step to `billingAddress`.
   - **If a `{discount_code}` was passed in the URL**, apply it last (overriding any cart-restored discount) — as a discount-code if it matches one, else a discount-container-code — then save the cart.
3. Any transaction exception is silently swallowed (no message, no log); the redirect still happens.
4. Redirect to `/cart/{key}` using the customer's **new** session-cart key after the merge — not the abandoned cart's.

## What the customer sees

**Nothing at this URL** — they never view it. A 302 redirect lands the address bar on `/cart/{key}` with the restored items, so the experience is: click the link → brief (often imperceptible) redirect → land on the cart. If a discount was attached, the cart shows a flash notification `sf.module.cart.succ.discount_accepted` ("Discount applied") and totals already include it. If shipping + billing addresses were restored, "Continue to checkout" jumps straight to the right step.

## Storefront behaviour

- **Additive merge, not replacement** — items already in the current cart are merged with the restored ones, not overwritten. The merge is idempotent (quantities coalesced), so repeat clicks don't bloat it.
- **The abandoned cart is never deleted here** — the link can be clicked repeatedly (each re-merges), supporting retry / multi-device. Purging is handled by separate retention rules ([[abandoned-cart-recovery]]).
- **Address restoration is gated on customer match** — addresses restore only if the abandoned cart was owned by a customer AND the current session's customer matches; guests restore items only.
- **Step restoration mirrors prior progress** — `shippingAddress` only if the cart is shippable AND a shipping address existed; `billingAddress` only if `has_billing_address` was set.
- **URL discount overrides the cart-restored discount** — it is applied last.
- **Failure modes are silent** — every error path lands on a fresh `/cart/{newKey}` with no message (see Known issues).

## JavaScript behaviour

**None on this URL** — it is a pure server-side redirect. JS only runs once the customer lands on `/cart/{key}` (see [[storefront-cart]]). The `{source}` value lives on the cart's `restore_source` field; analytics modules / pixels read it from there when they next fire.

## Customisations available to the merchant

- **Recovery email templates + sequence** — admin → Marketing → Abandoned-cart recovery → configure the copy, the email sequence and intervals (e.g. 1h / 24h / 72h), discount-code inclusion, and the `{source}` value per email. See [[abandoned-cart-recovery]].
- **Recovery discount-code campaigns** — admin → Marketing → Discounts → create a code, bind it to the recovery flow; its value becomes the `{discount_code}` parameter.
- **Channel beyond email** — apps (SMS, push) fire the same URL with their own `{source}`.

The page has **no Theme Editor presence** because it has no UI; the customisation surface is the recovery campaign and the cart page the customer lands on.

## Theme variations

None — the URL has no template. Whichever theme is active, the customer is redirected to that theme's cart.

## Known issues / by-design vs bug

- **Silent fallback to empty cart** — every failure path (missing/expired recovery code, cart already converted to an order, cart purged by retention, transaction error) drops the customer on a fresh `/cart/{newKey}` with no message. "I clicked the link but my cart is empty" tickets usually land here. By design (avoids leaking abandoned-cart state) but support-confusing.
- **Multi-use link affects analytics** — repeat clicks re-merge harmlessly, but each re-sets `restore_source` and `abandoned = true`, so a cart can read as restored repeatedly.
- **Guests get no address recovery** — gated on customer match, so a returning guest always starts at the shipping-address step (no stable identity to bind addresses to). By design.
- **No crawler guard** — a bot indexing a recovery email could trigger restoration. Recovery URLs should be `nofollow` from the email side. (verify whether the recovery-email templates apply `nofollow`.)
- **Discount code is publicly visible** — anyone with the link sees `{discount_code}`; a forwarded email hands it to a friend. By design — a recovery incentive, not user-locked.
- **Exceptions are silently swallowed** — no message and no log on transaction failure, so "I clicked and nothing happened" can't be traced without replaying the URL. (verify whether the silent fallback writes anywhere.)
- **Container-code vs discount-code** — a code that doesn't match a discount is stored as a "discount container code" (the same dual-path as the cart/checkout discount submit, see [[discount-stacking]]). Whether it reduces the total depends on cart contents (e.g. minimum-spend rules), so "Discount applied" can show with no reduction.

## Related

- [[storefront-architecture]] — request lifecycle.
- [[storefront-cart]] — the page customers land on after.
- [[abandoned-cart-recovery]] — the email pipeline emitting these URLs.
- [[cart-vs-order-lifecycle]] — Cart states (active → abandoned → recovered → converted).
- [[discount-stacking]] — how `{discount_code}` is applied.
- [[checkout]] — where customers go next.
- [[notification-delivery]] — how recovery emails reach customers.
- [[storefront-known-issues]] — cross-page bugs.

## Open questions

- Whether the `{code}` can be rotated (single-use vs reusable). This page never rotates it; does the email trigger? (verify)
- The canonical list of `{source}` strings used by the platform's own recovery sequence. (verify)
- Whether SMS / push channels use this exact URL or a different short-link. (verify)
