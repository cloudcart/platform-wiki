---
type: feature
nav_path: "Settings → Block Client IP addresses → List & modal"
route_name: banned-ip.settings
route_path: /admin/settings/banned-ip
aliases: ["Banned IP list", "Block IP modal", "Banned IP table", "Add blocked IP", "Delete blocked IP"]
tags: [settings, security, ban, ip, ui]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[settings-banned-ip]]. See the hub for the other aspects (enforcement, IP formats, scope & limits).

# Block Client IP addresses — list & modal

## Purpose

This aspect documents the admin UI of the **Block Client IP addresses** screen: the blocked-IP table, the create / edit modal, and the two distinct delete paths (single-row remove vs bulk-delete). It is what the merchant actually sees and clicks. For what blocking *does* to an order, see [[settings-banned-ip-enforcement]].

## Where to find it

Sidebar → Settings → **Block Client IP addresses**. Route `/admin/settings/banned-ip`.

## What the merchant can do here

- See a table of all blocked IPs with their IP address and description.
- Click **+ Block new IP** in the page header to open the create modal.
- Click any row (the IP-address column) to open the edit modal pre-populated.
- Remove a single entry via the per-row trash icon.
- Bulk-select multiple rows and bulk-delete them.
- Filter, search, paginate (default sort: `id` desc — newest IPs on top).

### What the merchant CANNOT do here

- Block ranges / CIDR blocks (single IP per row — see [[settings-banned-ip-ip-formats]]).
- Set an expiry / auto-unblock date (entries persist until manually deleted).
- Import a list of IPs from CSV / file (see [[settings-banned-ip-scope-limits]]).
- See orders attempted by a banned IP (no analytics on this page).

## Settings & fields

### List table

| Column | Notes |
|--------|-------|
| **IP address** (`ip`) | The blocked address. Clicking opens the edit modal. |
| **Description** (`description`) | Merchant's note (free text, up to 191 chars). |
| **Date added** (`created_at`) | When the IP was added to the blocklist. Displayed as a date. |
| **(actions)** | Per-row remove button. |

The list is sorted by `id` descending by default (newest IPs at top). Only the IP column is a clickable edit link — the `created_at` date and Description columns are NOT clickable.

### Create / Edit modal

| Field | Type | Notes |
|-------|------|-------|
| **IP address** (`item.ip`) | string | Required (Zod min 1 — *"IP address is required"*). Labelled "IP address", placeholder "IP address". Disabled during save. |
| **Description** (`item.description`) | string | Optional. Labelled "Description", placeholder "Reason for blocking". Max 191 chars (*"Description may not be greater than 191 characters"*). Disabled during save. |

Full UI shape (verified):

- **Size**: `lg`. **Title**: "Create new" (create mode) / "Edit" (edit mode).
- **Body card**: a two-line heading block — primary line *"Block client IP address"* (bold), sub-line short descriptive text — followed by the two inputs above.
- **Save action**: routes to either `create` or `edit` based on whether an existing row is being edited (`item.id` present).
- **Backdrop close**: enabled (no `no-close-on-backdrop`). Esc and outside-click dismiss without saving.
- **Reset on close**: create mode resets `item` to `{ ip: "", description: "" }` and clears the error store; edit mode populates `item` with a deep clone of the selected row.
- **Errors**: shown inline below each input via the error store (`getError('ip')`, `getError('description')`). Translation hints registered upfront: *"IP address is required"*, *"Invalid IP address"*, *"IP address already exists"*, *"Description may not be greater than 191 characters"*, *"Reason for blocking"*, *"Saved successfully"*.
- **On success**: toast *"Saved successfully"*; the row is added to / updated in the local table data optimistically.

## Business rules

### Row click opens the edit modal

Clicking anywhere on the IP-address column sets the active row data then opens the edit modal pre-populated. Other columns are not clickable.

### Per-row remove fires immediately (no confirmation)

The per-row trash icon (`column type=remove`) fires `DELETE /admin/api/core/settings/banned-ips/<id>` **immediately on click** — there is NO front-of-action confirmation popover for the single-row remove path. The merchant gets toast *"Deleted successfully"* on success. This path uses the numeric `id`.

### Bulk-delete is opt-in and DOES confirm

The merchant must select rows with checkboxes, then click the **Delete** bulk action explicitly. Bulk-delete uses `type: 'post'` with a `confirm` block — confirmation modal *"Are you are sure you want to delete? Caution: This action cannot be undone."* — POSTing to `/admin/api/core/settings/banned-ips/bulk-delete` with body `{ ips: [<selected IP strings>] }`.

> **Note:** the bulk endpoint takes literal **IP strings**, NOT IDs — different from the single-row remove path (which uses the numeric `id`) and different from many other bulk endpoints in the platform that use IDs.

### CRUD is synchronous

Adding an IP takes effect immediately on the next checkout attempt — no propagation delay, no queue, no notifications fired. The enforcement timing is detailed on [[settings-banned-ip-enforcement]].

## Related

- [[settings-banned-ip]] — hub.
- [[settings]] — parent settings hub.

## Open questions

None.
