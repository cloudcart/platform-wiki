---
type: entity
nav_path: "Entity → Customer Group → Lifecycle & deletion"
aliases: ["Customer Group lifecycle", "Delete customer group", "Cannot delete customer group", "Empty group cleanup", "Group deletion blocked", "Изтриване на клиентска група", "Жизнен цикъл на група"]
tags: [entity, customers, groups, lifecycle, deletion]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customer-group]]. See the hub for the other aspects (attributes, system groups, pricing & checkout, segmentation, API).

# Customer Group — Lifecycle & deletion

## Identity

This aspect documents the states a [[customer-group|Customer Group]] moves through — **created → active → empty → deleted** — and, critically, the rules that **block** deletion. Deletion is rejected while the group still has members or is referenced by a [[discount|Discount]]; the two reserved system groups can never be deleted at all. There is no "Archived" state.

## Aliases

- **Customer Group lifecycle** / **Жизнен цикъл на група** — the state-progression angle.
- **Delete customer group** / **Изтриване на клиентска група** — the deletion angle.
- **Cannot delete customer group** / **Group deletion blocked** — the error-message angle (when a merchant's delete fails).
- **Empty group cleanup** — finding and removing zero-member groups.

## Key Attributes

A Customer Group moves through these states:

1. **Created** — the merchant clicked + Add customer group, gave it a Name (see [[customer-group-attributes]]), saved. The group becomes available in the customer create / edit picker, the customer-list bulk **Set group** modal, the discount editor's group-restriction picker, the payment / shipping method editors' group-restriction picker, and the segment-builder's "Customer group" condition.
2. **Active** — the default state. The merchant assigns customers; the customer count climbs.
3. **Empty** — the group exists but has zero customers (`customers_count = 0`). Common after a re-grouping cleanup or when speculative groups were created. The **Has customers: No** filter on [[customers-custom-groups]] surfaces empty groups.
4. **Deleted** — the merchant deleted a single row or bulk-selected and deleted. Subject to the blocking rules below.

There is **no Archived state** — groups are either present or deleted. The merchant cannot "deactivate" a group; they either delete it (re-assigning its customers) or leave it in place.

### Delete is BLOCKED while the group has members or referencing discounts

Deletion is rejected outright when:

- the group still has customers → *"Cannot delete a customer group with customers"*, OR
- any [[discount|Discount]] still references the group → *"Cannot delete a customer group with discounts"*.

The merchant must clear **both** conditions first: bulk-reassign every customer in the group to another group (the customer-list bulk **Set group** action — see [[customer-group-segmentation]]) AND edit every referencing discount to remove the group. The exact backend error format for the discount case is *"Cannot delete customer group with discounts assigned to it. Edit discounts and try again! Group ID: {id}"* — the trailing `Group ID: {id}` tells the merchant which row to fix when bulk-deleting several groups.

The two reserved system groups (Default + Guests) are unconditionally undeletable — see [[customer-group-system-groups]].

### Dangling-reference risk: DiscountCodePro + Product Selections

Beyond the standard Discount module, Customer Groups are **also** referenced by two advanced features that the delete validator does NOT check:

- **DiscountCodePro** — the advanced discount-code engine has a per-code `customer_groups` filter (a separate `discount_code_pro_to_customer_group` link table).
- **Product Selections** (Smart Collections) — selections carry a `customer_group_id` column, so a merchant can show / hide entire product collections per group.

Deleting a group still referenced by a DiscountCodePro filter or a Product Selection succeeds but silently leaves a **dangling reference**. Defensive practice: manually clean up such references before deleting groups used in advanced discount or collection flows.

### Empty-group cleanup

Groups with zero customers are not auto-purged. The merchant uses the **Has customers: No** filter on [[customers-custom-groups]] to find them, then bulk-deletes. Each empty group still consumes one slot in the `customer_groups` plan count ([[plan-gates]]), so cleaning them up frees capacity to add new groups.

## Where it appears

- [[customers-custom-groups]] — the Delete control (single row + bulk), the **Has customers** filter, and where the deletion-block errors surface.
- [[customers]] — the bulk **Set group** action used to empty a group before deleting it.
- [[marketing-discounts]] — discounts that must be edited to remove the group reference before deletion.

## Related

- [[customer-group]] — hub.
- [[discount]] — referencing discounts block deletion.
- [[customer]] — members must be reassigned before deletion.
- [[plan-gates]] — empty groups still consume `customer_groups` slots.

## Open Questions

- ⏸️ Whether DiscountCodePro and Product-Selection references should also block group deletion (currently the delete validator only checks standard Discount references).
