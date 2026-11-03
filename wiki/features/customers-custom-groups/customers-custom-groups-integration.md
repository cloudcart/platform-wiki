---
type: feature
nav_path: "Customers → Customer groups → Integration & lifecycle"
route_name: customers-custom-groups
route_path: /admin/customers/groups
aliases: ["Customer group integration", "Group assignment on signup", "Guest group assignment", "Customer group caching", "Merge customer groups", "Интеграция на клиентски групи"]
tags: [customers, groups, integration, lifecycle, caching]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Customer groups — integration & lifecycle

> Part of [[customers-custom-groups]]. See the hub for the other aspects (manage, system groups, plan gating, API).

## Purpose

How customer groups wire into the rest of the platform: which group new customers and guests land in, where the group taxonomy is consumed (dropdowns, discounts, segments, filters), how group records are cached, what webhooks (don't) fire, and how to merge two overlapping groups when there is no native merge tool.

## Where to find it

Sidebar → Customers → **Customer groups** (`/admin/customers/groups`) defines the taxonomy; the *consumption* points are spread across [[customers]], [[marketing-discounts]], [[marketing-segments]], and the storefront signup / checkout flow.

## What the merchant can do here

Adding a group from [[customers-custom-groups-management]] makes it **immediately available** across every consuming surface — no extra publish step. The merchant uses those surfaces to act on the group:

- Assign a customer to a group via the Add Customer modal or the per-customer Edit modal on [[customers]].
- Bulk-reassign customers between groups via the [[customers]] list bulk action **"Change customer's group"**.
- Target a group with a promotion in [[marketing-discounts]].
- Build a segment that filters by group in [[marketing-segments]].

## Settings & fields

No settings live on this aspect — it documents wiring, not configuration. The single relevant data point is each customer's `group_id`, which the consuming surfaces read and write.

## Business rules

### Lifecycle assignment (who lands where)

- **Registered customers** → the **Default** group (id 1). When a customer signs up via the storefront, the registration flow assigns the Default group automatically.
- **Guest checkouts** → the **Guests** group (id 2). A customer who completes checkout without registering is bucketed here.

There is **no merchant configuration** to change which group new customers go into — it is fixed at the flow level. The system groups themselves are documented on [[customers-custom-groups-system-groups]].

### Consumption surfaces (where the taxonomy is used)

- **Add / Edit Customer** on [[customers]] — the "Customer group" dropdown is populated from this taxonomy.
- **[[customers-details]]** — the customer's group is shown as a badge on the identity card.
- **[[marketing-discounts]]** — targeting uses customer groups as a scope rule.
- **[[marketing-segments]]** — segment rules can use customer group as a field.
- **[[customers]] list filter** — filters by customer group.

### Caching

- **System groups (by id)** — cached with a 24-hour TTL on save (insert or update); deleting the group clears its cache.
- **Guests lookup** — additionally cached for 1 hour, layered with a per-request in-memory cache, so guest-group resolution stays fast on every guest checkout.

### Webhooks — group lifecycle is silent

Group create / delete does **not** fire a dedicated webhook — there is no `customer_group.*` event. Only `customer.updated` fires when an individual customer moves between groups (per [[settings-hooks]]). Receivers wanting to react to a customer's group change should listen for `customer.updated`.

### No native merge tool

If the merchant ends up with two overlapping groups (e.g. *"VIP"* and *"VIPs"*), there is no one-click merge. The flow is: (a) use the [[customers]] bulk action **"Change customer's group"** to move all customers from the duplicate into the canonical group, then (b) delete the now-empty duplicate from [[customers-custom-groups-management]] (subject to the delete protection on [[customers-custom-groups-system-groups]]).

### Used vs total groups

The page tracks two metrics: **total groups** (all defined groups) and **used groups** (groups with at least one customer, used for analytics views). The *Has customers* list filter surfaces the same distinction.

## Related

- [[customers-custom-groups]] — hub.
- [[customers-custom-groups-management]] — where groups are created (then appear in these dropdowns).
- [[customers-custom-groups-system-groups]] — Default / Guests definitions referenced by the assignment flow.
- [[customers]] — Add / Edit Customer, group filter, and the "Change customer's group" bulk action.
- [[customers-details]] — group badge on the customer card.
- [[marketing-discounts]] — discount targeting by group.
- [[marketing-segments]] — segment rules by group.
- [[settings-hooks]] — `customer.updated` webhook (no dedicated group event).

## Open questions

None.
