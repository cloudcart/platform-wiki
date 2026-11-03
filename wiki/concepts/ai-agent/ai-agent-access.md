---
type: concept
nav_path: "Dashboard → Connect your store to an AI agent → Access"
aliases: ["AI agent access", "AI agent permissions", "AI agent token", "cloudcart auth login", "cloudcart auth logout", "Browser login CLI", "Disconnect AI agent", "Read Only or Full Access for AI", "Права на AI агента", "Как да откача AI агент"]
tags: [ai, agent, access, tokens, security, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

# The AI agent's access to the store

> Part of [[ai-agent]]. The token's screen is documented in [[settings-pat-tokens]].

## Definition

The agent has no account of its own. It works with the rights of one of two sign-ins made on the computer it runs on, through the CloudCart CLI.

## Scope

### The two sign-ins

| | **Personal access token** | **Browser sign-in** |
|---|---|---|
| **How** | The owner creates a token (it starts with `cc_pat_`) and gives it to the agent once. | The CLI opens the store's admin, an admin signs in there. |
| **Works as** | The store owner, since a token is always the owner's. | The admin who signed in, with their staff permissions. |
| **Lasts** | Until its end date, or with no end date, until revoked. | 30 days, then sign in again. |
| **Who** | Only the owner can create one. | Any admin of the store. |
| **What you set** | The token's access level, validity and IP list. | The admin's sections in [[settings-staff]]. |

The agent's setup uses the token. Run with no flags, `cloudcart auth login` asks which of the two to use.

**To have the agent work within a part of the store**, give it a token with **Custom Permissions**, or a browser sign-in of a staff member whose permissions cover only those sections. The Admin GraphQL API checks both on every operation, and refuses with a message naming what is missing ([[admin-graphql-api]]). Some operations are for the owner alone.

### The token's options

Created under the user menu in the bottom-left corner → **PAT Tokens** (*PAT токени*), up to 100 per owner. See [[settings-pat-tokens-create-flow]].

**Access level**, with the screen's descriptions:

| Level | On screen | For |
|---|---|---|
| **Read Only** (marked *Recommended*) | *"View-only access to all resources. No modifications allowed. Safe for monitoring and reporting."* | Questions and reports. |
| **Full Access** | *"Complete read and write access to all store resources. Best for CI/CD pipelines and full automation."* | An agent that changes the store. |
| **Custom Permissions** | *"Select specific resources and permissions. Best for limited access scenarios."* | Part of the store: products, orders, customers, inventory, discounts, blog, settings, webhooks. |

The level holds on the Admin GraphQL API too: a Read Only token is refused every change, and a Custom Permissions token is refused what it was not given.

**Advanced settings** ([[settings-pat-tokens-restrictions]]):

- **Token validity:** start and end dates, or *No expiration*.
- **IP restrictions:** single addresses or ranges such as `192.168.1.0/24`. Empty allows all.

### Handling the token

The agent is told to use it only in the sign-in command, and never to print it, log it or write it into a file.
- The CLI keeps the sign-in on that computer, in a `.cloudcart` folder in the user's home, or in the system's keychain when set to.
- **A token works from anywhere for anyone holding it**, unless it has an IP list. It is guarded like a password.

### Who did what

Changes through a token are made as the store owner, so history screens show the owner rather than a separate "agent". The token's list shows when it was last used ([[settings-pat-tokens-list-view]]). A separate token per agent or job keeps these apart.

### Disconnecting

- **Revoke the token** on the PAT Tokens screen: it stops working at once, on every computer. Switching it off with its status toggle works the same and can be undone.
- **On the agent's computer:** `cloudcart auth logout` clears the stored sign-in. `cloudcart auth status` shows the current one.

A browser sign-in is not on the PAT Tokens screen. It ends with `cloudcart auth logout` on that computer, or after its 30 days.

### What the AI service sees

The agent's provider processes what the agent reads from the store, under the terms of the merchant's account there: products, and also orders and customers if the agent is asked to read them. Which agent and provider to use is the merchant's choice.

## Contrasts

- **Token vs API key ([[settings-api-keys]]).** A token signs in the CLI and the Admin GraphQL API, shows its value once and keeps only a hash. An API key serves the REST API and integrations. See [[merchant-roles-api-access]].
- **Token vs staff account.** A token is no staff account and does not count toward the `administrators` plan limit.

## Where it applies

- [[settings-pat-tokens]]: creating, limiting, revoking.
- [[settings-staff]]: the permissions of a browser sign-in.
- [[merchant-roles]]: owner and moderators.

## Related

- [[ai-agent]]: hub.
- [[pat-token]]: the credential.
- [[ai-agent-connect]]: when the agent asks for it.

## Open Questions

- None known.
