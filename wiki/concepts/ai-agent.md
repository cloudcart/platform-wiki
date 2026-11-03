---
type: concept
nav_path: "Dashboard → Connect your store to an AI agent"
route_name: dashboard
route_path: /admin/
aliases: ["AI agent", "AI co-worker", "Connect your store to an AI agent", "Connect store to AI", "Copy the setup instruction", "CloudCart AI Toolkit", "ai-toolkit", "Claude", "ChatGPT", "Cursor", "AI агент", "Свържи магазина си с AI агент", "Копирай инструкцията", "AI колега", "агент за магазина"]
tags: [ai, agent, automation, bulk-edit, cli, mcp, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 5
---

# AI agent connected to the store

## Definition

A merchant can connect their store to an **AI agent**: Claude, ChatGPT, Cursor or another agent they already use. Once connected, the agent works as a **co-worker in the store**. It is given a job in plain language and does it independently, next to the store's other staff:

- it **guides**: how a feature works, where a setting is, the exact clicks to get there;
- it **does the work**: adds and edits products, changes prices and stock, reads orders and customers;
- it **changes things in bulk**: "lower everything in Winter by 15%", "hide everything out of stock";
- it **uses the store as context**: writes ads, e-mails and descriptions from the real products.

The merchant connects it with one sentence copied from the admin, see [[ai-agent-connect]]. The agent then sets itself up and asks only for what the merchant alone can give.

The agent runs in its own app, on the merchant's computer or wherever that agent runs. It is not an app installed in the store and it has no screen in the admin. It reaches the store through the **Admin GraphQL API**, with a sign-in the merchant gave it.

## Scope

- [[ai-agent-connect]]: the card and the bar in the admin, the copied sentence, what the agent does after it is pasted, what only the merchant can do.
- [[ai-agent-capabilities]]: what to ask it for, how bulk changes run, what it cannot reach.
- [[ai-agent-access]]: the two ways to sign it in, whose rights it works with, the token's options, disconnecting it.
- [[ai-agent-toolkit]]: the parts it installs, which agents are supported and how each is set up, how it stays up to date.

## Contrasts

- **AI agent vs [[apps-aura-chat|Aura Chat]].** Aura Chat talks to **shoppers** on the storefront, as the shop. The AI agent works for the **merchant and staff**, on the store's admin data.
- **AI agent vs [[apps-cloudio-overview|Cloudio]].** Cloudio is CloudCart's own AI inside admin screens (descriptions, translations, rule generation), paid in tokens. The AI agent is the merchant's own, from their own AI provider, and works across the store.
- **AI agent vs a staff account ([[settings-staff]]).** A staff account is a person signing in to the admin. The agent has no account of its own: it works with a token issued by the owner, or with the session of the admin who signed it in, see [[ai-agent-access]].
- **AI agent vs [[apps-google-sheets|Google Sheets]].** Google Sheets suits changing values by hand in a spreadsheet. The agent suits a change that can be said as a rule, see [[ai-agent-capabilities]].
- **AI agent vs [[settings-api-keys|API keys]].** An API key connects a fixed integration through the REST API. The agent works through the Admin GraphQL API and decides what to call from the request.

## Where it applies

- **[[dashboard]]**: the *Connect your store to an AI agent* card.
- **Every other admin page**: the same offer as a bar above the navigation, until hidden.
- **[[settings-pat-tokens]]**: the token the agent signs in with.
- **[[settings-staff]]**: the permissions that limit an agent signed in as a staff member.

## Related

- [[pat-token]]: the credential itself.
- [[merchant-roles-api-access]]: API access next to staff accounts.
- [[headless-storefront]]: storefronts the agent can also build, when set up for development.
- [[apps-google-sheets]]: the spreadsheet way to edit in bulk.

## Open Questions

- None known.
