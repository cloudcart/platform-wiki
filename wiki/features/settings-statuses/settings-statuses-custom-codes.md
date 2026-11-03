---
type: feature
nav_path: "Settings → Statuses → (custom status codes)"
route_name: order-statuses
route_path: /admin/settings/statuses/order
aliases: ["Custom status slug", "Custom status code generation", "Slug collision suffix", "Recreated custom status code", "Status name vs code"]
tags: [settings, statuses, orders, integrations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-statuses]]. See the hub for the three taxonomies and the other cross-cutting mechanics (rename, delete protection, permissions).

# Statuses — custom status codes

## Purpose

When the merchant creates a new custom order status with name *"Available in 3 days"* from [[settings-statuses-orders-tab]], the platform doesn't just store the human label — it also derives an internal **status code** (a slug) from the name. That code is what webhooks, exports, JSON-API v2, [[settings-hooks]] subscribers, and downstream integrations see; the label is purely cosmetic.

This page documents the slug-generation rule, the suffix-collision behaviour when the merchant deletes and re-creates a status with the same name, and the practical integration consequences. Misunderstanding this layer is the single most common source of "my webhook stopped firing for that status" support tickets.

## Where to find it

The code is **generated automatically** when the merchant clicks Save on the Add-status modal on [[settings-statuses-orders-tab]]. The merchant never sees or chooses the code in the admin UI — only the name. The code is visible only through:

- JSON-API v2 reads of order resources (`status` field shows the code, not the rename).
- Webhook payloads on `order.updated` events from [[settings-hooks]].
- The platform's `order-status` table on the database (for support diagnosis).
- CSV / XML exports.

## What the merchant can do here

The slug behaviour is automatic; the merchant has no direct control. The merchant CAN choose a name carefully on creation (the code derives from the name, so "Available in 3 days" produces `order-available-in-3-days`), rename freely after creation (does NOT change the code — safe for integrations), and should be aware that deleting + re-creating with the same name creates a NEW code with a numeric suffix (breaks integrations that filtered on the old code).

What the merchant CANNOT do: set the code directly (auto-generated), re-use a code from a deleted custom status (uniqueness check appends a suffix), or change the code of an existing custom status (only the name).

## Settings & fields

There are no merchant-editable fields for the code itself. The relevant fields on the underlying status record are:

| Field | Value | Editable by merchant? |
|-------|-------|------------------------|
| `name` | The human label (from the Add-status modal or inline rename input). | Yes (via [[settings-statuses-orders-tab]]). |
| `status` (the code) | The slug derived from the name on creation. | **No** — auto-generated, immutable post-creation. |
| `custom` | `true` for merchant-added, `false` for built-in. | n/a (set by backend at creation time). |
| `type` | `order` for any custom status (Create is only allowed for order taxonomy). | n/a (fixed by route — see [[settings-statuses-permissions-validation]]). |

## Business rules

### Slug generation rule

When the merchant POSTs to `/statuses/order/create` with `name = "Available in 3 days"`, the backend:

1. Slugifies `<type>-<name>` → `order-available-in-3-days`.
2. **Truncates to 240 characters** (database column constraint).
3. Checks if a status with that slug already exists for the same type.
4. If yes, appends `-1`, `-2`, `-3`, ... until a unique slug is found.
5. Stores the row with that final slug as the status code.

For "Available in 3 days" on a fresh store, the resulting code is `order-available-in-3-days`. A subsequent create with the same name would become `order-available-in-3-days-1`.

### Renaming a custom status does NOT change its underlying code

If the merchant creates "Available in 3 days" (code: `order-available-in-3-days`) and later renames it to "Coming next week" via the inline edit (see [[settings-statuses-orders-tab]]), the code stays `order-available-in-3-days`.

**Practical merchant consequence**: webhooks, exports, JSON-API v2 reads, and integrations that referenced the old code continue working. The merchant can rename freely without breaking anything external — the rename is purely cosmetic. This is the property that makes the rename mechanic safe (see [[settings-statuses-rename-mechanic]]).

### Creating a custom status with the same name as a deleted one creates a NEW code

This is the trap. If the merchant:

1. Creates "Available in 3 days" → code `order-available-in-3-days`.
2. Deletes that status (see [[settings-statuses-delete-protection]]).
3. Re-creates "Available in 3 days".

The new status's code is `order-available-in-3-days-1` (because the slug-uniqueness check counts all rows including soft-historical ones if they share the slug — the platform does not free the slug on delete).

**Practical merchant consequence**: any integration (webhook subscriber, export filter, ERP sync, JSON-API v2 client) that was matching on the old code will **NOT** match the re-created status. The merchant has effectively created a new entity that happens to share a name with the deleted one. To avoid this:

- Don't delete + re-create — just rename the existing status to the new label.
- If a delete + re-create is unavoidable, audit and update any downstream filters first.

### Two custom statuses can never share a CODE, but CAN share a NAME

The platform enforces uniqueness on the slug; the human name has no uniqueness constraint. So the merchant could rename "Coming next week" to "Pending" (the same name as the built-in `pending` status), and the platform would accept it — the admin would then display two distinct rows both labelled "Pending", and the merchant would have to rely on context to tell them apart. The codes differ (`pending` for the built-in vs `order-coming-next-week` for the custom) so integrations are unaffected, but the merchant-facing label confusion is a real risk. See [[settings-statuses-permissions-validation]] for the lack of a reserved-word check.

### Code is generated from name, not slug-of-name

The slug step is `<type>-<slugify(name)>`, so the `type` prefix is always included. This is why every custom order status code starts with `order-` regardless of the name. A status named "Cancelled" creates a code `order-cancelled` (distinct from the built-in `cancelled` code) — built-ins do NOT have the `order-` prefix on their codes. This double-namespacing isolates custom from built-in codes.

### What integrations should match on

For stable webhook subscribers, JSON-API v2 clients, and ERP syncs: **match on code, not name** (names change with a single click); treat custom codes as opaque strings; re-discover the code list if a status gets deleted + re-created (there's no way to detect this from the receiving side without re-listing the taxonomy). A receiver that hardcodes `order-available-in-3-days` is fragile to delete + recreate; one that pulls the current code list from JSON-API v2 and matches on the current code is robust.

## Related

- [[settings-statuses]] — hub.
- [[settings-statuses-orders-tab]] — where custom statuses are created and named.
- [[settings-statuses-rename-mechanic]] — renames don't change codes (the property that makes renaming safe).
- [[settings-statuses-delete-protection]] — delete blocked when orders are attached; the rule that often forces "rename instead of delete".
- [[settings-statuses-permissions-validation]] — server-side validation including the no-reserved-word and no-uniqueness-on-name rules.
- [[settings-hooks]] — webhook subscribers always see the code; the rename mechanic is transparent to them.
- [[order-status]] — entity page.
- [[api-orders]] — JSON-API v2 endpoint that exposes the code in order resources.

## Open questions

- The exact JSON-API v2 endpoint for listing the current status taxonomy (so receivers can resolve names → codes dynamically). *(verify)*
- Whether the slug-uniqueness check considers ONLY active rows or also soft-deleted historical rows — the source pass said "all rows including soft-historical" but the exact deletion model (hard vs soft delete) was not captured. *(verify)*
