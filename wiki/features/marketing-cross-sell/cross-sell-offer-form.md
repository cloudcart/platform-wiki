---
type: feature
nav_path: "Marketing → Cross-Sell & UpSell → Offer form"
route_name: admin.cross_sell.diagram
route_path: /admin/marketing-new/cross-sell/diagram/{id?}
aliases: ["Cross-Sell offer form", "Cross-Sell create form", "Cross-Sell edit form", "Cross-Sell seven boxes", "Cross-Sell visual settings", "Cross-Sell date range"]
tags: [marketing, cross-sell, form, fields, diagram]
plan_gates: ["cross_sells"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-cross-sell]]. See the hub for the other aspects (trigger events, display modes & discounts, filters & limits, view tracking, engine comparison).

# Cross-Sell — the offer form

## Purpose

This is the **create / edit form** for a single Cross-Sell offer — the screen where the merchant defines what a customer sees, how it looks, when it fires, and what it offers. The form stacks **seven box sections** vertically. This page documents the boxes that describe the offer itself (titles, visual styling, product settings, date range); the conditions boxes are detailed on [[cross-sell-trigger-events]], and the display / discount boxes on [[cross-sell-display-discounts]].

## Where to find it

- Sidebar → Marketing → **Cross-Sell & UpSell** → **Add Cross Sell** (on the list — see [[marketing-cross-sell-list]]).
- The button routes to the visual diagram editor (`admin.cross_sell.diagram`). Each node in the diagram opens this field set in a **side-panel form**. The legacy `admin.cross_sell.edit` route still exists for direct form access but is not surfaced from the list.
- Direct: `/admin/marketing-new/cross-sell/diagram/{id?}`.

## What the merchant can do here

The form template stacks **seven boxes**. The three documented here:

### Box 1 — Product (root info)

- **Internal title** (`cross_sell[name]`, max 191) — visible only to the merchant.
- **Offer title** (`cross_sell[offer_title]`, max 191) — customer-facing label shown on the popup.
- **Description** (`cross_sell[description]`, TinyMCE rich-text editor) — long-form description shown on the popup.
- **Sandbox** checkbox in the box title-bar — toggles per-offer sandbox mode for testing without affecting live customers.

### Box 2 — Visual settings

- **Confetti effect** picker (`cross_sell[popup_effect]`) — a celebration animation that fires when the customer accepts the offer.
- **Background** colour picker (`cross_sell[background]`).
- **Text color** picker (`cross_sell[text_color]`).
- **Button background** colour picker (`cross_sell[button_background]`).
- **Button text color** picker (`cross_sell[button_text_color]`).
- **Button name** (`cross_sell[button_name]`) — text on the "Add to cart" / accept button.
- **Cancel button name** (`cross_sell[cancel_button_name]`) — text on the dismiss button.

### Box 7 — Date range

- **Active from** date input (`cross_sell[active_from]`, store date-format).
- **Active to** date input (`cross_sell[active_to]`) — disabled when the **No expiry** checkbox is ticked (`cross_sell[no_expire]`).
- **Display timer** checkbox (`cross_sell[meta][timer]`) — adds a countdown timer on the popup for urgency.

### Boxes 3-6 (covered elsewhere)

- **Box 3 — Target conditions** (event + targets) → [[cross-sell-trigger-events]].
- **Box 4 — Action conditions** (display type + offered products) → [[cross-sell-display-discounts]].
- **Box 5 — Product settings** (hide filters, max views) → [[cross-sell-filters-limits]].
- **Box 6 — Discounts** (`discount_type`, value) → [[cross-sell-display-discounts]].

### Storefront popup

Read-only — the customer-facing popup HTML the storefront renders when the offer fires. The merchant doesn't edit this template directly; they control its appearance via Box 1 (titles / description) + Box 2 (visual settings) above.

### What the merchant CANNOT do here

- **No multi-language preview** — the description / offer title is single-language; storefront language switching reuses the same text.
- **No bulk-edit of form fields** beyond status / duplicate / delete (see [[marketing-cross-sell-list]] bulk actions).

## Settings & fields

| Field | Key | Notes |
|---|---|---|
| Internal title | `cross_sell[name]` | max 191, merchant-only |
| Offer title | `cross_sell[offer_title]` | max 191, customer-facing |
| Description | `cross_sell[description]` | TinyMCE rich-text |
| Confetti effect | `cross_sell[popup_effect]` | accept animation |
| Background / text / button colours | `cross_sell[background]` etc. | colour pickers |
| Button name / cancel name | `cross_sell[button_name]` / `cross_sell[cancel_button_name]` | popup button labels |
| Active from / to | `cross_sell[active_from]` / `cross_sell[active_to]` | store date-format |
| No expiry | `cross_sell[no_expire]` | disables "Active to" |
| Display timer | `cross_sell[meta][timer]` | popup countdown |

### Validation per `error.validation.*`
- Offer title required: *"Моля, въведете заглавие на офертата."*
- Offer title min: *"Заглавието на офертата трябва да бъде минимум X знака."*
- Offer title max: *"Заглавието на офертата трябва да бъде по-малко от X знака."*

## Business rules

- **The offer is edited in a modal.** Opening an offer from the list shows its diagram page; the **Edit** button there opens this field set in a modal (not a separate full-page form). See [[marketing-up-sell-diagram]] for the diagram page shape.
- **Sandbox mode is per-offer**, set from the Box 1 title-bar checkbox — lets the merchant test an offer without affecting live customers.
- **The customer-facing popup is fully controlled from this form** — there is no separate template editor. Titles + colours + button labels + the optional timer are the only levers.
- **The "Active to" date is suppressed when "No expiry" is ticked** — `no_expire` and a populated `active_to` are mutually exclusive in the UI.

## Related

- [[marketing-cross-sell]] — hub.
- [[cross-sell-trigger-events]] — Box 3 (event + targets) detail.
- [[cross-sell-display-discounts]] — Box 4 + Box 6 (display mode + discounts) detail.
- [[cross-sell-filters-limits]] — Box 5 (product settings) detail.
- [[marketing-cross-sell-list]] — the list view this form is reached from.
- [[marketing-up-sell-diagram]] — the diagram editor that hosts this form as a side panel.

## Open questions

No outstanding questions.
