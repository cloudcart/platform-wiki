---
type: feature
nav_path: "Nitrogen → Storefronts → (storefront)"
route_name: nitrogen.storefront.overview
route_path: /admin/nitrogen/:storefrontId, /admin/nitrogen/:storefrontId/general, /admin/nitrogen/:storefrontId/environment, /admin/nitrogen/:storefrontId/nova, /admin/nitrogen/:storefrontId/api, /admin/nitrogen/:storefrontId/domains
aliases: ["Nitrogen storefront page", "Storefront detail", "Storefront settings", "Develop locally", "Production address", "Delete storefront", "Environments and variables", "Deployment tokens", "Storefront API tab", "Domains tab", "Route to this storefront", "Back to the store theme", "Настройки на витрината"]
tags: [nitrogen, storefronts, headless, domains, tokens, staff-permission]
plan_gates: []
created: 2026-05-21
updated: 2026-11-03
source_count: 4
---
# Nitrogen storefront page

## Purpose

This is the page of one Nitrogen storefront. From it the merchant develops and deploys the storefront, renames or deletes it, manages its variables, deployment tokens and Storefront API tokens, and routes a store domain to it.

## Where to find it

Sidebar → **Nitrogen** → a storefront's name on [[nitrogen-storefronts]]. New storefronts open here after [[nitrogen-create-storefront]].

The header shows the storefront's name, its address, an **Active** or **Paused** badge, and the buttons **View storefront** and **All deployments** ([[nitrogen-deployments]]).

## What the merchant can do here

- Copy the commands to develop locally and deploy (**Overview**).
- Rename the storefront, copy its address, delete it (**General**).
- Add and delete custom variables, and read the read-only ones (**Environments and variables**).
- See the deployment source, connect a GitHub account, create and delete deployment tokens (**Deployments**).
- Copy the public token and generate a new private one (**Storefront API**).
- Route a store domain to the storefront, or send it back to the theme (**Domains**).

## Sub-screens

| Tab | Route name | Path |
|-----|------------|------|
| Overview | `nitrogen.storefront.overview` | `/admin/nitrogen/:storefrontId` |
| General | `nitrogen.storefront.general` | `/admin/nitrogen/:storefrontId/general` |
| Environments and variables | `nitrogen.storefront.environment` | `/admin/nitrogen/:storefrontId/environment` |
| Deployments | `nitrogen.storefront.nova` | `/admin/nitrogen/:storefrontId/nova` |
| Storefront API | `nitrogen.storefront.api` | `/admin/nitrogen/:storefrontId/api` |
| Domains | `nitrogen.storefront.domains` | `/admin/nitrogen/:storefrontId/domains` |

The old `/admin/nitrogen/:storefrontId/customer-account` address opens **General**: sign-in by email code needs nothing set up (see [[headless-customer-accounts]]).

## Settings & fields

### Overview

- **Develop locally** — the commands: `npm install -g @cloudcart/cli`; for a GitHub storefront `git clone` and `npm install`, for a command-line one `cloudcart nitrogen init`; then `cloudcart nitrogen link --storefront "<name>"`, `cloudcart nitrogen env pull`, `npm run dev`.
- **Deploy** — on GitHub: *"Every push to the {branch} branch of {repository} deploys to production."* with **View the runs on GitHub**. From the command line: *"Deploy from the command line with a deployment token, set as CLOUDCART_NOVA_TOKEN in.env."* and `cloudcart nitrogen deploy`.
- **Production** (aside) — the current deployment, with **View all**:

| State | What it says |
|---|---|
| Building | *"GitHub Actions is building and deploying your project."* |
| Uploaded, first deploy | *"The storefront is uploaded. Its address can take a few minutes to answer the first time."* |
| Failed, GitHub | *"The build or deployment encountered an error. Push a new commit to try again."* |
| Failed, command line | *"The upload was refused. Run the deploy again."* |
| Nothing deployed | *"No production deployments yet"* |
| Live | The badges **Live** and **Current**, a screenshot, the commit and the address. |

### General

