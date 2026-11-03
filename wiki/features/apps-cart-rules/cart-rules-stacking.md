---
type: feature
nav_path: "Apps → Cart Rules → Stacking"
route_name: ""
route_path: ""
aliases: ["Cart rule stacking", "Cart-level stacking", "Product-level stacking", "Winner-takes-all", "Rule evaluation order", "Multi-row OR-fallback", "Products consumed across rules"]
tags: [apps, cart-rules, marketing, promotions, stacking, evaluation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-cart-rules]]. See the hub for the other aspects.

# Cart Rules — Stacking and evaluation order

## Purpose

When a cart matches multiple rules — or a multi-row rule has several matching rows — the engine decides **which discounts apply** and **in which order**. Short version (each detailed under *Business rules*):

1. Rules evaluate in **descending `sort_order`** (highest priority first).
2. Within a rule, **only ONE row fires** (OR-fallback ladder, highest-`sorting` row first).
3. **Products are consumed across rules** — once a rule matches a product, no later rule can.
4. **Cart-level matches are winner-takes-all** — only the highest-`value` cart-level match applies.
5. **Product-level matches accumulate** per line, subject to the negative-price guard.

Cart Rules also stack with the simpler [[marketing-discounts]] system — Discounts first; Cart Rules see the discounted basis.

## Where to find it

Stacking is **NOT configurable** in the rule editor — no per-rule "stack with others" toggle, no "exclusive" flag, no global `combine_rules` setting (older wiki phrasing referred to one; no such setting exists). The merchant controls it indirectly via `sort_order` priorities and cart-level vs product-level scope (see [[cart-rules-scoping]]).

## What the merchant can do here

Stacking is an engine behaviour, not a configured setting. The merchant influences which rules apply, and in which order, through three indirect levers (detailed in *Settings & fields*): distinct `sort_order` priorities; cart-level vs product-level scope via the action-triggers (see [[cart-rules-scoping]]); and deliberate sequencing — put narrow / specific rules first, broad / catch-all rules last, so broad rules don't starve narrow ones.

If the merchant needs *"these two rules must both apply on the same product"*, the answer is **"not possible at the cart level — make them product-level so they accumulate, or merge them into a single rule"**.

## Settings & fields

No user-editable settings on this aspect. The merchant influences it via:

| Lever | Where | Effect |
|---|---|---|
| `sort_order` | Drag-and-drop on the rules list | Higher first; decides which rule gets first dibs on overlapping products. |
| Action-trigger configuration | Each row's action block | Empty → cart-level (winner-takes-all). Any product-targeting trigger → product-level (accumulating). |
| Multi-row tier ordering | Row `sorting` integer | Highest-`sorting` row fires FIRST — that's the **bottom / last-added** row in the editor (evaluation runs bottom-to-top). Put the most generous tier there. |

## Business rules

### Evaluation order and basis

Every time the cart's product list is read, active rules evaluate in **descending `sort_order`** (highest priority first). Two basis facts:

- **Matching sees the post-discount price** — a rule matches the price the customer actually pays per line, **after** [[marketing-discounts]] has applied (or the regular price if none). So evaluation is **Discounts → then Cart Rules** on the discounted basis. See [[discount-stacking]] for the full matrix.
- A matching rule contributes both an **upsell message** (if its row has one) and a **discount action** (cart-level or per line). Only ONE message per rule shows — see *Message-row precedence*.

### Rows are an OR-fallback chain — highest-`sorting` row fires FIRST

Multi-row rules are an **OR-fallback ladder**, **NOT** accumulating deals on the same cart. The row with the **highest `sorting` value evaluates first** (`sorting=2` before `1` before `0`); the engine stops at the first row whose triggers all match, attaches that row's action, and **skips every other row of the rule**. So **only ONE row per rule fires**. Use this for tiered fallbacks (*"cart > 100 EUR → 10%; else cart > 50 EUR → 5%; else nothing"*).

**Which row is "first" — the direction is the INVERSE of top-to-bottom (easy to get backwards):** in the editor the rows are listed by `sorting` **ascending**, so the row you add **first** (Row 0, lowest `sorting`) sits at the **top**, and every row you add afterwards appends **below** it with a higher `sorting`. But the matcher tests the **highest `sorting` first**, so evaluation runs **bottom-to-top**: the **bottom (last-added) row is tested first**, and the **top row (Row 0) is the last-resort fallback** — applied only when no lower row matched. **Put the most generous tier on the bottom (last-added) row.** (Verified against the code: rows are stored `sorting`-ascending and the matcher reverses them before evaluating.)

