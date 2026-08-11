---
type: feature
nav_path: "Customers → Sign in as customer → Trigger icon"
route_name: admin.api.customers.sign_in
route_path: /admin/api/core/customers/sign-in/:customer_id
aliases: ["Sign in icon", "Login to customer account icon", "Right-to-bracket icon", "Customer impersonation trigger", "Влез като клиент бутон"]
tags: [customers, impersonation, support, sign-in, ui]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-sign-in]]. See the hub for the other aspects (redirect/token chain, security & audit gaps).

# Sign in as customer — the trigger icon

## Purpose

This aspect covers the **UI affordance** that starts a customer impersonation: the right-to-bracket icon the merchant clicks next to a customer's name. It documents where the icon lives, when it is hidden, and the fact that the click is a single-step, no-confirmation action that opens a new browser tab.

## Where to find it

From the [[customers]] list → next to any customer's name (inline icon, purple `right-to-bracket` chevron). Hover tooltip: *"Login to customer account"*.

The icon is **HIDDEN** for customers in **group ID 2** (the platform's reserved Guest group — see [[customers-custom-groups]]).

It may also appear on the customer's identity card in [[customers-details]] (verify whether also shown there).

The link opens in a **NEW TAB** (`target="_blank"`).

## What the merchant can do here

### Click the sign-in icon

The right-to-bracket icon on a customer row opens a new tab in which the merchant is authenticated as that customer on the storefront. The merchant then sees the storefront exactly as the customer would — their cart, wishlists, account page, applied discounts, group-specific prices, order history, and saved addresses. This is used to:

- See exactly what the customer sees.
- Debug a complaint that they can't add a product / apply a coupon / complete checkout.
- Verify the customer's order history, addresses, and recent activity from the storefront perspective.
- Make changes on behalf of the customer (e.g. update a saved address, complete a stuck checkout) when walking them through by phone is too slow.

### What the merchant CANNOT do here

- **Sign in as a Guest (group 2)** — the icon is hidden. Guests are checkout-only with no login session to assume.
- **Sign in without leaving the admin context** — the action always opens a new tab; the admin session in the original tab is preserved.
- **Sign in as a banned customer** — the icon still renders (the hidden-state checks group, not ban-state), but the click fails on the storefront with a suspension error.
- **Sign in without the `customers` permission** — the endpoint is permission-gated; moderators without that grant get a 403.

## Settings & fields

No settings on this action — it is a single-click affordance with no form, no options, and no parameters the merchant can adjust. The only thing that varies is *which* customer row the icon sits on.

**Visual:**

- Icon: `fa-light fa-right-to-bracket` rendered in purple (`cc-purple`).
- Tooltip: dark-themed tooltip with the text "Login to customer account".
- Located inline next to the customer's `full_name` link.

**Click target:**

- The link element is `<a target="_blank" href="/admin/api/core/customers/sign-in/<customer_id>">` — a vanilla HTML link, NOT a Vue router-link.
- The browser handles the new-tab opening; the admin SPA does not intercept.
- The link is built **unconditionally** for non-Guest customers (even banned ones); only the storefront-side login refuses banned customers.

## Business rules

### Excluded for group 2 (Guest)

The icon is hidden when the customer is in group ID 2. Group 2 is the platform's reserved Guest group — customers who completed checkout without registering (no login credentials, no profile). There is nothing to sign in as. For all other groups (Regular, custom tiers like VIP / Wholesale), the icon renders.

### Reused name-cell renderer

The icon is rendered by a shared name-cell component, so it appears anywhere that component is reused as a name renderer — primarily the [[customers]] list, and potentially the identity card on [[customers-details]] (verify).

### No confirmation modal — single-click action

The feature has **NO confirmation dialog, NO modal, NO warning prompt**. Clicking the icon immediately fires the redirect chain in a new tab. There is no "Are you sure?" / "This will log you into their account" step. This is consistent with the icon being a plain `<a target="_blank">` link with no `confirm` wired up. The merchant should treat the click as immediately effective.

### Smarty + Vue mixed

The icon is rendered by a modern Vue component, but the endpoint and authentication flow are backend Smarty / the application framework.

## Related

- [[customers-sign-in]] — hub.
- [[customers]] — parent list (the icon lives next to the customer's name).
- [[customers-details]] — verify whether also accessible from the identity card.
- [[customers-custom-groups]] — group 2 (Guest) is the excluded group.
- [[customer]] — entity page.

## Open questions

- Confirm whether the icon also renders on the [[customers-details]] identity card, or only in the list.
