---
type: feature
nav_path: "Settings → Cart and checkout → Accounts and registration"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Customer accounts settings", "Guest vs registered checkout", "Convert guests to members", "Customer accounts verification", "Registration address requirement", "Hide prices for non-logged-in users"]
tags: [settings, cart, checkout, accounts, customers]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-cart]]. See the hub for the other aspects (abandoned reminder, payment/shipping defaults, limits, checkout fields, UI behavior, Google Maps, marketing consent).

# Cart and checkout — Accounts and registration

## Purpose

Two adjacent boxes on the Cart and checkout page that together decide **who can place an order** and **what they must supply at sign-up**. Specifically: whether the storefront accepts guests, registered customers, or both; whether unconfirmed (email-not-verified) accounts can still place orders; whether the platform auto-promotes guests into customer accounts at order time; whether anonymous visitors can even see product prices; and whether the registration form is the place where billing/shipping addresses are collected (versus collecting them later at checkout).

## Where to find it

Sidebar → Settings → **Cart and checkout** → boxes **Accounts and profiles** (`account_and_profile`) and **Requirements upon registration** (`reg_and_req`). The first box sits at the top of the page below the global Save button. The second box sits immediately under it.

## What the merchant can do here

- Decide whether email-unverified customer accounts can complete checkout.
- Pick the storefront's customer mix: **guests-only**, **registered-only**, or **both**.
- (Only when "both" is picked) Auto-register guests at order time and email them a generated password.
- Hide product prices from anonymous visitors entirely (useful for wholesale / B2B catalogues).
- Force shipping and / or billing address to be collected at registration time rather than at checkout.

## Settings & fields

### Box: Accounts and profiles (`account_and_profile`)

> Help text: *"If you select to verify your customer's accounts, they will have to confirm their email addresses, used at the registration process. Choose whether only registered / non-registered customers can make purchases on your store. Choose both if you want both types of customers to be able to make purchases. If Convert guests into members is On, guests will be automatically converted into members and a password will be sent to their email addresses once they made a purchase at your store."*

Header label: *"Customer Accounts — Choose if you want to prompt your customer to create an account when they check out."*

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Customer accounts verification** (`unconfirmed_accounts_restrict`) | Pick whether unconfirmed (email-not-verified) customers can still place orders or not. | Backend validation requires one of `none`, `checkout`. Options come from `meta.unconfirmed_accounts_restrict_options` (backend-defined enum). |
| **Customer profiles** (`checkout_customer_access`) | Storefront accepts orders from: registered customers only, guests only, or both. | Backend validation requires one of `both`, `member`, `guest`. Options come from `meta.checkout_customer_access`. |
| **Convert guests into members** (`guest_to_customer`) | When ON, guests who place an order are auto-registered: a customer account is created and a generated password is emailed to them. | Visible only when **Customer profiles** = `both` (dependField rule). |

### Box: Requirements upon registration (`reg_and_req`)

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Show product price only for logged in users** (`show_prices_only_for_logged_users`) | Hides all product prices from anonymous visitors. They see products but no prices until they sign in. | Useful for wholesale / B2B stores. |
| **Require shipping address on registration** (`require_registration_shipping_address`) | Forces the merchant's customers to enter a shipping address during sign-up, not later at checkout. | |
| **Require billing address on registration** (`require_registration_billing_address`) | Same idea for billing address. | |

## Business rules

### "Convert guests into members" requires Customer profiles = `both`

The dependField hides the switch when **Customer profiles** is set to `member` or `guest`. The auto-promotion behaviour also doesn't apply in those modes (there are no guests to promote in members-only mode, and no members to promote into in guests-only mode). The backend, however, will silently store any value the client sends — see [[settings-cart]] for the general "dependFields are cosmetic" rule.

### Guest-to-member promotion is a side-effect of order placement

The actual conversion happens during the order-creation pipeline, not from this screen. When `guest_to_customer = yes` AND `checkout_customer_access = both` AND a guest places an order, the platform creates a Customer record, generates a password, and sends a notification email containing the credentials. See [[order-processing-pipeline]] (Stage 1, step 1) for the exact placement of this hook.

### `unconfirmed_accounts_restrict` interacts with the verification-email subsystem

When set to `checkout`, customers with unconfirmed email addresses are blocked at checkout until they click the verification link. The verification email itself is managed elsewhere — this screen only chooses whether unverified accounts can still complete an order. `none` means no restriction.

### Hide-prices-for-anonymous affects every storefront surface

Toggling `show_prices_only_for_logged_users` ON hides prices on category listings, product detail pages, search results, the cart bubble (if any anonymous preview is rendered), and any storefront modules that display prices. The setting is read at storefront render time; the [[settings-cart]] hub's "settings cache is cleared on save" rule means anonymous visitors see the new behaviour immediately on next page load.

### Registration-time address requirement vs checkout-time

The two `require_registration_*` switches push address collection earlier in the funnel — useful for B2B stores that want to qualify the customer before showing prices or letting them browse, but adds friction. Most storefronts leave both OFF (addresses collected at checkout) — checkout-field visibility is managed in [[settings-cart-checkout-fields]].

## Related

- [[settings-cart]] — hub.
- [[customer]] — Customer entity created on guest-to-member promotion.
- [[order-processing-pipeline]] — Stage 1, step 1 hosts the guest-to-customer conversion side-effect.
- [[settings-cart-checkout-fields]] — sibling aspect; checkout-field visibility decides which fields appear at the standard checkout-time address step.
- [[checkout-flow]] — end-to-end checkout sequence concept page.
- [[settings-general]] — store name + email used in the auto-registration welcome email template.

## Open questions

_None._
