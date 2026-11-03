---
type: feature
nav_path: "Internal admin → Blog modules side panel"
route_name: admin.storefront.widget.blog_panel
route_path: /admin/storefront/widgets/blog/panel
aliases: ["Blog panel module", "Blog modules side panel", "blog-panel", "blog_panel", "Модул панел блог", "Блог панел"]
tags: [design, modules, blog, panel, internal]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Storefront Modules — Blog modules side panel (`blog_panel`)

> Part of [[design-modules-blog]]. See the category page for the other blog modules.

## Purpose

The **Blog modules side panel** is a compact admin helper that lists JUST the blog tab's editable modules — Blog ([[design-module-blog-listing]]), Latest articles ([[design-module-blog-recent-articles]]), Last comments ([[design-module-blog-recent-comments]]) — without opening the full Modules screen grid. It's a navigation shortcut used by other admin surfaces (typically the page builder) to let the merchant pick a blog module to configure without leaving the page they're on.

This is NOT a module the customer sees on the storefront. It's an internal admin panel — a side-drawer that opens from a button or link on another admin screen.

## Where to find it

The panel is reachable via the URL `/admin/storefront/widgets/blog/panel` (route `admin.storefront.widget.blog_panel`). The merchant does NOT navigate to it directly from the sidebar — it opens as a side panel when another admin screen triggers it (typically a "Configure blog modules" button on the page builder).

If the merchant opens the URL directly, the panel still renders but appears unattached to a parent context.

## What the merchant can do here

- See three cards listing the blog tab's editable modules:
  - **Blog** — opens the [[design-module-blog-listing]] edit form.
  - **Latest articles** — opens the [[design-module-blog-recent-articles]] edit form.
  - **Last comments** — opens the [[design-module-blog-recent-comments]] edit form.
- Click any card to open that module's standard edit form in a side panel (same form as the Modules screen).
- Click **Close** (button on the right) or the dismiss "X" (top-left) to dismiss the panel without picking a module.

What the merchant CANNOT do here:

- Edit modules directly from this panel — clicking a card opens the standard module edit form; this panel is just the picker.
- See modules from other tabs (Products, User, Contacts, Others, Layout, Custom) — this panel is HARD-FILTERED to the `blog` tab only.
- Add a new blog module — same as the Modules screen, the catalogue is theme-fixed.
- Reorder the cards — order comes from the theme's `modules` block.

## Settings & fields

**None** — the panel has no merchant-editable fields. It's a list view.

| Element | Source |
|---|---|
| Panel title (**"Blog modules"**) | Translation key `sidebar.blog_widgets` |
| Close button | Translation key `sf.global.act.close` |
| Card title (per module) | Theme JSON `modules.{instance}.name` |
| Card description (per module) | Theme JSON `modules.{instance}.description` |
| Card URL | Route `admin.storefront.widget` with the instance name |

## Theme dependencies

Universal — every theme that has at least one blog module instance shows that instance as a card in this panel. Themes that don't ship blog modules render an empty panel (no cards, just the header).

The panel iterates over the merged `modules` block of the active theme JSON, filtered to `tab == 'blog'`. Whatever the theme declares is what the panel shows.

## Business rules

### Same source of truth as the Modules screen

The cards in this panel are the SAME module instances the merchant sees on the **Blogs, articles and comments** tab of the main Modules screen. Clicking a card here opens the SAME edit form. Edits made here are immediately reflected on the Modules screen and vice versa.

### Cards are filtered to `tab == 'blog'`

The Smarty template iterates the merged module list, but the outer `if ($tab == 'blog')` clause discards everything except the blog tab. Adding a custom module to a non-blog tab will not surface it here.

### Panel uses a dedicated CSS class for right-side rendering

The panel is styled with `.side-panel.blog-panel { right: 0 !important; }` so it anchors to the right edge of the parent screen. This positioning is hard-coded for this panel; other side panels position differently.

### Cards open in nested side panels

Each card link has `data-ajax-panel data-panel-class="medium"` — clicking it loads the module edit form INSIDE another side panel layered on top of this one. To return to the picker, the merchant closes the inner panel.

### No save / reset buttons HERE

This panel has nothing to save. Save / Reset happen on the per-module edit forms opened by clicking a card.

### Plan gating

None — the panel itself is universally available. Individual modules it lists may be gated (no blog modules currently are — see [[design-modules-blog]]).

## How it works (verified against backend)

### Route + controller

The route `admin.storefront.widget.blog_panel` maps to a controller method that:

1. Loads the platform code — returns the merged editable module catalogue, grouped by tab.
2. Renders `storefront.blog_panel` as a Smarty panel view, passing the catalogue.

### Template iteration

The template loops `foreach $modules as $tab => $data`, but the body wraps in `{if ($tab == 'blog')}` — so only the blog tab renders. Inside the blog block, it loops the tab's `groups` (sidebar groups, used as CSS hooks) and `modules` (cards).

### Card markup

Each card is an `<a>` with `data-ajax-panel data-panel-class="medium"` so clicking it triggers the nested-panel loader. The card title + description come from the theme's `modules.{instance}.name.{locale}` / `.description.{locale}` fields.

### Translation

Panel header label `sidebar.blog_widgets` resolves to **"Blog modules"** in English (and the locale equivalent in other languages).

### Why a separate panel exists

The page builder (when editing a Dynamic page) wants the merchant to be able to TUNE the blog module shown on the page without exiting the page builder. Opening the full Modules screen would lose the page-builder context. This panel exists as a focused alternative.

### No write-side endpoints

Unlike the standard module edit URL, this panel has no `save` or `reset` companion route — it's read-only navigation.

## Tips for merchants

- The merchant typically arrives here from a "Configure blog modules" button in the page builder. There's no top-level sidebar entry for this panel — searching the sidebar for it returns nothing.
- If a merchant asks "I clicked Configure blog modules and saw a small panel with three cards — what is it?" — that's this panel.
- The cards here are the same as the main Modules → Blog tab — there's no difference in behaviour, only in how the merchant arrived.
- If the panel appears empty, the active theme ships no blog module instances. The merchant should check the theme picker ([[design-themes]]) — a theme without blog support won't expose any blog modules.

## Related

- [[design-modules-blog]] — hub; the full blog module category.
- [[design-module-blog-listing]] — opened by the **Blog** card.
- [[design-module-blog-recent-articles]] — opened by the **Latest articles** card.
- [[design-module-blog-recent-comments]] — opened by the **Last comments** card.
- [[marketing-landing-pages]] — Dynamic page builder; primary caller of this panel.
- [[design-modules]] — main module catalogue; same edit forms surface here too.

## Open questions

- 📡 **Other callers of the panel.** Confirm whether any admin surface OTHER than the page builder opens this panel (verify). Searching the codebase for the route name suggests page builder is the only current caller.
- 📡 **Why blog-only and not a generic per-tab panel.** No generic `widget_panel/{tab}` route exists — the blog panel is the only one. Verify whether other tabs have similar shortcut panels planned.
