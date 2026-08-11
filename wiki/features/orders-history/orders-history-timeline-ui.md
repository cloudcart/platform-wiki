---
type: feature
nav_path: "Orders → Order details → History → Timeline"
route_name: admin.orders.history
route_path: /admin/orders/action/history/:order_id
aliases: ["Order history timeline", "History entry layout", "History accordion", "Order timeline UI", "История — изглед"]
tags: [orders, history, audit, ui, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-history]]. See the hub for the other aspects (action codes, record model, synthetic entries, enrichment, acting party, API & triggers).

# Order history — the timeline UI

## Purpose

The on-screen layout of the per-order audit log: how entries are grouped, what each row shows, when a row is expandable, and what the merchant can / cannot do with the timeline. This is the surface the merchant actually scrolls when investigating an order.

## Where to find it

From [[orders-details]] → embedded History panel (lazy-loaded inline via `data-box-ajax`). The merchant does not normally open the route directly.

## What the merchant can do here

### Read the chronological log

Each day-group renders as a box with a date header (format *"Jan 15 2026"*, `%b %e %Y`). Within each box, individual entries stack as feed items, each built from a fixed layout:

| Slot | Content | Notes |
|---|---|---|
| Left icon | `action_icon` (Font Awesome class) | Set per action type at the platform level (e.g., `fal fa-plus-circle` for adds). |
| Description | `message` (translated) | Short text — *"Order created"*, *"Payment marked as paid"*, *"Address edited"*, etc. Payment codes 21 + 22 append the affected product name in quotes (see [[orders-history-action-codes]]). |
| "Placed by" | Admin link, namespace string, or *"No such admin"* | See [[orders-history-acting-party]] for the full identification chain. |
| Right | Formatted `date` per the merchant's `time_format` | When `action_string` is set, also shows a chevron (`fa-angle-down` / `fa-angle-up`). |
| Below (collapsible) | Per-action sub-template body | Loaded inline; toggled via Bootstrap's `data-toggle="collapse"`. |

### Expand for detail

Only entries with a non-empty `action_string` are clickable. Clicking rotates the chevron and slides open a per-action sub-panel (one of ~24 pre-built sub-templates). A single jQuery click handler on `.history-entry` swaps the chevron class on each click; Bootstrap's collapse plugin handles the slide. Entries with no `action_string` render as flat rows with no chevron. The catalogue of sub-templates is documented in [[orders-history-action-codes]].

### What the merchant CANNOT do here

- **Edit** historical entries — the log is immutable (see [[orders-history-record-model]]).
- **Delete** entries — same.
- **Filter** the log — there is no per-action filter UI; the merchant scrolls through the days.
- **Export** the log as a separate file — they'd print the order page or screenshot it.

## Settings & fields

No editable settings on this surface. Two display behaviours are driven by store / order state:

- **Day-group header** uses `%b %e %Y`; per-entry time uses the store's `time_format`.
- **Outer container** is `my-collapsible`; the inner accordion uses the Bootstrap collapse plugin. No Vue components — this is a Smarty + jQuery surface.

## Business rules

### Hidden for draft orders

The whole accordion is conditionally rendered: when `is_draft = 1`, **NO** history is shown. A merchant building a manual order doesn't see a noise-laden timeline of their in-progress edits.

### Abandoned-cart recovery banner

When the order was recovered through an abandoned-cart flow (`order.abandoned` is truthy AND a `restore_source` value exists), the timeline injects a `<div class="note warning separator">` at the very **top**, above all day groups: *"Order was recovered through `<source>`"*. The `<source>` is typically `email` but may be `sms`, `push`, or another channel depending on the recovery campaign. This is the merchant's quick signal that the order resulted from a marketing recovery effort — useful for attribution. The campaigns that drive it live on [[marketing-campaigns]]; the trigger plumbing is in [[orders-history-api-and-triggers]].

### Permission

Standard orders permission scope, read-only. The merchant can see the full audit even for actions they did not perform.

### Side effects

None — the page is a pure read.

## Related

- [[orders-history]] — hub.
- [[orders-details]] — parent page that hosts this panel.
- [[orders-history-action-codes]] — the action-code map + expandable sub-templates.
- [[orders-history-acting-party]] — how the "Placed by" slot is resolved.
- [[orders-history-record-model]] — why the log is immutable / append-only.
- [[marketing-campaigns]] — abandoned-cart recovery campaigns behind the banner.

## Open questions

None.
