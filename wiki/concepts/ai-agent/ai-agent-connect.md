---
type: concept
nav_path: "Dashboard → Connect your store to an AI agent → Connecting"
aliases: ["Connect AI agent", "Connect your store to an AI agent card", "AI agent bar", "Hide for 7 days", "Copy the setup instruction", "Fetch and follow the instructions", "prompt.md", "Set up my AI agent", "Копирай инструкцията", "Свържи магазина си с AI агент", "Как да свържа AI агент"]
tags: [ai, agent, setup, dashboard, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 3
---

# Connecting the store to an AI agent

> Part of [[ai-agent]]. What it can then do is in [[ai-agent-capabilities]]; the sign-in in [[ai-agent-access]].

## Definition

Connecting takes one copied sentence. The merchant copies it from the admin and pastes it into their AI agent. The agent reads CloudCart's instructions, installs what it needs and asks the merchant for the store's address and a token.

## Scope

### Where the offer is

| Where | What it shows |
|---|---|
| **[[dashboard]]** | A card with a **New** badge (*НОВО*), titled *Connect your store to an AI agent* (*Свържи магазина си с AI агент*). Always there, on the onboarding and the full dashboard alike. |
| **Every other admin page** | A bar above the navigation with the same title and button. Its **X** (*Hide for 7 days*) hides it for 7 days on that browser, then it comes back. The dashboard card stays either way. |

The card's text: *"Copy the setup instruction with one click and paste it into Claude, ChatGPT or another AI agent. It connects to your store, and from there you can ask it questions and give it tasks in plain language."*

In a Bulgarian admin: *"Копирай инструкцията с един клик и я постави в Claude, ChatGPT или друг AI агент. Оттам той се свързва с магазина ти и можеш да го питаш и да му възлагаш на нормален език."*

### The button

**Copy the setup instruction** (*Копирай инструкцията*) copies this sentence, in English in every admin language because it is read by the agent:

```
Fetch and follow the instructions at https://raw.githubusercontent.com/cloudcart/ai-toolkit/main/prompt.md to set up my AI agent for CloudCart
```

The button then reads *"✓ Copied — now paste it into your agent"*. If the browser blocks copying, it reads *"Select the text and press Ctrl+C"* and shows the sentence in a field to copy by hand.

### The backup offer

After a copy, a store that can have [[settings-backups|daily backups]] and has no backup subscription sees a window, at most once in 30 days on that browser:

> *"Protect your store before your agent gets to work"*
> *"An AI agent can change products, prices and settings in your store. With daily backups you can restore the whole store or just part of it in a few clicks."*
> *"A restore brings back the latest daily copy, so changes made after it are not kept."*

**Activate backups** opens [[settings-backups]], at `/admin/settings/backups`. **Not now** closes the window. The sentence is already copied either way.

### What the agent does after it is pasted

1. **Asks two questions:** which language to work in, and what the store will be used for: **manage the store** (the default) or **build on it** (a Nitrogen storefront or other development). See [[ai-agent-toolkit]].
2. **Checks the computer:** Node.js 20 or newer and git, and installs what is missing where it can.
3. **Installs the toolkit** in the way that fits the agent.
4. **Installs the CloudCart CLI**, then asks the merchant for a personal access token and the store's domain, and signs in.
5. **Confirms the connection** and offers examples of what it can do now, in the merchant's language.

The store's domain can be the CloudCart address (`mystore.cloudcart.net`) or the store's own (`mystore.com`). The agent uses it without `https://` or a trailing slash.

### What only the merchant can do

- **Create the token.** In the admin, the user menu in the bottom-left corner → **PAT Tokens** (*PAT токени*). Only the store owner can create one. See [[ai-agent-access]] for the options.
- **Install Node.js** when that needs administrator rights on the computer. The agent says what is missing and waits.
- **Confirm inside the agent's app** where it asks: approving a plugin, running `/reload-plugins` in Claude Code, restarting Claude Desktop or Codex once so the new tools load.

### Which agents can connect

The instructions have the agent **run commands on a computer**, so it needs an agent that can do that: Claude Code, Claude Desktop, Cursor, Gemini CLI, VS Code, OpenAI Codex or another agent that runs MCP servers. Setup per agent is in [[ai-agent-toolkit]]. The ChatGPT desktop app can use the same local server through its connectors in developer mode where available; if it cannot, the instructions point to OpenAI Codex.

## Contrasts

- **The card vs the bar.** They copy the same sentence. Hiding the bar does not remove the card.
- **Connecting vs installing an app.** Nothing is installed in the store and no app appears under [[apps]]. The installation is on the merchant's side.

## Where it applies

- [[dashboard]]: the card.
- [[settings-pat-tokens]]: where the token is created.

## Related

- [[ai-agent]]: hub.
- [[ai-agent-access]]: signing in and disconnecting.
- [[ai-agent-toolkit]]: what gets installed.

## Open Questions

- None known.
