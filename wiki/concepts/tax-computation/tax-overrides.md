---
type: concept
nav_path: "Concept → Tax computation → Overrides"
aliases: ["Tax overrides", "Per-region tax override", "Per-category tax override", "Override precedence", "Category-only override", "Region-only override", "Combined override", "Books reduced VAT"]
tags: [taxes, vat, finance, overrides, precedence, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax-computation]]. See the hub for the other aspects (rate selection, pricing models, OSS, address resolution, order snapshot, fees-vs-VAT).

# Tax — per-category and per-region overrides

## Definition

Once the rate-selection engine has picked the **one** winning VAT rule (see [[tax-rate-selection]]), an override table is consulted **per cart line** to swap the base rate for a different one. Both override types — per-region and per-category — live in **the same table** and are distinguished by which columns are populated (see [[settings-taxes]] *"Per-region overrides + Per-category overrides share ONE storage table"*).

The override matcher iterates rows sorted by `category_id` DESC (overrides that carry a category come first) and selects the **first** row that matches both the cart line and the customer's address. The override's `tax` value then replaces the parent rule's base rate for that line.

## Scope

Covered:

- The 4-tier precedence ladder (combined → category-only → region-only → base).
- The order of evaluation that produces that ladder.
- The "no address" carve-out.
- The zero-override display rule.
- Worked example for *"books at a reduced rate"*.

Not covered here:

- Which parent VAT rule was picked — see [[tax-rate-selection]].
- The per-order snapshot of the resulting rates — see [[tax-order-snapshot]].
- Fees (additive, not per-line) — see [[tax-fees-vs-vat]].

## Precedence ladder — verified at the matcher

The matcher (verified against the per-line tax-resolution code) iterates overrides sorted by `category_id` DESC and selects the **first** one that matches the cart line and the customer's address. Precedence in practice:

1. **Combined match** — override where `category_id` matches the line's category AND (`state_iso_2` is null OR matches the customer's state). Wins first because the sort puts category-bearing rows ahead.
2. **Category-only match** — override where `category_id` matches the line's category AND `state_iso_2` is null. Wins SECOND only if no combined match found; the loop reaches it because it's in the category-sorted bucket.
3. **Region-only match (no category)** — override where `category_id` is null AND `state_iso_2` matches the customer's state. Wins THIRD — only reached when no override with a matching category exists (because category-bearing rows sort first and short-circuit the loop on the first match).
4. **Base rate** — the parent Tax's `tax` value applies when no override matches.

**Important correction:** older wiki phrasing claimed *"per-category beats per-region beats base rate"* as a clean 3-tier precedence. The actual behaviour is more nuanced — **category-only fires BEFORE region-only** when both exist independently. A region-only override only fires when NO category override matches the line's category. Merchants who set both expect them to combine — they don't; the category override wins outright when the line's category matches it.

## Contrasts

- **Combined vs category-only vs region-only** — three distinct override shapes share one table; the matcher picks the first that fits, with category-bearing rows ranked higher.
- **Per-line override vs per-order base** — overrides fire on every cart line independently. A cart with one book and one non-book line uses two different rates in the same order (see worked example).
- **Override `tax = 0` vs no override** — an explicit zero-rate override STILL renders on the invoice (so the customer sees the breakdown line), whereas a missing override silently uses the base rate.

## No-address carve-out

When the customer has **no address** (very rare — early-checkout draft state), the matcher only considers category-only overrides with `state_iso_2` null. Region-only overrides are skipped entirely. This avoids "matched against the empty string" false hits.

## Display rule — explicit zero still renders

An override with computed amount of **0** STILL renders on the invoice (so the customer sees the breakdown like *"Books at 9%: 0.00 EUR"*) — verified at the totals-aggregator step. Without this carve-out, zero-VAT overrides would silently disappear and the merchant couldn't show the customer that a reduced rate was applied.

## Worked example — books at a reduced rate

Setup:

- Base VAT rule for the country at 20%.
- Per-category override on the same rule: category "Books" → 9%.

Cart:

- One paperback (category Books) at `18.00 BGN` (gross).
- One mug (category Home) at `12.00 BGN` (gross).

Result:

- Book line: matched override → 9% applied. At GROSS pricing the net is `18.00 / 1.09 = 16.51`, VAT = `1.49`.
- Mug line: no matching override → base 20% applies. Net `10.00`, VAT `2.00`.
- Invoice prints **two tax lines**, one per rate.

## Where it applies

- [[settings-taxes]] — the override editor is on the same screen as the parent VAT rule.
- [[category]] — `category_id` is the join key for per-category overrides.
- [[checkout-flow]] — the matcher runs per cart line at checkout.
- [[orders-details]] — the order's tax breakdown shows the resulting per-line rates.

## Related

- [[tax-computation]] — hub.
- [[settings-taxes]] — management screen + override editor.
- [[category]] — drives per-category overrides.
- [[settings-geo-zones]] — `state_iso_2` for per-region overrides.

## Open Questions

None.
