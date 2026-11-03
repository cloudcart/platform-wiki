---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → B2B account data"
aliases: ["B2B customer metafields", "Trade account data", "Credit limit metafield", "Payment terms metafield", "Account manager", "Company registration number", "Contract file", "Wholesale customer data", "Данни за фирмен клиент", "Кредитен лимит", "Условия за плащане", "Акаунт мениджър", "Договор с клиент"]
tags: [metafields, use-case, customers, b2b, wholesale]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: B2B account data on business customers

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

A wholesale store handles its trade accounts with customer groups, group prices, VAT invoicing and fast ordering ([[b2b-wholesale]]). Around each business customer there is more information:

- a registration number;
- agreed payment terms and a credit limit;
- an account manager;
- a signed contract;
- an ERP account code;
- a delivery window for the warehouse.

On CloudCart the business is the **customer**. **Customer metafields** carry the account data. Their access settings decide what the buyer sees in their account on a Nitrogen storefront.

## Scope

### The data model

| `namespace.key` | Type | Customer account access | Notes |
|---|---|---|---|
| `b2b.registration_no` | `id`, `regex` `^[0-9]{9,13}$` | `READ` | Always unique: no two customers share it. |
| `b2b.erp_account` | `id` | `NONE` | The key an ERP sync matches on. |
| `b2b.payment_terms` | single-line text, `choices`: *Prepaid, 14 days, 30 days, 60 days* | `READ` | |
| `b2b.credit_limit` | `money` | `READ` | In the store's currency only. |
| `b2b.open_balance` | `money` | `READ` | Synced from accounting. |
| `b2b.account_manager` | `metaobject_reference` → `account_manager` | `READ` | |
| `b2b.contract` | `file_reference` | `READ` | The signed PDF. |
| `b2b.contract_ends` | `date` | `NONE` | Admin filter is not offered on customers; found through an integration. |
| `b2b.delivery_window` | single-line text | `READ` | *"Mon–Fri 8:00–14:00, ramp 3"*. |
| `b2b.internal_rating` | `rating`, scale 1–5 | `NONE` | Staff only. |

**Metaobject definition `account_manager`**: `name` (display name), `photo` (file, Image), `email`, `phone` (single-line text), `regions` (`list.single_line_text_field`).

The `b2b` namespace keeps these apart from consumer fields. Namespaces other than `custom` are created through the Admin GraphQL API; the admin itself uses `custom` ([[metafields-definitions]]).

### On the Nitrogen storefront

- The **trade account page** shows payment terms, credit limit and open balance, the contract to download, and an *"Your account manager"* card with photo and contacts. All are read with the buyer's own access token, only for `READ` definitions ([[metafields-permissions]]).
- The `NONE` fields never reach the storefront, whoever asks.

### What stays native

- **Prices, payment and shipping rules** come from the customer's **group** ([[customer-group]]). A metafield such as `payment_terms` describes the agreement. It does not make a payment method appear or a price change.
- **Invoice details** (company name, VAT number on the invoice) stay in the customer's and the order's own invoicing fields.
- **Credit limits** are not enforced at checkout by a metafield. Enforcement, if any, is the ERP's or a staff review's job.

## Contrasts

- **Customer metafields vs customer custom fields** ([[customers-custom-fields]]): a custom field such as *Tax ID* is filled in by the buyer at checkout. Account data here is set by the store and read-only for the buyer.
- **One business, several buyers**: without company records, each buyer is a separate customer. Shared account data is repeated per buyer. Alternatively it goes in a `trade_account` metaobject that each buyer's `b2b.account` references, so the terms are edited once.
- **Unique `id` vs plain text**: the `id` type refuses a second customer with the same registration number, which catches duplicate accounts early ([[metafields-capabilities]]).

## Where it applies

- Wholesalers, distributors, manufacturers selling to retailers, suppliers to the hospitality trade.
- Values are edited by staff with the Customers permission, or written by an integration with the `customers` token scope.

## Related

- [[metafields-use-cases]]: all use cases.
- [[b2b-wholesale]]: the platform's native B2B setup.
- [[metafields-use-case-customer-profile]]: consumer customer data.
- [[metafields-use-case-integration-data]]: ERP keys and sync.

## Open Questions

- None known.
