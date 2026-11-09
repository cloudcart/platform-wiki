---
type: feature
nav_path: "Design → Nitrogen"
route_name: nitrogen.storefronts
route_path: /admin/nitrogen
aliases: ["Nitrogen Storefronts", "Headless Storefronts list", "Storefronts list", "Nitrogen list", "Nitrogen first page", "Your storefronts", "Endless possibilities for your online store", "Welcome to Nitrogen, vibe coders", "Level complete", "Витрини Nitrogen", "Начална страница на Nitrogen"]
tags: [nitrogen, storefronts, headless, list, staff-permission]
plan_gates: []
created: 2026-05-21
updated: 2026-11-09
source_count: 6
---
# Nitrogen → Storefronts

## Purpose

This is the first page of the Nitrogen (headless storefront) area. With no storefront yet, it introduces Nitrogen and offers to create one. With storefronts, it shows each as a box. From here the merchant creates a storefront or opens one to manage it.

Nitrogen is CloudCart's **headless** layer: an AI agent or the merchant's developers build a storefront from the starter ([[headless-starter]]) and deploy it to Nova, and it reads the store through the Storefront API. See [[headless-storefront]].

## Where to find it

Sidebar → **Дизайн** / **Design** → **Nitrogen**, or **Go to Nitrogen** on the page that **Design** opens ([[design]]). The page has no breadcrumb and no standard header.

| Action | Route name | Path |
|--------|------------|------|
| Storefronts list | `nitrogen.storefronts` | `/admin/nitrogen` |
| Create storefront | `nitrogen.storefront.create` | `/admin/nitrogen/create` |
| Create storefront: repository | `nitrogen.storefront.select-repo` | `/admin/nitrogen/create/repository` |
| Storefront page | `nitrogen.storefront.overview` | `/admin/nitrogen/:storefrontId` |
| Deployments | `nitrogen.deployments` | `/admin/nitrogen/:storefrontId/deployments` |

## What the merchant can do here

### With no storefront yet

The page opens with the Nitrogen logo, a line typed out letter by letter, *"Welcome to Nitrogen, vibe coders"*, the title *"Endless possibilities for your online store"*, and *"Describe the store you want to your AI agent, and it builds it with a design entirely your own. Products, orders and payments stay in CloudCart."* **Create storefront** opens [[nitrogen-create-storefront]].

Beside it, an animated 8-bit picture shows a crew building three shop screens. The shops are made up, not the store's data. For an hour after it has played, the page opens as it was left, as remembered in that browser.

The squares of those shops can be coloured in. With 80% of them coloured, a pop-up reads *"Level complete!"* and *"With Nitrogen, making your own store design is just as easy as colouring in these pictures."*, with **Not now** and **Create storefront**.

Four boxes follow:

| Box | Text |
|---|---|
| **Build with your AI agent** | *"Once your storefront is created, paste one instruction into Claude, ChatGPT, Cursor or another agent, and it sets itself up to build on CloudCart."* |
| **A design entirely your own** | *"Describe the look you want and change it as often as you like, free from the limits of a ready-made theme."* |
| **Everything stays in CloudCart** | *"Products, orders, customers and payments stay where you manage them today."* |
| **Live in one command** | *"One command puts your storefront live on CloudCart's hosting, with no servers to look after."* |

Under them: *"Prefer someone else to build it? Your developer or agency can do it the same way."*

### With storefronts

The top is shorter, with the logo, the title, the text and **Create storefront**. Below it, under **Your storefronts**, each storefront has a box:

| Part | What it shows |
|---|---|
| **Picture** | A browser frame with the storefront's address, holding a screenshot of what is live. Without a screenshot it holds a drawing, and a storefront with nothing deployed reads *"No production deployments yet"*. |
| **Name** | The whole box opens [[nitrogen-storefront-overview]]. |
| **Status** | **Active** or **Paused** for a live or paused storefront. Otherwise the deploy's own word: **Building**, **Deploying**, **Failed** or **Cancelled**. A deploy under way updates by itself. |
| **Source** | The GitHub repository, or **Command line**. |
| **View storefront** | Opens the live storefront. Shown only when it is live. |

### Create a storefront

**Create storefront** opens [[nitrogen-create-storefront]].

### If the list cannot be read

The page reads *"Your storefronts could not be loaded."* with **Try again**.

### What this screen does not do

Deleting, renaming, variables, tokens and domains are on the storefront's page. A storefront is deleted on its **General** tab, where its name has to be typed. Deploys come from GitHub or the CLI, and their history is on [[nitrogen-deployments]].

## Settings & fields

This page has no editable fields. All editing happens on the tabs of [[nitrogen-storefront-overview]]: General, Environments and variables, Deployments, Storefront API, Domains.

## Business rules

### 10 storefronts per site

The platform allows up to 10 Nitrogen storefronts per site, the same on every plan; Nitrogen has no plan gate ([[headless-nitrogen-overview]]). It is not a merchant setting. The merchant deletes a storefront (on its General tab, never from the list) to free a slot. At the cap, **Create storefront** is off and the page says *"You have reached the limit of {max} storefronts."* Below the cap no count is shown. A creation past the cap is refused with *"Maximum of 10 storefronts allowed per site"*.

### Each storefront is isolated

Storefronts on the same site do not share deployment tokens, Storefront API tokens or variables. Only one at a time may serve the store's domains (see [[headless-nova-platform]]).

### All on one page

Every storefront is on this one page, newest first.

### Permission — Nitrogen Storefronts

The Nitrogen screens require the **Nitrogen Storefronts** permission. The store owner always has it. Whoever has it sees the **Design** menu with its **Nitrogen** link. A moderator can list, create, edit or delete storefronts here only when it is granted in [[settings-staff]]. Otherwise the calls get HTTP 403. See [[nitrogen]].

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
