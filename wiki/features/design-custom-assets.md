---
type: feature
nav_path: "Design → Custom CSS/JS"
route_name: admin.custom.assets
route_path: /admin/storefront/custom-assets
aliases: ["Custom CSS/JS", "Custom assets", "Custom CSS", "Custom JavaScript", "Custom code", "Storefront custom code", "Tracking code", "Tracking pixel", "Персонализиран код", "Custom JS", "Тракинг код", "Глобален код", "Custom HTML"]
tags: [design, custom, css, js, advanced]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 0
---
# Custom CSS/JS

## Purpose

The **Custom CSS/JS** screen is the merchant's "escape hatch" for inserting **arbitrary HTML, CSS, or JavaScript** into the head of every storefront page. This is the place to drop in third-party tracking pixels (Facebook Pixel, TikTok Pixel, Hotjar, etc. — when the dedicated integrations aren't enough), self-hosted webfont declarations (`@font-face`), chat-module snippets, A/B-testing tools, or per-store CSS overrides that the [[design-theme-editor]] doesn't expose as a named variable. The merchant pastes raw markup into a single full-width **CodeMirror code editor**; whatever they paste is injected verbatim into the `<head>` of every storefront page.

This is an **advanced surface**: there is no validation, no sanitisation, no preview, no per-page targeting, and no plan gating. The merchant is fully trusted to write safe markup — bad code on this screen breaks the storefront immediately and globally.

This page is a hub. The detail of the editor, the injection mechanics, and the storage / lifecycle behaviour each live on their own aspect page below.

## Where to find it

Sidebar → **Design** → **Custom CSS/JS** (sidebar label *Custom CSS/JS*). The link appears immediately below the **Colors and typography** link, within the same "Design edit" section of the Design sidebar.

The route is `/admin/storefront/custom-assets`. The breadcrumb reads **Design** → **Custom CSS/JS**.

Sub-routes:

| Action | Route name | Path | Method |
|--------|------------|------|--------|
| Open the editor | `admin.custom.assets` | `/admin/storefront/custom-assets` | GET |
| Save edited code | `admin.custom.assets_save` | `/admin/storefront/custom-assets/save` | POST |

There is no separate reset / delete endpoint — to remove all custom code, the merchant clears the editor and saves an empty string (see [[design-custom-assets-storage]]).

## Sub-pages (in this cluster)

This screen is split into 3 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[design-custom-assets-editor]] — the CodeMirror `htmlmixed` editor; the single `custom_assets` field; what kinds of markup can be pasted; what the merchant can and cannot do (no preview, no rollback, no per-page targeting); the Save action.
- [[design-custom-assets-injection]] — where the code lands (`<head>` of every storefront page), the render order vs theme stylesheets, no sanitisation, no per-page filter, the read path.
- [[design-custom-assets-storage]] — per-theme storage row (`custom-css-js`), theme-switching hides/reveals code, empty-save as the only off-switch, no version history, no cache invalidation, plan / permission gating, the disabled server-side parse helper.

## What the merchant can do here

The screen is a single full-width form with one big CodeMirror editor for pasting any combination of HTML, `<style>`, and `<script>` markup, then a **Save** action that persists the content. The full editor capabilities (modes, line numbers, folding, resize) and the catalogue of what the merchant **cannot** do (no preview, no per-page targeting, no rollback, no enable/disable toggle) are documented on [[design-custom-assets-editor]].

## Settings & fields

The screen has exactly **one editable field** — `custom_assets`, a free-form HTML / CSS / JS blob with no required value and no documented size cap — plus the **Edit** (Save) action. Field format, editor configuration, and the save confirmation message are detailed on [[design-custom-assets-editor]].

## Business rules

The business rules split across the aspect pages:

- **Stored per active theme** — switching themes hides the current custom code; each theme keeps its own row. See [[design-custom-assets-storage]].
- **Injected verbatim into the `<head>` of every page** — no per-page filter, no sanitisation, CSS overrides the theme's stylesheet by render order. See [[design-custom-assets-injection]].
- **Save replaces the full content** — no append / merge / version history; the merchant must keep their own backup. See [[design-custom-assets-storage]].
- **Empty save removes all custom code** — the only "off switch". See [[design-custom-assets-storage]].
- **No plan gate, no permission of its own** — every plan tier can use it; the sidebar link sits behind the `store.builder` permission. See [[design-custom-assets-storage]].

## Related

- [[design]] — parent Design pillar.
- [[design-custom-assets-editor]] — the editor UI + field + Save action (aspect).
- [[design-custom-assets-injection]] — where and how the code is injected (aspect).
- [[design-custom-assets-storage]] — storage, theme-scoping, lifecycle, gating (aspect).
- [[design-theme-editor]] — sibling; the variable-based customiser for colours, fonts, and layout variables (use this first; reach for Custom CSS/JS only when a needed style is not exposed as a variable).
- [[design-themes]] — theme picker; switching themes hides the current custom code.
- [[design-modules]] — sibling; some modules (Banner `script` slots, Navigation `snippet` items) also accept raw HTML / JS for per-slot embedding.
- [[design-navigation]] — the Navigation `snippet` item type also accepts raw HTML / JS (up to 12,000 chars per menu item) for in-line menu embeds.
- [[marketing-seo]] — SEO hub (meta info, tracking codes via the dedicated integrations).
- [[apps]] — many third-party integrations (Facebook Pixel, Google Analytics, etc.) have dedicated apps; prefer those when available.
- [[settings-brand]] — favicon / logo / social-share image (separate concern from custom head code).

## Open questions

- ⏸️ **Cache invalidation after save.** Saving does not flush external caches. Storefront CDN / Cloudflare caches may serve the old page until the cache TTL expires; merchants making time-sensitive changes should flush their CDN manually. See [[design-custom-assets-storage]].
- ⏸️ **Conflict with dedicated app integrations.** Not detected by the platform — merchants who install an integration app (e.g., Facebook Pixel) AND paste the pixel here will fire both. Avoid duplication manually.
