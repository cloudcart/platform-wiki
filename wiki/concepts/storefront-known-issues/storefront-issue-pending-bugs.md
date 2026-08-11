---
type: concept
nav_path: "Concept → Storefront known issues → Pending bugs"
aliases: ["Storefront known bugs", "Storefront pending fixes", "Crawler 404 order return", "Cross-sell empty", "Customer-account order detail missing weight", "COD-only shipping mismatch", "Checkout step jumping"]
tags: [storefront, bugs, pending-fix, issues]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[storefront-known-issues]]. See the hub for the other aspects (framework, inventory, discount codes, cart lifecycle, listing / search, display + customer).

# Storefront issues — pending bugs

## Definition

The pending-bugs aspect catalogues every entry tagged **Known bug** or **Pending fix** in the storefront-issues catalogue — plus a small number of behaviours marked *By design (verify)* that engineering has flagged as needing confirmation. Unlike the other aspect pages (which are mostly By design), every entry here either has an acknowledged defect or is awaiting verification before its category settles.

Six catalogue entries are in this group:

- Entry 23 — Crawler 404 on order return page (By design; included here because merchants sometimes misread it as a bug).
- Entry 24 — Cart side-panel cross-sell empty (Known bug, verify).
- Entry 25 — Customer-account order missing per-line product parameters + weight (Known bug).
- Entry 27 — Checkout COD-only shipping mismatch (Known bug, verify per courier).
- Entry 28 — Checkout step-jumping by URL (By design, verify edge cases).
- Entry 30 — Scalar-guarded search query (Pending fix) — also cross-referenced in [[storefront-issue-listing-search]].
- Entry 26 — Category `products_count = 0` placeholder (Known bug) — also cross-referenced in [[storefront-issue-listing-search]].

## Scope

Covered:

- Every entry whose category is **Known bug** or **Pending fix**.
- Entries marked **By design (verify)** that engineering wants confirmed.
- The single By-design entry merchants frequently misread as a bug (entry 23).

Not covered:

- Confirmed By-design behaviours — those live in [[storefront-issue-inventory-display]], [[storefront-issue-cart-discount-codes]], [[storefront-issue-cart-lifecycle]], [[storefront-issue-display-and-customer]], and the relevant rows of [[storefront-issue-listing-search]].
- Theme-specific defects — those belong on the theme's own page when one exists.
- Per-store quirks — those belong on the store's internal account notes.

## Contrasts

- **Known bug vs Pending fix** — both acknowledge the symptom is wrong. Known bug has no committed ship date; Pending fix has development underway with a release window committed. The support-agent response differs (do not promise a date for Known bug; mention release-notes ETA for Pending fix). Entries 24-27 are Known bug; entry 30 is Pending fix.
- **By design (verify) vs Known bug** — *(verify)* entries are categorised pending a backend check; the entry is the **first** thing to confirm if a ticket touches it. Entries 18, 24, 27, 28 carry *(verify)* markers — the agent should not assume the categorisation is final.
- **Crawler 404 By design vs broken order page** — entry 23 looks like a bug (the merchant sees `404` in their Google Search Console crawl logs against `/checkout/return/...` URLs) but is intentional SEO hygiene — order-return pages must never enter the search index. The agent surfaces the rule from [[seo-handling]].
- **Bug visibility for the customer vs for the merchant** — entry 25 (customer-account order detail missing per-line parameters + weight) is visible to **both** the customer (on their account-order page) and the merchant (on the checkout return order details). Entry 26 (`products_count = 0`) is primarily an admin-side display defect — (verify) whether the storefront's category-card display also reads the bad value.

## Where it applies

The seven catalogue entries in this aspect:

| # | Behaviour | Affected page(s) | Category | What to tell the merchant |
|---|---|---|---|---|
| 23 | Crawlers see HTTP 404 on the order return page | Checkout return | By design | The order-return page returns `404` with `X-Robots-Tag: noindex` when the request is identified as a crawler. This is intentional SEO hygiene — order pages must never enter the index. See [[seo-handling]]. |
| 24 | Cart side-panel cross-sell block is sometimes empty even when cross-sells are configured | Cart drawer | Known bug (verify) | A `@todo for CrossSell` marker exists in the cart drawer template. (verify) whether the marker reflects a current defect or a historic note. |
| 25 | Order detail in the customer account is missing per-line product parameters + weight | Customer account, checkout return | Known bug | A `ToDo: product parameters and weight doesn't work` comment exists in both the customer-account order template and the checkout-return order-details template. Acknowledge the symptom; a fix is on the backlog without committing to a date. |
| 26 | Category page count of products is shown as `0` (placeholder) | Category listing (admin nav-tree; also reflected in storefront category meta) | Known bug | The category-list response returns `'products_count' => 0` with a TODO marker. (verify) merchant impact on storefront vs admin. |
| 27 | Checkout cash-on-delivery shipping methods may be hidden when COD is the only enabled payment | Checkout shipping step | Known bug | Four `@todo check payments providers if is only COD active check shipping's where support COD` markers exist in the checkout flow. The merchant should test with COD-only configurations and report mismatches. (verify) per affected courier. |
| 28 | Checkout step jumping by URL (skipping step 2 to step 3) | Multi-step checkout | By design (verify) | A `@todo set step` marker exists in the checkout controller. The customer's `current_step` is server-authoritative — direct URL access to a later step should snap back to the cart's actual step. (verify) edge cases with addressless guest carts. |
| 30 | Scalar-guarded search query — `?query[$eq]=foo` no longer triggers PHP "Array to string conversion" warning | Storefront search | Pending fix | A scalar-guard was introduced after 62 such warnings in 24h. Behaviour for the customer is unchanged (the term is treated as empty). This is documented for completeness — no merchant action needed. |

### Support-agent quick path per entry

- **Entry 23** (By design) → cite [[seo-handling]]; crawler 404 in Search Console is expected.
- **Entry 24** (Known bug, verify) → take reproduction (products + theme) and escalate; do not promise a date.
- **Entry 25** (Known bug) → tell the merchant the customer-account order page will lack per-line parameters + weight; the admin's [[orders-details]] has the full detail.
- **Entry 26** (Known bug) → if merchant sees `0` on storefront category cards, suggest hiding the count in the theme until the fix lands.
- **Entry 27** (Known bug, verify) → merchant tests with COD-only configurations and submits failing cases per courier.
- **Entry 28** (By design, verify) → server-authoritative step snap-back; escalate addressless-guest-cart edge cases.
- **Entry 30** (Pending fix) → no merchant-facing action needed.

## Related

- [[storefront-known-issues]] — hub.
- [[storefront-issue-framework]] — the four categories.
- [[storefront-issue-listing-search]] — entries 26 + 30 also live there.
- [[seo-handling]] — entry 23 rationale.
- [[orders-details]] — entry 25 workaround (admin side has full detail).
- [[checkout-flow]] — entries 27 + 28.

## Open Questions

- Are there cases where the cart cross-sell block silently fails because of a stale module definition? (verify the `@todo for CrossSell` marker against current behaviour — entry 24.)
- For the `products_count = 0` bug — does this affect the storefront's category-card display, or only the admin nav-tree? (verify by reading the consumer — entry 26.)
- For entry 27 — which couriers are affected? Speedy, DPD BG, Econt? (verify per courier.)
- For entry 28 — what is the precise behaviour when a guest cart has no address and the customer URL-hops to step 3? Does the snap-back work, or does the customer see an empty state? (verify.)
