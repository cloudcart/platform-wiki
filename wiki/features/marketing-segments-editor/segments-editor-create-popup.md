---
type: feature
nav_path: "Marketing → Segments → Editor → Create popup"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Add segment popup", "Create segment popup", "Generate with AI", "Predefined templates", "Segment templates", "AI segment generation"]
tags: [marketing, segments, editor, templates, ai]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-segments-editor]]. See the hub for the other aspects (modal layout, condition builder, operators-and-values, validation, save pipeline, plan gates).

# Segment editor — Create popup (precursor)

## Purpose

When the merchant clicks **Create segment** on [[marketing-segments]], a small popup opens first to pick which downstream flow the [[segments-editor-modal-layout|editor]] opens in. This popup is **not** the editor — it is a route-picker between three options: build from scratch, generate with AI, or start from a predefined template. After choosing, the popup closes and the editor opens with the appropriate pre-fill (and the chosen type).

This popup does NOT run in Edit mode — editing an existing segment opens the editor directly with the stored conditions.

## Where to find it

From the [[marketing-segments]] list → **Create segment** (top-right). Backdrop and Escape both close this popup (it is light-weight, unlike the editor itself).

## What the merchant can do here

- **Build from scratch** — pick **Automated (X of Y)** or **One-time** to open the editor with an empty conditions tree (chosen type is passed through to the Create payload).
- **Generate with AI** — type a natural-language prompt; the system uses the `mini` model to produce a condition tree which opens in the editor as a One-time segment, pre-filled, for the merchant to verify before saving.
- **Pick a predefined template** — choose one of the 6 built-in templates (High Spenders, One-timers, Special product fans, Returning customers, Loyal customers, Cart abandoners); the editor opens pre-filled, always as a One-time segment.

## Settings & fields

### The three option cards

| Card | Title | Description text | Behaviour on click |
|------|-------|------------------|--------------------|
| **New segment from scratch** | "New segment from scratch" | "Build your own segment" | Expands to reveal two sub-cards: **Automated (X of Y)** and **One-time**. Picking either closes this popup and opens the editor with an empty conditions tree (the chosen type is passed through). |
| **Generate with AI** | "Generate with AI" | "Create a segment in seconds with CloudCart AI" | Expands to reveal a textarea (placeholder *"All users that have made a purchase in the last 30 days"*) + a **Generate** button. Disclaimer: *"*Please verify if the generated segment rule is accurate. We do not guarantee that the AI-generated rule will be 100% correct."*. Submitting routes to `POST /admin/api/core/marketing/segments/ai-generate`; on success the AI output's `conditions` are passed to the editor and a **One-time** segment is opened pre-filled. |
| **New segment from predefined template** | "New segment from predefined template" | "Use ready-made templates" | Expands to reveal 6 template cards. Picking one shows that template's description and an optional `*Note`. Confirming via **Create segment** closes this popup and opens the editor pre-filled with the template's conditions (always as a **One-time** segment). |

The **Automated (X of Y)** sub-card shows the merchant's current Automated-segment count vs cap (from the `segments` plan feature's `used` / `current`). If the merchant clicks Automated while at cap, the popup **does not open the editor** — instead it opens the standard per-feature purchase modal at [[plan-features]] with `mapping=segments`. After successful payment the editor opens with the unlocked Automated type. See [[segments-editor-plan-gates]] for the wider plan-feature interaction.

The textarea inside the AI card auto-focuses when it expands, so the merchant can immediately start typing. **Generate** is disabled while the prompt is empty (or while a generation is in flight).

### Built-in templates

Six templates are hard-coded in the Vue file. All template-created segments default to **One-time** (`regular` type) — even "Cart abandoners" which is a textbook automated-segment use case. The merchant must switch to Automated by going back through the Automated picker (since type is immutable once a segment is created).

| Template key | Title | Description shown in the card | Conditions (pre-filled) |
|--------------|-------|-------------------------------|--------------------------|
| `high_spenders` | High Spenders | "Customers who have spent a large amount of money in the store for a period not less than 180 days." (+ note: *"The amount depends on the store's niche. The default amount is 1500 EUR, you can edit accordingly."*) | Order → Average > 1500 AND Last order <= 180 days |
| `one_timers` | One-timers | "Customers who have made exactly one purchase." | Order → Times = 1 |
| `special_product_fans` | Special product fans | "Customers who bought or viewed specific product(s) multiple times." | View → Product (Any) → Times > 2 |
| `returning_customers` | Returning customers | "Customers who have made more than one purchase." | Order → Times > 1 |
| `loyal_customers` | Loyal customers | "Customers with high purchase frequency and/or high total spend." | Order → Times > 1 AND Average > 500 |
| `cart_abandoners` | Cart abandoners | "Customers who have abandoned their cart." | Cart → Cart abandoned = Abandoned |

### AI-generate flow

The AI prompt submits to `POST /admin/api/core/marketing/segments/ai-generate`, which runs the **`mini` model**. The model is constrained to produce only valid condition trees: schema-known condition keys only, operator/value only where allowed, date-interval values expressed as an interval + `days`/`hours`/`minutes`, exact dates as `YYYY-MM-DD` (a bare year is rejected — a year reference becomes an `in_last` interval, not an exact date), and 1–3 root conditions. If unsure the model returns no conditions.

The generated tree is normalised and its names are resolved to ids (customers, products, categories, vendors, etc.), then validated by the same condition manager that handles user edits — see [[segments-editor-validation]] for that normaliser and validator. Invalid AI output returns HTTP 422 with `conditions.<path>.<rule>` errors, which the popup surfaces so the merchant can rewrite the prompt. On success the conditions open in the editor as a **One-time** segment, pre-filled, still editable before saving.

## Business rules

- **Automated at cap → upsell modal instead of editor.** If the `segments` mapping is at cap, clicking Automated opens [[plan-features]] with `mapping=segments` rather than the editor. See [[segments-editor-plan-gates]].
- **AI and Template flows are always One-time.** Even when the template wants Automated semantics (e.g. `cart_abandoners`), the popup creates a One-time segment; switching to Automated requires re-creating via the Automated picker.
- **AI prompt is empty → Generate disabled.** Generate is also disabled while a request is in flight.
- **Backdrop and Escape close the popup.** Unlike the editor, this popup is dismissable — it has not collected any condition work yet.
- **The AI request pre-extracts numeric tokens** from the prompt (e.g. "20 days ago") to help the `mini` model resolve relative time references.

## Related

- [[marketing-segments-editor]] — hub.
- [[marketing-segments]] — parent list with the **Create segment** entry point.
- [[segments-editor-modal-layout]] — the editor modal that opens after this popup.
- [[segments-editor-condition-builder]] — the tree module that renders the template / AI-pre-filled conditions.
- [[segments-editor-validation]] — the same normalisers + condition manager validate AI output and user edits.
- [[segments-editor-plan-gates]] — the `segments` cap that gates the Automated sub-card.
- [[plan-features]] — the per-feature purchase modal opened when Automated is at cap.

## Open questions

No outstanding questions.
