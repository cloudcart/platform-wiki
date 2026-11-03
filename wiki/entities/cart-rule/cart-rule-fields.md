---
type: entity
nav_path: "Entity → Cart Rule → Fields"
aliases: ["Cart Rule fields", "Cart Rule attributes", "Cart Rule schema", "Cart Rule data model"]
tags: [entity, marketing, automation, discounts, rules-engine, fields]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Cart Rule — Fields

> Part of [[cart-rule]]. See the hub for related aspects (rows-and-triggers, actions, stacking, lifecycle, evaluation).

## Identity

The verbatim attribute catalogue for the [[cart-rule|Cart Rule]] entity — what the merchant edits on [[apps-cart-rules]], the validation strings the platform applies, and the computed-but-not-editable fields the listing surfaces.

## Aliases

- "Cart Rule fields" / "Cart Rule attributes" — common merchant-facing references in support tickets.
- "Cart Rule schema" / "Cart Rule data model" — when devs ask about the columns.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** (`name`) | Required, max 191 chars | Internal label for the merchant's reference — NOT shown to customers. Used to find the rule in the list. |
| **Title** (`title`) | Optional, max 191 chars | Customer-facing — displayed at checkout when the rule applies. Used for transparency ("Loyal Customer Deal Applied"). |
| **Status** (`status`) | `Active` / `Inactive` / `Draft` | Active = evaluating against every cart. Inactive = paused, no effect. Draft = saved but never fires. Toggle inline via the switch column on [[apps-cart-rules]] (no save needed — instant). See [[cart-rule-lifecycle]] for the Draft API restriction. |
| **Active from** (`active_from`) | Optional start date (Y-m-d) | When set, the rule does NOT fire before this date. NULL = always-on from creation. |
| **Active to** (`active_to`) | Optional end date (Y-m-d) | When set, the rule auto-deactivates after this date. NULL = no expiry. The **No expire** toggle nulls this field. |
| **Sort order** (`sort_order`) | Priority (integer 0–100,000) | Higher = evaluated first. New rules auto-set to `MAX(sort_order)+1` on `creating` (top priority by default). Drag-and-drop reorder on the list. See [[cart-rule-stacking]]. |
| **Rows** (multi-deal capability) | One rule can have many rows | Each row is an independent **trigger-set + action + message** combo. See [[cart-rule-rows-and-triggers]] for the OR-fallback semantics. |
| **Performance stats** | Auto-counted | Per-rule counters of how many times the rule fired and how much revenue it influenced. Surfaced on the [[apps-cart-rules]] list. See [[cart-rule-evaluation]] for the `withStats` derivation. |
| **`deleted_at`** | Soft-delete timestamp | When set, the rule is hidden from the list. Recovery requires support — no Restore button in UI. See [[cart-rule-lifecycle]]. |
| **`status_key`** (computed) | `active` / `inactive` / `draft` | Auto-derived from the `status` integer (1/0/2). Surfaced in the listing for filtering, not directly editable. |
| **Active date scope** | Internal eligibility filter | A rule is treated as active by the cart-engine when ALL of these are true: `status = Active` AND (`active_from` is blank OR `active_from` ≤ today) AND (`active_to` is blank OR `active_to` ≥ today). Date comparison uses the **store's timezone**, not UTC — so a rule's "active until" date ends at midnight in the store's timezone, not in UTC. |

The per-row fields — `triggers`, `action`, `action value type` (`percent` / `amount` / `free_shipping`), `message`, `sorting` — live on row records owned by the rule. See [[cart-rule-rows-and-triggers]] + [[cart-rule-actions]].

## Where it appears

- [[apps-cart-rules]] — list + editor where these fields are surfaced.
- [[cart-rules-conditions]] — per-row trigger field shape.
- [[cart-rules-actions]] — per-row action field shape.

## Related

- [[cart-rule]] — hub.
- [[cart-rule-rows-and-triggers]] — row sub-entity with its own field set.
- [[cart-rule-actions]] — row's action sub-record.
- [[cart-rule-lifecycle]] — how `status` + `active_from` / `active_to` interact.
- [[cart-rule-stacking]] — how `sort_order` controls evaluation order.

## Open Questions

None.
