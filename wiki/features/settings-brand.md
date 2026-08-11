---
type: feature
nav_path: "Settings → Brand settings"
route_name: brand.settings
route_path: /admin/settings/brand
aliases: ["Brand settings", "Brand", "Logos", "Favicon", "Лого", "Брандиране"]
tags: [settings, brand, logos, visual-identity]
plan_gates: ["brand_removal"]
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---
# Brand settings

## Purpose

The screen where the merchant uploads the seven brand assets that CloudCart uses across the store: the storefront header logo, the favicon (browser tab icon), the logo printed on invoices, the logo embedded in outgoing emails, a generic default product image used when a product has no photo, a special checkout-page logo, and the OpenGraph image used when the storefront is shared on social media. Each asset has its own card with drag-and-drop or click-to-upload, a preview thumbnail, a re-upload button, and a delete button. The page handles client-side image resizing before upload (except for the OG image which is a two-step file → URL flow) and clears the per-asset cache on save.

## Where to find it

Sidebar → Settings → **Brand settings**.

The page's breadcrumb reads "Settings → Brand settings". The route is `/admin/settings/brand`. The header icon is the images icon. Sub-header: *"Update your store's branding — logos, favicons, load image etc."*

## What the merchant can do here

- See all seven brand assets at once in a two-column grid (one column on mobile).
- For each asset card: drag-and-drop a file, click to open the picker, re-upload (↻ icon), or delete (trash icon → *"Remove logo?"* confirm).
- See a contextual preview module below each card (except OG image) showing how the asset is used in its actual context.
- See the recommended size + accepted file formats in the card's description text.
- See a global error banner above the grid if any upload failed.
- See an animated progress bar (0–90% during transfer, 100% on success, auto-cleared) on the active card.

What the merchant CANNOT do here:

- Set per-storefront / per-language brand variants — see [[settings-brand-limitations]].
- Reorder or rename the seven slots — they are fixed.
- Upload assets in bulk (one file per card).
- Crop, mask, or apply effects — only client-side downscale (preserves aspect ratio).

## Settings & fields

The page consists of seven fixed asset slots, each with its own card UI. The full slot inventory (slot IDs, backend labels, recommended sizes, storage backend) lives on [[settings-brand-slots]]. The card-level UI (drop zone, thumbnail, progress bar, re-upload / delete icons, preview module) and the client-side resize step are documented on [[settings-brand-upload-flow]].

Two slots have special behaviour:

- The **OG image** (`og_image_url`) uses a two-step file → URL flow and does not render the inline preview module — see [[settings-brand-og-image]].
- The **Favicon** uses a separate storage model with extra cache-busting on save — see [[settings-brand-favicon]].

The single "Remove logo?" confirmation modal (shared `CcDeleteComponent`) is opened from the trash icon on any card. On confirm, the slot deletes its asset and reverts to empty drop-zone state.

## Business rules

The seven slots, the storage split (six logo-model rows + one setting-value URL), client-side resize, and per-slot extension whitelisting are catalogued on [[settings-brand-slots]] and [[settings-brand-upload-flow]]. The slot-specific business rules — OG image two-step flow, Favicon cache-busting, per-slot cache flushing, `boarding_settings` flag, orphan cleanup, legacy-vs-modern endpoint split — are catalogued in the relevant aspect pages.

Cross-cutting rules (applied to every slot):

- **Seven fixed slots — neither configurable nor extensible.** The slot list is hard-coded; merchants can't add a "PDF receipt logo" slot.
- **No queue / no notifications / no webhooks fired.** Saving / deleting logos is purely synchronous: file upload → DB write → cache clear.
- **Permission.** This page sits under the standard settings-area permission — see [[merchant-roles]].
- **Saving updates `boarding_settings`.** Every successful save bumps `setting('boarding_settings')` to 1 so the onboarding wizard marks the branding step complete. See [[settings-brand-cache-and-storage]].
- **Error surface is global, not per-card.** All upload errors land in a single top-of-page red banner — see [[settings-brand-errors]].
- **SVG is NOT sanitised on upload** — see the security note on [[settings-brand-errors]].
- **Per-language / per-storefront variants are NOT supported** — see [[settings-brand-limitations]].

## Sub-pages (in this cluster)

- [[settings-brand-slots]] — the seven fixed slot definitions (slot ID, backend label, recommended size, storage backend, intended use).
- [[settings-brand-upload-flow]] — per-card UI (drop zone, thumbnail, progress bar, re-upload, delete confirm) + client-side resize step.
- [[settings-brand-og-image]] — the OG image two-step file → URL flow, missing preview module, orphan-file sweep.
- [[settings-brand-favicon]] — Favicon-specific storage (`FavIcon` model), `favicon_image` + `favicon_time` cache-busting, browser cache defeat.
- [[settings-brand-errors]] — global error banner, 422 response shape, allowed_extensions + allowed_mimetypes validation, SVG security note.
- [[settings-brand-cache-and-storage]] — per-slot cache flush, `boarding_settings` flag, legacy-vs-modern endpoint split, orphan-file pruning, two storage backends (Logo / FavIcon rows + setting value).
- [[settings-brand-limitations]] — fixed-slot list, no per-language / per-theme variants, no bulk upload, no crop, `brand_removal` plan-gate (lives on [[settings-general]], not here).

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `brand_removal` | Boolean (plan-level enable) | Whether the merchant can **hide the "Powered by CloudCart" footer credit** on the storefront. The toggle that enforces this lives on [[settings-general]] (Brand box), NOT on the Brand-assets page documented here. Brand-asset uploads (logos, favicon, OG image) on this page are NOT plan-gated. See [[settings-brand-limitations]] for the full plan-gate behaviour. |

## Related

- [[settings]] — parent hub.
- [[settings-general]] — store name and footer "Powered by CloudCart" toggle live there; brand identity is split across the two pages.
- [[settings-files]] — generic file upload screen used as a building block for the OG image step 1.
- [[settings-invoicing]] — uses the `invoice` logo on PDF invoices.
- [[settings-cart]] — checkout page uses the `checkout` logo.
- [[file-asset]] — entity page for files and uploaded media.
- [[merchant-roles]] — permissions tree for moderator access.

## Open questions

None.
