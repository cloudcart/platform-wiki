---
type: feature
nav_path: "Apps → Aura Chat → Install"
route_name: apps.aura_chat.overview
route_path: /admin/apps/aura_chat
aliases: ["install Aura Chat", "Aura Chat not showing", "chat not appearing on the store", "enable Aura Chat", "disable Aura Chat", "uninstall Aura Chat", "reinstall Aura Chat", "Aura Chat defaults", "Datalayer required", "Aftercare required", "инсталиране на Aura Chat", "чатът не се показва", "изключване на чата", "преинсталиране"]
tags: [apps, ai, chat, install, setup]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 4
---

# Aura Chat — installing, what a new store starts with, switching off

> Part of [[apps-aura-chat]]. See the hub for the other aspects (widget, skills, discount codes, proactive, conversations, usage).

## Purpose

This aspect covers getting the chat onto the storefront. It lists the settings a new store starts with, the two other apps some features need, and what switching the app off, uninstalling it and installing it again each do.

## Where to find it

**Apps → Aura Chat** (`/admin/apps/aura_chat`). Before installation the page shows the app description and an **Install** button. After installation the same address opens the **Overview** tab, and the usual app **Enable / Disable** control sits in the page header. The app is listed in the App Store under the **Aura** apps category.

## What the merchant can do here

- **Install** the app. The chat goes live on the storefront straight away, with the starter allowance.
- **Switch it off and on** with the app's Enable / Disable control.
- **Install Datalayer or Aftercare in place** when a feature needs them (the warnings sit on the Proactive Sales and Knowledge & Skills tabs).
- **Uninstall** it.

## Settings & fields

### What a new store starts with

| Area | Starting value | Where to change it |
|---|---|---|
| Store name shown in the chat | the shop's own domain, e.g. `myshop.bg` | [[apps-aura-chat-appearance]] |
| Currency, language | the store's own currency and default language | follows the store |
| Look | launcher on the right, page behind dimmed, product cards as a carousel, the standard bubble launcher, no brand colour | [[apps-aura-chat-appearance]] |
| Opening questions | none | [[apps-aura-chat-appearance]] |
| Rating row (thumbs) | **on**, with the four standard reasons | [[apps-aura-chat-topics-feedback]] |
| Line under the message box | the standard AI disclaimer in the store's language | [[apps-aura-chat-appearance]] |
| Skills | **all off** | [[apps-aura-chat-skills]] |
| Own instructions | empty | [[apps-aura-chat-skills]] |
| Catalog rules | none | [[apps-aura-chat-catalog-rules]] |
| Discount codes | off | [[apps-aura-chat-discount-codes]] |
| Agents | published-pages lookup always on; product research off | [[apps-aura-chat-agents]] |
| Topics | the eight standard topics | [[apps-aura-chat-topics-feedback]] |
| Proactive Sales | one rule, "Proactive message": after 10 seconds on a page, asks whether it can help, in the store's language; never speaks on `/checkout`, `/cart*`, `/account*` | [[apps-aura-chat-proactive]] |
| Allowance | a small starter allowance | [[apps-aura-chat-usage]] |

### The two helper apps

| Needed for | App | What goes wrong without it |
|---|---|---|
| The **Returns** skill | **Aftercare** ([[apps-aftercare]]) | The skill can be switched on, but the assistant can neither start a return nor look one up. |
| Proactive conditions on **Kind of page**, and the `{product}` / `{category}` variables | **Datalayer** ([[apps-datalayer]]) | Those conditions never match, silently, on exactly the pages they aim at. |

Each tab warns ("Aftercare is not installed", "These rules cannot fire yet") and offers **Install Aftercare** / **Install Datalayer**. The button installs that app on the spot; it does not change whether the chat itself is on.

## Business rules

### The chat appears once the app is installed and enabled

The storefront loads the chat only while the app is both installed and enabled. Look-and-feel changes (colour, position, launcher, questions) are read by the chat when a page loads. They show on the next page view and do not need the storefront scripts rebuilt.

### Switching off stops the chat without losing anything

Disabling the app takes the chat off the storefront. Settings, rules, conversations and the remaining allowance stay as they were, and enabling it again brings the same chat back.

### Uninstalling suspends; it does not delete

On uninstall the store is **suspended** on the chat service. The chat stops answering at once, the app's storefront access key is revoked, and the store's configuration and conversations are **kept**.

### Reinstalling brings the same setup back

Installing again finds the suspended store and reactivates it. The starting values above go **only to a store the chat service has never seen**. A reinstall refreshes just the store's currency, default language, storefront address and the app's access key. Everything else stays as the merchant left it: the look, opening questions, skills, own instructions, the allowance, proactive rules, topics, rating settings, disclaimer, catalog rules, discount policy, agent switches and past conversations.

### A failed install can be finished from the settings

If the chat service cannot be reached during install, the app is still recorded as installed and an alert asks the merchant to save the settings. Saving any Aura Chat settings registers the store.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-usage]] — the starter allowance and buying credit.
- [[apps-aura-chat-widget]] — what appears on the storefront.
- [[apps-aftercare]], [[apps-datalayer]] — the helper apps.
- [[apps]] — installing and uninstalling apps in general.

## Open questions

- Whether the launcher also shows on the checkout pages of every theme. The chat itself has no checkout exclusion; only the proactive message is kept off `/checkout` (verify).
