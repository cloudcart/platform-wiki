---
type: concept
nav_path: "Concept → Headless storefronts → Deployment methods"
aliases: ["Nitrogen deployment methods", "CLI deployment", "GitHub deployment", "GitHub App Nova", "cloudcart nitrogen deploy", "Deploy token", "Nova deploy tokens", "GitHub Connection"]
tags: [nitrogen, headless, deployment, cli, github, ci-cd, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, Nova platform, Storefront API, customer accounts, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — deployment methods

## Definition

Every Nitrogen storefront is locked at creation time to ONE of two deployment methods:

- **CLI / CI-CD mode** — the merchant runs `cloudcart nitrogen deploy` from their machine or their own pipeline.
- **GitHub mode** — the CloudCart Nova GitHub App pushes builds automatically on every git push to the default branch.

The choice is stored as `deployment_method` on the storefront record at creation and **cannot be changed** later — the storefront update endpoint only edits the `name`. To switch from CLI to GitHub (or vice versa), the merchant deletes the existing Nitrogen storefront and creates a new one with the other method.

## Scope

Covered:

- The CLI / CI-CD flow and the three example commands.
- The GitHub flow — GitHub App, repo secrets, repo variables, workflow YAML.
- The new-repo vs existing-repo PR-vs-direct-commit decision.
- The non-Nitrogen-project skip step in the workflow.
- Nova deployment tokens (separate from Storefront API tokens).
- GitHub access-token / refresh-token rotation.

Not covered:

- The actual Cloudflare Worker runtime — see [[headless-nova-platform]].
- The Storefront API tokens the deployed app uses to call CloudCart — see [[headless-storefront-api]].
- Env vars pushed into the build — see [[headless-environment-variables]].

## Contrasts

- **CLI mode vs GitHub mode** — CLI is for merchants running their own pipeline; GitHub is fully managed with auto-deploy on push. Each storefront locks to its initial choice.
- **Nova deploy tokens vs Storefront API tokens** — Nova deploy tokens authenticate the DEPLOY COMMAND'S calls to Nova itself (push a build). Storefront API tokens authenticate the DEPLOYED APP'S calls TO CloudCart (read products, write cart). Different tabs, different rotation rules, different scopes. See [[headless-storefront-api]] for the API-token side.
- **GitHub App vs OAuth personal token** — Nitrogen uses a **GitHub App** scoped to one repo with limited permissions, NOT a personal access token. The merchant can revoke the app's access from GitHub's settings at any time.

## Where it applies

### CLI / CI-CD mode

The merchant gets a **Nova deploy token** (shown once at creation, never retrievable again). They paste it into their local environment or their CI/CD pipeline's secrets (GitHub Actions, GitLab CI, CircleCI, custom Jenkins, etc.) and run `cloudcart nitrogen deploy` to push a build to Nova. The CLI is a standalone tool the merchant installs locally (`npm install -g @cloudcart/cli` (verify) or similar).

Three sample commands shown after creation:

- `cloudcart nitrogen link` — connect a local project folder to the storefront.
- `cloudcart nitrogen env pull` — download environment variables into a local `.env` file.
- `cloudcart nitrogen deploy` — build the project and deploy to Nova.

### GitHub mode — writes secrets AND a workflow YAML

When the merchant chooses GitHub mode, they install the **CloudCart Nova GitHub App** on a specific repository. CloudCart then writes the following via the GitHub App:

**Repo SECRETS:**

- `NOVA_CF_API_TOKEN`
- `NOVA_CF_ACCOUNT_ID`
- `NOVA_DEPLOY_TOKEN`
- `NOVA_DEPLOY_CALLBACK_URL` — the merchant's domain + `/api/core/nitrogen/nova/deploy/report`
- Every Storefront API env var (public token, store domain, etc.)
- A freshly-generated `SESSION_SECRET` (see [[headless-environment-variables]] for why this one is never rotated).

**Repo VARIABLES (non-secret):**

- `NOVA_WORKER_NAME` (`store-{handle}`)
- `NOVA_CF_NAMESPACE`
- `NOVA_CF_KV_NAMESPACE_ID`

**Workflow file** — `.github/workflows/cloudcart-nitrogen.yml` (or similar) is a multi-step GitHub Actions workflow that:

1. Checks for `package.json` (skip-step — see below).
2. Runs `npm ci` + `npx react-router build` (verify; framework-dependent).
3. Uploads each file in `build/client/` to Cloudflare KV with correct content-type.
4. Deploys the Worker.

Triggered on push to default branch + PR `open` / `sync` / `reopen`.

### New-repo vs existing-repo — direct commit vs PR

- **On NEW repos** (the merchant created the repo just for this Nitrogen project): the workflow is committed directly to the default branch, which immediately fires the first build.
- **On EXISTING repos** (the merchant already has code in the repo): the platform opens a Pull Request the merchant must review + merge before the first deploy runs.

The PR-vs-direct-commit decision is the `isNewRepo` flag at creation time (verify).

### Workflow includes a non-Nitrogen-project skip

The Actions workflow's FIRST step checks for `package.json`. If missing, every subsequent step is skipped — so the workflow is safe to commit to a repo that doesn't actually contain a Nitrogen project. This is how the platform onboards the workflow into the merchant's existing repo without breaking other CI.

### Deployments are signed as `cloudcart[bot]`

GitHub-mode deployments show up in the deployment history with a `cloudcart[bot] pushed commit <sha>` signature. The deployment row records commit SHA, commit message, branch, environment (production vs preview), status, started/finished timestamps, and a deployed URL — see [[nitrogen-deployments]].

### Nova deployment tokens — separate from Storefront API tokens

The Nova tab on [[nitrogen-storefront-overview]] exposes **Deployment Tokens** — these authenticate the CLI / CI-CD process when pushing a build to Nova. The first deploy token is created automatically when the storefront is created (named "Default"). The merchant can create up to `limits.max_nova_tokens_per_storefront` (default 10 — see [[headless-nitrogen-overview]]) named tokens for granular revocation (e.g., one per CI pipeline, or per developer machine).

Each token is shown ONCE on creation with a *"Copy this token now. You won't be able to see it again."* warning. The platform stores only a SHA-256 hash plus a 15-character prefix for masked display — if the merchant loses the raw value, the only recovery is to regenerate.

### Refresh-token rotation handles GitHub access-token expiry automatically

The GitHub connection model casts both `access_token` and `refresh_token` to the application framework's `encrypted` cast — they're encrypted at rest (verify column names). The platform has an `isTokenExpired` check + `refreshUserToken` method that uses the refresh token to mint a new access token when GitHub's 8-hour token expires.

If the refresh token itself fails (revoked / expired), deployments stop until the merchant reconnects via the **GitHub Connection** card on the Nova tab of [[nitrogen-storefront-overview]].

### Deployment method is immutable

The storefront update endpoint accepts the `name` field only. `deployment_method` is set at creation and never changes. Workflow:

- Switching CLI → GitHub → delete the existing storefront, create new one. Tokens, env vars, deployment history all gone.
- Switching GitHub → CLI → same — delete + recreate.

## Related

- [[headless-storefront]] — hub.
- [[headless-storefront-api]] — Storefront API tokens (the OTHER token surface).
- [[headless-nova-platform]] — where the deploy command actually lands (Cloudflare Workers).
- [[headless-environment-variables]] — env vars the workflow injects into the build.
- [[nitrogen-create-storefront]] — creation wizard where deployment method is chosen.
- [[nitrogen-storefront-overview]] — Nova tab (deploy tokens) + GitHub Connection card.
- [[nitrogen-deployments]] — deployment history.

## Open Questions

- Exact build command per supported framework (`npx react-router build` is verified for the React Router starter — other framework starters may differ).
- Default name of the workflow file is `cloudcart-nitrogen.yml` (verify against current GitHub App code).
- Confirm `isNewRepo` heuristic — likely "repo has zero commits" but verify.
