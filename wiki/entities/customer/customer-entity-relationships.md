---
type: entity
nav_path: "Entity → Customer → Relationships"
aliases: ["Customer relationships", "Customer orders", "Customer addresses", "Customer groups", "Customer subscriber overlap", "Customer tags", "Customer custom fields"]
tags: [entity, customers, relationships, addresses, groups, subscriber]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customer]]. See the hub for the other aspects (attributes, lifecycle, status flags, auth + email, API + webhooks).

# Customer — Relationships

## Identity

How a [[customer|Customer]] record connects to the rest of the platform — orders, addresses (billing + shipping), customer group, tags, subscriber segments, custom fields, favorites, social accounts, saved payment cards, carts, and message queues. Also documents the Customer / Subscriber boundary — the single most confusable distinction in this part of the schema.

## Aliases

- **Customer relationships** — the foreign-key + pivot relations.
- **Customer-Subscriber overlap** — the boundary between the two records.
- **Customer addresses** — multi-address management with one default per type.

## Key Attributes

A Customer:

- **Has many** [[order|Orders]] via `customer_id` — the customer's full order history. The detail page surfaces them as the **Orders** sub-tab ([[customers-details-orders]]).
- **Has many** order payments — pass-through via Orders → OrderPayment. Surfaced as the **Payments** sub-tab ([[customers-details-payments]]).
- **Has many** **shipping addresses** (`CustomerShippingAddress`) — multiple addresses supported per customer. `default_address_id` picks the default. Managed on [[customers-details-shipping-addresses]].
- **Has many** **billing addresses** (`CustomerBillingAddress`) — multiple supported. `default_billing_address_id` picks the default. Managed on [[customers-details-billing-addresses]].
- **Belongs to one** [[customer-group|Customer Group]] via `group_id` — required. Customer-groups carry discount tier, price visibility, and admin-side segmentation.
- **Belongs to many** customer **tags** (the platform's customer-tag table, separate from product tags) — filter and segment by tag.
- **Belongs to many** [[segment|Subscriber Segments]] via the `subscriber_to_segments` pivot — when the customer is also a Subscriber, segment memberships are tracked here.
- **Has many** **custom field** values (`CustomField`) — per-merchant custom fields defined on [[customers-custom-fields]] (e.g., "VAT number", "Company size"). Each value is keyed by customer-id + field-id.
- **Has many** favorites — products the customer has marked as favorites (see [[products-favorite-products]]).
- **Has many** saved payment cards (`CustomerCard`) — tokenised cards saved through provider integrations. See [[customer-entity-auth]] for security guarantees.
- **Has many** [[cart|Carts]] via `user_id` — abandoned and active carts (deleted in cascade when the customer is hard-deleted; see [[customer-entity-lifecycle]]).
- **Has many** abandoned-cart records ([[cart|AbandonedCart]]) when they leave items behind without completing checkout.
- **Has many** social-account links (`SocialAccount`) — Facebook / Google / Apple login bindings. See [[customer-entity-auth]].
- **Has many** Mobica-sent messages — SMS / Viber transactional and marketing messages sent to this customer's phone.
- **Has many** marketing-queue entries (Mailchimp, NewsletterQueue) when applicable.

### Multi-address rules

Customers carry **separate shipping and billing address collections**. Both can have multiple entries:

- `default_address_id` (shipping) and `default_billing_address_id` (billing) pick the default-at-checkout.
- The **first address** the customer creates is auto-set as the default for that type.
- **Deleting the default** requires re-picking another default (or clears the pointer when no other addresses exist).

### Customer ≠ Subscriber — the canonical confusion

A Customer **is referenced by** but is NOT the same as [[subscriber|Subscriber]]. A Subscriber is anyone with marketing consent on at least one channel; a Customer is anyone who has placed an order or registered for an account.

- A customer who has **placed an order but never opted into marketing** is a Customer but NOT a Subscriber.
- A **newsletter signup who has never placed an order** is a Subscriber but NOT a Customer.
- The same email **may be both** — but they are independent records with independent lifecycles.

The platform exposes a "Customers and subscribers" view on [[customers-details-overview]] that shows both perspectives for the same email. See [[subscriber-vs-customer]] for the full reconciliation rules.

The Subscriber entity is documented at [[subscriber]].

### Customer-group is required

Every Customer **belongs to exactly one** [[customer-group|Customer Group]] via `group_id`. The platform reserves a special "Guests" group ID for guest customers; everyone else is a `Registered` customer (typically in the "Default" group, but the merchant can create custom groups via [[customers-custom-groups]]).

Customer-groups drive:

- **Discount tier** — group-targeted [[discount-code|Discount Codes]] and [[discount|Discounts]].
- **Price visibility** — group-specific price lists / overrides.
- **Segmentation** — group is a first-class filter in [[customers]] and downstream reports.

### Customer tags vs Product tags

The customer-tag table is **separate** from the product-tag table — they share no rows. Customer tags exist purely for filtering and segmentation on [[customers]] and are surfaced as the tag chips on [[customers-details]] (verify).

### Custom fields layer

The merchant can define custom fields on [[customers-custom-fields]] (e.g., "VAT number", "Company size", "Industry"). Each definition is a field on the merchant's customers; per-customer values are stored against the field-id. The values surface on [[customers-details-overview]] alongside the built-in attributes — see [[customer-entity-attributes]] for the built-in set.

### Avatar is gravatar-derived

The Customer doesn't have a backing image column — the storefront and admin grid derive the avatar from **Gravatar** by the customer's email. Customers cannot upload a custom avatar from the storefront.

## Where it appears

- [[customers-details]] — wrapper with all the sub-tabs that surface relationships.
- [[customers-details-orders]] — Orders sub-tab.
- [[customers-details-products]] — Products bought sub-tab (derived from orders).
- [[customers-details-payments]] — Payments sub-tab.
- [[customers-details-shipping-addresses]] / [[customers-details-billing-addresses]] — address management.
- [[customers-details-reviews]] — reviews left on products (derived from product reviews).
- [[customers-custom-fields]] — custom-field definitions.
- [[customers-custom-groups]] — group definitions.
- [[products-favorite-products]] — favorite items per customer (insight view).

## Related

- [[customer]] — hub.
- [[customer-group]] — required group assignment.
- [[subscriber]] — independent record with shared email.
- [[subscriber-vs-customer]] — the canonical distinction.
- [[segment]] — subscriber segments that customers can belong to (when also subscribed).
- [[order]] — every Order belongs to one Customer.
- [[cart]] — abandoned + active carts owned by the customer.
- [[invoice]] / [[credit-note]] — financial documents tied to the customer's orders.
- [[product]] — customers favorite and buy products.
- [[discount-code]] — discount codes can target specific customers / groups.

## Open Questions

- ⏸️ Whether customer-tags propagate to the linked Subscriber record automatically when the customer is also a Subscriber — the `CustomerTagChange` event surfaces in code paths but the precise sync rule is not fully documented (verify).
