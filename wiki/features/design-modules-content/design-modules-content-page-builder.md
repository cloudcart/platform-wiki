---
type: feature
nav_path: "Design → Modules → Content → Page builder blocks"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Page builder content modules", "Title module", "Separator module", "Page builder video module", "Dynamic page modules"]
tags: [design, modules, content, page-builder, dynamic-pages]
plan_gates: ["storefront_builder", "static_pages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Content modules — Page-builder-only blocks

> Part of [[design-modules-content]]. See the hub for the carousel hero, banners, text blocks, video, and storage mechanics.

## Purpose

Three content modules are registered with the platform but **NEVER appear on the Modules screen** — they exist only as building blocks inside the Dynamic page builder:

- **`title`** — a heading element (`h1`-`h6`).
- **`separator`** — a horizontal divider line.
- **`video`** — a single-video embed (YouTube / Vimeo / Vbox7 / raw embed / HTML5). The full settings table is in [[design-modules-content-video]].

These modules exist because Dynamic pages need building blocks (headings, dividers, videos) that don't belong as standalone instances on the storefront-wide Modules screen — they're per-page composition primitives, not theme-slot fillers.

## Where to find it

Open [[marketing-landing-pages]] → pick a Dynamic page → click **Edit page builder** → drag the block from the block picker into a row → click the block to open the edit panel.

The Page Builder URL is gated by the `storefront_builder` plan feature — lower plans get redirected to the upsell when they reach the per-page builder URL.

## What the merchant can do here

- Drop a `title`, `separator`, or `video` block anywhere in a Dynamic page's row / column grid.
- Configure each block via the inline edit panel.
- Save the page — Save / Reset / Cancel mechanics are shared with all modules, see [[design-modules-content-storage]].
- Reorder blocks within rows by drag-drop.

What the merchant CANNOT do:

- Use these modules outside a Dynamic page. They are absent from the Modules screen.
- Open the Page Builder without the `storefront_builder` plan feature.
- Create more Dynamic pages than the `static_pages` numeric quota allows.

## Settings & fields

### `title` module

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `tag` | dropdown — **h1** / **h2** / **h3** / **h4** / **h5** / **h6** | Which heading level to render (controls visual size + SEO weight) | h2 |
| `title` | text | The heading text itself | empty |

Plain text only — no rich formatting. For richer headings (inline icons or links), use a Text module with a heading inside instead.

### `separator` module

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `style` | dropdown — **Solid** / **Dashed** / **Dotted** / **Double** | Line style | Solid |
| `position` | dropdown — **Center** / **Left** / **Right** | Where the (shorter than full-width) line sits | Center |
| `color` | colour picker | Line colour (hex) | empty |
| `margin_top` | number (px) | Vertical spacing above | 0 |
| `margin_bottom` | number (px) | Vertical spacing below | 0 |
| `height` | number (px) | Thickness of the line | 1 |
| `width` | number (px or %) | Length of the line | 100% |

### `video` module

See [[design-modules-content-video]] for the full field table — settings are shared between page-builder placement and the (rare) theme-instance placement.

## Business rules

### Page-builder-only — not on the Modules screen

These modules are intentionally excluded from the Modules screen because their semantics are *per-page composition*, not *storefront-wide slot*. The Modules screen catalogues theme-declared instances; these blocks are composed fresh per Dynamic page.

### Page Builder access gate — `storefront_builder`

The Page Builder URL itself is gated by the `storefront_builder` plan feature via a callback restriction. Lower plans get redirected to the upsell when they open the per-page builder URL. Once inside, the `title`, `separator`, and `video` blocks are universally available — no per-block plan gate.

### Page count gate — `static_pages`

The number of Dynamic pages a merchant can create is bounded by the `static_pages` numeric quota. Adding a page past the cap surfaces the HTTP 402 paywall modal with a *"Upgrade your quota from here"* link to the [[plan-features]] upsell. The quota can be extended via packs ([[plan-vs-feature-pack]]).

### Pre-rendered HTML stored per row

For pre-rendered HTML the platform stores the rendered output on the page row so storefront requests don't re-execute the modules. Edits in the page builder re-render and re-save the row. The detailed page-builder rendering pipeline is in [[design-modules-content-storage]].

### Block-rendering registry

Page-builder content goes through a separate rendering pass from the theme-slot modules. The page is stored as a tree of rows → columns → modules, each module carrying its own `settings` JSON. The page-builder iterates the tree, instantiates each module by `map` from the page-builder module registry, sets its settings, and fetches its template HTML.

### Heading hierarchy and SEO

Pick `h1` for the page's main heading (only ONE per page) and `h2` / `h3` for sub-sections. Search engines weight `h1` heavily — multiple `h1` tags or wrong nesting hurts ranking.

## Tips

- For a subtle break, use `separator` at 1px height with a light-grey colour.
- Set `width` to a percentage (e.g., `60%`) and combine with `position: center` for an Apple-style centred separator.
- Combine `title` + `separator` + `text` for a clean section-heading block — heading, divider, body copy.
- Use the page builder's column grid (multiple `video` blocks side-by-side) for a video-gallery layout that the standalone `videoSlider` doesn't provide.

## Related

- [[design-modules-content]] — hub.
- [[design-modules-content-video]] — full `video` field table (shared with page-builder).
- [[design-modules-content-storage]] — page-builder rendering pipeline and Page Builder access gate.
- [[marketing-landing-pages]] — Dynamic / Static page management.
- [[plan-gates]] — `storefront_builder` callback gate; `static_pages` numeric quota.
- [[plan-vs-feature-pack]] — extending `static_pages` via packs.
- [[plan-features]] — upsell page reached on quota / feature breach.
- [[widget-vs-page-builder-block]] — concept explaining why these modules are page-builder-only.

## Open questions

None.
