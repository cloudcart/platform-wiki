---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Code"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Code module", "Raw HTML block", "JS embed block", "Модул HTML", "Модул код"]
tags: [design, modules, page-builder, code, embed, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Code block (`code`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Code** block embeds an arbitrary HTML / JavaScript snippet on a Dynamic page. Use it for third-party modules (chat boxes, marketing pixels, custom forms, embedded videos), A/B test code, custom promo banners not available in the standard module catalogue, or any one-off content that doesn't map to a managed module.

This module is also documented at the utility level in [[design-modules-utility-page-builder]] — this aspect is the page-builder-specific deep dive.

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Code** from the block picker.

## What the merchant can do here

- Paste arbitrary HTML / JS into the `code` textarea (rows: 6 by default; the textarea is resizable).
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot validate the snippet from the form — the textarea is plain text.
- The merchant cannot use the block to inject snippets globally (every page) — use [[design-custom-assets]] for that.
- The merchant cannot use it for analytics tags / pixel codes that need to be in `<head>` — those need a global injection point ([[design-custom-assets]]).

## Settings & fields

| Field | Type | Validation | Default | Notes |
|-------|------|------------|---------|-------|
| `enabled` | toggle | `bool` | `true` | Master on/off. |
| `code` | textarea (rows: 6) | char:1-3,000,000 | `''` | Raw HTML / JS body. Accepts up to 3 million characters. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]].

## Business rules

### Output runs through text-variable replacement

Before render, the module pipes the snippet through `replaceTextVariables` — the same template-variable substitution used on `extra.text` content. So a merchant can write `{customer_name}` or `{store_name}` inside the snippet and the platform substitutes the current customer / store name at render time. (verify exact list of available variables)

### `nofilter` render — no escaping

The storefront template renders the snippet with the Smarty `nofilter` modifier — meaning the HTML is injected verbatim, no escaping, no sanitisation. The merchant is responsible for sane HTML / JS.

### Use a sandboxed iframe for untrusted code

The module does NOT wrap the snippet in an iframe sandbox. If the merchant pastes JavaScript that they don't fully control (e.g., a vendor pixel that mutates the DOM aggressively), it runs in the parent page's context with full DOM access. For dangerous third-party code, the merchant should manually wrap it in `<iframe srcdoc="...">` to sandbox it.

### Global vs. per-page injection

The Code block is per-page. To inject HTML / JS into EVERY page of the store (e.g., a chat module that should show site-wide), use [[design-custom-assets]] — that's the global injection point with `<head>` / `<body>` placement options.

### Analytics tags need a different surface

Google Analytics, Facebook Pixel, GTM container, and similar tracking tags need to load on every page, typically inside `<head>`. The Code block cannot place content in `<head>` — for those, use [[design-custom-assets]].

## Related

- [[design-modules-page-builder]] — hub.
- [[design-modules-utility-page-builder]] — broader catalogue of utility / page-builder modules.
- [[design-custom-assets]] — global HTML / JS / CSS injection (alternative to per-page Code blocks).
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **Variable substitution catalogue.** Exact list of `{variable}` tokens the snippet can use (`replaceTextVariables` map). (verify against the helper)
- 📡 **CSP behaviour.** Some merchants may have a stricter Content-Security-Policy — confirm whether inline `<script>` injected via this block is allowed. (verify per merchant)
