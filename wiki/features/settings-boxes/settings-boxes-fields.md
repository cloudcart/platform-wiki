---
type: feature
nav_path: "Settings → Delivery boxes → Create / Edit box"
route_name: boxes.settings
route_path: /admin/settings/boxes
aliases: ["Box fields", "Box dimensions", "Add delivery box", "Edit box", "Box create modal", "Полета на кашон", "Размери на кашон"]
tags: [settings, boxes, shipping, packaging, fields]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[settings-boxes]]. See the hub for related aspects (the box-packing algorithm, and the box lifecycle / delete / permission rules).

# Delivery boxes — list table & box fields

## Purpose

This aspect documents every visible field and control on the Delivery boxes screen: the list table, the Create / Edit modal layout, the eight numeric box fields (six dimensions + two weights), their validation rules, the pre-filled default values, and the no-confirmation delete behaviour. This is the section a support agent cites when a merchant asks "what do I type in this box?" or "why won't the form save?".

## Where to find it

Sidebar → Settings → **Delivery boxes**. Click **+ Add delivery box** to open the create modal, or click any row's name to open the edit modal.

## What the merchant can do here

- See all defined boxes in a table: Name, Outer dimensions (L × W × H), Inner dimensions (L × W × H), per-row Edit / Delete.
- Click **+ Add delivery box** to open the create modal.
- Click any row name to open the edit modal.
- Delete a box via the row trash icon.
- Sort by name (default sort: id desc — newest first).

## Settings & fields

### List table

| Column | Notes |
|--------|-------|
| **Name** | Click to edit. Sortable. |
| **Outer dimensions (L × W × H)** | Not sortable. |
| **Inner dimensions (L × W × H)** | Not sortable. |
| **(actions)** | Per-row remove button. |

### Create / Edit modal

| Field | Type | Constraints |
|-------|------|-------------|
| **Name** (`name`) | string | Required. |
| **Outer height** (`outer_height`) | number (mm) | Required. Min 1. Step 1. |
| **Outer width** (`outer_width`) | number (mm) | Required. Min 1. Step 1. |
| **Outer length** (`outer_depth`) | number (mm) | Required. Min 1. Step 1. The field is labelled "Outer length" but the underlying column is `outer_depth`. |
| **Inner height** (`inner_height`) | number (mm) | Required. Min 1. Step 1. Must be **strictly less than** `outer_height`. |
| **Inner width** (`inner_width`) | number (mm) | Required. Min 1. Step 1. Must be **strictly less than** `outer_width`. |
| **Inner length** (`inner_depth`) | number (mm) | Required. Min 1. Step 1. Must be **strictly less than** `outer_depth`. The field is labelled "Inner length" but the underlying column is `inner_depth`. |
| **Empty weight** (`empty_weight`) | number (g) | Required. Min 1. Step 1. Must be **strictly less than** `max_weight`. The box's own packaging weight. |
| **Max weight** (`max_weight`) | number (g) | Required. Min 1. Step 1. Maximum total content weight the box can hold. |

Both weight fields are **server-side required** — backend validation rejects a save if either is missing or zero. The backend treats them as core fields alongside the six dimension fields; there is no path to create a box without all eight numeric values. Box-packing for couriers that bill on total weight uses `empty_weight` to add packaging weight to the order, and uses `max_weight` to cap how much can be packed into the box (see [[settings-boxes-packing]]).

### Create / Edit modal layout (verified)

The modal is an `xl` size modal split into three visual zones around a central SVG box illustration:

| Zone | Fields | Notes |
|------|--------|-------|
| Top row | Name | Single full-width input. |
| Left column | Outer height, Inner height | Stacked vertically on desktop. |
| Center | Decorative SVG illustration | Box with dimension arrows (height/length/width labels). Renders smaller on mobile (`200×100`) vs desktop (`346×182`). |
| Right column | Empty weight, Max weight | Both in grams. |
| Bottom row (4-col grid) | Outer length, Inner length, Outer width, Inner width | All in millimetres. |

The SVG illustration is **decorative** — it does not respond to the entered dimensions or reflect proportions dynamically.

Modal title: **"Add Box"** for create / **"Edit `<box name>`"** for edit. Backdrop click is **enabled** (`no-close-on-backdrop: false`) — but blocked while a save is in progress (`saving=true`).

### Default values when opening the Create modal

When the merchant clicks **+ Add delivery box**, the form is pre-filled with these sample values:

- Outer dimensions: 10 mm × 10 mm × 10 mm (all three axes)
- Inner dimensions: 8 mm × 8 mm × 8 mm (all three axes)
- Empty weight: 10 g
- Max weight: 1000 g

These are illustrative defaults — the merchant should overwrite them all before saving. Without overwriting, the form passes validation (10 > 8, 1000 > 10) and creates a tiny 1-cm box with 1-kg capacity, which is rarely useful.

### Delete confirmation (none)

Deleting a box from the row trash icon is a **direct delete** — there is no confirmation modal in front of the delete action. A single accidental click immediately removes the box. (Compare with Banned IP and other tables which DO surface a confirmation.) The merchant relies on the bottom-of-screen toast *"Deleted successfully"* as the only feedback. The lifecycle consequences of deleting a box are covered on [[settings-boxes-lifecycle]].

## Business rules

### Frontend validation: inner must be strictly less than outer

The Create / Edit modal enforces these **client-side validation rules** before submitting:

- `inner_height < outer_height` — error: *"Inner height must be less than outer height"*
- `inner_width < outer_width` — error: *"Inner width must be less than outer width"*
- `inner_depth < outer_depth` — error: *"Inner depth must be less than outer depth"*
- `empty_weight < max_weight` — error: *"Empty weight must be less than max weight"*

If a merchant tries to enter equal inner and outer dimensions (e.g., 100 mm on both), the form blocks the save. The backend validation itself enforces only "required" (it does NOT cross-check inner < outer), so an API client bypassing the UI could theoretically submit equal values — but the standard merchant path uses the modal and gets the strict client-side check.

### Dimensions in millimetres only

The millimetre input directive constrains values to millimetres. No unit conversion is offered in the UI — a merchant thinking in centimetres has to multiply by 10 (10 cm = 100 mm). This is a common source of merchant confusion. There is no global "switch to centimetres" preference anywhere in the admin; the decision is intentional because couriers' tariff APIs almost universally expect millimetres, so storing them natively avoids conversion-rounding errors.

## Related

- [[settings-boxes]] — hub.
- [[settings-boxes]] — entity page; the data model behind each row.
- [[settings-staff]] — the moderator permission that gates this screen.

## Open questions

None.
