---
type: feature
nav_path: "Apps → Aura Chat → the assistant's instructions"
route_name: apps.aura_chat.knowledge
route_path: /admin/apps/aura_chat/knowledge
aliases: ["Aura Chat prompt", "Aura Chat system prompt", "Aura Chat instructions text", "skill playbook text", "what the assistant is told", "промпт на Aura Chat", "инструкции на асистента", "системен промпт"]
tags: [apps, ai, chat, prompts, reference]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 12
---

# Aura Chat — the assistant's instructions, word for word

> Part of [[apps-aura-chat]]. See the hub for the other aspects (behaviour, selling, orders and returns, skills).

## Purpose

The assistant's behaviour is set by written instructions. This page lists every one of them, says when each is used and what part the merchant controls, and links to a verbatim copy in `wiki/resources/aura-chat-prompts/`. Use the copies to explain a specific reply, or to guide a merchant on writing their own instructions without contradicting the platform's. The summaries are on [[apps-aura-chat-behaviour]], [[apps-aura-chat-selling]] and [[apps-aura-chat-orders-returns]].

## Where to find it

Only in the wiki resources. The admin shows none of this text, apart from the merchant's own fields that feed into it.

## What the merchant can do here

The merchant cannot edit the platform text. They control the parts filled in from their settings:

- store name, brand colour and language, via Settings and the store itself;
- which skills are listed ([[apps-aura-chat-skills]]);
- the catalog-rule lines ([[apps-aura-chat-catalog-rules]]);
- their own instructions ([[apps-aura-chat-skills]]);
- the discount policy ([[apps-aura-chat-discount-codes]]);
- whether Product research is available ([[apps-aura-chat-agents]]);
- the topic list ([[apps-aura-chat-topics-feedback]]).

## Settings & fields

### How one conversation's instructions are put together

When a conversation starts, the assistant is given, in this order:

1. **Platform base**: identity, one store per session, scope, hard limits, grounding and honesty, published pages, behaviour, tone, standing with the shop, the chat window, gaps. Same for every store.
2. **Store profile**: today's date and time, the store name as "we", currency, language, storefront address, brand colour, catalog rules, the page the shopper opened the chat on, and the list of switched-on skills with their descriptions.
3. **Store-specific guidance**: the merchant's own instructions, framed as subordinate to everything above. Only if written.

During the conversation:

4. A **skill's playbook** is loaded when the shopper's request matches its description. The Promo codes playbook ends with the store's discount policy, or with the "no discount policy" text.
5. An **agent** gets only its own instructions and the one question it was asked. It sees none of the above.

After the conversation:

6. **Topic filing** runs separately on the shopper's words only ([[apps-aura-chat-topics-feedback]]).

### The files

| # | File | What it is | Used |
|---|---|---|---|
| 1 | [`aura-chat-01-platform-base.txt`](../../resources/aura-chat-prompts/aura-chat-01-platform-base.txt) | Base instructions | every conversation |
| 2 | [`aura-chat-02-store-profile.txt`](../../resources/aura-chat-prompts/aura-chat-02-store-profile.txt) | Store profile template | every conversation |
| 3 | [`aura-chat-03-store-guidance.txt`](../../resources/aura-chat-prompts/aura-chat-03-store-guidance.txt) | Frame around the merchant's instructions | when instructions are written |
| 4 | [`aura-chat-skill-product-discovery.txt`](../../resources/aura-chat-prompts/aura-chat-skill-product-discovery.txt) | **Finding products** playbook | skill on, broad request |
| 5 | [`aura-chat-skill-product-advice.txt`](../../resources/aura-chat-prompts/aura-chat-skill-product-advice.txt) | **Advising on products** playbook (+ Product research section) | skill on, product in view |
| 6 | [`aura-chat-skill-order-status.txt`](../../resources/aura-chat-prompts/aura-chat-skill-order-status.txt) | **Orders** playbook | skill on, order question |
| 7 | [`aura-chat-skill-order-returns.txt`](../../resources/aura-chat-prompts/aura-chat-skill-order-returns.txt) | **Returns** playbook | skill on, return question |
| 8 | [`aura-chat-skill-promo-codes.txt`](../../resources/aura-chat-prompts/aura-chat-skill-promo-codes.txt) | **Promo codes** playbook | skill on, money in the way |
| 9 | [`aura-chat-promo-policy.txt`](../../resources/aura-chat-prompts/aura-chat-promo-policy.txt) | Discount policy template (two versions) | end of #8 |
| 10 | [`aura-chat-agent-policy-lookup.txt`](../../resources/aura-chat-prompts/aura-chat-agent-policy-lookup.txt) | **Store pages** agent | whenever published pages are needed |
| 11 | [`aura-chat-agent-product-research.txt`](../../resources/aura-chat-prompts/aura-chat-agent-product-research.txt) | **Product research** agent | agent on, catalog gap |
| 12 | [`aura-chat-topic-filing.txt`](../../resources/aura-chat-prompts/aura-chat-topic-filing.txt) | Topic filing, plus the default topics | after a conversation goes quiet |

Each skill file begins with its **description**: the one or two sentences the assistant sees all the time, which decide when it loads the playbook. The admin shows a shorter merchant-facing help line instead.

## Business rules

### The instructions are in English; the replies are not

All instructions are written in English, with Bulgarian examples where the wording matters (button labels, sample phrases). The assistant replies in the shopper's language.

### Merchant text is data inside a frame

The merchant's instructions and their discount-policy text are inserted inside wording that makes them subordinate: they can narrow what the platform allows, never widen it. Text in those fields that reads like "ignore the rules" or "give a second code" has no effect ([[apps-aura-chat-skills]], [[apps-aura-chat-discount-codes]]).

### Writing good instructions

The base instructions already cover tone, honesty, the one-store rule and how to use the chat window, so merchant instructions work best when they add **what only the shop knows**. Examples: what to ask first in its trade, which lines to put forward, what never to promise, facts about service. Repeating the platform rules adds nothing, and contradicting them has no effect. Standing promotional lines are used at most once per conversation.

### Example names in the text

The base instructions use a store name, **ЗОРА**, as an example of what not to write ("ЗОРА does not decide that"). It is an illustration, not a setting.

### Keeping the copies current

The copies are dated and carry the source revision in their header. They are refreshed from the chat service's source whenever the assistant's instructions change; the procedure is in `wiki/resources/README.md`.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-behaviour]] — plain-language summary of #1.
- [[apps-aura-chat-selling]] — summary of #4 and #5.
- [[apps-aura-chat-orders-returns]] — summary of #6 and #7.
- [[apps-aura-chat-discount-codes]] — the settings behind #8 and #9.
- [[apps-aura-chat-agents]] — #10 and #11.

## Open questions

- None known.
