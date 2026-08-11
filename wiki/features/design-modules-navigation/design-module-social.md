---
type: feature
nav_path: "Design → Modules → Navigation → Social"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Social module", "social", "extra.social", "Social icons module", "Social network links module", "Модул социални мрежи", "Социални икони"]
tags: [design, modules, navigation, footer, social]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Storefront Modules — Social (`social`)

> Part of [[design-modules-navigation]]. See the category page for the other navigation modules.

## Purpose

The **Social** module renders the row of social-network icons that link out to the store's social presences — Facebook, X (formerly Twitter), Instagram, Pinterest, YouTube, LinkedIn, TikTok. Each network has its own URL field and visibility toggle.

The module typically lives in the footer near the social-proof block; some themes also drop it in the header or on the contact page. This is one of the few modules the merchant configures from the Modules screen rather than from a dedicated settings page.

## Where to find it

| Surface | Location |
|---------|----------|
| Storefront slot | Theme-controlled — usually footer, sometimes header or contact page |
| Admin edit card | Sidebar → **Design** → **Modules** → **Others** tab → **Social links** card |
| Global URL fallbacks | [[settings-general]] (e.g., `facebook_link`, `instagram_link`, etc.) |

The underlying module mapping is `extra.social`; the instance name is usually `social`.

## What the merchant can do here

- **Master enable / disable** the whole module — when off, the row hides on the storefront.
- **Fill the URL** for each network — autofocused on Facebook by default.
- **Toggle visibility per network** — only networks with `show = on` render an icon on the storefront.
- **Leave a URL blank** — the module falls back to the corresponding global setting from [[settings-general]] (e.g., `facebook_link`).

What the merchant CANNOT do:

- **Add a custom network** (e.g., WhatsApp, Telegram, Discord) — the network list is hard-coded in the module restrictions. For unsupported networks, use [[design-module-navigation-links]] with an `external` link.
- **Reorder the icons** — render order is fixed by the theme's iteration of the module data (matches the order Facebook → X → Instagram → Pinterest → YouTube → LinkedIn → TikTok).
- **Customize the icon style** (filled vs outline, circular vs square) — controlled by the theme's CSS.

## Settings & fields

The module has 14 settings (7 networks × 2 fields each) plus the master enable. Each pair (`<network>_link` + `<network>_show`) belongs to one icon.

### Top-level

| Setting key | Type | Default | Allowed values | Limits | Validation | Notes |
|---|---|---|---|---|---|---|
| `enabled` | bool (switch) | `true` | `yes` / off | — | `bool` | Master on/off for the whole row |

### Per-network settings

| Setting key | Type | Default | Allowed values | Validation | Default `show` |
|---|---|---|---|---|---|
| `facebook_link` | URL | `http://www.facebook.com` | Valid URL | `url` rule | — |
| `facebook_show` | bool (switch) | `true` | `yes` / off | `bool` | ON |
| `x_link` | URL | `https://x.com/` | Valid URL | `url` rule | — |
| `x_show` | bool (switch) | `true` | `yes` / off | `bool` | ON |
| `instagram_link` | URL | `https://www.instagram.com` | Valid URL | `url` rule | — |
| `instagram_show` | bool (switch) | `true` | `yes` / off | `bool` | ON |
| `pinterest_link` | URL | `http://www.pinterest.com` | Valid URL | `url` rule | — |
| `pinterest_show` | bool (switch) | `false` | `yes` / off | `bool` | OFF |
| `youtube_link` | URL | `https://www.youtube.com` | Valid URL | `url` rule | — |
| `youtube_show` | bool (switch) | `false` | `yes` / off | `bool` | OFF |
| `linkedin_link` | URL | `https://www.linkedin.com` | Valid URL | `url` rule | — |
| `linkedin_show` | bool (switch) | `false` | `yes` / off | `bool` | OFF |
| `tiktok_link` | URL | `https://www.tiktok.com` | Valid URL | `url` rule | — |
| `tiktok_show` | bool (switch) | `false` | `yes` / off | `bool` | OFF |

