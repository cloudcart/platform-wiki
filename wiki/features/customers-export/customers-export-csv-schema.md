---
type: feature
nav_path: "Customers → Export customers → CSV schema"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_customers
aliases: ["Customer export CSV columns", "Export column list", "Customer CSV schema", "Total Spent column", "Phone column resolution", "Customer export encoding", "Експорт на клиенти — колони"]
tags: [customers, export, csv, schema, encoding]
plan_gates: ["customer_export"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers-export]]. See the hub for the other aspects (trigger & 2FA, filter scope, sync vs async, plan & permissions).

# Export customers — CSV schema

## Purpose

This aspect documents **the exact contents of the exported file**: the fixed column list and order, the appended custom-field columns, how the Phone and Total Spent columns are resolved, the filename pattern, and the encoding difference between synchronous and queued files.

## Where to find it

The columns are not configurable from any UI — they are fixed by the platform. The merchant simply opens the downloaded `.csv` (direct download for small sets, or the queued part files — see [[customers-export-sync-vs-async]]).

## What the merchant can do here

- Read the standard 19 columns plus one extra column per defined customer custom field.
- Open the file in Excel, Google Sheets, or LibreOffice Calc (encoding caveats below).

### What the merchant CANNOT do here

- Pick or reorder columns — the column set and order are fixed.
- Choose a non-CSV format — CSV only.
- Get every address per customer — only the **default shipping address** fields appear (one row per customer).

## Settings & fields

### CSV columns (fixed)

The exported CSV always contains these columns, in this order:

| # | Column | Source |
|---|--------|--------|
| 1 | **ID** | Customer record id |
| 2 | **Email Address** | `email` |
| 3 | **First Name** | `first_name` |
| 4 | **Last Name** | `last_name` |
| 5 | **Language** | Storefront language at export time |
| 6 | **Phone** | Customer phone (default shipping address phone, fallback billing, fallback `alternative_phone`) |
| 7 | **City** | Default shipping address city |
| 8 | **Postal Code** | Default shipping address post code |
| 9 | **Region** | Default shipping address state name |
| 10 | **Country** | Default shipping address country name |
| 11 | **Orders Count** | Completed orders count |
| 12 | **Total Spent** | Lifetime income (monetary value) |
| 13 | **Currency** | Store currency at export time |
| 14 | **Note** | Internal customer note |
| 15 | **Created** | `date_added` formatted `YYYY-MM-DD HH:MM:SS` |
| 16 | **Marketing** | `yes` / `no` |
| 17 | **Active** | `yes` / `no` |
| 18 | **Banned** | `yes` / `no` |
| 19 | **Customer Group** | Group name |
| 20+ | **Custom fields** | One column per defined custom field (see [[customers-custom-fields]]) |

If the store has defined customer custom fields, those columns are appended at the end in the merchant's `sort_order`. Multi-value option fields are joined with `; ` (semicolon + space); plain text and number fields are emitted as the raw stored value.

### Filename pattern

`customers-` + the export timestamp (`Y-m-d-H-i-s`) + `.csv`. The format is local-server time (UTC by default), not the store's timezone — so two exports a minute apart will have unique filenames regardless of the merchant's timezone.

## Business rules

### What "Phone" really resolves to

The Phone column is taken from the customer's DEFAULT shipping address `phone_international` first, falling back to the DEFAULT billing address `phone_international`, falling back to the customer-level `alternative_phone`. Customers with no default-address phone but with phones on a non-default address will show as missing — the export does NOT walk all addresses to find a phone.

### Total Spent is reported in the store's current currency

The "Total Spent" column reflects the customer's `income` aggregate (lifetime revenue from completed orders) and the "Currency" column reflects the **store's current currency**, NOT the currency the orders were placed in. For EUR-currency stores, the `income` value is pre-converted from BGN orders at the fixed rate 1.95583 BGN/EUR before being summed (see [[customer]]). A customer with mixed-currency historical orders shows a single, store-currency-consistent lifetime number.

### Default shipping address only — one row per customer

Multiple addresses per customer are NOT exported — only the **default shipping address** fields. Customers with several addresses still get a single row. To export all addresses, use the API (see [[customers-export-plan-permissions]]).

### Encoding differs by path — Excel implications

The file is standard CSV (comma-separated, UTF-8). Encoding behaviour **differs by path**:

- **Synchronous (small) exports** — built inline by the frontend from the JSON `data` array the server returned. **No UTF-8 BOM.** Excel users opening the file directly may need to import it via "Data → Get External Data → From Text" to preserve UTF-8 (Cyrillic, accented characters). Google Sheets and LibreOffice Calc handle UTF-8 correctly without extra steps.
- **Queued (background) exports** — generated server-side and **prepend the UTF-8 BOM (`\xEF\xBB\xBF`)** with `\r\n` (CRLF) line endings. Excel on Windows opens BOM-prefixed UTF-8 correctly by double-click.

So an inline 4 000-row export and a queued 6 000-row export from the same store can OPEN DIFFERENTLY in Excel — the queued file is the "Excel-friendly" one. If the merchant relies on Excel and the file looks corrupt, ask them to retry under conditions that trip the queued path (apply fewer filters / lift the row count above 5 000 — see [[customers-export-sync-vs-async]]) and the BOM-prefixed file should solve it.

## Related

- [[customers-export]] — hub.
- [[customers-custom-fields]] — definitions of custom fields included as extra columns.
- [[customers-custom-groups]] — group names appear in the `Customer Group` column.
- [[customer]] — entity page; the `income` aggregate + EUR/BGN conversion behind "Total Spent".
- [[customers-details]] — per-customer detail page (the export aggregates these fields per customer).

## Open questions

(All resolved.)
