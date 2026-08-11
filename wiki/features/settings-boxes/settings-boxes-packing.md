---
type: feature
nav_path: "Settings → Delivery boxes (box-packing behaviour)"
route_name: boxes.settings
route_path: /admin/settings/boxes
aliases: ["Box packing", "Box-packing algorithm", "Outer vs inner dimensions", "Shipping cost boxes", "Volumetric weight boxes", "No boxes defined", "Опаковане в кашони", "Изчисляване на доставка с кашони"]
tags: [settings, boxes, shipping, packaging, calculation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-23
source_count: 6
---

> Part of [[settings-boxes]]. See the hub for related aspects (the box fields / modal, and the box lifecycle / delete / permission rules).

# Delivery boxes — box-packing & shipping-cost consumption

## Purpose

This aspect explains **why** the merchant defines boxes at all: how the platform's shipping-cost calculator consumes them. It covers the outer-vs-inner dimension distinction, the 3D bin-packing algorithm that picks which box(es) to use for an order, and what happens when no boxes are defined. A support agent cites this when a merchant asks "why are my shipping quotes wrong?" or "do I really need to add boxes?".

## Where to find it

Boxes are defined at Sidebar → Settings → **Delivery boxes**. The packing logic itself is not a screen the merchant clicks — it runs automatically during shipping-cost calculation in the storefront checkout and the admin order flows. Box matching happens during the cart / checkout flow (the default shipping provider/type is configured on [[settings-cart]]).

## What the merchant can do here

The merchant controls packing behaviour indirectly, by defining the box catalogue:

- Define realistic boxes (outer + inner dimensions + weights) so the calculator has something to pack into.
- Define a "generic shipping box" representing typical packaging even for single-SKU stores.
- Define notably smaller inner than outer dimensions for fragile / padded goods (e.g., 1–2 cm of padding per side) so the packing algorithm reserves space for protective material.

## Settings & fields

There are no additional fields beyond those documented on [[settings-boxes-fields]]. The packing algorithm reads:

| Box value | Used by the algorithm to… |
|-----------|---------------------------|
| **Inner dimensions** (`inner_*`) | decide which products physically fit inside a box. |
| **Outer dimensions** (`outer_*`) | submit to the courier for dimensional / volumetric weight pricing. |
| **Empty weight** (`empty_weight`) | add packaging weight to the parcel's total. |
| **Max weight** (`max_weight`) | cap how much content can be packed into a single box. |

## Business rules

### Outer vs inner distinction

Two sets of dimensions exist because the shipping-cost calculation needs both:

- **Outer dimensions** — the box's external size; this is what couriers measure for dimensional / volumetric weight pricing.
- **Inner dimensions** — the usable space inside; the box-packing algorithm uses this to decide which products fit in which box.

A merchant defining boxes for fragile / padded products typically has notably smaller inner than outer dimensions.

### The box-packing algorithm (3D bin-packing)

CloudCart uses an open-source 3D bin-packing library ([DVDoug/BoxPacker](https://github.com/dvdoug/BoxPacker)) to decide which box(es) to use for an order. It takes the order's products (with their individual dimensions and weights — see [[product]]) and the merchant's defined boxes (with their inner dimensions and max weight) and chooses the smallest combination that fits everything. Practical behaviour merchants can expect:

- The algorithm tries to fit everything in **one** box first (smallest possible).
- If no single box fits, it splits the order across **multiple** boxes — smaller items go into smaller boxes when possible to minimise total shipped volume.
- The smallest box that fits the order's products by inner dimensions is chosen, then that box's **outer** dimensions are submitted to the courier for the cost quote.
- Products that don't fit any defined box (e.g., an oversized item the merchant forgot to define a box for) cause the calculator to fall back to per-product dimensional estimates or to fail with a "no suitable box" warning, depending on the [[shipping-provider]].

### When box-packing runs — and the per-product alternative

Box-packing is **not universal**. It runs only for **carriers that support parcel boxing** (Speedy, DPD Bulgaria, DHL / DHL Express, Pigeon Express, Next Level, …) AND only when the merchant has **at least one box defined**. For those carriers the order's items are bin-packed into the defined boxes (above), and the packed box's outer dimensions + weight drive the courier quote. Carriers that don't support boxing, or stores with no boxes defined, skip this path entirely.

Those same carriers also expose a **"Submit product sizes"** toggle (`item_sizes`, the *volumetric weight* option — see [[apps-dpdbulgaria-speedy|Speedy]]). When it is ON and the order isn't packed into a defined box, the carrier falls back to sending **each product as its own package** using the product's own dimensions, and the courier computes volumetric weight per product. So the parcel size a courier ultimately sees comes from one of two places: the **chosen delivery box** (when box-packing runs) or the **individual product dimensions** (the per-product fallback). Both are what to check when a parcel is rejected as too big — e.g. for a locker compartment; see [[shipping-provider-mech-pickup-points]] for the locker / office size + weight limits and the debugging angle.

### Consumed during shipping-cost computation

The defined boxes are consumed by the shipping-cost calculator via shipping methods in both the storefront and admin order flows. Without any boxes, the system falls back to per-product weight only — many courier tariffs need volume, so missing boxes can cause incorrect shipping quotes. See [[shipping-calculation]] for the full courier tariff lookup.

### What happens with NO boxes defined

If the merchant ships physical products but has zero box rows defined, courier tariff calculations that need dimensional weight cannot run the packing algorithm. Behaviour depends on the [[shipping-provider]] — most providers fall back to summing the products' raw dimensions / weights, which is less accurate and tends to **over-estimate** volume (no packing efficiency is applied). Some couriers may refuse to quote without dimensional input.

Practical guidance: every store that ships physical products should define at least one "generic shipping box" representing their typical packaging size, even if they only have one SKU.

## Related

- [[settings-boxes]] — hub.
- [[shipping]] — shipping providers and methods consume defined boxes during cost calculation.
- [[shipping-calculation]] — concept page; how boxes + product dimensions feed the courier tariff lookup.
- [[shipping-provider]] — the courier integration that receives the chosen box's outer dimensions.
- [[settings-cart]] — default shipping provider/type; box matching happens during cart/checkout.
- [[product]] — products carry the dimensions matched against box inner dimensions.
- [[shipping-provider-mech-pickup-points]] — locker / office max parcel size + weight; the packed box (or per-product dimensions) is what's checked against a locker compartment.

## Open questions

None.
