---
type: feature
nav_path: "Customers → Customer details → Reviews"
route_name: customers-reviews
route_path: /admin/customers/details/:id/reviews
aliases: ["Customer reviews", "Customer product reviews", "Review history", "Рецензии на клиента", "Ревюта"]
tags: [customers, reviews, ratings, moderation]
plan_gates: []
created: 2026-05-21
updated: 2026-11-03
source_count: 8
---
# Customer reviews

## Purpose

Every **product review** the customer has left on the store, in one paginated table. The merchant uses this sub-tab to find specific reviews, moderate one customer's reviews in bulk, spot patterns (a customer who always rates 1-star — a possible complainer or competitor), or quickly publish / hide / delete reviews from a single source.

This sub-tab is **conditional** — it only appears in the [[customers-details]] tab strip when the **Product Review app** is installed and active. Without that app the tab is not shown, and its address lands on Overview. It is a per-customer filtered view of the same reviews managed on the global [[apps-product-review]] reviews page.

## Where to find it

From [[customers-details]] → **Reviews** tab (when the Product Review app is installed and active). The route is `/admin/customers/details/:id/reviews`.

## What the merchant can do here

- See all reviews this customer has left in a paginated table (default 25 rows, max 100).
- See the newest reviews first; the sort is fixed.
- Free-text search via the `query` field above the filter chips (searches across the customer's email / first_name / last_name, the product name, and the review title).
- Filter the list (see Settings & fields).
- Tick rows and open **Tools** for the **Publish reviews** / **Hide reviews** / **Delete** bulk actions.
- Click the product image to open the product in the store, or the product name to open it in the admin.

What the merchant **cannot** do here:

- Edit the text, rating, or sub-replies of a review (no per-row Edit button, no edit modal). Editing or publicly replying happens on the dedicated [[apps-product-review]] reviews page.
- See the full review body — only the title is shown (see Business rules).
- Sort by rating / date from the UI.

## Settings & fields

The table is read-mostly: only the moderation status changes (via the bulk actions).

### Columns

| Column | Notes |
|--------|-------|
| **Product** | The product's image (tooltip *"See in store"*, links to the storefront page) and name (links to `/admin/products/edit/<id>`). |
| **Customer name** | The customer's full name (from the linked customer record). Falls back to `user_name` if a guest with no linked customer submitted it. |
| **Rating** | Read-only stars. |
| **Comment** (`title`) | The review's **TITLE only** (short summary). The full body (`comment` field) IS returned by the backend but is NOT displayed here — read it on the global [[apps-product-review]] reviews page. |
| **Date** (`created_at`) | When the review was submitted. Formatted server-side as `dd.MM.yyyy HH:mm` in the store's timezone. |
| (no title) | Two row icons: a publish arrow (tooltip *"Published"* / *"Unpublished"*) and a delete icon. See Business rules. |

### Filters

| Filter | Operator vocabulary | Notes |
|--------|---------------------|-------|
| **Rating** | is / is_not / lt / gt (Equals / Not equals / Lower than / Greater than) | Numeric. Useful to find all 1-star reviews. **No lte / gte operators** — the rating dropdown is missing "lower or equal" / "greater or equal" unlike most other numeric filters in the platform. |
| **Is approved** | Yes (1) / No (0) | Show only published, OR only pending / hidden reviews. |

### Bulk actions

| Action | Endpoint + behaviour | Confirmation? |
|--------|----------------------|---------------|
| **Publish reviews** (icon `fa-cloud-upload`) | POST `/admin/api/product_review/status/1` `{ids: [...]}`. Approves the reviews — they appear on the storefront product pages. Toast: *"Published successfully"* (error: *"Error while changing the status"*). | No — fires immediately. |
| **Hide reviews** (icon `fa-cloud-download`) | POST `/admin/api/product_review/status/0` `{ids: [...]}`. Marks the reviews hidden — stored but not shown on the storefront. Toast: *"The reviews was hidden successfully"* (verbatim — known typo in source string). | No — fires immediately. |
| **Delete** (icon `fa-trash-alt`) | DELETE `/admin/api/product_review/delete` `{ids: [...]}`. Permanent removal. Toast: *"Deleted successfully"* (error: *"Error while deleting"*). | Yes — *"Are you are sure you want to delete? Caution: This action cannot be undone."* (verbatim — "you are" typo kept as-is). |

After any of the three actions, the list refetches and the selected ids clear.

## Business rules

### Conditional tab — gated by the Product Review app

The Reviews tab shows ONLY when the Product Review app is installed and active; without the app it is hidden — historical reviews on the customer are not viewable through this UI, and re-installing the app restores access. A staff member without the `apps` permission does not see the tab. Opening or reloading the tab's address directly may land on Overview while the list of apps is still loading; the **Reviews** tab then opens it `(verify)`.

### Moderate with the bulk actions

Use **Tools** to publish, hide or delete reviews on this tab. The two row icons show a success toast but leave the review as it was. The global [[apps-product-review]] reviews page has working row icons.

### Moderation states: Publish / Hide / Delete

Reviews are typically Pending by default `(verify against the moderation policy in the [[apps-product-review]] settings)`. The three actions control storefront visibility:

- **Publish** — approved and visible on the storefront product page.
- **Hide** — stored but NOT visible. Use to keep a record (e.g., for follow-up with the customer) without showing it publicly.
- **Delete** — permanent removal; the only action requiring a confirmation dialog. Publish and Hide proceed immediately on click.

The same three actions exist on the global [[apps-product-review]] reviews page — this tab is just a per-customer filtered view of those reviews.

### Moderating recomputes the product's rating summary

All three bulk actions re-aggregate each affected product's average rating and review count, which are stored on the product record. So after moderation, the storefront rating module reflects the new state instantly (no manual recompute).

### Auto-scoped to one customer (array filter)

The view is auto-filtered by `filters[customer][operator]=in&filters[customer][value][0]=<customerId>` — the merchant can't widen it to other customers from this tab. The backend supports `in` and `not_in` on a list of customer ids, which is why the same endpoint serves the global reviews page's multi-customer filtering.

### Sort + pagination

No column header sorts. Default pagination is 25, max 100.

### `comment` body returned but not rendered

The backend review formatter returns `comment` (full body) and `answers_count` (number of sub-replies / answers) alongside `title`, but the table renders only `title`. Full body + answers are visible on the global [[apps-product-review]] reviews page.

### Permission

The customers permission for the page, plus the `apps` permission for the reviews: the endpoints sit under the app's own route group (`/admin/api/product_review/*`).

## Related

- [[customers-details]] — parent details page (Reviews tab only visible when the app is installed and active).
- [[apps-product-review]] — Product Review app hub: overview, full reviews moderation, settings; the canonical surface for editing / replying / reading full bodies.
- [[products-products]] — the product the review is about.
- [[customer]] — entity page.

## Open questions

- Confirm the default moderation state of a new review (Pending vs auto-published) against the [[apps-product-review]] settings.
