---
type: entity
nav_path: "Entity → Customer Group → Segmentation & bulk assignment"
aliases: ["Customer Group segmentation", "Bulk set group", "Group-based segment", "Group marketing targeting", "Reassign customers in bulk", "Сегментиране по група", "Масово задаване на група"]
tags: [entity, customers, groups, segments, marketing, webhooks]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customer-group]]. See the hub for the other aspects (attributes, system groups, pricing & checkout, lifecycle & deletion, API).

# Customer Group — Segmentation & bulk assignment

## Identity

This aspect documents how a [[customer-group|Customer Group]] is used as the **durable segmentation pivot** for marketing — the merchant labels customers with a group, builds a [[segment|Segment]] on *Customer group = X*, and targets a [[campaign|Marketing Campaign]] at that segment. It also covers the bulk **Set group** action that moves cohorts of customers between groups, and the webhook behaviour when a customer's group changes.

## Aliases

- **Customer Group segmentation** / **Group-based segment** / **Сегментиране по група** — the segment-builder angle.
- **Bulk set group** / **Reassign customers in bulk** / **Масово задаване на група** — the cohort-migration action.
- **Group marketing targeting** — the campaign-targeting use case.

## Key Attributes

### Group is the primary segmentation pivot for ad-hoc cohorts

When the merchant wants to email *"all wholesale customers"*, the workflow is:

1. Ensure all wholesale customers are in the Wholesale group (using bulk **Set group**, below).
2. Create a [[segment|Segment]] with condition *Customer group = Wholesale*.
3. Target a [[campaign|Marketing Campaign]] at that segment.

Customer Groups are the **durable label**; Segments are the **dynamic filter** that uses the label. This is the key contrast: a group is a static, exactly-one-per-customer assignment, whereas a segment is a query whose membership flexes with the underlying data.

### Bulk-assign happens on the customer list

The Customers list ([[customers]]) supports row selection + a bulk **Set group** action — the merchant picks a target group and applies it to all selected customers in one call. This is the primary tool for migrating cohorts between groups (e.g., promoting all customers with >5 completed orders to "Loyalty Gold"). It is also the way to **empty** a group before deleting it — see [[customer-group-lifecycle-deletion]].

The merchant can also reassign a single customer's group from the per-customer Edit screen on [[customers-details]].

### Group vs tags vs segments

A Customer Group is distinct from neighbouring grouping mechanisms:

- **Customer tags** — free-form and many-per-customer. A merchant attaches many tags to one customer ("VIP", "Tech-savvy", "Sofia") but assigns exactly one group.
- **[[segment|Segments]]** — dynamic subscriber filters; membership flexes as data changes. Groups are static labels that persist regardless of behaviour.
- **Roles / staff permissions** — govern admin users, not storefront customers. Customer Groups are 100% about storefront customers.

### Group changes fire `customer.updated` (no dedicated event)

When the merchant moves a Customer between groups — or a Cart Rule / sign-up flow auto-assigns a group — the platform fires the `customer.updated` webhook event ([[settings-hooks]]). There is **no dedicated `customer.group_changed` event**; receivers must compare the customer's `customer_group_id` against their last-seen snapshot to detect the change. The group entity itself has no `customer_group.*` webhook — group lifecycle (create / edit / delete) is silent.

## Where it appears

- [[customers]] — the customer list with row selection + bulk **Set group**.
- [[customers-details]] — per-customer group reassignment.
- [[marketing-segments]] — segment-builder *Customer group = X* condition.
- [[reports-customers]] — analytics filtered by group for cohort comparison.
- [[settings-hooks]] — `customer.updated` fires on group reassignment.

## Related

- [[customer-group]] — hub.
- [[segment]] — the dynamic filter built on group membership.
- [[campaign]] — targets group-defined segments.
- [[customer]] — the entity whose `customer_group_id` change fires `customer.updated`.
- [[notification-delivery]] — group membership influences which campaigns reach which subscribers.

## Open Questions

None.
