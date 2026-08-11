---
type: feature
nav_path: "Customers → Customer details"
route_name: customers-details.new
route_path: /admin/customers-new/details/:id
aliases: ["Customer details", "Customer profile", "Профил на клиент", "Детайли на клиент"]
tags: [customers, profile, detail]
plan_gates: ["customers"]
created: 2026-05-21
updated: 2026-06-10
source_count: 14
---
# Customer details

## Purpose

The **per-customer profile page** — opens when the merchant clicks a row in [[customers]]. A two-column layout with a tab strip beneath; the single source of truth for one customer: identity, lifetime KPIs, internal notes, tags, ban state, default address, full order / payment / address history.

Used when the merchant needs to look up an order someone phoned about, update preferred shipping addresses, check lifetime value before granting a discount, ban / unban, manually confirm an unverified email, or delete the record.

It is a **hub-and-tabs container**: the detail page owns the identity card, insights, note, tags picker, ban-reason card, and default-address card; every other surface lives on its own sub-tab. If the URL points to a non-existent customer ID, the page shows a *"Customer not found"* message.

## Sub-pages (in this cluster)

This page is split into 6 aspect pages, each covering one well-scoped slice. Drill into the aspect that matches the question — do not read every page.

- [[customer-details-identity-card]] — left-column identity card, insights KPI module, note card, tags picker, edit-pencil dropdown actions.
- [[customer-details-tab-strip]] — the sub-tab navigation; which tabs render, route names, conditional Reviews tab, current-build gaps.
- [[customer-details-ban-flow]] — Ban customer modal (required reason), one-click Remove ban, ban-reason card on the right column.
- [[customer-details-email-verification]] — *Email not verified* indicator, Confirm email address (bypass), Send confirmation email (regenerate code), pending-confirmation state.
- [[customer-details-default-address]] — right-column default address card with Google Map preview, separate query, empty state vs filled state, edit modal entry point.
- [[customer-details-delete]] — Delete customer dropdown action, cascade effects (cart, subscriber, webhook), auto-redirect, hard-delete-only.

## Where to find it

From [[customers]] → click any row → opens `/admin/customers-new/details/:id`.

The page is hosted inside the Customers wrapper, so the page header still shows the customer's full name, the **Ban / Remove ban** button, the dropdown with **Delete customer**, and the **"Banned"** chip when applicable.

## What the merchant can do here

The detail page surfaces six interaction zones, each documented on its own aspect page:

- **Insights + Identity + Note + Tags** (left column) — lifetime KPI panels, identity card with pencil-dropdown, conditional 191-char-capped note, REPLACE-mode tags picker. See [[customer-details-identity-card]].
- **Ban-reason card** (right column, conditional) — visible only when banned; the reason the merchant typed at ban time. See [[customer-details-ban-flow]].
- **Default address card** (right column) — field table + Google Map preview, or empty-state *+ Add address*. See [[customer-details-default-address]].
- **Sub-tab navigation** — Overview / Shipping / Billing / Orders / Products / Payments (+ conditional Reviews). See [[customer-details-tab-strip]].
- **Page-header actions** — Ban customer, Remove ban, Delete customer (inherited from the Customers wrapper). See [[customer-details-delete]].
- **Email verification overrides** — manual Confirm email / Send confirmation email on the identity-card pencil dropdown. See [[customer-details-email-verification]].

### What the merchant CANNOT do here

- View login history / device sessions for the customer.
- Impersonate the customer ("view as customer" for support purposes).
- Roll back the customer's email change history.

## Settings & fields

The detail page is primarily a layout / navigation container. Editable fields live in:

- The identity-card pencil-dropdown → opens the **Create / Edit Customer modal** (see [[customers]] for the full field list and [[customer-details-identity-card]] for entry points).
- The customer note card → opens the same modal in note-focused mode.
- The customer tags picker (inline, no modal).
- The per-sub-tab forms — addresses ([[customers-details-shipping-addresses]] / [[customers-details-billing-addresses]]) allow address CRUD.

## Business rules

### Real-time customer data sharing across sub-tabs

