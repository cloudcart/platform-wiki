---
type: feature
nav_path: "Profile → Choose plan → (downgrade behavior)"
route_name: plans
route_path: /admin/plans
aliases: ["Plan downgrade", "Downgrade flow", "Lower plan", "Plan switch limits", "Over-quota records after downgrade", "Понижаване на план"]
tags: [plans, pricing, downgrade, plan-gates]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[plans]]. See the hub for the other aspects (catalog display, country / partner filtering, LTA override, free-plan expiry, plan-feature cache).

# Plans — downgrade behavior

## Purpose

This page documents what happens when a merchant **switches from a higher plan to a lower plan** through the standard catalog — there is no separate "downgrade" UI, no warning modal, and no special button. The same **Upgrade now** CTA on the cheaper plan's card triggers the downgrade. This page covers the four merchant-visible consequences: no proration, no data cleanup, immediate gate enforcement on new creates, and the path back from over-quota state.

## Where to find it

`/admin/plans`. The downgrade flow uses the same `PlansList` cards + matrix + Choose button → [[plan-details]] side-panel → [[plans-purchase]] checkout as any other plan change. Nothing on the catalog visually distinguishes a downgrade from an upgrade — the button just says **Choose `{plan name}`** in both directions.

## What the merchant can do here

- **Switch to any cheaper plan** through the same Choose → checkout flow as an upgrade.
- **Keep all their existing records** (products, customers, etc.) after a downgrade — nothing is deleted.
- **Continue editing existing records** that are over the new plan's quota — only NEW creates are blocked.
- **Upgrade back** at any time to lift the lower-plan gates without losing data.

## What the merchant cannot do here

- **Get a prorated refund** for the unused portion of their current higher plan — proration is not applied. The merchant pays the full new-plan price on the next billing cycle; the higher plan's already-paid period is **not refunded**. (verify)
- **Create new records over the new plan's limit** — every gate-checked entity (products, customers, administrators, etc.) blocks new creates immediately. See [[plan-gates]].
- **Receive a confirmation modal warning about over-quota records** before confirming the downgrade — the flow goes straight from card click → side-panel → checkout, with no "you currently have 750 products but the Starter plan only allows 500, are you sure?" interrupt. (verify)
- **Bulk-delete over-quota records automatically** — there is no platform-side cleanup. The merchant must manually delete records to drop below the new limit, or accept the editing-only state.

## Settings & fields

This is a flow, not a screen with fields. The relevant data points the merchant sees:

| Where | What |
|-------|------|
| **[[plans-catalog-display|Plan card CTA]]** | *Choose `{plan name}`* — same button for upgrades and downgrades |
| **[[plan-details]] side-panel** | Shows the new plan's headline features + billing cycle picker |
| **[[plans-purchase]] checkout** | Confirms the new plan + cycle + add-ons; no separate downgrade-confirmation step |
| **After-checkout** | Plan badge in profile dropdown updates immediately; the new plan's gates take effect |
| **Over-quota gates** | When the merchant tries to create a new product / customer / etc. beyond the new limit, the gate error from [[plan-gates]] fires |

## Business rules

### Same flow as upgrade — no proration

The catalog screen does NOT visually distinguish downgrades from upgrades. Both go through the same **Choose `{plan name}`** button → [[plan-details]] side-panel → [[plans-purchase]] checkout flow. There is no separate confirmation step that says "you're downgrading — are you sure?".

There is no proration. The merchant pays the new plan's price on the next billing cycle. The remaining time on the higher plan is not refunded. (verify)

### Over-quota records are preserved on disk

After a downgrade is paid:

- All existing records (products, customers, administrators, etc.) that exceed the new plan's limit are **preserved**. Nothing is deleted, archived, or hidden.
- Existing over-quota records remain **visible and editable** in the admin panel. The merchant can update an existing product even if the product count exceeds the new plan's limit.
- The over-quota records also remain **visible on the storefront** — customers can still browse and order them.

This is intentional: deletion is destructive and the merchant might just be temporarily downgrading.

### Lower gates apply IMMEDIATELY to new creates

The instant the downgrade payment processes:

- **Creates of NEW records beyond the lower limit are blocked**. Trying to add a 501st product on a 500-product plan returns the gate error from [[plan-gates]].
- The plan-feature cache is flushed (the platform code per [[plans-cache-and-demo]]), so the new limits are picked up on the next gate-check with no stale window.
- The Plan badge in the profile dropdown shows the new plan name immediately.

### Path back from over-quota

To unblock creates after a downgrade, the merchant has two options:

1. **Delete excess records** to drop below the new limit. Once the count is at-or-below the limit, creates work again.
2. **Upgrade back** through the same `/admin/plans` flow. The higher plan's limits take effect immediately and the over-quota state goes away.

The platform does NOT auto-clean records. The platform does NOT automatically pick which records to delete. The merchant decides.

### Feature toggles also downgrade immediately

Plan-gated boolean features (e.g. multi-variant products via the `multi_variants` gate) flip OFF as soon as the downgrade is paid. Existing multi-variant products remain in the catalog but the merchant cannot create new ones until they upgrade again. The same applies to every other plan-gated feature — see [[plan-gates]] for the full enforcement model.

### Add-on packs survive a plan switch

If the merchant had purchased a [[plan-features|feature pack]] (e.g. extra product quota beyond the plan limit), the pack survives the plan switch — its quota is **added on top of** the new plan's base value at the next gate-check. See [[plan-features-subscription-lifecycle]] for the pack lifecycle and [[plans-cache-and-demo]] for how the layered values are computed.

## Related

- [[plans]] — hub.
- [[plans-purchase]] — the checkout flow downgrades use.
- [[plan-details]] — side-panel opened on Choose click.
- [[plan-gates]] — the gate-enforcement system that blocks new over-quota creates.
- [[plans-cache-and-demo]] — feature-cache flush that makes the new gates effective instantly.
- [[plan-features]] — feature packs that survive a plan switch.
- [[plan-features-subscription-lifecycle]] — pack lifecycle.
- [[merchant-subscription-lifecycle]] — broader merchant-support hub for plan / billing questions.

## Open questions

(All resolved.)
