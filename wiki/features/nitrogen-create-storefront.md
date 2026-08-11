---
type: feature
nav_path: "Nitrogen → Storefronts → Create Storefront"
route_name: nitrogen.storefront.create
route_path: /admin/nitrogen/create
aliases: ["Create Nitrogen Storefront", "Create headless storefront", "Nitrogen storefront wizard", "New storefront"]
tags: [nitrogen, storefronts, create, wizard, github, owner-only]
plan_gates: []
created: 2026-05-27
updated: 2026-06-10
source_count: 5
---
# Nitrogen → Create Storefront (multi-step wizard)

## Purpose

The **Create Storefront** wizard is how the merchant provisions a new headless storefront on the Nitrogen layer. The merchant supplies a name, chooses a deployment method (CLI / CI-CD OR GitHub), optionally creates a new GitHub repository from the Nitrogen starter template OR connects an existing repo, watches the provisioning steps complete, and finally lands on the storefront's detail page with API tokens and next-step instructions ready.

The wizard is multi-step:

1. **Setup** — Storefront name + deployment method. The CLI path finishes here. See [[nitrogen-create-storefront-setup]].
2. **GitHub connection** (GitHub path only) — OAuth + GitHub App install, name survives the round-trip. See [[nitrogen-create-storefront-github-connect]].
3. **Repository selection** (GitHub path only) — create a new repo OR pick an existing one. See [[nitrogen-create-storefront-repository]].
4. **Provisioning + success** — live progress display, then redirect to the storefront detail (GitHub) or a deploy-token success card (CLI). See [[nitrogen-create-storefront-provisioning]].

This is a hub page — drill into the aspect that matches the question.

## Where to find it

From the storefronts list ([[nitrogen-storefronts]]), click **Create Storefront** (top-right). Route name `nitrogen.storefront.create`, path `/admin/nitrogen/create`.

The wizard spans two route names:

| Step | Route name | Path |
|------|------------|------|
| Setup (name + method) and CLI success | `nitrogen.storefront.create` | `/admin/nitrogen/create` |
| Repository selection + provisioning + GitHub success | `nitrogen.storefront.select-repo` | `/admin/nitrogen/create/repository` |

Both routes render inside the settings wrapper with the rocket icon (`far fa-rocket`).

## What the merchant can do here

- **Name the storefront** and pick a deployment method (CLI / CI-CD or GitHub) — see [[nitrogen-create-storefront-setup]].
- **Take the CLI path** — create the storefront immediately, receive a one-time deploy token + three CLI commands, skip all repo steps — see [[nitrogen-create-storefront-setup]].
- **Connect a GitHub account** via OAuth + the CloudCart Nitrogen GitHub App, or disconnect / switch accounts — see [[nitrogen-create-storefront-github-connect]].
- **Create a new GitHub repo** from the `cloudcart/nitrogen-starter` template (choose name + Private/Public visibility), OR **connect an existing repo** from a searchable list — see [[nitrogen-create-storefront-repository]].
- **Watch provisioning** complete step-by-step, retry a failed step, and land on the new storefront's detail page — see [[nitrogen-create-storefront-provisioning]].

### What the merchant CANNOT do here

- Pick a non-GitHub Git provider for auto-deploy — only GitHub is supported (GitLab / Bitbucket / self-hosted require the CLI / CI-CD path).
- Pick which starter template to clone — the new-repo path always uses `cloudcart/nitrogen-starter`; a custom starter requires the existing-repo path.
- Pre-set environment variables — env vars are set in the storefront's Environment tab AFTER provisioning.
- Customise the Nova hostname — the platform generates a slug from the name.
- Connect more than one GitHub account on the same admin user — disconnect first to switch.

## Settings & fields

The wizard's combined payload to `POST /admin/api/core/nitrogen/storefronts` is:

| Field | Required | Notes |
|-------|----------|-------|
| **`name`** | Yes | `string, max:255`. Empty rejected client + server side. |
| **`deployment_method`** | No (defaults to `cli`) | `in:cli,github`. |
| **`repository`** | No | Full GitHub name `owner/repo`. Only sent in GitHub path. |
| **`branch`** | No | Default branch — `main` for new repos, repo's `default_branch` for existing. |
| **`is_new_repo`** | No | `boolean`. `true` for the create-new path, `false` for the existing-repo path. |

Per-field validation and the exact server rules live on the aspect pages: name/method on [[nitrogen-create-storefront-setup]]; repository/branch/is_new_repo on [[nitrogen-create-storefront-repository]] and [[nitrogen-create-storefront-provisioning]].

## Business rules

- **Owner-only.** The Create action is inside the pillar's `isOwner` group — **only the store owner can run this wizard**. Moderators cannot reach it (the sidebar entry is hidden; direct API calls are rejected with HTTP 403). There is no separate `nitrogen.create` row in [[settings-staff]] to delegate; the gate is binary. See [[nitrogen]] for the pillar-wide owner-only rule.
- **Max 10 storefronts per site.** The `max_storefronts_per_site` cap (default 10) is enforced before the storefront is created, on top of the owner check. The list endpoint exposes the same value via `meta.max_storefronts`.
- **GitHub via App, not personal tokens.** The integration uses the CloudCart Nitrogen GitHub App. Detail on [[nitrogen-create-storefront-github-connect]].
- **CLI path skips the repo steps.** Picking CLI / CI-CD goes from step 1 straight to the success card with a deploy token shown once. Detail on [[nitrogen-create-storefront-setup]].
- **Starter template is fixed: `cloudcart/nitrogen-starter`.** The new-repo path always clones it. Detail on [[nitrogen-create-storefront-repository]].

## Sub-pages (in this cluster)

- [[nitrogen-create-storefront-setup]] — Step 1: name + deployment-method picker; the CLI direct path; the one-time deploy token + three CLI commands on the success card.
- [[nitrogen-create-storefront-github-connect]] — GitHub OAuth + App-install flow; name persistence through the off-domain round-trip; the `?github=connected` return signal; disconnect; auto-redo on token failure.
- [[nitrogen-create-storefront-repository]] — Step 2: create-a-new-repo (template, name, visibility) vs connect-an-existing-repo (search, list, selection); the GitHub account card.
- [[nitrogen-create-storefront-provisioning]] — Step 3: the sequential provisioning steps (create-new vs connect-existing), progress bar, per-step failure + Retry, success redirect to the storefront detail.

## Related

- [[nitrogen]] — Nitrogen pillar hub.
- [[nitrogen-storefronts]] — Storefronts list (parent of this wizard).
- [[nitrogen-storefront-overview]] — Per-storefront detail page (where the merchant lands after success).
- [[nitrogen-deployments]] — Deployments tab on the storefront detail.
- [[settings-staff]] — staff roles (no delegation row exists for this owner-only wizard).

## Open questions

_None — wizard fully documented across the four aspect pages._
