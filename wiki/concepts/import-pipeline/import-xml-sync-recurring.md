---
type: concept
nav_path: "Concept → Import pipeline → XML Sync (recurring)"
aliases: ["Recurring XML import", "XML Sync schedule", "Feed hash short-circuit", "Per-field update policy", "Discontinued product handling", "XML sync transport", "xml_sync-interval"]
tags: [ops, imports, xml, sync, feeds, concepts]
plan_gates: [xml_sync_limit, "xml_sync-interval"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[import-pipeline]]. See the hub for the other aspects (stages, concurrency lock, validation, upsert + provenance, plan gates + 2FA, history + recovery).

# Import pipeline — XML Sync (recurring)

## Definition

[[apps-xml-sync]] is the **recurring** variant of the XML import pathway. Instead of one-shot upload + process, the merchant configures a feed URL + mapping ONCE and the platform pulls fresh data on a recurring schedule (default 12 hours; plan-feature `xml_sync-interval` can shorten the cadence for higher-tier plans). Each sync run is recorded as its own row in [[settings-import-history]].

XML Sync is **plan-gated by `xml_sync_limit`** — a quota of concurrent sync tasks per plan. A merchant exceeding the limit can't add more sync feeds until they upgrade. The sync supports **per-field update policies** (always update price; never overwrite description), **discontinued-product handling** (deactivate / keep when SKU disappears from feed), and a **feed-hash short-circuit** (skip downstream insertion when the feed content hasn't changed since last sync).

## Scope

Covered:

- Recurring schedule mechanics — default 12-hour cadence + `xml_sync-interval` plan cap.
- Per-field update policies — always update / update if delta < N% / never update.
- Discontinued-product handling — "Disable missing items" toggle.
- Feed-hash short-circuit — skipping insertion when feed unchanged.
- HTTP / HTTPS transport constraints — no FTP, no SFTP, no S3, no Basic Auth headers, no gzip.
- One-time mapping reuse — sync tasks don't re-map every run.
- Per-run history rows in [[settings-import-history]].
- The status surface — [[apps-xml-sync-status]] for verifying recent runs.

Not covered here:

- One-time XML import (non-recurring) — see [[apps-xml-import]] feature page.
- Concurrent-import lock interaction (a manual "Run now" can be blocked) — see [[import-concurrency-lock]].
- Plan gates on the sync task itself — see [[import-plan-gates-and-2fa]].

## Contrasts

