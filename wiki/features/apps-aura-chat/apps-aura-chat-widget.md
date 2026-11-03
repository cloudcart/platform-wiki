---
type: feature
nav_path: "Storefront → Aura Chat window"
route_name: apps.aura_chat.settings
route_path: /admin/apps/aura_chat/settings
aliases: ["Aura Chat window", "chat widget", "chat launcher", "chat bubble", "product cards in chat", "add to cart from chat", "Избери действие", "Добави в количката", "Допълнителен въпрос", "Към количката", "Прикачи снимка", "Нов разговор", "Този разговор приключи", "Чатът временно не е достъпен", "чат прозорец", "балонче на чата"]
tags: [apps, ai, chat, storefront, widget]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 4
---

# Aura Chat — what the shopper sees in the chat

> Part of [[apps-aura-chat]]. See the hub for the other aspects (appearance, skills, proactive, conversations).

## Purpose

This page describes the chat window on the storefront from the shopper's side: what is on screen, what each button does, and the messages a shopper sees when something stops the chat. The merchant styles it on [[apps-aura-chat-appearance]]. The labels quoted here are the Bulgarian ones.

## Where to find it

On the storefront, on every page while the app is installed and enabled ([[apps-aura-chat-setup]]). The launcher sits bottom-left, bottom-centre or bottom-right. To try it, open the shop in a browser. The **Preview** box on the Settings tab shows the look only; it does not run a conversation.

## What the merchant can do here

The storefront window has no settings of its own. What changes it:

- look, launcher, cards, questions, disclaimer, rating row — [[apps-aura-chat-appearance]], [[apps-aura-chat-topics-feedback]];
- what the assistant can do — [[apps-aura-chat-skills]];
- when it speaks first — [[apps-aura-chat-proactive]].

## Settings & fields

### The launcher and the home screen

- **Launcher** — a bubble, a bubble with a prompt (*Пишете на {store}…*), or an icon only. When a proactive message is waiting, it gets a red count, like an unread message.
- **Home screen** — the greeting *Здравейте 👋 Как можем да помогнем?*, **Съобщения** (this browser's recent conversations), **Чести въпроси** (the merchant's opening questions) and **Нов разговор**.

### In a conversation

| Element | What it is |
|---|---|
| **Composer** | *Напишете съобщение…*, **Прикачи снимка** and send. While the assistant answers, send becomes stop; anything typed meanwhile is sent when it finishes. |
| **Photos** | Real images only. A photo counts as a request: the assistant says what it sees and searches for it. |
| **Product cards** | Photo, brand, name, price (old price struck through and a **Намален** badge when reduced, **Изчерпан** when sold out), a number in the corner and the assistant's one-line note. Several show as a swipeable row or a list, whichever the merchant chose. |
| **Избери действие** | The one button on a card, and the photo does the same. It opens **Виж продукта** (the product page, same tab), **Добави в количката**, **Допълнителен въпрос** and, once something is in the basket, **Към количката**. |
| **Допълнителен въпрос** | Pins the product above the composer so the next question is about it. At most three can be pinned. |
| **Shop cards** | A map, the address, a phone button, **Упътване** and **Отвори в Google Maps**. Opening hours are said in the text, not on the card. The shops come from [[apps-stores]]. |
| **Question cards** | The assistant's questions, usually with 3–6 answer buttons and a free-text field (*Или напишете отговор…*). Questions answered by reading something off, such as a name, an order number or an IBAN, have the field only. Several questions stack as a deck with a counter, and the shopper can step back to change an answer. |
| **Discount code** | When one is issued: the code (**Код**) and a link that applies it to the basket. See [[apps-aura-chat-discount-codes]]. |
| **Working labels** | Short status lines while the assistant works, such as *Търси в каталога*, *Проверява поръчката* and *Подбира продукти*. |
| **Rating row** | *Помогнах ли ти?* **Да / Не**. See [[apps-aura-chat-topics-feedback]]. |
| **Disclaimer** | The merchant's line under the message box. |

## Business rules

### "Add to cart" puts the product in the shopper's real basket

On the shop's main domain, **Добави в количката** adds one piece straight to the shopper's own store basket, and the basket count in the header updates. Everything added during one conversation lands in one basket. When the storefront is open on another address, the items are held for that conversation and join the shopper's basket when they press **Към количката**. The store's normal checks apply; if it refuses, the card says *Продуктът не можа да бъде добавен.* or the store's own message.

### A quiet conversation closes after 55 minutes

After 55 minutes without a message, the conversation shows *Този разговор приключи.* in place of the composer. Writing again starts a **new** conversation, which does not remember the old one.

### History lives in the shopper's browser

The **Съобщения** list is kept in the shopper's own browser for 30 days. It is not carried to another device or browser, and clearing site data removes it. The merchant's copy in [[apps-aura-chat-conversations]] is separate and is not affected.

### Labels follow the store's language; replies follow the shopper

The window's labels use the store's default language: Bulgarian or English, with any other language falling back to Bulgarian. The assistant writes back in whatever language the shopper writes in.

### When the chat cannot answer

The shopper sees a short notice that says nothing about billing:

| Why | What the shopper reads |
|---|---|
| Allowance used up ([[apps-aura-chat-usage]]) | *Чатът временно не е достъпен. Моля, опитайте по-късно или се свържете с магазина по друг начин.* |
| Store suspended (app uninstalled) | *Чатът временно не е достъпен. Моля, свържете се с магазина по друг начин.* |
| Store unknown to the chat service | *Чатът не е активен за този магазин.* |

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-appearance]] — the settings behind the look.
- [[apps-aura-chat-behaviour]] — why the assistant writes around its cards the way it does.
- [[cart]] — the storefront basket the chat adds to.
- [[apps-stores]] — the shops on the shop cards.

## Open questions

- Whether the shop cards read opening hours for every shop type, or only for shops that have them filled in (verify).
