---
type: feature
nav_path: "Apps → N18 Audit"
route_name: apps.n18_audit.overview
route_path: /admin/apps/n18_audit
aliases: ["N18 Audit", "N18 fiscal audit", "Naredba N18", "Регистър Наредба Н-18", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, fiscal, audit, compliance, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# N18 Audit (Bulgarian fiscal-compliance register)

## Purpose

**N18 Audit** integration — Bulgaria-specific fiscal-compliance module that generates **monthly XML audit files** per Annex №38 of Ordinance H-18/2006 ("Наредба Н-18"). For merchants applying the **alternative regime for absentee payments** ("алтернативен ред за дистанционни плащания") under Bulgarian tax law.

What it does:
- Generates one XML file PER REPORTING MONTH from the store's **orders** — its sales and reversals for that month — in the `dec_audit.xsd` schema (Annex 38), Windows-1251 encoding.
- Stores generated XMLs in CloudCart for re-download.
- The merchant downloads each XML and submits it to NAP (Bulgarian National Revenue Agency) through the NAP portal — from the 1st to the 15th of the month following the reporting month.

The merchant must first register their e-shop with NAP per Annex 33; NAP issues a unique e-shop number (UIN / `e_shop_n`) that the integration requires.

**This is NOT real-time fiscal-receipt reporting.** CloudCart does NOT auto-submit to NAP — it produces a monthly file the merchant uploads manually. For real-time fiscal receipts and customer-facing QR codes, the merchant integrates a registered fiscal device (separate from this app).

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What the merchant does control is the app's own settings — the audit reporting is driven by the `active` setting (with the NAP-assigned `uin`), not by an app-level on/off button.

## Where to find it

Sidebar → Apps → install → **N18 Audit**. See [[apps-n18-audit-settings]] for configuration.

## What the merchant can do here

- Add a reporting period (single month) and generate its XML audit file.
- Download a generated XML (`apps.api.n18_audit.download` route).
- Delete a generated XML from CloudCart's storage (`apps.api.n18_audit.delete` route).
- Backfill any past month — generate one period at a time (no "earliest period" restriction).

### What the merchant CANNOT do here
- Auto-submit to NAP — submission to the NAP portal is always manual.
- Generate a period in real time — generation is queued and may take minutes (longer under load).
- Generate by day or week — the picker accepts whole months only.

## Settings & fields

App key: `n18_audit`. Only ONE setting is required when activating:

- `uin` — the NAP-assigned unique e-shop number (required when `active = 1`).

Optional:
- `domain` — defaults to the store's primary host URL (used in the XML's `domain_name` field).
- `payment_two` / `payment_four` — map CloudCart payment providers to NAP payment-service-provider identifier types (`n18_type` of 2 or 4 on the payment-provider configuration).
- `terminalId` — POS terminal ID mapping (for type-2 payment providers).

Audit data is per `site_id`: each store has its own UIN and its own list of generated XML files, managed separately.

## Business rules

### What enters the report — orders, by their status history

The audit file is generated from the store's **orders**, selected by their **order-status history** (not from invoices). Each period's file has two kinds of rows:

- **Sales** (`<order>`) — every order that reached status **`paid`**, **`completed`**, or **`fulfilled`** during the month (by the date that status was set).
- **Reversals** (`<rorder>`) — orders that had **already been sold** (previously reached paid / completed / fulfilled) and then moved to a reversing status — **`voided`**, **`timeouted`**, **`cancelled`**, **`failed`**, **`refunded`**, **`chargebacked`**, **`disputed`**, or **`not_fulfilled`** — during the month, and were **not** re-sold afterwards.
- **Partial returns** are read separately from the order's return records (by the return date), because a partial return does not change the order status and would otherwise be invisible; each appears as a reversal row.

**Each order is reported once.** When an order is included in a month's file it is marked internally (an `n18` = `YYYY-MM` stamp) so it can't also be pulled into a different month's report.

### The document number comes from invoicing — invoicing should have been active for the period

Each sale must carry the **document number** Наредба Н-18 requires (чл. 52о) — the **cash-receipt number** (касова бележка), or the **invoice number** when only an invoice was issued. CloudCart takes that number from the store's **invoicing** (receipts / invoices):

