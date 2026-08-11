---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms → Layout position"
route_name: ""
route_path: ""
aliases: ["Subscribe form layout position", "Form positioning", "layoutPosition enum", "Per-device form position", "Позиция на формата"]
tags: [marketing, subscribers, forms, layout, position, popup, storefront]
plan_gates: ["subscriber_forms"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-subscribers-subscribe-forms]]. See the hub for the other aspects (list view, builder, templates, triggers, fields, submission flow, GDPR consent, known issues).

# Subscribe forms — layout position

## Purpose

`layoutPosition` is the **per-device position object** on every subscribe form. It controls **where** on the viewport the form anchors when it shows — corner, edge, full-width bar, modal centre, etc. The merchant configures desktop and mobile independently (no tablet axis — tablet inherits desktop). The actual rendered position is read at storefront render time as `layoutPosition[deviceType]`.

The structural template chosen on form creation (see [[subscribe-forms-templates]]) seeds initial values, but the merchant can override either device's position freely.

## Where to find it

Inside the form builder iframe (see [[subscribe-forms-builder]]) — the position picker is a top-level setting alongside template / display triggers / styling. Stored on the form record as:

```
layoutPosition.desktop = <enum value>
layoutPosition.mobile = <enum value>
```

## What the merchant can do here

- Pick the desktop position from the 15-value enum.
- Pick the mobile position independently from the same enum.
- Combined with per-device `media` slots and per-device `style`, this is the **only** axis through which the merchant differentiates how the form looks on mobile vs desktop. There is no "hide on mobile" or "hide on desktop" toggle — see [[subscribe-forms-known-issues]].

## Settings & fields

### The 15-value `layoutPosition` enum (verbatim from the builder)

| Value | Visual placement |
|-------|------------------|
| `topLeft` | Anchored to the top-left of the viewport. |
| `topCenter` | Centered horizontally at the top. |
| `topRight` | Anchored to the top-right. |
| `topFull` | Full-width bar at the top. |
| `centerLeft` | Vertically centered on the left edge. |
| `centerCenter` | Centered in the viewport (modal-style). |
| `centerRight` | Vertically centered on the right edge. |
| `bottomLeft` | Anchored to the bottom-left. |
| `bottomCenter` | Centered horizontally at the bottom. |
| `bottomRight` | Anchored to the bottom-right. |
| `bottomFull` | Full-width bar at the bottom. |
| `left` | Sidebar pinned to the left edge (used by the `sidebar` template). |
| `right` | Sidebar pinned to the right edge (used by the `sidebar` template). |
| `full` | Full-screen takeover (used by the `fullscreen` and mobile-fallback layouts). |
| `mobile` | Mobile-optimised default sheet (mobile only). |

### Per-device — desktop vs mobile only

The merchant configures **desktop** and **mobile** separately. There is no tablet axis in the builder — tablet inherits the desktop position. (verify) The module JS at storefront render time picks `layoutPosition.desktop` or `layoutPosition.mobile` based on viewport width.

## Business rules

### Template-suggested defaults

Each structural template seeds the position fields differently — see [[subscribe-forms-templates]] for the per-template defaults. Once picked, the merchant can override either device's position; the template just provides a sensible starting point.

### Mobile-only values

Two of the 15 values are intended primarily for mobile:

- **`full`** — full-screen takeover. Used by `fullscreen` template on both devices and as the mobile fallback for `sidebar` (a tall side strip is impractical on narrow viewports).
- **`mobile`** — a mobile-optimised default sheet shape (the builder uses this label for the catch-all responsive mobile rendering).

### Some values are template-coupled

- **`left` / `right`** are intended for the `sidebar` template. Other templates ignore them or render them as `centerLeft` / `centerRight` (verify).
- **`topFull` / `bottomFull`** are intended for the `bar` template (slim full-width bar) but can also be applied to other templates if the merchant wants a banner shape.

### No "hide on this device" toggle

The builder lets the merchant style the form differently per device, but there is **NO toggle to hide the form on one device entirely** (see [[subscribe-forms-known-issues]]). To hide on mobile, the merchant has to manage URL targeting differently per device — not actually achievable without two separate forms with disjoint included-URL sets.

### Position is not size — width/height are a separate styling setting

`layoutPosition` only controls **where** the form is anchored, not **how big** it is. The form's **width and height** are free-form pixel values set under the form's styling (see [[subscribe-forms-builder]] → Styling → Dimensions), not here, and they are not clamped — the only per-device responsiveness this page offers is placement, not resizing. A merchant asking to "make the form wider / taller" is looking for the styling dimensions, not a layout position.

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[subscribe-forms-templates]] — the 5 structural templates that seed initial `layoutPosition` values.
- [[subscribe-forms-builder]] — where the position picker lives.
- [[subscribe-forms-known-issues]] — the missing per-device visibility toggle is documented as a known limitation.

## Open questions

- Whether tablet truly inherits desktop or has its own breakpoint logic in the module JS. (verify)
