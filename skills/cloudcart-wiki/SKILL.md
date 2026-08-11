---
name: cloudcart-wiki
description: Answer any question about how CloudCart works — a documented behaviour, a navigation path, a business rule, a plan gate, or why the platform behaves the way it does — by navigating the wiki in this repository. Use whenever the answer should come from what CloudCart actually does rather than from how e-commerce platforms usually work.
---

# CloudCart wiki

This repository holds a structured knowledge base of the CloudCart platform: every admin-panel screen, the data model behind it, the cross-cutting concepts, the JSON API v2 resources, and the customer-facing storefront pages. This skill is the protocol for answering from it.

The wiki is the **source of truth for the platform's mechanics, rules and navigation**. Ground every concrete claim in a page you actually read. Never fill a gap from memory or from how other platforms work.

## How to navigate

**Do not grep the whole wiki, and do not read pages at random.** There are ~2500 pages; the entry point is a map.

1. **Read `wiki/index.md` first.** It is a compact two-tier map, one line per entry, grouped into five sections:
   - **Concepts** — "how does X work"
   - **Admin areas** — "where do I set X"
   - **Entities** — the data model
   - **API** — JSON API v2 resources
   - **Storefront** — the public pages a shopper sees

2. **Pick the one section that fits, then the single best hub page.** Feature pages are **not** listed individually in the map. To reach a feature, open its admin-area hub — `[[settings]]`, `[[orders]]`, `[[products]]`, `[[apps]]`, `[[marketing]]`, `[[customers]]`, `[[design]]` — and follow its links.

3. **Drill into the target page and read it fully.** Pay attention to the frontmatter `nav_path` (the click path through the admin) and `route_path` (used to build a clickable URL by prefixing the store's domain), plus the `## Settings & fields` and `## Business rules` sections.

4. **Follow the dependency chain.** After the literal-answer page, traverse its `## Related` section and the inline `[[wikilinks]]` in its body until you have covered every component the answer touches — prerequisites, the entities it manipulates, the concepts it rests on, the screens that consume it, sibling aspects in the same cluster. Not a fixed number of pages: keep going while an unread surface is still relevant.

5. **Cover every dimension the question touches**, not only the one you entered from:
   - how it is **configured** — the admin feature page under `wiki/features/`
   - how it **works underneath** — the concept page under `wiki/concepts/`
   - how it is **modelled** — the entity page under `wiki/entities/`
   - how it **appears where the question happens** — for anything a shopper sees, the customer-facing page under `wiki/storefront/` is part of the answer, not optional

   `wiki/storefront/` is the public shop (home, category, product, cart, checkout, account, blog). That is distinct from the admin **Design / My Store** screens under `wiki/features/`, where the merchant *configures* themes and modules.

Before composing, ask which relevant surface you have **not** opened yet. Stopping at the first plausible page is the main failure mode.

## What to look for while reading

- **Pre-action options** — checkboxes, toggles and radio choices the user must set *before* the action commits, which change its outcome.
- **Prerequisites** configured on some other screen first.
- **Side effects** — what else changes as a result.
- **Plan-tier gates** — features locked behind a specific plan.
- **Gotchas** the wiki explicitly warns about.
- **Adjacent features** that serve the underlying goal more directly than the literal question.
- **The likely next question**, and its answer, resolved now.

## Conventions in the wiki

**Frontmatter** — every page opens with a metadata block:

| Field | What it gives you |
|---|---|
| `nav_path` | the literal click path through the admin panel |
| `route_path` | the URL path — prefix the store's domain to make it clickable |
| `aliases` | alternative labels and phrasings, **including Bulgarian**; match questions against these rather than assuming the language |
| `plan_gates` | plan features that gate the screen |
| `updated` | when the page was last revised |

**Page structure** — feature pages carry `## Purpose`, `## Where to find it`, `## What the merchant can do here`, `## Settings & fields` (every control: label, effect, default, validation — the section to cite most), `## Business rules`, `## Related`, `## Open questions`. Entity pages use `## Identity` / `## Key Attributes` / `## Where it appears`; concept pages use `## Definition` / `## Scope` / `## Contrasts` / `## Where it applies`.

**Large topics are split** into a hub page plus a subfolder of aspect pages. The hub holds the definition and lists its aspects; each aspect covers one thing and links back. Open the hub when the whole topic is the question, the aspect when the question is specific.

**Reading marks:**

- `(verify)` — the claim was not confirmed against a running system. Repeat the uncertainty; do not present it as settled fact.
- `## Known issues` — separates *by-design* behaviour from genuine defects. That distinction is usually the answer to "is this broken, or am I doing it wrong?".
- `[[wikilinks]]` resolve by **filename stem**, so `[[orders-details]]` means `orders-details.md` wherever it sits in the tree.
- **Verbatim strings are deliberate.** Route paths, setting keys, status values, validation error messages and webhook event names are quoted exactly as the platform emits them, so they can be matched against what the user is actually seeing on screen.

**Platform terminology** — *Administrator* is the store owner, *Moderator* is subordinate staff, *Customer* buys from the storefront, *Subscriber* receives newsletters without necessarily being a customer, *storefront* is the public site, *admin panel* is the back office.

## Non-negotiables

- **Every concrete claim traces to a page you read.** Never invent a navigation path, a field name, or a business rule.
- **Do not bridge two facts into a third.** If the wiki states A and B and they appear to interact, do not conclude C unless a page says C. Flag the gap instead. Plausibility is not evidence, and a confident-sounding inference is indistinguishable from a fabrication to the person reading your answer.
- **State the full predicate of a rule.** When a rule has several conditions, give every one of them. A trigger reported with a condition omitted is wrong, not shorter — and the omitted condition is usually what explains why a real case behaves differently.
- **If the question is ambiguous, ask.** Picking the most plausible reading and answering it produces confident output that may be wrong.
- **Answer in the user's terms.** Use the labels a merchant sees in the admin UI. Widget IDs, route names, component names and wiki page slugs are internal — they belong in your reasoning, not in the answer.
- **Surface design intent.** Many behaviours are deliberate: a screen requires data entered elsewhere first, a workflow separates two concerns on purpose, a limit is fiscal rather than technical. When the wiki says so, say so — otherwise intentional design reads as a missing feature.
- **Flag what the wiki does not cover.** A stated gap is useful; a guess dressed as documentation is not.

## Scope of this copy

This is a **public, redacted** copy of an internal wiki. Some pages were removed and some passages rewritten where they described security mechanics, internal infrastructure, or staff-only tooling. Where a page reads as though something was omitted, it probably was. Nothing that remains was altered in its merchant-facing meaning.
