---
type: concept
nav_path: "Concept → Backups and restore → Partial restore"
aliases: ["Partial restore", "Segment-based restore", "Append-only restore", "Partial restore segments", "Nine-segment restore picker", "Частично възстановяване", "Append-only бекъп"]
tags: [backups, ops, restore, partial-restore, append-only, concepts]
plan_gates: ["backups", "partial_restore"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[backups-and-restore]]. See the hub for the other aspects (cadence, subscription gates, retention, full restore, safety backup, concurrency).

# Backups — partial restore

## Definition

**Partial restore** is a separate add-on subscription (`partial_restore` pack on top of the base `backups` pack) that lets the merchant pick which of nine data segments to restore — and it is **append-only**: only records missing from the live store are restored from the backup, existing records are NEVER overwritten. The storefront stays live; no maintenance mode is enabled. The merchant ticks the segments they need from a picker form and the platform enforces dependency rules so an inconsistent partial restore cannot be submitted.

The most-misunderstood detail is the "append-only" nature: partial restore can recover **deleted** records but cannot undo **edits** to existing ones. A merchant who accidentally changed the price on 500 products yesterday cannot fix it with partial restore — the records still exist in the live store, and partial restore won't overwrite them. For edit recovery the merchant needs [[backup-restore-full-restore]] (with all the post-backup data loss that implies).

The info box on the partial-restore dialog states this explicitly: *"Only missing records will be restored. Existing data in your store will not be overwritten. A safety backup will be created before restoring."*

## Scope

Covered:

- The append-only semantics (missing records added, existing records untouched).
- The nine selectable segments and what each covers.
- The dependency-enforcement rules (auto-selection in the picker + server-side rejection).
- The no-storefront-downtime guarantee.
- The safety-backup auto-creation before every partial restore.
- The cancellation rule (partial restores ARE cancellable).

Not covered here:

- The `partial_restore` add-on subscription gate — see [[backup-restore-subscription-gates]].
- Full-database replacement restore — see [[backup-restore-full-restore]].
- The safety backup itself — see [[backup-restore-safety-backup]].
- 2FA gate, concurrency, cancellation mechanics — see [[backup-restore-concurrency]].

## Contrasts

- **Partial restore vs. Full restore**: partial ADDS missing records (storefront stays up); full REPLACES everything (storefront goes down). Partial cannot undo edits; full can. See [[backup-restore-full-restore]].
- **Append-only vs. Merge**: append-only means "do nothing if the record exists" — there is no field-level merge that combines pre- and post-backup values. The record is either restored (if missing) or untouched (if present).
- **Segment-level granularity vs. per-record granularity**: the merchant picks which of nine segments to restore, NOT individual products / orders / customers. To restore 5 specific deleted products, the merchant ticks the Products segment and ALL deleted products in that segment are restored.

## Where it applies

### Partial restore — additive only, segment-based, dependency-enforced

The optional `partial_restore` pack adds a per-backup **Partial Restore** action on [[settings-backups]] that opens a segment-picker form. The merchant ticks which of nine segments to restore from the backup:

| Segment | What it covers (merchant-facing) | Auto-requires |
|---------|----------------------------------|---------------|
| **Categories** | Product categories + category access restrictions | — |
| **Vendors** | Brand / vendor records | — |
| **Customer Groups** | Customer-group definitions | — |
| **Properties** | Product properties (color, size, material) + their option lists | Categories |
| **Products** | Products + variants + all attached product data (parameters, quantities, bundles, collections, comparisons, files, banners, labels, smart selections, linked products, quantity discounts, upsell/cross-sell, tags, suppliers) | Categories, Vendors, Properties |
| **Customers** | Customer accounts + addresses + custom fields + saved cards + tags | Customer Groups |
| **Orders** | Orders + line items + addresses + discounts + fulfillments + payments + shipping + history | Customers, Products |
| **Discounts** | Discount rules + codes + Pro discount targets + cart rules | Customer Groups |
| **Pages** | CMS pages + content + page-history snapshots | — |

The picker shows dependencies visually and **auto-selects required segments** when the merchant ticks a dependent segment. Ticking Orders automatically ticks Customers and Products; ticking Products automatically ticks Categories, Vendors, and Properties. The picker cannot be saved with a dependency missing.

The platform also **enforces dependencies server-side** — submitting Orders without Customers and Products is rejected with a validation error. So the merchant cannot accidentally start an inconsistent partial restore via API or a stale browser session.

### Append-only — never overwrites existing records

Partial restore is **append-only**: only records that DON'T exist in the live store are restored. Existing records are NEVER overwritten. So partial restore can:

- Recover deleted products (their IDs and references come back exactly).
- Recover deleted customers (their full account history is reconstructed).
- Recover deleted orders (with the historical line items, addresses, etc.).
- Recover deleted categories / vendors / properties.
- Recover deleted CMS pages.

But partial restore CANNOT:

- Undo a price edit (the product still exists, so the existing record stays untouched).
- Undo a customer-address change (the customer still exists).
- Undo a stock decrement (the variant still exists).
- Undo a settings change (settings rows are existing records).
- Merge field-level values from snapshot and live.

For any of those, the merchant needs [[backup-restore-full-restore]] — accepting the post-backup data loss.

### Storefront stays live during partial restore

Unlike full restore, partial restore does NOT enable maintenance mode and does NOT replace existing records. The storefront stays live; customers can keep browsing and checking out while the restore runs. The trade-off is the append-only constraint — the merchant gets uninterrupted service but loses the ability to undo edits.

### Safety backup before every partial restore

Like full restore, partial restore also creates a safety backup before running. The info box on the partial-restore dialog states: *"Only missing records will be restored. Existing data in your store will not be overwritten. A safety backup will be created before restoring."* See [[backup-restore-safety-backup]] for the safety-backup mechanics.

The safety backup is useful for partial restores too: if the additive merge produced unexpected results (e.g., a restored deleted product now conflicts with a manually re-created one), the safety backup lets the merchant roll back to the pre-restore state.

### Only partial restores are cancellable

Partial restores can be cancelled while running — the merchant clicks Cancel on the active-restore banner on [[settings-backups]] or on [[settings-queue-view]]. The platform stops the additive merge, drops any orphaned temporary databases the partial restore created, and removes the safety backup that was auto-created for the cancelled restore (so a cancelled partial restore leaves no trace in the list).

Full restores cannot be cancelled from the admin. See [[backup-restore-concurrency]] for the cancellation rules.

### Partial restore is subscription-gated

Partial restore requires a separate `partial_restore` pack subscription ON TOP of the base `backups` subscription — see [[backup-restore-subscription-gates]].

## Related

- [[backups-and-restore]] — hub.
- [[settings-backups]] — the admin screen with the Partial Restore action.
- [[backup-restore-full-restore]] — the alternative (full database replacement; storefront down).
- [[backup-restore-safety-backup]] — auto-created before every partial restore.
- [[backup-restore-subscription-gates]] — the `partial_restore` add-on gate.
- [[backup-restore-concurrency]] — cancellation rules and 2FA gate.
- [[backup]] — the backup entity.

## Open Questions

None — all previously-flagged items in this aspect resolved.
