---
type: entity
aliases: ["Smart Collection rule builder", "Smart Collection criteria", "Collection conditions", "Selection rules", "Smart Collection fields and operators", "Условия на колекция"]
tags: [catalog, products, collections, smart-grouping, rules, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[smart-collection]]. See the hub for the other aspects (evaluation, storefront, discount link, vs category, management).

# Smart Collection — the rule builder

## Identity

The **rule builder** is the criteria editor on the Smart Collection edit modal. It defines *which* products a [[smart-collection|Smart Collection]] includes. Membership is not a hand-picked list — it is the set of products that satisfy every rule the merchant writes. The merchant adds one or more **criteria rows** (`rows[]`); each row is a single rule built from three parts:

- **Field** — what product attribute to match on (e.g. Price, Tags, Categories).
- **Operator** — how to compare (e.g. Includes, More than, Between).
- **Value** — what to compare against (a multi-select picker, a number, or Yes / No, depending on the Field).

Each row also carries a `sort_order` controlling its position in the AND-chain. The actual computation of which products match — and the caching of the result — is covered in [[smart-collection-entity-evaluation]].

## Aliases

- "Rule builder" / "criteria editor" — the merchant-facing names for this part of the modal.
- "Conditions" / "criteria" / "rules" — interchangeable terms for the rows.
- "Field / Operator / Value" — the three parts of each row.
- Bulgarian: "Условия на колекция", "Правила".

## Key Attributes

### Rules within a collection are AND-combined

Every criteria row in a single Smart Collection is **AND-combined** with every other. A collection with three rows — *"Category includes Shoes"*, *"Price between 100 and 200"*, *"Tag includes sale"* — matches a product ONLY when all three conditions hold. There is **no OR logic at the collection level** and **no "match ANY" mode**. To express OR (e.g. *"Red shirts OR Blue trousers"*), the merchant creates two separate Smart Collections and surfaces both in the storefront — or links a single [[discount]] to both (see [[smart-collection-entity-discount-link]]).

### 10 supported criteria fields

| Field | Compares against |
|-------|------------------|
| **Products** | Specific product IDs (multi-select autocomplete from the merchant's catalog). |
| **Categories** | Specific categories (multi-select autocomplete from [[products-categories]]). |
| **Discounts** | Currently-active discounts (limited to fixed / percent / flat, non-shipping, non-customer-restricted). |
| **Manufacturer** | Specific vendors (multi-select from [[products-vendors]]). |
| **Tags** | Product tags (multi-select autocomplete from existing tags). |
| **Price** | Numeric currency value (supports Equal / Not equal / More than / Less than / Between / Not between). |
| **Digital product** | Boolean (is the product digital?). |
| **Sale** | Boolean (is the product on sale?). |
| **New** | Boolean (does the product carry the New flag?). |
| **Category property** | A specific category property + a specific option (e.g. Color = Red). |

### Operators are field-dependent

The Operator dropdown only offers operators valid for the chosen Field:

- **Multi-select fields** (Products / Categories / Discounts / Manufacturer / Tags): **Includes** / **Does not include**.
- **Price**: **Equal** / **Not equal** / **More than** / **Less than** / **Between** / **Not between**.
- **Boolean fields** (Digital product / Sale / New): **Yes** / **No**.
- **Category property**: a property + option pair (e.g. Color = Red).

### Value input shape follows the field

- Product / Category / Vendor / Tag / Discount → multi-select picker.
- Price → number(s) (one value, or two for Between / Not between).
- Booleans → Yes / No.
- Category property → a property + an option pair.

## Where it appears

- [[products-smart-collections]] — the rule builder lives on the Add / Edit modal of this screen.
- [[products-categories]] — source of the Categories criteria field.
- [[products-vendors]] — source of the Manufacturer criteria field.
- [[products-property]] — source of the Category property criteria field.
- [[marketing-discounts]] — source of the Discounts criteria field (active fixed / percent / flat discounts only).

## Related

- [[smart-collection]] — hub.
- [[smart-collection-entity-evaluation]] — how the rules are computed into a cached product list.
- [[product]] — the entity rules match against.
- [[category]] — the Categories field references this.
- [[vendor]] — the Manufacturer field references this.
- [[category-property]] — the Category property field references this.
- [[discount]] — the Discounts field references active discounts.

## Open Questions

None.
