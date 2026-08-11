---
type: concept
nav_path: "Concept → Module vs Page Builder block → Block mechanics"
aliases: ["Page Builder block mechanics", "Dynamic page composition", "Static page builder", "Drag-drop blocks", "Block per-page storage", "PageHistory 500-version cap", "autoSave", "Page Builder palette", "Блок — механика"]
tags: [design, modules, page-builder, concepts]
plan_gates: ["storefront_builder"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[widget-vs-page-builder-block]]. See the hub for the other aspects (module mechanics, shared template library, theme-switch behaviour, system pages + restrictions).

# Page Builder block mechanics

## Definition

A **Page Builder block** is a **drag-and-drop content element on a Dynamic page** — one of the four page types on [[marketing-landing-pages]] (Static / FAQ / External / **Dynamic**). The merchant composes a Dynamic page row-by-row, dragging blocks from a palette onto rows. Each block lives ONLY on the one page where it was dragged — there is no "global" block. Content is stored inside the Page's content JSON, keyed by page ID and the block's position in the page's row layout.

The Page Builder opens at `/admin/marketing/pages/builder/<page_id>` after the merchant creates / opens a Dynamic page. Usage is gated by the `storefront_builder` plan feature ([[widget-vs-pb-system-pages-and-restrictions]]).

## Scope

Covered:

- The drag-drop composition surface — rows + flex layout + per-block settings panel.
- Per-page storage — content JSON keyed by page ID.
- Version history — every save creates a `PageHistory` row; **500 most-recent snapshots retained per page**, older are auto-deleted on save. (verify)
- `autoSave` endpoint behaviour — fires on every drag / drop / edit, returns the history list panel + a fresh preview URL per snapshot. (verify)
- Cross-theme survival of blocks (covered in detail under [[widget-vs-pb-theme-switch-behavior]]).
- The palette catalogue — what blocks the merchant sees in the side palette (driven by the theme's page-builder block library).

Not covered:

- Module mechanics — see [[widget-vs-pb-module-mechanics]].
- The 25-template shared form library — see [[widget-vs-pb-shared-template-library]].
- Page-Builder–only block types (`code`, `store_locations`, `cc_form`, etc.) — listed in [[widget-vs-pb-shared-template-library]].
- The Static Pages screen itself (list + create + page-type selection) — see [[marketing-landing-pages]].
- System-page assignments + the `PageRestriction` rule for `blog.list` / `blog.view` — see [[widget-vs-pb-system-pages-and-restrictions]].

## Contrasts

- **Block vs. module — placement**: block placement is decided by the merchant (drag-drop). Module placement is decided by the theme. See [[widget-vs-pb-module-mechanics]].
- **Block vs. module — scope**: a block renders only on the one Dynamic page it was dragged onto. A module renders on every page with its slot.
- **Block vs. module — version history**: blocks have version history (up to 500 snapshots per page); modules do NOT.
- **Block vs. module — theme dependency at runtime**: a block's data is theme-independent (lives in the page JSON); rendering may degrade if the new theme doesn't ship the block type. See [[widget-vs-pb-theme-switch-behavior]].
- **Dynamic page vs. other page types**: Page Builder works only on Dynamic pages. Static / FAQ / External pages on [[marketing-landing-pages]] use TinyMCE or raw HTML, never the block palette.

## Where it applies

- [[marketing-landing-pages]] — Static Pages screen; the **Dynamic** page type opens the Page Builder.
- Route — `/admin/marketing/pages/builder/<page_id?>`.
- [[design-themes]] — the active theme declares which block types appear in the palette.
- [[plan-gates]] — `storefront_builder` gates Page Builder usage entirely.

## Composition surface — rows, palette, drag-drop

When the merchant creates a Dynamic page, the Page Builder presents:

- **A canvas of rows** — each row holds a horizontal flex layout. Rows stack vertically to form the page.
- **A side palette** — lists every block type the active theme declares in its page-builder block library. The palette is filtered by page type (system-page restrictions apply; see [[widget-vs-pb-system-pages-and-restrictions]]).
- **A drag-drop interaction** — merchant drags a block from the palette onto a row; clicks the block to open its settings panel; edits the form (driven by one of the 25 shared templates — see [[widget-vs-pb-shared-template-library]]).

Each block has its own settings, independent of other blocks. The page's full composition is saved as a JSON content blob on the Page row.

## Per-page storage

Block content is stored inside the Page's content JSON — separately from the global module-settings store ([[widget-vs-pb-module-mechanics]]). Implications:

- Two banners with the same content on two different Dynamic pages require **two separate block instances** on two pages. A module instance is configured once and renders on every page with its slot; a block is per-page.
- The block JSON travels with the page. Exporting / cloning a Dynamic page copies all its blocks.
- Switching themes does NOT delete blocks (covered under [[widget-vs-pb-theme-switch-behavior]]); the data persists even if the new theme can't render some block types.

## Version history — 500-snapshot cap per page

Every save of a Dynamic page creates a `PageHistory` row with the full content snapshot. The platform retains the **500 most-recent snapshots per page**; older versions beyond the 500 newest are auto-deleted on save. (verify)

The cap applies uniformly across both the legacy page editor and the modern Page Builder UI. The merchant rolls back to any of the most recent 500 saves via the Page Builder's history panel.

## `autoSave` — snapshot per change + preview URL

The Page Builder calls an `autoSave` endpoint for **every change** the merchant makes (drag, drop, edit a field). Each call:

- Creates a fresh `PageHistory` row capturing the new state.
- Returns the rendered history list panel for the side UI.
- Returns a **fresh preview URL** pointing at THAT specific snapshot's ID. The merchant can open the URL to view the snapshot live on the storefront — including before the merchant clicks the final "Save" / "Publish". (verify)

The 500-version cap is enforced inside `autoSave` too — every save deletes the rows beyond the most-recent 500.

## Palette catalogue — driven by the theme

The block types shown in the palette come from the active theme's page-builder block library (declared in `theme.json`). A theme that doesn't declare `yotpo-reviews` as a page-builder block won't show that block in the palette — even if the Yotpo app is installed. The merchant cannot enable a block type the active theme doesn't ship.

For the full catalogue of block types and which form templates serve them, see [[widget-vs-pb-shared-template-library]].

## Example: banner on one Static Page

1. Merchant creates a Dynamic page on **Marketing → Pages** → opens the Page Builder.
2. Drags a row → drags a `banner` block onto the row.
3. Configures the banner with custom images + links in the settings panel.
4. `autoSave` fires; the history sidebar updates with a new snapshot; the preview URL refreshes.
5. The banner renders ONLY on this Dynamic page (`/page/<slug>`). It doesn't appear elsewhere.
6. To put the same banner on the homepage, the merchant either drags another banner block into the homepage's Dynamic page OR configures the `bannersHomePage` [[widget-vs-pb-module-mechanics|module instance]].

## Related

- [[widget-vs-page-builder-block]] — hub.
- [[marketing-landing-pages]] — Static Pages screen + the Dynamic page type.
- [[design-themes]] — the theme decides what blocks appear in the palette.
- [[plan-gates]] — `storefront_builder` gates Page Builder usage.

## Open Questions

- Exact `PageHistory` retention behaviour at the 500th snapshot — confirmed cap but the precise delete order is unconfirmed. (verify)
- Whether `autoSave` debounces rapid edits or really creates one row per keystroke. (verify)
