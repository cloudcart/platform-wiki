---
type: feature
nav_path: "Apps → XML Import → Fetch transport"
route_name: apps.xml_import
route_path: /admin/apps/xml_import (backend fetch layer; no UI)
aliases: ["XML Import fetch transport", "XML Import — URL source", "XML Import — Guzzle 120s timeout", "XML Import — SSL verification off", "XML Import — User-Agent", "XML Import — encoding detection", "XML Import — Ping::host", "XML Import — xml_hash", "XML Import — 3-strike auto-deactivate"]
tags: [apps, imports, xml, transport, fetch, encoding]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-xml-import]]. See the hub for the other aspects (wizard, job pipeline, mapping fields, plan gates, side effects).

# XML Import — fetch transport

## Purpose

When the parse stage runs (see [[apps-xml-import-job-pipeline]]), it has to actually GO and get the XML. The fetch transport defines how the platform reaches out to the supplier's URL, what it tolerates (broken SSL certs, non-standard encodings, gzip), what it rejects (file uploads, unreachable hosts), and how it short-circuits when nothing has changed. It also defines the 3-strike auto-deactivate that protects the platform from feeds that have permanently broken.

This page covers the transport layer end-to-end. The pipeline that schedules these fetches is on [[apps-xml-import-job-pipeline]]; what gets parsed out of the fetched bytes is on [[apps-xml-import-mapping-fields]].

## Where to find it

There is no merchant UI for the transport. Failures surface in two places:

- The Status page (task list) shows a red exclamation icon — hover reveals the underlying error string.
- An in-CP admin notification fires per failure strike (separate from the task's `error` column).

## What the merchant can do here

- Diagnose a failing task by reading the error tooltip on the Status page.
- Re-enable an auto-deactivated task once the underlying feed problem is fixed.
- Change the feed URL via the wizard — see [[apps-xml-import-wizard]].

What the merchant CANNOT do here:

- Upload a file directly — only HTTP/HTTPS URLs are accepted. For file-based imports use [[apps-csv-import]].
- Increase the 120 s fetch timeout. Slow feeds simply have to be hosted on faster infrastructure or chunked at source.
- Override SSL peer verification (it's already permissive — disabled by default).

## Settings & fields

Transport defaults:

| Setting | Value | Notes |
|---------|-------|-------|
| Source type | URL only (HTTP / HTTPS) | File upload NOT supported. |
| Timeout | **120 s** total per request | Anything slower aborts as an error → strike. |
| SSL peer verification | **Off** | Self-signed / broken certs still work. |
| Decode content | Off | gzip / deflate responses are NOT auto-decompressed. |
| User-Agent | Fake Chrome 120 on Windows | Unblocks suppliers that gate by UA. |
| `Accept-Language` | Merchant's storefront language | Used by some feeds to localise. |
| Pre-fetch check | the platform code on URL | Fast-fails unreachable hosts before the full Guzzle call. |
| Hash short-circuit | `xml_hash` MD5 of response body | Identical bytes = no records inserted. |
| Strike threshold | **3 consecutive failures** | Task auto-deactivates. |

## Business rules

### Source = URL only

The `xml_import.url` is required and must be a valid URL — the source must be a publicly-fetchable HTTP/HTTPS endpoint. **File upload is NOT supported in this app**; for spreadsheets / non-URL sources the merchant uses [[apps-csv-import]] instead.

### Fetch transport — 120 s timeout, no SSL peer verification, browser-style User-Agent

The fetch uses Guzzle with:

- **Timeout: 120 seconds** total per request. Any feed taking longer aborts as an error and counts as a strike.
- **SSL peer verification disabled** — feeds with broken / self-signed certificates still work. Some supplier infrastructure ships expired or self-signed certs; this default keeps imports unblocked.
- **Decode content: off** — gzip / deflate responses are NOT auto-decompressed (the streaming parser expects raw XML text; auto-decompression conflicts with the encoding detector below).
- A **fake browser User-Agent** (Chrome 120 on Windows). Some supplier feeds gate access by user-agent; this default unblocks most cases.
- Custom `Accept-Language` header set to the merchant's storefront language.

### Pre-fetch reachability check

Before issuing the actual fetch the task uses the platform code reachability check on the URL. If the host is unreachable the task short-circuits — recorded as a strike + admin notification — without attempting the full Guzzle fetch. This is faster failure feedback than waiting for the 120 s timeout.

### Encoding detection — reads `<?xml encoding="..." ?>` preamble

The platform reads the first 10 lines (120 chars each) of the URL stream and looks for the `<?xml... encoding="..." ?>` declaration. The declared encoding is passed to the streaming XMLReader. If no declaration is found, **UTF-8 is assumed**. There is **no on-the-fly mb_convert_encoding** — the file is consumed in its declared encoding directly. Feeds declared as CP1251 / Windows-1251 are honoured.

This matters for Bulgarian-supplier feeds that ship in Windows-1251 (still common). As long as the preamble correctly declares the encoding, the import works.

### `xml_hash` short-circuit — identical content skips insert

After each fetch the platform computes an MD5 over the raw response body. If the hash matches the previously stored `xml_hash` for the task, **no records are queued for insertion** — the existing catalog is left untouched. This makes unchanged feeds cheap: the parse still runs and computes the hash, but downstream writes are skipped.

The fetch + parse still consume time / network — only the downstream write is skipped. This is also why editing the wizard fields clears `xml_hash`: see [[apps-xml-import-wizard]] for the edit-clears-hash mechanic.

### 3-strike auto-deactivate on consecutive failures

Every fetch / parse failure increments the task's internal counter. **On the 3rd consecutive failure the task is auto-deactivated** (active flipped to 0). The merchant must investigate and re-enable manually. A successful run resets the counter.

Conditions that count as a failure strike:

- The feed URL is unreachable (DNS / TCP-level failure from the platform code pre-check, returned as a curl-style error).
- The fetch returns a non-200 HTTP status code.
- The fetch throws any other exception (timeout, SSL failure beyond peer-verification, malformed response).

Each strike triggers an admin notification (in-CP alert) — separate from the task's `error` column on the Status list. The alert message carries the **app name + task name + the error text**, but **no clickable link** to the task. To investigate, the merchant opens the XML Import task list / [[apps-xml-import-status|Status page]] — there the task name links to its editor and the red-icon tooltip shows the last error. (No email is sent for these strikes — the alert is in-CP only.)

### What the merchant sees on the Status page

The red exclamation icon next to a task is the entry point: hovering shows the error string from the last attempt. The active toggle reflects 3-strike auto-deactivation — flipped OFF means the platform stopped trying. The merchant manually toggles back ON after fixing the underlying feed problem; the strike counter resets on the next successful run.

## Related

- [[apps-xml-import]] — hub.
- [[apps-xml-import-job-pipeline]] — where the fetch is invoked from.
- [[apps-xml-import-wizard]] — URL configuration; editing the URL clears `xml_hash` and forces a re-fetch.
- [[apps-xml-import-status]] — the Status screen where failure tooltips and the active toggle live.
- [[apps-csv-import]] — alternative for file-based imports.

## Open questions

_None._
