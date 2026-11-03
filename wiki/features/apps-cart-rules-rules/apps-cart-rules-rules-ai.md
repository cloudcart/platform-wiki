---
type: feature
nav_path: "Apps → Cart Rules → Rules → Generate with AI"
route_name: apps.cart-rules.create
route_path: /admin/apps/cart-rules/rules/create/:type/:rule
aliases: ["Generate cart rule with AI", "AI cart rule", "Cart rule templates", "RuleGeneratorPopup", "Cart rule natural language"]
tags: [apps, marketing, automation, rules-engine, ai]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---

# Cart Rules — AI generation & templates

> Part of [[apps-cart-rules-rules]]. See the hub for the other aspects (list, editor, plan limits).

## Purpose

The **Generate with AI** flow lets the merchant create a cart rule from a plain-language description instead of building it by hand, OR pick a pre-built template. Either path opens the [[apps-cart-rules-rules-editor]] pre-filled, where the merchant reviews and saves. The AI path turns intent like *"10% off cart when total > 150 BGN AND customer has 3+ past orders"* into a structurally-valid rule; the template path skips the AI entirely.

## Where to find it

**Sidebar → Apps → Cart Rules → Rules → + Generate with AI** (button on the list), or the **AI generator panel inside an open rule** in the editor.

The AI call POSTs to `/api/cart-rules/ai` (route name `apps.cart-rules.ai`). Templates instead router-push to `apps.cart-rules.create` with `type: "template"` + the template ID.

## What the merchant can do here

The **RuleGeneratorPopup** offers two ways to start a rule:

- **Free-text textarea** — type a natural-language description, hit **Generate**, get a fully-populated rule rendered in the editor.
- **Template chips** — pick a pre-built template from the *"Or choose a template"* section to open the editor pre-filled, no AI call required.

## Settings & fields

### Dual input mode

| Mode | Behaviour |
|---|---|
| **Free-text textarea** | The merchant types a natural-language description into a single textarea with example placeholder *"Buy 3 products from Category New at the price of 2. The cheapest of the 3 products is free"*. Hitting **Generate** POSTs `/admin/api/cart-rules/ai` with `{question}` — the AI returns a fully-populated rule structure which is rendered in the editor. A reminder is shown below: *"Please verify if the generated rule is accurate. We do not guarantee that the AI-generated rule will be 100% correct."* |
| **Template chips** | Below the textarea, a *"Or choose a template"* section lists pre-built rule templates as ghost-button chips with a magic-wand icon. Clicking a template router-pushes to `apps.cart-rules.create` with `type: "template"` + `rule: <template.id>` — the editor opens pre-filled with the template's rule structure, NO AI call required. Templates load via the `templates` mixin (separate endpoint). |

The **Generate** button is disabled when `question` is empty AND no template was clicked. Generation runs through a CloudioLoader animation while waiting (`generateLoader = true`); the modal stays open until the API responds. On success: toast *"Rule generated successfully"* + modal closes + editor opens pre-filled. On API error: validation errors surface inline below the textarea via `responseErrors.question`.

### What the AI fills in

When the free-text path succeeds, the returned rule structure populates:

- Rule `name` + `title`.
- Triggers (`condition_type` + `filter_type` + `value_type` + `value` + `records`).
- Action (`action_type` + `value_type` + `value`).
- Customer-facing motivational `message`.

### Best practices for AI input

- Be specific about catalog records: name the vendor / category / tag / customer group rather than "some brand".
- Mention threshold values numerically.
- Specify the time window if time-limited.
- Mention WHICH items get discounted if it's not the whole cart.
- Mention the customer-segment if it's group-targeted.

## Business rules

- **AI-generated rules pass schema validation by construction.** The request bundles a strict JSON schema (the same one used for save-time validation), so the model is forced to return a structurally-valid rule — it can't produce a broken state. The generated rule still goes through the same server-side validation on save (see [[apps-cart-rules-rules-editor]]).
- **AI generation uses OpenAI gpt-4o-mini** (verified). The Generate-with-AI flow calls OpenAI's gpt-4o-mini model directly via the platform's OpenAI client helper — NOT CloudIO.
- **Templates bypass the AI entirely — zero token cost** (verified). The template chips do NOT call `/api/cart-rules/ai`; they navigate to the create route with the template ID and the controller loads the pre-built structure server-side. Using templates is free (no token consumption, no OpenAI roundtrip), while the free-text path costs tokens and adds a few seconds of latency. Merchants who don't need custom logic should prefer templates for common patterns.
- **Always review the generated rule.** The reminder text is explicit that AI output is not guaranteed correct; the merchant must verify before saving.

## Related

- [[apps-cart-rules-rules]] — hub.
- [[apps-cart-rules-rules-editor]] — the editor the generated rule opens in.
- [[apps-cart-rules]] — engine overview; § "AI engine".
- [[cart-rule]] — the underlying rule entity.
- [[cart-rules-examples]] — example rules that map well to templates.

## Open questions

None — all previously-flagged items resolved.
