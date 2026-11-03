---
type: feature
nav_path: "Customers → Customer details → Identity card"
route_name: customers-details
route_path: /admin/customers/details/:id
aliases: ["Customer identity card", "Customer insights module", "Customer note", "Customer tags picker", "Customer metafields card"]
tags: [customers, profile, detail, tags, insights, metafields]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-11-03
source_count: 6
---

> Part of [[customers-details]]. See the hub for the other aspects (tab strip, ban flow, email verification, default address, delete).

# Customer details — Identity card, insights, note, metafields, tags

## Purpose

The **left-column stack** on the customer detail page: five cards that surface who the customer is, what they're worth to the store, what staff has noted privately, the customer's metafields, and what segmentation tags they belong to. The merchant's *"at a glance"* customer panel — read first when a customer phones in, before drilling into orders or addresses.

Cards (top-to-bottom): the **Insights** KPI module, the **Identity** card, the **Note** card (conditional), the **Metafields** card, the **Tags** picker.

## Where to find it

[[customers]] → click any row → opens `/admin/customers/details/:id`. All five cards are in the **left column** of the two-column layout. The right column holds the [[customer-details-default-address|default address]] and conditional [[customer-details-ban-flow|ban-reason]] cards.

## What the merchant can do here

### Insights module (top of left column)

A card with a graph icon and the **"Insights"** label badge in a purple chip. KPI panels side-by-side (stack vertically on mobile):

| Panel | Big number | Sub-label |
|-------|------------|-----------|
| **Completed orders** | `orders_completed_price_formatted` (lifetime completed revenue) | *"{count} completed orders"* |
| **Total orders** | `orders_total_price_formatted` (lifetime total revenue) | *"{count} total orders"* — all statuses |
| **Wallet balance** | The customer's [[virtual-wallet|Virtual Wallet]] balance | *"Virtual Wallet"*. For every customer outside the Guests group. |

The two order panels come from the customer's denormalized `income` block — eventually consistent (typically within seconds). See "Business rules" below.

### Identity card

The customer's "who" card. The headline is the customer's name; the pencil icon at the top-right opens an action dropdown.

- **Customer name** (heading) + edit pencil → dropdown with **Edit customer** / **Change password** / **Confirm email address** / **Send confirmation email** (the last two only when email is unverified — see [[customer-details-email-verification]]).
- **Email** with verification status indicator (red *"Email address not verified"* + red X when `email_confirmed = no`; standard text when verified).
- **Registered on `<date>`**, **Customer phone** (when set), **Customer group** badge, and **Custom fields** (the per-store custom fields defined on [[customer]]).

### Identity-card dropdown options

| Option | What it does |
|--------|--------------|
| **Edit customer** | Opens the full Customer Create/Edit panel pre-filled, titled with the customer's name. See [[customers-create-modal]]. |
| **Change password** | Opens the password window. See [[customers-change-password]]. |
| **Confirm email address** | Only when `email_confirmed = no` — see [[customer-details-email-verification]]. |
| **Send confirmation email** | Only when `email_confirmed = no` — see [[customer-details-email-verification]]. |

### Customer note card

- Renders **ONLY** when the customer has a note set — empty notes don't render the card at all.
- Title row: notebook icon + label *"Notes"* (left) + pencil edit button (right).
- Server-validated to 191 chars max.
- Click pencil → opens the full Edit Customer panel with the **Customer note** field focused. See [[customers-create-modal]].
- Note is NEVER shown to the customer — admin-only.

### Metafields card

A card titled **Metafields**, below the note card, holding the store's customer [[metafields-definitions|metafields]].

- Pinned definitions show first, in pin order. **Show all ({count})** opens the rest and **Show pinned only** closes them. With no pinned definition it reads *"No metafield is pinned."*
- With no definitions at all it reads *"No metafield definitions yet. They are added in Settings → Metaobjects."*
- If the values cannot be read it says *"The metafields could not be loaded."* with a **Try again** button.
- Each field uses the input for its type; see [[metafields-value-inputs]].
- A save bar appears as soon as a value differs from the saved one. It saves the metafields alone, separately from the rest of the customer. **Discard** puts the saved values back. A refused value shows its error on the field.

