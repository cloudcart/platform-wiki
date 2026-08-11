---
type: feature
nav_path: "Marketing → Discounts → Container codes"
route_name: discounts-codes_list
route_path: /admin/marketing-new/discounts/codes
aliases: ["Container codes", "Promo code management", "Generated coupons", "Bulk single-use codes", "Промо кодове", "Управление на промо кодове", "Контейнерни кодове"]
tags: [marketing, discounts, coupons, container, generated-codes]
plan_gates: ["discount_coupon"]
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---
# Container codes (Promo code management)

## Purpose

The **Container codes** page lists every **single-use coupon code** generated under all of the store's **Container discounts** — the discount type designed for high-volume coupon campaigns ("Black Friday: 1,000 unique 10%-off codes for our newsletter subscribers"). Each code in the list is a one-redemption coupon row that lives independently from the parent Container discount; the parent defines the *terms* (percent or flat amount), while each individual code in the table is what the customer types at checkout.

The page is **read + generate + toggle** — there is no per-code edit form. Each row shows the code string, its value, its created date, and an active toggle. The merchant uses this page to: see the inventory of generated codes (with copy-to-clipboard for sharing), generate a new batch of codes, toggle a code on/off if it leaks or needs to be retired, and filter by type / value / active state.

This page is large enough that it is split into six aspect pages. Drill into the one that matches the question rather than reading all of them.

## Where to find it

The Container codes list sits one level under the Discounts page. From any Container-discount row in the [[marketing-discounts]] table, click "Promo code management" — the breadcrumb is "Marketing → Discounts → Container codes" and the route is `discounts-codes_list` at `/admin/marketing-new/discounts/codes`. The codes shown are the store's generated Container codes (entity: [[discount-code]]).

### Creating the Container parent first

The codes don't exist on their own — they belong to a **Container parent discount**. The merchant creates that parent via **+ Add discount → "Discount with multiple promo codes - Container"**. The Container parent form is short: **Discount status** (`active`), **Discount name** (`name`), the **Discount value** (a percentage `type_value`), the **Discount target**, **Customer groups**, **Regions**, and a **Date range** (no timer). The parent holds the *terms*; the per-code batches are generated afterwards from this Container codes page (see [[discounts-codes-generator]]). The parent is created with `is_container = 1` and `code_apply = 1` (so its codes can apply on already-discounted carts — see [[discounts-codes-redemption]]).

## What the merchant can do here

- **Browse + manage the generated codes** — see [[discounts-codes-list-view]] for columns, filters, sort, row toggle, and bulk actions.
- **Generate a new batch of codes** — see [[discounts-codes-generator]] for the modal, validation, code shape, and the legacy generator's 1,000-per-request cap (the modern Vue modal is uncapped).
- **Distribute and redeem codes** — see [[discounts-codes-redemption]] for the cart-link auto-apply URL, single-use redemption, and cart stacking.
- **Understand which terms come from the parent** — see [[discounts-codes-parent-terms]] for inherited terms, the percent-value cap, plan-gating, and delete cascade.
- **Decide between Container codes and Code PRO** — see [[discounts-codes-vs-code-pro]].
- **Manage codes programmatically** — see [[discounts-codes-api]] for JSON-API v2 access.

## Sub-pages (in this cluster)

- [[discounts-codes-list-view]] — the list view: columns (Code / Value / Created At / Active), filters, sort, per-row toggle, bulk status + delete, and what the merchant cannot do here.
- [[discounts-codes-generator]] — the "Generate codes" modal (modern Vue + legacy), field validation, the generator retry loop, the hard-coded 10-char `[A-Z0-9]` code shape, and the legacy 1,000-per-request cap (modern modal uncapped).
- [[discounts-codes-redemption]] — single-use redemption, the `/cart/discount:<CODE>` auto-apply link, case-insensitive lookup, and the cart-array stacking rule (Container codes vs stand-alone codes are mutually exclusive).
- [[discounts-codes-parent-terms]] — what each code inherits from the parent Container (target, customer group, dates), the percent-value cap, `discount_coupon` plan-gating, the parent's `code_apply` reject-on-conflict, and the `uses` recompute.
- [[discounts-codes-vs-code-pro]] — identical-terms mass-generation vs Code PRO's per-code terms; when to pick each.
- [[discounts-codes-api]] — JSON-API v2 list / create / toggle / delete, same side-effects, no audit log, no 1,000 cap.

## Settings & fields

The page itself has no settings beyond the listing controls and the generator modal — both documented on the aspect pages:

- Listing columns, filters, sort, and row actions — [[discounts-codes-list-view]].
- Generator modal fields + validation — [[discounts-codes-generator]].

## Business rules

The detailed business rules live on the aspect pages. The headline rules:

- **Identical terms, mass-generated, single-use.** Every code under one Container shares the parent's terms; each redeems exactly once. For per-code terms use [[marketing-discounts-code-pro]] — see [[discounts-codes-vs-code-pro]].
- **Code shape is hard-coded** at 10 uppercase `[A-Z0-9]` characters — see [[discounts-codes-generator]].
- **Container codes count against the `discount_coupon` plan feature** — see [[discounts-codes-parent-terms]].
- **Container codes and stand-alone codes are mutually exclusive in the cart** — see [[discounts-codes-redemption]].

## Related

- [[marketing-discounts]] — parent feature; the Container discount type lives there.
- [[marketing-discounts-code-pro]] — alternative multi-code engine with per-code terms.
- [[marketing-discounts-code-pro-generator]] — alternative bulk generator with prefix/suffix/length/range controls.
- [[marketing-discounts-code-pro-export]] — CSV export for Code PRO codes.
- [[discount-code]] — entity page for individual generated Container codes.
- [[discount]] — entity page for the parent Container discount.
- [[settings-hooks]] — Container discount CRUD fires `discount.created` / `discount.updated` / `discount.deleted`.

## Open questions

No outstanding questions.
