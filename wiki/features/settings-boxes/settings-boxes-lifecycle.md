---
type: feature
nav_path: "Settings → Delivery boxes (lifecycle, delete, permissions)"
route_name: boxes.settings
route_path: /admin/settings/boxes
aliases: ["Box lifecycle", "Delete box", "Box delete safety", "Box permission", "No bulk import boxes", "Box side effects", "Изтриване на кашон", "Достъп до кашони"]
tags: [settings, boxes, shipping, packaging, lifecycle, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[settings-boxes]]. See the hub for related aspects (the box fields / modal, and the box-packing algorithm).

# Delivery boxes — lifecycle, delete safety & permissions

## Purpose

This aspect covers the operational lifecycle of a box record outside of data entry: what deleting a box does (and doesn't) affect, why retiring old box sizes is safe, the absence of a bulk-import path, the lack of any count cap, the moderator permission that gates the screen, and the cache / side-effect profile of saving a box. A support agent cites this when a merchant asks "is it safe to delete this box?", "can I import all my boxes at once?", or "why can't my staff member see Delivery boxes?".

## Where to find it

Sidebar → Settings → **Delivery boxes**. Moderator access is granted from [[settings-staff]].

## What the merchant can do here

- Retire (delete) box sizes that are no longer used.
- Define as many boxes as needed (no cap).
- Grant a staff member access to the screen via the Settings or Delivery boxes permission.

The merchant **cannot** bulk-import boxes — there is no CSV import, clipboard-paste, or bulk-create path.

## Settings & fields

This aspect has no fields of its own — the box record's fields are documented on [[settings-boxes-fields]]. The controls relevant here are the per-row delete (trash) action and the moderator permission grant on [[settings-staff]].

## Business rules

### Delete safety — orders snapshot the chosen box at dispatch

Deleting a box is a defensive operation. The shipping cost computed at the moment of order placement is already stored on the [[order]] row (the box is referenced by id and dimensions at calculation time). Deleting the box record afterwards does **not** affect that historical cost. New orders calculated after deletion simply skip the deleted box in the packing algorithm.

So merchants can safely retire old box sizes; just verify the active shipping methods still have at least one usable box. If a merchant reports "I deleted a box and got an error", escalate for a deeper backend check — but the schema treats boxes as reference data, not transactional. `(verify)` on deeper backend ingest.

### No bulk-import / CSV

The merchant must create each box one at a time through the modal. There is no CSV import path, no clipboard-paste shortcut, and no API endpoint to bulk-create. For migrations from another platform, the merchant either re-enters each box manually or contacts CloudCart support to seed the boxes directly.

### No maximum count

The platform has no soft or hard cap on the number of boxes a merchant can define. Performance is unaffected at typical scales (a few dozen distinct sizes) because the packing algorithm (see [[settings-boxes-packing]]) runs only at quote-time and the box list is loaded into memory once. Stores with very large catalogues (50+ box sizes) work but with marginally higher quote latency.

### Permission

The Boxes route group is gated by the `settings.boxes` permission. A moderator needs either the broad **Settings** permission OR the specific **Delivery boxes** (`settings.boxes`) permission grant from [[settings-staff]] to list, create, edit, or delete delivery boxes. Owners always pass.

### Cache + side effects

CRUD on a box is synchronous, database-write only. No queue, no notifications, and no webhooks fire on box create / edit / delete.

## Related

- [[settings-boxes]] — hub.
- [[settings-staff]] — moderator permission (`settings.boxes`) that gates the screen.
- [[order]] — orders snapshot the chosen box for archival, so deletion is non-destructive to history.
- [[settings-boxes]] — entity page.

## Open questions

- Confirm on deeper backend ingest whether deleting a box referenced by an in-flight (not-yet-dispatched) order can surface any error. `(verify)`
