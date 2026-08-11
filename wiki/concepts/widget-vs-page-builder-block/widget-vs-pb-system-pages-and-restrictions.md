---
type: concept
nav_path: "Concept → Module vs Page Builder block → System pages + restrictions"
aliases: ["System-page assignment", "Builder system pages", "home thank-you 404 Dynamic page", "blog.list required module", "blog.view required module", "PageRestriction", "storefront_builder plan gate", "video_slider_widget plan gate", "Plan gates Page Builder", "Системни страници"]
tags: [design, modules, page-builder, plan-gates, concepts]
plan_gates: ["storefront_builder", "video_slider_widget"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[widget-vs-page-builder-block]]. See the hub for the other aspects (module mechanics, block mechanics, shared template library, theme-switch behaviour).

# System pages + plan-gate restrictions

## Definition

The Page Builder isn't only for custom landing pages — a Dynamic page can be **assigned to a system slot** to replace the theme's default `home`, `thank_you`, or `error.404` page. This gives the merchant a drag-drop way to compose the store's homepage and post-checkout pages. Two layers of restrictions apply:

- **`PageRestriction`** — a per-system-page rule that REQUIRES specific blocks. Currently only `blog.list` and `blog.view` enforce required-module rules. (verify)
- **Plan-feature gates** — `storefront_builder` gates Page Builder usage entirely; `video_slider_widget` gates a single module (Video Slider) at the module layer.

## Scope

Covered:

- The system-page slots a Dynamic page can be assigned to (`home`, `thank_you`, `error.404`, `blog.list`, `blog.view`).
- The `PageRestriction` table's enforced rules and the error message the merchant sees on save.
- Which system pages have NO enforced required-module rule.
- The `storefront_builder` plan gate (Page Builder usage).
- The hardcoded `site_id` allowlist (`3819`, `9674`) that bypasses `storefront_builder` at the platform level.
- The `video_slider_widget` plan gate (Video Slider module).
- The behaviour at the storefront when the merchant's plan downgrades below the gate.

Not covered:

- The Static Pages list / **Assigned to** dropdown UI — see [[marketing-landing-pages]].
- The Modules screen behaviour for the Video Slider module specifically — see [[design-modules]].
- Generic plan-gate behaviour across the platform — see [[plan-gates]].
- Block content storage — see [[widget-vs-pb-block-mechanics]].

## Contrasts

- **Blog system pages vs. home / thank-you / 404**: `blog.list` and `blog.view` enforce a required-block rule (`blog-list` / `blog-view` must be present). `home`, `thank_you`, `error.404` do NOT enforce any required block — the merchant can save them empty. (verify)
- **Plan gate on creation vs. plan gate on render**: `storefront_builder` blocks Dynamic page CREATION at the admin layer AND suppresses Page Builder content RENDERING on the storefront for downgraded merchants. (verify)
- **Plan gate vs. site_id allowlist**: hardcoded `site_id`s (`3819`, `9674`) bypass `storefront_builder` regardless of plan. This is a CloudCart-set carve-out, NOT a plan upgrade. (verify)
- **Page-level gate vs. module-level gate**: `storefront_builder` gates the entire Page Builder surface. `video_slider_widget` gates a single module (Video Slider). No other module has a plan gate.
- **System-page assignment vs. ordinary Dynamic page**: an unassigned Dynamic page serves at `/page/<slug>`. An assigned one replaces the theme's default rendering for the chosen system slot (`/`, `/thankyou`, etc.).

## Where it applies

- [[marketing-landing-pages]] — Static Pages screen; **Assigned to** dropdown.
- [[plan-gates]] — `storefront_builder` + `video_slider_widget` definitions.
- [[plan-features]] — plan-feature paywall surface.
- [[design-modules]] — Video Slider module edit panel hits the `video_slider_widget` gate.

## System-page assignment

On [[marketing-landing-pages]], a Dynamic page can be assigned via the **Assigned to** dropdown to one of these system slots:

| System slot | What it replaces | Required block (if any) |
|-------------|------------------|-------------------------|
| `home` | Theme's default homepage | None enforced. (verify) |
| `thank_you` | Theme's default post-checkout thank-you page | None enforced. (verify) |
| `error.404` | Theme's default 404 page | None enforced. (verify) |
| `blog.list` | Theme's default blog index | **MUST include `blog-list` block**. |
| `blog.view` | Theme's default blog-article page | **MUST include `blog-view` block**. |

