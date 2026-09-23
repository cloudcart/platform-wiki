---
type: feature
nav_path: "Apps → Aura Chat → Settings"
route_name: apps.aura_chat.settings
route_path: /admin/apps/aura_chat/settings
aliases: ["Aura Chat settings", "Aura Chat appearance", "chat brand color", "chat position", "launcher style", "launcher icon", "opening questions", "suggested questions", "ready-made questions", "chat disclaimer", "Store name in chat", "вид на чата", "цвят на чата", "готови въпроси", "текст под полето за писане"]
tags: [apps, ai, chat, settings, appearance]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 4
---

# Aura Chat — Settings tab: look, opening questions, disclaimer

> Part of [[apps-aura-chat]]. See the hub for the other aspects (skills, proactive, conversations, usage).

## Purpose

The **Settings** tab controls how the chat looks on the storefront and what it offers before the shopper has typed anything. What the assistant *does* is set on Knowledge & Skills ([[apps-aura-chat-skills]]); this tab is only its presentation.

## Where to find it

**Apps → Aura Chat → Settings** (`/admin/apps/aura_chat/settings`). Five boxes, top to bottom: **Appearance**, **Preview**, **Opening questions**, **Ask what the shopper thought**, **The line under the message box**. Changes reach the storefront on the next page view ([[apps-aura-chat-setup]]).

## What the merchant can do here

- Name the chat and give it the brand colour.
- Place the launcher and choose its shape, including a custom icon.
- Choose how product cards are laid out.
- Offer up to six ready-made questions, optionally on the closed launcher.
- Switch the rating row on or off and edit its reasons ([[apps-aura-chat-topics-feedback]]).
- Edit or clear the disclaimer line.

## Settings & fields

### Appearance

"The chat takes your brand color and shades its background from it… The position applies to the launcher and to the open chat alike."

| Field | Values | Notes |
|---|---|---|
| **Store name** | text, required, max 120 characters | "How the chat introduces your shop — its title, and the invitation to write." The assistant also treats this name as "we", and it fills `{store}` in proactive messages and `{name}` in the disclaimer. A new store starts with its domain here. |
| **Brand color** | a colour (`#hex`) | Buttons and accents take it; the background is shaded from it. Empty = the chat's own colour. |
| **Position** | **Left** · **Center** · **Right** (default) | Applies to the launcher and to the open window. |
| **Page behind the chat** | **Dim** (default) · **Dim and blur** | What happens to the shop page while the chat is open. |
| **Product cards** | **Carousel** (default) · **List** | Several products as a swipeable row, or stacked. |
| **Launcher** | **Bubble** (default) · **Bubble with a prompt** · **Icon only** | "Bubble with a prompt" adds a line inviting the shopper to write. |
| **Launcher icon** | uploaded image (**Upload image** / **Replace image**) | "Used for the icon launcher and as the avatar on proactive messages. Shown small and cropped to a circle, so a square image works best." It goes into the store's file manager and is shrunk if very large. |

### Preview

"Roughly how the chat will sit on your storefront." It shows the look with a sample exchange; it is not a working chat.

### Opening questions

"Ready-made questions a visitor can tap instead of typing. Turn them off and the chat simply opens empty."

- **Offer ready-made questions** — the switch.
- The list — up to **6** questions, each up to 200 characters (placeholder *e.g. Where is my order?*, **Add a question**, **Remove**).
- **Show them on the launcher, before the chat is opened** — shows them as chips beside the closed launcher as well.

Tapping one sends it as the shopper's first message. Inside the window they sit under **Чести въпроси** on the home screen ([[apps-aura-chat-widget]]).

### Ask what the shopper thought

The thumbs-up / thumbs-down row and its reasons. Documented on [[apps-aura-chat-topics-feedback]].

### The line under the message box (Disclaimer)

- **Shown under the message box** — up to 200 characters. Placeholder: *Leave empty to show nothing*.
- "Write {name} where the assistant's name should appear, and renaming it later changes this line too."
- A new store starts with the standard line in its language:
  - Bulgarian: *{name} може да допуска неточности. Това е асистент, задвижван от изкуствен интелект.*
  - English: *{name} can make mistakes. This is an assistant powered by artificial intelligence.*
- "Clearing it removes the line entirely — the assistant still says it cannot be certain when it is not, but nothing is shown by default."

## Business rules

### The name is who the assistant is

The **Store name** is not only a title. The assistant is told it *is* that shop and must speak as "we", never naming the shop in the third person ([[apps-aura-chat-behaviour]]). A brand name reads better here than a domain.

### `{name}` is filled in when shown, not when saved

The disclaimer stores `{name}` as written and puts the current Store name in each time it is shown. Renaming the chat updates the line without editing it.

### Opening questions are the shopper's words

A tapped question is sent exactly as written, as if the shopper typed it. The assistant answers it with whatever skills are on. A question no skill can answer, such as *Where is my order?* with the Orders skill off, gets a polite "not something this chat can look up".

### Saving needs the chat service

Every box is saved to the chat service. If it cannot be reached, the tab shows *Could not reach the chat server.* and nothing is saved.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-widget]] — the result on the storefront.
- [[apps-aura-chat-topics-feedback]] — the rating row.
- [[apps-aura-chat-proactive]] — where the launcher icon is also used.
- [[apps-aura-chat-setup]] — the starting values, and what a reinstall resets.

## Open questions

- None known.