**Common merchant mistake** — putting the more generous tier on the **top** row thinking it fires "first". It fires **last**; the top row wins only when no other row matched.

> **Rows and the rules list run in OPPOSITE directions — same drag gesture, opposite meaning.** In the **rules list**, the **top** rule has the highest `sort_order` and is evaluated **first** (top-to-bottom — see *Evaluation order* above). Inside **one rule**, the **top** row has the lowest `sorting` and is evaluated **last** (bottom-to-top). So dragging a *rule* to the top makes it win first; dragging a *row* to the top makes it the fallback.

### Message-row precedence — the upsell pattern

The customer sees the message from the **lowest tier they have NOT yet qualified for** (`sorting` greater than the matched row's). Example, a 3-row rule: Row 0 cart > 25 EUR → 5%, Row 1 cart > 50 EUR → 10%, Row 2 cart > 100 EUR → free shipping. At 40 EUR only Row 0 matches → 5% applied, and Row 1's message *"Spend over 50 EUR for 10% off"* shows. Only one message per rule displays; matching the **top tier** shows none — nothing above to upsell to.

### Products consumed across rules

When a rule matches (any one row fires), its matched products are **removed from the pool** before the next rule evaluates: Rule A consumes its matches, so Rule B sees only the remainder, and so on. Consequences:

- A product line cannot be discounted by 2 rules — **first rule to match it wins it**.
- Rule priority (`sort_order` descending) decides first pick of overlapping products; a broad, high-priority rule starves later, more-specific rules.

**Merchant impact:** "5% off Brand X" at priority 10 and "10% off Brand X RED variants" at priority 5 → every Brand X item (including RED) gets the 5% first; the RED rule never sees them. Fix: **raise the more specific rule above the broad one** so it claims the RED items first.

### Cart-level stacking — only the HIGHEST-`value` cart match wins

When multiple rules produce a cart-level (whole-cart) match, the engine keeps **only the one with the highest stored `value`** — it does NOT sum them and does NOT split by `value_type`. Only ONE cart-level match applies even if 3 matched, **regardless of percent / amount / free_shipping**:

- **Two percent-off cart rules** (e.g. 50% and 30%): only the higher % wins; the lower silently doesn't fire.
- **Cart-level percent + cart-level amount**: the winner is the highest **raw stored `value`** (`matches->sortByDesc('value')->first`). Both are stored ×100 but in **different units** — amount in cents (10 EUR → `1000`), percent ×100 (50% → `5000`). The comparison is therefore cross-unit and arbitrary: a percent rule's raw value is usually the larger number, so **a 50% rule (`5000`) outranks a 10 EUR amount-off (`1000`)** — even on a small cart where 50% is only a couple of EUR and the 10 EUR rule would take off more. Avoid mixing the two on overlapping triggers.
- **Cart-level `free_shipping` vs another cart-level rule**: a free-shipping rule's stored `value` is null/zero, so any matching cart-level percent or amount rule outranks it — **free shipping is silently dropped** whenever another cart-level match exists. It survives only as the ONLY cart-level match. A *"free shipping over 50 EUR"* rule can quietly stop firing once any other cart-level percent / amount rule starts matching.
- **Product-level percent-off + product-level amount-off on the same line**: both apply (line matches accumulate, subject to the negative-price guard on amount-off — see [[cart-rules-actions]]).

There is **NO merchant-toggleable setting** for this.

### Identical `sort_order` ties are non-deterministic

Two active rules with the same `sort_order` have **no tiebreaker** (not id, creation date, or name) — order between them is unspecified. **Set distinct priorities** when evaluation order matters.

### Drag-reorder normalises priorities to 1..N

Drag-dropping in the rules list reassigns `sort_order` to `1, 2, 3, …` (highest = top). Manually-edited gaps like `100, 50, 25` flatten to `3, 2, 1` after the first drag-reorder.

## Related

- [[apps-cart-rules]] — hub.
- [[cart-rule]] — Cart Rule entity.
- [[cart-rules-conditions]] — the filter taxonomy each row evaluates against.
- [[cart-rules-actions]] — where the cents-vs-percent value scale is set.
- [[cart-rules-scoping]] — what makes an action cart-level vs product-level.
- [[cart-rules-cooldowns]] — date / status / priority gating that precedes stacking.
- [[marketing-discounts]] — Discounts evaluate FIRST; Cart Rules see the discounted basis.
- [[discount-stacking]] — cross-system stacking matrix.
- [[cart-rules-known-issues]] — sort_order non-determinism; empty-row-trigger bug; A/B testing not supported.

## Open questions

None.
