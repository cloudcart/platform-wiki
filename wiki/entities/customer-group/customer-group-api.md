---
type: entity
nav_path: "Entity → Customer Group → JSON-API v2"
aliases: ["Customer Group API", "Customer groups JSON-API", "Customer group plan cap", "Group limit reached", "customer_groups plan feature", "API за клиентски групи", "Лимит на групи"]
tags: [entity, customers, groups, json-api, plan-gated]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customer-group]]. See the hub for the other aspects (attributes, system groups, pricing & checkout, lifecycle & deletion, segmentation).

# Customer Group — JSON-API v2 & plan cap

## Identity

This aspect documents **programmatic access** to [[customer-group|Customer Groups]] via JSON-API v2, the fact that API writes hit the **same protection layer** as the admin UI, and the `customer_groups` **plan cap** — including the quirk that both system groups consume slots from the merchant's allowance.

## Aliases

- **Customer Group API** / **Customer groups JSON-API** / **API за клиентски групи** — the programmatic angle.
- **Customer group plan cap** / **`customer_groups` plan feature** / **Лимит на групи** — the plan-gating angle.
- **Group limit reached** — the error string a merchant / integration hits at the cap.

## Key Attributes

### Read / create / update / delete via JSON-API v2

Customer groups can be read, created, updated, or deleted via JSON-API v2 — see [[api-customer-groups]] for the endpoint shape, the `name` attribute (max 100 chars, case-insensitive unique — see [[customer-group-attributes]]), and the `customers_count` aggregate.

**Same side effects apply.** A POST / PATCH / DELETE through JSON-API v2 hits the same protection layer as the admin UI: the 24-hour group cache is invalidated on save, the Guests-lookup 1-hour cache is refreshed, and the delete validator enforces *both* the "no customers" AND "no referencing discounts" rules (see [[customer-group-lifecycle-deletion]]).

**Reserved-name + system-group protection applies via API too** (see [[customer-group-system-groups]]):

- Creating or renaming any group to **"Default"** (case-insensitive — `Default`, `default`, `DEFAULT`) → HTTP 422 *"Group name is reserved"*.
- Renaming the Default group itself → *"Cannot edit default group"*.
- Deleting the Default group → *"Cannot delete the default group"*; deleting Guests → *"Cannot delete the guests group"*.

**No `customer_group.*` webhook** — group lifecycle is silent. Customer-side group reassignment fires `customer.updated` only (no dedicated `customer.group_changed` event — see [[customer-group-segmentation]]).

**Dangling-reference risk via API**: like the admin UI, the API delete validator only checks standard [[discount|Discount]] references — NOT DiscountCodePro or Product Selections. Clean those up manually before deleting referenced groups.

### Plan cap: `customer_groups` count

The plan-feature key `customer_groups` caps how many custom groups the merchant can create. The page header on [[customers-custom-groups]] shows *"X of Y groups used"* (with ∞ for unlimited plans); clicking + Add when at cap opens the upgrade modal instead. Server-side, the overflow check returns *"Group limit reached"*.

**Known quirk — system groups consume slots.** The cap check counts ALL groups, **including** the two system groups (Default + Guests). So a plan that allows e.g. "3 customer groups" effectively gives the merchant **1 custom group** (3 total minus the 2 system groups). The page-header "X of Y used" display reflects this — both system groups occupy slots from the merchant's perspective. If a plan says "5 customer groups", the merchant actually gets **3** custom ones.

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Where it appears

- [[api-customer-groups]] — the JSON-API v2 endpoint for groups.
- [[json-api-v2]] — auth, rate limit, and the shared side-effects principle.
- [[customers-custom-groups]] — the admin surface showing the "X of Y groups used" plan-cap header.
- [[plan-gates]] — the `customer_groups` feature key.

## Related

- [[customer-group]] — hub.
- [[api-customer-groups]] — the endpoint shape.
- [[json-api-v2]] — the API platform.
- [[plan-gates]] — the `customer_groups` count cap.
- [[discount]] — the only reference type the delete validator checks.

## Open Questions

None.
