---
type: feature
nav_path: "Marketing → Discounts → Container codes → List view"
route_name: discounts-codes_list
route_path: /admin/marketing-new/discounts/codes
aliases: ["Container codes list view", "Container codes row actions", "Container codes bulk actions", "Container codes columns", "Списък с промо кодове", "Масови действия върху промо кодове"]
tags: [marketing, discounts, coupons, container, list-view, bulk-actions]
plan_gates: ["discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Container codes — list view, columns, row & bulk actions

> Part of [[marketing-discounts-codes]]. See the hub for the generator, redemption, parent-term inheritance, and the JSON-API.

## Purpose

The list view is what the merchant sees when they open **Promo code management** on a Container discount. It shows every single-use code generated under all of the store's Container discounts, lets the merchant copy a code as a shareable cart link, toggle a code on/off, and run bulk status / delete operations. There is **no per-code edit form** — a code is generated, toggled, or removed, never edited in place.

## Where to find it

From any Container-discount row in the [[marketing-discounts]] table, click "Promo code management". The list loads at `/admin/marketing-new/discounts/codes`; the breadcrumb reads "Marketing → Discounts → Container codes".

## What the merchant can do here

- **See every Container code in the store** with columns: **Code** (the literal string, click-to-copy as a `/cart/discount:<code>` URL), **Value** (the percentage or money amount, formatted in store currency), **Created At**, and an **Active** toggle per row. (There is no separate "Type" column in the modern list.)
- **Copy a code as a cart-link** — clicking the code icon copies a pre-built `<store-domain>/cart/discount:<CODE>` URL that auto-applies the code when shared (newsletter, SMS). The redemption mechanics are on [[discounts-codes-redemption]].
- **Filter** by **Active** state (Yes / No).
- **Sort** by Code, Value, Created At, or Active.
- **Search** the table to find a specific generated code by string.
- **Toggle a single code** active / inactive via the row switch. Inactive codes are rejected at checkout (the customer sees "invalid code").
- **Bulk-toggle status and bulk-delete** via the table action bar.
- **Generate a new batch** via the *Generate codes* action — opens the modal documented on [[discounts-codes-generator]].

### What the merchant CANNOT do here

- **Edit an existing code's type or value** — there is no per-code form. A wrong-value code can only be deleted (or deactivated) and replaced.
- **Choose the length, prefix, or character set** of generated codes — hard-coded at 10 characters, uppercase A-Z plus digits 0-9. For finer control use [[marketing-discounts-code-pro-generator]] (see [[discounts-codes-vs-code-pro]]).
- **Generate more than 1,000 codes in one request on the legacy generator** — its validator returns *"You can generate maximum 1000 promo codes"*. The modern Vue "Generate codes" modal has no upper cap (see [[discounts-codes-generator]]).

## Settings & fields

### Listing columns

| Column | What it shows |
|--------|---------------|
| **Code** | The literal code string, click-to-copy as a cart-discount URL (`/cart/discount:<CODE>`). Sortable. |
| **Value** | Percent ("15%") or money ("10.00 EUR") — formatted in the store currency. Sortable. |
| **Created At** | When the code was generated. Sortable. |
| **Active** | Inline toggle — calls `/admin/api/core/discounts/codes/change-status` with `{ids, status}`. Sortable. |
| (actions) | Per-row remove. |

### Filters & sort

| Filter | Options |
|--------|---------|
| **Active** | Yes / No |

Default sort is newest-first. Sortable columns: Code, Value, Created At, Active.

### Row & bulk actions

| Action | Endpoint | Method |
|--------|----------|--------|
| Toggle active (row) | `/admin/api/core/discounts/codes/change-status` | POST (`{ids, status: 1|0}`) |
| Bulk: Set status active | `/admin/api/core/discounts/codes/change-status` | POST (`status: 1`) |
| Bulk: Set status unactive | `/admin/api/core/discounts/codes/change-status` | POST (`status: 0`) |
| Bulk: Delete | `/admin/api/core/discounts/codes` | DELETE (`{ids}`) |
| Per-row Remove | `/admin/api/core/discounts/codes` | DELETE (single id) |

The per-row Remove confirmation message is *"Remove this code?"*.

## Business rules

- **Toggle revokes without deleting.** The per-row Active toggle flips the code's `active` flag. An inactive code is rejected at checkout — the customer sees the "invalid code" message. Use this to revoke leaked codes while preserving their history for analytics.
- **Delete is a direct removal, parent untouched.** Deleting a Container code removes the code row directly. The parent Container discount is untouched, and historical order-discount rows that reference the deleted code remain in place for accounting — see [[discounts-codes-parent-terms]] for the cascade detail.
- **No "uses" counter per code in this listing.** The merchant sees only the active flag (active = available; inactive = consumed or manually disabled). The parent's aggregate `uses` counter is documented on [[discounts-codes-parent-terms]].
- **Permission.** The page and its endpoints are scoped under the same `marketing.discounts` permission as the rest of the Discounts engine.

## Related

- [[marketing-discounts-codes]] — hub.
- [[marketing-discounts]] — parent feature; the Container discount type lives there.
- [[discount-code]] — entity page for individual generated Container codes.

## Open questions

No outstanding questions.
