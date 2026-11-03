---
type: feature
nav_path: "Nitrogen → Storefronts → (storefront) → All deployments"
route_name: nitrogen.deployments
route_path: /admin/nitrogen/:storefrontId/deployments, /admin/nitrogen/:storefrontId/deployments/:deploymentId
aliases: ["Nitrogen deployments", "Deployment history", "Deployment status", "Nova deployments", "Failed deployment", "История на деплойментите"]
tags: [nitrogen, deployments, staff-permission]
plan_gates: []
created: 2026-05-21
updated: 2026-11-03
source_count: 3
---
# Deployments

## Purpose

The history of a Nitrogen storefront's deploys, and the details of each. The merchant uses it to see what is live, whether the last deploy worked, and which commit it came from.

## Where to find it

On the storefront's page ([[nitrogen-storefront-overview]]), click **All deployments** in the header, or **View all** on the **Production** card.

## What the merchant can do here

- Read the list of deploys, newest first, and see which one is **Current**.
- Open a deploy for its details.
- Follow the links to the commit and to the workflow's runs on GitHub.

Deploys start from a push or from `cloudcart nitrogen deploy`: these screens have no button that deploys, redeploys, rolls back or shows logs. Build logs are on GitHub, through **View on GitHub** and **View build logs**. See [[headless-deployment-methods]].

## Sub-screens

| Label | Route name | Route path |
|-------|------------|------------|
| Deployments list | `nitrogen.deployments` | `/admin/nitrogen/:storefrontId/deployments` |
| Deployment details | `nitrogen.deployment.detail` | `/admin/nitrogen/:storefrontId/deployments/:deploymentId` |

## Settings & fields

### List

Columns **Deployment** (with the **Current** badge on the live one), **Status**, **Commit**, **Started**. Empty: *"No deployments yet"*, *"A deploy from GitHub or the command line shows here."*

### Details

- Header: the commit message, the start date, *Deployment #{id}*, and **Current** when it is the live one.
- **Deployment** card: **Status**, **Environment**, **Deployment URL**.
- **Build details** card: **Source** (the short commit with a link, and the branch; or *"Deployed from the command line"*), **Workflow** (**View on GitHub**), **Duration**.

### Statuses

| Status | Meaning |
|---|---|
| **Pending** | Waiting to start. |
| **Building** | GitHub Actions is building it. |
| **Deploying** | Uploaded; a first deploy waits for its address to answer. |
| **Live** | Serving visitors. |
| **Failed** | The build or the upload failed. |
| **Cancelled** | Cancelled before it finished. |

## Business rules

### One row per deploy

A deploy has one row in the history, updated as it moves on:

- A deploy uploaded where the environment already served one is **Live** at once, since the upload replaces the worker.
- A first deploy stays **Deploying** until the status check sees its address answer, and then that same row turns **Live**. The address can take a few minutes.
- A failure report from GitHub takes the row of its commit when there is one.

### Commit and branch come from the push

A deploy records the commit and the branch that the push or the CLI sent, not who pushed. A deploy from the command line may have neither.

### Only production

Only production is served, so every deploy that shows as live is the storefront's production. See [[headless-nova-platform]].

### The Nitrogen Storefronts permission is required

The list and the details need the **Nitrogen Storefronts** permission: the store owner always has it, a moderator only when it is granted in [[settings-staff]]. Without it, the calls get HTTP 403. See [[nitrogen]].

## Related

- [[nitrogen]] — Nitrogen hub.
- [[nitrogen-storefront-overview]] — the storefront's page, and its Production card.
- [[headless-deployment-methods]] — how a deploy starts.
- [[headless-nova-platform]] — where it lands.

## Open questions

_None._