| Field | What it does |
|---|---|
| **Storefront name** | At most 255 characters. *"How the admin and the CLI name this storefront: cloudcart nitrogen link --storefront takes it."* |
| **Production address** | *"Where Nova serves this storefront. A store domain can be routed to it under Domains."* Read-only, with a copy button. |
| **Delete storefront** | *"Removes the storefront from Nova with its address, deployments and tokens. A domain routed to it shows the store's theme again. This can't be undone."* The merchant types the storefront's name to confirm. *"The repository on GitHub is not touched."* |

### Environments and variables

- **Production** — the branch, or *"Deployed from the command line"*, and the address. *"The variables are bound to the storefront when it is deployed: a change takes effect with the next deploy."*
- **Custom variables** — columns **Key**, **Value**, **Environment**. **Add variable** asks for **Key**, **Value**, **Environment** (**All environments** or **Production**) and **Secret** (*"Its value is hidden in the admin once saved."*).
- **Read-only variables** — *"Set by CloudCart for every environment of this storefront."*

Key rules, the names and the limits are on [[headless-environment-variables]].

### Deployments

- **Source** — the repository and branch, or the CLI command.
- **GitHub account** (GitHub storefronts) — *"The admin reads the workflow's runs with it, to show how a deploy goes."* **Connect GitHub** or **Disconnect**.
- **Deployment tokens** — **Create token** asks for a **Token name**. Columns **Name**, **Token**, **Last used**, **Created**, **Active**. Up to 10; rules on [[headless-deployment-methods]].

### Storefront API

- **Public access token** — shown in full with a copy button; the `PUBLIC_STOREFRONT_API_TOKEN` variable. *"Sent with every Storefront API request, from the browser too."* It has no replace button.
- **Private access token** — masked; the `PRIVATE_STOREFRONT_API_TOKEN` variable. *"Sent only from the storefront's server, never to a browser."*
- **Generate new token** asks for confirmation, then shows the new token once. The confirmation warns that a storefront on Nitrogen 2 deployed with the old token is refused until it is deployed again.

The headers and token rules are on [[headless-storefront-api]].

### Domains

*"Route a store domain to this storefront. The admin panel, images, checkout and payment callbacks keep working — they stay on the platform."* Columns **Domain** and **Serves**:

| Serves | Meaning | Action |
|---|---|---|
| **Routed to this storefront** | Visitors of the domain see this storefront. | **Back to the store theme** |
| **Store theme** | The theme serves it, and it can be routed. | **Route to this storefront** |
| **DNS not managed by CloudCart** | *"Move this domain's DNS to CloudCart (Cloudflare) before it can serve the storefront."* | None |
| **CloudCart service domain** | *"This is your CloudCart platform address. The storefront already has its own address on cloudcart.dev."* | None |

## Business rules

### Routing a domain

**Route to this storefront** opens a confirmation listing what keeps working on the same domain, and warns to check that the storefront covers the store's URLs and to deploy again after switching. The refusals, `www.` handling and the variables that change are on [[headless-nova-platform]]. The paths the platform keeps are on [[headless-legacy-vs-nitrogen]].

**Back to the store theme**: *"will be served by the store's theme again. The Nitrogen storefront stays reachable on its own address."*

### A variable change waits for a deploy

Saving or deleting a variable changes nothing on the live storefront until its next deploy. The delete confirmation says so: *"The deployed storefront keeps it until its next deploy."*

### The Nitrogen Storefronts permission is required

Every tab needs the **Nitrogen Storefronts** permission. The store owner always has it; a moderator has it only when it is granted in [[settings-staff]]. Without it the calls are refused with HTTP 403. See [[nitrogen]].

## Related

- [[nitrogen]] — Nitrogen hub.
- [[nitrogen-storefronts]] — the list of storefronts.
- [[nitrogen-deployments]] — deployment history.
- [[headless-storefront]] — the Nitrogen model.
- [[headless-storefront-api]] — endpoint, headers, tokens.
- [[headless-nova-platform]] — hosting, address, routing a domain.
- [[headless-environment-variables]] — variables.
- [[headless-deployment-methods]] — deployment tokens and GitHub.
- [[settings-domains]] — where a domain joins the store.

## Open questions

_None._
