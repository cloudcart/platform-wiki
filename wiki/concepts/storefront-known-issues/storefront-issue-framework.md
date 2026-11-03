---
type: concept
nav_path: "Concept → Storefront known issues → Framework"
aliases: ["Storefront issue framework", "By design vs bug framework", "Storefront issue categories", "How to use the storefront-issues catalogue"]
tags: [storefront, bugs, issues, support, framework]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[storefront-known-issues]]. See the hub for the other aspects (inventory, discount codes, cart lifecycle, listing / search, display + customer, pending bugs).

# Storefront issue framework

## Definition

The framework page captures the **categorisation rules + the support-agent workflow** that the storefront-issues catalogue depends on. Every entry in the aspect pages ([[storefront-issue-inventory-display]], [[storefront-issue-cart-discount-codes]], [[storefront-issue-cart-lifecycle]], [[storefront-issue-listing-search]], [[storefront-issue-display-and-customer]], [[storefront-issue-pending-bugs]]) is tagged with one of four categories — and the support agent's response on a live ticket changes depending on which.

The four categories:

- **By design** — the platform deliberately behaves this way. There is no plan to change it. The agent's job is to surface the rule + educate the merchant.
- **Known bug** — engineering has acknowledged the symptom is wrong. It is on the backlog without a committed ship date. The agent acknowledges the symptom + tells the merchant a fix is on the backlog without committing to a date.
- **UX trade-off** — the behaviour is intentional but is a compromise against performance, SEO, privacy, or another constraint. The merchant may dislike it. The agent explains the rationale + the workaround.
- **Pending fix** — a fix is actively in progress. The entry expires from the catalogue once the fix ships. The agent mentions the fix is in progress + that the release-notes will communicate the ETA.

## Scope

**In scope** for the catalogue:

- Storefront-only behaviour — the customer-facing site, the customer-facing checkout flow, the customer account, blog comments, search, wishlist, compare.
- Behaviours that have been raised in support tickets at least once.
- Issues affecting more than one merchant (cross-cutting, not store-specific).

**Out of scope** — handled elsewhere:

- Admin-panel bugs → the affected admin feature page.
- Theme-specific cosmetic issues limited to a single theme → the theme's own page when one exists.
- Per-store quirks (one merchant's misconfiguration, one store's data anomaly) → the store's internal account notes, not the global wiki.
- Payment-provider-specific transaction failures → the provider's `payment-providers-*` feature page.
- Courier-specific shipping label or office-list bugs → the courier's `apps-*` feature page.

## Contrasts

- **By design vs Known bug** — the diagnostic question is *"is the symptom an intentional consequence of a documented rule?"* — if yes, **By design** and the agent surfaces the rule; if no, **Known bug**. Example: stock returns automatically after a cancellation. This *looks* wrong to a merchant who thinks of stock as a one-way ledger, but is the deliberate cancellation/restore semantic from [[inventory-tracking]] (see [[storefront-issue-inventory-display]] entry 1) — **By design**.
- **Known bug vs Pending fix** — both acknowledge the symptom is wrong. The difference is timeline: a Known bug has **no committed ship date** (do not promise a date to the merchant); a Pending fix is actively in progress with a release window committed. Once shipped, the Pending fix entry expires from the catalogue.
- **UX trade-off vs Known bug** — a UX trade-off is intentional. *"The category page resets scroll position on back-button"* (see [[storefront-issue-listing-search]]) is a trade-off — the storefront re-renders the listing because filter state + pagination + cache-headers preclude a perfect scroll-restoration. The merchant may dislike it; the documentation explains the rationale + the workaround (use pagination instead of infinite scroll). A **Known bug**, by contrast, has no defensible rationale — it is just broken.
- **Storefront issue vs admin-panel issue** — the storefront catalogue covers what the **customer** sees on the storefront. *"The admin order-edit screen shows a wrong tax line"* is an admin bug, not a storefront issue, even if the same data was correctly captured by the storefront. Route admin-panel symptoms to the affected admin feature page.

## Where it applies

The framework is the **decision layer** for every entry in the six aspect pages. The aspect pages catalogue specific symptoms; the framework decides how the support agent should respond.

### How to use the catalogue on a live ticket

When a merchant reports a storefront behaviour:

1. **Search the catalogue first** with the symptom keywords across all six aspect pages — start from the [[storefront-known-issues]] hub.
2. If categorised as **By design**, explain the rule + cite the originating concept page so the merchant has the model.
3. If categorised as **Known bug**, acknowledge the symptom + tell the merchant a fix is on the backlog **without committing to a date**.
4. If **UX trade-off**, explain the rationale + the workaround (e.g., *"use pagination instead of infinite scroll"*).
5. If **Pending fix**, mention that the fix is in progress + that the ETA will be communicated via release notes.
6. If the symptom is **not** found in the catalogue, escalate per the normal support flow and add the verified outcome to the next docs sync.

### How to add a new entry

- Do **not** edit the catalogue directly during a live ticket — the catalogue is a sync artefact.
- File the symptom in the support tracking system with the route, theme, reproduction steps, and the screenshot the merchant sent.
- After verification (either confirmed bug or confirmed by-design), append the row to the relevant aspect page at the next docs-sync window. New entries should always cite the originating concept page or feature page so the support agent can link the merchant to the rule.
- When a fix ships for a **Pending fix** entry, remove the row + leave a single-line note in `wiki/log.md` so the catalogue's revision history is preserved.

### Routing a new symptom to the right aspect page

| Symptom is about… | Aspect page |
|---|---|
| Stock display, oversell, out-of-stock label, bundle availability | [[storefront-issue-inventory-display]] |
| Discount codes interacting in the cart (container vs promo, stacking, shipping) | [[storefront-issue-cart-discount-codes]] |
| Cart merge, cookie lifetime, abandoned-cart restore, thank-you page refresh | [[storefront-issue-cart-lifecycle]] |
| Category listing, search results, filter sidebar, infinite scroll, category counts | [[storefront-issue-listing-search]] |
| Currency picker, VAT display, autocomplete, compare, wishlist, blog comments, session | [[storefront-issue-display-and-customer]] |
| The symptom is a known defect with no current rationale (Known bug / Pending fix) | [[storefront-issue-pending-bugs]] |

## Related

- [[storefront-known-issues]] — hub.
- [[inventory-tracking]] — the most-cited By-design rule source.
- [[discount-stacking]]
- [[checkout-flow]]
- [[abandoned-cart-recovery]]

## Open Questions

None.
