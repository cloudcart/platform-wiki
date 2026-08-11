---
type: feature
nav_path: "Apps → Membership → Data model"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Membership data model", "Membership record", "Membership fields", "Lifetime membership", "Membership expiry"]
tags: [apps, administration, membership, data-model]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Membership — data model

> Part of [[apps-membership]]. See the hub for the other aspects (purchase flow, renewal/revocation, records admin, API).

## Purpose

This aspect documents **what a membership record actually is** in CloudCart: a simple, time-bound link between one customer, one product, one page, and one expiry timestamp. Understanding this shape explains why several "expected" features (gift memberships, household plans, multi-tier-in-one-record) do not exist.

## Where to find it

Membership records are surfaced in the Settings tab at `/admin/orders/subscriptions/settings` (see [[apps-membership-records-admin]] for the table UI). The records themselves are stored in the `@apps_memberships` table created on install.

## What the merchant can do here

- Read a member's current status as the set of records attached to their customer account.
- Understand that one customer can hold multiple membership records (one per page granted).
- Recognise that a `null` expiry means a lifetime membership.

### What the merchant CANNOT do here

- Cover multiple customers with a single membership record — one record = exactly one customer.
- Store multiple tiers or multiple pages inside one record — each page granted is its own record.

## Settings & fields

### The 5-field membership record

The `@apps_memberships` table stores per-membership rows with these fields:

| Field | Meaning |
|---|---|
| `customer_id` | The customer holding the membership. |
| `product_id` | Optional — the product associated (typically the membership-tier product the customer purchased). |
| `page_id` | Optional — the page / content the membership grants access to. |
| `expired` | Expiry timestamp. `null` = lifetime (never expires). |

So a membership is a **simple time-bound 1:1:1 link**: one customer ↔ one product ↔ one page ↔ one expiry.

### Relationships

- One customer per membership.
- One product per membership (the purchased membership-tier product).
- A membership grants access to exactly one page (the gated content). Granting access to several pages means several records — see [[apps-membership-purchase-flow]] for how a single purchase fans out into multiple records.

## Business rules

### One membership belongs to exactly one customer

Each membership row holds exactly `customer_id`, `product_id`, `page_id`, and `expired`. **One membership belongs to exactly one customer.** The merchant cannot purchase a membership for someone else's account from inside the platform, and a single membership cannot cover multiple customers — a household of 4 needs 4 separate memberships.

### No gift / family / multi-customer memberships

There is no gift or family workflow. For a gift purchase the merchant would need a manual admin process: create the membership record for the recipient via the create endpoint after the gift purchase (see [[apps-membership-api]]).

### `expired = null` means "lifetime membership"

When a Product Page is configured with `days = 0` (or empty), the resulting membership record gets `expired = null`. The page-access query filters for `expired > now OR expired IS NULL` (effectively never expires). So the merchant sets up lifetime memberships by linking a Product to a Page with no validity days — a single purchase grants permanent access.

### For multi-tier setups, use multiple records

There is no "tier" column. For multi-tier setups the merchant creates multiple membership records per customer, or uses different products per tier. The "tier" is an emergent concept built from differently-priced digital products with different page links and validity periods (see the hub [[apps-membership]]).

## Related

- [[apps-membership]] — hub.
- [[customers]] — the customer holding the membership.
- [[products-products]] — the digital product associated with the record.
- [[apps-membership-records-admin]] — where records are listed and edited.

## Open questions

None.
