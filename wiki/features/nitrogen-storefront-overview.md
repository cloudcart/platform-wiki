---
type: feature
nav_path: "Nitrogen → Storefronts → (storefront)"
route_name: nitrogen.storefront.overview
route_path: /admin/nitrogen/:storefrontId, /admin/nitrogen/:storefrontId/general, /admin/nitrogen/:storefrontId/environment, /admin/nitrogen/:storefrontId/nova, /admin/nitrogen/:storefrontId/api, /admin/nitrogen/:storefrontId/domains
aliases: ["Nitrogen storefront page", "Storefront detail", "Storefront settings", "Develop locally", "Production address", "Delete storefront", "Environments and variables", "Deployment tokens", "Storefront API tab", "Domains tab", "Route to this storefront", "Back to the store theme", "Настройки на витрината"]
tags: [nitrogen, storefronts, headless, domains, tokens, staff-permission]
plan_gates: []
created: 2026-05-21
updated: 2026-11-04
source_count: 4
---
# Nitrogen storefront page

## Purpose

This is the page of one Nitrogen storefront. From it the merchant develops and deploys the storefront, renames or deletes it, manages its variables, deployment tokens and Storefront API tokens, and routes a store domain to it.

## Where to find it

A storefront's name on [[nitrogen-storefronts]], at `/admin/nitrogen`; the admin's menu has no link to this area ([[nitrogen]]). New storefronts open here after [[nitrogen-create-storefront]].

The header shows the storefront's name, its address, an **Active** or **Paused** badge, and the buttons **View storefront** (once it has an address) and **All deployments** ([[nitrogen-deployments]]).

## What the merchant can do here

- Copy the commands to develop locally and deploy (**Overview**).
- Rename the storefront, copy its address, delete it (**General**).
- Add, delete and copy custom variables, and read the read-only ones (**Environments and variables**).
- See the deployment source, connect or disconnect a GitHub account, create, turn off and on, and delete deployment tokens (**Deployments**).
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

- After creation, a notice reads *"Storefront created and connected to GitHub."* or *"Storefront created."*
- **Develop locally** — the commands: `npm install -g @cloudcart/cli`; for a GitHub storefront `git clone` and `npm install`, for a command-line one `cloudcart nitrogen init`; then `cloudcart nitrogen link --storefront "<name>"`, `cloudcart nitrogen env pull`, `npm run dev`.
- **Deploy** — on GitHub: *"Every push to the {branch} branch of {repository} deploys to production."* with **View the runs on GitHub**. From the command line: *"Deploy from the command line with a deployment token, set as CLOUDCART_NOVA_TOKEN in.env."* and `cloudcart nitrogen deploy`. The card's button, **Deployment settings** or **Deployment tokens**, opens the **Deployments** tab.
- **Production** (aside) — the current deployment, with **View all**:

| State | What it says |
|---|---|
| Building | *"GitHub Actions is building and deploying your project."* with **View build logs** |
| Uploaded, first deploy | *"The storefront is uploaded. Its address can take a few minutes to answer the first time."* |
| Failed, GitHub | *"The build or deployment encountered an error. Push a new commit to try again."* with **View build logs** |
| Failed, command line | *"The upload was refused. Run the deploy again."* |
| Nothing deployed | *"No production deployments yet"*, then *"Push to the {branch} branch to deploy."* or *"Deploy from the command line to get started."* |
| Live | The badges **Live** and **Current**, a screenshot linking to the storefront, the commit message, the branch, the short commit and the address. |

### General

| Field | What it does |
|---|---|
| **Storefront name** | At most 255 characters, with a counter. *"How the admin and the CLI name this storefront: cloudcart nitrogen link --storefront takes it."* **Save** works once the name has changed. |
| **Production address** | *"Where Nova serves this storefront. A store domain can be routed to it under Domains."* Read-only, with a copy button. |
| **Delete storefront** | *"Removes the storefront from Nova with its address, deployments and tokens. A domain routed to it shows the store's theme again. This can't be undone."* The merchant types the storefront's name to confirm. *"The repository on GitHub is not touched."* |

### Environments and variables

