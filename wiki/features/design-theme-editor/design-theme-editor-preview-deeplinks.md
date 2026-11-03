---
type: feature
nav_path: "Design → Theme Editor → Live preview & deep-links"
route_name: admin.css.builder
route_path: /admin/builder
aliases: ["Theme live preview", "Preview iframe", "Mobile tablet desktop preview", "Deep-link sub-tab", "Homepage builder link", "Theme Editor sidebar links"]
tags: [design, theme, preview, iframe, deep-links, layout-modules]
plan_gates: ["change_theme"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[design-theme-editor]]. See the hub for the other aspects (variables & types, colours, typography, images, save & reset, CSS compile).

# Theme Editor — Live preview & deep-links

## Purpose

The right-hand panel of `/admin/builder` is a live-preview `<iframe>` of the merchant's actual public storefront, with **Mobile** / **Tablet** / **Desktop** viewport toggles and a full-screen expander. The sidebar exposes **sub-tab deep-links** (`?colors`, `?typography`, `?images`) and **layout-module deep-links** (Header / Foot / Grid / Buttons, plus an optional Homepage page-builder link). This aspect documents how the preview behaves, how it auto-reloads on save, and how deep-links route the merchant in and out of the editor.

## Where to find it

`/admin/builder` — the iframe occupies the right-hand side of the editor; viewport buttons sit at the bottom-right of the iframe; sidebar deep-links sit below the three sub-tab links.

The Theme Editor opens as a **standalone full-screen builder** (not the normal admin layout) with a top-left **Back to CloudCart** link that returns to [[design-themes]].

## What the merchant can do here

### Live-preview iframe

- **See the merchant's actual public storefront** rendered in the iframe (homepage by default).
- **Toggle the iframe viewport width** between Mobile / Tablet / Desktop via the bottom-right buttons.
- **Full-screen the iframe** via the expander icon — the iframe expands to fill the editor.
- **NOT preview a colour / font / image change before Save** — the iframe shows the LIVE storefront, not a draft; new styles appear only after **Save theme** runs and the iframe auto-reloads.
- **NOT navigate the iframe to a different storefront page from the toolbar** — it stays on the homepage (verify whether non-homepage URLs are supported).

### Sub-tab deep-links

- **Open the Colours sub-tab directly** via `/admin/builder?colors`.
- **Open the Typography sub-tab directly** via `/admin/builder?typography`.
- **Open the Images sub-tab directly** via `/admin/builder?images`.

These query params are how the Design sidebar (and any external link into the editor) lands the merchant on a specific section without an extra click.

### Layout-module sidebar links

Below the three sub-tab links, the sidebar shows direct links into the layout modules the active theme exposes:

- **Header settings** — opens the Header module's edit panel.
- **Foot settings** — opens the Footer module's edit panel.
- **Grid settings** — opens the Grid module's edit panel.
- **Buttons settings** — opens the Buttons module's edit panel.

Each link is rendered ONLY if the active theme ships that module instance (a theme without a Grid module hides the Grid settings link). Clicking opens the same module edit panel the merchant would reach from [[design-modules]].

### Homepage page-builder link

- **Homepage** — shown only if the active theme advertises `page_builder`. Clicking opens [[marketing-landing-pages]]. Because the merchant typically has unsaved changes, the link **prompts with *"Save changes?"*** — on confirm it submits the form and then redirects; on cancel it redirects without saving.

### Back to CloudCart

- The top-left **Back to CloudCart** link in the standalone editor's top bar returns the merchant to [[design-themes]].

## Settings & fields

### Iframe URL

The preview loads the merchant's public storefront homepage URL directly — it is the same live site, with no separate sandbox or extra login.

### Viewport widths

| Button | Approximate width |
|--------|---------------------|
| **Mobile** | ~375px |
| **Tablet** | ~768px |
| **Desktop** | Full panel width |

The widths are CSS-driven on the iframe wrapper; the iframe itself doesn't navigate or reload when the merchant toggles widths.

### Deep-link query strings

| URL | Sub-tab opened on load |
|-----|------------------------|
| `/admin/builder` | Colours (default). |
| `/admin/builder?colors` | Colours. |
| `/admin/builder?typography` | Typography. |
| `/admin/builder?images` | Images. |

The query string is the only sub-tab activator on initial load — once the editor is open, the merchant uses the sidebar sub-tab links to switch.

## Business rules

### Live preview is the LIVE storefront, not a draft

The right-hand iframe is the merchant's actual public storefront URL — not a sandboxed preview. The merchant sees the new styles ONLY after **Save theme** runs and the storefront stylesheet is recompiled. There is no "preview before save" state. See [[design-theme-editor-save-reset]] for the Save flow and [[design-theme-editor-css-compile]] for the recompile.

### Iframe auto-reloads only on successful save

After a successful Save the iframe reloads so it re-renders against the recompiled stylesheet — see [[design-theme-editor-css-compile]] for the recompile that produces the new bytes. Failed saves do NOT reload (the merchant keeps editing the same draft form). Reset also auto-reloads on success.

### Three deep-link sub-tab anchors

On load, the `?colors` / `?typography` / `?images` query string auto-opens the matching sub-tab (see the table above) and takes precedence over any saved cookie / session state.

### Layout-module link visibility is theme-driven

Visibility is per-module-instance, not per-module-type, so a theme with two Grid module instances would surface only the first (verify).

### Homepage link is plan-gated and confirmation-gated

The Homepage sidebar link is shown only when the active theme advertises `page_builder`. The page-builder destination itself requires the `storefront_builder` plan-feature: the link can be visible, but clicking takes the merchant to the upsell screen if the plan is insufficient. The **"Save changes?"** confirm/cancel behaviour is covered in the action bullet above; see [[marketing-landing-pages]] for the destination.

### Adorimo "hire expert" inline card

A small inline card at the bottom of the sidebar promotes the **Hire expert** paid-services catalogue for merchants who want a designer to do the customisation. Clicking opens the paid-services panel; it doesn't navigate away from the editor.

### Plan gating (`change_theme`)

The `change_theme` plan-feature gates only the **Install action** at `storefront/templates/action/change/%` (used by the Reset → reinstall flow and [[design-themes]]'s theme-switch button). Lower plans cannot switch themes but CAN still edit the active theme's variables in this editor — the editor itself enforces no `change_theme` check. See [[plan-gates]], [[plan-features]].

### Permission

The Theme Editor, iframe, and all deep-links are gated by the `store.builder` permission key (also satisfied by the broader `store` key). A staff role without it sees no sidebar link and cannot reach the editor by URL.

## Related

- [[design-theme-editor]] — hub.
- [[design-theme-editor-save-reset]] — Save / Reset flow that the iframe auto-reload listens to.
- [[design-theme-editor-css-compile]] — recompile pipeline that produces the new stylesheet the iframe reloads against.
- [[design-themes]] — the destination of the Back to CloudCart link; also the source the editor opens from.
- [[design-modules]] — the home of the layout-module instances reached via the sidebar deep-links (Header / Foot / Grid / Buttons).
- [[marketing-landing-pages]] — homepage page-builder reached via the Homepage sidebar link.
- [[plan-gates]] / [[plan-features]] — `change_theme` and `storefront_builder` plan-feature mechanics.

## Open questions

- Whether the iframe officially supports navigating to a non-homepage URL (e.g., to preview a category page); the editor's controls don't expose this even though the iframe itself could load any storefront URL.
- Whether a theme with two instances of the same layout module surfaces both in the sidebar or only the first (verify).
