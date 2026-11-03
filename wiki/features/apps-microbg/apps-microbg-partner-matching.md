---
type: feature
nav_path: "Apps → MicroBG → Partner matching"
route_name: apps.microbg.overview
route_path: /admin/apps/microbg/overview
aliases: ["MicroBG partner matching", "MicroBG EIK email cascade", "MicroBG customer sync", "MicroBG B2B B2C dedup"]
tags: [apps, erp, bulgaria, partner-matching, b2b, customers]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-microbg]]. See the hub for the other aspects (architecture split, registration, prerequisites, sync mechanics, troubleshooting).

# MicroBG — partner matching cascade

## Purpose

When a CloudCart order arrives in Micro.bg, the buyer must be linked to a Micro.bg **партньор** (partner) row. Micro.bg runs a deterministic two-step lookup cascade to decide whether to update an existing partner or create a new one. Getting the inputs right on the CloudCart side is the difference between clean per-business deduplication and a collapsed pile of anonymous "общ клиент" partners that no accountant wants to untangle.

## Where to find it

The cascade runs **inside Micro.bg** when each order webhook arrives — there is no UI for it on the CloudCart side. The inputs are:

- The buyer's **Адрес за фактуриране** (billing address) on the CloudCart order — specifically the EIK field.
- The buyer's **email** on the CloudCart order.

The CloudCart-side configuration that decides which of these are populated is on [[settings-cart]] — the "Bulstat/EIK or EGN" field's mode (Required / Опционално / Hidden).

## What the merchant can do here

The merchant doesn't directly run the cascade — it executes automatically per order. What they can do is **set the conditions** so the cascade resolves correctly:

- Configure [[settings-cart]] → "Bulstat/EIK or EGN" = **Опционално** so B2B buyers can provide EIK + B2C buyers can leave it blank.
- Encourage customers to provide an Адрес за фактуриране at checkout when buying for a company.
- Use the email field consistently — when the same buyer reuses email, Micro.bg dedups them under the same partner row.

### What the merchant CANNOT do here

- Override the cascade order. EIK match always wins over email match when both are present.
- Manually merge partners on the CloudCart side. Partner cleanup happens in Micro.bg's UI.
- Force Micro.bg to use a non-billing-address EIK (e.g. one stored only on the customer record). The cascade reads the order's billing address, not the customer profile.

## Settings & fields

There are no fields specific to partner matching on the CloudCart side. The relevant CloudCart-side fields read at order time are:

- **Billing address EIK** (from the order's `billing_address.eik`, populated by the checkout EIK field).
- **Buyer email** (from the order's `customer.email`).

The cascade then proceeds on Micro.bg's side using those two values.

## Business rules

### Partner matching cascade

When a CloudCart order arrives in Micro.bg via the `order.created` webhook (see [[apps-microbg-sync-mechanics]]), the partner-lookup cascade is:

1. **Order has Адрес за фактуриране (billing address) with EIK** → Micro.bg searches partners by EIK.
   - Match found → update existing partner with the latest details.
   - Not found → create new partner from the billing address.
2. **Order has no billing address** (or billing-address EIK is empty) → Micro.bg searches by **email**.
   - Match found → update existing partner.
   - Not found → create new partner from the buyer's email + name.

### Why hiding the EIK field corrupts B2B dedup

Setting [[settings-cart]] → "Bulstat/EIK or EGN" = **Hidden** removes the EIK input from the storefront checkout. The order arrives at Micro.bg with no billing-address EIK, so the cascade falls through to step 2 (email-based dedup). For a B2B buyer that pays from a personal email, every subsequent order becomes a *new* partner row in Micro.bg unless the email exactly matches the previous order. Worse: when the same company orders from two different employee emails, they get split into two partners in Micro.bg — exactly the opposite of what the accounting team needs.

Setting the EIK field to **Required** is also wrong because it blocks B2C buyers (who have no Bulgarian EIK) from checking out at all — see [[apps-microbg-prerequisites]]. **Опционално** is the only configuration that supports both buyer types cleanly: B2B buyers fill the field and get EIK-matched, B2C buyers leave it blank and get email-matched.

### What gets written to the partner on each match

When Micro.bg finds an existing partner (by either EIK or email), it updates the partner with the latest billing-address fields from the order — company name, MOL, VAT number, address, phone. This means a customer who corrects their billing address on a new order will have the partner row reflect the new details after that order syncs. There is no "create new partner anyway" override; Micro.bg always upserts on the first match.

### Mixed B2B / B2C storefronts

The cascade handles mixed audiences correctly *if* the EIK field is **Опционално**:

- A consumer (no EIK provided, no billing address) ends up under their email as a partner.
- A company (EIK provided in the billing address) ends up under their EIK as a partner.
- A consumer who later turns into a company on a subsequent order — and provides EIK — will create a *new* EIK-keyed partner. The previous email-keyed partner remains in Micro.bg but is no longer used by future orders from this buyer. `(verify)` whether Micro.bg auto-merges in this case.

## Related

- [[apps-microbg]] — hub.
- [[settings-cart]] — the "Bulstat/EIK or EGN" field mode that decides whether EIK reaches the order.
- [[customer]] — the CloudCart-side customer entity Micro.bg reads from.
- [[orders-details]] — the order's billing-address fields read by the cascade.
- [[apps-microbg-prerequisites]] — the full prerequisites checklist that includes the EIK setting.

## How it works (verified against backend)

The cascade is implemented on Micro.bg's side; CloudCart only exposes the order data via the `order.created` webhook payload. The webhook payload includes:

- The order's billing address (or `null` if the buyer didn't provide one).
- The buyer's email + name from the order's customer block.

Micro.bg's webhook receiver reads `billing_address.eik` first. If present, it queries its partner table by EIK. If absent or empty, it falls through to email-based lookup. The two queries are mutually exclusive — Micro.bg does not attempt email lookup when EIK is provided.

## Open questions

- Whether Micro.bg writes the previous CloudCart customer-id into the partner record (for later cross-reference) or only the EIK / email. `(verify)`
- Behaviour when the same CloudCart customer changes from email-keyed (no EIK) to EIK-keyed on a subsequent order. `(verify)` whether the old email-keyed partner is auto-merged or just left orphaned.
