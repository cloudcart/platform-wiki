---
type: concept
nav_path: "Concept → Customer-group targeting"
aliases: ["Customer group targeting", "Customer groups", "Group-based differentiation", "What customer groups do", "Group pricing and checkout", "B2B group differentiation", "Wholesale group pricing", "Таргетиране по клиентска група", "Клиентски групи — за какво служат", "Диференциация по група"]
tags: [customers, groups, b2b, pricing, discounts, cart-rules, segmentation, concepts]
plan_gates: ["customer_groups"]
created: 2026-06-14
updated: 2026-06-23
source_count: 2
---

# Customer-group targeting (how customer groups differentiate the store)

## Definition

A **customer group** is a single label every customer carries (`customer.group_id`) — *"Retail"*, *"VIP"*, *"Wholesale"*, *"B2B"*, *"Loyalty Gold"*. The group record itself is intentionally thin (just `id` + `name` — see [[customer-group-attributes]]); it stores **no** price, discount, or allow-list. Its power comes from being a **gate** that *other* features point back at: discounts, Cart Rules, and segments each carry a customer-group reference, and the platform evaluates them against the buyer's current group at checkout / send time.

So the question *"what can customer groups do?"* is really *"which features can be conditioned on a group?"* — and the answer is a surprisingly wide set of levers, all driven from one label the merchant assigns once.

## Scope

Covered: the levers a group drives (pricing, checkout-method gating, Cart-Rule behaviour, segmentation), where membership is assigned, and the order-snapshot rule. The group taxonomy screen is [[customers-custom-groups]]; the data model is the [[customer-group]] entity cluster.

Not covered: the B2B store model end-to-end ([[b2b-wholesale]]); discount stacking order ([[discount-stacking]]); the Cart-Rule engine internals ([[apps-cart-rules]]); subscriber vs customer ([[subscriber-vs-customer]]).

## The levers — what a group can drive

1. **Differentiated pricing → group-targeted discounts.** The CloudCart pattern for *"Wholesale = 30% off everything"* is a [[discount]] of type `percent` with a `customer_group_ids` filter, not a price field on the group. Regular discounts, [[marketing-discounts-code-pro|Code PRO]] codes, and **free-shipping** discounts all accept a group filter. At checkout the discount query keeps only discounts whose group filter is empty (all customers) or matches the buyer's group.
2. **Payment- / shipping-method show-hide → [[apps-cart-rules|Cart Rules]].** A Cart Rule with a **customer-group condition** shows or hides payment and shipping methods per group — e.g. *Invoice (deferred payment)* only for B2B, *Same-day courier* only for a "Local Sofia" group. This is the real mechanism; payment providers and shipping methods carry **no** customer-group field of their own.
3. **Any group-conditioned cart behaviour → Cart Rules.** Beyond show/hide, a group-conditioned rule can add a fee, attach a gift, or surface an offer — anything the Cart-Rule action set supports.
4. **Targeted marketing → segments + campaigns.** A [[marketing-segments|segment]] can use *Customer group = X* as a condition, and campaigns send to that segment — the durable way to reach "all VIPs".
5. **Cohort analytics + admin filtering.** Reports filter by group for cohort comparison (see [[reports-customers]]); the [[customers]] AND [[orders]] lists can both be filtered by customer group; and the order webhook payload carries the customer's `group_id`.

## Contrasts

- **Group vs customer tag / custom field** — a customer has exactly **one** group (mutually exclusive buckets) but many tags. Groups gate pricing/checkout/segments; [[customers-custom-fields|tags & custom fields]] are free-form metadata that don't gate checkout.
- **Group condition vs category cart-restriction** — per-category payment/shipping restrictions ([[products-categories-cart-restrictions]]) gate by the **products in the cart**, not by **who** the customer is. Group gating (via Cart Rules) is the customer-side equivalent.
- **Group vs segment** — a group is a manually-assigned, durable bucket; a [[marketing-segments|segment]] is a rule-computed audience that *can include* group as one of its conditions.

## Where it applies

- **Assignment** — new registered customers default to **Default** (id 1); guest checkouts fall into **Guests** (id 2); the merchant moves customers per-customer ([[customers-details]]) or in bulk (*Set group* on [[customers]]). See [[customer-group-system-groups]].
- **Configuration** — the group filter on [[marketing-discounts]] / Code PRO; the customer-group condition on [[apps-cart-rules]]; the group condition on [[marketing-segments]].
- **Evaluation** — at checkout ([[checkout-flow]]) the buyer's group decides which discounts apply and which Cart Rules fire. The storefront **search index is group-aware**: it pre-computes per-group discounted prices and per-group smart-collection membership (merging each group's rows with the global / no-group defaults), and storefront pages are cached in a **separate bucket per group** for guests / crawlers (signed-in customers bypass the full-page cache and always render fresh — see [[storefront-arch-caching-invalidation]]) — so group-differentiated pricing stays both correct and fast. See also [[apps-listing-engine]].
- **Snapshot** — the order freezes `customer_group_id` at order time. Moving a customer to a new group does **NOT** re-price or re-flag past orders — differentiation is only evaluated at the moment of each checkout. See [[customer-group-pricing-checkout]].

## Related

- [[customer-group]] — the entity (data shape, system groups, lifecycle, API).
- [[customers-custom-groups]] — the admin screen where groups are created / renamed / deleted.
- [[b2b-wholesale]] — the B2B / wholesale store model that leans on group pricing.
- [[discount-stacking]] — how the group-targeted discounts combine with others.
- [[apps-cart-rules]] — the customer-group condition that gates payment / shipping.
- [[marketing-segments]] — group as a segment condition for campaigns.
- [[customer-group-pricing-checkout]] — the per-aspect detail on pricing + checkout gating + the order snapshot.
- [[plan-gates]] — the `customer_groups` cap on how many groups a plan allows.
- [[checkout-flow]] — where group membership is evaluated.

## Open Questions

None.
