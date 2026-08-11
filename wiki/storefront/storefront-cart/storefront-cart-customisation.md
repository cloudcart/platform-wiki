---
type: storefront-page
route_name: cart.list
route_path: /cart/{cart_key}
themes_using: [all]
tags: [storefront, cart, settings, plan-gate, known-issues]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[storefront-cart]]. See the hub for the other aspects (the three render surfaces, cart actions / mutations + JS hooks).

# Cart — merchant customisation, plan gate & known issues

## Purpose

Documents the levers the **merchant** controls over the cart — store-wide settings, the Theme Editor block, and per-product line behaviour — plus the `checkout` plan gate and the by-design-vs-bug edge cases support agents hit most. The surfaces these settings affect are on [[storefront-cart-surfaces]]; the mutations they gate are on [[storefront-cart-actions]].

## URL & route

These settings shape the same render route the hub documents — `cart.list` — `/cart/{cart_key}` — and the action routes on [[storefront-cart-actions]]. The settings themselves are edited in the admin panel, not on a storefront route.

**Plan gate**: every cart route is wrapped by a middleware that throws `checkout.disabled` if the merchant's plan doesn't include the `checkout` feature. Crawlers requesting `/cart/*` receive a 404 with `X-Robots-Tag: noindex`.

## How it loads

Settings are read server-side when each cart surface renders (and when each mutation runs), so changing a setting takes effect on the next cart load — no rebuild required. The render flow itself is on [[storefront-cart-surfaces]].

## What the customer sees

Settings change what the customer sees: `show_cart=no` hides the cart UI entirely, `action_after_add_to_cart` decides whether the drawer opens after Add-to-cart, the `checkoutText` block adds copy under the totals, and `checkout_min_price` / `checkout_max_price` can block the "Proceed to checkout" CTA with an error message. The visual surfaces are detailed on [[storefront-cart-surfaces]].

## Storefront behaviour

The settings below directly alter storefront behaviour (the mutation mechanics they gate are on [[storefront-cart-actions]]):

- `show_cart=no` removes every cart surface from the storefront.
- `action_after_add_to_cart` switches the post-add behaviour between opening the drawer, redirecting to `/cart`, or staying silent + toast.
- `cart_max_products` / `cart_max_quantity` cause `cart.add` to throw translated cap errors.
- `checkout_min_price` / `checkout_max_price` bound the checkout CTA.

## JavaScript behaviour

These are server-side settings; they have no dedicated JS hooks of their own. They influence which `cc.*` events fire and whether the drawer opens — the hook + event inventory is on [[storefront-cart-actions]].

## Customisations available to the merchant

**Store-wide settings ([[settings-cart]]):**

- `show_cart` — `yes` / `no` — global kill-switch for the header cart bubble. When `no`, no cart UI shows anywhere on the storefront.
- `action_after_add_to_cart` — `panel` (open drawer) / `redirect` (jump to `/cart`) / `none` (silent + toast).
- `compact_cart_panel` — when on, clicking the header cart bubble opens the drawer instead of navigating to `/cart`.
- `cart_max_products` — per-variant quantity cap (0 = unlimited).
- `cart_max_quantity` — per-cart total quantity cap (0 = unlimited).
- `checkout_min_price` — minimum cart subtotal to allow checkout. **Not enforced in the cart** — the Proceed CTA stays active; the customer is stopped on the checkout page, which shows the error in place of the form. See [[settings-cart-limits-and-decrement]].
- `checkout_max_price` — maximum cart subtotal, stopped the same way.

**Theme Editor → Cart module:**

- "Checkout text" content block (`checkoutText` module) — free-form HTML below the totals summary.

**Per-product (affects how a line displays):**

- `allow_quantity_change` — when `no`, the line shows a static quantity, no stepper.
- `tracking` + `continue_selling` — drives the stepper cap and out-of-stock notices (see [[inventory-variant-model]] for the master switches; stock is never reserved at the cart stage — decrement happens on the order, see [[cart-vs-order-lifecycle]]).
- Bundle sub-products — each sub-product has `setting('visible_cart')` that toggles whether it appears under the parent line.

## Theme variations

- All settings apply across themes; what varies is which surface a theme chooses to expose. For example a theme may honour `compact_cart_panel` with a hover-dropdown while another shows click-to-open only — the theme-variation surface is documented on [[storefront-cart-surfaces]].

## Known issues / by-design vs bug

- **Cart key is permanent for a session** — once a customer's cart has a key, that key stays in the URL. Refreshing `/cart/{key}` shows the same cart. By design.
- **Guest cart merge on login** — when a guest with items in their cart logs in, their guest cart merges into their stored customer cart. Quantities sum, duplicate variants are coalesced, customer-cart options win on conflict. By design (see [[cart-vs-order-lifecycle]]).
- **"Clear cart" doesn't fire `cc.cart.product.updated`** — it fires `removed` and `deleted` instead. Listeners that only bind to `updated` will miss clear events. (Mechanics on [[storefront-cart-actions]].)
- **`action_after_add_to_cart=none` still fires the cart-updated event and reloads the cart module** — the visual drawer just doesn't open. Some merchants expect "none" to be truly silent; this is by design.
- **Crawlers get 404** — search-engine crawlers requesting `/cart/*` get a 404 with `noindex`. By design — cart pages shouldn't be indexable.
- **Plan-gate hard-crash** — when the merchant's plan doesn't include `checkout`, every cart route throws `checkout.disabled`. This affects sandbox / trial plans. By design.

## Related

- [[storefront-cart]] — hub.
- [[settings-cart]] — every store-wide cart setting documented here.
- [[storefront-cart-surfaces]] — the surfaces these settings affect.
- [[storefront-cart-actions]] — the mutations these settings gate.
- [[cart-vs-order-lifecycle]] — guest-merge semantics + why stock isn't reserved at cart stage.
- [[inventory-variant-model]] — the `tracking` + `continue_selling` master switches that drive line behaviour.
- [[checkout]] — where the gated "Proceed to checkout" path lands.

## Open questions

None.
