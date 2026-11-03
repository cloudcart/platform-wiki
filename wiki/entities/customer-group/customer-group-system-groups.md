---
type: entity
nav_path: "Entity → Customer Group → System groups"
aliases: ["Default customer group", "Guests group", "System customer groups", "Reserved group name", "Guest checkout group", "Системни групи", "Група Гости", "Група по подразбиране"]
tags: [entity, customers, groups, guests, system]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customer-group]]. See the hub for the other aspects (attributes, pricing & checkout, lifecycle & deletion, segmentation, API).

# Customer Group — System groups

## Identity

Two [[customer-group|Customer Groups]] exist by default on every store and are **platform-controlled**: the **"Default"** group (literal English name `Default`) into which newly registered customers fall, and the **"Guests"** group (literal English name `Guests`) into which every guest checkout falls. Neither can be deleted, and the Default group rejects any edit. This aspect documents both system groups plus the case-insensitive reservation of the *"Default"* name.

## Aliases

- **Default customer group** / **Група по подразбиране** — the registered-customer default.
- **Guests group** / **Guest checkout group** / **Група Гости** — the anonymous-buyer bucket.
- **System customer groups** / **Системни групи** — both together.
- **Reserved group name** — the *"Default"* name-reservation rule.

## Key Attributes

| System group | Literal name | Role | Protection |
|--------------|--------------|------|------------|
| **Default** | `Default` (English on all-language stores, NOT localised) | The group new registered customers default into. | Cannot be deleted (*"Cannot delete the default group"*); cannot be renamed / edited (*"Cannot edit default group"*). |
| **Guests** | `Guests` (English, literal) | The group every guest checkout's Customer record is assigned to. Typically ID 1 or 2 depending on store age. | Cannot be deleted (*"Cannot delete the guests group"*). |

### Every customer belongs to exactly one group

The customer's `group_id` is a required FK. Newly registered customers default to **Default**; guest checkouts default to **Guests**. The merchant can manually reassign registered customers per-customer via [[customers-details]] or in bulk via the customer-list action — see [[customer-group-segmentation]] for the bulk **Set group** flow.

### Guests is a one-way trap

The platform reserves the Guests group for the guest-checkout flow. The merchant CANNOT:

- Delete the Guests group.
- Reassign the platform-default that guests fall into.
- Move registered customers INTO the Guests group (it is a one-way trap for the guest flow).

The Guests group is the merchant's primary filter for distinguishing one-time anonymous buyers from registered repeat customers.

### The name "Default" is reserved (case-insensitive)

The platform refuses to create or rename any group to **"Default"** (or `default`, `DEFAULT`, `Default ` — the validator lower-cases then uppercase-first-letters the input before comparing). The error is *"Group name is reserved"*. Even if the existing Default group were somehow gone, the merchant cannot reclaim that name for a custom group — this keeps the auto-recreated "Default" group identifiable across merchants.

### The name "Guests" is NOT reserved (but the Guests group itself can't be deleted)

The reservation applies **only** to "Default". A merchant CAN create a custom group named *"Guests"* — the validator does not block it. However, the system-owned Guests group that the platform auto-creates remains undeletable regardless of any name match. So a store can technically end up with the platform's Guests group plus a merchant-made "Guests" group; only the platform one is protected.

## Where it appears

- [[customers-custom-groups]] — the group list shows the Default + Guests rows; their Edit / Delete controls are disabled or error out.
- [[customer]] — every customer's `group_id` resolves to one of these two system groups unless reassigned.
- [[checkout-flow]] — guest checkout writes the Customer record into the Guests group.

## Related

- [[customer-group]] — hub.
- [[customer]] — carries the `group_id` that defaults to a system group.
- [[customer-group-lifecycle-deletion]] — the full deletion-blocking ruleset (system groups are the unconditional case).
- [[checkout-flow]] — guest checkout assigns the Guests group.

## Open Questions

- ⏸️ Whether the "Guests" group can be renamed by the merchant in any UI surface (currently appears to be platform-controlled).
