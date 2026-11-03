---
type: concept
nav_path: "Concept → Headless storefronts → Deployment methods"
aliases: ["Nitrogen deployment methods", "CLI deployment", "GitHub deployment", "GitHub App Nova", "cloudcart nitrogen deploy", "Deploy token", "Deployment tokens", "CLOUDCART_NOVA_TOKEN", "NOVA_DEPLOY_TOKEN", "NOVA_DEPLOY_URL", "nova-deploy.yml", "Deploy to Nova"]
tags: [nitrogen, headless, deployment, cli, github, ci-cd, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 6
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, Nova platform, Storefront API, customer accounts, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — deployment methods

## Definition

Every Nitrogen storefront is locked at creation to one of two deployment methods:

- **Command line or CI/CD** — the merchant runs `cloudcart nitrogen deploy` from their machine or their own pipeline, with a deployment token.
- **GitHub** — every push to the repository's default branch builds on GitHub Actions and deploys to production.

The method cannot be changed later: the storefront's update takes only its name. To switch, delete the storefront and create a new one; its tokens, variables and deployment history go with it.

## Scope

Covered:

- The command-line flow and its commands.
- The GitHub flow: what is written to the repository, the workflow's steps, new versus existing repositories.
- Deployment tokens (separate from Storefront API tokens).
- The GitHub account row.

Not covered:

- Hosting — see [[headless-nova-platform]].
- The Storefront API tokens the deployed app uses — see [[headless-storefront-api]].
- Variables — see [[headless-environment-variables]].

## Contrasts

- **Command line vs GitHub** — the command line suits a merchant's own pipeline; GitHub deploys on push with nothing else to run.
- **Deployment tokens vs Storefront API tokens** — a deployment token authenticates the deploy. A Storefront API token authenticates the deployed app's calls to CloudCart. Different tabs on [[nitrogen-storefront-overview]]: **Deployments** and **Storefront API**.
- **Build vs deploy** — a pull request is built only. A push to the default branch is built and deployed.

## Where it applies

### Command line or CI/CD

The merchant installs the CLI with `npm install -g @cloudcart/cli`, gets a **deployment token** (shown once, on the page that creates the storefront), and sets it as `CLOUDCART_NOVA_TOKEN` in the project's `.env`. The admin's next steps:

- `cloudcart nitrogen init` — create the project from the CloudCart starter.
- `cloudcart nitrogen link --storefront "<name>"` — link it to this storefront.
- `cloudcart nitrogen env pull` — write the storefront's variables to `.env`.
- `npm run dev` — start it locally.
- `cloudcart nitrogen deploy` — build and deploy to production.

`cloudcart nitrogen env push` sends a local `.env`'s custom variables up (see [[headless-environment-variables]]).

### GitHub: what is written to the repository

Through the CloudCart GitHub App, the platform writes exactly:

- one secret, `NOVA_DEPLOY_TOKEN`: the storefront's **Default** deployment token;
- one variable, `NOVA_DEPLOY_URL`: `https://<store domain>/admin/api/core/nitrogen/nova`;
- one workflow, `.github/workflows/nova-deploy.yml`, named **Deploy to Nova**.

No hosting credential and no storefront variable or secret is placed in the repository. The platform binds the variables at deploy.

### The workflow

It runs on a push to the default branch, and on pull requests (opened, synchronize, reopened). Its steps:

1. Checkout.
2. **Check if Nitrogen project**: without a `package.json` every later step is skipped, so the workflow is safe in a repository that holds no project yet.
3. Set up Node, `npm ci`, `npx react-router build`.
4. **Deploy to Nova**, on a push only: a manifest of `build/client`, an upload session, a direct upload of the assets still missing, then the worker bundle.
5. **Report failure**, on a push only.

A pull request runs the install and the build, to check it. The pull request's text says: *"Pull requests are built to check them; nothing is deployed until they are merged."* The commit message and branch on a deployment come from the push.

**A repository already connected keeps its copy of the workflow.** Until the merchant replaces that file, an older repository runs the older steps, including deploying a pull request to production.

### New repository vs existing repository

- **New repository:** the workflow is committed straight to the default branch, which starts the first build.
- **Existing repository:** the platform opens a pull request, *"Add Nova deployment workflow"*, from the branch `nova/add-deployment-workflow`. The first deploy runs after it is merged.

See [[nitrogen-create-storefront-repository]] for the screen.

### Deployment tokens

The **Deployments** tab on [[nitrogen-storefront-overview]] lists them: **Name**, **Token**, **Last used**, **Created**, and an **Active** toggle. The first, named **Default**, is made with the storefront. The merchant may create up to 10 (*"Maximum of 10 deployment tokens allowed per storefront"*), for example one per pipeline.

A token is shown once, with *"Copy this value now. You won't be able to see it again."* A lost token cannot be shown again: create a new one, and delete or turn off the lost one.

On a GitHub storefront, the **Default** token is the repository's `NOVA_DEPLOY_TOKEN`, so turning it off or deleting it stops the deploys from GitHub. Deleting any token warns: *"Delete this token? A deploy that uses it — the CLI's, or the GitHub workflow's with Default — is refused from now on."*

### The GitHub account

The **GitHub account** row on the Deployments tab appears on a GitHub storefront: *"The admin reads the workflow's runs with it, to show how a deploy goes."* The connection renews itself when GitHub's token expires. If the merchant disconnects it, or it stops working:

- deploys from GitHub go on, because they use the token in the repository's secrets;
- the admin stops reading the workflow's runs for that admin;
- no new storefront can be made from a repository until GitHub is connected again.

## Related

- [[headless-storefront]] — hub.
- [[headless-storefront-api]] — Storefront API tokens (the other token surface).
- [[headless-nova-platform]] — where a deploy lands.
- [[headless-environment-variables]] — what is bound at deploy.
- [[nitrogen-create-storefront]] — the wizard where the method is chosen.
- [[nitrogen-storefront-overview]] — the Deployments tab.
- [[nitrogen-deployments]] — the deployment history.

## Open Questions

_None._
