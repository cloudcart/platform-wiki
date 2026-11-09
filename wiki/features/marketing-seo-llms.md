---
type: feature
nav_path: "Marketing → SEO → Llms.txt file"
route_name: seo-main
route_path: /admin/marketing/seo
aliases: ["llms.txt", "Llms.txt file", "LLM instructions", "AI assistant instructions", "AI crawler file", "llmstxt.org", "tell ChatGPT about my store", "AI shopping assistants", "llms.txt файл", "инструкции за изкуствен интелект", "AI асистенти", "какво вижда ChatGPT за магазина"]
tags: [marketing, seo, llms, ai, discoverability]
plan_gates: []
created: 2026-08-24
updated: 2026-11-09
source_count: 6
---
# Llms.txt file (instructions for AI assistants)

## Purpose

A plain-text file the store publishes at **`/llms.txt`** telling AI assistants what the shop sells and which pages are worth reading. It follows the **llmstxt.org** convention and is the sibling of [[marketing-seo-robots|robots.txt]]: *robots.txt says where crawlers may not go; llms.txt says what is worth understanding.*

The merchant writes it in **Markdown**, in their own words. It is not a catalogue dump and not a feed — the format asks for a title, a one-line summary of the business, and a short list of links an assistant should follow.

## Where to find it

Sidebar → **Marketing → SEO** (`/admin/marketing/seo`) → the **Llms.txt file** card. It is a plain 10-row text area, saved with the card's own **Save** button like every other card on that screen — see [[marketing-seo-overview-card-save]].

The published result is at `https://<store-domain>/llms.txt`.

## What the merchant can do here

- Write the file's whole contents by hand, in Markdown.
- Leave the store's generated summary in place (see below). The box opens pre-filled with that summary; saving it, even unchanged, stores a fixed copy that no longer follows later changes to the name, description or contacts. Clearing the box and saving returns to the live summary.
- Replace it at any time — the public file follows within five minutes at most.

### What the merchant CANNOT do here

- Switch the file off. There is no toggle, and clearing the box does **not** stop `/llms.txt` from answering.
- Serve a different file per domain or per store language — one text is published on every domain the store answers on.
- Have the platform keep it in sync with the catalogue. Nothing is regenerated after the merchant types their own text; it stays exactly as written until they change it.

## Settings & fields

| Field | What it does | Limits |
|---|---|---|
| **Llms.txt** (`llms.txt`) | The exact body served at `/llms.txt`. Markdown, published verbatim. | Up to **65 536 characters**. Blank is allowed and means "use the generated summary". |

Saving also stamps the file's **last-modified** time, which is what assistants see in the response header.

## Business rules

### Empty does not mean off — the store describes itself instead

Clearing the field does not remove the file. The store falls back to a **summary built from what it already knows about itself**:

- `# ` the **store name** ([[settings-general]]) — or the domain, if the name was never filled in.
- `> ` the **SEO description of the CMS page assigned as the home page** ([[landing-pages-system-slots]]), not the Home section on [[marketing-seo-meta]]. Skipped when no page holds the home slot or the description merely repeats the store name. Each language version of a multi-language store is its own store and publishes its own file.
- `## Pages` — a link to the store home and one to `/contacts`.
- `## Contact` — the store's e-mail ([[settings-general]]) and the **Phone** of the invoicing issuer details ([[settings-invoicing-issuer-block]]), each only when filled in. The phone is printed exactly as typed there: no reformatting, a `+` only if the merchant typed one. To fix a wrong phone in the file, correct that field (or write the file by hand).

This is a **starting point, not a strategy**. It says the shop exists and how to reach it; it says nothing about what the shop is good at, which brands it carries, or which pages matter. A merchant who cares about how assistants describe them should write their own.

### 🔴 The generated summary always links to the PRIMARY domain

The file is served on **every** domain the store answers on, but the links inside the generated version are built from the store's **primary** domain ([[settings-domains]]). So a store on several domains publishes, on each of them, a file pointing back at the primary one.

That is harmless for a store with one real domain and a redirect. It matters when two domains are genuinely separate storefronts — the assistant reading the secondary domain is sent to the primary. Writing the file by hand does not fix this either, since the same text is served everywhere. A merchant in that position should write links that are correct for the domain that matters most to them.

### Trial and expired stores serve nothing at all

A store on a **trial** plan, or one whose plan has **expired**, publishes no llms.txt: the URL answers **404**, not an empty page. That is deliberate — *"no such file"* is a truthful answer, whereas an empty file would read as *"this shop describes itself as nothing"*.

This mirrors how those stores are held back from crawlers generally — see [[marketing-seo-overview-trial-block]]. The moment the store is on a paid plan, the file starts answering. A store in development mode does serve its file (so it can be previewed), while its robots.txt still blocks everything; demo stores serve it normally.

A store domain routed to a Nitrogen storefront serves this same file: the platform keeps `/llms.txt` there. See [[headless-legacy-vs-nitrogen]].

### Changes appear within five minutes

The response is cached for **five minutes**, and the cache is cleared the moment the merchant saves this box — so a save is normally visible immediately. A change to the store name, e-mail, phone or home-page description is not tied to that clearing: allow up to five minutes for the generated summary to follow. The response also carries a `Cache-Control: public, max-age=300` header, so whatever fetched the file may hold its own copy for that long.

### It is a public file, published exactly as typed

Everything in the box is served verbatim on a public URL that anyone can open. It is not a private channel to an AI vendor: treat it like any other page of the shop and keep internal notes, prices for specific customers, and staff instructions out of it.

There is also no guarantee any given assistant reads it. The convention is voluntary — publishing the file makes the store's own description available to those that do.

## Related

- [[marketing-seo]] — hub: the SEO screen and its cards.
- [[marketing-seo-robots]] — the crawler-directive sibling; the two files answer different questions.
- [[marketing-seo-sitemap]] — the machine-readable URL list, for crawlers rather than assistants.
- [[marketing-seo-overview-card-save]] — the per-card Save / Revert model this box follows.
- [[marketing-seo-overview-trial-block]] — why trial and expired stores are held back.
- [[landing-pages-system-slots]] — the page in the home slot, whose SEO description is the summary line.
- [[settings-general]] — store name and e-mail; [[settings-invoicing-issuer-block]] — the phone.
- [[settings-domains]] — the primary domain the generated links are built from.

## Open questions

- Whether a merchant serving genuinely separate storefronts on two domains has any supported way to publish a different llms.txt per domain, or whether the single shared text is the intended ceiling.
