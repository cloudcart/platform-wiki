---
type: concept
nav_path: "Concept → Storefront known issues → Display & customer"
aliases: ["Storefront display issues", "Currency picker absent", "VAT display rule", "Compare wishlist persistence", "Blog comment moderation", "Address autocomplete Google Maps"]
tags: [storefront, display, currency, vat, compare, wishlist, blog, session, issues]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[storefront-known-issues]]. See the hub for the other aspects (framework, inventory, discount codes, cart lifecycle, listing / search, pending bugs).

# Storefront issues — display & customer-area

## Definition

The display-and-customer-area entries cover behaviours around **how the storefront presents prices and currency, what the customer-account area offers, and what dependencies the storefront has on merchant-configured external services**. All seven entries below are **By design** — each is the documented behaviour of a deliberate platform choice (single-currency, store-wide VAT mode, optional Google Maps autocomplete, login-required wishlist, etc.).

Seven catalogue entries are in this group: no built-in currency picker, store-wide VAT-included display, anonymous compare via cookie, login-gated wishlist, blog comment moderation per article, Google Maps autocomplete dependency, and customer session length being platform-driven.

## Scope

Covered:

- Display rules (currency picker absence, VAT display).
- Customer-area persistence (compare, wishlist).
- Blog comment moderation default.
- Address-autocomplete dependency on the merchant's Google Maps API.
- Customer session length.

Not covered:

- Theme-specific currency or price formatting — theme behaviour.
- Customer profile edit screens — see the customer-account feature pages.
- The wholesale-pricing app (the standard workaround for B2B-vs-B2C separation) — see the wholesale-pricing app's feature page when one exists.

## Contrasts

- **Single-currency store vs currency picker** — entry 15 is By design. CloudCart stores are single-currency; there is no built-in currency switcher. For BGN → EUR dual display, the merchant installs [[apps-bgn2eur]]. Custom multi-currency requires custom theme development.
- **Store-wide VAT mode vs per-customer-group VAT** — entry 16 is By design. The *"Show prices with VAT included"* setting on [[settings-taxes]] is store-wide — not per-customer-group, not per-geography. B2B-vs-B2C separation requires two stores or the wholesale-pricing app.
- **Compare via cookie vs Compare requires login** — entry 17 is By design. The compare list reads a `compare-product` cookie — anonymous comparisons persist by browser. Clearing cookies clears the compare list.
- **Wishlist requires login vs anonymous wishlist** — entry 18 is By design (verify). Wishlist is attached to the logged-in customer via the wishlist module. (verify) whether an anonymous wishlist cookie exists and how long it persists.
- **Blog comment auto-publish vs moderation** — entry 19 is By design. Per-article comment-type setting: `automatic` posts immediately as `approved`, anything else posts as `pending` until a staff member moderates. Default is `pending`.
- **Google Maps autocomplete vs plain-text input** — entry 22 is By design. The autocomplete dropdown calls the **merchant's** Google Maps API. Without a configured key (set under [[settings-cart]] → *Google Maps integration*), the autocomplete silently falls back to plain text input. The merchant pays Google for the API quota.
- **Platform session length vs per-store session length** — entry 29 is By design. Session lifetime comes from the platform's session config (not exposed to the merchant). (verify) whether a remember-me option is offered on the login form.

## Where it applies

The seven catalogue entries:

| # | Behaviour | Affected page(s) | Category | What to tell the merchant |
|---|---|---|---|---|
| 15 | Storefront does NOT have a customer-facing currency picker | Product detail, cart, checkout, all storefront pages | By design | CloudCart stores are **single-currency** — there is no built-in currency switcher. For BGN → EUR dual display, the merchant installs [[apps-bgn2eur]]. Custom multi-currency requires custom theme development. See [[multi-currency]]. |
| 16 | Prices on the storefront include VAT (or exclude it) for all visitors | Product detail, category listing, cart, checkout | By design | Driven by the *"Show prices with VAT included"* setting in [[settings-taxes]]. The display rule is store-wide — not per-customer-group, not per-geography. B2B-vs-B2C separation requires the merchant to operate two stores or use the wholesale-pricing app. See [[tax-computation]]. |
| 17 | Compare list survives across visits (cookie-based, no login required) | Compare, product detail | By design | The compare list reads the `compare-product` cookie — anonymous comparisons persist by browser. Clearing cookies clears the compare list. (verify) max-products in compare. |
| 18 | Wishlist requires login to persist (anonymous wishlist may not survive across sessions) | Wishlist, product detail, customer account | By design (verify) | Wishlist is attached to the logged-in customer via the wishlist module. (verify) whether an anonymous wishlist cookie exists and how long it persists. |
| 19 | Blog comments appear immediately on some stores but require approval on others | Blog article | By design | Controlled per-article — `automatic` comment-type posts immediately as `approved`, anything else posts as `pending` until a staff member moderates. Default comment status is `pending`. The success message even tells the customer *"posted, pending moderation"* in the non-automatic case. |
| 22 | Address autocomplete requires a Google Maps API key configured by the merchant | Checkout shipping/billing address | By design | The autocomplete dropdown calls the merchant's Google Maps API. Without a configured key (set under [[settings-cart]] → *Google Maps integration*), the autocomplete silently falls back to plain text input. The merchant pays Google for the API quota. |
| 29 | Customer session length is driven by the platform's session-lifetime config, not a per-store setting | Customer login, account | By design | Session lifetime comes from the platform's session config (not exposed to the merchant). (verify) whether a remember-me option is offered on the login form. |

### Support-agent quick path

All seven are **By design**. The agent's response template:

- *"Why is there no currency picker on my storefront?"* → entry 15; recommend [[apps-bgn2eur]] for dual display, custom theme dev for full multi-currency.
- *"I want B2B customers to see prices without VAT"* → entry 16; recommend a separate store or the wholesale-pricing app.
- *"My customer's wishlist disappeared"* → entry 18; was the customer logged in when they added items?
- *"Comments aren't appearing on my blog"* → entry 19; check the per-article comment-type setting.
- *"Address autocomplete stopped working"* → entry 22; check the merchant's Google Maps API key + their Google billing.
- *"My customer keeps getting logged out"* → entry 29; platform-level session config, not a per-store setting.

## Related

- [[storefront-known-issues]] — hub.
- [[storefront-issue-framework]] — the four categories.
- [[multi-currency]] — entry 15.
- [[tax-computation]] — entry 16.
- [[settings-taxes]] — entry 16 UI.
- [[settings-cart]] — entry 22 (Google Maps integration).
- [[apps-bgn2eur]] — entry 15 workaround.

## Open Questions

- What is the maximum number of products supported in the Compare list? (verify per-theme — does the underlying handler cap, or is it UI-bound?)
- Does the anonymous wishlist persist across visits via cookie, or is it lost on session end? (verify the wishlist menu data source.)
- Is there a customer-facing "remember me" toggle on the login form, or is session length entirely driven by the platform-level session config? (verify per theme.)
