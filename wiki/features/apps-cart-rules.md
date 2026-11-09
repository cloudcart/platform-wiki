---
type: feature
nav_path: "Marketing → Apps → Cart Rules"
route_name: apps.cart-rules.overview
route_path: /admin/apps/cart-rules
aliases: ["Cart Rules", "Aura Cart Rules", "Правила за количката", "Cart rules engine", "Conditional discounts", "Trigger-action rules", "Касови правила", "Маркетингови правила", "no enable disable button", "app has no active toggle"]
tags: [apps, marketing, automation, rules-engine, discounts]
plan_gates: ["cart_rules_total", "cart_rules_range", "cart_rules_conditions", "cart_rules_actions"]
created: 2026-05-22
updated: 2026-11-09
source_count: 9
---

# Cart Rules

## Purpose

**Cart Rules** (marketed as **Aura Cart Rules**) is a **trigger-and-action rules engine** that runs against every cart. Unlike simple [[marketing-discounts]] (one discount, one condition), it declares composite promotions — e.g. *"10% off when the cart has 3+ items from Vendor X AND total > 50 EUR"*, *"Buy 5, get the cheapest free"*, or tiered deals.

One rule can hold **multiple distinct deals** (called "rows"). Every cart at checkout passes through every active rule in **priority order** (sort order, descending). Matching rules **partially stack** — product-level matches accumulate on the targeted lines; cart-level matches are winner-takes-all (only the single highest-`value` cart-level match applies). Each row can carry a **customer message** (*"Add 6 EUR more for free shipping"*): a dashed box in the cart and the checkout summary, shown while the shopper has **not** reached that row — see [[cart-rules-stacking]] for exactly when it shows and [[apps-cart-rules-rules-editor]] for hiding it.

> This page is the **hub**. It defines what Cart Rules is, then points to focused aspect pages for every dimension. For deep dives, follow the wikilinks below — the body here does not repeat them.

> **No on/off control.** Once installed, the engine runs; its screen has no Enable / Disable switch. The installed-apps list may still show Cart Rules as **inactive**: that list reads the app record's on/off flag, which installing sets to off and which an app without a switch never changes. So *"the app is inactive"* never explains a rule not applying — check the rule itself, and use **Uninstall** to turn the app off.
>
> What *can* be switched off is an individual **rule** — every cart rule has its own Active / Inactive switch and its own date window, see [[cart-rules-cooldowns]].

## Where to find it

**Sidebar → Marketing → Apps → Cart Rules** (the link, marked with the app icon, opens the rules list). The **Cart rules** card under Marketing → Discounts → **Add discount** opens the same list; on a store without the app, the app's install screen shows instead. The Overview lives at `/admin/apps/cart-rules` (route `apps.cart-rules.overview`); the rules list + editor lives at `/admin/apps/cart-rules/rules` (route `apps.cart-rules.settings`) — see [[apps-cart-rules-rules]] for the list/editor UI specifics. Routes are namespaced under `apps.cart-rules.*` (overview / settings / create / edit). Admin API endpoints are at `/admin/api/cart-rules/...`.

## Sub-pages (in this cluster)

Split into 7 aspect pages, each one well-scoped slice. Drill into the matching aspect, not every page.

- [[cart-rules-conditions]] — the trigger taxonomy: cart / product / customer condition types, every `filter_type`, the three operator pools (numeric / string / record-set), `sub_value` rule.
- [[cart-rules-actions]] — `action_type=discount` with `value_type` `amount` / `percent` / `free_shipping`; action-trigger extras (`product_lowest_price`, `product_from_condition`, etc.); the `free_shipping` waybill-side caveat.
- [[cart-rules-scoping]] — what a rule applies to (whole cart vs. specific products / vendors / categories / tags / smart collections / customer groups); how scoping interacts with action triggers.
- [[cart-rules-stacking]] — cart-level winner-takes-all; product-level accumulation; **products consumed across rules**; interaction with [[marketing-discounts]]; the multi-row OR-fallback ladder.
- [[cart-rules-cooldowns]] — date-window gating (`active_from` / `active_to`); status states (Active / Inactive / Draft); priority via `sort_order`; **no per-customer cooldown exists**; no audit log; no usage cap.
- [[cart-rules-examples]] — 4 worked end-to-end scenarios (cart-total %, BOGO, VIP free shipping, tiered + free-shipping stack).
- [[cart-rules-known-issues]] — by-design vs bug catalogue: deleted-reference orphaning, identical-sort-order non-determinism, empty-row-trigger bug, `STATUS_DRAFT` inaccessibility, soft-delete with no restore, `value=0` still fires, `rows: maxItems` schema quirk, no audit log, A/B testing not supported.

## What the merchant can do here

- **Rules list** — every rule with status, date window, sort order, performance stats; drag-and-drop reorder; toggle status; soft-delete; *+ New rule* constructor; *+ Generate with AI* button.
- **Rule editor** — `name` (internal), `title` (customer-facing), `active_from` / `active_to`, No-expire toggle, status, `sort_order`. Each rule has many **rows**, each with a checkout message + triggers (AND) + one action. See [[cart-rules-conditions]] and [[cart-rules-actions]].

### What the merchant CANNOT do here

