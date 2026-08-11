---
type: feature
nav_path: "Nitrogen → Storefronts"
route_name: nitrogen.storefronts
route_path: /admin/nitrogen
aliases: ["Nitrogen Storefronts", "Headless Storefronts list", "Storefronts list", "Nitrogen list"]
tags: [nitrogen, storefronts, headless, list, owner-only]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 4
---
# Nitrogen → Storefronts (list)

## Purpose

The **Storefronts list** is the landing screen of the Nitrogen (headless storefront) area. It shows every Nitrogen storefront the merchant has created on this site, with each row exposing the storefront's name, Nova hostname (the deployed URL), current status, and creation date. From this list the merchant creates a new storefront (CLI/CI-CD-based or GitHub-based), opens an existing one to manage its deploys / environment variables / API tokens / customer-account integration, or deletes one outright.

Nitrogen is CloudCart's **headless** layer: the merchant builds and deploys their own Vue / React / Next / Nuxt storefront against CloudCart's Storefront API; this list manages the metadata (name, deploy tokens, env vars, scopes, GitHub linkage) for each headless build target.

## Where to find it

Sidebar → **Nitrogen** (top-level pillar) → routes to `/admin/nitrogen`. The page renders `NitrogenStorefrontsListPage.vue` (modern Vue, `CcDomain/Nitrogen/Pages/NitrogenStorefrontsPage`). Breadcrumb reads **Nitrogen → Storefronts**.

The header shows the rocket icon (`far fa-rocket`), title "Nitrogen Storefronts", and the description: *"Create and manage your headless storefronts. Each storefront gets its own API tokens and environment configuration."*

Sub-routes reachable from this screen:

| Action | Route name | Path |
|--------|------------|------|
| Storefronts list | `nitrogen.storefronts` | `/admin/nitrogen` |
| Create storefront — step 1 | `nitrogen.storefront.create` | `/admin/nitrogen/create` |
| Create storefront — step 2 (repo) | `nitrogen.storefront.select-repo` | `/admin/nitrogen/create/repository` |
| Storefront detail | `nitrogen.storefront.overview` | `/admin/nitrogen/:storefrontId` |
| Deployments (per storefront) | `nitrogen.deployments` | (under detail) |

## What the merchant can do here

### See the storefronts table

A standard CcTable with these columns:

| Column | What it shows |
|--------|---------------|
| **Name** | Storefront display name. Clicking opens the detail page (`nitrogen.storefront.overview`) for that storefront. |
| **Nova URL** | The Nova-hosted hostname (`<slug>.nova.cloudcart.com` or similar) where deployed builds are served. |
| **Status** | The storefront's deployment status badge (waiting for first deployment / deployed / failed / building). |
| **Created** | Creation date (`type: 'date'`). |
| **Actions** | Inline row actions (delete). |

Above the table the right side shows a **`{count} of {max} storefronts`** chip — the live count vs the per-site cap. The default cap is **10 storefronts per site** (`config('nitrogen_scopes.limits.max_storefronts_per_site', 10)`).

The **Create Storefront** button is disabled once the cap is reached.

### Create a new storefront

Click **Create Storefront** (top-right primary button). Routes to `nitrogen.storefront.create` — see [[nitrogen-create-storefront]] for the full 2-step wizard (Name + deployment method → optional GitHub repo selection → success page with deploy token / CLI instructions).

### Delete a storefront

A row action calls `apiNitrogenStorefronts.remove`. On success: toast "Storefront deleted successfully" and the row is removed from the local query cache (with pagination repair if the deleted row was the last on its page). Deletion removes the storefront's deploy token, env vars, Nova tokens, and GitHub installation linkage; existing deployments on Nova are NOT automatically torn down by this action.

### Open the empty state

If the merchant has zero storefronts, the table is replaced by an empty-state panel:

- Rocket icon (`far fa-rocket`, `text-4xl`).
- Title: **"No Storefronts"**.
- Body: **"Create your first Nitrogen storefront to get started with headless commerce"**.
- Primary action button: **"Create Your First Storefront"** → `nitrogen.storefront.create`.

### What the merchant CANNOT do here

- Bulk-delete storefronts — the table has `show-bulk-actions="false"` (deletion is row-by-row).
- Rename a storefront from the list — renaming happens in the detail page.
- Reorder storefronts — there's no manual sort; the table is sortable=false on every column (server-controlled order, newest first).
- Trigger a deploy from the list — deploys are queued from the detail page's Deployments tab or from the CLI / GitHub Actions workflow.
- See deploy history on the list — only the latest status badge is shown; full history requires opening the storefront.

## Settings & fields

This is a list view — no editable fields on the row itself. All editing happens via the per-storefront detail page sub-tabs (Environment / Customer Account / Nova tokens / Storefront API tokens) and the Deployments tab.

## Business rules

### Per-site cap of 10 storefronts (default)

The platform allows up to 10 Nitrogen storefronts per site by default. The exact cap is `config('nitrogen_scopes.limits.max_storefronts_per_site', 10)` — it is platform-level (not merchant-editable). Hitting the cap disables the "Create Storefront" button; the merchant must delete an existing storefront to free a slot.

### Each storefront is fully isolated

Per the header description: *"Each storefront gets its own API tokens and environment configuration."* Storefronts on the same CloudCart site do NOT share deploy tokens, Nova tokens, Storefront API tokens, env vars, or GitHub installation. Building one storefront and breaking another's deploy chain is impossible.

### List is paginated server-side

The `apiNitrogenStorefronts.index` query is paginated. URL query params round-trip via `useQueryParams` so a bookmarked URL `/admin/nitrogen?page=2` restores the same page.

### Permission — owner-only

The Nitrogen route group (`/admin/api/core/nitrogen/*`) is wrapped in the `isOwner` middleware. **Only the store owner can list, create, edit, delete, or rotate tokens on storefronts here.** Moderators — even if they have full [[settings-staff]] permissions — get HTTP 403 and never see the sidebar entry. There is no `nitrogen.*` row in the staff permission tree to delegate. See [[nitrogen]] for the full owner-only carve-out across this pillar.

## How it works (verified against backend)

- The page mounts `NitrogenStorefrontsListPage.vue` which calls `apiNitrogenStorefronts.index.useQuery({ params: query })`.
- Backend route is in the platform code → the request handler → returns `{ data: [...], meta: { total, max_storefronts: 10 } }`.
- The `meta.max_storefronts` is read from `config('nitrogen_scopes.limits.max_storefronts_per_site', 10)`. Editing this config requires a platform-level deploy.
- `Create Storefront` validation lives in the request handler:
  ```
  'name' => 'required|string|max:255',
  'deployment_method' => 'sometimes|in:cli,github',
  'repository' => 'sometimes|nullable|string|max:255',
  'branch' => 'sometimes|nullable|string|max:255',
  'is_new_repo' => 'sometimes|boolean',
  ```
- The Storefront service also enforces the `max_storefronts_per_site` cap server-side on `create` — even if the merchant bypasses the UI, the API rejects with the configured limit.

## Related

- [[nitrogen]] — Nitrogen pillar hub.
- [[nitrogen-create-storefront]] — Create-storefront wizard (Name + deployment method + repo selection + provisioning).
- [[nitrogen-storefront-overview]] — Per-storefront detail page (Environment / Customer Account / Nova tokens / Storefront API tokens / Deployments).
- [[nitrogen-deployments]] — Deployments tab (per-storefront).
- [[apps]] — App Store (for adjacent storefront-side apps).

## Open questions

_None — list view fully documented._
