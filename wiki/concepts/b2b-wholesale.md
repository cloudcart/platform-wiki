---
type: concept
nav_path: "Concept → B2B & wholesale selling"
route_name: (none)
route_path: (none)
aliases: ["B2B", "Wholesale", "B2B selling", "Wholesale store", "Trade pricing", "Group pricing", "На едро", "B2B магазин", "Търговия на едро", "Фирмени клиенти", "Ценови групи", "Private store"]
tags: [b2b, wholesale, customer-groups, pricing, concepts, hub]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---
# B2B & wholesale selling

## Definition

**B2B & wholesale selling** is configuring the store for business buyers rather than (or alongside) retail shoppers — differentiated pricing, company / VAT invoicing, restricted access, and fast bulk ordering. The backbone is the [[customer-group]] entity: every customer belongs to exactly one group, and the group drives **pricing**, **checkout restrictions**, and **segmentation**.

## Scope

- **Customer groups** — define groups (Wholesale, VIP, B2B) on [[customers-custom-groups]]; assign each customer to one group (per-customer on [[customers-details]] or bulk on [[customers]]).
- **Group pricing** — express wholesale prices as group-targeted [[marketing-discounts]] (e.g. "15% off for Wholesale").
- **Checkout restrictions** — payment ([[settings-payment-providers]]) and shipping ([[settings-shipping]]) methods can be gated to specific groups (wholesale sees invoice-on-delivery; retail sees card only).
- **Company / VAT invoicing** — B2B billing fields (company name, VAT ID) on the billing address feed the invoice — see [[invoicing-and-accounting]].
- **Restricted / trade-only storefront** — [[apps-private-store]] hides the store (or parts) behind login.
- **Fast bulk ordering** — [[apps-fast-order]] lets buyers add many SKUs quickly.

## Contrasts

- **Group vs tag/segment.** A customer belongs to exactly ONE [[customer-group]] (drives price + checkout); tags / segments are many and drive *marketing* only.
- **Private store vs customer group.** [[apps-private-store]] controls *visibility* (who can see the store); the group controls *price & checkout* once they are in.
- **Wholesale price = discount, not a second price column.** There is no separate B2B price field on the product — wholesale pricing is expressed as group-targeted [[marketing-discounts]], not a parallel price list. (Common misconception worth flagging.)

## Where it applies

- Group assignment per customer ([[customers-details]]) or in bulk ([[customers]]).
- Company / VAT invoices — see [[invoicing-and-accounting]].
- Group-gated payment & shipping at checkout.

## Related

- [[customer-group-targeting]] — the full set of levers a customer group drives (pricing, checkout-method gating, segments).
- [[customer-group]] — the entity at the centre of B2B.
- [[customers-custom-groups]] — where groups are created.
- [[marketing-discounts]] — group-targeted pricing.
- [[apps-private-store]] / [[apps-fast-order]] — trade-only access + bulk ordering.
- [[invoicing-and-accounting]] — company / VAT invoices.

## Open Questions

- Per-group **fixed price lists** do NOT exist — verified against code. The group record carries no price; differentiated pricing is achieved only via group-targeted [[discount|Discounts]] (incl. free-shipping discounts + [[marketing-discounts-code-pro|Code PRO]]). See [[customer-group-targeting]].
- Whether a customer can be auto-assigned to a group on registration by rule (verify).
