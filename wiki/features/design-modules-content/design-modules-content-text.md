---
type: feature
nav_path: "Design → Modules → Content → Text"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Text module", "Text block module", "TinyMCE module", "Static text module", "homeText module", "footerText module", "cartText module", "checkoutText module", "headerText module", "Text carousel module", "Rotating text module", "Testimonials module", "Модул текст", "Модул текстов карусел"]
tags: [design, modules, content, text, tinymce, testimonials]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Content modules — Text blocks + Text carousel

> Part of [[design-modules-content]]. See the hub for the carousel hero, banners, video, page-builder modules, and storage mechanics.

## Purpose

The text modules are the **rich-text editorial slots** of the storefront — every theme exposes a handful of named slots (e.g., `homeText1`, `footerText`, `cartText`) where the merchant types marketing copy, disclaimers, welcome messages, or shipping policy via a TinyMCE editor.

The `textCarousel` module extends this into a rotating multi-slide variant — typically used for testimonials, customer quotes, or rotating taglines.

Both module types are backed by the same underlying maps (`extra.text` and `extra.textCarousel`) but each named INSTANCE is an independent stored row.

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab:

- **Text fields** group — every `extra.text` instance the active theme ships.
- **Slider** group — the `textCarousel` instance(s).

Click the card to open the edit panel.

## What the merchant can do here

- Edit the rich-text body of each text instance (TinyMCE, up to 30 000 chars).
- Set the optional title heading shown above the text.
- For `textCarousel`, configure 1-20 rotating slides with HTML body, captions, schedule.
- Save / Reset / Cancel — full pipeline in [[design-modules-content-storage]].

The merchant CANNOT add a NEW text instance — only instances declared by the active theme have cards. For brand-new copy slots, build a Dynamic page in [[marketing-landing-pages]].

## Settings & fields

### Text block (`extra.text`) — fields

| Field | Type | Description / Validation | Default |
|-------|------|--------------------------|---------|
| `enabled` | toggle | Master on/off | on |
| `title` | text (0-250 chars) | Optional heading shown above the text content | "Example title" |
| `text` | rich text (TinyMCE, 1-30000 chars) | The block's main content — supports headings, lists, images, links, basic HTML | "Example text" |

For the `buttonToTop` INSTANCE (also internally an `extra.text` module), the title and text fields are HIDDEN — only the enable toggle is shown. See the back-to-top module in [[design-modules-navigation]].

### Known text-module instances by slot

The instance name is the slot identifier. The active theme decides which ones exist:

- `homeText1` / `homeText2` / `homeText3` — three independent text blocks on the homepage (each with its own slot).
- `welcomeText` / `homeWelcome` — welcome / hero text on the homepage.
- `headerText` — text in the header (e.g., *"Free shipping over X"*).
- `headerLeft` / `headerRight` — text before / after the logo.
- `footerText` / `footerContent` / `footerContacts` — text in the footer.
- `cartText` / `checkoutText` / `checkoutPrice` / `checkoutSideText` — text on the cart / checkout pages.
- `checkoutSignInGuestText` / `checkoutSignInLoginText` / `checkoutSignInRegisterText` — text shown during checkout based on the customer's sign-in state.
- `productText` — text shown on the product-detail page.
- `homeTopBanner` / `homeTopTextAfterCategoryShowcase` — text at specific homepage anchors.
- `homeVideoText` — text overlaid on the homepage video section.

### Text carousel (`extra.textCarousel`) — top-level controls

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `enabled` | toggle | Master on/off | on |
| `amount` | dropdown 1-20 | Number of slides | 1 |
| `full_width` | dropdown — **yes** / **no** | Stretch to viewport edges | yes |
| `slides_per_view` | dropdown 1-8 | Number of slides visible at once | 1 |
| `caption` | dropdown — **yes** / **no** | Show per-slide caption | yes |
| `controls` | dropdown — **yes** / **no** | Show prev / next arrows | yes |
| `indicators` | dropdown — **yes** / **no** | Show pagination dots | yes |
| `autoplay` | dropdown — **yes** / **no** | Auto-advance | yes |
| `interval` | number (ms) | Time between advances | 5000 |
| `cycle` | dropdown — **yes** / **no** | Loop back to first after last | yes |
| `pause` | dropdown — **yes** / **no** | Pause on hover | yes |
| `space_between` | number (px) | Margin between slides | 0 |

### Text carousel — per-slide fields (1-20)

| Field | Description |
|-------|-------------|
| `caption` | Short caption / heading for the slide |
| `html` | Rich-text content (TinyMCE) — the main text body |
| `sorting` | Sort order (ascending) |
| `from` / `to` | Schedule the slide (auto-show / auto-hide based on date range) |

## Business rules

### Each instance is independent

`homeText1`, `homeText2`, `homeText3` are three SEPARATE rows of stored JSON — saving copy into `homeText1` does not propagate to the others. The instance name tells the merchant which slot it fills; the module type (`extra.text`) tells the platform how to render it.

### Slot semantics from the name

The naming convention is the merchant's only signal of WHERE the text renders — `cartText` shows in the cart, `footerText` in the footer, `homeText1` in the first homepage slot. Hovering the card description reveals theme-specific guidance.

### Inline images are supported

TinyMCE allows inline images uploaded to the file manager and referenced inline. Useful for "as seen on" badges, small inline icons, or trust logos beside copy.

### When to use a Static page instead

For long-form content (about-us, policy text, terms), use a Static page in [[marketing-landing-pages]] and link to it from a text module. Text modules are best for short, prominent messaging — when the content runs past a few paragraphs, it belongs on its own page.

### Text carousel — pairs with testimonials

The most common `textCarousel` use is a "what our customers say" row on the homepage. Set `slides_per_view=3` and `space_between=30` for a clean three-up testimonials layout. Per-slide `from` / `to` lets the merchant rotate post-event customer feedback in / out automatically.

### Plan-gating

Neither text modules nor `textCarousel` are plan-gated — universally available.

### Per-language content via multylang

When the `multylang` app is installed, the body field stores per-language sub-keys (one body per language). Without the app, only one body is stored regardless of the storefront's language switcher. See [[design-modules-content-storage]] for the translation-merge mechanics.

## Tips

- The TinyMCE editor supports keyboard shortcuts (Ctrl-B, Ctrl-I, Ctrl-K for link) — faster than the toolbar.
- For testimonials, embed the customer's photo via inline image upload — much more compelling than text-only quotes.
- Use the per-slide schedule on `textCarousel` to time-limit post-event feedback (e.g., trade-show quotes from last month).
- The `title` field is optional — leave it blank if the slot doesn't have a heading.

## Related

- [[design-modules-content]] — hub.
- [[design-modules-content-carousel]] — image hero slider (shares scheduling shape with `textCarousel`).
- [[design-modules-content-banners]] — banner grids (shares the link-picker model).
- [[design-modules-content-storage]] — TinyMCE save pipeline + multylang translation merge.
- [[design-modules-navigation]] — `buttonToTop` (an `extra.text` module with hidden fields) and `htmlLine` (promo strip).
- [[marketing-landing-pages]] — Static / Dynamic pages for long-form copy.
- [[design-themes]] — theme decides which text instances exist.

## Open questions

None.
