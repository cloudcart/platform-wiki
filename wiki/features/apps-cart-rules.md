---
type: feature
nav_path: "Apps → Cart Rules"
route_name: apps.cart-rules.overview
route_path: /admin/apps/cart-rules
aliases: ["Cart Rules", "Cart rules engine", "Conditional discounts", "Trigger-action rules", "Касови правила", "Маркетингови правила", "no enable disable button", "app has no active toggle"]
tags: [apps, marketing, automation, rules-engine, discounts]
plan_gates: ["cart_rules_total", "cart_rules_range", "cart_rules_conditions", "cart_rules_actions"]
created: 2026-05-22
updated: 2026-08-06
source_count: 8
---

# Cart Rules

## Purpose

**Cart Rules** is the merchant's most powerful marketing-automation tool — a **trigger-and-action rules engine** that runs against every cart at checkout. It is far more capable than simple [[marketing-discounts]] (one discount, one condition). Cart Rules let the merchant declare composite conditional promotions — e.g. *"10% off when the cart has 3+ items from Vendor X AND total > 50 EUR"*, *"Buy 5, get the cheapest free"*, or tiered stacked deals.

One rule can hold **multiple distinct deals** (called "rows"). Every cart at checkout passes through every active rule in **priority order** (sort order, descending). Matching rules **partially stack** — product-level matches accumulate on the targeted lines; cart-level matches are winner-takes-all (only the single highest-`value` cart-level match applies). Each row can show a **custom checkout message** to motivate the customer (*"Add 6 EUR more for free shipping"*) — it is customer-facing and shows on the cart and at checkout, so it is worth filling in on every rule as a built-in upsell (see [[apps-cart-rules-rules-editor]] for the guidance).

> This page is the **hub**. It defines what Cart Rules is, then points to focused aspect pages for every dimension. For deep dives, follow the wikilinks below — the body here does not repeat them.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be switched off is an individual **rule** — every cart rule has its own Active / Inactive / Draft status and its own date window, see [[cart-rules-cooldowns]].

## Where to find it

**Sidebar → Apps → Cart Rules.** The Overview lives at `/admin/apps/cart-rules` (route `apps.cart-rules.overview`); the rules list + editor lives at `/admin/apps/cart-rules/rules` (route `apps.cart-rules.settings`) — see [[apps-cart-rules-rules]] for the list/editor UI specifics. Routes are namespaced under `apps.cart-rules.*` (overview / settings / create / edit). Admin API endpoints are at `/admin/api/cart-rules/...`.

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
- Test a rule against a fake cart before activating — no simulator. Workaround: create as Draft, briefly activate, test, set back. (Draft state itself is API-inaccessible — see [[cart-rules-known-issues]].)
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
- **Products are consumed across rules** — once a rule matches a product, no later rule can match it; priority decides first pick. **Cart Rules + Discounts stack**: Cart Rules see the cart AFTER [[marketing-discounts]] apply (Discounts → Cart Rules on the discounted basis). See [[cart-rules-stacking]].
- **Any admin can access** — no per-role gate; every staff member can create / modify / delete rules. **No audit log of edits** (only `created_at` / `updated_at` / `deleted_at`; no actor, no diff history). See [[cart-rules-known-issues]].
- **Value scale — you enter the HUMAN value; it is stored ×100.** Send `50` for 50 EUR and `10` for 10% — the save step multiplies both by 100 (stored `5000` / `1000`). Quantities and counts are plain integers. Because money is then held in cents and percent as percent×100, the two are compared in **different units** during cart-level stacking — which is the root of the winner-takes-all gotcha. See [[cart-rules-conditions]] → *Value scale* and [[cart-rules-stacking]].
- **Plan-tier gating — FOUR distinct limits** — `cart_rules_total`, `cart_rules_range`, `cart_rules_conditions`, `cart_rules_actions`, each individually expandable via feature packs. See [[plan-features]] + [[plan-vs-feature-pack]].

## Programmatic access

- **GraphQL — fully supported** at `/api/gql` (queries + create / update / status / delete / sort mutations). Status enum: `INACTIVE=0, ACTIVE=1, DRAFT=2` (but Draft cannot be set via create/update — see [[cart-rules-cooldowns]]); condition-type enum `PRODUCT, CART, CUSTOMER`; action value-type enum `AMOUNT, PERCENT, FREE_SHIPPING`. Operations on a store without the app installed return *"Cart Rules app is not installed."*
- **JSON-API v2 — NOT exposed.** No `/api/v2/*` resource; integrations must use GraphQL.
- **AI generation** (*+ Generate with AI* button, `POST /admin/api/cart-rules/ai`) — admin-session only; calls OpenAI directly, NOT via [[apps-cloudio-overview|Cloudio]]. Request: `question` required, max 255 chars. Failures surface as *"Unexpected error. Please try again later"*.

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

None open. Currency handling and the simulator gap (with the Draft-activate-test workaround) are documented above. Aspect-specific open questions live on the relevant aspect page.
