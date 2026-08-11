---
type: feature
nav_path: "Design → Modules → Content → Code"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Code module", "Raw HTML module", "HTML/JS module", "Custom code module", "extra.code", "code", "Модул код", "HTML блок", "JavaScript блок"]
tags: [design, modules, content, code, html, javascript, page-builder]
plan_gates: ["storefront_builder"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Code module (`extra.code`)

> Part of [[design-modules-content]]. See the category page for the other content modules.

## Purpose

The **Code** module is a raw HTML / JS block — the escape hatch for embedding third-party modules, analytics fragments, affiliate snippets, iframes, and any code the platform's other modules don't directly support. It is exposed primarily inside the Dynamic page builder (see [[marketing-landing-pages]]) — not as a standalone module INSTANCE on the storefront Modules screen. The merchant drops it onto a page in the builder, pastes the code, and the storefront renders it inside an isolated container.

Because the module renders the code AS IS — no sanitisation, no escaping — it is also the most dangerous module. A broken `<script>` block can hang the page; an unclosed tag can cascade into the layout.

## Where to find it

The Code module is available in the Dynamic page builder — see [[marketing-landing-pages]]. Open a Dynamic page in the builder, drag the **Code** block from the module palette, and paste the code into the textarea.

The Page Builder URL is gated by the `storefront_builder` plan feature — lower plans see a plan-upgrade prompt at the per-page builder URL. See [[plan-gates]].

The module is also available as a backing INSTANCE for any theme that registers a `code` slot (rare — most themes don't), surfaced under the **Others** tab on the Modules screen.

## What the merchant can do here

- Paste raw HTML / JS into a large textarea.
- Toggle the block on / off (enable / disable).
- Save (regenerates the page-builder render) / Reset / Cancel.

What the merchant CANNOT do here:

- Have CloudCart sanitise the code — it is rendered exactly as pasted.
- Embed `<script>` tags that reach the parent DOM directly when rendered inside the page-builder's `<iframe srcdoc>` container — the iframe sandboxing prevents direct DOM access. To send messages out, the script must use `postMessage`.
- Use this module to drop in store-wide analytics tags. For that, use [[design-custom-assets]] — those live in `<head>` / `<body>` boilerplate and persist across all pages.

## Settings & fields

| Field | Type | Restriction | Default | What it controls |
|-------|------|-------------|---------|------------------|
| `enabled` | toggle | `bool` | on | Master on / off. When off, the block renders empty. |
| `code` | textarea | `char:1,3000000` | empty | The raw HTML / JS content. Up to ~3 MB of code. |

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists the code; regenerates page-builder render | None | *"Module successfully edited"* |
| **Reset module** | Clears the code field back to empty | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes the panel without saving | None | — |

## Business rules

### NO server-side sanitisation

The module stores the merchant's input verbatim and renders it verbatim. There is no HTML sanitiser, no JavaScript checker, no tag stripping. Everything the merchant pastes ends up in the page. This means:

- A typo in a `<script>` block can crash the page.
- An unclosed `<div>` can cascade into the rest of the layout.
- A malicious snippet (XSS, crypto-miner) has nothing stopping it.

This is intentional — the module's whole purpose is to be the escape hatch.

### Page-builder iframe isolation

When the Code module renders inside a Dynamic page built in the [[marketing-landing-pages]] page builder, the platform wraps the rendered output in an `<iframe srcdoc="...">` with auto-height. This sandboxes the code — scripts inside cannot directly touch the parent page's DOM. They can only communicate via `window.postMessage`. This is what protects the surrounding storefront from a broken Code block — but it also means analytics scripts pasted here will not track page-views on the parent page.

### Variable replacement on read

Like [[design-module-text]], the Code module runs the body through a text-variables-replace pass on read — placeholders like `{store_name}` are substituted with runtime values before render. This is useful for embedding personalised affiliate links.

### Use [[design-custom-assets]] for store-wide tracking

Google Analytics, Facebook Pixel, and similar tracking tags belong in the [[design-custom-assets]] custom-head / custom-body snippets, NOT in a Code module on a single page. Tracking tags inside an iframe-sandboxed Code block will not fire on the parent page.

### 3 MB code cap

The `code` field is bounded at 3 000 000 characters — effectively unlimited for any reasonable embed.

### Cache invalidation on save / reset

Both **Save** and **Reset** regenerate the per-site cache key + the page-builder pre-rendered HTML for the affected page.

## Theme-specific notes

- **Primarily a page-builder block** — surfaced through the Dynamic page builder, not the Modules screen. A few themes register a `code` instance for a specific theme slot (e.g., a "below header" raw HTML block), but most do not.
- **`code` page-builder block** renders inside `<iframe srcdoc>` with auto-height. The iframe sandboxing is theme-agnostic — set by the page-builder rendering pass, not the theme.
- **For raw HTML in a standalone module surface** outside the page builder, use:
  - [[design-module-banner]] `type=script` slot — a 6-row textarea per banner, renders inline (no iframe sandbox). For small embed scripts.
  - [[design-custom-assets]] — for `<head>` / `<body>` boilerplate that should apply to every page.

## Related

- [[design-modules-content]] — hub.
- [[design-modules]] — parent module catalogue.
- [[marketing-landing-pages]] — Dynamic page builder; this is where the Code block primarily lives.
- [[design-custom-assets]] — store-wide custom `<head>` / `<body>` snippets (the correct place for analytics tags).
- [[design-module-banner]] — the `script` slot on banners is the inline (non-iframe) alternative for small HTML snippets.
- [[plan-gates]] — `storefront_builder` plan feature gates the Page Builder.

## Open questions

- 📡 **Iframe sandbox flags.** The exact `sandbox` attribute applied to the `<iframe srcdoc>` (whether `allow-scripts`, `allow-same-origin`, `allow-popups` are set) determines what merchant code can do. (verify) against the page-builder rendering code.
- 📡 **`postMessage` API contract.** Whether the platform listens to messages from Code-block iframes for height resizing / event tracking — (verify).
- 📡 **Per-language code content.** With `multylang`, the `code` field could store per-language variants — useful for localised affiliate snippets. (verify) whether the module supports this.
