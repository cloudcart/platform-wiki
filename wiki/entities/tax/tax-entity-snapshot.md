---
type: entity
nav_path: "Entity → Tax / Fee → Order snapshot lifecycle"
aliases: ["Tax snapshot", "Order tax snapshot", "Tax lifecycle", "Mid-order recompute", "Tax historical accuracy"]
tags: [entity, taxes, vat, snapshot, lifecycle, orders]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax]]. See the hub for the other aspects (attributes, VAT vs Fee, overrides, validation, business rules).

# Tax / Fee — order snapshot lifecycle

## Identity

How a Tax / Fee rule moves through the runtime — from "Defined" on [[settings-taxes]] to "Applied to an order" at checkout to "Snapshotted on the order" once persisted. The snapshot is the mechanism that keeps **historical invoices accurate** when the merchant later edits the rate, deletes the rule, or flips OSS. It is also the reason mid-order edits behave in a counter-intuitive way.

## Aliases

- **Tax snapshot** — the frozen tax breakdown written to the order row.
- **Order tax snapshot** — same, when emphasising the order side.
- **Mid-order recompute** — the exception where new line items use the CURRENT rule, not the snapshot.

## Key Attributes — the three lifecycle phases

| Phase | When it fires | Mutation site | Reverted by? |
|-------|---------------|---------------|--------------|
| **1. Defined** | Merchant saves the Tax / Fee row on [[settings-taxes]] | `taxes` row created / updated; Settings cache flushed | Deleting the rule. No webhooks, no notifications. |
| **2. Applied to a cart / order** | At checkout, the engine evaluates all rules against the customer's address + cart + payment / shipping pick | In-memory totals pipeline; no DB write yet | Customer abandons the cart; cart drops. |
| **3. Snapshotted on the order** | The order is persisted | Applied tax lines copied into the order's tax breakdown (rate, VAT flag, OSS flag, exemption reasons, resulting amount) | Nothing — the snapshot is immutable for the original line items. |

## Snapshot contents per applied tax line

Each tax line in the snapshot carries:

- **Rate** (the percent or flat value as applied — already overridden if a category / region override fired).
- **VAT flag** (was this a `vat = yes` rule).
- **OSS flag** (was OSS active when this line was computed — see [[tax-oss-semantics]]).
- **Exemption reasons** (the `without_vat_reasons` / `without_vat_reasons_non_eu` wording, frozen at snapshot time).
- **Resulting amount** (the actual currency amount applied to the line).

The snapshot does NOT carry a foreign key back to the Tax row. Deleting the parent Tax does NOT cascade — the snapshot stands independently.

## Why the snapshot exists — three concrete cases

**Case A — government raises VAT mid-year:**
Government raises VAT from 20% to 22%. Merchant edits the rule from 20% → 22%. **Existing orders keep their 20% on every download, credit note, export.** New orders from this point forward apply 22%.

**Case B — merchant deletes a rule:**
Merchant cleans up an old rule that's no longer needed. **Orders that applied it before deletion still print the line on their invoices** — the rule's existence is not required after the snapshot is taken.

**Case C — merchant edits the exemption wording:**
Merchant rewrites the `without_vat_reasons` text to match a new legal directive. **Existing orders keep their old wording on already-printed invoices.** Only orders placed after the edit show the new wording.

## Mid-order recompute — the exception

When the merchant adds a product to an **existing** `pending` / `paid` / `authorized` Order (via the [[orders-details]] line-items editor), the new line item is NOT taxed from the snapshot. Instead:

- The engine re-runs the picker against the **current** Tax / Fee rules.
- The new line uses **whatever rate is in force right now**.
- OSS flag changes also apply to the new line — the snapshot covers only the originally-created lines.

This can produce **mixed-rate Orders**:

- Order placed Jan 1 with 5 lines at 20% VAT (snapshotted).
- Merchant adds a 6th line on Feb 1 after VAT rose to 22%.
- The order now has 5 lines at 20% + 1 line at 22%. The invoice prints both rates.

Merchants who don't expect this often raise tickets — *"Why does my order have two different VAT rates?"* The answer is that mid-order edits use current rules, by design, to reflect the current legal rate at the time the line was added.

## No delete protection from existing orders

Deleting a Tax / Fee rule does NOT retroactively affect existing orders (because they hold the snapshot). The merchant can safely clean up old rules — but they should be careful not to delete a rule that's still needed for new orders, since deletion is immediate. There is no warning UI on delete.

## Settings cache flushed on save

Saving a Tax / Fee rule flushes the platform Settings cache so the next checkout picks up the new rule immediately. No queue, no notifications, no webhooks from this screen — the change is visible on the very next checkout request.

## Where it appears

- [[order]] — the order row holds the snapshot.
- [[orders-details]] — every order's totals section displays the per-line and total tax breakdown from the snapshot.
- [[orders-invoice]] — invoices print snapshot values.
- [[orders-credit]] — credit notes reverse from the snapshot.
- [[orders-receipt]] — cash receipts use the snapshot.
- [[tax]] — entity hub.

## Related

- [[tax]] — hub.
- [[tax-entity-attributes]] — the rule fields that get snapshotted.
- [[tax-order-snapshot]] — concept-side detail on the snapshot mechanism.
- [[tax-rate-selection]] — picks the rule whose values get snapshotted.
- [[tax-oss-semantics]] — OSS flag at snapshot time.
- [[orders-details]] — mid-order recompute trigger (the line-items editor).
- [[order-processing-pipeline]] — where the snapshot fits in the order timeline.

## Open Questions

None.
