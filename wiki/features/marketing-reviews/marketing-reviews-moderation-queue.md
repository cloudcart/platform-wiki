---
type: feature
nav_path: "Apps → Product Reviews → Reviews"
route_name: apps.product_review.reviews
route_path: /admin/apps/product_review/reviews
aliases: ["Reviews moderation queue", "Pending reviews list", "Reviews table", "Списък с ревюта", "Модерация на ревюта"]
tags: [marketing, apps, reviews, moderation]
plan_gates: ["product_reviews_added_rating"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Reviews — Moderation queue (table)

> Part of [[marketing-reviews]]. See the hub for related aspects (modals, arrival flows, submission rules, replies, plan cap, Q&A tab).

## Purpose

The Reviews tab inside the Product Reviews app is the merchant's single inbox for every customer review submitted across all products in the store. This aspect documents the **table** itself — its columns, sort, filters, free-text search and bulk actions. Inline detail / answers / create modals are documented in [[marketing-reviews-modals]].

## Where to find it

Sidebar → **Apps** → **Product Reviews** (after install) → **Reviews** tab.

Route: `/admin/apps/product_review/reviews`. The tab strip on this app is **Overview**, **Settings**, **Reviews** (this page), **Questions** (only when Q&A is enabled — see [[marketing-reviews-questions-tab]]).

## What the merchant can do here

- See **all reviews** across all products in a paginated table, newest first (`id desc`).
- Toggle a single review's publish status by clicking the **up-arrow** icon in the row's action cell. Filled = published, outlined = hidden. Toast: *"Status changed successfully"*.
- Click the **trash** icon to delete a single review. Confirmation dialog. Toast: *"Deleted successfully"*.
- Bulk-select rows for bulk Publish / Hide / Delete.
- Filter the table (rating, approval state, customer).
- Free-text search across customer email/name, product name, review title.
- Click **+ Add new review** to manually create a review on behalf of a customer (see [[marketing-reviews-modals]]).

## Settings & fields

### Table columns

| Column | Sortable | Notes |
|--------|----------|-------|
| **Product** (`name`) | No | Product name + thumbnail + link to the product. |
| **Customer name** | No | Either the customer's full name (when logged in) or the guest's `user_name`. |
| **Rating** | **Yes** | 1–5 stars. Default sort on this column is descending. |
| **Comment** | No | Review title — click to open the detail modal with full text + stars. |
| **Date** | No | Review submitted, formatted in store timezone (`d.m.Y H:i`). |
| (Answers) | No | Speech-bubble icon with count badge — click to open the answers modal. |
| (Actions) | No | Publish / Hide toggle + Delete icon. |

### Filters (filter sidebar)

| Filter | Operator | Notes |
|--------|----------|-------|
| **Rating** | Equals / Not equals / Lower than / Greater than | Numeric. Useful to find every 1-star review in one click. |
| **Is approved** | Yes / No | Show only published OR only pending reviews. |
| **Customer** | Includes / Does not include | Autocomplete-based customer picker (multi-select). |

Free-text **search** column scope (verbatim): `queryFilterColumns = ['customer:email,first_name,last_name', 'product:name', 'title']` — i.e. customer email, customer first/last name, product name, review title.

### Bulk actions

| Action | Endpoint | Confirmation? | Toast on success |
|--------|----------|---------------|------------------|
| **Publish reviews** | `POST /admin/api/product_review/status/1` | No | *"Published successfully"* |
| **Hide reviews** | `POST /admin/api/product_review/status/0` | No | *"The reviews was hidden successfully"* |
| **Delete** | `DELETE /admin/api/product_review/delete` | Yes — *"Are you are sure you want to delete? Caution: This action cannot be undone."* | *"Deleted successfully"* |

### Default sort

Server-side default ordering is `id desc` — newest reviews show first. The Rating column header click toggles client-side sort on Rating only; other columns are not sortable.

### Status states (two only)

There are exactly two states for a review:

- `is_approved = 1` — **Published**: shows on the storefront product page.
- `is_approved = 0` — **Hidden**: stored, visible only in this admin queue, never rendered to storefront visitors.

There is no separate "Spam" or "Trash" state — deleting is a hard delete (see Business rules). For how a review *arrives* in either state, see [[marketing-reviews-arrival-flows]].

## Business rules

### Index query filters out replies

The table lists ONLY root reviews. Replies live in the same backing table with `parent_id` pointing at the root review; the index query explicitly excludes any row with a non-null `parent_id`. Replies surface only inside the answers modal — see [[marketing-reviews-replies]].

### Status change recomputes the product summary immediately

Every Publish / Hide / Delete (bulk OR per-row) recomputes the affected product's aggregate rating + total review count. The storefront product page's "X stars (Y reviews)" headline reflects the moderation decision **on the next page load — no cache TTL**.

### Bulk delete is irreversible — answers cascade

Per-row trash and bulk Delete both **hard-delete** the review row and cascade the delete down to every threaded answer. There is no soft-delete fallback. The data is gone.

### Verified-buyer is NOT visually badged on the row

Reviews submitted under verified-buyer mode (`added_reviews_conditions = 'buyer'`) carry the `customer_id` and `order_id` on the row, but the queue UI **does not visually badge "verified buyer"** — the merchant only sees the customer's name. See [[marketing-reviews-submission-rules]].

### Guest-review fields appear inline

Guest submissions (`added_reviews_conditions = 'all'` with no logged-in customer) write the typed name + email directly on the review row as `user_name` + `user_email`. The Customer column shows `user_name`. The customer relation is null in that case.

### Permission

The Reviews moderation queue inherits the standard Apps permission gate. The Marketing pillar visibility uses `marketing.*` permissions (see [[marketing]]); per-feature staff permissions are configurable in [[settings-staff]].

### Deep-link the filtered view

The page's filter / search / page state is mirrored to the URL — the merchant can deep-link to "Page 3 of 1-star pending reviews from customer Jane" and share / bookmark that view.

### What the merchant CANNOT do here

- **Edit the review's text** — only Approve / Hide / Delete. No way to fix a typo or shorten a too-long review.
- **Reply to a review as the merchant from this screen** — see [[marketing-reviews-replies]].
- **Flag for re-moderation** — only two states (`is_approved = 1` published, `is_approved = 0` hidden) and a delete. There's no "needs review" intermediate state.
- **Bulk-publish only reviews above a rating threshold** — done at submission time via [[apps-product-review]] Settings. Bulk Publish applies to whichever rows are selected.
- **Export reviews to CSV** — no built-in export action.

## Related

- [[marketing-reviews]] — hub.
- [[apps-product-review]] — parent app: settings, install, broader review policy.
- [[customers-details-reviews]] — per-customer view of the same review data.
- [[marketing]] — Marketing pillar.
- [[settings-staff]] — per-role permissions.
- [[settings-admin-notifications]] — "New review added" admin email notification.

## Open questions

- 📡 **CSV export.** No built-in export action; would the merchant find one useful? (verify)