The detail page loads the customer record once and shares it across all sub-tabs (Overview, Orders, Addresses, etc.). So when the merchant edits the customer in the modal, every sub-tab shows the new data without a page reload.

The default-address card refreshes independently — an address-only change updates just that card, not the whole customer record. See [[customer-details-default-address]].

### Notes are admin-only

Notes are NEVER shown to the customer. They're for internal record-keeping (e.g., *"called complaining about late delivery 2026-04-12 — refunded 50 BGN as goodwill"*, *"wholesale customer — always 30-day NET payment"*). Hard-capped at 191 characters server-side — see [[customer-details-identity-card]].

### Ban reason is admin-only

The ban reason is visible to admins on this page but is never shown to the customer directly. (The placeholder text on the ban modal says the reason *"will be set to your customer via email"* — verify whether the email side is implemented `(verify)`.) See [[customer-details-ban-flow]].

### Reviews tab is conditional

The Reviews sub-tab appears only when the [[apps-product-review]] app is installed AND active. See [[customer-details-tab-strip]].

### Permission

This page requires the **customers** permission section. Per [[settings-staff]] restrictions, moderators may see only customers in specific groups depending on their permission grants.

## Programmatic access

Customer records can be read and updated via **JSON-API v2** — see [[api-customers]] for endpoints, attributes, and validation. Related resources have their own endpoints: shipping/billing addresses ([[api-customer-shipping-address]], [[api-customer-billing-address]]) and tags ([[api-customer-tags]]).

**Same side effects apply.** A PATCH fires the same lifecycle as the identity-card Edit modal: `customer.updated` webhook, email-change routed through the pending-confirmation flow (NOT immediate — see [[customer-details-email-verification]]), 191-char note cap enforced server-side, tag-change propagated to the Subscriber record, marketing toggle triggering a segment recompute.

**"Confirm email address" and "Send confirmation email"** (manual overrides) are NOT in JSON-API v2 — they have admin-only endpoints. See [[customer-details-email-verification]].

**DELETE mirrors the dropdown**: cart cascade-deleted, Subscriber record removed, `customer.deleted` webhook fires, past orders kept (orphaned with snapshot data), no soft delete. See [[customer-details-delete]].

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `customers` | Numeric (max customer records) | Same store-wide customer-record cap as [[customers]]. Viewing/editing existing customers is NOT gated. The cap only blocks creating NEW customers (identity-card Edit modal's "guest → registered" auto-merge, or JSON-API v2 POST); visiting the detail page for an existing customer never trips it. |

Read/update/delete of an EXISTING customer is permission-gated only; plan gating is enforced at creation. Numeric gates extend via packs ([[plan-vs-feature-pack]]).

## Related

- [[customers]] — parent list page.
- [[customer-details-identity-card]] — identity, insights, note, tags.
- [[customer-details-tab-strip]] — sub-tab navigation.
- [[customer-details-ban-flow]] — ban / remove-ban flows.
- [[customer-details-email-verification]] — verification + manual override flows.
- [[customer-details-default-address]] — default address card.
- [[customer-details-delete]] — delete customer cascade.
- [[customers-details-overview]] — Overview tab.
- [[customers-details-shipping-addresses]] — Shipping addresses tab.
- [[customers-details-billing-addresses]] — Billing addresses tab.
- [[customers-details-orders]] — Orders history tab.
- [[customers-details-products]] — Products bought tab.
- [[customers-details-payments]] — Payments tab.
- [[customers-details-reviews]] — Reviews tab (conditional).
- [[customer]] — entity page.
- [[customer-group]] — customer-group definitions used in the identity card.
- [[settings-staff]] — permission grants for the Customers section.
- [[settings-hooks]] — `customer.updated` webhook fires on edits made here.
- [[marketing-segments]] — segments built from customer tags shown here.
- [[subscriber-vs-customer]] — the customer-record vs marketing-subscriber distinction behind the Marketing flag + tag propagation.
- [[apps-product-review]] — gates the Reviews sub-tab.

## Open questions

- The Ban modal placeholder text says the reason *"will be set to your customer via email"* — verify whether the ban-notification email is actually sent.
