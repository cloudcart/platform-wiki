---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Button"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Button module", "Button block", "CTA button block", "Модул бутон"]
tags: [design, modules, page-builder, button, cta, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Button block (`button`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Button** block renders one to three call-to-action buttons inline on a Dynamic page. Each button carries its own link, target, label, colour, size, width, and HTML attributes. Use it for hero CTAs ("Shop now"), secondary actions ("Learn more"), or paired buttons in a banner ("Sign up | Browse catalogue").

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Button** from the block picker.

## What the merchant can do here

- Pick the **amount** (1, 2, or 3 buttons in the row).
- Pick the row **position** (`text-left` / `text-center` / `text-right`).
- For each button:
  - Set the link URL (internal or external).
  - Toggle "open in new tab" (target).
  - Set the button label (text).
  - Pick the button colour (theme-shipped variant).
  - Pick the button size (theme-shipped variant).
  - Toggle full-width.
  - Add custom HTML attributes (`data-*`, `id`, `aria-*`, etc.).
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot add more than 3 buttons in a single block — to render more, use multiple Button blocks.
- The merchant cannot configure the button corner-radius from here — that lives in [[design-module-buttons-settings]] and applies globally.
- The merchant cannot pick a "button to product" — for product-bound add-to-cart use [[design-module-pb-add-to-cart]].

## Settings & fields

### Row-level

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. |
| `amount` | select (1-3) | 1 | Number of buttons in the row. |
| `position` | select | `text-center` | Row alignment: `text-left` / `text-center` / `text-right`. |

### Per-button (1 to 3)

Each button in `buttons[i]` (or the top-level fields for amount=1) carries:

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `text` | text input | `''` | Button label. |
| `link` | URL input | `''` | Where the button goes. Internal `/page/...` or external `https://...`. |
| `target` | toggle | `false` | When ON, opens in a new tab (`target="_blank"`). |
| `color` | image-preview select | (theme) | Theme-shipped colour variant — applied via CSS class. |
| `size` | select | `''` | Theme-shipped size variant. |
| `full_width` | toggle | `''` | When ON, the button stretches to the column width. |
| `attributes` | text input | `''` | Custom HTML attributes appended to the `<a>` tag (e.g., `data-event="cta_click"`). |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]].

## Business rules

### Single-button vs. multi-button rendering

When `amount = 1`, the block renders a single `<a class="_button...">` with the row-level position. When `amount = 2` or `3`, the block renders a `<div class="_widget-buttons-wrap">` wrapping the buttons in a horizontal flex group — each button still carries its own colour / size / width.

### Picks up global button radii

Every button rendered by this block uses the `_button` CSS class, which means it inherits the global corner-radius set in [[design-module-buttons-settings]] and the theme's button colour palette. To override per-block, use [[design-custom-assets]] custom CSS.

### Custom attributes pass through unsanitized

The `attributes` field is rendered as raw text on the `<a>` tag. The merchant is responsible for valid HTML — there is no syntax validation. Common use: `data-gtm-id="hero-cta"`, `id="signup-cta"`, `rel="noopener"`.

### Empty `text` hides the button on the storefront

The template wraps the button's HTML in `{if $button->getSetting('text')}` — if the label is blank, the button (or the whole multi-button row) is skipped. The merchant must fill `text` for the button to render.

### No product / customer binding

Unlike [[design-module-pb-add-to-cart]], this block is a generic CTA — it does not bind to a product, doesn't trigger any cart action, and the customer just navigates to the link URL. Use the Add-to-cart block when you want a single-product purchase CTA.

## Related

- [[design-modules-page-builder]] — hub.
- [[design-module-pb-add-to-cart]] — sibling: product-bound add-to-cart button.
- [[design-module-buttons-settings]] — global button border-radius applied here.
- [[design-custom-assets]] — custom CSS for per-button overrides.
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **Per-button `target` semantics.** The toggle is a boolean; confirm whether it sets `target="_blank"` only or whether merchants need to add `rel="noopener noreferrer"` manually via `attributes`. (verify)
- 📡 **Theme-shipped colour / size catalogues.** Each theme ships its own palette of `_button` variants (`_primary`, `_secondary`, etc.) — the select shows what the theme advertises. (verify per theme)
