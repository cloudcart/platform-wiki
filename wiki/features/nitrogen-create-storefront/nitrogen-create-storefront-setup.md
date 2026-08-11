---
type: feature
nav_path: "Nitrogen → Storefronts → Create Storefront → Setup"
route_name: nitrogen.storefront.create
route_path: /admin/nitrogen/create
aliases: ["Create Storefront step 1", "Nitrogen storefront setup step", "Nitrogen CLI deploy path", "Nitrogen deploy token"]
tags: [nitrogen, storefronts, create, wizard, cli, deploy-token]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Nitrogen → Create Storefront — Setup step + CLI path

> Part of [[nitrogen-create-storefront]]. See the hub for the other aspects (GitHub connection, repository selection, provisioning).

## Purpose

This is **Step 1** of the Create Storefront wizard: the merchant names the storefront and picks a deployment method. When the method is **CLI / CI-CD**, the wizard finishes here — the storefront is created immediately and a success card hands over a one-time deploy token plus the three `cloudcart` CLI commands to link, pull env, and deploy. When the method is **GitHub**, this step just collects the name and hands off to [[nitrogen-create-storefront-github-connect]].

## Where to find it

Route name `nitrogen.storefront.create`, path `/admin/nitrogen/create`. Reached from the **Create Storefront** button (top-right) on the storefronts list ([[nitrogen-storefronts]]). A single centered card (`max-w-xl`).

## What the merchant can do here

- Type a **Storefront Name** (auto-focused on mount).
- Pick a **deployment method**: **CI/CD or manual** (`cli`) or **GitHub** (`github`).
- **Cancel** (ghost) → returns to the storefronts list.
- Click **Next** (GitHub) or **Create Storefront** (CLI) — the primary button label changes with the selected method.
- On the CLI success sub-view: copy the **deploy token**, read the three CLI commands, and click **Go to Storefront**.

## Settings & fields

### Step 1 inputs

| Field | What it controls | Validation |
|-------|-----------------|------------|
| **Storefront Name** | Display name (shows in the list and breadcrumbs). Placeholder: *"e.g. My Headless Store"*. Auto-focus on mount. | `required`, `string`, `max:255`. Empty disables the Next/Create button. Server enforces the same rules; trim is applied client-side. |
| **How do you want to deploy?** | Two card-style radio options: **CI/CD or manual** (terminal icon — *"Deploy using the CloudCart CLI or your own CI/CD pipeline. You'll get a deploy token."*) and **GitHub** (GitHub icon — *"Automatically deploy on every push to your GitHub repository."*). | Required pick. Default: `github`. |

**Action bar** — **Cancel** (ghost) and the primary button whose label depends on `deploymentMethod`:

- `cli` → reads *"Create Storefront"* and immediately creates the storefront (skipping the repo step).
- `github` → reads *"Next"* and routes to the GitHub connection step after a connectivity check.

### CLI success sub-view fields

After a successful CLI create (same route re-renders, no navigation), the card shows:

- Green success banner: *"Storefront created!"*.
- **URL card** with the storefront's Nova hostname (e.g., `https://my-store.nova.cloudcart.com`) and the badge *"Waiting for first deployment"*.
- **Deploy token** card — masked display with a copy button plus a one-time-only warning.
- **Next steps** card with three sequential CLI commands:
  - `cloudcart nitrogen link` — *"Connect your local project to this storefront"*.
  - `cloudcart nitrogen env pull` — *"Download environment variables to.env"*.
  - `cloudcart nitrogen deploy` — *"Build and deploy your storefront to Nova"*.
- **Go to Storefront** primary button → routes to the storefront's detail page ([[nitrogen-storefront-overview]]).

## Business rules

### CLI path skips the repository step entirely

When the merchant picks CLI / CI-CD and clicks **Create Storefront**, the wizard POSTs `{ name, deployment_method: 'cli' }` to `POST /admin/api/core/nitrogen/storefronts` and, on success, re-renders the CLI success sub-view in place (no route change). There is no repo selection because deploys are merchant-managed via the `cloudcart` CLI plus the issued deploy token. On error, an inline message renders under the form (the API message, or fallback *"Failed to create storefront"*).

### Deploy token shown ONCE — copy or rotate

The deploy token on the CLI success card is the **only** time the full token is displayed. After leaving the page, the merchant sees only a masked preview and must **rotate** the token (from the storefront detail page) to obtain a fresh full value. This matches GitHub's personal-access-token pattern.

### Default method is GitHub

The deployment-method picker defaults to `github`, so the primary button initially reads *"Next"*. The merchant must actively switch to CLI / CI-CD to get the immediate-create + deploy-token flow.

### Name is required client- and server-side

An empty (or whitespace-only, after trim) name disables the primary button; the server applies the same `required|string|max:255` rule, so a bypassed client check still fails server-side.

## Related

- [[nitrogen-create-storefront]] — hub.
- [[nitrogen-create-storefront-github-connect]] — the GitHub-path next step (when method = `github`).
- [[nitrogen-storefront-overview]] — storefront detail page reached by **Go to Storefront**.
- [[nitrogen-deployments]] — Deployments tab where CLI deploys appear after `cloudcart nitrogen deploy`.

## Open questions

_None._