### URL field length limit

Each `<network>_link` text input is capped at 255 characters in the merchant form (`maxlength="255"`). The validation `url` rule rejects malformed URLs.

### Per-network FontAwesome icon class rendered

| Network | Icon class |
|---------|------------|
| Facebook | `fab fa-facebook` |
| X (formerly Twitter) | `fab fa-x-twitter` (rendered explicitly — overridden because `x` would not map to a stock FontAwesome class) |
| Instagram | `fab fa-instagram` |
| Pinterest | `fab fa-pinterest` |
| YouTube | `fab fa-youtube` |
| LinkedIn | `fab fa-linkedin` |
| TikTok | `fab fa-tiktok` |

### Theme-specific notes

- **Visual style.** Themes render the icons with their own CSS — filled circles (Echappe), outlined squares (Themex), flat rows (Flair). The merchant CANNOT change the icon visual style without theme customisation.
- **Placement.** Most themes render `social` in the footer; some (e.g., contact-page-focused themes) also expose it on the contact page. Verify per theme.
- **`google_plus` field commented out.** Google+ used to be in the network list (`google_link` / `google_show`) but the code has commented them out post-shutdown of Google+. They no longer appear in the form or save schema.

## Business rules

### URL + show toggle BOTH required for an icon to render

For each network, the icon only appears on the storefront when BOTH:

1. The `<network>_link` field has a value (or the global fallback in [[settings-general]] has a value), AND
2. The `<network>_show` toggle is ON.

Filling the URL but leaving `show` off means the icon stays hidden. Toggling `show` on but leaving URL blank means the module consults the global fallback URL.

### Global URL fallback when module URL is blank

If the merchant leaves `<network>_link` blank but `<network>_show` is ON, the module reads the global setting `setting('<network>_link', '')` instead. This lets merchants set the URL once in [[settings-general]] and have it apply across the store. The clean practice is to fill the URL directly in the module; the fallback exists for migration from older versions where social URLs lived only in general settings.

### Whole row hides when all networks are off

The module exposes `doNotShowSocials` — when EVERY network's `show` is off, themes can call this method and skip rendering the wrapper element entirely. Otherwise, the row renders with whichever icons are enabled.

### X migration carryover

Stores migrated from the pre-rebrand era (when the network was Twitter) had a `twitter_link` / `twitter_show` field. The current module uses `x_link` / `x_show`. Migration scripts should copy old `twitter_*` values into `x_*` if a merchant still uses the legacy field; otherwise the X icon falls back to its hard-coded default URL.

### Cache invalidation

Save / Reset regenerate the storefront cache key — the new icon row applies on the next request.

### Reset behaviour

**Reset module** restores the 14 settings + master enable to the defaults shown above (Facebook / X / Instagram ON; Pinterest / YouTube / LinkedIn / TikTok OFF; canonical default URLs). The global-settings fallbacks ([[settings-general]]) are NOT touched.

### No plan-gating

`extra.social` is not in the `paid_widgets` allowlist — available on every plan.

## Related

- [[design-modules-navigation]] — hub.
- [[settings-general]] — global social URL fallbacks (`facebook_link`, `instagram_link`, `x_link`, etc.).
- [[design-module-navigation-links]] — alternative for unsupported networks (WhatsApp, Telegram, Discord) via an `external` link with `https://wa.me/...` / `tg://...` URLs.
- [[design-modules]] — parent module catalogue.

## Open questions

- 📡 **Social URL fallbacks.** The module reads `setting('<network>_link', '')` when its own URL is blank. GraphQL-resolvable: query [[settings-general]] for the configured global social URLs.
- 📡 **Per-language social URLs.** With `multylang` installed, social URLs may differ per language (e.g., a regional Facebook page per market). Verify whether the module JSON honours per-language keys or whether the URLs are language-agnostic.
- ⏸️ **Adding a network.** Currently requires a platform code change (extend the restrictions array + add the FontAwesome icon mapping in the template). No merchant-facing UI for custom networks.
