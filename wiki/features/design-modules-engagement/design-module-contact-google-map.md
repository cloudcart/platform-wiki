---
type: feature
nav_path: "Design → Modules → Engagement → Google Map"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/googleMap
aliases: ["Google Map module", "googleMap module", "Map module", "Модул карта", "Google карта"]
tags: [design, modules, engagement, contact, google-map, maps]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Engagement module — googleMap

> Part of [[design-modules-engagement]]. See the category page for the other engagement modules.

## Purpose

`googleMap` embeds an interactive **Google Map** on the storefront's `/contacts` page (and any other slot the active theme drops it into) with one or more **pins** marking the store's physical location(s). The merchant configures the pin set, the default zoom, the map type (Roadmap / Satellite / Hybrid / Terrain), the loading background colour, and a long list of UI-control toggles (zoom controls, scroll-wheel zoom, Street View, pan, rotate, etc.).

It uses the platform-supplied Google Maps embed key by default — no merchant setup is required for the basic embed. Merchants who run multiple physical stores typically pair it with [[apps-store-locations]] for a richer multi-store overlay.

## Where to find it

Sidebar → **Design** → **Modules** → **Contacts** tab → card labelled *"Google Map"*.

Clicking the card opens the settings form: a live map preview to add / move pins, plus a settings panel for the map-level options.

## What the merchant can do here

- **Add a pin** by clicking on the embedded preview map OR by clicking **Add a pin** and typing an address (the platform geocodes it).
- **Edit a pin's caption** (rich text shown in the info-bubble popup) and address.
- **Drag a pin** to refine its position.
- **Delete a pin**.
- Set the **default zoom**, **map type**, **background colour**, and toggle ~14 Google Maps UI controls.
- Save / Reset / Cancel — Reset wipes ALL configured pins (no undo).

## Settings & fields

| Field | Type | Validation | Default | What it controls |
|-------|------|------------|---------|------------------|
| `pins` | JSON array | (free-form) | `[]` | The location markers — each pin has an `address`, geocoded `lat` / `lng`, and a `caption` (rich text shown in the info bubble) |
| `key` | text | (free-form) | `null` | Custom Google Maps API key (rarely needed — platform supplies a default) |
| `zoom` | Slider (0–18) | `int:0,18` | `11` | Default zoom level |
| `mapTypeId` | Select | `in:HYBRID,ROADMAP,SATELLITE,TERRAIN` | `ROADMAP` | Map type |
| `backgroundColor` | Color picker | `regex:color` | `#fff` | Background colour while tiles are loading |
| `disableDefaultUI` | Select (yes / no) | `in:yes,no` | `no` | Hide ALL default Google controls in one switch |
| `disableDoubleClickZoom` | Select (yes / no) | `in:yes,no` | `no` | Disable zoom on double-click |
| `draggable` | Select (yes / no) | `in:yes,no` | `yes` | Allow the shopper to pan the map |
| `keyboardShortcuts` | Select (yes / no) | `in:yes,no` | `yes` | Enable keyboard pan/zoom |
| `mapMaker` | Select (yes / no) | `in:yes,no` | `yes` | Enable Google Map Maker (legacy Google API) |
| `mapTypeControl` | Select (yes / no) | `in:yes,no` | `yes` | Show the map-type toggle (Map / Satellite buttons) |
| `noClear` | Select (yes / no) | `in:yes,no` | `no` | Preserve markers on re-init |
| `overviewMapControl` | Select (yes / no) | `in:yes,no` | `yes` | Show the mini overview map |
| `panControl` | Select (yes / no) | `in:yes,no` | `yes` | Show pan arrows |
| `rotateControl` | Select (yes / no) | `in:yes,no` | `yes` | Show rotation control |
| `scaleControl` | Select (yes / no) | `in:yes,no` | `yes` | Show the scale bar |
| `scrollwheel` | Select (yes / no) | `in:yes,no` | `no` | Allow zoom via mouse wheel |
| `streetViewControl` | Select (yes / no) | `in:yes,no` | `no` | Show the Street View Pegman |
| `zoomControl` | Select (yes / no) | `in:yes,no` | `yes` | Show +/- zoom buttons |
| `enabled` | toggle | `bool` | `true` | Master on/off — when off the module renders nothing |

