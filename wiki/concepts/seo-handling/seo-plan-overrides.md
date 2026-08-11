---
type: concept
nav_path: "Concept → SEO handling → Plan overrides"
aliases: ["Trial robots", "Plan expired SEO", "Development mode SEO", "Demo store noindex", "cc-demo noindex", "Plan-gated SEO", "SEO override"]
tags: [seo, plan-gates, trial, plan-expired, cc-demo, override, concepts]
plan_gates: ["trial", "plan_expired", "cc-demo"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[seo-handling]]. See the hub for related aspects (sitemap / robots, canonical / noindex, meta tags, redirects, sharing / RSS, route catalog).

# SEO — plan overrides (trial, expired, dev, demo)

## Definition

Three categories of store get SEO directives that **ignore the merchant's admin settings entirely** and force the storefront into an invisible-to-Google state. The admin UI does NOT warn the merchant about this. These overrides are the **single most common cause** of "why isn't my new store on Google?" support tickets.

- **Trial / `plan_expired` / development stores** → robots.txt is hard-coded to `User-agent: *` + `Disallow: /` regardless of what the merchant typed into [[marketing-seo-robots]].
- **`cc-demo` plan stores** → every page emits `<meta name="robots" content="noindex, nofollow">` regardless of any SEO setting.

## Scope

Covered:

- The three categories that get `Disallow: /` (trial, `plan_expired`, development mode).
- The `cc-demo` plan and its `noindex, nofollow` meta override.
- Functional equivalence + the difference at upgrade time (robots.txt flip is automatic; demo-store upgrade requires plan migration).
- No SEO surface has its own plan gate (the admin screens are accessible to trial / expired merchants — only the live storefront output is overridden).

Not covered here:

- The merchant-saved robots.txt body, the platform safety block, and the 5-minute cache → [[seo-sitemap-robots]].
- The general `noindex` rules on filtered pages → [[seo-canonical-noindex]].
- The [[plan-gates]] concept generally — this aspect documents only SEO-specific overrides.

## Contrasts

- **Trial-store `Disallow: /` vs. Demo-store `noindex, nofollow`** — both prevent Google indexing but in different ways. Trial / `plan_expired` stores get `Disallow: /` in robots.txt — Google doesn't even fetch the pages. `cc-demo` plan stores get `noindex, nofollow` meta — Google fetches the pages and then ignores them. Functionally equivalent; the difference matters when the merchant upgrades a trial store to paid (robots.txt flips back to merchant-saved on the next request, no admin action needed) vs. a demo store being upgraded (different plan migration).
- **Development mode vs. `plan_expired`** — same `Disallow: /` output, different cause. Development mode is set by CloudCart staff on demo / staging stores. `plan_expired` is set when the merchant's paid plan lapses and is not yet renewed.
- **Override vs. merchant intent** — the merchant can write any robots.txt body or any per-section meta they want, and the admin screen will save it. The live storefront simply ignores it under these three plan states. The admin UI provides NO warning banner about this.

## Where it applies

### Trial / expired / dev stores — hard-coded `Disallow: /` override

Three categories of store get a different robots.txt regardless of what the merchant saves:

- Stores on the **trial plan** (not yet upgraded to a paid plan).
- Stores with **`plan_expired`** (paid plan lapsed, not yet renewed).
- Stores running in **development mode**.

For these stores, the storefront serves:

```
User-agent: *
Disallow: /
```

This blocks Google (and every other crawler) from the entire site. The merchant's saved robots.txt is **ignored**. The admin UI doesn't warn the merchant about this.

When the plan flips to a paid active state, the live `/robots.txt` **immediately** starts serving the merchant's saved body (or the platform default template) — but during trial / expired periods, the store is NOT in Google's index. This is the single most common cause of "why isn't my new store on Google?" support tickets.

### Demo stores are always `noindex`

Stores on the `cc-demo` plan always render `<meta name="robots" content="noindex, nofollow">` on every page, regardless of any SEO setting. Demo stores are CloudCart's internal templates / sales-demos; they're never meant to appear in Google.

### Plan gates on SEO admin surfaces

**No SEO surface has a plan-gate of its own.** Trial / expired stores are allowed into the admin screens (so the merchant can configure SEO during trial), BUT the live storefront serves `Disallow: /` for those stores regardless of what the merchant typed. After upgrade, the saved settings take effect immediately on the next request — no admin action needed.

### Practical support pattern

When a merchant says "Google isn't indexing my store":

1. Check the plan state first. If trial / `plan_expired` / dev / `cc-demo`, that's the cause — instruct upgrade.
2. Only if the plan is a paid active state, proceed to debug merchant-side robots.txt, sitemap, canonical, or per-section meta. See [[seo-sitemap-robots]] + [[seo-canonical-noindex]] + [[seo-meta-tags]].

## Related

- [[seo-handling]] — hub.
- [[seo-sitemap-robots]] — the merchant-saved robots.txt pipeline these overrides bypass.
- [[seo-canonical-noindex]] — the general `noindex` rules `cc-demo` short-circuits.
- [[plan-gates]] — general plan-gating concept; trial / `plan_expired` / `cc-demo` definitions.
- [[marketing-seo-robots]] — admin editor for robots.txt (saved but overridden during trial / expired).
- [[marketing-seo]] — Main SEO settings hub (accessible during trial, but live output is overridden).

## Open Questions

None.
