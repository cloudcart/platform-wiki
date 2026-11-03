---
type: feature
nav_path: "Settings → Cart and checkout → Cart UI behaviour"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Cart bubble", "Cart bubble counter", "Cart icon visibility", "Cart sort order", "Cart animations", "Buy now action", "action_after_add_to_cart", "Side panel cart", "compact_cart_panel", "Merge cart on login", "merge_cart", "bubble_display_quantity", "cart_order_by"]
tags: [settings, cart, checkout, storefront, ui]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-cart]]. See the hub for the other aspects (accounts, abandoned reminder, payment/shipping defaults, limits, checkout fields, Google Maps, marketing consent).

# Cart and checkout — Cart UI behaviour

## Purpose

The box on the Cart and checkout page that controls **storefront-side cart-UI behaviour** — what the cart icon looks like in the header, what number the bubble counter shows, how items are sorted inside the cart, what happens when the customer clicks "Buy now" or "Add to cart", whether the cart page renders as a slide-out side-panel or a full page, and whether anonymous carts merge into the customer's existing cart at login.

None of these settings affect what the customer can buy — they only shape the **storefront UI experience** around the cart.

## Where to find it

Sidebar → Settings → **Cart and checkout** → box **Cart appearance and animations** (`miscellaneous`). Header label rendered: *"Miscellaneous"*.

## What the merchant can do here

- Show or hide the cart icon in the storefront header.
- Choose whether the bubble counter shows **unique variants** count or **total quantity**.
- Choose how products are sorted in the cart: by **category** or by **addition order**.
- Enable / disable cart-button animations when the customer hits "Add to cart".
- Pick what happens after "Buy now" / "Add to cart" — jump to checkout, jump to cart page, show a confirmation popup, or do nothing.
- Render the cart page as a slide-out side panel instead of a full page.
- Merge an anonymous cart into the customer's existing cart at login.

## Settings & fields

### Box: Cart appearance and animations (`miscellaneous`)

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Show cart icon at the site header** (`show_cart`) | Toggle visibility of the cart icon in the storefront's top navigation. | |
| **How to display the cart bubble** (`bubble_display_quantity`) | `variants` = count of unique products / `quantity` = total item count. | |
| **Sort products in cart by** (`cart_order_by`) | `category` / `id` (addition order). | |
| **Enable cart button animations** (`checkout_animation`) | Whether "Add to cart" triggers a small animation on the storefront. | |
| **Action after customer clicks on 'Buy now' button** (`action_after_add_to_cart`) | `checkout_redirect` (jump to checkout) / `go_to_cart` (jump to cart page) / `show_popup` (confirmation modal) / `stay_on_page` (do nothing). | |
| **Show 'Cart page' as a side panel** (`compact_cart_panel`) | Renders the cart page as a slide-out side panel instead of a full page. | Help block: *"Works only with Forward to the cart page function."* |
| **Merging carts** (`merge_cart`) | At login, if the customer had an old anonymous cart, its products are merged into the now-logged-in cart. | Help block: *"At the entrance, if the customer had an old cart with products, add them to the new cart"*. |

## Business rules

### Side-panel cart requires "Forward to cart page" action

`compact_cart_panel = ON` only takes effect when `action_after_add_to_cart = go_to_cart`. Picking the side-panel option while Add-to-cart redirects to checkout, shows a popup, or stays on the page means the side panel never renders — because the cart page is never opened. The help block on the field surfaces this requirement to the merchant.

### Bubble counter modes give different numbers for multi-variant carts

`bubble_display_quantity = variants` shows the **count of unique cart lines** (e.g., a cart with "Red T-shirt × 3 + Blue T-shirt × 2" shows `2`). `bubble_display_quantity = quantity` shows the **total unit count** (the same cart shows `5`). Stores selling high-quantity items (multi-pack groceries, B2B wholesale) typically pick `quantity` for accuracy; stores selling distinct goods (clothing, jewellery) often pick `variants` to keep the bubble visually compact.

### `cart_order_by = category` groups by product taxonomy

Picking `category` groups cart lines by the product's primary category. This is useful for grocery / multi-section stores where the customer wants to see "Dairy" items together. `id` falls back to addition order — items appear in the cart in the order the customer added them.

### Merge-cart-on-login is one-way

When the customer logs in and has an anonymous cart that overlaps with their logged-in cart (same SKU in both), the merge **adds the anonymous quantities to the logged-in quantities** — the customer ends up with the union. The anonymous cart is then cleared. This is a one-way operation: the merchant cannot un-merge, and the anonymous cart's session is discarded on next page load.

If the merchant disables this (`merge_cart = no`), the anonymous cart is **discarded** at login and the customer sees only their previously-saved logged-in cart. This is the safer choice for B2B stores where mixing accounts is undesirable.

### "Buy now" actions affect single-product pages, not multi-product checkout

`action_after_add_to_cart` describes what happens immediately after a customer clicks an Add-to-cart / Buy-now button on a product detail page — it does NOT govern what happens when the customer hits the final checkout button. The four options:

- `checkout_redirect` — skip the cart entirely, go straight to checkout.
- `go_to_cart` — navigate to the cart page (also where `compact_cart_panel` takes effect).
- `show_popup` — display a confirmation modal listing what was just added; the customer can choose to continue shopping or proceed.
- `stay_on_page` — no navigation; the bubble counter updates silently.

The first three are the common choices; `stay_on_page` is used by stores where the customer often adds many items before reviewing.

### Cart icon hidden hides the bubble too

`show_cart = no` removes the cart icon from the storefront header entirely. Customers can still reach the cart via direct URL, but it's effectively a checkout-funnel-only flow. Bubble counter settings (`bubble_display_quantity`) become moot when the icon itself isn't rendered.

### Animations are theme-cooperative

`checkout_animation = ON` triggers the storefront's add-to-cart animation, but the actual animation is implemented in the active theme. Themes that don't implement an animation handler will silently ignore the setting. Most stock CloudCart themes support it.

## Related

- [[settings-cart]] — hub.
- [[cart]] — the cart entity rendered by these UI rules.
- [[checkout-flow]] — end-to-end checkout sequence; the `action_after_add_to_cart` rules feed into this.
- [[settings-cart-accounts-registration]] — sibling aspect; affects whether anonymous carts exist at all (guests-only / both modes).
- [[customer]] — the customer entity whose login triggers merge-cart logic.
- [[storefront-architecture]] — storefront rendering pipeline that reads these UI settings at page load.

## Open questions

_None._
