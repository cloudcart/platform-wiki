---
type: concept
nav_path: "Concept → Storefront known issues → Listing & search"
aliases: ["Storefront listing issues", "Storefront search issues", "Filter sidebar issues", "Infinite scroll issues", "Category count placeholder"]
tags: [storefront, listing, search, filters, issues]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[storefront-known-issues]]. See the hub for the other aspects (framework, inventory, discount codes, cart lifecycle, display + customer, pending bugs).

# Storefront issues — listing & search

## Definition

The listing-and-search entries cover behaviours on **category pages, search pages, and the storefront filter sidebar** — the parts of the storefront where the customer browses and narrows down products. These entries split across **By design**, **UX trade-off**, **Known bug**, and **Pending fix** categories — unlike the inventory + discount-code groups which are all By-design.

Four catalogue entries are in this group: empty-query handling on the search page (By design), filter-sidebar state on back-button (UX trade-off), infinite-scroll scroll-position loss (UX trade-off), the `products_count = 0` placeholder on category responses (Known bug), and the scalar-guarded search query (Pending fix). The scalar-guard + category-count entries are also surfaced under [[storefront-issue-pending-bugs]] for cross-aspect visibility on actual defects.

## Scope

Covered:

- Empty-search-query handling.
- Filter-sidebar back-button state preservation.
- Infinite-scroll back-button scroll-position.
- Category-count placeholder on category-list responses.
- Scalar-guarded search query (Pending fix entry).

Not covered:

- The search ranking algorithm or relevance scoring — see [[storefront-architecture]] for the search index read path.
- Filter configuration on the admin side — see the products-filters admin feature page when one exists.
- Per-theme filter rendering — theme-specific.

## Contrasts

- **Empty query By design vs broken** — entry 14 is By design. The search handler scalar-guards non-string payloads and falls back to an empty string, and the listing renders with zero results rather than a 404 or PHP error. This was a deliberate fix to block scanner-induced PHP warnings (`?query[$eq]=...`).
- **Filter sidebar state vs scroll position** — entry 20 is a UX trade-off. The category page re-fetches from cache on back-navigation; query-string filter state may not restore on all themes. Workaround: use bookmarkable filter URLs (the URL DOES contain the filter selection); browser back from a product detail typically restores state, but back from a deeper page may not.
- **Infinite scroll trade-off vs broken scroll** — entry 21 is a UX trade-off. Themes that use infinite-scroll (load-more) re-render from the first page on back-navigation — the customer lands at the top of the listing, not at the product they clicked. Use a paginated theme variant if scroll-position-on-back is critical.
- **`products_count = 0` placeholder vs zero-product category** — entry 26 is a **Known bug**. The category listing controller returns `'products_count' => 0` with a TODO marker — the value is a placeholder, not a real count. (verify) merchant impact on storefront vs admin — if the storefront's category-card display reads this value directly, the merchant sees `0` next to category names that have products.
- **Scalar-guard search fix vs ongoing scanner attacks** — entry 30 is a **Pending fix** documented for completeness. Behaviour for the customer is unchanged (the term is treated as empty). No merchant action needed.

## Where it applies

The five catalogue entries:

| # | Behaviour | Affected page(s) | Category | What to tell the merchant |
|---|---|---|---|---|
| 14 | Empty search query (`?query=` or `?q=`) returns the search page with no error | Storefront search | By design | The search ajax endpoint scalar-guards non-string payloads and falls back to an empty string — the listing renders with zero results rather than 404. This was a deliberate fix to block scanner-induced PHP warnings (`?query[$eq]=...`). |
| 20 | Filter sidebar state resets on browser back-button | Category listing, search | UX trade-off | The category page re-fetches from cache on back-navigation — query-string filter state may not restore on all themes. Workaround: use bookmarkable filter URLs (the URL DOES contain the filter selection); browser back from a product detail typically restores state, but back from a deeper page may not. (verify) per theme. |
| 21 | Infinite-scroll category page loses scroll position on back-button | Category listing | UX trade-off | Themes that use infinite-scroll (load-more) re-render from the first page on back-navigation — the customer lands at the top of the listing, not at the product they clicked. Use a paginated theme variant if scroll-position-on-back is critical. (verify) which themes use infinite-scroll vs pagination. |
| 26 | Category page count of products is shown as `0` (placeholder) | Category listing (admin nav-tree, also reflected in storefront category meta) | Known bug | Category responses return `'products_count' => 0` with a TODO marker. (verify) merchant impact on storefront vs admin. |
| 30 | Scalar-guarded search query — `?query[$eq]=foo` no longer triggers PHP "Array to string conversion" warning | Storefront search | Pending fix | A scalar-guard was introduced after 62 such warnings in 24h. Behaviour for the customer is unchanged (the term is treated as empty). This is documented for completeness — no merchant action needed. |

### Support-agent quick path per entry

- **Entry 14** → By design; reassure the merchant the page is intentional.
- **Entry 20 / 21** → UX trade-off; explain rationale + workaround (paginate, bookmarkable URLs).
- **Entry 26** → Known bug; acknowledge symptom without committing to a date. If the merchant is seeing `0` on storefront category cards, suggest the workaround of disabling the count display in the theme until the fix lands.
- **Entry 30** → Pending fix; customer-side behaviour is unchanged.

## Related

- [[storefront-known-issues]] — hub.
- [[storefront-issue-framework]] — the four categories.
- [[storefront-issue-pending-bugs]] — entries 26 + 30 also live there.
- [[storefront-architecture]] — the search index read path for category + search.
- [[product-visibility]] — the full "why isn't my product showing in listings / search?" checklist (the index-sync delay is one item).

## Open Questions

- Does the filter sidebar reliably preserve state on back-button across every theme, or only on those that use query-string-driven filters? (verify per theme.)
- Which storefront themes use infinite-scroll category pages vs paginated ones? (verify the full list — zora-new, echappe, themex, knowledge-tmarket, jeans-gameon all need checking individually.)
- For the `products_count = 0` bug — does this affect the storefront's category-card display, or only the admin nav-tree? (verify by reading the consumer.)
