---
type: feature
nav_path: "Design → Modules → Others (Други) → Top bar (Горна част) → Promo bar (Промо лента)"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Promo bar module", "Promobar module", "htmlLine", "extra.htmlLine", "HTML line module", "Top bar module", "Промо лента", "Модул промо лента"]
tags: [design, modules, navigation, header, promo, marketing]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 7
---

# Storefront Modules — Promo bar (`htmlLine`)

> Part of [[design-modules-navigation]]. See the category page for the other navigation modules.

## Purpose

The **Promo bar** module — **"Промо лента"** in the Bulgarian admin, internal name `htmlLine` — renders a thin horizontal strip, usually at the very TOP of the storefront above the header (it is the storefront's **top bar / промо лента**), with a short marketing message and an optional call-to-action button. Common uses: "Free shipping over X", "Black Friday — 30% off", "Use code SALE10 at checkout". This **is** the store's promo / announcement bar — the one a merchant means by "топ лента" / "top bar".

The bar can be SCHEDULED via `From` / `To` dates, so the merchant can pre-configure promo announcements weeks in advance. Outside the date window, the bar is auto-hidden regardless of the master enable toggle.

## Where to find it

| Surface | Location |
|---------|----------|
| Storefront slot | Top of the page (above header) by default; bottom on themes using `header-two` template (configurable) |
| Admin edit card | Sidebar → **Дизайн → Модули** (`/admin/storefront/widgets`) → tab **Други** (Others) → group **Горна част** (Top bar) → card **Промо лента** |

The module key is `extra.htmlLine`; the instance name is `htmlLine`. There is one instance per store.

Every built-in theme that has the bar puts it in the **Горна част** group of the **Други** tab, beside the other top-of-page modules (see [[design-modules-cross-tabs-groups]]).

## What the merchant can do here

- **Master enable / disable** the bar.
- **Schedule a display window** via `From` / `To` datetime fields (optional; both blank = always-on once enabled).
- **Write the message** in the rich-text editor: formatting, links, and an image button that inserts a picture from the store's files ([[settings-files]], up to 1024 MB per file); its code view also takes HTML such as an image tag.
- **Optionally show a CTA button** next to the message:
  - Pick left / right side.
  - Set the button text (e.g., "Shop now").
  - Set the button URL.
  - Toggle open-in-new-tab.
- **Pick top / bottom placement** — only when the active header is the `header-two` template (more on this in *Theme-specific notes*).

What the merchant CANNOT do:

- Run multiple promo bars at once — single instance per store.
- Target pages or customer segments — the bar shows on every page to everyone. For one page, use a [[marketing-landing-pages]] Dynamic page instead.
- A cart-driven **"spend X more for free shipping"** meter in the bar — its line is **static text**. The live hint exists only in the checkout summary ([[checkout-page-steps]]) and Bump Cart ([[apps-bumpcart]]).

### This is the only announcement / free-shipping bar — no App Store app provides one

The top-of-storefront announcement strip (including a *"Free shipping over X"* line) is this native module, besides the static text blocks ([[design-modules-content-text]]) and banners ([[design-modules-content-banners]]). **No App Store app** renders an announcement or free-shipping bar; the marketing apps place offers inside product and cart pages ([[apps-up-cross-sell]]). So a *"where is my announcement bar configured"* ticket resolves to this module, never to an app.

## Settings & fields

### Top-level fields

| Setting key | Type | Default | Allowed values | Limits | Validation | Notes |
|---|---|---|---|---|---|---|
| `enabled` | bool (switch) | `false` | `yes` / off | — | — | Master on/off |
| `period.from` | datetime | "" | store date+time format (e.g., `dd-mm-yyyy HH:MM:SS`); stored as UTC | — | optional | Start showing the bar from this date/time; outside window → auto-hide |
| `period.to` | datetime | "" | store date+time format; stored as UTC | — | optional | Stop showing the bar after this date/time |
| `text` | rich text (TinyMCE) | "" | HTML | — | **required** if displayed | Promo message body; empty / whitespace / tags-only → bar auto-hides |
| `promobar_position` | enum (select) | `bottom` | `top` / `bottom` | `in:top,bottom` | optional | Honoured only on the `header-two` header template; ignored otherwise |
| `cookie_name` | string (hidden) | empty | md5 hash | — | auto-generated on save | Keeps the dismissible-bar cookie unique per save; NOT in the form |

### Button group (only validated when `button.enabled` is true)

| Setting key | Type | Default | Allowed values | Validation | Notes |
|---|---|---|---|---|---|
| `button.enabled` | bool (switch) | `true` | `yes` / off | — | When off, all other `button.*` fields are unused |
| `button.float` | enum (select) | `right` | `left` / `right` | optional | Which side of the bar the button sits on |
| `button.text` | string | `View more` | free text | **required** when button enabled | CTA label |
| `button.link` | URL | "" | valid URL | **required + url validation** when button enabled | Where the button takes the customer |
| `button.target` | string (checkbox) | `_blank` | `_blank` / empty (`_self`) | optional | Open-in-new-tab |

When `button.enabled` is off, the platform skips validation for `button.text` and `button.link`.

### Theme-specific notes

- **Top vs bottom placement.** The `promobar_position` field only appears in the form when the active header is the `header-two` template. On any other header, position is pinned by the theme — usually top, but it varies.
- **Sticky behaviour.** Some themes stick the bar to the top as the customer scrolls; others let it scroll away. Theme-controlled, not configurable.
- **Single-line vs multi-line.** Long `text` may wrap or overflow depending on the theme's CSS. Keep messages short.

## Business rules

### Auto-hide outside the scheduled window

`period.from` / `period.to` are evaluated against current UTC time at render. If `from` is in the future OR `to` is in the past, the bar is force-hidden — regardless of the master toggle. A "Black Friday week" promo can be pre-configured weeks ahead and will appear / disappear automatically.

### Auto-hide on Lighthouse / pagespeed audits

The bar force-hides itself for Lighthouse / pagespeed test requests. Intentional — the promo bar can slow First Contentful Paint, and the platform protects performance metrics.

### Auto-hide when text is empty

If `text` has no visible text (blank, whitespace or tags only), the bar is force-hidden. An image counts as a tag, so an **image-only bar never shows**: keep at least one character of text beside the image. The platform sets no recommended image size; the picture shows at the size its HTML gives, within the theme's bar styling.

### Datetime conversion to UTC

The merchant enters `period.from` / `period.to` in store-local time using the store's `date_format` + `time_format`. On save the values are converted to UTC; at render they are compared against UTC.

### Cookie name auto-rotated on every save

The shared bar template carries a close control, handled by each theme's script (verify per theme). Closing sets a cookie named after `cookie_name`, which is regenerated on every save, so a customer who closed last week's promo sees the new one.

### Button text auto-hides when empty

Even with `button.enabled = true`, clearing the button text force-hides the button. The merchant can keep the button toggled on globally but suppress it for one promo by leaving the text blank.

### Cache invalidation

Save / Reset regenerate the storefront cache key. Guests see it within 20 minutes ([[storefront-arch-caching-invalidation]]).

### No plan-gating

`extra.htmlLine` is not in the `paid_widgets` allowlist — available on every plan.

### Translation behaviour

With `multylang` installed, `text` and `button.text` accept per-language entries via the language switcher inside the TinyMCE editor. Without it, only one language is stored.

## Related

- [[design-modules-navigation]] — hub.
- [[design-modules]] — parent module catalogue.
- [[marketing-landing-pages]] — Dynamic pages for per-page promo strips.
- [[marketing-discounts]] — Discount campaigns the promo bar typically advertises.
- [[design-themes]] — theme controls bar's CSS, stickiness, and default position (top vs bottom).

## Open questions

- 📡 **Per-language text.** With `multylang` installed, per-language entries are stored. Confirm the `multylang` app is installed for the store.
- ⏸️ **Lighthouse detection method.** Confirm which audit bots are caught (PageSpeed, GTmetrix, etc.).