- **Production** — the branch, or *"Deployed from the command line"*, and the address. *"The variables are bound to the storefront when it is deployed: a change takes effect with the next deploy."*
- **Custom variables** — *"Your storefront's own settings and keys. A secret's value stays hidden here; cloudcart nitrogen env pull writes it to.env."* Columns **Key**, **Value**, **Environment**, and a delete action. Clicking a value copies it; a secret shows as dots. **Add variable** asks for **Key** (*"Upper-case letters, digits and underscores, starting with a letter."*), **Value**, **Environment** (**All environments** or **Production**) and **Secret** (*"Its value is hidden in the admin once saved."*). Empty: *"No custom variables yet."*
- **Read-only variables** — *"Set by CloudCart for every environment of this storefront."* Those ending in `_TOKEN` or `_SECRET` show as dots.

Key rules, the names and the limits are on [[headless-environment-variables]].

### Deployments

- **Source** — the repository and branch, with *"A push to the production branch builds the storefront on GitHub Actions and deploys it."*; or `cloudcart nitrogen deploy`, with *"The storefront is deployed from the command line, with a deployment token."*
- **GitHub account** (GitHub storefronts) — *"The admin reads the workflow's runs with it, to show how a deploy goes."* Shows *"No GitHub account connected"* with **Connect GitHub**, or the account's name with **Connected** and **Disconnect**. Disconnecting warns: *"Your GitHub account is removed from this admin: it stops reading the workflow's runs for you, and you can't make a storefront from a repository until you connect again. Deploys from GitHub go on: they use the token in the repository's secrets."*
- **Deployment tokens** — **Create token** asks for a **Token name** (at most 100 characters) and shows the new token once. Columns **Name**, **Token**, **Last used**, **Created**, **Active** (a switch that turns the token off and on), and a delete action. Up to 10. On a GitHub storefront, turning off or deleting **Default** stops the deploys from GitHub. Rules on [[headless-deployment-methods]].

### Storefront API

- **Public access token** — shown in full with a copy button; the `PUBLIC_STOREFRONT_API_TOKEN` variable. *"Sent with every Storefront API request, from the browser too."* It has no replace button.
- **Private access token** — masked, or *"Not generated"*; the `PRIVATE_STOREFRONT_API_TOKEN` variable. *"Sent only from the storefront's server, never to a browser."* A link opens **Environments and variables**.
- **Generate new token** asks for confirmation, then shows the new token once. The confirmation warns that a storefront on Nitrogen 2 deployed with the old token is refused until it is deployed again.

The headers and token rules are on [[headless-storefront-api]].

### Domains

*"Route a store domain to this storefront. The admin panel, images, checkout and payment callbacks keep working — they stay on the platform."* Columns **Domain**, with a **Primary** badge on the store's primary domain, and **Serves**. Empty: *"No domains found for this store."*

| Serves | Meaning | Action |
|---|---|---|
| **Routed to this storefront** | Visitors of the domain see this storefront. | **Back to the store theme** |
| **Store theme** | The theme serves it, and it can be routed. | **Route to this storefront** |
| **DNS not managed by CloudCart** | *"Move this domain's DNS to CloudCart (Cloudflare) before it can serve the storefront."* | None |
| **CloudCart service domain** | *"This is your CloudCart platform address. The storefront already has its own address on cloudcart.dev."* | None |

## Business rules

### Routing a domain

**Route to this storefront** opens a confirmation listing what keeps working on the same domain, and warns: *"Make sure the storefront covers your store URLs (products, categories, pages) before switching, and deploy it again after switching so it picks up the new domain."* It also warns about links in the store's e-mails ([[headless-legacy-vs-nitrogen]]). The refusals, `www.` handling and the variables that change are on [[headless-nova-platform]]. The paths the platform keeps are on [[headless-legacy-vs-nitrogen]].

**Back to the store theme**: *"will be served by the store's theme again. The Nitrogen storefront stays reachable on its own address."*

### A variable change waits for a deploy

Saving or deleting a variable changes nothing on the live storefront until its next deploy. The delete confirmation says so: *"The deployed storefront keeps it until its next deploy."*

### The Nitrogen Storefronts permission is required

Every tab needs the **Nitrogen Storefronts** permission. The store owner always has it; a moderator has it only when it is granted in [[settings-staff]]. Without it the calls are refused with HTTP 403. See [[nitrogen]].

## Related

- [[nitrogen]] — Nitrogen hub.
- [[headless-starter]] — the starter the commands on **Overview** work from.
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
