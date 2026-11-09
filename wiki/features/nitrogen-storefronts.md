---
type: feature
nav_path: "Nitrogen → Storefronts"
route_name: nitrogen.storefronts
route_path: /admin/nitrogen
aliases: ["Nitrogen Storefronts", "Headless Storefronts list", "Storefronts list", "Nitrogen list", "Витрини Nitrogen"]
tags: [nitrogen, storefronts, headless, list, staff-permission]
plan_gates: []
created: 2026-05-21
updated: 2026-11-09
source_count: 6
---
# Nitrogen → Storefronts (list)

## Purpose

The **Storefronts list** is the landing screen of the Nitrogen (headless storefront) area. It shows every Nitrogen storefront the merchant has created on this site, with each row's name and address, deployment source, status and creation date. From here the merchant creates a storefront, opens one to manage it, or deletes one.

Nitrogen is CloudCart's **headless** layer: an AI agent or the merchant's developers build a storefront from the starter ([[headless-starter]]) and deploy it to Nova, and it reads the store through the Storefront API. See [[headless-storefront]].

## Where to find it

Open the address `/admin/nitrogen`: the admin's menu has no link to this area ([[nitrogen]]). Breadcrumb **Nitrogen → Storefronts**. The header reads "Nitrogen Storefronts", with the description *"Create and manage your headless storefronts. Each storefront gets its own API tokens and environment configuration."*

| Action | Route name | Path |
|--------|------------|------|
| Storefronts list | `nitrogen.storefronts` | `/admin/nitrogen` |
| Create storefront | `nitrogen.storefront.create` | `/admin/nitrogen/create` |
| Create storefront: repository | `nitrogen.storefront.select-repo` | `/admin/nitrogen/create/repository` |
| Storefront page | `nitrogen.storefront.overview` | `/admin/nitrogen/:storefrontId` |
| Deployments | `nitrogen.deployments` | `/admin/nitrogen/:storefrontId/deployments` |

## What the merchant can do here

### See the storefronts

| Column | What it shows |
|--------|---------------|
| **Storefront** | The name, which opens [[nitrogen-storefront-overview]], and its address. |
| **Source** | The GitHub repository, or **Command line**. |
| **Status** | **Active** or **Paused**. Storefronts are created Active and no admin action pauses them; a Paused one cannot be given a domain. |
| **Created** | Creation date. |
| (delete) | A delete action on each row. |

The header shows the counter `Storefronts: {total} / {max}`. **Create storefront** is disabled once the cap of 10 is reached.

### Create a storefront

**Create storefront** opens [[nitrogen-create-storefront]].

### Delete a storefront

A row's delete action confirms: *"Delete this storefront? It is removed from Nova with its address, deployments and tokens, and a domain routed to it shows the store's theme again."* On success the toast reads *"Storefront deleted successfully"*. The repository on GitHub is not touched. See [[headless-nova-platform]].

### The empty state

With no storefronts the table reads **"No storefronts yet"** and *"Create your first Nitrogen storefront to get started with headless commerce."*, with a **Create storefront** button.

### What this screen does not do

Storefronts are deleted one at a time. Renaming, variables, tokens and domains are on the storefront's page. Deploys come from GitHub or the CLI, and their history is on [[nitrogen-deployments]].

## Settings & fields

This is a list: no editable fields on a row. All editing happens on the tabs of [[nitrogen-storefront-overview]]: General, Environments and variables, Deployments, Storefront API, Domains.

## Business rules

### 10 storefronts per site

The platform allows up to 10 Nitrogen storefronts per site, the same on every plan; Nitrogen has no plan gate ([[headless-nitrogen-overview]]). It is not a merchant setting. The merchant deletes a storefront to free a slot. A creation past the cap is refused with *"Maximum of 10 storefronts allowed per site"*.

### Each storefront is isolated

Storefronts on the same site do not share deployment tokens, Storefront API tokens or variables. Only one at a time may serve the store's domains (see [[headless-nova-platform]]).

### The list is paginated

The page number stays in the address, so a bookmarked `/admin/nitrogen?page=2` opens the same page. Order: newest first.

### Permission — Nitrogen Storefronts

The Nitrogen screens require the **Nitrogen Storefronts** permission. The store owner always has it; a moderator can list, create, edit or delete storefronts here only when it is granted in [[settings-staff]]. Otherwise the calls get HTTP 403. See [[nitrogen]].

### Validation on creation

**Storefront name** is required, at most 255 characters. See [[nitrogen-create-storefront-setup]].

## Related

- [[nitrogen]] — Nitrogen pillar hub.
- [[nitrogen-create-storefront]] — the create wizard.
- [[nitrogen-storefront-overview]] — the storefront's page and tabs.
- [[nitrogen-deployments]] — deployment history.
- [[headless-storefront]] — the Nitrogen model.

## Open questions

_None._
