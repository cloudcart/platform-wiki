---
type: concept
nav_path: "Concept → Storefront known issues → Inventory display"
aliases: ["Storefront inventory issues", "Out-of-stock display issues", "Oversell race condition", "Bundle stock display"]
tags: [storefront, inventory, stock, oversell, bundle, issues]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[storefront-known-issues]]. See the hub for the other aspects (framework, discount codes, cart lifecycle, listing / search, display + customer, pending bugs).

# Storefront issues — inventory display

## Definition

The inventory-related entries in the storefront-issues catalogue. These are the most-asked symptoms in support tickets because the per-Variant stock model + decrement timing + oversell semantics produce behaviours that **look wrong** to merchants who think of stock as a single per-product counter. Every entry below is **By design** — the platform is doing exactly what its rules say it should — and the agent's job is to surface the rule from [[inventory-tracking]] and the aspect pages it splits into.

Six catalogue entries are in this group: automatic restock on cancel, race-condition oversells when timing is `paid`, the clamp-at-0 rule, "Out of stock" still showing Add-to-cart with `continue_selling = yes`, the variant-picker "Out of stock" label, and bundle stock derivation from child variants.

## Scope

Covered:

- The six By-design entries listed above — full catalogue rows + the *what to tell the merchant* line.
- Cross-reference to the underlying [[inventory-tracking]] sub-aspects.

Not covered:

- The mechanics of the inventory model itself — see [[inventory-tracking]] and its sub-pages.
- The actual Known-bug entries that touch inventory — none currently in the catalogue; new ones go into [[storefront-issue-pending-bugs]].
- Admin-side inventory bugs — those belong on the affected admin feature page ([[products-products]], [[products-inventory]]).

## Contrasts

- **Automatic restock vs broken cancellation** — entry 1 is **By design** (cancellation/refund credits stock back), not a bug. See [[inventory-restock]] for the per-line decrement-tracking flag that prevents double-credit.
- **Race-condition oversell vs random oversell** — entry 2 is driven by the `order_status_for_quantity_decrease` setting on [[settings-cart]]. With `paid` semantics, two pending orders can race for the same unit; with `pending` semantics, stock is reserved at submit. See [[inventory-decrement-timing]] — this is a deliberate choice, not a bug.
- **`quantity` never goes negative vs ledger gap** — entry 3 is the clamp-at-0 rule. To know how many units the merchant owes customers, count outstanding paid orders against the 0-stock variant; do NOT read it off the variant `quantity` field. See [[inventory-oversell]].
- **`continue_selling` + Add-to-cart at 0 vs broken out-of-stock check** — entry 4. With `continue_selling = yes`, the storefront accepts orders at `quantity = 0` (backorder semantics). See [[inventory-oversell]].
- **"Out of stock" label vs disabled option** — entry 5. The variant picker keeps the option visible with an "Out of stock" label so the customer knows the variant exists. To capture demand, the merchant can request a "Notify me" CTA via [[products-missing-product]].
- **Bundle stock derived from children vs bundle stock as its own counter** — entry 6. Bundle availability comes from the **lowest** child-variant quantity divided by required units per bundle line. See [[inventory-bundle-stock]].

## Where it applies

The six catalogue entries:

| # | Behaviour | Affected page(s) | Category | What to tell the merchant |
|---|---|---|---|---|
| 1 | Stock automatically returns to the variant when an order is cancelled or refunded | Product detail, cart, checkout | By design | This is the intended restore semantic from [[inventory-tracking]] — cancellation/refund credits the units back so the variant returns to in-stock. The platform tracks per-line whether decrement happened, so stock is never double-credited. See [[inventory-restock]]. |
| 2 | Two customers can buy the same last unit when payment is slow | Product detail, cart, checkout | By design | Driven by the `order_status_for_quantity_decrease` setting on [[settings-cart]]. If set to `paid`, stock decrements only when the order is paid — so two `pending` orders can race for the same unit. Switching to `pending` semantics reserves stock at submit. See [[inventory-decrement-timing]]. |
| 3 | Variant `quantity` never goes negative even when 5 customers buy a 0-stock variant with "Continue selling" ON | Product detail, admin variant list | By design | The platform clamps `quantity` at 0 on every decrement. To see how many units the merchant owes customers, count outstanding paid orders against the 0-stock variant — do NOT read it off the variant `quantity` field. See [[inventory-oversell]]. |
| 4 | "Out of stock" still shows "Add to cart" when `continue_selling = yes` | Product detail, embed modules | By design | When the parent product has `continue_selling = yes`, the storefront accepts orders at `quantity = 0` (backorder semantics). The variant's `data-continue-selling` attribute on the quantity input is what allows this. See [[inventory-oversell]]. |
| 5 | Variant picker shows "Out of stock" label instead of disabling the option when a variant is out | Product detail | By design | The picker uses an out-of-stock label rendering, not disabled options — this keeps the option visible so the customer knows it exists. The merchant can request a "Notify me" CTA via [[products-missing-product]] to capture demand. |
| 6 | Bundle product shows in-stock even when one child variant is at 0 (or shows out-of-stock when children are in stock) | Product detail, category listing | By design | Bundle stock is derived from the **lowest** child-variant quantity divided by required units per bundle line. The bundle is out-of-stock when any required child is depleted. See [[inventory-bundle-stock]]. |

### Support-agent quick path

All six entries are **By design**. The agent's response is *"this is the documented behaviour from the inventory model — here is the rule"* and a wikilink into [[inventory-tracking]] (or the appropriate sub-aspect). If the merchant insists the symptom is wrong, escalate to verify against the current code; if confirmed wrong, the entry would move into [[storefront-issue-pending-bugs]].

## Related

- [[storefront-known-issues]] — hub.
- [[storefront-issue-framework]] — the four categories.
- [[inventory-tracking]] — concept hub.
- [[inventory-decrement-timing]] — the `paid` vs `pending` setting that drives entry 2.
- [[inventory-restock]] — the per-line decrement-tracking flag from entry 1.
- [[inventory-oversell]] — the clamp-at-0 rule from entries 3 + 4.
- [[inventory-bundle-stock]] — bundle availability derivation for entry 6.
- [[products-missing-product]] — Notify-me capture for entry 5.
- [[settings-cart]] — `order_status_for_quantity_decrease`.

## Open Questions

- Are there themes where the variant picker DOES disable out-of-stock options instead of labelling them? (verify per theme — if yes, entry 5 is theme-conditional.)
