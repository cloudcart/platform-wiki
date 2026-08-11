---
type: feature
nav_path: "Settings → Taxes and fees → Downstream integrations"
route_name: taxes.settings
route_path: /admin/settings/taxes
aliases: ["Tax integrations", "Tax row downstream consumers", "SmartBill tax", "DPD VAT eligibility", "XML feed VAT", "BGN to EUR migration", "Tax API access"]
tags: [settings, taxes, integrations, apps, smartbill, dpd, xml-feed, json-api]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-taxes]]. See the hub for the other aspects (VAT rules, fees, overrides, pricing display, OSS / no-VAT, validation).

# Taxes and fees — downstream integrations

## Purpose

Catalogues every system OUTSIDE the Tax management screen and the cart-totals engine that reads from the Tax row. These integrations are merchant-impacting in subtle ways — with no active VAT rule (or the wrong one), invoicing apps treat lines as net-of-VAT, couriers lose access to fiscal-receipt features, and XML feeds export wrong prices. Also covers the one-time BGN→EUR migration and the read-only JSON-API v2 access model.

## Where to find it

The integrations live in their own admin screens (see Related), but they all read silently from the rules configured on Settings → Taxes and fees (`/admin/settings/taxes`). There is no *"integrations"* tab on the Tax form — every consumer reads the same single source-of-truth Tax row.

## What the merchant can do here

This page is reference-only — it does not document a UI screen; the actionable knobs are spread across the linked apps and the Tax form itself. The practical takeaway: if any downstream consumer (SmartBill invoice, DPD COD receipt, XML feed price) shows wrong VAT behaviour, first check whether the active VAT rule on Settings → Taxes and fees has the expected `vat=yes`, `price_with_vat`, and zone scope.

## Settings & fields

This page does NOT own settings — it documents how OTHER consumers read the existing Tax row. The fields each integration reads are called out in the per-consumer sections below and summarised in the *Cross-module dependencies* table. The canonical field catalogue lives on the [[settings-taxes]] hub.

## Business rules

The integrations share three operational invariants:

- **One source of truth.** Every consumer reads the SAME Tax row — there is no per-integration override layer. Fixing the Tax row fixes every downstream consumer at once.
- **Read-time evaluation, no event broadcast.** No integration subscribes to a *"Tax updated"* event; they read fresh on each invoice generation, courier eligibility check, feed run, or order computation. A Tax edit takes effect on the next request that touches the integration.
- **Past orders are frozen.** A per-order snapshot (see *Historical orders frozen by snapshot* below) means edits and deletes NEVER retroactively change historical invoices; only future orders pick up the change.

## What integrations read the Tax row

### SmartBill invoicing integration

The [[apps-smart-bill|SmartBill]] integration reads the active VAT rule's `price_with_vat` flag to mark each invoice line as tax-included or not. It requires an active rule with `vat=yes` — so with **NO active VAT rule**, SmartBill marks every line as net-of-VAT regardless of the storefront's pricing model. A store on inclusive pricing (`price_with_vat=1`) whose VAT rule was accidentally deleted will see invoices that misrepresent the VAT breakdown until the rule is restored.

### DPD Bulgaria + DPD Romania — fiscal-receipt eligibility for COD

The DPD Bulgaria and DPD Romania courier integrations check for an existing VAT rule to gate the carrier's **fiscal-receipt option on COD orders**. A store with no VAT rule loses that feature — a soft block: COD orders still go through, but the fiscal-receipt sub-option in the courier's order action panel disappears.

### XML product feed exports

The [[apps-xml-feed-generator]] family reads the active VAT rule to extract / include VAT in feed prices. The result is cached for one feed-generation run — so a Tax edit DURING generation may not reflect in that run, but the next run uses the new rule.

### Historical orders frozen by snapshot