- **Orders are selected by their status regardless of invoicing** — a sale is picked up even without invoicing.
- **But its document number is filled only from active invoicing.** If invoicing (receipts / invoices) was **not** active during a past period, those sales appear with an **empty document number**, which makes the file non-compliant. So in practice invoicing must have been active during any period you report — see [[settings-invoicing]].

### Which reporting month an order lands in — by status-change date

An order is attributed to the month in which its **status changed**, not the month it was placed:

- A **sale** lands in the month its order reached **`paid` / `completed` / `fulfilled`**.
- A **reversal** lands in the month its order moved to a reversing status; a **partial return** lands in the month it was returned.

| Scenario | Reported in | As |
|---|---|---|
| Ordered in April, reached `paid` / `completed` / `fulfilled` in April | April | `<order>` (sale) |
| Ordered in April, reached `paid` / `completed` / `fulfilled` only in May | **May** | `<order>` (sale) |
| Sold in May, refunded / cancelled in June | **June** | `<rorder>` (reversal) |
| Sold in May, a **partial** return processed in June | **June** | `<rorder>` (partial return) |

A sale and its later reversal therefore commonly fall in **different monthly files** — the sale in the month it was paid, the reversal in the month it was refunded / returned.

### How sales appear — currency, amounts and payment type

- **Currency.** Amounts are reported in **BGN for order dates before January 2026** and in **EUR from January 2026 onward** (matching Bulgaria's euro adoption — see [[apps-bgn2eur]]). An order in the other currency is converted at the fixed **1.95583** rate.
- **Amounts per sale**: goods value **without VAT**, **discount**, **VAT**, and **total with VAT**; each line item carries its name (trimmed to ~200 characters), quantity, unit price and VAT rate. Reversals are written as **negative** amounts and summed into `<r_total>` (a negative total).
- **Payment type.** Each sale's payment maps to a NAP payment-type code, configured **per payment provider** (the `n18_type` mapping set from the app's payment settings — see [[apps-n18-audit-settings]]). **Cash-on-delivery (наложен платеж) has its own codes** — COD collected through a postal-money-order courier is reported under a different code from other COD, and COD is **not** merged into "bank transfer". This matters because the alternative regime this file serves is specifically about дистанционни / COD payments.

### Regenerating a period creates a new file

Each generation of a month produces a **new, separate file** (its name carries the generation timestamp) — it does **not** overwrite the previous one. If the merchant regenerates a month, **both** files exist; the merchant downloads the correct one and deletes the obsolete file manually. (Starting a new generation for a period cancels any generation of that period still in progress.)

### Monthly XML export, not real-time

There is no per-transaction NAP reporting. Each reporting month is exported as one XML file covering that month's sales and reversals. Submission deadline: the 1st–15th of the following month, via the NAP portal (по електронен път).

### Bulgarian-specific

Only relevant for Bulgarian-operating merchants. Other countries have their own regulations (e.g., Romania's e-Factura via [[apps-smart-bill]], Hungary's Online Számla via [[apps-szamlazz]]).

### Combined with invoicing apps

The merchant typically runs N18 Audit + a separate invoicing app ([[apps-fgo]]) — N18 produces the monthly NAP audit file, FGO handles formal invoice numbering. Both are required for compliance.

### B2B-only stores

The Annex 38 regime applies to merchants using the alternative regime for absentee payments. A Bulgarian B2B-only merchant operating under a different regime (e.g., only formal invoices, no B2C cash-equivalent flows) should confirm with their accountant whether Annex 38 applies. The integration is opt-in — the merchant decides whether to install based on their NAP regime.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-n18-audit-settings]] — settings sub-page.
- [[apps-fgo]] — Bulgarian invoicing (sister compliance integration).
- [[settings-invoicing]] — invoicing provider configuration.
- [[orders]] — orders that generate fiscal receipts.
- [[apps-szamlazz]] — Hungarian counterpart with similar NAV reporting.
- [[online-sales-without-cash-register]] — the Наредба Н-18 regime where the courier issues the fiscal receipt for COD online orders (no merchant cash register).
- **Regulation source** — Наредба № Н-18/2006, Глава седма "г" "Алтернативен режим" (consolidated, лекс.бг): https://lex.bg/laws/ldoc/2135540645
- **NRA portal page** — *Алтернативен режим за регистриране и отчитане на продажбите*: https://nra.bg/wps/portal/nra/fiskalni-ustroystva-supto-i-e-magazini/page.turgovia-v-internet-i-e-magazini/page.lternativen-rejim-za-registrirane-i-otchitane-na-prodajbite
- **Focused legal text** — [`wiki/resources/naredba-n18-alt-rezhim.txt`](../resources/naredba-n18-alt-rezhim.txt) (Чл. 52о–52у + Приложения 33 и 38, ~33 KB, grep-friendly).
- **XML schema + sample** — [`wiki/resources/dec_audit.xsd`](../resources/dec_audit.xsd) (original Windows-1251), [`dec_audit.utf8.xsd`](../resources/dec_audit.utf8.xsd) (UTF-8 copy), [`dec_audit-sample.xml`](../resources/dec_audit-sample.xml) (sample audit file), and [`dec_audit-schema-cheatsheet.md`](../resources/dec_audit-schema-cheatsheet.md) (per-element field reference).

