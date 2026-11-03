---
type: feature
nav_path: "Plan → Feature → Buy → Checkout flow"
route_name: plan-feature-packs
route_path: /admin/plan/feature/:id
aliases: ["Plan feature buy flow", "Feature pack checkout side panel", "Buy feature pack checkout", "Post-purchase quota refresh", "Dynamic-pricing pack id", "Купи пакет — плащане"]
tags: [plans, plan-feature, feature-pack, checkout, purchase, vue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-feature]]. See the hub for the other aspects (pack list, plan restrictions, pack lifecycle).

# Plan feature — buy → checkout flow

## Purpose

This aspect covers what happens **after** the merchant clicks **Buy** on a pack row: the checkout side panel opens with the chosen pack pre-loaded, the merchant runs the standard payment flow, and on success the calling [[plan-features]] card updates its quota in place — without a refetch. It also covers the per-open usage recompute and the dynamic-pricing pack-id format that lets the checkout charge the right quantity.

## Where to find it

- Triggered from the **Buy** button on any pack row in [[plan-feature-detail-pack-list]], on the `/admin/plan/feature/{id}` screen.
- The checkout itself renders as a side panel layered above the *Plan feature* panel (the parent panel grows to size `xll` while checkout is open).

## What the merchant can do here

- **Open the checkout side panel** for the selected pack by clicking *Buy* (or *Upgrade* on a numeric feature).
- **Complete payment** through the standard Order overview / Invoice / Payment / Discount / Totals / Pay-now flow (shared with [[plans-purchase]]).
- **Return to the pack list** — the checkout's Cancel header button is renamed **Back to overview** to signal the merchant goes back to the pack list, not the merchant home.

## Settings & fields

No editable fields beyond the standard checkout panel inputs (invoice details, payment method, discount code — all documented in [[plans-purchase]]). The pack is pre-seeded; the merchant does not re-pick a quantity here.

The Buy action seeds the checkout with:

| Field | Value |
|-------|-------|
| `type` | `pack.model_type` (e.g. `cloudcart_feature`) |
| `mapping` | `pack.id` (for dynamic-pricing, the `<pack_id>_<value>` form) |
| `value` | `pack.value` (the quota contribution) |

## Business rules

### Per-feature usage recomputed on each open

When the merchant opens the *Plan feature* screen, the backend computes a fresh **usage** record for the feature: `{ total: <plan_value + active_pack_values>, used: <current usage>, remaining: <total − used> }`. Storage gets a special breakdown with file count + free / total bytes. The pre-existing cache is bypassed for this load so the merchant sees up-to-date numbers.

### Buy → 50ms-delayed checkout open

Clicking *Buy feature* / *Upgrade*:
1. Sets `pack = { type: pack.model_type, mapping: pack.id, value: pack.value }`.
2. `setTimeout( => { this.buyPanel = true; }, 50)` — opens the checkout panel after a 50ms delay to avoid a race between the parent panel's close animation and the checkout open.
3. The checkout panel renders with `record: pack` and `type: pack.model_type`, and the merchant runs the standard pay-now flow.
4. On success, the screen emits a `success` event with the checkout result to its parent.

### Dynamic-pricing pack id carries the quantity

For features with `dynamic_pricing = 1`, each pack row's `id` is formatted as `<pack_id>_<value>` (e.g. `42_500`, `42_1000`, `42_2000`). The checkout endpoint detects this pattern, loads the pack model by the first segment, and pulls the matching quantity from the dynamic-pricing ladder (see [[plan-feature-detail-restrictions]] for how the ladder is generated). This is how a single pack record backs many priced quantity steps.

### Post-purchase in-place quota refresh

When checkout returns success and the panel closes, the parent [[plan-features]] list updates the affected feature card **without re-fetching**:
- For numeric features, the pack's `value` is added to both `usage.total` and `usage.remaining`.
- For boolean features, both are flipped to `true`.

The merchant sees the new quota immediately on the card they bought from.

### Cache flush after purchase

After a successful pack purchase, the plan-feature value cache is flushed for the affected feature so subsequent gate-checks elsewhere in the admin see the new effective quota right away. See [[plan-gates]].

### Max-value rejection stays on-screen

If the buy would push total quota past the feature's `max_value`, the backend rejects the cart-add with the localised `plan.plan_limit` message and the merchant stays on the screen (no checkout opens). See [[plan-feature-detail-restrictions]].

## Related

- [[plan-feature]] — hub.
- [[plan-feature-detail-pack-list]] — the table whose *Buy* button starts this flow.
- [[plan-feature-detail-restrictions]] — the `max_value` rejection + dynamic-pricing ladder behind the pack id.
- [[plan-feature-detail-pack-lifecycle]] — what the resulting subscription does over time (renewal, cancel, downgrade survival).
- [[plans-purchase]] — the shared checkout side-panel flow.
- [[plan-features]] — the parent card that updates in place on success.
- [[billing-cards]] — saved card used during checkout.
- [[plan-gates]] — gate-check cache flushed after purchase.

## Open questions

None.