### Customer tags picker

A dedicated card below the Metafields card.

- Tag-shape icon + label *"Tags"* (header row) + helper text *"Use tags to define customer groups and segments. Create marketing campaigns to specific groups"*.
- **Multi-tag search-select** — typeahead against `GET /admin/api/core/customers/tags`. Each chip is a current tag.
- **Create on the fly**: typing a non-existing tag shows an *"Add '{name}' as a tag for this customer"* footer link in the dropdown. Case-insensitive dedup — an already-existing tag triggers an *"exists"* message instead.
- **Save tags** button — disabled until the list differs from the one loaded. Saving adds the chips to the customer. Toast: *"Tags saved successfully"*. See "Tag saves only ADD tags" below.

The picker feeds the [[customers]] list filter and the segments built on [[marketing-segments]] — applying a tag here changes campaign eligibility immediately.

## Settings & fields

Editable fields on the identity card live in the Edit Customer panel — see [[customers-create-modal]] for the full list. Identity-card-surfaced fields:

| Field | Editable from | Note |
|-------|---------------|------|
| `first_name`, `last_name` | Panel | Required, max 191 chars. |
| `email` | Panel | See [[customer-details-email-verification]]. |
| `alternative_phone` | Panel | Shows as **Customer phone**. |
| `group_id` | Panel | Surfaced as badge. |
| Note | Panel | Hard-capped 191 chars server-side. |
| Custom fields | Panel → custom fields | Per-store definitions on [[customers-custom-fields]]. |
| Metafields | Metafields card (inline) | Own save bar. |
| Tags | Tags card (inline) | Save adds new chips. |

## Business rules

### Insights numbers are eventually consistent

The Customer record stores `income`, `completed_orders`, `orders_total`, `orders_total_price`, `last_order_date` directly on the row (denormalized). A queued job recalculates these whenever an order is created, paid, refunded, cancelled, or fulfilled. So the Insights KPIs can briefly lag the actual order state — they converge once the job runs (typically within seconds). The page loads the customer once on opening, so moving between tabs doesn't refresh them; reload the page to see the freshest numbers.

### Customer note has a 191-character hard cap

The customer note (admin-only field) is limited to **191 characters maximum**. A note longer than 191 chars throws the `customer.err.note_max_chars_%1$s` translation error. (191 is the platform's standard index-friendly column limit.) For longer records, the merchant should use customer tags + a separate notes system, or keep the note terse. Notes are NEVER shown to the customer — admin-only.

### Tag saves only ADD tags

The save endpoint adds the posted tags to the customer and keeps every tag the customer already has — it does NOT replace the set. Removing a chip in the picker and saving leaves that tag on the customer, and saving an empty picker is rejected. Through the Admin GraphQL API ([[settings-pat-tokens]]), `addCustomerTags` adds tags the same way and `removeCustomerTags` removes tags by their IDs. Saving here does not copy the tags to the matching Subscriber record; segments in [[marketing-segments]] that use the **Customer tag** condition read the customer's own tags.

### Identity-card "Edit pencil" opens the panel

The pencil icon at the top-right of the identity card is the entry point to all customer-editing operations. There is no inline editing of name / email — the merchant always goes through the panel.

## Related

- [[customers-details]] — hub.
- [[customers]] — list page; the picker feeds the list-filter and the Customer Create/Edit panel opens from both surfaces.
- [[customer]] — entity page; carries all the fields surfaced here.
- [[customer-group]] — customer-group definitions used in the identity-card badge.
- [[customers-custom-fields]] — per-store custom fields rendered at the bottom of the identity card.
- [[customers-change-password]] — change-password window.
- [[customer-details-email-verification]] — Confirm-email / Send-confirmation dropdown items.
- [[marketing-segments]] — segments built from the tags applied here.
- [[metafields-definitions]] — the definitions behind the Metafields card.

## Open questions

None.
