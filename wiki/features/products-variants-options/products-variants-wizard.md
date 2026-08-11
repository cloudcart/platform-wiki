---
type: feature
nav_path: "Products → Variants → Add variant (wizard)"
route_name: variants-index.new
route_path: /admin/products/variants
aliases: ["Create variant wizard", "Add variant", "Variant wizard", "Edit variant parameter", "Помощник за варианти"]
tags: [products, variants, wizard, modal]
plan_gates: ["multi_variants", "variants.listing"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Variants — create / edit wizard

> Part of [[products-variants-options]]. See the hub for the other aspects (list table, types, values, listing toggle, data model, API).

## Purpose

The 2-step modal behind **+ Add variant** on the Variants list (see [[products-variants-list-table]]). Step 1 defines the parameter (Name + Type + advanced toggles); Step 2 sets the initial option values. The single-screen Edit modal (no Step 2) uses the same Step 1 fields and is reached by clicking an existing parameter's name on the list.

## Where to find it

Sidebar → Products → **Variants** → click **+ Add variant** (or click an existing parameter's Name to open the Edit modal).

The wizard runs inside a single modal with a horizontal progress indicator at the top showing "STEP 1 — Variant settings" and "STEP 2 — Set Variant values" (active step highlighted purple).

## What the merchant can do here

- Step 1: name a new variant parameter, choose its option type, and (paid) flip the "Show each variant as a separate product in listing" + "Include the variant name in the product title" toggles.
- Step 2: bulk-create the initial option values for the new parameter, in the input shape that matches the chosen type.
- Navigate back to Step 1 from Step 2 (the parameter persists; the merchant can keep iterating).
- Use the Edit modal (single screen) to rename or retype an existing parameter, subject to the "type locked once products use it" rule — see [[products-variants-data-model]].
- Add more values later from the per-parameter Values sub-page (see [[products-variants-values]]).

## Settings & fields

### Step 1 — Variant settings

**General settings card:**

- **Name** — required, max 150 characters, **unique store-wide** (can't have two parameters both called "Color").
- **Option type** — radio selector with 6 visual previews: **Select option** / **Radio button** / **Image sample** / **Color sample** / **2D schema** / **Numeric alpha**. Required. Catalog: see [[products-variants-types]].
- Info-box linking to the help article *"Get more detailed information about creating product variants"*.

**Advanced settings card (collapsible):**

- **Show each variant as a separate product in the product listing** — paid plan feature; a "Paid" badge appears when the merchant lacks the `variants.listing` subscription. Full mechanics: see [[products-variants-listing-toggle]].
- **Include the variant name in the product title** — visible only when `variants.listing` is active. When ON, the product card title becomes `<base product name> - <variant value>`.

**Server-side timing.** The parameter is **created on the server when Next is clicked** (not when Save is clicked at the end). So refreshing mid-wizard leaves an empty parameter that the merchant can finish from the Values sub-page (see [[products-variants-values]]).

### Step 2 — Set Variant values

The field shape depends on the type chosen in Step 1:

| Type chosen | Field shape on Step 2 |
|---|---|
| **Select / Radio / 2D / Numeric alpha** | `tag`-mode multi-input where the merchant types value names; pressing Enter / comma creates new tags. Autocomplete against existing options for this parameter via `/admin/api/core/variant-parameters/{id}/options/autocomplete`. |
| **Image sample** | Per-row inputs (Name + Image file upload). |
| **Color sample** | Per-row inputs (Name + Hex color picker, default `#FFFFFF`). |

Reorder, edit, delete rows inline. An info-box reads *"You can add or remove values later from the respective value list for this variant."*

**Back** returns to Step 1 (the created parameter persists). **Save** posts the values as a bulk-create FormData payload to the parameter's options endpoint. After Save, the wizard closes and the new parameter is invalidated into the table cache.

### Edit-parameter modal (single screen)

Clicking an existing parameter row's name on the Variants list opens an Edit modal — same Step 1 fields (Name, Option type radio, advanced toggles) but without the progress indicator and without Step 2. Save commits via PATCH to the parameter; toast: *"Updated successfully."*

The Type field is editable but **cannot be changed** once products use the parameter (validated server-side; see [[products-variants-data-model]]). To switch type, the merchant creates a new parameter and migrates products.

## Business rules

### Parameter name validation

- Required, max 150 characters, **unique across the store**.
- Type field required, must be one of: `select`, `radio`, `image`, `color`, `2d`, `numeric_alpha`. Type-specific value validation runs in Step 2 — see [[products-variants-types]].

### Wizard half-finished state

Because the parameter is persisted at the Step 1 → Step 2 transition (not at Save), a merchant who closes the modal between steps leaves an **empty parameter** in the table. They can re-open the Values sub-page later to add values (see [[products-variants-values]]). This is intentional: it avoids losing the Step 1 data if the connection drops on Step 2.

### Paid badge + pack-purchase prompt

When the merchant flips the "Show each variant as a separate product in listing" toggle without the `variants.listing` plan feature, the request is rejected and the per-feature pack-purchase modal opens. Mechanics + 24-hour throttle: see [[products-variants-listing-toggle]].

### Side effects on Save

- **Search re-index** — newly active variant parameters trigger a storefront search-engine resync.
- **Storefront cache invalidation** — variant pickers, product listings, and category-page caches are flushed.
- **No merchant webhook** for parameter / value CRUD — the `product.created` / `product.updated` webhooks don't fire on parameter changes alone.

## Related

- [[products-variants-options]] — hub.
- [[products-variants-list-table]] — list screen the wizard launches from.
- [[products-variants-types]] — catalogue of the 6 option types + per-type value validation.
- [[products-variants-values]] — the Values sub-page for ongoing value management after Step 2.
- [[products-variants-listing-toggle]] — the paid "separate product in listing" toggle behaviour.
- [[products-variants-data-model]] — hard caps + "type locked once in use" rule the Edit modal enforces.

## Open questions

None.
