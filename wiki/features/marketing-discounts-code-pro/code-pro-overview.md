---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Overview"
route_name: discounts-code_pro-list
route_path: /admin/marketing-new/discounts/code-pro/:id
aliases: ["Code PRO overview", "Code PRO vs Container", "Code PRO mini-campaigns", "Code PRO plan gates"]
tags: [marketing, discounts, code-pro, overview, plan-gates]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-code-pro]]. See the hub for the other aspects (form, fields, business rules, checkout, endpoints).

# Code PRO — overview, contrasts, plan-gating

## Purpose

This page explains **what makes Code PRO different** from the other coupon types CloudCart ships and which plan-gates control creation. Read this first when scoping a Code PRO campaign or when a merchant asks *"which coupon type should I use?"* or *"why can't I create a Code PRO discount?"*.

## Where to find it

The Code PRO discount type is created from [[marketing-discounts]] via **+ Add discount → Discount code (PRO)** card. The parent campaign uses route `discounts-create` with `type=code-pro`; the per-code management surface is the parent feature [[marketing-discounts-code-pro]].

## What the merchant can do here

Pick Code PRO as a discount type when each code needs its own terms. The decision tree:

- One code, one set of terms → **Promo code** (regular Discount with `type=code`).
- Many codes, all sharing the same terms (e.g., single-use coupons mass-generated) → **Container codes** ([[marketing-discounts-codes]]).
- Many codes, **each with its own terms** (e.g., influencer campaigns) → **Code PRO**.

### Each code is its own mini-campaign

Where a Container discount has many identical-terms codes, **a Code PRO discount has many independent codes** — each carries its own discount value, target, date window, customer-group restriction, region, `max_uses`, per-customer cap. The merchant builds them one at a time via the form (see [[code-pro-form]]) or in bulk via the generator ([[marketing-discounts-code-pro-generator]]) and they redeem entirely on their own merits. This is what makes Code PRO suited for influencer / affiliate campaigns: each partner gets a code with personalized terms, and the parent discount is just an organizational umbrella.

### Code uniqueness — store-wide on the Code PRO table

The `code` field is unique on `discounts_code_pro.code` — meaning if the merchant has two Code PRO campaigns, they **cannot share code strings between them**. Attempting to save a duplicate returns: *"Discount code is exists"* (`code_pro.validation.code.unique`).

This is **stricter than Container codes** (where each code is unique within the entire `discount_codes` table) and **stricter than regular Promo / Container parent codes** (where each `discounts.code` is unique on its own table). The three tables (`discounts.code`, `discounts_code_pro.code`, `discount_codes.code`) are independent — a string can theoretically exist once in each table, but the customer entering it at checkout would match whichever the lookup hits first.

Uniqueness is enforced by a **form-validation check at create time** (the `discounts_code_pro.code` column carries a plain, non-unique index — there is no database UNIQUE constraint). The check runs only when a **new** code is created; **editing** an existing code does not re-check uniqueness.

## Settings & fields

This page documents only the type-picker entry surface. For the per-code form fields see [[code-pro-fields]].

### Type-picker modal → "Discount code (PRO)" card

From the [[marketing-discounts]] list, **+ Add discount** opens the discount-type modal. The **Discount code (PRO)** card:

- If the `discount-code-pro` plan feature is currently enabled, routes to `discounts-create` with `type=code-pro` (creates the parent campaign).
- If the plan feature is NOT enabled, opens the shared **PlanFeature upgrade modal** with message *"To create a discount code, you need to upgrade your plan."* — a paywall before the user can even start.

The parent campaign form (`type=code-pro`) only has **one block: General settings** — status + name + a "Go to codes" link/banner. All discount terms live per-child-code; the parent is just a campaign umbrella.

## Business rules

### Plan-gating — three keys

Code PRO touches three plan-feature keys:

| Plan feature key | Gates | Default |
|---|---|---|
| `discount-code-pro` | Creating Code PRO parent discounts; per-code CRUD via [[code-pro-endpoints-api]]; segment / campaign integrations. | `1` (enabled at platform level via `restrict.defaults`); individual plans opt out by setting to `0`. |
| `discount-code-pro-generator` | The admin-panel bulk-generator batch-size cap (default 5,000 codes per request). | Plan-specific. |
| (none) | Adding / editing individual codes once a parent exists. | Unlimited per parent (subject to performance). |

On plans that have `discount-code-pro` disabled, the merchant cannot create a Code PRO discount through the admin panel, AND JSON-API v2 requests return **HTTP 403 Forbidden** with *"Not supported by plan"* (older wiki phrasing said 402; corrected).

The **bulk generator** consults `discount-code-pro-generator` only on the admin-panel path. **The JSON-API v2 bulk-generate endpoint has a hard-coded ceiling of 5,000 codes per request regardless of plan-feature value.** So a plan with `discount-code-pro-generator = 10000` will still be capped at 5,000 codes per call when invoked through the API — see [[code-pro-endpoints-api]]. To generate more, the integrator must issue multiple sequential calls.

### Permission

The page and all CRUD endpoints are protected by the standard `marketing.discounts` permission (the merchant role must have access to the Marketing → Discounts area).

### Per-code active flag — independent from parent

The PRO discount has its own `active` toggle (in [[marketing-discounts]] list), and **each code under it has its own `active` flag**. A code is redeemable only when BOTH are active. The merchant can pause one specific code (e.g., an influencer whose contract expired) without affecting the rest of the campaign — see [[code-pro-business-rules]] for the toggle mechanics and [[code-pro-checkout]] for the active-scope filter.

## How it works

The type-picker modal reads the `discount-code-pro` plan feature live (no caching) and switches between the create route and the upgrade modal at click time. Once the parent discount is saved, the "Codes management (N)" link appears on the [[marketing-discounts]] row and points to this cluster.

## Related

- [[marketing-discounts-code-pro]] — hub.
- [[marketing-discounts]] — parent feature; Code PRO is one of seven discount types.
- [[marketing-discounts-codes]] — Container codes (the "identical-terms mass-generated" alternative).
- [[discount]] — entity page for the parent Code PRO campaign.
- [[plan-gates]] — how plan-feature keys are evaluated at runtime.
- [[code-pro-endpoints-api]] — JSON-API v2 surface; same plan-gating.

## Open questions

No outstanding questions.
