---
type: feature
nav_path: "Apps → Cart Rules → Conditions"
route_name: ""
route_path: ""
aliases: ["Cart rule conditions", "Cart rule triggers", "Cart rule filters", "Condition types", "Filter taxonomy", "Operator pools"]
tags: [apps, cart-rules, marketing, promotions, conditions, triggers]
plan_gates: ["cart_rules_conditions"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-cart-rules]]. See the hub for the other aspects (actions, scoping, stacking, cooldowns, examples, known issues).

# Cart Rules — Conditions (triggers)

## Purpose

A **condition** (also called a "trigger") is the *if* in *if-this-then-that*: it decides whether a row's action fires against a given cart. Every condition is a 4-part declaration — `condition_type` → `filter_type` → `value_type` (operator) → `value` (plus optional `sub_value` / `records` / `operator` for record-set matching).

Pick ONE `condition_type` first; that choice limits which `filter_type` values are allowed; the `filter_type` then fixes which operator pool (numeric / string / record-set) the comparison may use.

Triggers within a row are joined with **AND**. To express OR, use multiple rows in one rule, or multiple rules. The `cart_rules_conditions` plan feature caps row-triggers per row (default fallback: 5).

## Where to find it

Each row in the **rule editor** at `/admin/apps/cart-rules/rules/create` (or `/edit/{id}`) has a *Triggers* section. Click *Add condition* to add a row-trigger; the picker exposes the four parts above. Action-triggers (a different, narrower list) live inside the row's *Action* block — see [[cart-rules-actions]].

## What the merchant can do here

- Add up to `cart_rules_conditions` row-triggers per row (default 5).
- Pick a `condition_type`: **Cart**, **Product**, or **Customer**.
- Pick a `filter_type` allowed for that condition type.
- Pick a comparison operator from that filter's operator pool.
- Provide the comparison value (with optional `sub_value` for `between`).

## Settings & fields

### Cart-level vs product-level — the distinction that changes the rule's meaning

The **`condition_type`** decides *what* is measured, and picking the wrong scope silently changes what the rule means:

- A **`cart`** filter measures the **whole cart** — all products together.
- A **`product`** filter measures **one specific product line** — the product(s) the row scopes to.

The sharpest trap is **quantity**:

| Merchant intent | Correct filter | What it measures |
|---|---|---|
| *"Buy **2 or more of a specific product**"* | **Product → `product_quantity`** (UI: *Продукт → Количество на продукта*), operator `gte`/`gt`, value `2` | the units of **that one product line** |
| *"Cart has **5+ items total**" (any products)* | **Cart → `cart_quantity`** (UI: cart quantity) | the **sum of every line's quantity** — cart-wide |
| *"Cart has **3+ different products**"* | **Cart → `cart_products_count`** (UI: *Количка → Брой продукти в количката*) | the number of **distinct product lines** — cart-wide |

So *"buy 2 of product X → discount"* must be **Product → `product_quantity` ≥ 2** (usually paired with a Product record-set condition selecting product X or its category). Using `cart_quantity` or `cart_products_count` for this is **wrong** — they fire for **any** cart with 2 total units / 2 different products, not "2 of X". The same cart-vs-product split applies to **value**: `product_amount` / `product_line_amount` = one line's value; `cart_amount` = the whole cart's value.

### Cart-level filters (`condition_type = "cart"`)

| Filter (`filter_type`) | What it checks | Value type |
|---|---|---|
| `cart_amount` | The **whole cart's** total value (all products, post-discount) — not one product | numeric (cents) |
| `cart_products_count` | Number of **different products** in the cart (distinct product lines, `products.keyBy(product_id).count`) — cart-wide, **not** the units of one product | numeric |
| `cart_quantity` | **Total units** across all products (`products.sum('quantity')`) — cart-wide, **not** one product's quantity | numeric |

### Product-level filters (`condition_type = "product"`)

