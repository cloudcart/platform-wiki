---
type: feature
nav_path: "Design → Static pages → Plan gates"
route_name: admin.pages.list
route_path: /admin/design/pages
aliases: ["Plan gates", "static_pages", "faq_page", "landing_page", "storefront_builder", "Page count cap", "Page count limit", "Лимит страници"]
tags: [marketing, content, pages, plan-gates, billing]
plan_gates: ["static_pages", "faq_page", "landing_page", "storefront_builder"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (list view, page types, editor, system slots, FAQ editor, builder rules).

# Landing Pages — Plan gates

## Purpose

Landing-page creation is gated by **four** plan-feature keys — one numeric cap on the total count, and three access gates per page type. This page documents the exact mapping per key, where the gate redirects when blocked, and how the remaining-pages count is derived.

## Where to find it

The pages list is at `/admin/design/pages` ([[landing-pages-list-view]]); it shows no remaining-pages counter (the retired list showed one as **+ Add new page (N)**). The plan gates act on two surfaces:

- **Choose page type** modal on [[landing-pages-types]] — shows every card on every plan; the plan features gate the screens the cards open.
- The page builder itself — `storefront_builder` gates every builder action (opening, auto-save, block settings); separately, the **Video slider** and **Lookbook** blocks show a padlock in the palette and their settings are refused without their own plan feature.

When blocked by any gate, the merchant is redirected to the per-feature upsell page at [[plan-features]].

## What the merchant can do here

- Meet the access gates when a page-type card opens a screen the plan doesn't include (the modal itself hides or dims no card).
- Click through to [[plan-features]] when over a cap or below a tier — that page shows the upgrade or feature-pack offer.
- Extend the numeric `static_pages` cap via a feature pack (without a full plan upgrade) — see [[plan-vs-feature-pack]].
- Extend the access gates (`landing_page`, `faq_page`, `storefront_builder`) only via a plan upgrade — they're not feature-pack extendable. (verify)

## Settings & fields

### The four plan-feature mappings

| Mapping | Shape | What it controls |
|---|---|---|
| `static_pages` | Numeric | Total page count cap across all four types (regular / faq / landing / builder). Hitting the cap blocks new pages until upgrade or delete. Extendable via feature pack. |
| `landing_page` | Access | Lower plans cannot pick the **External page** (`landing`) type at all — `/admin/design/pages/add/landing` is gated; the type-picker card still shows. |
| `faq_page` | Access | Lower plans cannot pick the **FAQ page** type at all — `/admin/design/pages/add/faq` is gated; the type-picker card still shows. |
| `storefront_builder` | Access + callback | Gates the **Dynamic page** (builder) type at `/admin/marketing/pages/builder/*`. The access check is a callback for the whole builder; it does not restrict individual modules — only **Video slider** and **Lookbook** carry gates of their own, see [[landing-pages-builder-rules]]. |

### The remaining-pages count

The retired list fetched its "(N)" counter from the admin's remaining-items endpoint; the current list does not call it. The count is:

```
remaining = plan_feature_cap[static_pages] - count(pages)
```

Where the `count(pages)` includes ALL four types (regular + faq + landing + builder), and the cap comes from the plan's `static_pages` value plus any active feature packs. The current list shows no counter — see [[landing-pages-list-view]].

## Business rules

### When over the `static_pages` cap

The merchant is redirected to the per-feature upsell at [[plan-features]]. The numeric `static_pages` cap extends via packs — see [[plan-vs-feature-pack]]. Alternatives that don't require an upgrade: delete unused pages from [[landing-pages-list-view]] to free slots.

### When below the access tier for a specific page type

The merchant is redirected to the per-feature upsell at [[plan-features]]. The per-type access gates (`landing_page`, `faq_page`, `storefront_builder`) require a plan upgrade — feature packs do NOT lift them. (verify)

### Plan-feature gating sits on the destination, not the card

The **Choose page type** modal shows every card on every plan. The check is tied to the destination address: opening `/admin/design/pages/add/faq` on a plan without `faq_page` is restricted server-side, and the same holds for `landing` and the builder. How the gate applies when the admin app switches to the form without a full page load is not confirmed (verify).

### Two builder modules have gates of their own

Even when the merchant's plan includes `storefront_builder`, two modules are gated separately: **Video slider** and **Lookbook** show a padlock in the builder palette (linking to their app) until the app is installed and enabled — Video slider also needs its plan feature — and the builder refuses to open or save their settings on a plan without the feature. No other module is restricted by plan. See [[landing-pages-builder-rules]].

### Bulk Delete frees `static_pages` slots immediately

Deleting pages from [[landing-pages-list-view]] (single or bulk) frees the slots at once; the count is taken live. No nightly recount or cache-flush delay.

### Bulk Duplicate consumes `static_pages` slots

Each copy made via the bulk Copy action is a new page counted against `static_pages`. If the merchant is close to the cap, bulk-duplicating multiple pages may hit the cap mid-batch — the remaining copies are blocked. (verify — does the controller pre-check the cap on bulk Copy?)

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-list-view]] — the pages list (no counter).
- [[landing-pages-types]] — the type cards whose destinations these features gate.
- [[landing-pages-builder-rules]] — the builder's own rules, including the two separately gated modules.
- [[plan-features]] — the per-feature upsell page the merchant is redirected to.
- [[plan-gates]] — the platform-wide plan-gate catalogue.
- [[plan-vs-feature-pack]] — feature packs that extend `static_pages` without a full plan upgrade.

## Open questions

- 📡 **Exact plan caps per tier.** `static_pages`, `faq_page`, `landing_page`, and `storefront_builder` caps are set per plan via the platform's plan-gate config; merchants should check their plan's actual values via Account → Plan. GraphQL-resolvable: query the merchant's current plan + feature-pack stacks to read the actual caps.
- 📡 **Whether bulk Copy pre-checks the cap.** When the merchant bulk-copies N pages but only M slots remain, does the controller copy M pages and block the rest, or refuse the entire bulk operation? (verify)
- 📡 **Whether `landing_page` / `faq_page` / `storefront_builder` can be extended via feature packs.** Currently assumed plan-upgrade-only — verify against the feature-pack config. (verify)
