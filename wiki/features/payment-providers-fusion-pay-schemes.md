---
type: feature
nav_path: "Payment Providers → Fusion Pay → Schemes"
route_name: apps.fusion_pay.schemes
route_path: /admin/payment-providers/fusion_pay/schemes
aliases: ["Fusion Pay Schemes", "TBI Pay schemes", "TBI free leasing schemes", "Схеми Fusion Pay", "ТБИ Пей схеми"]
tags: [paymentproviders, payment-providers, fusion-pay, tbi-bank, bnpl, schemes]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 1
---
# Schemes

## Purpose

The Schemes tab for Fusion Pay lists TBI Bank's **free-leasing schemes** (the 0%-interest installment plans TBI defines on their side) and lets the merchant map each scheme to a filter so it applies to specific products. Without a mapping, all free-leasing schemes TBI returns apply to any qualifying order; with a mapping, a scheme is scoped to carts that match the merchant's filter — typically "products in category X" or "products from manufacturer Y".

The merchant also picks **one free-leasing scheme as the "free scheme"** — the one highlighted at storefront as the default 0% offer. This is a single-select toggle across all the merchant's promo schemes.

## Where to find it

Sidebar → **Payment Providers** → **Fusion Pay** → **Schemes** tab.

The route is `/admin/payment-providers/fusion_pay/schemes`. On load the page fetches the merchant's current TBI free-leasing schemes and renders one row per scheme with its mapping configuration.

## What the merchant can do here

- **See the table of free-leasing schemes** TBI Bank currently offers. Only TBI's promo schemes tied to a category appear; interest-bearing schemes are not shown here. The table has three columns: **Name**, **Period**, and **Active** (the "free scheme" toggle). The mapping itself is configured inside the Edit Scheme modal, not shown as a separate column.
- **Read the permanent info banner** at the top: *"Here you can expect schemes that are provided by Fusion Pay. You can not add schemes by yourself."* It doubles as guidance when the list is empty.
- **Click any row to open the Edit Scheme modal** and configure a filter mapping for that scheme.
- **Toggle the "free scheme" switch** on a row to make that scheme the highlighted default. Only one scheme can hold this flag at a time — toggling one ON clears the flag on every other row; toggling OFF clears the default entirely.
- The list refreshes on page load from TBI; merchants don't add or delete TBI's schemes themselves.

## The Edit Scheme modal

Clicking a scheme row opens a right-side slide-out modal (size `lg`) with **Cancel** + **Save** buttons. The body has one card containing a product-filter control with two parts:

- **Filter type selector** — dropdown with these options:
  - "Include specific Products" → `product` (picker: *Choose specific products*)
  - "Include products by Manufacturer" → `vendor` (picker: *Choose vendors*)
  - "Include products by Smart Collection" → `selection` (picker: *Choose smart collections*)
  - "Include products by Category" → `category` (picker: *Choose categories*)
  - "All products" → `all` (no picker; scheme matches everything)
- **Value picker** — adapts to the chosen filter type (an AJAX-search picker over the matching catalog).

There is **no `tag` filter and no `brand` filter** in the Fusion Pay schemes mapping — only `product`, `vendor`, `selection`, `category`, plus `all`. (Klear's financing-program filter, by contrast, exposes a fifth `tag` option.)

When the merchant edits an existing mapping, the modal pre-fills both the filter type and the value from the scheme's stored mapping. On Save it persists `{id, filter, filter_value}` and shows the toast *"You have successfully edited the scheme."*, then closes and updates the table row in place.

## The "Set as free scheme" toggle

Each row has an inline active-switch. Toggling it:

1. Sets the row's `free_scheme` flag to the new value AND clears `free_scheme` on every other row (single-default enforcement).
2. Toggling ON shows the toast *"You have successfully activated the scheme."*; OFF shows *"You have successfully deactivated the scheme."*.
3. On failure: *"Error occurred while changing the status. Please try again later."*

## Settings & fields

### Per-scheme mapping

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Scheme** (read-only) | TBI's scheme ID + name + period. Comes from TBI's calculation API; the merchant can't edit it. | Set by TBI | Only TBI promo schemes tied to a category appear. |
| **Filter** | The product attribute to filter on — `product`, `vendor`, `selection`, `category`, or `all`. | Empty | Required to save a mapping. |
| **Filter value** | The value the filter must match — e.g., a category, a manufacturer. | Empty | Required to save a mapping. Together with Filter, this becomes one entry in the merchant's mapping, keyed by the scheme ID. |
| **Set as free scheme** | Marks this scheme as the default highlighted 0% offer. | OFF | Toggle. Setting it clears the previous default. Stored as `free_schema` in the provider configuration. |

## Business rules

### What the schemes list comes from

The list is fetched from TBI with no price and no category, then filtered to TBI's **promo** schemes that are tied to a category. The merchant ONLY sees free-leasing schemes — interest-bearing schemes are handled automatically by the storefront pricing module based on the [[payment-providers-fusion-pay-settings|Settings tab's period range]] and TBI's calculation API. If TBI returns an error or empty array, the table renders empty (the standard "no rows" placeholder); no custom empty-state copy is shown, but the permanent info banner above the table stays visible as guidance.

### How the merchant's filter translates to storefront behavior

When the storefront requests pricing schemes, it sends the cart's category to TBI, which returns all matching schemes. The `mapping` from this tab is consulted only at display time — schemes that have a mapping show the merchant's filter as additional context for the customer.

### "Free scheme" — the single default

The configuration field `free_schema` (singular, spelled with an "a") holds the ID of the merchant's default 0% scheme. Setting another scheme overwrites the value. Only one scheme can hold this flag at a time.

### Tier multipliers

The Schemes tab is purely about mappings — it does NOT re-fetch TBI's tier multipliers. Those refresh on Settings save instead.

### Plan-gating

Inherits the parent provider's gating — none beyond having a TBI reseller contract.

## Related

- [[payment-providers-fusion-pay]] — parent hub for Fusion Pay.
- [[payment-providers-fusion-pay-settings]] — reseller credentials, period range, button tiers.
- [[payment-providers-dsk-zero-schemes]] — equivalent concept (merchant-curated 0% schemes) but a different model: DSK Zero schemes are entirely merchant-defined (months + products), while Fusion Pay schemes come from TBI Bank's catalog.
- [[product]] — products that the filter resolves against.
- [[payment-providers]] — top-level Payment Providers area.

## Open questions

(none)
