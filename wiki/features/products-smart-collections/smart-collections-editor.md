---
type: feature
nav_path: "Products → Smart Collections → Editor"
route_name: selections
route_path: /admin/products/smart-collections
aliases: ["Smart Collections editor", "Smart Collections modal", "Smart Collections Add Edit modal", "Selection editor", "Collection edit modal"]
tags: [products, collections, selections, editor, modal, seo]
plan_gates: ["product_collections"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[products-smart-collections]]. See the hub for the other aspects (list view, rule builder, rule types, evaluation, storefront side-effects, rules and limits).

# Smart Collections — Add / Edit modal

## Purpose

The right-side modal that opens when the merchant clicks **+ Add collection** or any existing collection row. It is the single editor for both create and edit flows — the inputs are identical; only the title and the persisted-vs-new state differ. It hosts the collection's identity (name), its rule set (the [[smart-collections-rule-builder]] block), and its storefront-publish metadata (SEO + URL handle).

## Where to find it

Sidebar → Products → **Smart Collections** → click **+ Add collection** or click any existing row. The modal opens on top of the list — see [[smart-collections-list-view]] for the entry points.

## What the merchant can do here

### Modal layout

The modal opens as a **right-side `xl`-sized modal** — it uses the `modal-right` class, slides in from the right edge of the screen rather than centering. The header carries a **Close** + **Save** button pair at the top; there is no footer (no-footer mode). The title reads *"Create new"* on create and *"Edit"* on edit.

### General settings card

- **Collection name** (required, single text input) — the merchant's label, shown on the storefront and in the admin.
- A `<hr/>` divider.
- **Criteria rule builder** — the multi-row condition editor that drives membership. See [[smart-collections-rule-builder]] for the full row layout and [[smart-collections-rule-types]] for the catalogue of fields the merchant can match against.

### Advanced settings card (collapsible)

- **SEO title** — `<title>` tag for the collection's storefront landing page.
- **SEO description** — meta description.
- **URL handle** — URL slug. Prefixed with `/selection/` (e.g., handle `summer-sale` → storefront URL `/selection/summer-sale`). Auto-derived from the collection name if left blank. The `/selection/` prefix is hardcoded — see [[smart-collections-storefront-side-effects]].
- **Canonical URL** — optional canonical link for SEO when the same collection content appears under multiple URLs.

The Advanced card is rendered through the shared `SeoGooglePreview` block — the same SEO preview / character count module used on Categories and other settings screens.

### What the merchant cannot do from this modal

- Manually pick specific products into the collection (the manual cross-sell list lives on each product's editor under Linked Products in [[products-products]]).
- See / edit which discounts are linked to the collection (discount management is in the Discounts feature; the list view does surface the linked discount(s) per collection — see [[smart-collections-list-view]]).
- Reorder products within a collection from this modal — product order on the storefront is governed by the product-field sort on the theme layer.

## Settings & fields

### Selection record fields (11 fields)

Each smart-collection record stores:

| Field | Purpose |
|---|---|
| `name` | Collection display name (required). |
| `description` | Long description. |
| `url_handle` | URL slug. Auto-derived from name if blank. |
| `seo_title` | SEO title for the storefront landing page. |
| `seo_description` | SEO meta description. |
| `canonical` | Canonical URL for SEO. |
| `executing` | Boolean — the Pending / Finished badge mechanism. See [[smart-collections-evaluation]]. |
| `products` | Cached product list — denormalised for quick storefront render. |
| `last_generated_at` | Timestamp of last evaluation completion. |
| `image` | Collection image. |
| `max_thumb_size` | Image thumbnail cap. |

### Field-length caps (server-side validated)

- **Collection name** — max **191 characters**. Required.
- **Description** — max **250,000 characters**.
- **URL handle** — max **255 characters**. Auto-derived from name if blank.

The rule-builder fields and their per-type caps (e.g., price 0–50,000) are catalogued on [[smart-collections-rule-types]].

## Business rules

### Save flips the collection to Pending

Every Save (create or edit) marks the collection's `executing` flag to `1`, queuing the regeneration job. The Status column on the list shows Pending until the job finishes — see [[smart-collections-evaluation]] for the three job sources and how the merchant recovers from stuck Pending.

### URL handle auto-derives from name

If the merchant leaves URL handle blank, the platform slugifies the collection name and stores that as the handle. Once persisted, editing the name does NOT re-derive the handle (changing the storefront URL on every rename would break inbound links). The merchant edits the handle explicitly when they want a different URL.

### SEO fields feed the storefront landing template

The SEO title, description, and canonical fields render directly into the `<head>` of the storefront `/selection/<slug>` page. Blank fields fall back to platform defaults (collection name as title, no canonical). The `SeoGooglePreview` block shows the merchant a live SERP-style preview of the values as they type.

### No autosave

Edits are committed only on **Save**. Closing the modal without saving discards changes — there is no draft state. (verify whether the platform shows an "unsaved changes" prompt on close)

### Right-side modal is intentional

The `modal-right` slide-in is the platform's convention for editor modals that need vertical room for the rule builder. The Close + Save pair lives at the top of the header (no footer) so the action buttons are visible regardless of scroll position when the rule list grows past one viewport.

## Related

- [[products-smart-collections]] — hub.
- [[smart-collections-list-view]] — where the merchant opens this modal.
- [[smart-collections-rule-builder]] — the criteria editor that lives inside the General card.
- [[smart-collections-rule-types]] — the catalogue of rule fields available in the builder.
- [[smart-collections-evaluation]] — what happens after Save (Pending → Finished).
- [[smart-collections-storefront-side-effects]] — what the SEO + URL handle fields drive on the storefront.
- [[smart-collection]] — entity page.

## Open questions

- (verify) Does the modal warn on close with unsaved changes, or silently discard?
- (verify) Renaming the collection — does the auto-slug ever re-derive, or only on the initial blank-handle save?
