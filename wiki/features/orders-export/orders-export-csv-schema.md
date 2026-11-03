---
type: feature
nav_path: "Orders → Export → CSV schema"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders
aliases: ["Orders export columns", "Orders export schema", "Orders CSV columns", "Export column list", "Export ghost rows", "Export UTF-8 BOM", "Export CRLF"]
tags: [orders, export, csv, schema, columns]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-export]]. See the hub for related aspects (trigger / 2FA, sync vs async, delivery, filter scope, permissions / plan).

# Orders export — CSV schema

## Purpose

Documents the **fixed canonical column set**, multi-row layout, product-option "ghost row" representation, header translation, and encoding choices (UTF-8 BOM + CRLF) that determine what the orders-export CSV looks like once the merchant opens it. The merchant cannot customise the schema from this UI — for custom column sets they must transform the exported CSV in their own tools.

## Where to find it

The CSV is produced by both the synchronous and asynchronous paths described in [[orders-export-sync-vs-async]]. The schema below applies to both — the only differences are encoding choices on the async ZIP-bundled output (BOM + CRLF).

## What the merchant can do here

- Read the produced file in Excel / Google Sheets / Numbers — column headers are language-translated for the merchant's admin UI language.
- Re-shape columns in the merchant's own tooling after export (the schema is fixed at write time).

The merchant CANNOT add / remove / re-order columns from the export UI, choose XLSX / XML / JSON output, or merge the multi-row line-item layout into one row per order.

## Settings & fields

### Fixed column schema

The CSV uses a fixed column ordering across both sync and async paths. The full column list:

| # | Column |
|---|--------|
| 1 | Order ID |
| 2 | Created (date) |
| 3 | Product name |
| 4 | Variant option 1 |
| 5 | Variant option 2 |
| 6 | Variant option 3 |
| 7 | Product options (custom text / file labels) |
| 8 | SKU |
| 9 | Barcode |
| 10 | Product quantity |
| 11 | Vendor |
| 12 | Weight |
| 13 | Product price |
| 14 | Discounted price |
| 15 | Total price before discount |
| 16 | Total price after discount |
| 17 | Category |
| 18 | Customer name |
| 19 | Customer email |
| 20 | Phone |
| 21 | Shipping address |
| 22 | State |
| 23 | City |
| 24 | Total |
| 25 | Discount |
| 26 | Tax amount |
| 27 | Delivery method |
| 28 | Shipping price |
| 29 | Payment provider |
| 30 | Payment status |
| 31 | Payment provider reference ID |
| 32 | Order status |
| 33 | Shipment status |
| 34 | Tracking number |
| 35 | Invoice number |
| 36 | Invoice create date |
| 37 | Credit number |
| 38 | Credit create date |
| 39 | Postal code |
| 40 | Billing address |
| 41 | Company MOL |
| 42 | Company name |
| 43 | Company Bulstat (EIK) |
| 44 | Company VAT |
| 45 | Admin note |
| 46 | Note from merchant |
| 46+ | Shipping hours receiving (when ShippingHoursManager app installed) |
| Last 5 | Referer + UTM campaign / medium / source + Discount code |

### Row mode — one row per line item

Multi-row: a single order with N line items produces **N rows** in the CSV (one per product line). The order-level fields (customer, totals, addresses, etc.) repeat on each row.

### Product-option ghost rows

For each order line with product options (custom text, file uploads, dropdowns selected by the customer at checkout), the export adds **one extra "ghost" row** per option after the product line. The ghost row has the option name as the product name and the option quantity / price filled in; all other columns are blank. This creates a parent-child layout in the CSV that flattens product-with-options into multiple lines per order item.

## Business rules

### Headers translated per admin language

The export's column headers are translated based on the admin's current language (`site('language_cp')`). When the merchant has the admin UI set to Bulgarian, headers come in Bulgarian. For multi-language stores, the merchant may want to switch admin language before exporting to match the destination system's expected language.

### UTF-8 BOM prepended on async CSV files

The asynchronous (queued) CSV writer prepends the UTF-8 BOM bytes (EF BB BF) at the start of each generated CSV file before upload. This ensures Excel on Windows opens the file in UTF-8 mode instead of falling back to Windows-1251 / mojibake. The synchronous browser-built CSV does NOT add the BOM directly — the frontend's CSV handler typically handles it client-side. Merchants opening the asynchronous file in Excel should see Bulgarian / Greek / Cyrillic / accented characters correctly without a manual import step.

### CRLF line endings on async CSV

The async CSV writer uses CRLF (`\r\n`) line endings on every row, including the header. This matches what Excel-on-Windows and locale-default text viewers expect — without it, some viewers collapse the entire CSV onto one line, which merchants typically describe as "wrong encoding." Both sync and async outputs end up CRLF-formatted once unzipped, so behaviour is effectively identical between the two delivery paths.

### Date formatting follows merchant preference

The `Created` column and any invoice / credit-note date columns are formatted using the merchant's `date_format` setting. A merchant who uses `d.m.Y` in their CloudCart settings will see `26.05.2026` in the CSV; a merchant on `Y-m-d` sees `2026-05-26`. This applies to BOTH sync and async paths.

### Currency formatting respects each order's currency

The price columns (`Product price`, `Discounted price`, `Total price`, `Discount`, `Tax amount`, `Shipping price`) use each individual **order's** currency — not the store's default. For multi-currency stores, the CSV will contain rows with mixed currencies (e.g., one row in EUR, the next in USD). Merchants who need a single-currency export should filter the orders list by currency first — see [[orders-export-filter-scope]].

### Conditional last columns

The last block of columns is conditional:

- **Shipping hours receiving** — appears only when the `ShippingHoursManager` app is installed.
- **Referer + UTM (campaign / medium / source) + Discount code** — always appear as the last 5 columns.

## Related

- [[orders-export]] — hub.
- [[orders-export-sync-vs-async]] — the two paths that both produce this same schema (with the BOM / CRLF difference noted above).
- [[orders-export-delivery]] — where the file lands and how the merchant opens it.
- [[orders-export-filter-scope]] — the currency-filter caveat for clean single-currency exports.
- [[order]] — entity page (the exported records).

## Open questions

None.
