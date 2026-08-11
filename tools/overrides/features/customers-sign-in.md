---
type: feature
nav_path: "Customers → Sign in as customer"
route_name: admin.api.customers.sign_in
aliases: ["Sign in as customer", "Login as customer", "Customer impersonation", "View as customer", "Влез като клиент", "Имитиране на клиент"]
tags: [customers, impersonation, support, sign-in]
plan_gates: []
created: 2026-05-21
updated: 2026-08-11
source_count: 6
---

# Sign in as customer (impersonation)

## Purpose

The merchant's **impersonation feature** — log in to the storefront AS a specific customer, in a new browser tab. Used by support staff to see exactly what the customer sees (their cart, wishlists, account page, applied discounts), to debug a complaint that they can't add a product / apply a coupon / complete checkout, to verify the customer's order history and addresses from the storefront perspective, and to make changes on the customer's behalf (e.g. update a saved address, complete a stuck checkout) when walking them through by phone is too slow.

It's a one-click action — the merchant clicks the **right-to-bracket** icon next to a customer's name on [[customers]]; a new tab opens and the merchant is authenticated as that customer on the storefront. There is no confirmation prompt.

## Where to find it

From the [[customers]] list → next to any customer's name (inline icon, purple `right-to-bracket` chevron). Hover tooltip: *"Login to customer account"*. The icon is HIDDEN for customers in **group ID 2** (the reserved Guest group — see [[customers-custom-groups]]). The link opens in a NEW TAB (`target="_blank"`).

The action is gated by the `customers` permission section ([[settings-staff]]).

## Sub-pages (in this cluster)

- [[customers-sign-in-trigger]] — the right-to-bracket icon: where it lives, the group-2 (Guest) hidden-state, the new-tab single-click (no-confirmation) UX, and what the merchant can / cannot do from it.

## What the merchant can do here

- Click the sign-in icon to open the storefront in a new tab, logged in as the chosen customer — see [[customers-sign-in-trigger]].
- See the storefront as that customer would: their cart, addresses, orders in My Account, applied discounts, and group-specific prices.
- Make changes on the customer's behalf from the storefront.

What the merchant CANNOT do: sign in as a Guest (group 2 — icon hidden), sign in without leaving the admin context (always a new tab), sign in as a banned customer (icon renders but the storefront refuses the session), or sign in without the `customers` permission (403).

## Settings & fields

No settings on this action — it is a single-click impersonation flow with no form and no parameters. The only relevant control lives elsewhere: the `customers` API permission section on [[settings-staff]], which gates the whole feature.

## Business rules

- **Excluded for group 2 (Guest)** — the icon is hidden; Guests have no login session to assume. See [[customers-sign-in-trigger]].
- **New-tab UX preserves the admin session** — the original admin tab is unaffected; the new tab is a separate customer session.
- **A banned customer cannot be impersonated** — the icon still renders, but the storefront refuses to open the session and shows the suspension notice.
- **Permission is coarse** — granting `customers` access also grants impersonation; there is no separate "may impersonate" permission. Grant the `customers` section only to staff who should be able to act as a customer.
- **The action is not recorded in the customer's or the order's history** — a store with staff-accountability or data-access logging requirements should keep its own record of when impersonation is used.
- **Treat the opened session as privileged** — it is a real, logged-in customer session. Close the tab when finished, and do not share the address it opens.

## Related

- [[customers-sign-in-trigger]] — the trigger icon (aspect).
- [[customers]] — parent list (the icon lives next to the customer's name).
- [[customers-details]] — verify whether also accessible from the identity card.
- [[customers-custom-groups]] — group 2 (Guest) is the excluded group.
- [[settings-staff]] — moderator permissions for the `customers` section.
- [[customer]] — entity page.

## Open questions

- Confirm whether the icon also renders on the [[customers-details]] identity card, or only in the [[customers]] list.
