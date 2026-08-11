---
type: feature
nav_path: "Marketing → SEO → Robots.txt → Trial-store block"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Robots.txt trial block", "Disallow all override", "Trial store not indexed", "plan_expired robots", "Development robots.txt", "Why isn't my store on Google", "Робот файл триал блокиране"]
tags: [marketing, seo, robots, plan-gates, trial]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-seo-robots]]. See the hub for the other aspects (the editor card, the served file).

# Robots.txt — the trial / expired / dev block

## Purpose

The storefront has a separate code path for **non-production** sites. For stores in development mode, stores with `plan_expired`, and stores on the `trial` plan, the merchant's saved `robots.txt` is **completely ignored** and a hard-coded blanket-block is served instead:

```
User-agent: *
Disallow: /
```

This is the single most common cause of "why isn't my new store on Google?" support tickets: the merchant has carefully written a correct robots.txt on [[seo-robots-editor]], sees it in the textarea, but the live `/robots.txt` returns `Disallow: /` because the store is still on trial. This page documents the override, its three trigger conditions, and how to confirm it.

## Where to find it

This is a storefront-side override, not an admin control. There is no toggle for it on any screen. The merchant observes it by visiting `https://<their-domain>/robots.txt` (which returns `Disallow: /`) while the [[seo-robots-editor]] textarea still shows their own typed body. The relevant inputs are the store's plan / billing state — not anything editable on the SEO page.

## What the merchant can do here

- Diagnose the block by comparing the live `/robots.txt` (returns `Disallow: /`) against the [[seo-robots-editor]] textarea (still shows their typed body).
- Lift the block by upgrading to a paid plan (or moving the store to production) — the live `/robots.txt` immediately starts serving the saved body or the platform default.

### What the merchant CANNOT do here

- Override the block from the SEO page. No robots.txt body, however correct, makes a trial / expired / dev store crawlable.
- See a warning banner. There is currently no merchant-visible notice that the override is active.

## Settings & fields

This aspect has no settings of its own. The only inputs are the store's plan state (`trial`), billing state (`plan_expired`), and environment (development) — none of which are edited from the robots.txt card. The merchant's saved body (on [[seo-robots-editor]]) is bypassed entirely while any of the three conditions holds.

## Business rules

### The override fires on THREE conditions

The blanket-block template is served when the store is in **development** OR has **`plan_expired`** OR is on the **`trial`** plan. Decoded:

- **trial** — a pre-purchase store still on the trial plan.
- **plan_expired** — a lapsed paid plan that has expired.
- **development** — stores running in a non-production environment.

Any one of the three is enough to trigger `Disallow: /`.

### The saved body is ignored, not deleted

The textarea on [[seo-robots-editor]] still accepts edits and the database still stores them. Only the live-served file is overridden. When the merchant upgrades to a paid plan and `plan_expired` flips off (or the store moves to production), the live `/robots.txt` **immediately** starts serving the merchant's saved body — or the platform default template if they never edited it. See [[seo-robots-served-file]] for that normal pipeline.

### The blanket block still gets the appended safety lines

The `Disallow: /` template is concatenated with the same checkout / cart / wishlist Disallow block + `Crawl-Delay: 3` that the normal pipeline appends (see [[seo-robots-served-file]]). Since `Disallow: /` already blocks everything, the extra lines are redundant but harmless.

### No warning banner — first thing to check on an indexing ticket

There is no admin-side notice that the override is active. For a "my new store isn't on Google" ticket, the first thing to check is the store's **plan state**, not the robots.txt text. If the store is on trial / expired / development, the block is by-design and the fix is to upgrade or go to production. Only after that should the merchant's robots.txt content (on [[seo-robots-editor]]) be reviewed.

### Relationship to other SEO trial overrides

This robots.txt block is one facet of a broader trial / expired crawl block that also forces a noindex posture on page meta — that page-wide override is documented on [[marketing-seo-overview-trial-block]], and the cross-cutting concept view is [[seo-plan-overrides]]. This page covers only the robots.txt-specific behaviour.

## Related

- [[marketing-seo-robots]] — hub.
- [[seo-robots-editor]] — the saved body that is bypassed while the override is active.
- [[seo-robots-served-file]] — the normal assembly pipeline used once the store is on a paid plan in production.
- [[marketing-seo-overview-trial-block]] — the page-wide trial / expired crawl block (covers meta noindex too).
- [[seo-plan-overrides]] — the cross-cutting concept view of plan-state SEO overrides.

## Open questions

- 📡 **Override invisible in admin.** Trial / expired stores see their saved body in the textarea, not the live-served `Disallow: /`. No warning banner is currently rendered. GraphQL-resolvable: query the merchant's plan / billing state to determine whether the store is on trial or `plan_expired`.
