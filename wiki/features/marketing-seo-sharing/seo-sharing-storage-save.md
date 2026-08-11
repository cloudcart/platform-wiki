---
type: feature
nav_path: "Marketing → SEO → Sharing → Storage & save mechanics"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Sharing save mechanics", "add-this endpoint", "AddThis save endpoint", "og_image_url storage", "Sharing module storage", "enabled 0 strip quirk", "Sharing validation map", "Споделяне запис", "Споделяне валидация"]
tags: [marketing, seo, sharing, distribution]
plan_gates: []
created: 2026-05-26
updated: 2026-06-10
source_count: 4
---
> Part of [[marketing-seo-sharing]]. See the hub for the other aspects (the default Open Graph image, the sharing toolbar).

# Sharing card — storage & save mechanics

## Purpose

This aspect documents **how the Sharing card persists** — the two separate storage targets, the legacy save endpoint, the validation map, and two quirks that produce support tickets: the `enabled = 0` strip and the unsanitised Custom toolbar. This is the page to read when a Sharing save behaves unexpectedly, succeeds for some fields but not others, or resets after a theme change.

## Where to find it

There is no separate UI for this — it is the save behaviour behind the **"Share product"** card on Sidebar → Marketing → **SEO** (`/admin/marketing-new/seo`). The card uses the shared inline **Save / Revert** wrapper; Save toast is "Saved Successfully".

## What the merchant can do here

- Save the card (writes toolbar config + `og_image_url` in one POST).
- Revert unsaved edits with the inline Revert button.

The split storage, endpoint, and quirks below are behaviours the merchant indirectly triggers, not separate controls.

## Settings & fields

The save writes to **two different stores**:

| Where it is stored | Fields | Survives theme change? |
|--------------------|--------|------------------------|
| **Theme-scoped module settings row** (keyed by module mapping `extra.addThisShare`) | `enabled`, `layout`, `show_counter`, `show_compact`, `show_top_services`, `ui_click`, `ui_hover_direction`, `custom_toolbar` — plus non-UI defaults `services`, `ui_cobrand`, `ui_header_color`, `ui_header_background`, `ui_language` | **No** — theme-scoped, so switching theme can reset the toolbar config. |
| **Global store settings table** | `og_image_url` | **Yes** — global, survives theme changes. |

### Non-UI defaults carried in the module row

The module's `_default_settings` also stores values the Vue UI does **not** expose:

- `services` = `["facebook", "twitter", "google_plusone_share", "pinterest_share"]` (the hard-coded network list).
- `ui_cobrand` = `"MyBrand"`.
- `ui_header_color` = `#fff`, `ui_header_background` = `#bc9f75` — regex-validated as colour strings; settable via a direct POST even though the UI hides them.
- `ui_language` = `en`.

## Business rules

### Two stores, one save call

On save, the module toggles go to the theme-scoped module settings row; `og_image_url` is the only write to the global settings table. The practical consequence: switching theme can reset the toolbar config but the default `og:image` always survives — see [[seo-sharing-og-image]].

### The Sharing card uses a LEGACY endpoint

The merchant-saves POST goes to `/admin/marketing/seo/add-this` (the legacy sitecp router), NOT the modern `/admin/api/core/seo/settings/*` path that the other six SEO cards use. The Core admin API does not expose a sharing endpoint at all — the Vue page reaches into the legacy route directly. This is why a Sharing save can fail while the other cards on the same screen succeed.

### `enabled = 0` is treated specially on save

When the merchant turns the master "Share product" switch OFF and clicks Save, the Vue page **deletes** `enabled` from the outgoing payload. The server only updates fields present in the payload, so the previous `enabled` value sticks. **Net effect: toggling OFF + Save does NOT persist the OFF state.** A known Vue-side quirk. To suppress the toolbar, merchants rely on the per-theme hard-disable instead — see [[seo-sharing-toolbar]].

### Validation is built from the module's restrictions map

The module's `_restrictions` array is flattened and turned into validation rules. There are no explicit per-field validate calls in the handler; failures are repackaged into field-keyed JSON errors. Rules enforced:

- `enabled` — bool.
- `layout` — `in:small|large|custom`.
- `show_counter` / `show_compact` / `show_top_services` / `ui_click` — `yes|no`.
- `ui_hover_direction` — `in:-1|1`.
- `custom_toolbar` — 1–750 characters.
- `ui_header_color` / `ui_header_background` — regex-validated colour strings (defaults `#fff` / `#bc9f75`).

### Custom toolbar HTML is NOT sanitized on save

Validation runs against the restrictions map, but the module's `sanitize` step is not invoked from the SEO save path. The 750-character limit is the **only** guardrail, so any markup or `<script>` the merchant pastes reaches the storefront verbatim — an XSS risk on themes that still render the toolbar. See [[seo-sharing-toolbar]] for what the field accepts.

### Default settings map (full)

`enabled = true`, `layout = "large"`, `show_counter = "yes"`, `show_compact = "yes"`, `show_top_services = "yes"`, `ui_click = "yes"`, `ui_hover_direction = -1` (down), `custom_toolbar = ""`, `services = ["facebook", "twitter", "google_plusone_share", "pinterest_share"]`, `ui_cobrand = "MyBrand"`, `ui_header_color = "#fff"`, `ui_header_background = "#bc9f75"`, `ui_language = "en"`.

### Permission

The endpoint sits behind `hasApiPermission:marketing.seo`.

## Related

- [[marketing-seo-sharing]] — hub.
- [[seo-sharing-og-image]] — `og_image_url`, the only global-settings write (survives theme change).
- [[seo-sharing-toolbar]] — the toggles persisted in the theme-scoped row + the `enabled = 0` and unsanitised-HTML consequences.
- [[marketing-seo]] — parent SEO screen.

## Open questions

No outstanding questions.