## How it works (verified against backend)

### Generate-and-download flow

1. The merchant picks a reporting month (e.g., `2026-04`) via the **Add new period** modal and saves.
2. CloudCart queues a background task that gathers all paid + refunded orders for that month and emits the Annex 38 XML (`dec_audit.xsd` schema, Windows-1251 encoding).
3. The file is stored in CloudCart; the merchant is notified by in-app alert (`"A task to generate an XML file has started. When task done, you'll be notified."`).
4. The merchant downloads the XML from the list view and uploads it to the NAP portal manually.

The list view shows one entry per period, each with `period`, `name` (e.g., "N18 Audit 2026-04 - 2026-05-22 14:23:11.xml"), `size`, `created_at`, `downloadUrl`.

### "Add new period" modal (single-month picker)

A right-side slide-out modal with one month-picker input (`MM-YYYY`) and a static notice that the XML cannot be generated in real-time and may take "several hours under load." Buttons: **Cancel** (closes), **Save** (POSTs `period` to `/admin/api/n18_audit/create`). On the API response:
- `status === 'error'` shows the returned `msg` as a toast and keeps the modal open.
- Success shows a confirmation toast and closes the modal.
- Validation errors on `period` render under the picker (e.g., missing or wrongly formatted month).

Each save creates one period entry. To backfill, the merchant repeats the flow per month. The N18 Audit **install** date does not matter — the file is built from **orders whose status changed in that month**, so a past period still has its sales / reversals. The only invoicing caveat is that each sale's **document number** is drawn from invoicing, so invoicing should have been active back then for a fully compliant file (see "The document number comes from invoicing" under Business rules).

### Regulatory context: Annex 38 of Ordinance H-18/2006

This is for merchants applying the **alternative regime for absentee payments** under Наредба № Н-18/2006. The CloudCart app implements the file-submission obligation in **Чл. 52т, ал. 2**. The full consolidated ordinance text lives on lex.bg at `https://lex.bg/laws/ldoc/2135540645`; only the alternative-regime section is relevant — articles **Чл. 52о – 52у** (Глава седма "г"), **Приложение № 33** (e-shop registration form that issues the UIN), and **Приложение № 38** (the XML audit-file schema).

A focused extract is checked into `wiki/resources/naredba-n18-alt-rezhim.txt` (UTF-8, ~33 KB, 711 lines). Grep markers:
- Articles → `^Чл\. <N>\.` (covers `Чл. 52о` to `Чл. 52у`)
- Annex 33 → `^Приложение № 33`
- Annex 38 → `^Приложение № 38`

The XML schema the app emits lives at [`wiki/resources/dec_audit.xsd`](../resources/dec_audit.xsd) (Windows-1251 original) + [`dec_audit.utf8.xsd`](../resources/dec_audit.utf8.xsd) (UTF-8 copy), with a minimal example at [`dec_audit-sample.xml`](../resources/dec_audit-sample.xml) / [`dec_audit-sample.utf8.xml`](../resources/dec_audit-sample.utf8.xml). For an element-by-element field reference with Bulgarian documentation strings and value enumerations (paym codes, r_paym codes, e_shop_type), see [`dec_audit-schema-cheatsheet.md`](../resources/dec_audit-schema-cheatsheet.md).

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
