---
type: feature
nav_path: "Products → Banners Labels → Create / Edit"
route_name: product-banners.create
route_path: /admin/products/banners-labels/create
aliases: ["Create banner", "Edit banner", "Create label", "Edit label", "Banner fields", "Label fields", "Image label fields", "Text label fields", "Полета на банер", "Полета на етикет"]
tags: [marketing, products, banners-labels]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 10
---

> Part of [[products-banners-labels]]. See the hub for the other aspects (targeting / auto-population, scheduling / lifecycle).

# Banners & Labels — fields & forms

## Purpose

The create / edit forms for the two badge types on the [[products-banners-labels]] screen — **Banners** (image labels) and **Labels** (text labels). This aspect covers the field-by-field shape of each form, the position choices, and the hex-colour and date validation rules. (For who the badge attaches to, see [[products-banners-labels-targeting]]; for when it shows on the storefront, see [[products-banners-labels-scheduling]].)

The distinction in one line:

- **Banner** = a small **image** overlay placed in a corner of the product card / detail page. The `Name` is an internal reference only — customers see only the image.
- **Label** = a coloured **text pill** (e.g., "SALE", "BESTSELLER", "-20%"). Here the `Name` **is** the visible badge text shown on the storefront.

## Where to find it

Sidebar → Products → **Banners Labels**. The top-right "Create new" button opens a modal that asks the merchant to choose:

- **Image label** → creates a Banner (route `product-banners.create`).
- **Text label** → creates a Label (route `product-labels.create`).

Editing reuses the same form. The distinct routes within this feature:

| Label | Route name | Route path |
|-------|------------|------------|
| Main wrapper | `product-banners-label` | `/admin/products/banners-labels` |
| Banners list | `product-banners.list` | `/admin/products/banners-labels` |
| Create banner | `product-banners.create` | `/admin/products/banners-labels/create` |
| Edit banner | `product-banners.edit` | `/admin/products/banners-labels/edit/banner/:id` |
| Labels list | `product-labels.list` | `/admin/products/banners-labels/labels` |
| Create label | `product-labels.create` | `/admin/products/banners-labels/create` (modal pick) |
| Edit label | `product-labels.edit` | `/admin/products/banners-labels/edit/label/:id` |

## What the merchant can do here

### Create / edit a banner (image label)

Fields:

- **Name** — required, max 191 chars; the merchant's reference. **NOT shown to customers** — only the image renders.
- **Description** — optional, max 64,000 chars; internal notes.
- **Image** — required; the actual badge image (PNG / JPG, transparency supported). Min / max size depends on theme.
- **Position** — required; one of `tl` / `tr` / `bl` / `br` — decides which corner of the product card the banner overlays.
- **Active from** / **Active to** — optional scheduling dates (see [[products-banners-labels-scheduling]]).
- **Status** — Active / Inactive toggle.
- **Conditions** — required, 1-2 rows (see [[products-banners-labels-targeting]]).

### Create / edit a label (text label)

Fields:

- **Name** — required, max 191 chars; **this IS the badge text shown on the storefront**.
- **Description** — optional, max 64,000 chars; internal notes.
- **Color** — background colour, validated as `#RRGGBB` hex.
- **Text color** — text colour, validated as `#RRGGBB` hex.
- **Position** — same `tl` / `tr` / `bl` / `br` choices.
- **Active from** / **Active to** / **Status** — same as banner.
- **Conditions** — same target system as banner (see [[products-banners-labels-targeting]]).

### What the merchant CANNOT do here

- Animate / use video for banners (image-only).
- Use a "preview" mode — the only way to verify is on the live site after save.
- Set per-language banners (one image / label applies to all languages on the site; for multi-language stores keep the image language-neutral).
- Make a banner / label apply only to certain **variants** — it is product-level, not variant-level.

## Settings & fields

### Positions

| `position` | Corner |
|------------|--------|
| `tl` | top-left |
| `tr` | top-right |
| `bl` | bottom-left |
| `br` | bottom-right (default) |

If two badges land on the same corner of the same product, the theme stacks them visually — but the merchant should arrange positions so they don't collide (e.g., put "Sale" top-left and "Free shipping" top-right). See the open question on [[products-banners-labels]] about stacking order.

### Field reference

| Field | Banner | Label |
|-------|--------|-------|
| `name` | internal reference (hidden) | visible badge text |
| `description` | optional, ≤ 64,000 chars | optional, ≤ 64,000 chars |
| `image` | required | n/a |
| `color` / `text_color` | n/a | `#RRGGBB` hex |
| `position` | `tl` / `tr` / `bl` / `br` | `tl` / `tr` / `bl` / `br` |

## Business rules

### Hex colour validation (labels only)

The Color and Text color fields must match `#[a-fA-F0-9]{6}` exactly — 6-character hex with a leading `#`. Short forms (e.g., `#fff`) and named colours (e.g., `red`) are **rejected**. An empty value is allowed (theme falls back to its default colour).

### Date validation

`active_to` must be **≥** `active_from`, otherwise the form rejects with *"must be a date after or equal to the active from date"*. The scheduling semantics that follow from these dates live on [[products-banners-labels-scheduling]].

### Conditions are mandatory

Every banner / label needs at least one condition row before it can save (the targeting rules — 1 minimum, 2 maximum — are detailed on [[products-banners-labels-targeting]]).

### Name length

Both `name` fields cap at 191 chars. For labels this directly limits the visible badge text; keep it short ("SALE", "-20%") so it fits the pill on the product card.

## Related

- [[products-banners-labels]] — hub.
- [[products-banners-labels-targeting]] — the conditions / record-type system that every form's Conditions block feeds into.
- [[products-banners-labels-scheduling]] — what `status` + `active_from` + `active_to` mean on the storefront.
- [[products-products]] — products that get the badges.
- [[product]] — entity page.

## Open questions

- Exact min / max image dimensions per theme are theme-dependent and not surfaced in the form. `(verify)`
