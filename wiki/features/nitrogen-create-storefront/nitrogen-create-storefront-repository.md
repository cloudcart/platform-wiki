---
type: feature
nav_path: "Nitrogen → Storefronts → Create Storefront → Repository"
route_name: nitrogen.storefront.select-repo
route_path: /admin/nitrogen/create/repository
aliases: ["Connect a Repository", "Nitrogen create new repo", "Nitrogen connect existing repo", "Nitrogen starter template", "cloudcart/nitrogen-starter"]
tags: [nitrogen, storefronts, create, wizard, github, repository]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Nitrogen → Create Storefront — Repository selection

> Part of [[nitrogen-create-storefront]]. See the hub for the other aspects (setup, GitHub connection, provisioning).

## Purpose

This is **Step 2** of the wizard, shown when the merchant has chosen the GitHub path and is GitHub-connected ([[nitrogen-create-storefront-github-connect]]). The merchant picks one of two mutually-exclusive strategies: **create a new repository** from the Nitrogen starter template (choosing name + visibility), OR **connect an existing repository** from a searchable list. The selection feeds the provisioning step ([[nitrogen-create-storefront-provisioning]]).

## Where to find it

Route name `nitrogen.storefront.select-repo`, path `/admin/nitrogen/create/repository`. The page header reads *"Connect a Repository"* with the GitHub icon (`fab fa-github`). A storefront context line reads *"Setting up repository for **{storefrontName}**"* (read from sessionStorage).

## What the merchant can do here

- Pick **Create a new repository** (default, badged "Recommended") or **Connect an existing repository**.
- For new-repo: set a **Repository name** and choose **Private** or **Public** visibility.
- For existing-repo: **search** loaded repos, **refresh** the list, and **select** a repo row.
- **Back** (ghost) → returns to the setup route.
- **Create Repository & Storefront** / **Connect & Create Storefront** (primary) → proceeds to provisioning.

## Settings & fields

### Option A — Create a new repository (default, "Recommended")

Sparkles icon, label *"Create a new repository"*. Description: *"We'll create a new GitHub repository from the Nitrogen starter template, pre-configured with everything you need. Your storefront will be ready to develop and deploy in minutes."* Three checkmark feature lines:

- *"Repository created from `cloudcart/nitrogen-starter`"* (starter template repo).
- *"GitHub Actions workflow for automatic deployments"*.
- *"Environment variables and deploy secrets pre-configured"*.

Selecting this card slides down two fields:

| Field | What it controls | Validation |
|-------|-----------------|------------|
| **Repository name** (prefixed with the merchant's GitHub username + `/`) | The new repo's name on GitHub. Placeholder: *"my-storefront"*. Help text: *"Lowercase letters, numbers, and hyphens. No spaces."* | `required`. Regex `^[a-zA-Z0-9._-]+$` (also allows underscores and dots; the help text understates). Errors: *"Repository name is required."* / *"Only letters, numbers, hyphens, underscores, and dots are allowed."* |
| **Visibility** | Two tiles: **Private** (lock icon — *"Only you and collaborators"*) and **Public** (globe icon — *"Visible to everyone"*). | Default: **Private** (`newRepoPrivate = true`). |

### Option B — Connect an existing repository

Link icon, label *"Connect an existing repository"*. Description: *"Link a repository you've already set up. Best if you have an existing Nitrogen project or prefer your own project structure."* Two info lines: *"You may need to add the deployment workflow manually"* (info-blue) and *"Repository secrets and variables configured automatically"* (check-green).

Selecting this card slides down:

- **Search input** + refresh button — filters loaded repos by name OR `full_name` (case-insensitive substring).
- **Repository list** — scrollable (`max-h-[300px]`); each row shows the repo name, a "Private" badge if private, the `full_name` (org/repo), and a relative date (today / yesterday / Nd ago / Nw ago / Nmo ago / Ny ago). Clicking a row sets the selection; a checkmark marks the selected row.
- **Footer** — *"{count} repositories"* (or *"X of Y"* when search filters).
- **Empty state** — *"No repositories match your search."* / *"No repositories found."* + a link to `https://github.com/settings/installations` (*"Can't find a repository? Check app permissions"*).

The list is loaded from `GET /admin/api/core/nitrogen/github/repositories` → `{ data: [...] }`.

### Action bar

- **Back** (ghost, left-arrow) → returns to `nitrogen.storefront.create`.
- **Create Repository & Storefront** OR **Connect & Create Storefront** (primary, label depends on strategy) — disabled until valid (`canContinue`): strategy `create` requires a non-empty repository name; strategy `existing` requires a selected repo.

## Business rules

### Starter template is fixed: `cloudcart/nitrogen-starter`

The new-repo path always clones from `cloudcart/nitrogen-starter` (shown as a code label on the option card). The repo is created in the chosen visibility (Private by default) with the GitHub Actions deploy workflow pre-committed.

### Visibility defaults to Private

Making a Nitrogen storefront's source public is a deliberate opt-in — the Visibility tile defaults to **Private**, since most merchants keep their code private.

### Existing-repo requires its own deploy workflow

The existing-repo path warns *"You may need to add the deployment workflow manually"* — unlike the new-repo path, an existing project may not already contain the GitHub Actions workflow, though repository secrets and variables are still configured automatically.

### Repo-loading failure re-authorises silently

If the repository list fails to load (revoked installation / expired token), the wizard auto-disconnects, re-saves the storefront name, and routes back through the GitHub OAuth flow rather than showing an error — see [[nitrogen-create-storefront-github-connect]].

## Related

- [[nitrogen-create-storefront]] — hub.
- [[nitrogen-create-storefront-github-connect]] — the connection prerequisite for this step.
- [[nitrogen-create-storefront-provisioning]] — the next step that consumes the chosen strategy.

## Open questions

_None._
