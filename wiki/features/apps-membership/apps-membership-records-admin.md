---
type: feature
nav_path: "Apps → Membership → Records admin (Settings tab)"
route_name: apps.membership.settings
route_path: /admin/orders/subscriptions/settings
aliases: ["Membership settings tab", "Membership records list", "Add subscription modal", "Additional days modal", "Membership filters"]
tags: [apps, administration, membership, admin-ui]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Membership — records admin (Settings tab)

> Part of [[apps-membership]]. See the hub for the other aspects (data model, purchase flow, renewal/revocation, API).

## Purpose

This aspect documents the **Settings tab** of the Membership app — which, despite its name, is not a settings form. It is a filterable table of every membership record plus two modals (Create, Extra Days). This is where the merchant manually creates, extends, and deletes individual memberships.

## Where to find it

Sidebar → Apps → Membership → **Settings** tab, at `/admin/orders/subscriptions/settings`.

## What the merchant can do here

- Browse, filter, and paginate every membership record.
- Manually create a membership (Add Subscription modal).
- Extend an existing membership by N days (Additional days modal).
- Delete / cancel an individual membership (per-row action).

### What the merchant CANNOT do here

- Bulk-extend, bulk-delete, or export — every action is per-row.
- Extend a lifetime membership — the +Additional days trigger is hidden for `expired = null` rows.
- Generate a downloadable / scannable membership card or pass.

## Settings & fields

### Settings tab is actually a List + 2 modals (not a settings form)

Despite being titled "Settings", the Settings tab is a **table-with-filters view** of every membership record + a Create modal + an Extra Days modal. There is no form-level configuration; merchants create or extend individual memberships directly here.

**Table columns**: Customer name, Product, Page, Status, Active to (expiry date), and an actions column.

**Available filters** (top of the list):

| Key | Label | Type | Operators |
|---|---|---|---|
| `status` | Status | Single-select | Active / Disabled |
| `date` | Date | Date picker + operator | exactly / before / after |
| `customer` | Customer | Multi-select (autocomplete from `/admin/autocomplete/customer`) | Includes / Does not include |
| `product` | Product | Multi-select (`/admin/api/core/products/search`) | Includes / Does not include |
| `pages` | Page | Multi-select (`/admin/autocomplete/pages`) | Includes / Does not include |

Pagination: 25 per page by default, query-param-backed (`?page=N&perpage=N`).

### Add Subscription modal (Create)

Triggered from the **Create new** button (in the empty-state of the table, or from the parent app's "Create modal" prop):

| Field | Type | Validation |
|---|---|---|
| **Select user** (`customer_id`) | Searchable autocomplete (`/admin/api/core/customers/autocomplete`) | Required ("You have not selected a user"). |
| **Select the page** (`page_id`) | Searchable autocomplete (`/admin/api/core/pages/search`) | Required ("You have not selected any pages"). |
| **Access days** (`days`) | Integer input | Required. Min 0 / Max 3652 (10 years). Tooltip: *"If you want the user to get unlimited access in the field you need to enter 0"* (so 0 = lifetime). Max-exceeded error: *"Maximum number of days you can enter is 3652 (10 years)"*. |

Buttons: **Close** (cancel) and **Save**. Save POSTs `{customer_id, page_id, days}` to `/admin/api/membership/create` (see [[apps-membership-api]]). Success toast: *"Successfully added a subscription"* and the new row is appended to the table without a refetch.

### Additional days modal (Extra Days)

Triggered from a per-row action button on an existing membership row. Shows ONE field:

| Field | Type | Validation |
|---|---|---|
| **Add extra days** (`extra_days`) | Integer input | Required. Min 0 / Max 365. Tooltip: *"Add additional free days to access the selected order pages. If you want the user to get unlimited access in the field you need to enter 0"*. |

The Save button is disabled while `extra_days = 0` (so the merchant must type a positive value or the field is blocked — the "0 = unlimited" tooltip applies to the Create modal, not this one). Save POSTs `{id, extra_days}` to `/admin/api/membership/add-extra-days`. Success toast: *"You have successfully added additional free days"*. Error toast: *"An error occurred, please try again"*. The row's expiry date refreshes in-place after success.

## Business rules

### No bulk actions, no exports

The list does not expose bulk-extend, bulk-delete, or CSV export. Each Extra Days action is per-row. Cancellation is per-row via the row's delete action (which sends a delete request per membership ID — see [[apps-membership-api]]).

### "+ Additional days" button is hidden for lifetime memberships

The per-row **+ Additional days** trigger is rendered only when the row has a non-null `expired_date`. So for lifetime memberships (where `expired = null` per a `days = 0` setup — see [[apps-membership-data-model]]) the button is hidden — there is no need to extend an already-unlimited membership. The Delete action remains available for those rows.

### No membership card / digital pass

There is no Apple Wallet, Google Wallet, or PDF-card endpoint. The customer's "membership card" is implicit — they log in and access the pages the membership grants them (page-gating enforcement is documented in [[apps-membership-renewal-revocation]]). The merchant cannot generate a downloadable / scannable pass.

## Related

- [[apps-membership]] — hub.
- [[apps-membership-api]] — the endpoints the modals POST to.
- [[customers]] — the customer selected in the Create modal.
- [[products-products]] — the product column / filter.

## Open questions

None.
