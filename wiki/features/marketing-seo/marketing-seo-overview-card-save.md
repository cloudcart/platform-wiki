---
type: feature
nav_path: "Marketing → Seo → Per-card save model"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["SEO per-card save", "SEO Save Revert", "SEO independent card save", "SEO dirty detection", "Canonical instant save", "Robots confirm modal", "Запазване по карта SEO"]
tags: [marketing, seo, save, ux]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-seo]]. See the hub for the other page-level aspects (layout, settings map, save endpoints, trial block) and the seven per-card deep dives.

# Main SEO settings — per-card save model

## Purpose

This aspect documents **how saving works on the Main SEO screen** — specifically the fact that each of the seven cards saves independently, how the screen decides a card is "dirty", the special instant-save behaviour of the Canonical card, and the extra confirmation step on the Robots.txt card. This is the page-level behaviour that explains why merchants see a separate Save / Revert pair on each card rather than one global submit.

## Where to find it

Sidebar → Marketing → **SEO**. Route name `seo-main`, path `/admin/marketing-new/seo`. The save controls described here appear inline on each of the seven cards on that screen; full layout is on [[marketing-seo-overview-layout]].

## What the merchant can do here

- Edit one card (for example Canonical) and save it **without touching** any other card.
- See an inline **Save / Revert** action bar appear on a card the moment its value differs from what was loaded.
- Click **Revert** on a dirty card to discard the in-progress change and restore the loaded value.
- On the Robots.txt card, confirm an explicit "Are you sure?" modal before the save actually fires.

## Settings & fields

This aspect describes UX behaviour rather than stored settings; the per-card stored values are catalogued on [[marketing-seo-overview-settings-map]]. The relevant controls are the **Save** and **Revert** buttons that each card surfaces when dirty.

## Business rules

### Cards save independently — no global submit

Unlike the meta-titles page (one save button for the whole form — see [[marketing-seo-meta]]), here each card has its own **Save / Revert** pair. The shared wrapper detects "dirty" state by comparing the in-memory value to the on-mount snapshot; when dirty, it opens an inline action bar. The merchant can save Canonical without touching Robots — and a failed save in one card leaves the others untouched.

### Canonical is an instant-save exception

The Canonical card is the exception to the Save / Revert pattern: it is a single switch wired to save instantly on toggle, with **no Revert** button. The on/off value is sent the moment the merchant flips the switch. See [[marketing-seo-canonical]] for what the toggle renders on the storefront.

### Robots.txt has an extra confirm step

The Robots.txt card adds a step before the network call: clicking Save opens a confirm modal titled "Are you sure?" with the body "There is a possibility that you will break your site by changing the contents of this file." and a primary "OK" button. This modal exists because a bad robots.txt edit (for example typing `Disallow: /`) can de-index the entire store. See [[marketing-seo-robots]] for the robots.txt body rules.

### Why this matters for support

Because cards are independent, a merchant reporting "my SEO save didn't work" is almost always describing **one** card. Ask which card, then check that card's save endpoint (see [[marketing-seo-overview-save-endpoints]]) rather than assuming the whole page failed.

## Related

- [[marketing-seo]] — hub.
- [[marketing-seo-canonical]] — the instant-save Canonical card.
- [[marketing-seo-robots]] — the confirm-modal Robots.txt card.
- [[marketing-seo-meta]] — the contrasting single-submit meta-titles screen.

## Open questions

None.
