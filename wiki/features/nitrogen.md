---
type: feature
nav_path: "Design → Nitrogen (Headless storefronts)"
route_name: nitrogen
route_path: /admin/nitrogen
aliases: ["Nitrogen", "Headless storefronts", "Nitrogen admin", "Nitrogen page", "Where is Nitrogen", "Design Nitrogen", "Дизайн Nitrogen", "Витрини Nitrogen", "Хедлес магазин", "Къде е Nitrogen", "Страница Nitrogen"]
tags: [nitrogen, hub, staff-permission]
plan_gates: []
created: 2026-05-21
updated: 2026-11-05
source_count: 4
---
# Nitrogen (Headless storefronts)

## Purpose

The **Nitrogen** area of the admin is where a store's own storefront is created, connected, deployed and put on the store's domain. This is where a design of the store's own begins: see [[nitrogen-vs-themes]] for how it compares with a standard theme, and [[headless-starter]] for the starter it is made from and the `cloudcart-nitrogen` skill an agent must use.

The area manages storefronts. It has no design tools: the storefront itself is code, written outside the admin by an AI agent or a developer. Its content comes from the rest of the admin, including metafields and metaobjects ([[metafields-metaobjects]]).

## Where to find it

Sidebar → **Дизайн** / **Design** → **Nitrogen**, the first link of that menu, tagged **new**. The page that **Design** opens leads here too, through **Go to Nitrogen** ([[design]]). The address is `/admin/nitrogen`.

On these pages the Design menu stays open, with **Nitrogen** lit. The first page has no breadcrumb; those after it start at **Nitrogen**.

## The screens

| Screen | Address | Page |
|---|---|---|
| First page: an introduction, or the storefronts | `/admin/nitrogen` | [[nitrogen-storefronts]] |
| Create storefront | `/admin/nitrogen/create` | [[nitrogen-create-storefront]] |
| Create storefront: repository | `/admin/nitrogen/create/repository` | [[nitrogen-create-storefront-repository]] |
| A storefront: **Overview** | `/admin/nitrogen/:storefrontId` | [[nitrogen-storefront-overview]] |
| A storefront: **General** | `/admin/nitrogen/:storefrontId/general` | [[nitrogen-storefront-overview]] |
| A storefront: **Environments and variables** | `/admin/nitrogen/:storefrontId/environment` | [[nitrogen-storefront-overview]] |
| A storefront: **Deployments** | `/admin/nitrogen/:storefrontId/nova` | [[nitrogen-storefront-overview]] |
| A storefront: **Storefront API** | `/admin/nitrogen/:storefrontId/api` | [[nitrogen-storefront-overview]] |
| A storefront: **Domains** | `/admin/nitrogen/:storefrontId/domains` | [[nitrogen-storefront-overview]] |
| Deployment history | `/admin/nitrogen/:storefrontId/deployments` | [[nitrogen-deployments]] |
| One deployment | `/admin/nitrogen/:storefrontId/deployments/:deploymentId` | [[nitrogen-deployments]] |

## What the merchant can do here

**Storefronts**

- With none yet, read what Nitrogen is, on an introduction page.
- See every storefront as a box: a picture of what is live, its address, name, status and source, and a link to view it.
- Create one (up to 10), or open one. Deleting is on a storefront's **General** tab.

**Creating a storefront**

- Name it and choose how it deploys: **GitHub**, marked **Recommended**, or **Command line or CI/CD**. This cannot be changed later.
- On GitHub: connect a GitHub account, then create a new repository from the starter (private or public) or connect an existing one, and follow the setup step by step ([[nitrogen-create-storefront-provisioning]]).
- On the command line: receive one box to copy for an AI agent and, under **Advanced**, the deployment token, shown once, and the commands to run.

**Developing and deploying**

- Copy one instruction for an AI agent, which sets itself up and designs the storefront with the merchant ([[nitrogen-storefront-overview]]).
- Under **Advanced**, copy the commands to develop locally and to deploy.
- See what is live: the screenshot, commit, branch and address, or why the last deploy failed, with links to the build logs on GitHub.
- Read the history of deploys and the details of each.

**Variables**

- Add custom variables, optionally secret, delete them, and copy their values.
- Read the variables CloudCart sets. A change takes effect with the next deploy.

**Tokens and access**

- Create deployment tokens (up to 10), turn them off and on, and delete them.
- Connect or disconnect the GitHub account.
- Copy the public Storefront API token, and generate a new private one.

**Going live**

- Route a store domain to the storefront, and send it back to the store's theme.
- Open the storefront, rename it, copy its address, or delete it.

## What is not here

- **Designing or editing the storefront.** That is code in the project.
- **Deploying, redeploying, rolling back or reading logs.** A deploy starts from a push or from `cloudcart nitrogen deploy`; logs are on GitHub ([[headless-deployment-methods]]).
- **Preview deploys.** Only production is served ([[headless-nova-platform]]).
- **Replacing the public token, or choosing a token's scopes.** The public token has no replace button, and scopes are not shown.
- **Defining metafields and metaobjects.** They are under Settings → Metaobjects ([[metafields-metaobjects]]).
- **Adding a domain to the store.** That is [[settings-domains]]; the **Domains** tab only routes one that is already there.

## Settings & fields

Not applicable: the fields are on the screens above.

## Business rules

### The Nitrogen Storefronts permission

The entire Nitrogen area (`/admin/api/core/nitrogen/*`: storefronts, tokens, deployments, deployment tokens, variables, domains, GitHub connection) requires the **Nitrogen Storefronts** permission, a row of its own in the [[settings-staff]] permission tree. The store owner always has it. Whoever has it sees the **Design** menu with its **Nitrogen** link. A moderator can list, create, edit or delete storefronts and generate tokens only when that permission is ticked for them. Without it, the calls are refused with HTTP 403.

### What an agent can do through the API

The Admin GraphQL API lists storefronts, replaces the private token and sets variables ([[headless-environment-variables]]). Creating a storefront, deleting one, deployment tokens and routing a domain are done on these screens, so an agent asks the merchant to do them.

## Related

- [[nitrogen-vs-themes]] — Nitrogen compared with a standard theme.
- [[headless-starter]] — the starter, and the agent's rule.
- [[metafields-metaobjects]] — the store's own fields and content types, which a Nitrogen storefront shows.
- [[metafields-use-cases]] — what to build with them.
- [[nitrogen-storefronts]] — the list of storefronts.
- [[nitrogen-create-storefront]] — the create wizard.
- [[nitrogen-storefront-overview]] — one storefront's page and tabs.
- [[nitrogen-deployments]] — deployment history.
- [[headless-storefront]] — the Nitrogen model, Nova and the Storefront API.

## Open questions

_None._
