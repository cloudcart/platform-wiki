---
type: concept
nav_path: "Concept → Multi-language → Sync + fallback"
aliases: ["Master to sister sync", "One-way sync", "Re-translation overwrite", "Sister-side edits lost", "No translation fallback", "Missing translation 404", "Multilang sync rules"]
tags: [i18n, multi-language, multilang, sync, fallback, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[multi-language]]. See the hub for the other aspects (three layers, customer/order locale, Multilang app, translation engine, sister-site model, SEO + switcher).

# Multi-language — sync + fallback rules

## Definition

Three rules govern the data flow between master and sister sites in the Multilang app. Together they explain almost every "translation isn't working as I expected" support ticket:

1. **Sync is master → sister, one-way.** Editing a master entity pushes changes to sisters. Editing a sister entity stays local — the master doesn't pick it up.
2. **Re-triggering translation OVERWRITES sister-side manual polish.** A subsequent `multilang_product_translate` task replaces the sister's content with a freshly-generated translation, throwing away any manual edits made on the sister after the previous translate.
3. **There is no runtime fallback for missing translations.** If a sister doesn't have a translated entity, the storefront does NOT show the master's source-language text — the entity is simply absent on the sister (404 on direct URL, omitted from category listings).

These three rules collectively force a specific merchant workflow: **edit on the master, translate, polish on the sister LAST**, and never re-translate without expecting to redo the polish.

## Scope

Covered:

- The one-way sync direction (master → sister) and what it does + doesn't propagate.
- The re-translation overwrite rule and its operational consequence.
- The missing-translation behaviour (404 + omitted from listings; no source-language fallback).
- The recommended merchant workflow given these rules.

Not covered here:

- The Multilang app + master/sister provisioning — see [[multi-language-multilang-app]].
- The translation engine (Google API, queue tasks, quotas) — see [[multi-language-translation-engine]].
- Per-sister commercial-setting independence (pricing, payment, shipping) — see [[multi-language-sister-site-model]].
- SEO hreflang + the language switcher module — see [[multi-language-seo-and-switcher]].

## Contrasts

- **Master edit (syncs to sisters) vs sister edit (stays local)** — fundamental asymmetry. Treating the sister as "another instance where I can also edit canonically" is the most common merchant misconception about Multilang.
- **Translate task (overwrites) vs sister-side manual polish (stays until next translate)** — the manual polish is durable until the next `multilang_product_translate` runs against the same entity, at which point Google re-generates the field from the master and replaces the sister's value.
- **Sister missing translation (404, omitted from listings) vs sister has translation (rendered normally)** — there is no third state of "rendered with fallback source-language text." A missing entity is missing.

## Where it applies

### Rule 1 — Sync is master → sister, one-way

When the merchant edits a master entity:

- The sync queue picks up the change.
- Each linked sister receives an updated copy (translated or copied per the merchant's setting for that entity).
- The sister's record is updated.

When the merchant edits a sister entity directly:

- The change is saved on the sister.
- **Nothing propagates back to the master.**
- **Nothing propagates to other sisters either** — sister-to-sister is not a path.

This is by design — the master is the canonical content source. If the merchant wants a content change to apply across all languages, the change has to be made on the master.

What sync DOES propagate (content + SEO meta) and what it does NOT propagate (per-sister commercial settings — pricing, payment, shipping, tax, theme) is covered in [[multi-language-sister-site-model]].

### Rule 2 — Re-translation OVERWRITES sister-side manual polish

When the merchant runs `multilang_product_translate` on a product that's already been translated AND manually polished on the sister:

1. Google generates a fresh translation from the master's current content.
2. The fresh translation is written to the sister site's record.
3. The sister's previous content — including any manual polish — is GONE.

There is no merge, no diff, no "preserve manual edits" flag. The translate task is a full overwrite of the translatable fields.

Operational consequence — the recommended workflow:

- **Edit on the master** until the source content is finalised.
- **Run translate ONCE** (or once per re-edit batch on the master).
- **Polish on the sister LAST**, knowing the polish is the LAST step.
- **Never re-translate after polishing** unless the merchant is willing to redo the polish.

For merchants who need the polish to be durable: keep the polished phrasings in an external note (spreadsheet / doc) so they can be reapplied after any future re-translate.

### Rule 3 — No runtime fallback for missing translations

When the sister site is missing a translated entity (e.g., the merchant created a new product on the master but hasn't translated it yet), the platform does NOT automatically render the source-language text on the storefront. The sister site simply doesn't have that entity yet:

- The sister site's category listing won't include it.
- Direct URL access on the sister returns 404.
- The storefront language switcher won't show this entity as available in the missing language.

The merchant has to either:

- **Manually run the translation / copy task** for the missing entity from [[apps-multilang-products]].
- **Configure the sister site to auto-sync new entities** from master (so master-side creates queue a translate task automatically).

There is no runtime fallback "show BG content if EN content is missing" — the storefront only renders what's actually on the sister site's records.

This is sometimes called out by merchants as a feature gap ("why not just fall back to the master text?"), but the platform's design choice is to keep each sister's catalog complete-or-missing, never partially-rendered-in-wrong-language. Showing source-language text on a "translated" site would be more confusing than a clean 404.

### Example — sister-side manual polish lost to re-translation

1. Merchant runs `multilang_product_translate` on "Laptop Acer Aspire 5", sister EN. Google translates.
2. Merchant goes to the EN sister's product editor and polishes the auto-translation (e.g., changes "laptop computer" → "laptop"). Manual polish saved on the sister.
3. Merchant later updates the master product's description (e.g., adds a new feature paragraph).
4. Merchant re-runs `multilang_product_translate`. Google translates the new master description from scratch.
5. The fresh translation OVERWRITES the sister's polished version. The "laptop computer" → "laptop" edit is GONE.

Right workflow: only update the master AFTER all sister polish is done (treating sister polish as "final"), then run translate once.

## Related

- [[multi-language]] — hub.
- [[multi-language-multilang-app]] — master/sister model + cross-site SSO (needed to log into the sister to polish).
- [[multi-language-translation-engine]] — the translate task that does the overwriting.
- [[multi-language-sister-site-model]] — what is per-sister (NOT synced) vs what syncs from master.
- [[apps-multilang-products]] — per-product translation status + manual translate / copy trigger.
- [[apps-multilang-progress]] — sync queue progress tracker.

## Open Questions

- (verify) whether bulk-translate batches that hit quota partway through leave the un-translated entities as "missing translation" (so the sister 404s on them) or as "translated with stale content" (sister keeps prior translation).
- (verify) exact behaviour when the master entity is deleted — does the sister copy stay or get deleted by sync?
