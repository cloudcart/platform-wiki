---
type: concept
nav_path: "Dashboard → Connect your store to an AI agent → The toolkit"
aliases: ["CloudCart AI Toolkit", "ai-toolkit", "cloudcart-plugin", "CloudCart CLI", "cloudcart app execute", "@cloudcart/cli", "Dev MCP", "@cloudcart/dev-mcp", "Storefront MCP", "@cloudcart/storefront-mcp", "platform-wiki", "Claude Code plugin", "Claude Desktop MCP", "Codex MCP", "Install profile"]
tags: [ai, agent, cli, mcp, setup, developer, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-05
source_count: 3
---

# The AI agent's toolkit

> Part of [[ai-agent]]. The agent installs all of this itself after [[ai-agent-connect]]; this page says what it is. The commands are in the [instructions](https://raw.githubusercontent.com/cloudcart/ai-toolkit/main/prompt.md).

## Definition

The **CloudCart AI Toolkit** is what an AI agent needs to work with a store. It has a small set of parts, published at `github.com/cloudcart/ai-toolkit`.

## Scope

### The parts

| Part | What it is for | Installed for |
|---|---|---|
| **CloudCart CLI** (`@cloudcart/cli`, command `cloudcart`) | Runs real reads and writes on the store: `cloudcart app execute`. Holds the sign-in. | Both profiles |
| **Dev MCP** (`@cloudcart/dev-mcp`) | Searches the Admin GraphQL schema and validates an operation before it runs. Does not touch the store's data. | Both profiles |
| **Platform wiki** (`github.com/cloudcart/platform-wiki`) | A public copy of this wiki, for questions on how the platform works. No account or token needed. | Both profiles |
| **Storefront MCP** (`@cloudcart/storefront-mcp`) | The Storefront API's schema, for building a Nitrogen storefront. | Build profile |

### The two profiles

The agent asks which one fits before it installs anything:

- **Manage my store** (the default, if the merchant is unsure): products, prices, stock, orders, customers, questions about the platform.
- **Build or develop on my store**: all of the above plus the Storefront MCP, for a Nitrogen storefront or other custom work. It can be added later.

### The instruction for a Nitrogen storefront

A storefront's page in the admin gives the merchant its own text to copy ([[nitrogen-storefront-overview]]). It points the agent at `design_prompt.md` in the toolkit, rather than `prompt.md`, and carries the commands for that storefront. The agent makes sure the build profile is installed and the store is connected, sets up the project, and hands it to the `cloudcart-nitrogen` skill.

### Requirements

- **Node.js 20 or newer**, which also brings `npm` and `npx`.
- **git.**
- **Claude Code on macOS or Linux:** `bash` and `python3` for the plugin's background hooks. On Windows the hooks do not run; the rest works.

### How each agent is set up

| Agent | How | Comes with |
|---|---|---|
| **Claude Code** | Plugin `cloudcart-plugin` from the `cloudcart/ai-toolkit` marketplace, then `/reload-plugins` | Skills, both MCP servers, wiki kept up to date |
| **Cursor** | *Cursor: Install Plugin From URL* with the toolkit's address | Skills, both MCP servers; wiki fetched on first use |
| **Gemini CLI** | `gemini extensions install` with the toolkit's address | Skills, both MCP servers; wiki fetched on first use |
| **VS Code** | *Chat: Install Plugin From Source* with the toolkit's address | Skills, both MCP servers; wiki fetched on first use |
| **Claude Desktop** | The Dev MCP added to `claude_desktop_config.json`, then a restart | The profile's MCP servers, a copy of the wiki, standing instructions |
| **OpenAI Codex** | `codex mcp add` for the Dev MCP | The profile's MCP servers, a copy of the wiki, standing instructions |
| **Other MCP clients** | A stdio server running `npx -y @cloudcart/dev-mcp@latest` | The profile's MCP servers, a copy of the wiki, standing instructions |

Every agent also installs the CLI and signs in, see [[ai-agent-access]].

**The plugin's skills** teach the agent how to work: answering from the wiki (`cloudcart-platform-expert`), catalog work with its previews and safeguards (`cloudcart-product-management`), Nitrogen storefronts (`cloudcart-nitrogen`), planning a new project (`project-setup`) and installing the CLI and the Dev MCP. Agents without the plugin instead get four standing rules in their own instructions file: store data only through the CLI, validate each operation with the Dev MCP first, answer platform questions from the wiki, and read `cloudcart-nitrogen` from the toolkit before building a storefront ([[headless-starter]]).

### Staying up to date

- **The wiki:** in Claude Code, a background check at the start of each session, at most once in 24 hours. Without the plugin, the agent refreshes its copy with a fetch and a hard reset when asked; the copy is read-only.
- **The MCP servers** run from `@latest` on each start.
- **The plugin in Claude Code** does not update by itself: `claude plugin marketplace update cloudcart-ai-toolkit`, `claude plugin install cloudcart-plugin@cloudcart-ai-toolkit`, then `/reload-plugins`.
- **The CLI:** `cloudcart version` shows the installed one.

## Contrasts

- **Dev MCP vs the CLI.** The Dev MCP knows what can be called, the CLI calls it. Only the CLI touches the store.
- **Plugin agents vs the others.** The difference is the skills: with them come the catalog safeguards in [[ai-agent-capabilities]].

## Where it applies

- [[ai-agent-connect]]: when it gets installed.
- [[headless-deployment-methods]]: the same CLI deploys Nitrogen storefronts.

## Related

- [[ai-agent]]: hub.
- [[ai-agent-access]]: the CLI's sign-in.
- [[headless-storefront]]: what the build profile is for.
- [[headless-starter]]: the starter, and when the `cloudcart-nitrogen` skill is required.

## Open Questions

- None known.
