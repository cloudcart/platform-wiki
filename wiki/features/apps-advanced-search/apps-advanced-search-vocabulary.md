---
type: feature
nav_path: "Apps → Aura Search → Optimization → Synonyms / Stopwords"
route_name: apps.advanced_search.optimization.synonyms
route_path: /admin/apps/advanced_search/optimization/synonyms
aliases: ["search synonyms", "add a synonym", "Shoppers type", "Your catalog calls it", "one way both ways synonym", "stopwords", "ignored words in search", "typo tolerance", "misspelling search", "fuzzy search", "синоними в търсенето", "стоп думи", "думи, които се игнорират", "правописни грешки в търсенето"]
tags: [apps, search, synonyms, stopwords, matching]
plan_gates: ["advanced_search"]
created: 2026-09-23
updated: 2026-09-23
source_count: 5
---

# Aura Search — synonyms, stopwords and typo tolerance

> Part of [[apps-advanced-search]]. See the hub for the other aspects (plans, overview, searches, pins, AI, settings, indexing).

## Purpose

How the **words** of a search are read before anything is matched: which words the shopper's word also stands for (synonyms), which words are dropped (stopwords), and how much misspelling is forgiven. These decide whether a search finds the product at all. Ranking is covered separately on [[apps-advanced-search-ai]].

## Where to find it

**Apps → Aura Search → Optimization**, sub-tabs **Synonyms** (`/optimization/synonyms`) and **Stopwords** (`/optimization/stopwords`). **Add a synonym** on an opportunity card or in a term's drill-down opens the synonym form with the term filled in.

## What the merchant can do here

- **Add synonym** rules: what **Shoppers type** on the left, what **Your catalog calls it** on the right, **One way** or **Both ways**.
- **Remove** a rule, and **Save**.
- Add and delete words in the **Stopwords** list.

## Settings & fields

### Synonyms

| Limit | Value |
|---|---|
| Rules | up to **200** |
| Words or phrases per side | up to **20** |
| Length of one phrase | up to **100** characters |

A rule with an empty side is refused (*At least one word is required*). Everything is stored lower-case.

### Stopwords

A list of words, each up to **100** characters. Saving an empty list is refused (*At least one stopword is required*); the list is cleared with **Delete**.

## Business rules

### How a synonym rule fires

- A rule fires when a **whole word or phrase** from its left side appears in the search. A rule for *tv* fires on *tv stand* but not on *tvorba*.
- **One way:** a search for a left-side word also looks for the right side. *тениска → t-shirt* makes *тениска* find products named *T-shirt*, but not the other way round.
- **Both ways:** each side also looks for the other — what a merchant means by "these are the same thing".
- A search matching several rules collects all their right sides.
- A synonym **adds** to what the shopper typed; it never replaces it.

### 🔴 Synonyms apply on the next search — no reindex, whatever the screen says

The synonym screen reads *New synonyms apply after the next reindex*. In fact the rules are applied **when each search is built**, so a saved rule works on the very next search, in the dropdown and on the `/search` page. Rebuilding the index is not needed.

### A synonym widens what matches, not what "all words" requires

With **Require all search words to match** on ([[apps-advanced-search-settings]]), every word the shopper typed must still be found. A product that is only reached through a synonym has to pass that test too. When a synonym "does nothing", this setting is the first thing to check.

### When to use a synonym

The usual source is the **No results** view ([[apps-advanced-search-analytics]]). The *finds nothing, but you sell it* card points at exactly this case: shoppers' word and the catalogue's word differ. Brand names spelled in another alphabet (*айфон* / *iPhone*), slang, and trade names versus everyday names are the typical rules.

### 🔴 The Stopwords list is saved, but the search does not use it

The **Stopwords** tab keeps the words entered there, and they are listed again on the next visit. **The search does not currently read that list.** Adding a word to it does not change any search result.

The words the search **does** ignore are a built-in list for the **store's language**, applied as the search runs:

- Common function words — *и*, *с*, *за*, *the*, *and*, *of* and the like — are dropped from searches of **two or more words**. Colours and small numbers that a general list would drop (*син*, *две*, *три*) are **kept** in Bulgarian, because shoppers filter by them.
- **Stray single letters** in a multi-word search are dropped.
- A **one-word** search is never stripped. Searching just *с* still runs.
- If every word would be dropped, the search runs as typed.

Built-in lists exist for Bulgarian, English, German, Greek, Russian, French, Romanian, Turkish, Italian, Spanish, Polish, Finnish, Hungarian, Czech and Dutch. For other store languages only the single-letter rule applies.

### Typo tolerance is automatic, and scaled to word length

Misspellings are forgiven by how long the word is:

| Word length | Misspelling forgiven |
|---|---|
| 1–4 characters | none — must match exactly |
| 5–7 characters | one wrong, missing or extra letter |
| 8+ characters | two |

So *маратонка* finds *маратонки*, but a four-letter word typed with one wrong letter finds nothing. **Codes, SKUs and barcodes** are matched exactly regardless. The level cannot be changed from the admin; every store uses this setting.

When a search finds products only because a misspelling was forgiven, the engine counts it under **Typos corrected** ([[apps-advanced-search-ai]]). The query itself is never rewritten.

## Related

- [[apps-advanced-search]] — hub.
- [[apps-advanced-search-analytics]] — the **No results** terms synonyms are made for.
- [[apps-advanced-search-overview]] — the opportunity card that opens the synonym form.
- [[apps-advanced-search-settings]] — "Require all search words to match" and the searched fields.
- [[apps-advanced-search-pinned]] — pinning, for when the product is found but not first.
- [[apps-advanced-search-ai]] — what happens after the words are read: matching by meaning and ranking.

## Open questions

- Whether the merchant's Stopwords list is meant to be applied again in a later release. Nothing reads it at present.
