---
type: feature
nav_path: "Marketing → Discounts → Container codes"
route_name: discounts-codes_list
route_path: /admin/marketing/discounts/codes, /admin/marketing/discounts/create/container
aliases: ["Container codes", "Promo code management", "Generated coupons", "Bulk coupon codes", "Промо кодове", "Управление на промо кодове", "Контейнерни кодове"]
tags: [marketing, discounts, coupons, container, generated-codes]
plan_gates: ["discount-container", "discount_global"]
created: 2026-05-23
updated: 2026-11-04
source_count: 5
---
# Container codes (Promo code management)

## Purpose

The **Container codes** page lists every code in the store's **shared pool of Container codes** — the codes behind the discount type designed for high-volume coupon campaigns ("Black Friday: 1,000 unique 10%-off codes for our newsletter subscribers"). The pool is one store-wide list: a code is attached to no Container discount and has its own percent. The Container discounts supply the target, dates and region and limit the total value, while each code in the table is what the customer types at checkout.

The page is **read + generate + toggle** — there is no per-code edit form. Each row shows the code string, its value, its created date, and an active toggle. The merchant uses this page to: see the inventory of generated codes (with copy-to-clipboard for sharing), generate a new batch of codes, toggle a code on/off, and filter by active state.

This page is large enough that it is split into six aspect pages. Drill into the one that matches the question rather than reading all of them.

## Where to find it

The Container codes list sits one level under the Discounts page. From any Container-discount row in the [[marketing-discounts]] table, click "Promo code management" — the breadcrumb is "Marketing → Discounts → Container codes" and the route is `discounts-codes_list` at `/admin/marketing/discounts/codes`. The codes shown are the store's generated Container codes (entity: [[discount-code]]).

### Creating a Container discount first

Codes only work while at least one active Container discount exists. The merchant creates one via **+ Add discount → "Discount with multiple promo codes - Container"**. The form is short: **Discount status** (`active`), **Discount name** (`name`), the **Discount value** (a percentage `type_value`, the most the entered codes can add up to), the **Discount target**, **Customer groups**, **Regions**, and a **Date range** (no timer). Codes are generated separately from this Container codes page (see [[discounts-codes-generator]]). A Container is created with `is_container = 1` and `code_apply = 1`, and its form has no such switch, so its codes apply on discounted products too (see [[discounts-codes-redemption]]).

## What the merchant can do here

- **Browse + manage the generated codes** — see [[discounts-codes-list-view]] for columns, filters, sort, row toggle, and bulk actions.
- **Generate a new batch of codes** — see [[discounts-codes-generator]] for the modal, validation, and code shape.
- **Distribute and redeem codes** — see [[discounts-codes-redemption]] for the cart-link auto-apply URL, reuse until turned off, and cart stacking.
- **Understand which terms come from the Container** — see [[discounts-codes-parent-terms]] for the terms it supplies, its value limit, plan-gating, and deleting codes.
- **Decide between Container codes and Code PRO** — see [[discounts-codes-vs-code-pro]].
- **Manage codes programmatically** — see [[discounts-codes-api]] for JSON-API v2 access.

## Sub-pages (in this cluster)

- [[discounts-codes-list-view]] — the list view: columns (Code / Value / Created At / Active), filters, sort, per-row toggle, bulk status + delete, and what the merchant cannot do here.
- [[discounts-codes-generator]] — the "Generate codes" modal, field validation, the generator retry loop, the hard-coded 10-char `[A-Z0-9]` code shape, and the absence of an upper limit on the count.
- [[discounts-codes-redemption]] — reuse until turned off, the `/cart/discount:<CODE>` auto-apply link, case-insensitive lookup, and the cart-array stacking rule (Container codes vs stand-alone codes are mutually exclusive).
- [[discounts-codes-parent-terms]] — what a code takes from the winning Container (target, dates, region), the value limit, plan-gating, and the `uses` recount.
- [[discounts-codes-vs-code-pro]] — a shared pool with a percent per code vs Code PRO's full per-code terms; when to pick each.
- [[discounts-codes-api]] — JSON-API v2 list / create / update / delete, generate up to 1,000 per call, no audit log.

## Settings & fields

The page itself has no settings beyond the listing controls and the generator modal — both documented on the aspect pages:

- Listing columns, filters, sort, and row actions — [[discounts-codes-list-view]].
- Generator modal fields + validation — [[discounts-codes-generator]].

## Business rules

The detailed business rules live on the aspect pages. The headline rules:

- **Shared pool, reusable.** Each code has its own percent; target, dates and region come from the Container that wins at checkout. A code works until it is turned off or deleted. For per-code terms use [[marketing-discounts-code-pro]] — see [[discounts-codes-vs-code-pro]].
- **Code shape is hard-coded** at 10 uppercase `[A-Z0-9]` characters — see [[discounts-codes-generator]].
- **Container discounts do not use the `discount_coupon` quota**, which counts only discounts holding their own code — see [[discounts-codes-parent-terms]].
- **Container codes and stand-alone codes are mutually exclusive in the cart** — see [[discounts-codes-redemption]].

## Related

- [[marketing-discounts]] — parent feature; the Container discount type lives there.
- [[marketing-discounts-code-pro]] — alternative multi-code engine with per-code terms.
- [[marketing-discounts-code-pro-generator]] — alternative bulk generator with length, range and random controls.
- [[marketing-discounts-code-pro-export]] — CSV export for Code PRO codes.
- [[discount-code]] — entity page for individual generated Container codes.
- [[discount]] — entity page for the Container discount.
- [[settings-hooks]] — saving a Container discount fires `discount.created` / `discount.updated`; changes to Container codes send none.

## Open questions

No outstanding questions.