- Run actions other than discounts — `action_type` is fixed to **discount** (no auto-add free product, no upgrade shipping tier, no send notification).
- Trigger on browsing history, session length, or time-of-day. The filter taxonomy is fixed to cart / product / customer attributes (see [[cart-rules-conditions]]).
- Test a rule against a fake cart before activating — no simulator. Workaround: save it Inactive, briefly activate, test, set it back to Inactive. (Draft cannot be set in the admin — see [[cart-rules-known-issues]].)
- Bulk-edit rules; export / import rules; clone a rule (no Clone action).

## Settings & fields

This hub lists the top-level rule fields only. Field-level reference for **conditions** is on [[cart-rules-conditions]]; field-level reference for **actions** is on [[cart-rules-actions]].

| Field | Notes |
|---|---|
| `name` (max 191) | Internal label, not customer-facing |
| `title` (max 191, optional) | Customer-facing label shown at checkout + on the order detail screen |
| `active_from`, `active_to` (Y-m-d) | Optional start / end dates (store timezone) — see [[cart-rules-cooldowns]] |
| `status` | `1` Active, `0` Inactive, `2` Draft (Draft is API-inaccessible — see [[cart-rules-known-issues]]) |
| `sort_order` (0–100,000) | Priority; higher = evaluated first. New rules auto-set to highest + 1 |
| Rows | Up to `cart_rules_range` rows; each row holds triggers + one action + an optional checkout message |

## Business rules

The cross-cutting rules that span all aspects:

- **Rules evaluate in descending `sort_order`**, and the **date window applies first** — a rule outside its `[active_from, active_to]` window doesn't evaluate at all, even if status is Active. See [[cart-rules-cooldowns]].
- **Row evaluation = AND across triggers** — no OR within a row; use multiple rows or rules for OR. Multi-row rules are an **OR-fallback ladder, not accumulating tiers** — only ONE row per rule fires. See [[cart-rules-stacking]].
- **Products are consumed across rules** — once a rule matches a product, no later rule can match it; priority decides first pick. **Cart Rules + Discounts stack**: Cart Rules see the cart after product discounts and line-level codes from [[marketing-discounts]], and before order-level discounts. See [[cart-rules-stacking]].
- **Any admin can access** — no per-role gate; every staff member can create / modify / delete rules. **No audit log of edits** (only `created_at` / `updated_at` / `deleted_at`; no actor, no diff history). See [[cart-rules-known-issues]].
- **Value scale.** Enter the human value (`50` for 50 EUR, `10` for 10%); it is stored ×100, and quantities stay plain integers. Cart-level stacking compares the stored values across the two units — see [[cart-rules-conditions]] and [[cart-rules-stacking]].
- **Plan-tier gating — FOUR distinct limits** — `cart_rules_total`, `cart_rules_range`, `cart_rules_conditions`, `cart_rules_actions`, each individually expandable via feature packs. See [[plan-features]] + [[plan-vs-feature-pack]].

## Programmatic access

- **GraphQL — fully supported** at `/api/gql` (queries + create / update / status / delete / sort mutations). Status enum: `INACTIVE=0, ACTIVE=1, DRAFT=2` (but Draft cannot be set via create/update — see [[cart-rules-cooldowns]]); condition-type enum `PRODUCT, CART, CUSTOMER`; action value-type enum `AMOUNT, PERCENT, FREE_SHIPPING`. Operations on a store without the app installed return *"Cart Rules app is not installed."*
- **JSON-API v2 — NOT exposed.** No `/api/v2/*` resource; integrations must use GraphQL.
- **AI generation** (*+ Generate with AI*, `POST /admin/api/cart-rules/ai`) — admin-session only; calls OpenAI directly, not [[apps-cloudio-overview|Cloudio]]. `question` max 255 chars; failures show *"Unexpected error. Please try again later"*.

## Related

- [[apps]] — App Store hub.
- [[apps-cart-rules-rules]] — list + editor sub-page (UI specifics).
- [[cart-rule]] — Cart Rule entity (data model).
- [[marketing-discounts]] — simpler single-condition discounts; Cart Rules is for complex compositional logic. The two systems stack — see [[cart-rules-stacking]].
- [[marketing-discounts-shipping]] — Native Free shipping discount (contrast with Cart Rule `free_shipping` action — see [[cart-rules-actions]]).
- [[marketing-segments]] — customer segmentation (similar condition language).
- [[customers-custom-groups]] — customer groups referenced via `customer_group` record_type.
- [[customer-group-targeting]] — the concept: a customer-group condition here is the mechanism that gates payment / shipping methods per group.
- [[products-products]] / [[products-vendors]] / [[products-categories]] / [[products-tags]] / [[products-smart-collections]] — entities referenced by record-set filters.
- [[products-options-overview]] — product options referenced by `product_option` filter.
- [[apps-cloudio-overview]] — contrast: Cart Rules AI calls OpenAI directly, NOT Cloudio.
- [[orders-details]] — where applied cart-rule modifications surface on placed orders.
- [[discount-stacking]] — cross-system stacking rules across discounts, cart rules, and promo codes.
- [[plan-features]] / [[plan-vs-feature-pack]] — the four `cart_rules_*` caps + feature-pack expansion model.

## Open questions

None open. Aspect-specific open questions live on the aspect pages.
