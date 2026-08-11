---
type: feature
nav_path: "Marketing → Segments → Create-segment popup"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Create new segment", "Add segment modal", "Segment templates", "Generate with AI"]
tags: [marketing, segments, ai, templates]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-segments]]. See the hub for related aspects (list page, types, conditions, etc.).

# Segments — Create-segment popup

## Purpose

The **Create new segment** popup is a small route-picker modal that decides which downstream flow the editor opens in. It is NOT the editor itself — it gathers the merchant's choice (from scratch / AI / template) and then opens [[marketing-segments-editor]] with the appropriate pre-fill.

## Where to find it

Sidebar → **Marketing** → **Segments** → **Create segment** button (top of [[segments-list-page]]).

Backdrop and Escape both close the popup (light-weight).

## What the merchant can do here

The merchant sees **three expandable option cards**.

| Card | Title | Description text | Behaviour on click |
|------|-------|------------------|--------------------|
| **New segment from scratch** | "New segment from scratch" | "Build your own segment" | Expands to reveal two sub-cards: **Automated (X of Y)** and **One-time**. Picking either closes this popup and opens [[marketing-segments-editor]] with an empty conditions tree (the chosen type is passed through). |
| **Generate with AI** | "Generate with AI" | "Create a segment in seconds with CloudCart AI" | Expands to reveal a textarea (placeholder *"All users that have made a purchase in the last 30 days"*) + a **Generate** button (variant `cloudio`, with a wand-magic-sparkles icon). Disclaimer in small grey print: *"\*Please verify if the generated segment rule is accurate. We do not guarantee that the AI-generated rule will be 100% correct."*. Submitting routes to `POST /admin/api/core/marketing/segments/ai-generate` with the prompt; on success the AI output's `conditions` are passed to the editor and a **One-time** segment is opened pre-filled. |
| **New segment from predefined template** | "New segment from predefined template" | "Use ready-made templates" | Expands to reveal 6 template cards. Picking one shows that template's description and an optional `*Note` (e.g., the "High Spenders" note about currency). Confirming via **Create segment** closes this popup and opens the editor pre-filled with the template's conditions (always as a **One-time** segment, regardless of plan availability). |

## Settings & fields

### Automated counter

The "Automated (X of Y)" sub-card shows the merchant's current Automated-segment count vs cap (from the `segments` plan feature's `used` / `current`). If the merchant clicks Automated while at cap, the popup **does not open the editor** — instead it opens the **`PlanFeature` upsell modal** with `mapping=segments` (the standard per-feature purchase modal at [[plan-features]]). After successful payment the meta refetches and the editor opens with the unlocked Automated type.

### AI card

The textarea inside the AI card auto-focuses on expand (after a `nextTick`) so the merchant can immediately start typing. **Generate** is **disabled while the prompt is empty** (or while a generation is in flight).

### Built-in templates (6 hard-coded)

| Template key | Title | Description shown in the card | Conditions (pre-filled) |
|--------------|-------|-------------------------------|--------------------------|
| `high_spenders` | High Spenders | "Customers who have spent a large amount of money in the store for a period not less than 180 days." (+ note about currency / 1500 EUR default) | Order → Average > 1500 AND Last order <= 180 |
| `one_timers` | One-timers | "Customers who have made exactly one purchase." | Order → Times = 1 |
| `special_product_fans` | Special product fans | "Customers who bought or viewed specific product(s) multiple times." | View → Product (Any) → Times > 2 |
| `returning_customers` | Returning customers | "Customers who have made more than one purchase." | Order → Times > 1 |
| `loyal_customers` | Loyal customers | "Customers with high purchase frequency and/or high total spend." | Order → Times > 1 AND Average > 500 |
| `cart_abandoners` | Cart abandoners | "Customers who have abandoned their cart." | Cart → Cart abandoned = Abandoned |

## Business rules

### Templates always create One-time segments

All template-created segments default to **One-time** (`regular` type) — even "Cart abandoners" which is a textbook automated-segment use case. The merchant must switch to Automated by first closing the editor and creating a fresh segment through the Automated picker (since type is immutable once a segment is created — see [[segments-types]] and [[marketing-segments-editor]]).

### AI-generated segments are One-time

Even though "All users that have made a purchase in the last 30 days" is a textbook automated use case, the AI flow opens a **One-time** segment pre-filled with the generated conditions. The merchant is responsible for verifying the rule (per the disclaimer) and re-creating it as Automated if needed.

### Over-cap interception

The popup intercepts the over-cap case **before** opening the editor — the merchant sees the upsell modal instead. This avoids the merchant building out conditions only to discover at save time they can't add another Automated segment.

## Related

- [[marketing-segments]] — hub.
- [[marketing-segments-editor]] — opened pre-filled by this popup.
- [[segments-types]] — the One-time vs Automated distinction this popup picks.
- [[segments-list-page]] — hosts the **Create segment** button that opens this popup.
- [[plan-features]] — the per-feature upsell modal triggered on Automated cap.
- [[segments-api-and-plan-gates]] — defines the `segments` cap that the Automated counter reads.

## Open questions

- 📡 **AI endpoint contract.** The exact response shape of `POST /admin/api/core/marketing/segments/ai-generate` (whether it always returns a conditions tree, how it signals "couldn't parse") (verify).
