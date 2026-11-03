---
type: feature
nav_path: "Apps → XML Sync → Fetch transport"
route_name: apps.xml_sync
route_path: /admin/apps/xml_sync (feed fetch)
aliases: ["XML Sync fetch transport", "XML Sync feed URL", "XML Sync HTTP only", "XML Sync no FTP", "XML Sync no auth", "XML Sync parameters", "XML Sync encoding", "XML Sync CP1251", "XML Sync no gzip", "XML Sync User-Agent"]
tags: [apps, imports, xml, sync, recurring, transport, encoding]
plan_gates: ["xml_sync_limit"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-xml-sync]]. See the hub for the other aspects (job pipeline, update policy, discontinued handling, side effects).

# XML Sync — fetch transport

## Purpose

Before XML Sync can do anything, it has to **fetch the supplier feed over the wire**. This page documents what transports are supported (HTTP/HTTPS URL only), what authentication is and is not possible, the HTTP client settings (timeout, SSL, User-Agent), how feed encoding is detected, and the gzip limitation. These constraints decide whether a given supplier feed can even be connected to XML Sync at all — the most common "the feed won't load" support cause.

## Where to find it

- The feed **URL** and **`parameters`** fields are on Step 1 of the [[apps-xml-sync]] wizard.
- Fetch failures surface on [[apps-xml-sync-status]] (the task `error` column) and as in-CP admin alerts — see the 3-strike rule in [[apps-xml-sync-job-pipeline]].

## What the merchant can do here

- Point the task at any **HTTP or HTTPS URL** that returns raw XML.
- Append query-string credentials via the **`parameters`** field (the only auth-style escape hatch).
- Use feeds declared in **CP1251 / Windows-1251** as well as UTF-8, provided the encoding is declared in the XML preamble.

What the merchant **cannot** do here:

- Use **FTP / SFTP / S3** transport — not supported.
- Configure **HTTP basic-auth / OAuth / API-key headers** — header-based auth is not supported.
- Feed **gzip-compressed** XML — feeds are not auto-decompressed; the parser expects raw XML on the wire.
- Upload a file directly — only URLs are accepted. For file-based imports use [[apps-csv-import]].

## Settings & fields

| Field / setting | Value |
|-----------------|-------|
| Feed source | HTTP / HTTPS **URL only** (validated as a standard URL) |
| `parameters` | Step 1 query-string key/value pairs appended to the URL |
| HTTP client timeout | **120 seconds** |
| SSL peer verification | **off** |
| `decode_content` | off (no auto-gzip) |
| User-Agent | browser-style header |
| Encoding source | the `<?xml encoding="..."?>` preamble (first 10 lines, 120 chars each); UTF-8 default |

## Business rules

### HTTP/HTTPS URL only — no FTP, no auth, no auto-decompression

The URL is validated as a standard HTTP/HTTPS URL. **FTP / SFTP / S3 transport is NOT supported.** **HTTP basic-auth / OAuth / API-key headers are NOT supported** as configuration. The only authentication-style escape hatch is the **`parameters`** field on Step 1 — query-string key/value pairs appended to the URL, so a supplier feed expecting `?token=XYZ&key=ABC` works, but anything requiring an HTTP header does not. **Gzip-compressed feeds are NOT auto-decompressed** — the parser expects raw XML text on the wire.

### Fetch transport: 120s timeout, SSL peer verification off, browser-style User-Agent

The HTTP client uses the same configuration as XML Import — a **120-second timeout**, **SSL peer verification off**, **`decode_content` off** (no auto-gzip), and a **browser-style User-Agent** header (some suppliers block non-browser clients). The stream-level context used for charset detection (a separate, non-client read) similarly disables SSL verification and sets a 10-second connect timeout. SSL being off means a supplier with a broken / expired certificate still loads — convenient, but the merchant should trust the source URL.

### Encoding: declared in the `<?xml encoding="..."?>` preamble; UTF-8 default

The platform reads the **first 10 lines (120 chars each)** from the URL stream and parses the `<?xml encoding="..." ?>` attribute, passing the declared encoding to the XML reader. **CP1251 / Windows-1251 feeds are supported when correctly declared in the preamble.** If no preamble is found, **UTF-8 is assumed**. A Cyrillic feed served as Windows-1251 but lacking the declaration will mojibake — the fix is for the supplier to declare the encoding, not a CloudCart setting.

### `xml_hash` short-circuit follows the fetch

After a successful fetch + parse, the content hash (`xml_hash`) is computed and compared to the stored value to skip unchanged feeds — but that is a pipeline concern documented in [[apps-xml-sync-job-pipeline]]. The fetch itself **always happens** regardless; there is no Last-Modified / If-Modified-Since pre-check.

## Related

- [[apps-xml-sync]] — hub.
- [[apps-xml-sync-job-pipeline]] — the `xml_hash` short-circuit + 3-strike failure handling that consumes the fetch result.
- [[apps-xml-sync-status]] — where fetch / parse failures surface.
- [[apps-xml-import-fetch-transport]] — the sibling import's identical transport configuration.
- [[apps-csv-import]] — file-based alternative when the source isn't a URL.

## Open questions

_None._
