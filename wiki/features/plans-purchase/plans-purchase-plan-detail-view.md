---
type: feature
nav_path: "Profile → Plan: {current-plan} → Plan detail"
route_name: admin.plan.show
route_path: /admin/plan/{mapping}
aliases: ["Plan detail", "Plan details page", "Plan feature breakdown", "Plan inventory view", "Read-only plan view", "Детайли на плана", "Преглед на план"]
tags: [plans, pricing, features, read-only, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[plans-purchase]]. See the hub for the other aspects (billing cycle, recommended add-ons, checkout panel, business rules, subscription outcomes, discount codes).

# Plans purchase — plan detail (read-only)

## Purpose

The **plan detail** view shows the **full feature breakdown** for a single plan as a read-only inventory — one section per feature group, with the plan's value for each feature listed. There is **no purchase form** on this view. It's the screen the *Plan* badge in the profile dropdown links to ("Plan: Start Up" → click to see what *Start Up* includes), or a deep-link merchants use to compare a target plan against their current limits.

Both the detail view and the purchase flow share the same Smarty templating + the same currency / VAT formatting, so they're related via the [[plans-purchase]] hub.

## Where to find it

- **Profile dropdown → Plan badge** — clicking *Plan: <current-plan-name>* opens the detail page for the merchant's current plan (`/admin/plan/{mapping}`).
- **Direct URL** — `/admin/plan/{mapping}` for any plan, e.g. `/admin/plan/cc-pro`, `/admin/plan/business`, `/admin/plan/startup`.
- **NOT** linked from the catalog *Upgrade now* button — that button goes to `/admin/plan/{mapping}/purchase` (see [[plans-purchase-billing-cycle]]).

The `{mapping}` segment is the plan's URL slug — stable identifiers: `startup`, `basic`, `cc-pro`, `business`, `enterprise`, `unicorn`.

## What the merchant can do here

- See every active feature group + the plan's value for each feature row.
- Use the breadcrumb back to [[plans]] to return to the catalog.
- Read what a plan includes WITHOUT being funnelled into a purchase form.

What the merchant **cannot** do here:

- Buy the plan from this screen — there is no submit button.
- Edit any field — every value is read from the plan-details catalog.
- See features that are flagged as hidden for this plan (filtered out — see Business rules).

## Settings & fields

| Field shown | What it represents |
|-------------|--------------------|
| **Breadcrumb** | *Plans → <plan-name>* (the *Plans* link returns to [[plans]]) |
| **Feature groups** | One section per active feature group (Resources, Branding, Reports, Support, etc.) |
| **Feature row** | Two-column row: feature name (left) + plan's value (right), e.g. *Products — 500* or *Custom hostname — ✗* |
| **No purchase button** | The detail view is purely informational — no form, no submit |

## Business rules

### Feature rows filtered by hidden-features table

The feature-row list is filtered through the *hidden features* table: rows where the (plan × feature) pair is flagged hidden don't render at all. This keeps the breakdown clean for plans where certain features simply don't apply (instead of rendering them as ✗ everywhere). See [[plan-features]] for the underlying feature catalog.

### Free-plan record swap for DE

When a German merchant requests `/admin/plan/startup` (with or without `/purchase`), the platform notices `mapping = startup` + `issuer_company = DE` and substitutes the DE Starter plan record (ID 60 — *(verify)*) with the label *14-Tage-Test (Starter)* before rendering. So the detail view actually shows the DE Starter plan's feature breakdown under the *Start Up* URL, branded as a 14-day Starter trial.

The free-plan record swap for other countries is unchanged — they see the normal Start Up breakdown.

### Plans without active billing variants → 404

If a plan exists but has no priced details (all variants inactive), the detail URL throws a not-found error. The catalog listing also filters those plans out, so a merchant should never get there organically — but a deep-link to a soft-deleted plan would 404.

### Side-panel layout hides admin chrome

The detail screen renders as a **side panel** (open-from-right overlay) over the admin panel rather than full-page navigation. The side-panel header has a close (×) button that returns the merchant to `/admin` (the dashboard). The standard sidebar nav, top-bar nav, breadcrumb-bar, user-account dropdown, and help button are hidden while the panel is open — the merchant focuses on the breakdown without distraction. There's no back button to the [[plans]] catalog inside the panel itself; the merchant uses the breadcrumb at the top.

### Pricing read-only — no override

Every figure shown is read from the plan-details catalog row. The merchant cannot override price, period, currency, or VAT — the detail view is purely informational.

## Related

- [[plans-purchase]] — hub.
- [[plans]] — the catalog listing of plans.
- [[plan-features]] — per-feature purchase flow (buying extra quota beyond the plan's limit, e.g. more products / customers without changing tier).
- [[plan-feature]] — individual feature entity.
- [[plan-gates]] — how the limit-reached / feature-not-enabled screens funnel merchants toward the purchase flow.
- [[plans-purchase-billing-cycle]] — the sibling purchase flow at `/admin/plan/{mapping}/purchase`.
- [[account-plan]] — alternative entry into the plan management UI.

## Open questions

None.