| Filter (`filter_type`) | What it checks | Notes |
|---|---|---|
| `product` | Specific product IDs | Record-set: operator IN / NOT IN + array of product IDs |
| `vendor` | Specific vendor(s) | Record-set IN / NOT IN |
| `category` | Specific category/ies | Record-set IN / NOT IN |
| `tag` | Specific tag(s) | Record-set IN / NOT IN |
| `selection` | Specific smart-collection(s) | Record-set IN / NOT IN |
| `product_title` | Title comparison | String (contains / equals / starts / ends) |
| `product_variant` | A variant attribute (Size = L) | String |
| `product_option` | A line option (engraving, gift wrap selected) | String — see [[products-options-overview]] |
| `product_new` | Product flagged "new" | yes / no |
| `product_featured` | Product is featured | yes / no |
| `product_sale` | Product is on sale | yes / no |
| `product_amount` | Value of **one specific product line** (its price × qty) — not the cart total | numeric (cents) |
| `product_line_amount` | Same as `product_amount` — one line's value | numeric (cents) |
| `product_quantity` | **Units of one specific product** (that product's line quantity). Use this for *"N or more of a particular product"* (UI: *Продукт → Количество на продукта*) — **not** the cart-wide `cart_quantity` / `cart_products_count` | numeric |

### Customer-level filters (`condition_type = "customer"`)

| Filter (`filter_type`) | What it checks | Notes |
|---|---|---|
| `order_amount` | Sum of the customer's **COMPLETED** past order totals | numeric. Pending, failed, cancelled, refunded and voided orders do NOT count — a customer who spent 200 EUR but had every order cancelled will NOT match `order_amount > 100`. |
| `order_count` | Number of the customer's **COMPLETED** past orders | numeric. 5 pending orders awaiting payment will NOT match `order_count >= 3` until they reach `paid` / `completed`. |
| `customer_group` | Membership in specific group(s) | Record-set, operator IN / NOT IN. Use the auto-created **Guests** group to target guest checkouts; `NOT IN Guests` targets registered customers — there is no separate `is_registered` / `is_guest` filter. |

**Customer filters cannot check:** campaign / segment membership (Cart Rules don't read it), the date of the last order, or average order value — only the lifetime aggregates above are exposed. To target any of these, build a [[marketing-segments|Segment]], assign its members to a custom group via [[customers-custom-groups]], then trigger on the `customer_group`.

### Comparison operators — `value_type` vs `operator` are TWO DIFFERENT FIELDS (the #1 mistake)

Every condition shows what looks like a single "operator" dropdown, but depending on the filter it writes to **one of two different backend fields**. Confusing them is the most common way a rule silently fails:

| Filter family | UI dropdown reads | Field that holds the choice | Allowed values |
|---|---|---|---|
| **Record-set** — `product`, `vendor`, `category`, `tag`, `selection`, `customer_group` | *In / Not in* | **`operator`** | `in`, `not_in` |
| **Numeric** — `product_quantity`, `cart_quantity`, `cart_products_count`, `product_amount`, `product_line_amount`, `cart_amount`, `order_amount`, `order_count` | *≥ / > / = / between …* | **`value_type`** | `gte`, `gt`, `lte`, `lt`, `equal`, `not_equal`, `between` |
| **String** — `product_title`, `product_variant`, `product_option` | *contains / equals / starts / …* | **`value_type`** | `contains`, `not_contains`, `equal`, `not_equal`, `start`, `end`, `in`, `not_in` |

> **The trap (verified from a real broken rule):** on a `product_quantity` condition the numeric comparison was written to the **`operator`** field (`operator: "gte"`) instead of **`value_type`**. `value_type` stayed **null**, so the editor rendered the operator as **"Select" / "undefined"** — *"product's quantity **undefined** 2 qty"* — the condition never matched and the whole promotion silently did nothing. **`operator` accepts ONLY `in` / `not_in`** (record-set inclusion); it is NOT the ≥/>/= dropdown. A numeric comparison put there is meaningless.

**So *"2 or more of a product"* is:** `condition_type=product`, `filter_type=product_quantity`, **`value_type=gte`**, `value=2`, with **`operator` left null** (nothing to include/exclude). Only its paired record-set trigger — e.g. `category`, `operator=in`, `records=[…]` — uses `operator`. One row, two triggers, two DIFFERENT operator fields.

Available operators depend on the filter's data type. There are **three parallel operator pools** — numeric, string, record-set — and each filter draws from exactly one. Picking an operator outside the filter's pool silently returns "no match".

**Numeric pool** — for amount, quantity, line-amount, order-amount, order-count filters:

| Operator (`value_type`) | Behaviour |
|---|---|
| `equal` / `not_equal` | Exact match |
| `gt` / `gte` | Greater than / Greater than or equal |
| `lt` / `lte` | Less than / Less than or equal |
| `between` | Range — requires both `value` (low bound) AND `sub_value` (high bound). A null on either side means "no bound" (e.g., `value=10, sub_value=null` means *"≥ 10 and no upper limit"*). |

**String pool** — for `product_title`, `product_variant`, `product_option`. All comparisons are **case-insensitive** (both sides lowercased first), so *"Red T-Shirt"* matches condition value *"red"* under `contains`:

| Operator (`value_type`) | Behaviour |
|---|---|
| `equal` / `not_equal` | Exact match |
| `contains` / `not_contains` | Substring search |
| `start` / `end` | Starts with / Ends with |
| `in` / `not_in` | Treats the cart-side value as a comma-separated list of patterns and wildcard-matches each against the condition value. Used when the cart-side value is itself a delimited list. |

**Record-set pool** — for vendor / category / tag / selection / product / customer_group:

| Operator | Behaviour |
|---|---|
| `in` / `not_in` | The condition holds an array of record IDs (`records[]`); the cart-side value must be present in / absent from that array. |

Record-set conditions require `operator` + `records` and **forbid** `value` / `value_type`.

### Value scale — provide the HUMAN value; it is stored ×100

When you **create or edit** a rule — the admin form **and** the API both go through the same save helper — you provide the **human value**, and the platform scales it on save (verified: the platform code → `toIntegerPrice` for money, `× 100` for the action percent):

| Kind | Filters / fields | You send | Stored |
|---|---|---|---|
| **Money** | `cart_amount`, `product_amount`, `product_line_amount`, `order_amount`, action `value_type=amount` | the currency amount — **`50`** for 50 EUR | cents (`5000`) |
| **Percent** | action `value_type=percent` | the whole percent — **`10`** for 10% | ×100 (`1000`); 50% → `5000` |
| **Quantity / count** | `cart_quantity`, `cart_products_count`, `product_quantity`, `order_count` | the plain integer — **`2`** means 2 | as-is (no scaling) |

So *"cart over 50 EUR"* is **`value: 50`**, not `5000` — sending the already-×100 value would set a **100× threshold** (5000 EUR). The **stored ×100** form (money in cents, percent×100) is only what the internal cart-level stacking comparison ranks by (see [[cart-rules-stacking]]); you never enter it.

### `sub_value` rule

`sub_value` is **REQUIRED** when `value_type = "between"` (numeric pool only) and must be null otherwise (schema-enforced on save).

### Schema validation on save

The platform validates the rule structure against a strict schema before saving:

- `filter_type` must match the `condition_type` taxonomy (product filters only when `condition_type=product`, etc.).
- Record-set filters (product / vendor / category / tag / selection / customer_group) REQUIRE `operator` (in/not_in) + `records`; `value` and `value_type` must be null.
- Numeric value filters (`cart_amount`, `cart_products_count`, `cart_quantity`, `product_amount`, `product_line_amount`, `product_quantity`, `order_amount`, `order_count`) require `value_type` from: `between`, `gt`, `gte`, `equal`, `not_equal`, `lte`, `lt` — a **null `value_type` is rejected** with *"Field is required"* (this is where a comparison mis-written into `operator` gets caught).
- **Caveat — the AI generator bypasses this.** The two validators differ: the standard form / API save requires a real `value_type` on numeric filters, but the **AI rule generator** uses a separate schema that *permits* `value_type: null` (and restricts `operator` to `in`/`not_in`). So an AI-built rule can be persisted in the broken "undefined operator" state above without being caught until a human opens and re-saves it. **After any AI generation, confirm each numeric condition shows a real operator (≥ / > / =), not "Select".**
- Boolean filters (`product_new`, `product_featured`, `product_sale`) require `value` from `["yes", "no"]` and a null `value_type`.
- `sub_value` REQUIRED when `value_type = between`, null otherwise.
- AI-generated rules conform by construction, but the same Save-time validation still runs.

## Business rules

### Product-level triggers in a row are matched PER-PRODUCT (intersected)

When a row has several **product-level** triggers, they are evaluated against the **same product line**: the engine keeps the set of cart products that satisfy each product trigger and **intersects** them (`array_intersect`). So a row with **`category = X` AND `product_quantity ≥ 2`** matches only if **one product is BOTH in category X AND has quantity ≥ 2** — i.e. *"2 or more of a product in category X"*. It does **not** match "1 product from category X plus 2 of some unrelated product". This intersection is exactly what makes *"buy N of a specific product / category → discount"* expressible: pair a product record-set trigger (`product` / `category` / `vendor` / `selection` / `tag`) with **`product_quantity`** in the same row.

**Cart-level and customer-level triggers are NOT per-product** — `cart_quantity`, `cart_amount`, `cart_products_count`, `order_amount`, `order_count` measure the **whole cart / customer**, independent of which product matched. (Subtlety: when a row also has product triggers, `cart_products_count` counts within the product-matched set, not the entire cart.)

- **AND across triggers within a row.** All triggers in the row must match for its action to fire.
- **OR across rows of the same rule** is not what it looks like — multi-row rules are an OR-fallback ladder where only ONE row fires per rule. See [[cart-rules-stacking]] for the reverse-evaluation rule.
- **You provide the human value; the save helper multiplies it by 100 (see "Value scale" below).** A *"cart over 50 EUR"* trigger is **`value: 50`**, NOT `5000`. Money is stored as cents; the action percent is stored ×100; quantity/count are plain integers. This stored form is what the cart-level stacking comparison uses — see [[cart-rules-stacking]].
- **Cart-side values match the POST-DISCOUNT amount.** Each line's amount is taken after [[marketing-discounts]] apply, so *"cart_amount > 100"* tests the discounted total, not the catalog total.
- **Deleted records silently disappear from record-set triggers** — see [[cart-rules-known-issues]] for the orphan-reference behaviour (especially dangerous for `not_in`).

## Related

- [[apps-cart-rules]] — hub.
- [[cart-rule]] — Cart Rule entity that holds these conditions.
- [[cart-rules-actions]] — actions also use this filter taxonomy (with extras like `product_lowest_price`).
- [[cart-rules-stacking]] — how matched rules interact; the cents-vs-percent scale gotcha.
- [[cart-rules-known-issues]] — empty-row-trigger bug; deleted-reference orphaning.
- [[products-options-overview]] — product options referenced by `product_option`.
- [[marketing-segments]] — segment → group bridge for advanced customer targeting.
- [[customers-custom-groups]] — custom customer groups referenced via `customer_group`.

## Open questions

None.
