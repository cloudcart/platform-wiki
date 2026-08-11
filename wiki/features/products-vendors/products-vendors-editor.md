---
type: feature
nav_path: "Products → Vendors → Add / Edit"
route_name: vendors
route_path: /admin/products/vendors
aliases: ["Add vendor", "Edit vendor", "Vendor modal", "Vendor logo", "Vendor SEO", "URL handle", "Добави производител", "Редактирай производител"]
tags: [products, vendors, manufacturers, brands, editor, seo]
plan_gates: ["vendors"]
created: 2026-06-10
updated: 2026-06-10
source_count: 10
---

> Part of [[products-vendors]]. See the hub for the other aspects (the list + filters, business rules + backend behaviour).

# Vendors — Add / Edit modal

## Purpose

The create-and-edit form for a single vendor. It captures the vendor's display name and description, an optional logo, and the SEO settings that drive the vendor's storefront landing page. The same modal handles both creating a new vendor and editing an existing one.

## Where to find it

Sidebar → Products → **Vendors**, then click **+ Add vendor** (create) or any vendor row / its Edit icon (edit). The form opens as a standard modal on top of the list (see [[products-vendors-list]]).

## What the merchant can do here

- Enter the vendor's **Name** and a rich-text **Description**.
- Upload (or remove) a **Brand logo**.
- Expand **Advanced settings** to set the **SEO title**, **SEO description**, and **URL handle**, with a live preview of the `/vendor/<handle>` URL.
- **Save** to create or update the vendor; **Cancel** to discard.

## Settings & fields

The modal title is *"Add vendor"* on create, *"Edit vendor"* on edit. It is organised into three cards.

**General settings**
- **Name** — required free-text. The vendor's display name; appears in product listings, on the vendor landing page, and on customer-facing badges.
- **Description** — rich-text editor for the vendor's biography / company info. Shown on the vendor landing page.

**Logo** (separate card)
- **Brand logo** — single image upload (drag-and-drop or click-to-pick). When an image is already set, a Delete-image action becomes available. The logo appears on the vendor landing-page header and may be used in product cards / category listings depending on the storefront theme.

**Advanced settings (collapsible)**
- Rendered with `url-prefix="/vendor/"`, giving a live preview of the rendered URL (`{host}/vendor/{handle}`).
- **SEO title** — the `<title>` tag for the vendor's landing page.
- **SEO description** — the meta description.
- **URL handle** — the URL slug for the landing page, prefixed with `/vendor/` (a handle `apple` → storefront URL `/vendor/apple`). Auto-derived from the name when left blank.

### Field map

| Section | Field | Notes |
|---------|-------|-------|
| General | **Name** | Required. |
| General | **Description** | Optional rich-text. |
| Logo | **Brand logo** | Optional single image. |
| Advanced | **SEO title** | Defaults to the vendor name when blank. |
| Advanced | **SEO description** | Optional. |
| Advanced | **URL handle** | Defaults to a slugified version of the name when blank. Prefixed with `/vendor/`. |

### Validation caps & uniqueness

- **Name** — required, max **191** characters, must be unique store-wide (case-insensitive comparison). Saving a duplicate name returns *"The name has already been taken"*. A second model-layer uniqueness check catches near-duplicates that bypass the form (e.g., bulk imports).
- **Description** — optional, max **250,000** characters (effectively unlimited rich text).
- **URL handle** — optional input, max **191** characters; auto-derived from the name on first save when blank.
- **SEO title** — optional, max **191** characters; falls back to the vendor name in the storefront when blank.
- **SEO description** — optional, max **2,000** characters.

Validation messages are translated to the active store language.

## Business rules

### URL-handle auto-derivation + uniqueness

When the URL handle is left blank, the platform slugifies the vendor name and writes it to the handle. Two vendors cannot share a handle — if a slug already exists, the platform appends a numeric suffix automatically.

### One save = logo + fields in one request

The modal submits as `multipart/form-data` so the logo image rides along with the text fields in a single request. Save triggers the standard table refresh plus the vendor lifecycle events (see [[products-vendors-rules]]).

### Logo storage & orphan files

The uploaded logo is stored alongside other store assets (see [[settings-files]] for the storage backend). Logo removal has a dedicated Delete-image action in the modal. Deleting the **vendor** later does NOT automatically delete its logo file — it becomes orphan storage, so the merchant who wants to free the file should remove the image first.

### No "Generate with AI" button in this modal

The backend has AI endpoints that can produce a vendor name suggestion, description, and SEO copy from a free-form prompt, but the current modal does **not** wire them up — there is no "Improve with AI" / "Generate suggestion" button in the create / edit form. The endpoints exist for a possible future UI revision or for integrations, and have no merchant-facing entry point here today. `(verify — whether a later UI revision exposes these)`

## Related

- [[products-vendors]] — hub.
- [[products-vendors-rules]] — what fires on save (lifecycle events, listing-engine re-sync on a name change) and the `vendors` plan cap that can block a create.
- [[settings-files]] — where the uploaded logo is stored.
- [[seo-handling]] — how the SEO title / description / handle feed the vendor landing page.
- [[vendor]] — entity page.

## Open questions

- Whether a future Vue revision exposes the backend AI description endpoints as a modal button. `(verify)`
