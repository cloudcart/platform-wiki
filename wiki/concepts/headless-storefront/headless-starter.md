---
type: concept
nav_path: "Concept → Headless storefronts → The starter"
aliases: ["Nitrogen starter", "Starter theme", "Nitrogen starter theme", "Nitrogen template", "nitro-starter", "cloudcart/nitro-starter", "cloudcart nitrogen init", "Start a Nitrogen storefront", "cloudcart-nitrogen skill", "Nitrogen skill", "Стартираща тема", "Начална тема", "Стартова тема", "Nitrogen стартер", "Започни с Nitrogen", "Скил за Nitrogen"]
tags: [nitrogen, headless, starter, ai, concepts]
plan_gates: []
created: 2026-11-04
updated: 2026-11-04
source_count: 4
---

> Part of [[headless-storefront]]. Choosing between Nitrogen and a theme is on [[nitrogen-vs-themes]].

# Headless — the Nitrogen starter

## Definition

The **starter** is CloudCart's public template, `cloudcart/nitro-starter`: a working storefront for a CloudCart store, with its pages, components and queries already built. A merchant who chooses Nitrogen does not begin with an empty project. A new storefront begins as a copy of the starter, and the design is made on top of it.

> **An agent must use the `cloudcart-nitrogen` skill** to build or change a storefront made from the starter, before the first line of code.

## Scope

### The agent's rule

- **Claude Code, Cursor, Gemini CLI and VS Code** have the skill with the CloudCart plugin ([[ai-agent-toolkit]]).
- **Claude Desktop, OpenAI Codex and other MCP clients** do not install it. They read it from the toolkit first: `https://raw.githubusercontent.com/cloudcart/ai-toolkit/main/skills/cloudcart-nitrogen/SKILL.md`, and the files in its `references/` folder beside it.
- **The Storefront MCP** is needed as well. An agent set up as *Manage my store* adds the build profile first.

The skill works in five stages: the store and its design, the build, SEO and security, analytics and the merchant's pixels, and a review of the whole site, including a mobile speed score of 90 or more. Its rule for the design is to build on the starter, never over it: through the design tokens and the existing components, not through a second copy of them. It pushes and deploys only when the merchant says so, because a deploy changes the live storefront.

### What it holds

| Area | Pages |
|---|---|
| **Catalogue** | Home, product (variants, bundles, customizations, reviews, fast order, back in stock, questions), categories with filters and sorting, smart collections, all products, brands, tags, search with results as you type, comparison (off by default) |
| **Buying** | Cart with cross-sell and up-sell offers. Checkout and payment stay the platform's |
| **Content** | CMS pages and policies, blog with categories and tags, physical stores, contact form |
| **Customer account** | Sign-in by e-mail code, registration, profile, orders, returns, addresses, wishlist, downloads, payments |
| **Other** | Returning items and tracking a return, data requests, `/robots.txt`, `/llms.txt` |

The addresses are the store's own, so links, bookmarks and search results keep working when a store moves to the storefront.

### What it is built on

React Router 7, Vite, TypeScript and Tailwind CSS 4, with `@cloudcart/nitrogen` and `@cloudcart/nitrogen-react`, on Node.js 22 or 24. The look is set in the design tokens and the components under the theme templates.

### Starting from it

- **With GitHub:** the admin's wizard creates a repository from the starter, with the deployment workflow in it ([[nitrogen-create-storefront-repository]]).
- **From the command line:** the storefront is made in the admin first ([[nitrogen-create-storefront-setup]]). Then, in the project's folder:

```bash
cloudcart nitrogen init my-store
cloudcart nitrogen link
cloudcart nitrogen env pull
cloudcart nitrogen dev
cloudcart nitrogen deploy
```

`deploy` needs the storefront's deployment token ([[headless-deployment-methods]]).

### The merchant's own data

The starter's pages show no metafields or metaobjects, because each store defines its own. They are added page by page ([[metafields-nitrogen]]), and [[metafields-use-cases]] has a model for each need. A project made from the current starter is on a Nitrogen version that has them (2.2.0 or later). The skill's `references/metafields.md` covers how to read and show them.

## Contrasts

- **The starter vs a theme.** A theme is configured from the admin and stays CloudCart's. The starter's files become the project's own and change as code.
- **The project's copy vs the template.** New starter versions do not reach a project by themselves. `cloudcart nitrogen generate route` copies one of the starter's routes back into the project.

## Where it applies

- [[nitrogen-create-storefront]]: creating a storefront from it.
- [[headless-deployment-methods]]: GitHub or the command line.
- [[ai-agent-capabilities]]: an agent building on it.

## Related

- [[headless-storefront]]: hub.
- [[nitrogen-vs-themes]]: Nitrogen compared with a standard theme.
- [[ai-agent-toolkit]]: the skills and the two profiles.
- [[metafields-nitrogen]]: the store's own data on a storefront.

## Open Questions

- None known.
