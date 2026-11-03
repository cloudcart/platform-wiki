---
type: feature
nav_path: "Customers → Customer groups → System groups & delete protection"
route_name: customers-custom-groups
route_path: /admin/customers/groups
aliases: ["System customer groups", "Default group", "Guests group", "Protected groups", "Delete protection", "Cannot delete group", "Системни клиентски групи"]
tags: [customers, groups, protection, delete, system]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Customer groups — system groups & delete protection

> Part of [[customers-custom-groups]]. See the hub for the other aspects (manage, plan gating, integration, API).

## Purpose

Explains the two **protected system groups** (Default and Guests), why the merchant must never delete or rename them, and the **layered delete-confirmation matrix** that protects every group with customers or referencing discounts. This is the page to read for any *"why can't I delete this group?"* support question.

## Where to find it

Sidebar → Customers → **Customer groups** (`/admin/customers/groups`). The protection logic runs when the merchant bulk-selects rows and triggers the **Delete** action.

## What the merchant can do here

The merchant can bulk-select rows aggressively and trigger Delete — the platform safely deletes only the eligible groups and **filters out** any protected group before sending the request. The confirmation message adapts to the selection:

| Scenario | Confirmation message |
|----------|----------------------|
| 1 group selected, neither system nor has customers | *"Are you are sure you want to delete? Caution: This action cannot be undone."* |
| 1 group selected, it IS group 1 or 2 (system) | *"You cannot delete this group, because it is main one."* (Confirm disabled) |
| 1 group selected, it has customers | *"You cannot delete this group, because it has customers."* (Confirm disabled) |
| Multiple selected, some system + some with customers | *"You cannot delete a main group or a group with customers, only other groups will be deleted."* |
| Multiple selected, some have customers | *"One or more selected groups have clients in it. They will be ignored from delete."* |

What the merchant **cannot** do: delete the Default or Guests group, rename the Default group, or delete any group that still has customers or referencing discounts.

## Settings & fields

There are no settings on this aspect — it is enforcement behaviour. The relevant data is the group's id (1 / 2 mark the system groups) and the live **Customers** count surfaced in the list (see [[customers-custom-groups-management]]).

## Business rules

### The two protected system groups (verified names)

The platform reserves two groups by **literal name**:

- **Default** — group id 1; the group every newly registered storefront customer is assigned to.
- **Guests** — group id 2; the group every guest checkout (no registration) is bucketed into.

The merchant must **never rename** these — the platform looks them up *by name* for signup and guest checkout, so a rename would break those flows. The assignment behaviour itself is documented on [[customers-custom-groups-integration]].

### Cannot-delete protection on the system groups

Both are protected at the data layer, with dedicated errors:

- Deleting the Default group → *"Cannot delete the default group"*.
- Deleting the Guests group → *"Cannot delete the guests group"*.

These blocks cannot be bypassed — the same protection applies via JSON-API v2 (see [[customers-custom-groups-api]]).

### Default is also un-editable (not just un-deletable)

A non-obvious protection: the merchant cannot **rename** the Default group. Any edit attempt on it is rejected with *"Cannot edit default group"*. The merchant **can** rename Guests via the admin REST endpoint. (Note: the JSON-API v2 adapter blocks renaming *both* Default and Guests at the entity-update level, while the admin REST endpoint blocks only Default — verify which path the current admin UI uses.) *(verify)*

### "Default" is a reserved name — even creating a new group with it is blocked

Trying to create a new group named *"Default"* (or *"default"*, *"DEFAULT"* — case-insensitive comparison) is rejected with *"Group name is reserved"*. The platform protects the literal string "Default" as a system identifier even if the existing system group were somehow removed.

### Delete cascade blocked by BOTH customers AND discounts

A group cannot be deleted while it still has customers **or** while any discount rule targets it:

- Group with customers → *"Cannot delete customer group with customers assigned to it. Edit customers and try again!"*
- Group referenced by a discount → *"Cannot delete customer group with discounts assigned to it. Edit discounts and try again!"*

So the safe cleanup flow is: (a) edit any discount in [[marketing-discounts]] to remove the group from its target scope, (b) bulk-reassign customers on the [[customers]] list to another group, and only then (c) delete the group from [[customers-custom-groups-management]].

### Self-healing on every fresh deployment

If an instance somehow loses its Default or Guests group (e.g. a DB restore from before the seed), the platform recreates it on next reference — keyed by name. New installs and after-restore scenarios are self-healing.

## Related

- [[customers-custom-groups]] — hub.
- [[customers-custom-groups-integration]] — how Default / Guests assignment happens on signup and guest checkout.
- [[customers-custom-groups-api]] — the same protection layer applies via JSON-API v2.
- [[customers]] — bulk-reassign customers before deleting a group.
- [[marketing-discounts]] — re-scope discounts before deleting a group.
- [[customer-group]] — entity page.

## Open questions

- Whether the current admin UI uses the JSON-API adapter (blocks renaming both Default and Guests) or the admin REST endpoint (blocks only Default). *(verify)*
