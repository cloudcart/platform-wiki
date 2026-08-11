---
type: feature
nav_path: "Settings → Brand settings → Limitations"
route_name: brand.settings
route_path: /admin/settings/brand
aliases: ["Brand limitations", "No per-language logo", "No per-storefront logo", "brand_removal plan gate", "Brand settings constraints"]
tags: [settings, brand, limitations, plan-gates]
plan_gates: ["brand_removal"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-brand]]. See the hub for related aspects (slots, upload flow, OG image, favicon, errors, cache & storage).

# Brand settings — Limitations

## Purpose

What the Brand settings page does NOT support — fixed-slot list with no extensibility, no per-language / per-storefront / per-theme brand variants, no bulk upload or crop tooling. Plus the one plan-gate that affects branding: `brand_removal`, which controls whether the merchant can hide the "Powered by CloudCart" footer credit — though the toggle that enforces it lives on [[settings-general]], not on the Brand settings page documented here.

## Where to find it

The constraints documented here apply to the Brand settings page (`/admin/settings/brand`). The `brand_removal` plan-gate's *toggle* lives on [[settings-general]] (Brand box), but the *consequence* (whether the footer credit shows or hides) affects the storefront across every page.

## What the merchant can do here

What the merchant CANNOT do — the limits this aspect documents:

- Cannot add a new slot for a use case the platform doesn't support (e.g., "PDF receipt logo", "social card image for LinkedIn-only").
- Cannot rename or reorder the seven slots.
- Cannot set different logos per language on a multi-language storefront.
- Cannot set different logos per storefront in a multi-storefront deployment.
- Cannot set different logos per active theme.
- Cannot bulk-upload multiple assets in one operation.
- Cannot crop, mask, or apply effects — only client-side downscale preserving aspect ratio.
- Cannot hide the "Powered by CloudCart" footer credit unless on a plan with `brand_removal` enabled (and even then the toggle lives on a different page).

## Settings & fields

### Seven fixed slots — neither configurable nor extensible

The slot list is hard-coded in the platform: `main`, `favicon`, `invoice`, `mail`, `default_image`, `checkout`, `og_image_url`. See [[settings-brand-slots]] for the inventory. The merchant cannot:

- Add a new slot type.
- Remove an unused slot type.
- Rename a slot's backend label.

If a merchant has a use case the seven slots don't cover (e.g., "I want a different logo on packing slips than on PDF invoices"), the answer is: not supported. The closest slot must be reused, or the use case handled through a different mechanism (e.g., a custom theme override for packing slips).

### Per-language / per-storefront brand variants — NOT supported

The `Logo` model is store-scoped — there is no `locale` or `theme` column. Each of the seven slots holds exactly one asset that applies to every storefront language and every active theme. Merchants running multi-language storefronts who want different logos per locale (e.g., a Cyrillic vs Latin wordmark) currently cannot do this from this page.

Workarounds:

| Workaround | Description |
|------------|-------------|
| **Single bilingual logo** | Design one logo that works for both languages (text-free or bilingual wordmark). Most common solution. |
| **Theme per-language image override** | Some themes support per-language image overrides in their theme settings. Theme-specific — not all themes support this. See [[design-theme-editor]]. |
| **HTML-based logo block** | Place an HTML-based logo block in the storefront template that reads the current locale and swaps images. Requires template editing. |

The same applies to multi-storefront deployments — there is no "storefront A uses logo X, storefront B uses logo Y" mechanism.

### No bulk upload

Each card accepts ONE file at a time. There is no merchant-facing "upload all seven brand assets in one shot" operation. The hidden file input does NOT have the `multiple` attribute. Dropping or picking multiple files only consumes the first.

### No crop / mask / effects

The only image processing the page performs is client-side downscale (via the shared `resizeImageIfNeeded` helper) that preserves aspect ratio. There is no:

- Crop tool.
- Mask / shape overlay (circular favicon mask, rounded-corner logo, etc.).
- Filter or effect application (brightness, contrast, grayscale).
- Background-removal.

The merchant must prepare their image in an external tool (Photoshop, Figma, Canva, etc.) before uploading.

### `brand_removal` plan-gate

This is the ONE plan-gate that affects the merchant's branding experience:

| Mapping | Shape | What it controls |
|---|---|---|
| `brand_removal` | Boolean (plan-level enable) | Whether the merchant can hide the **"Powered by CloudCart"** footer credit on the storefront. Enforced via the platform code — if the plan does NOT include `brand_removal`, the storefront ALWAYS renders the credit regardless of the merchant's `show_powered_by_info` toggle. When `brand_removal` IS included, the merchant's toggle on [[settings-general]] (Brand box) takes effect — they can hide the credit. |

Two important nuances:

1. The toggle that enforces this gate lives on **[[settings-general]]**, NOT on the Brand settings page documented here. The Brand settings page itself has no plan-gating — every plan can upload all seven brand assets equally.
2. The merchant's choice persists across plan changes. A downgrade re-asserts the "Powered by CloudCart" credit (because the gate evaluates false) but the merchant's toggle preference is preserved — re-upgrading restores the hidden state without re-toggling.

See [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]] for the broader plan-feature framework.

## Business rules

### Why the slot list is fixed

The seven slots correspond to the seven rendering contexts the platform supports natively: storefront header, browser tab, invoice PDF, transactional email header, product-fallback image, checkout page header, and OG image. There is no "freeform brand asset library" wireable into custom contexts. Merchants needing a brand asset for a non-platform context should upload via [[settings-files]] and reference the URL in the consumer (custom template, third-party app).

### Why no per-language / per-theme variants

The `Logo` and `FavIcon` models have no `locale` or `theme` column. The platform's current answer is "one logo per slot, designed to work across languages and themes" — sufficient for most merchants using language-neutral brand-strip / wordmark logos. Themes can override brand rendering in their own templates if they choose, but the platform-level model is locale- and theme-neutral.

### `brand_removal` is access-shaped, not feature-pack-shaped

The gate is a boolean plan-level enable, not a count or quota. Either the merchant's plan includes `brand_removal` and they can hide the credit, or it doesn't and they can't. No partial enablement, no "X uses per month" semantics.

### Plan downgrade re-asserts the credit

When a merchant downgrades to a plan without `brand_removal`, the storefront immediately re-asserts the "Powered by CloudCart" credit on the next page render (because the platform code evaluates the gate at render time). The merchant's toggle preference is NOT reset to off — it persists, so re-upgrading restores the hidden state immediately without re-toggling.

### The Brand settings page is permission-gated, not plan-gated

This page sits under the standard settings-area permission. A moderator needs the relevant section grant from [[settings-staff]] → Access permissions (broadly: `settings` or a more granular sub-permission depending on the moderator's role mapping). See [[merchant-roles]] for the full permissions tree. Plan does NOT restrict access to the page itself — every plan's merchants can reach `/admin/settings/brand` and manage their assets.

## Related

- [[settings-brand]] — hub.
- [[settings-brand-slots]] — the fixed seven-slot inventory.
- [[settings-general]] — where the `show_powered_by_info` toggle (enforced by `brand_removal`) actually lives.
- [[plan-gates]] — the plan-feature framework.
- [[plan-vs-feature-pack]] — access-shaped vs feature-pack-shaped gates.
- [[plan-features]] — per-feature upsell pages.
- [[design-theme-editor]] — per-theme image overrides as a workaround for per-language logos.
- [[merchant-roles]] — permissions tree.
- [[settings-staff]] — moderator access grants.

## Open questions

None.