- **Recurring XML Sync vs one-time XML Import** — [[apps-xml-import]] is fire-and-forget; the merchant uploads / configures a URL, the platform processes, done. [[apps-xml-sync]] is recurring — same feed URL, runs every 12 hours (or shorter). Both share `import1` queue.
- **One-shot mapping vs reused mapping** — for one-time imports the mapping lives only on that task. For XML Sync, the mapping is reused on every scheduled run — the merchant doesn't re-map every 12-hour pull.
- **Per-field update policy vs full upsert** — most importers do a blanket upsert on mapped fields. XML Sync layers per-field policies on top, so the merchant can pin certain fields against feed-driven changes (e.g., never overwrite the merchant-curated description with the supplier's generic copy).
- **Feed-hash short-circuit vs always-process** — XML Sync hashes the parsed feed content and skips downstream insertion when the hash matches the last sync. Most other importers process every run.

## Where it applies

The XML Sync flow has three configuration screens + ongoing scheduled runs:

- **Sync task creation / edit** — [[apps-xml-sync]] (Apps → install → XML Sync → New / Edit).
- **Recent run status** — [[apps-xml-sync-status]] — last N runs with timestamps + outcome.
- **Historical audit** — [[settings-import-history]] — every scheduled run gets its own history row.

### Scheduled-run lifecycle

1. **Sync task configured** — merchant enters feed URL, picks match column (`sku` / `barcode` / `product.id`), maps XML fields → product fields, sets per-field update policies + discontinued-product handling.
2. **First run fires immediately** after save — re-initialises the parser queue and pulls the feed.
3. **Subsequent runs** fire every 12 hours by default (or shorter per `xml_sync-interval` plan feature).
4. **Each run** writes a row to [[settings-import-history]] with stats (`created_count`, `updated_count`, `skipped_count`, `failed_count`).
5. **Manual "Run now"** is available from the sync task — kicks off an immediate run (subject to the [[import-concurrency-lock]] gate).

### Per-field update policies

For each mapped field the merchant picks an update policy:

- **Always update** — overwrite every run. Typical for price, quantity.
- **Update if delta within N%** — overwrite only if the new value differs by less than N percent from the current. Protects against feed typos (a feed with `price=0.01` instead of `100` would otherwise zero out pricing).
- **Never update** — set on initial import, never overwrite after. Typical for merchant-curated descriptions and SEO fields.

### Discontinued-product handling

The "Disable missing items" toggle on the sync task decides what happens when an SKU that was previously in the feed disappears (the supplier discontinues it):

- **ON** — the product is auto-deactivated (visibility = inactive). The product still exists in the database; it just stops showing on the storefront. The merchant decides later whether to delete it permanently.
- **OFF** — the product stays as-is. The merchant's stock and visibility are not touched.

ON is the safer default for syncing-only catalogues (no manually-added products that aren't in the feed). OFF is safer for mixed catalogues where the merchant has products not in the supplier feed.

### Feed-hash short-circuit

After parsing the feed, XML Sync computes a hash of the parsed content. If the hash matches the previous sync's hash, **downstream insertion is skipped entirely** — no upsert runs, no webhooks fire, no the search index re-indexes. The history row still gets written (with `skipped_count` reflecting all rows), but no actual database writes occur.

The short-circuit dramatically reduces cost on syncs against feeds that change infrequently. A daily feed that's only updated weekly will skip the upsert 6 days out of 7.

### HTTP / HTTPS-only transport

- **FTP / SFTP / S3** are NOT supported.
- **HTTP Basic Auth / OAuth / API-key headers** are NOT configurable — the only escape hatch is the `parameters` field (Step 1) which adds query-string key/value pairs to the URL.
- **Gzip-compressed feeds** are NOT auto-decompressed — parser expects raw XML.
- **Last-Modified / If-Modified-Since headers** are NOT checked — the platform always fetches; the feed-hash short-circuit handles the no-change case after fetch.

These constraints are why some supplier integrations need a thin proxy to translate FTP / SFTP / Basic-Auth into a plain HTTPS URL.

### Example — daily supplier XML sync

Merchant installs [[apps-xml-sync]] → creates a sync task → enters feed URL `https://supplier.com/feed.xml`, picks "Match by SKU" as `product_map`, maps XML fields, sets per-field policies (always update price + quantity, never update description), enables "Disable missing items". The first sync fires immediately on save; subsequent syncs run every 12 hours (or shorter per `xml_sync-interval`). Each run writes a history row in [[settings-import-history]] with stats. The merchant verifies recent runs via [[apps-xml-sync-status]]; after 6 months the history has 365+ rows because retention is indefinite — see [[import-history-and-recovery]].

## Related

- [[import-pipeline]] — hub.
- [[apps-xml-sync]] — the feature page for the sync task itself.
- [[apps-xml-sync-status]] — last-N-runs status surface.
- [[apps-xml-import]] — one-time XML import (the non-recurring sibling).
- [[settings-import-history]] — per-run history rows.
- [[import-concurrency-lock]] — manual "Run now" is subject to the single-import lock.
- [[import-plan-gates-and-2fa]] — `xml_sync_limit` + `xml_sync-interval` plan features.
- [[import-upsert-and-provenance]] — per-field upsert pattern that the policies extend.

## Open Questions

- Exact delta-percentage range options for the "update if delta < N%" policy (single value, dropdown, per-field?).