**Pin caption allowed HTML tags:** `<img><b><a><p><br><s><em><hr><strong><small><code><kbd><samp><var><del><ins><cite><q><span><div><blockquote><ul><ol><li><font><pre><h1>` through `<h6>`. `<img>` IS allowed here (unlike `contactInformation`), so a small logo can be embedded in the info bubble.

## Theme dependencies

Universal — every theme with a `/contacts` page can render this module, and the platform treats it as a built-in system module, so it is available even in themes that don't list it. Some themes also drop the map into the footer or sidebar.

## Business rules

### Where the map centers

The map centers on the **average** of all pin coordinates. With one pin, the center is that pin. With **zero pins** at default zoom 11, the map shows a generic, blank-ish world view — so a brand-new instance (or one where the merchant deleted every pin and saved an empty list) renders a world map until a pin is added.

### Geocoding can fail

When the merchant types an address in **Add a pin**, the platform geocodes it to coordinates. A free-form address that fails to geocode returns an error and the pin is **not** added — re-type a more specific address.

### Reset wipes pins

Clicking **Reset module** restores defaults — `pins: []`, `zoom: 11`, all controls back to platform defaults. There is no undo and pins must be manually re-added. The confirmation prompt warns: *"Are you sure you want to reset this module?"*. Saving or resetting may take a short moment to appear on the storefront while the cache refreshes.

### Disabled state

Setting `enabled = false` (the master toggle) hides the entire module from the storefront — no map, no pins, no fallback. The contact form still renders if `contactInformation → show_form = yes`.

### Map type values are case-sensitive

The four `mapTypeId` values (`HYBRID`, `ROADMAP`, `SATELLITE`, `TERRAIN`) are case-sensitive; the select control sets them correctly.

### Scroll-wheel zoom is off by default

The default `scrollwheel: no` is intentional — mid-page, scroll-wheel zoom hijacks the shopper's scroll. Merchants who place the map at the bottom of the page can safely turn it back on.

### Multi-store overlay via apps-store-locations

When [[apps-store-locations]] is installed, it overlays its store data on top of the merchant's pins, so multi-store merchants don't re-enter pins per location. The pins configured here remain visible as a fallback.

### Custom API key

The `key` field accepts a custom Google Maps API key — useful when the merchant brings their own Google Cloud project for higher quotas or custom map styling. When empty (the default), the module uses the platform's shared embed key. The key is not validated, so a wrong key fails silently on the storefront (a "for development purposes only" watermark, or no map).

## Related

- [[design-modules-engagement]] — hub.
- [[design-module-contact-form]] — sibling; usually rendered next to the map on `/contacts`.
- [[design-module-contact-information]] — sibling; the prose block above the map.
- [[apps-store-locations]] — multi-store data overlay that complements this module's pin set.
- [[settings-general]] — store address default (used to seed the first pin when no pins are configured).
- [[design-themes]] — theme controls where the map renders (most themes use `/contacts`; some also use it in the footer).

## Open questions

- 📡 **Custom Google API key.** Platform supplies a default key; merchant key in `key` field is optional. GraphQL-resolvable: query whether the merchant has a custom key configured.
- 📡 **Multi-store overlay.** [[apps-store-locations]] overlays store data on top of the module's pin set. GraphQL-resolvable: query whether the store-locations app is installed.
- ⏸️ **`mapMaker` toggle.** Google Map Maker was deprecated in 2017. (verify) the toggle still appears in the modern form, but it has no effect on modern map renders.
- ⏸️ **Pin caption HTML allowlist.** `<img>` is allowed in pin captions but not in `contactInformation` — (verify) the reason for the divergence.
