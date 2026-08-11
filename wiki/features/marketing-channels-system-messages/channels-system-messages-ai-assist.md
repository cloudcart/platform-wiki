---
type: feature
nav_path: "Marketing → Channels → Channels setup → System messages → Write with AI"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Write with AI", "AI assist for system messages", "Cloudio AI", "AI generation of templates", "MINI_MODEL template generation"]
tags: [marketing, channels, system-messages, ai, cloudio]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-system-messages]]. See the hub for the other aspects (catalog, editor, variables, validation, business rules, counters).

# System messages — Write with AI

## Purpose

A per-field AI helper that drafts a complete message body from a short merchant prompt — niche-aware, channel-aware, and respecting the channel's character limit. Reduces blank-page friction for merchants who don't want to write the transactional copy from scratch.

## Where to find it

Inside the editor (see [[channels-system-messages-editor]]) — every text field that takes message content has a **Write with AI** button (Cloudio variant) next to its **Add variable** dropdown. Clicking it reveals a `CcAiPromptField` below the active editor.

## What the merchant can do here

- **Click Write with AI** on any content field to reveal the prompt input.
- **Type a short brief** in the prompt input (placeholder *"What's the message about?"*) and submit.
- **Get a complete generated message** back, in the prompt's language, respecting the channel's character cap.
- **Iterate** by submitting another prompt — the field's content is overwritten with the new generation.
- The merchant **cannot** pick a different model, change temperature, or compare versions; the platform's defaults apply.

## Settings & fields

The AI prompt input is a single free-text field (the *"What's the message about?"* sentence). There are no per-merchant tuning knobs (model, temperature, system prompt are platform-controlled — see *Backend model and tuning* below). The generated text appears in the editor field as a normal pill-aware string and is then subject to the standard per-channel validation on [[channels-system-messages-fields-validation]].

## Flow

1. Merchant clicks **Write with AI** on a field (e.g., Viber message text, Web Push title, Web Push body).
2. A prompt field opens below the editor with placeholder *"What's the message about?"*.
3. Merchant types a short brief — e.g., *"Notify the customer their order is being prepared"*.
4. Merchant submits. The platform POSTs `{prompt, field, variables}` to the AI generation endpoint — where:
   - `field` is one of `message`, `title`, `body`.
   - `variables` is the list of available merge tags for the channel + context (see [[channels-system-messages-variables]]).
5. On success: the response text replaces the editor content. Toast *"Message generated successfully"*. The prompt field auto-closes.
6. On error: toast *"Failed to generate message. Please try again."* The prompt field stays open so the merchant can retry.

## What the AI knows

| Aspect | Detail |
|--------|--------|
| Prompt | The merchant's short sentence — *"Notify the customer their order is being prepared"* — drives generation. |
| Channel awareness | The AI is told the channel type (Viber / SMS / Web Push) and the channel's character limit. |
| Industry context | The store's industry (`industry_array`) is injected into the system prompt so messages are niche-appropriate (a pharmacy gets pharmacy-style language; an apparel store gets apparel-style). |
| Available variables | The merge-tag list is passed in so the AI can drop in `{$customer_first_name}`, `{$order_id}`, etc. |
| Language | Instructed to *"Write in the same language as the user prompt"* — Bulgarian prompt → Bulgarian message; English prompt → English message. |

## Per-channel character cap

The AI output is hard-trimmed to the channel limit on the server:

| Channel | Cap applied to AI output |
|---------|--------------------------|
| Viber | 1000 chars |
| SMS | 160 chars (verify — see open question) |
| Web Push title | 63 chars |
| Web Push body | 128 chars |

After substitution at send-time, the merchant is responsible for not exceeding the limit with their chosen variables — the AI doesn't know the actual recipient's first-name length.

## Backend model and tuning

| Setting | Value |
|---------|-------|
| Provider | Cloudio integration |
| Model tier | `MINI_MODEL` (lower-cost model) |
| Temperature | 0.7 |
| Trim behaviour | Output is hard-trimmed to the channel limit if the AI returns text longer than the cap. |
| Whitespace | Trailing whitespace stripped. |
| Empty response | Yields a 422 (caught and surfaced as the generic error toast). |

## Failure modes

| Status | UI message |
|--------|-----------|
| 503 (Cloudio service unavailable) | Generic toast *"Failed to generate message. Please try again."* (underlying error: *"AI service unavailable."*) |
| 422 (generation failed) | Same generic toast (underlying: *"AI generation failed."*) |
| 422 (empty response) | Same generic toast (underlying: *"AI returned an empty response."*) |

The merchant always sees the same generic *"Failed to generate message. Please try again."* — the specific cause is captured server-side but not surfaced in the UI.

## Business rules

### AI respects char limit but not after substitution

The AI is told the channel limit and trims pre-send. But if the merchant inserts `{$customer_first_name}` and the actual recipient is *"Konstantina-Aleksandra"*, the substituted message may exceed the cap. There is no second-pass trim on substitute.

### Iterating — submit another prompt

The merchant can submit another prompt to overwrite the generated text. There is no "compare versions" view; the editor field shows the latest generated text only.

### Variables in the AI output

Because the variable list is passed in, the AI typically drops `{$customer_first_name}` etc. into its output. Those become pills in the editor as normal (see [[channels-system-messages-variables]]).

### One field at a time

Each Write with AI button targets one field. Web Push templates with title + body need two separate prompts — there is no "generate both" shortcut.

## Related

- [[marketing-channels-system-messages]] — hub.
- [[channels-system-messages-editor]] — host of the Write with AI button + prompt field.
- [[channels-system-messages-variables]] — variable list passed to the AI.
- [[channels-system-messages-fields-validation]] — char-cap rules the AI output is trimmed against.
- [[channels-system-messages-catalog]] — events for which AI-generated copy is most useful (order status change, fulfillment change).

## Open questions

- AI-assist SMS cap is documented as 160 chars while the SMS NTH field allows 918 chars (multi-part). Confirm whether AI trims to single-part SMS specifically — marked (verify).
