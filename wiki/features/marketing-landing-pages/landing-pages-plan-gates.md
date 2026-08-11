---
type: feature
nav_path: "Marketing → Landing Pages → Plan gates"
route_name: admin.pages.list
route_path: /admin/marketing/pages
aliases: ["Plan gates", "static_pages", "faq_page", "landing_page", "storefront_builder", "Page count cap", "Page count limit", "Лимит страници"]
tags: [marketing, content, pages, plan-gates, billing]
plan_gates: ["static_pages", "faq_page", "landing_page", "storefront_builder"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (list view, page types, editor, system slots, FAQ editor, builder rules).

# Landing Pages — Plan gates

## Purpose

Landing-page creation is gated by **four** plan-feature keys — one numeric cap on the total count, and three access gates per page type. This page documents the exact mapping per key, where the gate redirects when blocked, and how the "(N)" counter on **+ Add new page** is derived.

## Where to find it

The plan gates affect three surfaces:

- **+ Add new page** counter on [[landing-pages-list-view]] — shows `static_pages` remaining cap.
- **Choose page type** modal on [[landing-pages-types]] — each card's clickability is gated by its corresponding plan-feature key.
- The hidden module palette in the page builder — `storefront_builder` runs a per-module restriction callback.

When blocked by any gate, the merchant is redirected to the per-feature upsell page at [[plan-features]].

## What the merchant can do here

- See the remaining-pages allowance via the "(N)" counter on **+ Add new page**.
- See which page-type cards are dimmed / hidden because of the access gates on the **Choose page type** modal.
- Click through to [[plan-features]] when over a cap or below a tier — that page shows the upgrade or feature-pack offer.
- Extend the numeric `static_pages` cap via a feature pack (without a full plan upgrade) — see [[plan-vs-feature-pack]].
- Extend the access gates (`landing_page`, `faq_page`, `storefront_builder`) only via a plan upgrade — they're not feature-pack extendable. (verify)

## Settings & fields

### The four plan-feature mappings

| Mapping | Shape | What it controls |
|---|---|---|
| `static_pages` | Numeric | Total page count cap across all four types (regular / faq / landing / builder). The **+ Add new page (N)** counter shows remaining slots; hitting the cap blocks new pages until upgrade or delete. Extendable via feature pack. |
| `landing_page` | Access | Lower plans cannot pick the **External page** (`landing`) type at all — `/admin/marketing/pages/add/landing` route is gated. Restricts the type-picker card. |
| `faq_page` | Access | Lower plans cannot pick the **FAQ page** type at all — `/admin/marketing/pages/add/faq` route is gated. Restricts the type-picker card. |
| `storefront_builder` | Access + callback | Gates the **Dynamic page** (builder) type at `/admin/marketing/pages/builder/*`. Also runs the platform code callback that restricts specific modules per plan tier — see [[landing-pages-builder-rules]]. |

### The "(N)" counter mechanism

The header's "(N)" remaining-pages counter is fetched async via `data-box-ajax="{route('admin.common.remaining', 'page')}"`. The endpoint reads:

```
remaining = plan_feature_cap[static_pages] - count(pages)
```

Where the `count(pages)` includes ALL four types (regular + faq + landing + builder), and the cap comes from the plan's `static_pages` value plus any active feature packs. The counter may briefly show "(...)" until the AJAX resolves on first render — see [[landing-pages-list-view]].

## Business rules

### When over the `static_pages` cap

The merchant is redirected to the per-feature upsell at [[plan-features]]. The numeric `static_pages` cap extends via packs — see [[plan-vs-feature-pack]]. Alternatives that don't require an upgrade: delete unused pages from [[landing-pages-list-view]] until the counter goes positive.

### When below the access tier for a specific page type

The merchant is redirected to the per-feature upsell at [[plan-features]]. The per-type access gates (`landing_page`, `faq_page`, `storefront_builder`) require a plan upgrade — feature packs do NOT lift them. (verify)

### Plan-feature gating runs BOTH client-side (card hidden) AND server-side (route blocked)

The merchant typically sees the gated type card visually disabled on the **Choose page type** modal — that's the client-side hint. The authoritative check is server-side: if a merchant hand-edits the URL to `/admin/marketing/pages/add/faq` on a plan that doesn't include `faq_page`, the route still redirects to the upsell. The same is true for `landing` and the builder.

### Builder `storefront_builder` has a SECOND layer beyond access

Even when the merchant's plan includes `storefront_builder`, **specific modules** in the builder palette can be restricted per plan tier via the platform code. The merchant on a mid-tier `storefront_builder`-enabled plan can use the builder, but premium modules (e.g. some product-slider variants) may be hidden. See [[landing-pages-builder-rules]].

### Bulk Delete frees `static_pages` slots immediately

Deleting pages from [[landing-pages-list-view]] (single or bulk) immediately re-counts and the "(N)" counter updates on the next AJAX poll. No nightly recount or cache-flush delay.

### Bulk Duplicate consumes `static_pages` slots

Each copy made via the bulk Copy action is a new page counted against `static_pages`. If the merchant is close to the cap, bulk-duplicating multiple pages may hit the cap mid-batch — the remaining copies are blocked. (verify — does the controller pre-check the cap on bulk Copy?)

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-list-view]] — the "(N)" counter on **+ Add new page**.
- [[landing-pages-types]] — the four type cards gated by these features.
- [[landing-pages-builder-rules]] — the per-module restriction layer for `storefront_builder`.
- [[plan-features]] — the per-feature upsell page the merchant is redirected to.
- [[plan-gates]] — the platform-wide plan-gate catalogue.
- [[plan-vs-feature-pack]] — feature packs that extend `static_pages` without a full plan upgrade.

## Open questions

- 📡 **Exact plan caps per tier.** `static_pages`, `faq_page`, `landing_page`, and `storefront_builder` caps are set per plan via the platform's plan-gate config; merchants should check their plan's actual values via Account → Plan. GraphQL-resolvable: query the merchant's current plan + feature-pack stacks to read the actual caps.
- 📡 **Whether bulk Copy pre-checks the cap.** When the merchant bulk-copies N pages but only M slots remain, does the controller copy M pages and block the rest, or refuse the entire bulk operation? (verify)
- 📡 **Whether `landing_page` / `faq_page` / `storefront_builder` can be extended via feature packs.** Currently assumed plan-upgrade-only — verify against the feature-pack config. (verify)
