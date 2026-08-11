---
type: feature
nav_path: "Products → Variants → Separate-product listing toggle"
route_name: variants-index.new
route_path: /admin/products/variants
aliases: ["Variants listing", "Separate product in listing", "variants.listing", "Show each variant as a separate product", "Include variant name in product title", "Самостоятелна продуктова карта"]
tags: [products, variants, listing, plan-gate, storefront]
plan_gates: ["multi_variants", "variants.listing"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Variants — "separate product in listing" toggle

> Part of [[products-variants-options]]. See the hub for the other aspects (list table, wizard, types, values, data model, API).

## Purpose

A paid plan feature flipped on the per-parameter create/edit modal (the wizard Step 1 advanced section, or the Edit modal) — when enabled, each variant combination becomes a separate product card on category listing pages instead of a single card with variant pickers. The toggle is gated by `variants.listing` and is **24-hour throttled** independently of the plan gate.

## Where to find it

**Products → Variants → + Add variant → Step 1 → Advanced settings → "Show each variant as a separate product in the product listing"** (and the sibling **"Include the variant name in the product title"** toggle).

The same advanced section is reachable in the Edit modal on an existing parameter.

## What the merchant can do here

- Toggle ON to enable per-variant listing cards (paid; requires `variants.listing`).
- Toggle "Include the variant name in the product title" to append `<variant>` onto the listing card title — visible only when `variants.listing` is active.
- See a "Paid" badge + warning info-box explaining the feature when not subscribed.
- Click the **See pricing** button to open the per-feature pack-purchase modal.
- After purchase, flip the toggle ON (subject to the 24-hour throttle below).

## Settings & fields

### Advanced section fields

| Field | Notes |
|---|---|
| **Show each variant as a separate product in the product listing** | Boolean. Plan-gated by `variants.listing`. "Paid" badge + pack-purchase prompt shown when feature is locked. Warning info-box explains the listing-rebuild side effect. |
| **Include the variant name in the product title** | Boolean. Visible only when `variants.listing` is active. When ON, the product card title becomes `<base product name> - <variant value>`. |

### Effects on the storefront listing

When **enabled (paid):**

- Each variant combination becomes a separate product card on category listing pages.
- The product card title can optionally include the variant name (`<product> - <variant>`).
- Customers see N cards instead of 1 — better for SEO and discoverability of specific variants but multiplies listing density.

When **NOT enabled (default):**

- The product appears as ONE card on category listings.
- Variants are picked on the product detail page only.

## Business rules

### 24-hour throttle (independent of the plan gate)

Once toggled (on or off), the merchant cannot toggle the same parameter again for 24 hours. Same applies to the related "Include variant name in product title" toggle.

This guard exists because changing this flag triggers a **storefront listing rebuild**. Until the next_update timestamp passes (24 hours later), the toggle on the form is disabled. The throttle applies even on the API path — see [[products-variants-api]].

### Storefront listing rebuild after toggle

Flipping the flag ON or OFF affects the storefront category pages and search results. The listing-rebuild engine regenerates the cards on the next request (no manual re-publish needed). The 24-hour throttle prevents toggle-thrashing while the rebuild runs.

### Plan-gate behaviour

- `variants.listing` is a Boolean plan feature (not a numeric cap). When the merchant turns the toggle ON without the feature, the request is rejected and the per-feature pack-purchase modal opens — see [[plan-vs-feature-pack]].
- The "Paid" badge sits next to the toggle when locked.
- After purchase, the toggle becomes editable (still subject to the 24-hour throttle).
- The listing rebuild only runs while the subscription is active; on expiry, the listing engine reverts the product card back to a single product card per parent product.

### "Include variant name in product title" depends on `variants.listing`

The second toggle is only visible when `variants.listing` is active. It does nothing on its own — it just changes the title format of the listing cards produced by the parent toggle.

### Apps that depend on this toggle

Some merchant-installed apps (e.g., listing-engine variants — see [[apps-listing-engine]]) interact with this toggle. The same 24-hour throttle applies regardless of the trigger surface.

## Related

- [[products-variants-options]] — hub.
- [[products-variants-wizard]] — the wizard/edit modal where this toggle lives.
- [[products-variants-api]] — same gate + throttle applies on the JSON-API v2 path.
- [[plan-vs-feature-pack]] — the pack-vs-upgrade decision for `variants.listing`.
- [[plan-features]] — catalogue of plan feature keys (`multi_variants`, `variants.listing`).
- [[plan-gates]] — how plan gates work mechanically.
- [[apps-listing-engine]] — companion app that reacts to this toggle.

## Open questions

None.
