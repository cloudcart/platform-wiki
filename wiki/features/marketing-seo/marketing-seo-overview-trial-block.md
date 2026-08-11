---
type: feature
nav_path: "Marketing → Seo → Trial-store crawl block"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Trial store not on Google", "New store not indexed", "Disallow all on trial", "Trial robots override", "Demo store noindex", "Expired store crawl block", "Защо магазинът ми не е в Google"]
tags: [marketing, seo, robots, trial, indexing, plan-gate]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-seo]]. See the hub for the other page-level aspects (layout, card-save model, settings map, save endpoints) and the seven per-card deep dives.

# Main SEO settings — trial / expired / demo crawl block

## Purpose

This aspect explains the single biggest "why isn't my new store on Google?" support pattern: a store that is on **trial**, **expired**, in **development mode**, or on the **demo plan** is crawl-blocked at the storefront regardless of what the merchant types into the Robots.txt card or how the Canonical switch is set. The block is enforced by the storefront, is not surfaced anywhere in the admin UI, and the merchant cannot override it from the Main SEO screen.

## Where to find it

The override is enforced by the storefront when it serves `/robots.txt` and when it renders page meta — it is not a control on any admin screen. The robots.txt body the merchant edits lives on [[marketing-seo-robots]] (a card on [[marketing-seo]]), but that text is bypassed for the plan states below.

## What the merchant can do here

There is no merchant-facing control to disable this block — it is plan-state driven. The only "action" available to the merchant is to **upgrade off** the trial / expired / development / demo state, after which the block lifts automatically (no manual re-enable needed).

## Settings & fields

This aspect has no settings of its own. The relevant inputs are the merchant's saved robots.txt body (on [[marketing-seo-robots]]) and the Canonical switch (on [[marketing-seo-canonical]]) — both of which are overridden for the plan states below.

## Business rules

### Trial / expired / development → blanket `Disallow: /`

When the store is on **trial**, past `plan_expired`, or running in **development mode**, the storefront serves a trial robots template instead of the merchant's saved text. That template is a blanket:

```
User-agent: *
Disallow: /
```

Everything is blocked. New trial sites are therefore **not indexable** until the merchant upgrades. The merchant's own robots.txt body is ignored entirely for these three states, and there is no merchant-visible warning. The override is applied at robots.txt render time on the storefront, not at save time — so the Robots.txt card on [[marketing-seo-robots]] will happily show whatever the merchant typed, while the live `/robots.txt` returns `Disallow: /`.

### Demo plan → noindex meta instead

Stores on the demo (`cc-demo`) plan get a different override: at meta-tag render time the storefront hard-injects `<meta name="robots" content="noindex, nofollow">` into the page head, regardless of the Canonical setting. Demo stores still serve the merchant's robots.txt text and still emit canonical tags — but Google ignores them because of the noindex meta. See [[marketing-seo-canonical]] for normal canonical behaviour.

### The sitemap is still reachable, but pointless under the block

The storefront's `/sitemap.xml` runs without plan-gate or trial blocking, so a direct visit always returns the sitemap. But because `/robots.txt` returns `Disallow: /` for trial / expired sites, crawlers will not fetch the sitemap anyway. See [[marketing-seo-sitemap]].

### Upgrade lifts the block automatically

Once the store moves off trial / expired / development / demo, the storefront stops serving the trial template (or stops injecting the noindex meta) and returns the merchant's configured robots.txt and canonical tags. No manual merchant intervention is required — the flip is automatic on the plan-state change.

### Support framing

For a "my new store isn't on Google" ticket, the first thing to check is the store's plan state, not the robots.txt text. If the store is on trial / expired / development / demo, the block is by-design and the fix is to upgrade. Only after that should the merchant's robots.txt content (see [[marketing-seo-robots]]) be reviewed.

## Related

- [[marketing-seo]] — hub.
- [[marketing-seo-robots]] — the robots.txt body that is overridden for these plan states.
- [[marketing-seo-canonical]] — canonical tags still emit on demo stores but are ignored due to noindex meta.
- [[marketing-seo-sitemap]] — reachable but not crawled while the block is active.

## Open questions

- 📡 **Plan-state visibility.** The trial/expired/demo crawl block is not surfaced anywhere in the admin UI; merchants discover it only via a support ticket. A future merchant-facing warning banner on the Main SEO screen would cut these tickets. The current plan state is resolvable from the merchant account record.
