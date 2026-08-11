---
type: feature
nav_path: "Settings → Taxes and fees → Validation and restrictions"
route_name: taxes.create
route_path: /admin/settings/taxes/:type/:id?
aliases: ["Tax validation", "Fee validation", "Rate max 90%", "Tax form errors", "Save-time normalisation", "VAT flag immutability", "Tax hard delete", "Tax/Fee delete", "unique_geozone validator"]
tags: [settings, taxes, validation, restrictions, delete]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-taxes]]. See the hub for the other aspects (VAT rules, fees, overrides, pricing display, OSS / no-VAT, integrations).

# Taxes and fees — validation and restrictions

## Purpose

The reference for every validation rule on the Tax / Fee save endpoint: required fields, max-length / max-value caps, conditional required-when rules, the `vat` flag's immutability (Tax cannot become Fee after create), the `unique_geozone` validator (one VAT per zone), the save-time normalisation that silently rewrites a few fields, and the hard-delete semantics (no soft-delete, no FK cascade — but past orders keep their snapshot).

## Where to find it

The validation runs on the save endpoint behind the Tax / Fee form (`/admin/settings/taxes/:type/:id?`). Errors surface in the form's inline error slots. The delete endpoint is `DELETE /admin/api/core/settings/taxes/<id>` (also covers bulk-delete with the same permission gate).

## What the merchant can do here

This page is a reference for what the platform DOES on save / delete — there is no dedicated UI surface, only the inline form errors and the delete trash icon.

When a save fails, inline error messages surface in the form's error slots, e.g. *"You have not specified a name"*, *"The rate must not be greater than 90"*, *"You already have a VAT tax - `Standard EU VAT`"*. The merchant fixes the offending field and re-saves.

Clicking the row's trash icon deletes the row immediately, with **no confirmation modal** (one click → toast *"Deleted successfully"*). There is no admin undo; restoring means re-creating the rule from scratch.

## Settings & fields — validation schema

| Field | Constraint | Error / notes |
|-------|-----------|---------------|
| `name` | required, string, max **100** chars | *"You have not specified a name"* / *"The name must be up to 100 characters"*. |
| `type` | required, enum: `percent` \| `flat` | Decides whether `tax` is a percentage rate or a flat currency amount. |
| `tax` | required, **max 90** for percent; max 10,000,000 character-length for flat | Percent rates are capped at **90%** (NOT 100% — the common merchant assumption is wrong). Flat amounts have no numeric ceiling. Error on excess percent: *"The rate must not be greater than 90"*. |
| `target` | enum: `restofworld` \| `regions` | Defaults to `regions` when omitted; auto-corrected to `regions` if invalid value submitted. |
| `geo_zone_id` | **REQUIRED when `target = regions`**; must exist; must be **unique among VAT rules** (one VAT per zone) | Saving a second VAT for a zone that already has one is rejected with *"You already have a VAT tax - `<name>`"* (or *"You already have a global store VAT tax - `<name>`"* for rest-of-world). Fees have **NO** uniqueness check — multiple fees CAN target the same zone. |
| `vat` | yes / no — **NOT a user-toggleable form field** | The flag is auto-set on create based on which type card the merchant picked (Add Tax → `yes`, Add Fee → `no`). On update, the existing value is preserved — **the merchant cannot flip a Tax into a Fee (or vice versa) after creation**. To switch type, the merchant must delete and re-create. |
| `oss_registration` | nullable | Presence-based: the platform stores `true` when the request includes the field at all, `false` when omitted. Not a numeric value. |
| `price_with_vat` | only meaningful for `vat=yes` rules; **FORCED to `0` for fees** | The save layer hard-sets `price_with_vat = 0` for any Fee row regardless of submitted value. |
| `shipping` | only meaningful for `vat=yes` rules; **FORCED to `no` for fees** | The save layer hard-sets `shipping = no` for any Fee row regardless of submitted value. |
| `without_vat_reasons` / `without_vat_reasons_non_eu` | optional, **max 64,000 characters** | Free-text rendered on invoices. See [[settings-taxes-oss-no-vat]]. |
| `regions[].text` / `regions[].tax` | required when a `regions[]` row is submitted | Per-region override sub-rows must all have a text label (the place name) and a tax value; partial rows are rejected. |
| `categories[].description` | required when `categories[].category_id` is provided | Per-category override sub-rows must have a description; the description renders on the invoice line for that category's tax breakdown. |
| `payment_provider` | **REQUIRED when fee + `payment_active = target`** | *"You have not specified a payment method for which the fee will apply"*. |
| `shipping_provider` | **REQUIRED when fee + `shipping_active = target`** | *"You have not selected a shipping method for which the fee will apply"*. |
| `payment_active` / `shipping_active` | enum: `global` \| `target`, form-only | Form-side switches that drive the `payment_provider` / `shipping_provider` required-when rules. When set to `global`, the corresponding provider column is NULLed on save. Not stored separately on the row. |