When the merchant assigns a Dynamic page to a system slot:

- The page-builder page replaces the theme's default rendering for that slot.
- The storefront serves the Dynamic page's composition instead of the theme's hardcoded layout.

This is the merchant's main alternative to the theme's default homepage / thank-you / 404 — a drag-drop composition instead of a fixed theme layout.

## `PageRestriction` — only two rules enforced

The platform's required-module enforcement is a helper that ships only **two rules**:

- `blog.list` system page → MUST contain a `blog-list` block.
- `blog.view` system page → MUST contain a `blog-view` block.

If the merchant tries to save a Dynamic page assigned to `blog.list` without a `blog-list` block, validation fails with the error message:

> *"You must add module ":module" for publish this page"*

(The `":module"` placeholder is filled with the missing block type, e.g., `"blog-list"`.)

For `home`, `thank_you`, `error.404`: **NO required-block rule is enforced**. The merchant CAN save an empty homepage Dynamic page with no products block. Whether the resulting storefront page looks reasonable is up to the theme's fallback rendering. (Earlier documentation may have suggested a "homepage requires products" rule — that rule is NOT enforced.)

## `storefront_builder` — gates Page Builder usage

The `storefront_builder` plan feature gates **Page Builder usage end-to-end**:

- The **Dynamic** page-type card on **Marketing → Pages → New** is hidden / blocked for merchants whose plan doesn't include the feature. They cannot create new Dynamic pages.
- For Dynamic pages created BEFORE the plan downgrade, the platform's the platform code helper returns `true` and **suppresses Page Builder content rendering on the storefront** for those merchants. (verify) Existing Dynamic pages effectively render as empty until the plan is upgraded again.
- A **hardcoded `site_id` allowlist** at the platform level (`3819`, `9674`) bypasses this restriction — those two specific stores can use Page Builder regardless of plan. This is a permanent CloudCart-set carve-out, NOT a plan upgrade. (verify) Merchants outside this allowlist must be on a plan that includes `storefront_builder`.

## `video_slider_widget` — gates one module

A single module instance — the **Video Slider** (`extra.videoSlider` type) — is gated by the `video_slider_widget` plan feature:

- Opening the Video Slider edit panel without the plan feature triggers a plan-upgrade prompt.
- The Video Slider module is **HIDDEN from the storefront** when the plan doesn't include the feature.

No other module is currently plan-gated. The merchant's plan affects only the Video Slider module + Page Builder usage; every other module instance the active theme declares is available on all plans (subject to app-conditional loading — see [[widget-vs-pb-module-mechanics]]).

## Per-block restrictions beyond the two enforced rules

`PageRestriction` can theoretically carry more per-module-type restrictions, but only the `blog.list` / `blog.view` rules are populated. (verify) No "homepage must contain a products block", no "thank-you page must contain order-details" — the merchant CAN ship an empty homepage Dynamic page; the Modules / Theme fallback layer is what keeps such pages from looking entirely broken.

## Example: assigning a Dynamic page to `home`

1. Merchant picks the **Dynamic** page type on **Marketing → Pages → New**. (Requires `storefront_builder` OR site_id in the allowlist.)
2. Drags a banner row + a product-showcase block in the Page Builder.
3. Sets **Assigned to** = `home` → saves. No `PageRestriction` error fires.
4. The storefront `/` URL now serves this composition instead of the theme's default homepage.
5. If the plan later drops `storefront_builder`, the page still exists but Page Builder content is suppressed on the storefront — the merchant must upgrade or reassign to recover.

## Related

- [[widget-vs-page-builder-block]] — hub.
- [[marketing-landing-pages]] — Static Pages screen + **Assigned to** dropdown.
- [[plan-gates]] — `storefront_builder` + `video_slider_widget` gate definitions.
- [[plan-features]] — plan-feature paywall the merchant hits.
- [[design-modules]] — Video Slider module surface.

## Open Questions

- Whether the `site_id` allowlist (`3819`, `9674`) is still active in production or is a legacy carve-out. (verify)
- Whether the platform code suppresses the entire page or just blocks individually. (verify)
- Whether a Dynamic page assigned to `home` while `storefront_builder` is inactive falls back to the theme's default homepage or to a blank page. (verify)
