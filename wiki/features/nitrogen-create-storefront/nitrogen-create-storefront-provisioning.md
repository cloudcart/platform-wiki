---
type: feature
nav_path: "Nitrogen → Storefronts → Create Storefront → Provisioning"
route_name: nitrogen.storefront.select-repo
route_path: /admin/nitrogen/create/repository
aliases: ["Nitrogen provisioning step", "Setting Up Your Storefront", "Nitrogen provision steps", "Nitrogen create payload"]
tags: [nitrogen, storefronts, create, wizard, provisioning, github]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Nitrogen → Create Storefront — Provisioning + success

> Part of [[nitrogen-create-storefront]]. See the hub for the other aspects (setup, GitHub connection, repository selection).

## Purpose

This is **Step 3** of the GitHub path: after the merchant clicks Continue on the repository step ([[nitrogen-create-storefront-repository]]), the page switches to a provisioning sub-view that runs the creation steps in sequence, shows live progress, lets the merchant retry a failed step, and on full success redirects to the new storefront's detail page. This aspect also documents the combined create payload + server-side validation.

## Where to find it

Same route as the repository step (`nitrogen.storefront.select-repo`, `/admin/nitrogen/create/repository`), with the internal step set to provisioning. Header swaps to *"Setting Up Your Storefront"* with the cog icon; the breadcrumb appends *"Setting Up"*. On full success the page auto-routes to `nitrogen.storefront.overview` ([[nitrogen-storefront-overview]]).

## What the merchant can do here

- **Watch** the sequential provisioning steps complete (progress bar + per-step state icons).
- **Retry** a failed step (and the steps after it) via a danger button when one fails.
- Be **auto-redirected** to the new storefront's detail page on success — no further action needed.

The merchant should not close the page during provisioning (the card warns *"This usually takes a few seconds. Please don't close this page."*).

## Settings & fields

The provisioning card (centered, `max-w-lg`) contains:

- **Header** — rocket icon in a purple circle + *"Setting up your storefront"* + the don't-close warning.
- **Progress bar** — shows `completed + 0.5 × inProgress` over `total`.
- **Steps list** — sequential items, each with a state icon (`completed` = green check / `in-progress` = purple spinner / `failed` = red X / `pending` = grey dot) and a label whose colour also reflects state (purple-bold while in-progress, grey when done, red-bold when failed, light-grey when pending).

### Step list — Create-new-repo path (3 steps)

1. *"Creating GitHub repository"* — POSTs `/admin/api/core/nitrogen/github/create-repo` with `{ name, private }`.
2. *"Initializing from starter template"* — copies content from `cloudcart/nitrogen-starter` into the new repo.
3. *"Provisioning storefront & configuring deployment"* — creates the storefront with the GitHub linkage (`repository = full_name`, `branch = 'main'`, `is_new_repo = true`).

### Step list — Connect-existing path (2 steps)

1. *"Connecting GitHub repository"* — verifies the repo + the App installation.
2. *"Provisioning storefront & configuring deployment"* — creates the storefront with `repository = full_name`, `branch = default_branch || 'main'`, `is_new_repo = false`.

### Combined create payload

The final step POSTs to `POST /admin/api/core/nitrogen/storefronts`:

| Field | Required | Notes |
|-------|----------|-------|
| **`name`** | Yes | `string, max:255`. |
| **`deployment_method`** | No (defaults to `cli`) | `in:cli,github`. Set to `github` on this path. |
| **`repository`** | No | Full GitHub name `owner/repo`. |
| **`branch`** | No | `main` for new repos; the repo's `default_branch` for existing. |
| **`is_new_repo`** | No | `boolean`. `true` for create-new, `false` for existing. |

Server-side validation:

```
'name' => 'required|string|max:255',
'deployment_method' => 'sometimes|in:cli,github',
'repository' => 'sometimes|nullable|string|max:255',
'branch' => 'sometimes|nullable|string|max:255',
'is_new_repo' => 'sometimes|boolean',
```

## Business rules

### Per-step failure isolates and offers Retry

On failure, the failing step turns red, an error banner appears under the steps showing the API error message, and a **Retry** danger button re-runs the failed step and the steps after it (the already-completed earlier steps are not redone). This means a transient GitHub hiccup at the template-copy stage doesn't force re-creating the repo.

### Success auto-redirects to the storefront detail

On full success the page auto-routes to `nitrogen.storefront.overview` with the new storefront's id — the merchant lands on their newly-created storefront's detail page ([[nitrogen-storefront-overview]]) rather than back on the wizard.

### Max 10 storefronts per site — enforced before the repo is created

The `max_storefronts_per_site` cap (default 10) is enforced at the storefront-creation stage **before** the GitHub repo is created, so a merchant at the cap is rejected without leaving an orphan repo behind. The wizard's UI cap reads the same value via the list endpoint's `meta.max_storefronts`. See the hub [[nitrogen-create-storefront]] for the owner-only + cap rules.

### Branch defaults differ by strategy

New-repo provisioning always uses `branch = 'main'` (the starter template's default branch). Existing-repo provisioning uses the repo's own `default_branch`, falling back to `main` only if none is reported.

## Related

- [[nitrogen-create-storefront]] — hub.
- [[nitrogen-create-storefront-repository]] — the prior step whose strategy selects the 2-step vs 3-step path.
- [[nitrogen-storefront-overview]] — storefront detail page reached on success.
- [[nitrogen-deployments]] — Deployments tab where the first auto-deploy appears.

## Open questions

_None._