The per-category uniqueness check (*"Category already in use"*) on the overrides ladder is documented on [[settings-taxes-overrides]].

## Business rules

### `vat` flag immutability — cannot flip Tax ↔ Fee after create

The Add-Tax-or-Add-Fee choice in the type picker modal is **permanent**. On update the original `vat` value is preserved and re-saved unchanged, ignoring whatever the form sent. The admin UI exposes no toggle for this field — and even a direct API write attempting to flip it is silently ignored. To switch type, the merchant must delete the row and re-create.

### Save-time normalisation — silent rewrites on save

On save the platform silently:

- **Sets `target='regions'`** if a `geo_zone_id` is entered but no target.
- **Clears `geo_zone_id`** to null if `target='restofworld'`.
- **Forces `shipping=no`** and **`price_with_vat=0`** for non-VAT taxes (fees).

So merchants don't need to clean up fields when switching a tax from regional to rest-of-world — the platform does it on save.

### Cache + side effects

Saving a tax / fee flushes the **Settings cache**, so the next checkout / order-creation computation uses the new rule immediately. No queue, notifications, or webhooks fire from this page.

### Permission

A moderator needs either the broad **Settings** permission OR the specific **Taxes** (`store.taxes`) grant from [[settings-staff]] to list, create, edit, or delete tax rules. Owners always pass. The delete endpoint `DELETE /admin/api/core/settings/taxes/<id>` honours the same gate.

### Delete is hard delete — no soft-delete, no FK cascade, no confirmation modal

Deleting is immediate: there is **no** soft-delete, **no** cascade-protection check, and **no** confirmation modal (one click → toast *"Deleted successfully"*). There is **no** FK-block — even a tax / fee referenced by recent orders can be removed.

Existing orders that referenced this tax keep their own snapshot, taken at order time, so historical invoices are unaffected. New orders no longer apply the deleted tax / fee.

### Rate precision — 2 decimal places

Tax rates carry **2 decimal places of precision** — `20.005%` is rounded to `20.01%` on save. Merchants see and enter the human-readable value (`20.00`); the scaled internal storage is handled automatically. See [[settings-taxes-pricing-display]] for the broader rate-precision context.

### `unique_geozone` vs the *"newest wins"* precedence

The save-time uniqueness check normally prevents two VAT rules from targeting the same zone. So the *"newest regional tax wins"* compute-time precedence (see [[settings-taxes-vat-rules]]) only fires for stores that bypassed the validator — typically older data or imports that pre-date it.

## Related

- [[settings-taxes]] — hub.
- [[settings-taxes-vat-rules]] — `unique_geozone` validator + the auto-Global companion logic.
- [[settings-taxes-fees]] — the fee-side hard-overrides (`price_with_vat=0`, `shipping=no`).
- [[settings-taxes-overrides]] — *"Category already in use"* error on overlapping override rows.
- [[settings-taxes-pricing-display]] — rate ×100 precision storage.
- [[settings-staff]] — `store.taxes` permission gate.
- [[settings-cart]] — `lock_orders` (separate setting; doesn't affect tax saves).

## Open questions

None.
