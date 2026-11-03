---
type: feature
nav_path: "Apps → Econt → Pallet"
route_name: apps.econt.settings
route_path: /admin/shipping/econt/settings
aliases: ["Econt pallet", "Econt palletized shipping", "Палетно изпращане Еконт", "Pallet shipment Econt"]
tags: [apps, shipping, courier, bulgaria, econt, pallet, settings]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-econt]]. See the hub for the other aspects (Settings, addresses, shipments, waybill mapping, COD / insurance, coverage / caches).

# Econt — Pallet shipping

## Purpose

Pallet shipping is the Econt-specific flow for large / heavy products that require palletized transport (rather than parcel-shipment). The merchant enables it on the Settings tab's Pallet box, configures dimensions + triggers (categories or minimum weight), and the platform automatically chooses pallet vs regular shipment per order using a deterministic decision tree.

When pallet IS chosen, the platform sends the shipment to Econt with the PALLET package type and the configured dimensions (defaults to 60×60×60 cm if the merchant didn't customise them).

## Where to find it

Sidebar → Apps → Econt → **Settings** tab → **Pallet** box (section 9 of the Settings layout — see [[econt-settings-tab]]).

## What the merchant can do here

- Enable / disable pallet shipping store-wide for Econt.
- Set pallet dimensions (Length / Height / Width in cm — each min 60).
- Pick product categories that trigger pallet shipping; OR set a minimum weight (kg) that triggers pallet shipping; OR both (combined).
- Let the platform fall back to defaults (60×60×60 cm) when no custom dimensions are entered.

## Settings & fields

### Pallet box (editor — `Pallet.vue`)

- Display mode shows pallet dimensions summary.
- Pencil → opens slide-down editor with:

| Field | Notes |
|---|---|
| **Pallet shipment** | Master switch. Enable/disable palletized shipping. |
| **Length (cm)** | Required, **min 60**. Only when master switch ON. |
| **Height (cm)** | Required, **min 60**. Only when master switch ON. |
| **Width (cm)** | Required, **min 60**. Only when master switch ON. |
| **Categories** (`Apply pallet shipping on`) | Multi-tag select against the merchant's categories list. Alert above: *"You can select categories, if you do not select categories, the 'pallet shipment' type will be applied to each shipment."* |
| **Minimum weight** | Number, **integer kg** (no decimals). |
| **Apply on min total** | Currency threshold (additional rule for pallet eligibility). |

## Business rules

### Pallet eligibility decision tree (verified against backend)

The merchant's Pallet config drives whether a SPECIFIC order ships as a pallet. The decision tree:

```
1. If categories empty AND palletWeight <= 0:
     → NOT pallet (no rule configured).
2. If categories empty AND palletWeight > 0:
     → Pallet IF (cart weight > palletWeight)
3. If categories defined:
     → Check if ANY order line is in those categories.
     → If yes AND palletWeight > 0 AND weight > palletWeight: Pallet.
     → If yes AND palletWeight = 0: Pallet (category alone is enough).
     → If no categories match: NOT pallet.
```

This **answers the pallet-eligibility question**: when the merchant configured "shoes" category but no shoes in the order, the platform falls back to REGULAR shipping (not pallet).

### Pallet dimensions default to 60×60×60 cm

When pallet shipment is enabled but the merchant hasn't set custom dimensions, the platform sends 60×60×60 cm as defaults. The settings UI also enforces a 60cm minimum on each axis.

### Pallet rules cascade

When pallet shipment is enabled:
- Specific categories OR weight OR total threshold triggers the pallet flow.
- Pallet shipments may have different rates from regular parcels.
- Some Econt services don't support pallets — the platform's quote API may return fewer options for these orders.

### "Apply on categories" alert behavior

If the merchant leaves Categories empty, the pallet flow applies to **every** shipment (subject to the minimum-weight / minimum-total triggers being met) — that's exactly what the in-form alert warns about. To restrict pallet to certain product groups, the merchant MUST add categories.

## Related

- [[apps-econt]] — hub.
- [[econt-settings-tab]] — Settings tab section 9 hosts the Pallet box editor; full Settings field reference.
- [[settings-boxes]] — package dimensions baseline (the non-pallet shipping size source).
- [[orders-shipping-waybill]] — uses the pallet-vs-regular decision at waybill time.

## Open questions

None.
