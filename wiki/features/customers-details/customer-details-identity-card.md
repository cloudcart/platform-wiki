---
type: feature
nav_path: "Customers → Customer details → Identity card"
route_name: customers-details.new
route_path: /admin/customers-new/details/:id
aliases: ["Customer identity card", "Customer insights module", "Customer note", "Customer tags picker"]
tags: [customers, profile, detail, tags, insights]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[customers-details]]. See the hub for the other aspects (tab strip, ban flow, email verification, default address, delete).

# Customer details — Identity card, insights, note, tags

## Purpose

The **left-column stack** on the customer detail page: four cards that surface who the customer is, what they're worth to the store, what staff has noted privately, and what segmentation tags they belong to. The merchant's *"at a glance"* customer panel — read first when a customer phones in, before drilling into orders or addresses.

Cards (top-to-bottom): the **Insights** KPI module, the **Identity** card, the **Note** card (conditional), the **Tags** picker.

## Where to find it

[[customers]] → click any row → opens `/admin/customers-new/details/:id`. All four cards are in the **left column** of the two-column layout. The right column holds the [[customer-details-default-address|default address]] and conditional [[customer-details-ban-flow|ban-reason]] cards.

## What the merchant can do here

### Insights module (top of left column)

A purple-highlighted card with a graph icon and the **"Insights"** label badge in a purple `#efe5ff` chip. Two KPI panels side-by-side (stack vertically on mobile):

| Panel | Big number | Sub-label |
|-------|------------|-----------|
| **Completed orders** | `orders_completed_price_formatted` (lifetime completed revenue) | *"{count} completed orders"* |
| **Total orders** | `orders_total_price_formatted` (lifetime total revenue) | *"{count} total orders"* — all statuses |

Both numbers come from the customer's denormalized `income` block — eventually consistent (typically within seconds). See "Business rules" below.

### Identity card

The customer's "who" card. The headline is the customer's name; the pencil icon at the top-right opens an action dropdown.

- **Customer name** (heading) + edit pencil → dropdown with **Edit customer** / **Change password** / **Confirm email address** / **Send confirmation email** (the last two only when email is unverified — see [[customer-details-email-verification]]).
- **Email** with verification status indicator (red *"Email address not verified"* + red X when `email_confirmed = no`; standard text when verified).
- **Registered on `<date>`**, **Customer phone** (when set), **Customer group** badge, and **Custom fields** (the per-store custom fields defined on [[customer]]).

### Identity-card dropdown options

| Option | What it does |
|--------|--------------|
| **Edit customer** | Opens the full Customer Create/Edit modal pre-filled. |
| **Change password** | Opens a password change modal. **Current-build note**: in the modern UI, the change-password component itself is NOT yet wired to render `(verify)`. The legacy customer-details page DOES render the modal — see [[customers-change-password]]. |
| **Confirm email address** | Only when `email_confirmed = no` — see [[customer-details-email-verification]]. |
| **Send confirmation email** | Only when `email_confirmed = no` — see [[customer-details-email-verification]]. |

### Customer note card

- Renders **ONLY** when the customer has a note set — empty notes don't render the card at all.
- Title row: notebook icon + label *"Notes"* (left) + pencil edit button (right).
- Note rendered HTML-aware — line breaks and inline tags pass through; server-validated to 191 chars max.
- Click pencil → opens the Edit Customer modal in **note-only + focus-note mode** (`focusNote: true, noteOnly: true`). The identity-form section is HIDDEN — the merchant sees only the note textarea + Custom fields card. The textarea auto-focuses on open.
- Note is NEVER shown to the customer — admin-only.

### Customer tags picker

A dedicated card below the note card.

- Tag-shape icon + label *"Tags"* (header row) + helper text *"Use tags to define customer groups and segments. Create marketing campaigns to specific groups"*.
- **Multi-tag search-select** with `mode="tags"` — typeahead against `GET /admin/api/core/customers/tags`. Each chip is a current tag.
- **Create on the fly**: typing a non-existing tag shows an *"Add '{name}' as a tag for this customer"* footer link in the dropdown. Case-insensitive dedup — an already-existing tag triggers an *"exists"* message instead.
- **Save tags** button — disabled until the local list differs from the initial set. Clicking POSTs to `/admin/api/core/customers/add-tags` with `{ids: [customer_id], tags: [...]}`. The endpoint **REPLACES** the customer's full tag set (not additive). Toast: *"Tags saved successfully"*. After save, the initial snapshot resets and the customer record re-fetches.

The picker feeds the [[customers]] list filter and the segments built on [[marketing-segments]] — applying or removing a tag here changes campaign eligibility immediately.

## Settings & fields

Editable fields on this page all live in the Edit Customer modal — see [[customers]] for the full list. Identity-card-surfaced fields:

| Field | Editable from | Note |
|-------|---------------|------|
| `first_name`, `last_name` | Modal → identity section | Required, max 191 chars. |
| `email` | Modal → identity section | Pending-confirmation flow — see [[customer-details-email-verification]]. |
| `phone_number` | Modal → identity section | Validated as international (libphonenumber). |
| `customer_group_id` | Modal → identity section | Surfaced as badge. |
| Note | Modal in note-only mode | Hard-capped 191 chars server-side. |
| Custom fields | Modal → custom fields card | Per-store definitions on [[customers-custom-fields]]. |
| Tags | Tags card (inline) | REPLACES the full set on save. |

## Business rules

### Insights numbers are eventually consistent

The Customer record stores `income`, `completed_orders`, `orders_total`, `orders_total_price`, `last_order_date` directly on the row (denormalized). A queued job recalculates these whenever an order is created, paid, refunded, cancelled, or fulfilled. So the Insights KPIs can briefly lag the actual order state — they converge once the job runs (typically within seconds). The modern Vue page caches the customer record (TanStack Query), so sub-tab navigation doesn't re-fetch; a hard refresh is needed to see the freshest numbers.

### Customer note has a 191-character hard cap

The customer note (admin-only field) is limited to **191 characters maximum**. A note longer than 191 chars throws the `customer.err.note_max_chars_%1$s` translation error. (191 is the platform's standard index-friendly column limit.) For longer records, the merchant should use customer tags + a separate notes system, or keep the note terse. Notes are NEVER shown to the customer — admin-only.

### Tag saves REPLACE the full set and propagate to Subscriber

The save endpoint replaces the customer's full tag set with what's posted — it is NOT additive. The frontend handles this automatically (it sends the local picker state), but JSON-API callers should be aware. Tag changes also propagate to the matching Subscriber record (joined by `customer_id`), so tags applied here AUTOMATICALLY become criteria in [[marketing-segments]] and campaign-targeting flows.

### Identity-card "Edit pencil" opens the modal

The pencil icon at the top-right of the identity card is the entry point to all customer-editing operations. There is no inline editing of name / email — the merchant always goes through the modal.

## Related

- [[customers-details]] — hub.
- [[customers]] — list page; the picker feeds the list-filter and the Customer Create/Edit modal opens from both surfaces.
- [[customer]] — entity page; carries all the fields surfaced here.
- [[customer-group]] — customer-group definitions used in the identity-card badge.
- [[customers-custom-fields]] — per-store custom fields rendered at the bottom of the identity card.
- [[customers-change-password]] — change-password modal (rendered by the legacy page; modern UI has it as TODO).
- [[customer-details-email-verification]] — Confirm-email / Send-confirmation dropdown items.
- [[marketing-segments]] — segments built from the tags applied here.

## Open questions

- Confirm whether the modern UI's *"Change password"* modal has been wired up since the TODO was noted `(verify)`.
