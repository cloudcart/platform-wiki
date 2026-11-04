---
type: concept
nav_path: "Concept → Discount stacking → What the amount comes off"
aliases: ["Discount target meaning", "For every product in the cart", "For each product in the cart", "Orders over", "Per line discount", "Per unit discount", "One amount off the cart", "Fixed code off every line", "Negative cart total", "За всеки продукт в количката", "Поръчки над", "Отстъпка от всеки ред", "Отстъпка за всеки продукт", "Отстъпка веднъж от количката", "Фиксирана отстъпка от цялата количка", "Отрицателна сума в количката"]
tags: [marketing, discounts, targeting, flat, percent, concepts]
plan_gates: []
created: 2026-11-04
updated: 2026-11-04
source_count: 4
---

> Part of [[discount-stacking]]. See the hub for the other aspects (evaluation order, code_apply, cart code slots, uses counter, plan gating, Cart Rules interaction).

# Discount stacking — what the amount comes off

## Definition

The same amount gives a different result depending on two choices: whether the discount has a code, and which target it has. **"For every product in the cart" means every product: a fixed amount comes off each line, or each unit, not once off the cart.** One amount off the whole cart is the "Orders over" target.

## Scope

### Fixed amount

| Target | Without a code | With a promo code | Code PRO condition |
|---|---|---|---|
| **За всеки продукт в количката** / *For every product in the cart* (`all`) | Off each unit of every product. It becomes the product's own price on listings and product pages | The full amount off every line, once per line, whatever the quantity | Same as a promo code |
| **Поръчки над** / *Orders over* (`order_over`) | One amount off the order | One amount off the order | One amount off the order |
| Specific products, categories, vendors, smart collections | Off each unit of those products, as their own price | One amount split across the matching lines in proportion to their value. Any rounding difference lands on the first matching line | One amount per condition, split across its lines |

### Worked example

A 20 EUR discount on a cart of three lines: 2 × 15 EUR, 1 × 50 EUR and 1 × 30 EUR, a subtotal of 110 EUR.

| Discount | Lines after the discount | Subtotal |
|---|---|---|
| No code, every product | 30 (priced below 20, so no discount), 30, 10 | 70 |
| Code, every product | 10, 30, 10 | 50 |
| Code, orders over 50 EUR | One 20 EUR row off the order | 90 |
| Code, only the first two lines | 22.50, 37.50, 30 | 90 |

### Percentage

- **Code, every product or a specific target:** the percentage comes off each matching line.
- **No code, every product or a specific target:** it comes off each unit, as the product's own price.
- **Orders over:** one amount, the percentage of the subtotal.

The sums match apart from rounding. The rounding differs because a no-code percentage is worked out per unit, and a code per line.

### When the amount is larger than what it comes off

| Discount | What happens |
|---|---|
| No code, products | A product whose lowest price is below the amount gets no discount |
| No code, orders over | Not applied, and no other orders-over discount is tried |
| Code, every product or a specific target | Refused when entered if the matching lines add up to less than the amount. Each line has no lower limit, so a line and the total can go below zero. 30 EUR on three lines worth 72.22 EUR in all gives −17.78 EUR |
| Code, orders over | Only the threshold is checked, not the amount. A 40 EUR code with a 13 EUR threshold on a 20 EUR cart gives −20 EUR |
| Code PRO | The amount is not compared with the cart. Lines and the total can go below zero |
| Countdown | Not applied |

### Which target for which aim

- **One amount off the whole cart:** "Поръчки над", with a threshold at or above the amount, so that the amount always fits. The subtotal has to be above the threshold, so a cart of exactly the threshold does not qualify.
- **An amount off each product line:** "За всеки продукт в количката", with an amount below the cheapest line in the cart.
- **A lower price customers see on listings:** a discount without a code.

## Contrasts

- **Per unit vs per line.** Without a code, 2 pieces of a product save twice the amount. With a code, the same line saves the amount once.
- **In the line vs in the totals.** A code for every product or a specific target shows inside each product line, with the code in brackets, and adds no discount row to the totals. An orders-over discount is a row in the totals.
- **Other order-level discounts.** A Countdown and a payment-method discount are worked out on the order, see [[countdown-discount-cart-totals]]. Free shipping takes the shipping row, see [[marketing-discounts-shipping]].

## Where it applies

- [[flat-discount-targeting]] and [[percent-discount-targeting]]: the target on the discount form.
- [[code-pro-fields]]: the conditions of a Code PRO code.
- [[orders-discount-add]]: a code added to an existing order works the same way.
- [[api-discounts]]: `all` means the same through the API.

## Related

- [[discount-stacking]]: hub.
- [[discount-stacking-code-apply]]: lines that already hold a product discount.
- [[discount-stacking-evaluation-order]]: what is worked out first.

## Open Questions

- None known.
