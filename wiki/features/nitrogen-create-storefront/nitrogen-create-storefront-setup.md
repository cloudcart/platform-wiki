---
type: feature
nav_path: "Design → Nitrogen → Create Storefront → Setup"
route_name: nitrogen.storefront.create
route_path: /admin/nitrogen/create
aliases: ["Create Storefront step 1", "Nitrogen storefront setup step", "Nitrogen CLI deploy path", "Nitrogen deploy token", "Deployment token", "Command line or CI/CD"]
tags: [nitrogen, storefronts, create, wizard, cli, deploy-token]
plan_gates: []
created: 2026-06-10
updated: 2026-11-05
source_count: 5
---
# Nitrogen → Create Storefront — Setup step + CLI path

> Part of [[nitrogen-create-storefront]]. See the hub for the other aspects (GitHub connection, repository selection, provisioning).

## Purpose

This is **Step 1** of the Create Storefront wizard: the merchant names the storefront and picks a deployment method. With **Command line or CI/CD** the wizard finishes here: the storefront is created at once, and a result page hands over one box to copy for an AI agent and, under **Advanced**, a one-time deployment token and the commands to start. With **GitHub**, this step collects the name and hands off to [[nitrogen-create-storefront-github-connect]].

## Where to find it

Route name `nitrogen.storefront.create`, path `/admin/nitrogen/create`. Reached from the **Create storefront** button on the storefronts list ([[nitrogen-storefronts]]). The header reads "Create Nitrogen storefront".

## What the merchant can do here

- Type a **Storefront name** (focused when the page opens).
- Pick a deployment method: **GitHub** or **Command line or CI/CD**.
- **Cancel** returns to the storefronts list.
- Click **Next** (GitHub) or **Create storefront** (command line): the primary button's label changes with the method.
- On the command-line result page: copy the instruction for an AI agent, open **Advanced** for the **deployment token** and the next steps, and click **Go to storefront**.

## Settings & fields

### Step 1 inputs

| Field | What it controls | Validation |
|-------|-----------------|------------|
| **Storefront name** | The name in the list and in `cloudcart nitrogen link --storefront`. Placeholder: *"e.g. My Headless Store"*. | Required, at most 255 characters. Empty disables the primary button. |
| **How do you want to deploy?** | Two option cards: **GitHub**, badged **Recommended** (*"Automatically deploy on every push to your GitHub repository."*) and **Command line or CI/CD** (*"Deploy with the CloudCart CLI or your own pipeline, with a deployment token."*). | Default: **GitHub**. |

### Command-line result page

After a successful creation, on the same address:

- The header reads *"Storefront created"*.
- **Copy this and give it to your AI agent**: the same box as on [[nitrogen-storefront-overview]], and the copied text carries the deployment token.
- **Advanced** slides open two cards.
- **Deployment token** card: the token with a copy button and the one-time warning, then *"Set it as CLOUDCART_NOVA_TOKEN in the project's.env."*
- **Next steps** card, ending with *"The storefront answers on its address after the first deploy."*:
  - `npm install -g @cloudcart/cli`
  - `cloudcart nitrogen init`, `cloudcart nitrogen link --storefront "<name>"`, `cloudcart nitrogen env pull`, `npm run dev`
  - `cloudcart nitrogen deploy`
- **Go to storefront** opens the storefront's page ([[nitrogen-storefront-overview]]).

## Business rules

### The command-line path skips the repository step

There is no repository to choose, because the merchant deploys with the CLI and the token. On an error, a message appears under the form: the platform's own, or *"Failed to create storefront"*.

### The deployment token is shown once

This page is the only time the **Default** token is displayed in full, and the only time the copied instruction carries it. A token that is lost cannot be shown again: create a new one on the storefront's **Deployments** tab, and delete or turn off the lost one. Tokens are created and deleted, not rotated. See [[headless-deployment-methods]].

### Default method is GitHub

The picker starts on **GitHub**, so the primary button first reads **Next**. On GitHub, **Next** checks the connection and opens the repository step, or GitHub's own sign-in first.

### Name is required

An empty or spaces-only name disables the primary button, and the server applies the same rule.

## Related

- [[nitrogen-create-storefront]] — hub.
- [[nitrogen-create-storefront-github-connect]] — the GitHub-path next step (when method = `github`).
- [[nitrogen-storefront-overview]] — the storefront's page, reached by **Go to storefront**.
- [[nitrogen-deployments]] — where deploys appear after `cloudcart nitrogen deploy`.

## Open questions

_None._
