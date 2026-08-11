---
type: concept
nav_path: "Concept → Storefront known issues"
aliases: ["Storefront known issues", "Storefront bugs", "By design vs bug", "Storefront quirks", "Known storefront issues", "Известни проблеми storefront"]
tags: [storefront, bugs, issues, support, debugging]
created: 2026-06-08
updated: 2026-06-10
source_count: 5
---

# Storefront known issues

## Definition

This concept is a **single catalogue** of storefront behaviours that frequently generate support tickets, with each entry tagged as **By design**, **Known bug**, **UX trade-off**, or **Pending fix**. It is the support agent's **first stop** when a merchant reports *"the storefront does X — is this a bug?"*. Knowing which is which saves an escalation cycle and protects the merchant from being told *"we'll file a ticket"* for something the platform deliberately does.

The catalogue is forward-looking — entries are appended at the next docs-sync after a ticket has been investigated and verified. The catalogue itself is the deliverable; this hub wraps a thin framework around it and points to the aspect pages where individual entries live.

The four categories are not synonyms. **By design** = the platform deliberately behaves this way; there is no plan to change it; the merchant should be educated on the rule. **Known bug** = engineering has acknowledged the symptom is wrong; it is on the backlog without a committed ship date. **UX trade-off** = the behaviour is intentional but is a compromise against performance, SEO, privacy, or another constraint; the merchant may dislike it; document the rationale + the workaround. **Pending fix** = a fix is actively in progress; the entry expires from the catalogue when the fix ships.

See [[storefront-issue-framework]] for the full categorisation rules + the support-agent instruction loop.

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each scoped to a coherent group of symptoms. The Assistant should drill into the aspect that matches the merchant's complaint, not read every page.

- [[storefront-issue-framework]] — the four categories (By design vs Known bug vs UX trade-off vs Pending fix), scope rules, how to use the catalogue on a live ticket, how to add new entries.
- [[storefront-issue-inventory-display]] — stock-display behaviours: automatic restock on cancel, race-condition oversells, clamp-at-0, "Out of stock" still showing Add-to-cart, variant-picker out-of-stock label, bundle stock derivation.
- [[storefront-issue-cart-discount-codes]] — discount-code interactions in the cart: container-code vs promo-code mutual exclusion, single-code default rule, shipping / `order_over` carve-outs.
- [[storefront-issue-cart-lifecycle]] — cart-state behaviours: anonymous-vs-logged-in merge, 24-hour guest cookie lifetime, abandoned-cart restore that merges instead of replaces, thank-you-page refresh safety.
- [[storefront-issue-listing-search]] — category / search behaviours: empty-query handling, scalar-guarded search, filter-sidebar back-button state, infinite-scroll scroll-position, `products_count = 0` placeholder.
- [[storefront-issue-display-and-customer]] — display + customer-area behaviours: single-currency design, VAT-included display, Google Maps autocomplete dependency, compare / wishlist persistence, blog-comment moderation gate, session length.
- [[storefront-issue-pending-bugs]] — the actual Known bug + Pending fix entries: crawler 404 on order return (by design), cart cross-sell empty (bug), customer-account order missing per-line parameters + weight (bug), COD-only shipping mismatch (bug), checkout step-jumping (verify), scalar-guard search fix (pending fix).

## Scope

**In scope** — storefront-only behaviour (the public site + the customer-facing checkout flow):

- Behaviours that have been raised in support tickets at least once.
- Issues affecting more than one merchant (cross-cutting, not store-specific).
- Customer-facing flows: product detail, category listing, cart, checkout, customer account, blog, search, wishlist, compare.

**Out of scope** — handled elsewhere:

- Admin-panel bugs — those belong under the affected admin feature page.
- Theme-specific cosmetic issues limited to a single theme — those belong on the theme's own page when one exists.
- Per-store quirks (one merchant's misconfiguration, one store's data anomaly) — those belong on the store's internal account notes, not on the global wiki.
- Payment-provider-specific transaction failures — those belong on the provider's `payment-providers-*` feature page.
- Courier-specific shipping label or office-list bugs — those belong on the courier's `apps-*` feature page.

See [[storefront-issue-framework]] for the full scope rationale + the routing decision tree.

## Contrasts

- **By design vs Known bug** — the platform has many behaviours that *look* wrong to a merchant unfamiliar with the model. The single most-asked example: *"stock returned automatically after I cancelled an order — is the system broken?"* — no, that is the deliberate cancellation/restore semantic from [[inventory-tracking]] (see [[storefront-issue-inventory-display]] entry 1). The diagnostic question is always: *"is the symptom an intentional consequence of a documented rule?"* — if yes, it is **By design** and the agent's job is to surface the rule. If no, it is a candidate **Known bug**.
- **Known bug vs Pending fix** — a defect with no committed ship date is a **Known bug** (cite the symptom, do not promise a date). The same defect once development has started + a release window is committed becomes a **Pending fix**. Once shipped, the entry expires.
- **UX trade-off vs Known bug** — a UX trade-off is intentional. *"The category page resets scroll position on back-button"* is a trade-off (see [[storefront-issue-listing-search]]). The merchant may dislike it; the documentation explains the rationale + the workaround. A **Known bug**, by contrast, has no defensible rationale — it is just broken.
- **Storefront issue vs admin-panel issue** — this concept covers what the **customer** sees on the storefront. *"The admin order-edit screen shows a wrong tax line"* is an admin bug, not a storefront issue, even if the same data was correctly captured by the storefront. Route admin-panel symptoms to the affected admin feature page.

## Where it applies

Every storefront-page file under `wiki/storefront/` should cite this concept under its own *"Known issues / by-design vs bug"* section. The per-page section is the **LOCAL** list of issues for that one page; this concept page is the **GLOBAL** index that aggregates them and makes them searchable across the whole storefront.

Cross-cutting concepts that drive the entries in the aspect pages:

- [[inventory-tracking]] — stock-decrement timing, oversell behaviour, out-of-stock display rules → [[storefront-issue-inventory-display]].
- [[discount-stacking]] — code-vs-code conflicts, container-vs-promo mutual exclusion → [[storefront-issue-cart-discount-codes]].
- [[checkout-flow]] — cart cookie lifetime, abandoned-cart restore, guest-vs-registered, merge-on-login → [[storefront-issue-cart-lifecycle]].
- [[multi-currency]] — single-currency design + no built-in currency picker → [[storefront-issue-display-and-customer]].
- [[tax-computation]] — VAT-inclusive vs VAT-exclusive display → [[storefront-issue-display-and-customer]].
- [[abandoned-cart-recovery]] — recovery link behaviour + cart merge → [[storefront-issue-cart-lifecycle]].

## Related

- [[inventory-tracking]]
- [[discount-stacking]]
- [[checkout-flow]]
- [[multi-currency]]
- [[tax-computation]]
- [[order-status-workflow]]
- [[abandoned-cart-recovery]]
- [[shipping-calculation]]
- [[seo-handling]]
- [[settings-cart]]
- [[settings-taxes]]
- [[products-missing-product]]

## Open Questions

None at the hub level — see each aspect page for its own open questions.