When an order is created, the platform snapshots the applicable Tax rule values into a separate `orders_taxes` record. Historical invoices read from that snapshot, so deleting or editing a Tax row never changes past orders; new orders use the current configuration. See [[settings-taxes-validation]] for hard-delete behaviour.

## Hidden write path — BGN→EUR migration

During the platform's one-time Bulgarian-leva-to-euro currency migration (a CloudCart-staff-run tool, not merchant-accessible), every `flat`-type Tax row had its amount divided by the official conversion rate and rounded. This write **bypasses the normal Tax save logic** — no normalisation, no automatic cache flush. Implications for migrated stores:

- The Settings cache flush that normally fires on a Tax edit does NOT fire here. CloudCart staff must clear the cache manually post-migration.
- Percent-type taxes were NOT touched (rates are currency-agnostic).
- Per-tax overrides and the `without_vat_reasons` / `without_vat_reasons_non_eu` text fields were NOT touched.

Merchants who notice unexpected VAT amounts shortly after a currency migration should check whether their cache was flushed correctly.

## JSON-API v2 access — read-only, computed-only

There is **NO dedicated tax / fee resource** in the public **JSON-API v2** — the tax and fee records on this screen cannot be read or written through the public API. What IS exposed is the **computed tax breakdown per order** — see [[api-order-tax]] for the order-level tax line read endpoint. Integrations consume the final per-order amounts the engine produced (after VAT precedence, OSS rules, per-category overrides, etc.), not the rule configuration. To inspect or modify the rules themselves, the merchant must use this admin screen; see [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

The rules are kept out of the API on purpose: VAT rules are tied to legal jurisdictions, so a programmatic regional-VAT add could (a) trigger the auto-Global companion creation (see [[settings-taxes-vat-rules]]), (b) lock the storefront's billing-address country picker (the *"country-limit"* side effect), or (c) overwrite the merchant's compliance-critical *"without VAT reasons"* text.

## Cross-module dependencies — at-a-glance summary

| Consumer | What it reads | Failure mode when Tax is missing |
|---|---|---|
| Cart-totals engine | All matching VAT / fee rules + winning VAT's `price_with_vat` | Order has no VAT line; fees still stack without VAT. |
| [[apps-smart-bill\|SmartBill]] | Active VAT's `price_with_vat` (requires `vat=yes`) | Invoice lines marked net-of-VAT regardless of storefront pricing model. |
| DPD Bulgaria / DPD Romania | Whether an active VAT rule exists | COD fiscal-receipt option hidden from courier action panel. |
| [[apps-xml-feed-generator]] | Active VAT for price extraction | Feed prices may not include / exclude VAT correctly. |
| Historical-order snapshot | Tax row values at order-create time | Frozen — past invoices unaffected by later edits / deletes. |
| BGN→EUR migration (staff-only) | Flat-type tax amounts | Bypasses normal save logic — cache flush required manually. |
| [[api-order-tax]] (JSON-API v2) | Per-order computed tax breakdown | Read-only; integrations cannot edit Tax rules. |

## Related

- [[settings-taxes]] — hub.
- [[settings-taxes-vat-rules]] — the `vat=yes` rule SmartBill / DPD / XML feeds all look for.
- [[settings-taxes-validation]] — hard-delete semantics + `orders_taxes` snapshot persistence.
- [[apps-smart-bill]] — invoicing integration consuming `price_with_vat`.
- [[apps-xml-feed-generator]] — feed exports consuming the active VAT.
- [[apps-store-locations]] — separate app; uses geo zones but NOT the Tax row.
- [[api-order-tax]] — JSON-API v2 endpoint for the per-order tax breakdown.
- [[json-api-v2]] — API overview (authentication, rate limit, side-effects principle).
- [[multi-currency]] — concept page; context for the BGN→EUR migration command.

## Open questions

- The full list of courier apps gating the COD fiscal-receipt option on an active VAT rule — DPD BG / DPD RO are confirmed; other carriers may follow the same pattern (verify).
