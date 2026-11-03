---
type: concept
nav_path: "Dashboard → Connect your store to an AI agent → What it can do"
aliases: ["What can the AI agent do", "AI agent bulk edit", "Bulk changes with AI", "Bulk price change AI", "AI co-worker tasks", "Ask the agent", "Какво може AI агентът", "Масови промени с AI", "масова промяна на цени с AI"]
tags: [ai, agent, bulk-edit, products, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

# What the AI agent can do

> Part of [[ai-agent]]. Connecting it is in [[ai-agent-connect]]; its rights in [[ai-agent-access]].

## Definition

Once connected, the agent takes requests in plain language and in the merchant's language. Anything the **Admin GraphQL API** offers, it can reach: over 1,100 operations across the store's areas. How the platform works, it answers from this wiki rather than from memory.

## Scope

### What to ask for

| Kind of work | Examples |
|---|---|
| **Guide me** | "How does the abandoned-cart e-mail work?", "Where do I change the order notification?", "Is this behaviour by design?" The answer gives the path to click. |
| **Manage the catalog** | "Add a product called Summer Dress for 29.90", change a price, swap a photo, hide or delete items. |
| **Bulk changes** | "Lower the price of everything in Winter by 15%", "Hide everything that is out of stock", "Add 10 to the stock of these variants". |
| **Know the store** | Orders, best sellers, low stock, customers: "Which products are low on stock?" |
| **Use the store as context** | "Write a Facebook ad for my three best sellers", better descriptions, e-mail campaigns from real products. |
| **Tidy up** | Fix descriptions, organise categories, clean up the catalog. |
| **Build** (when set up for development) | Pages and components of a Nitrogen storefront, see [[headless-storefront]]. |

The Admin GraphQL API also covers customers, discounts and marketing, design, payments and shipping settings, apps, metafields ([[metafields-admin-api]]), imports and exports.

### How bulk changes run

The toolkit's skill for catalog work has the agent go through the same steps. It finds the products or variants, shows the merchant what will change, calculates any formula per item, applies the change and reports the result.

- **Preview:** for 10 or more products, the number and the first 5, then it waits for a yes.
- **Delete:** it always asks first, for one product or many.
- **New products:** it asks whether to save them as a draft or live.
- **100 rows or more:** it works from a script that first saves the current values to a CSV file and runs as a dry run, changing nothing until it is run to apply.
- **Over 1,000 rows:** that saved file is not skipped, even if the merchant says to skip it. It is the way back.
- **Errors on single items:** the rest continues, and all failures are listed at the end.

These rules come with the toolkit's skills, on agents that take the plugin. On the others, the agent has only the standing instructions, so ask it to show the plan first. See [[ai-agent-toolkit]].

Products have bulk operations for active, hidden, featured and new flags, categories, vendor, tags, out-of-stock status, stock tracking, duplicating and deleting; variants for price, quantity and continue-selling, and up to 500 different updates at once on one product. For any other field, such as a description or SEO title, the agent updates products one by one.

### When to use which tool

- **A rule that can be said in a sentence** ("15% off this category", "hide what's out of stock"): the agent. Nothing to export or format.
- **Values changed by hand across a sheet:** [[apps-google-sheets]].
- **A regular feed from a supplier or ERP:** [[import-pipeline]] and [[erp-integrations]].

### What it cannot reach

- **Anything the Admin GraphQL API does not offer**, and what is only on the merchant's computer unless the merchant gives it the file.
- **Actions a person must confirm.** A customers export or import asks for a two-factor code when the store has that step on: from the admin's e-mail or authenticator app.
- **More than its sign-in allows**, see [[ai-agent-access]].
- **More than 300 requests a minute** on the Admin GraphQL API. Large jobs take time.

There is no general undo for a change made through the API, as there is none for one made in the admin. See [[settings-backups]] for backups.

## Contrasts

- **Reading vs changing.** Reports and questions need only reading; changing the store needs a sign-in that may write.
- **Answering from the wiki vs from the store.** "How does X work?" comes from this wiki and cannot see the store's settings; "what is my X?" comes from the store's data.

## Where it applies

- [[products]]: the catalog work above.
- [[orders]] and [[customers]]: reading them, and the changes the API offers.
- [[metafields-admin-api]]: metafields and metaobjects.

## Related

- [[ai-agent]]: hub.
- [[apps-google-sheets]]: spreadsheet bulk edits.
- [[settings-pat-tokens]]: the token.

## Open Questions

- None known.
