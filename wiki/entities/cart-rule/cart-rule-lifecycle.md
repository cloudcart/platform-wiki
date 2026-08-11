---
type: entity
nav_path: "Entity → Cart Rule → Lifecycle"
aliases: ["Cart Rule lifecycle", "Cart Rule states", "Cart Rule soft-delete", "Cart Rule expiry"]
tags: [entity, marketing, automation, discounts, rules-engine, lifecycle]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Cart Rule — Lifecycle

> Part of [[cart-rule]]. See the hub for related aspects (fields, rows-and-triggers, actions, stacking, evaluation).

## Identity

The states a [[cart-rule|Cart Rule]] passes through, the save-time transitions the editor performs, and the absence of an audit trail / restore path.

## Aliases

- "Cart Rule lifecycle" / "Cart Rule states" — merchant-facing terms.
- "Cart Rule soft-delete" — the `deleted_at` flow and the missing Restore button.
- "Cart Rule expiry" — the `active_to`-driven date-window state.

## Key Attributes

Lifecycle is driven by these fields (defined verbatim on [[cart-rule-fields]]):

- **`status`** — `Active (1)` / `Inactive (0)` / `Draft (2)`.
- **`active_from`** / **`active_to`** — date-window gate; Expired is computed from `active_to`, not a separate status.
- **`deleted_at`** — soft-delete timestamp.
- **`created_at`** / **`updated_at`** — the only timestamps the platform records (no actor identity).

## States

A Cart Rule moves through these states:

1. **Draft** — `status = Draft (2)`. The model defines this state but **the merchant cannot set it via the standard create/update API or via GraphQL** (validation restricts status to 0/1). It is a defined-but-API-inaccessible state, preserved for historical compatibility. Effective lifecycle is binary (Active / Inactive) at the merchant-facing level.
2. **Active** — `status = Active (1)`. Evaluating against every cart at checkout. Date-window gating (`active_from` / `active_to`) still applies — Active outside the date window does nothing. See [[cart-rule-fields]] for the active-date-scope semantics.
3. **Inactive** — `status = Inactive (0)`. Paused; no effect. Carts proceed through checkout as if the rule didn't exist. The merchant flips Inactive when temporarily disabling a rule (e.g., end-of-promotion review before re-running).
4. **Expired** — Active but `active_to` past. Behaves like Inactive — no effect — but the merchant intent is *"this was a time-bound promotion that ended"*. The rule stays in the list with the date-window indicator showing it's expired. Not a separate status enum value — internally still `status = Active`; expiry is computed from the date window. Pushing `active_to` forward instantly re-activates the rule.
5. **Soft-deleted** — `deleted_at` set. Hidden from the [[apps-cart-rules]] list. The rule's data is preserved but **NO restore mechanism exists in the UI or API** — only direct database access by CloudCart support can recover a soft-deleted rule. Merchants who want a reversible "off" state should use **Inactive**, not Delete.

## Save-time transitions

- Status toggle on the list is **instant** — no save dialog. Flipping Active → Inactive (or back) takes effect immediately for all subsequent checkouts.
- Drag-and-drop reorder on the list updates `sort_order` for the affected rules in one operation — see [[cart-rule-stacking]].
- Editing a rule's content requires opening the editor — but rules can be edited even while Active (unlike [[campaign|Campaigns]], which are locked while Active). The merchant should be cautious — mid-edit reads see a rule in a half-changed state until save completes.

## No audit trail

The platform records only `created_at`, `updated_at`, `deleted_at` timestamps on the rule. There is no actor identity (no `created_by` / `updated_by`), no diff history, no revisions. *"Who disabled this rule last Thursday"* is unanswerable from the platform. Merchants who need compliance trails must keep their own log externally.

## Soft-delete is one-way without support

The trash icon on the list sets `deleted_at` (soft-delete). The rule disappears from the list. To restore a soft-deleted rule, the merchant must contact CloudCart support — there is no merchant-facing Restore button. Recovery exists for compliance / audit reasons but is not part of the regular workflow.

## Soft-deleted Cart Rules persist indefinitely

Once soft-deleted, a Cart Rule's row stays in the database with its `deleted_at` set. No automatic hard-purge job removes these rows on a schedule — the merchant cannot reclaim the database row without contacting CloudCart support to either restore (clear `deleted_at`) or hard-delete. For the merchant's day-to-day list, soft-deleted Cart Rules are invisible and do not affect storefront / cart logic.

## Soft-delete preserves analytics references

The `withStats` scope on the Cart Rule model joins against the `orders_modification` table to compute used-count and total-discount. Soft-deleted rules can still be queried — their old order modifications remain, so analytics for historical orders that triggered now-deleted rules continue to compute correctly. The merchant doesn't see the deleted rule in the list, but a historical order's discount line still references it for reporting. See [[cart-rule-evaluation]] for the `withStats` derivation.

## No simulator before activation

The merchant CANNOT test a rule against a fake cart before activating it. The workaround: save as Draft (where supported) → temporarily flip to Active → place a test order → flip back. There is no "preview" or "what-if cart" UI.

## No bulk actions, no clone, no export

Cart Rules don't support multi-select bulk actions on the list, can't be cloned (the merchant must recreate by hand), can't be exported / imported between stores. Each rule is constructed individually.

## Where it appears

- [[apps-cart-rules]] — list + editor; inline Active toggle; soft-delete trash icon.
- [[cart-rules-known-issues]] — the operational gaps (no clone, no simulator, no audit).

## Related

- [[cart-rule]] — hub.
- [[cart-rule-fields]] — `status`, `active_from`, `active_to`, `deleted_at` field definitions.
- [[cart-rule-evaluation]] — what runs while Active; `withStats` analytics.
- [[campaign]] — sibling that locks while Active (contrast).
- [[discount]] — sibling promotion entity with its own lifecycle.

## Open Questions

None.
