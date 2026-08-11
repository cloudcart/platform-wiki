---
type: feature
nav_path: "Customers → Import"
route_name: admin.complete.import
route_path: /admin/import/complete-import/customers
aliases: ["Import customers", "Customer import", "CSV import", "Bulk add customers", "Импорт на клиенти", "Импортиране на клиенти", "Качване на клиенти от файл"]
tags: [customers, import, csv, 2fa, plan-gated, bulk]
plan_gates: ["customer_import", "customers"]
created: 2026-05-23
updated: 2026-06-10
source_count: 11
---

# Import customers

## Purpose

**Import customers** lets the merchant bulk-add (or update-by-email) customers from a CSV file via a side-panel modal launched from the **Customers list** ([[customers]]) header. The wizard has **2 visible numbered steps + a success card**:

1. **STEP 1** — Upload file + pick header-line toggle + pick a default customer group.
2. **STEP 2** — Map each CSV column to a customer field (email is required).
3. *(no third step label — a "Import task created" success card replaces the wizard content after STEP 2 submits.)*

The import is **gated by two-factor authentication** (admin must enter a 2FA code before the upload panel opens), **gated by plan feature** (`customer_import`), and runs as a background job on the `import6` queue — it does NOT block the merchant's session.

This page is the hub for the seven aspect pages below. Drill into the aspect that matches the question — do NOT read every page.

## Where to find it

Sidebar → **Customers** → click **Import** in the page header (top-right, next to **Export customers** and **+ Add customer**).

The action is exposed through the Customer hub's header — it is NOT a dedicated route. The permission id is `customers.import` (under the `customers.all` permission group).

## Sub-pages (in this cluster)

- [[customers-import-wizard]] — the 3-step wizard UI in full: 2FA gate, Step 1 upload card + CSV-template button, Step 2 mapping dropdowns, Step 3 success card and the Track-progress link.
- [[customers-import-fields]] — the customer field map (`customer.first_name` / `customer.last_name` / `customer.full_name` / `customer.email` / `customer.note` / `customer.marketing` / `group.name`), required fields, validation messages, the CSV-template column layout, and why **address fields are intentionally disabled**.
- [[customers-import-concurrency]] — the cross-import-type lock (one running import per store across customers / products / redirects / blog / subscribers), the **409** retry path, the 3-trigger self-healing for stuck imports (30-minute progress staleness, etc.), and the cancel endpoint.
- [[customers-import-processing]] — the background-job pipeline: batches of 500, ERP import buffer in chunks of 50, temp-table `csv_import_<unix-timestamp>`, email-dedup logic, group auto-creation, `csv_tasks` tracking record, per-task progress doc + failed-records sample.
- [[customers-import-side-effects]] — what happens to imported customer records: `customer.created` / `customer.updated` webhooks per row, `imported = yes` flag (NOT a per-import tag — contrasts with product imports), password-email behaviour, and the existing-customer update-on-email-match rule.
- [[customers-import-plan-gates]] — the `customer_import` access gate + the `customers` numeric cap (over-cap rows silently rejected mid-import), the `customers` / `customers.all` / `customers.import` permission grants, and the 2FA requirement.
- [[customers-import-api-alternative]] — when to use JSON-API v2 ([[api-customers]]) instead, why there is no bulk-import endpoint in the API, and same-side-effects-per-call semantics.

## What the merchant can do here

The full UI walkthrough — Step 0 (2FA) → Step 1 (upload) → Step 2 (map fields) → Step 3 (success card) — lives on [[customers-import-wizard]].

**What the merchant CANNOT do** (verified — see siblings for detail):

- Map address fields — disabled pending the multi-address-per-customer model migration; see [[customers-import-fields]].
- Set passwords for imported customers — the platform generates passwords automatically; see [[customers-import-side-effects]].
- Preview a dry-run before committing — no preview step; the job runs immediately on Submit.
- Upload multiple files at once — one CSV per import.
- Roll back an import — once the job runs, there is no undo; manually delete imported customers from [[customers]].
- Run more than one import at a time — the cross-import lock blocks new uploads; see [[customers-import-concurrency]].

## Settings & fields

The full field map + validation strings live on [[customers-import-fields]]. Top-level summary:

| Step | Field | Verbatim key | Required? |
|------|-------|--------------|-----------|
| 1 | Has header line | `has_header_line` | YES (`0`/`1`) |
| 1 | Customer group | `customer_group_id` | YES (falls back to **Default** group server-side) |
| 1 | Upload file | `import_file` | YES (`.csv` or `.txt`) |
| 2 | Email mapping | `customer.email` | YES (only required customer-field mapping) |
| 2 | Mapping format | `import_binds` array of `{customer_field: csv_column_index}` | — |

## Business rules

The hub captures the cross-cutting rules; the deep dive lives on the siblings:

- **2FA gate runs before Step 1** — see [[customers-import-plan-gates]].
- **Plan feature `customer_import` gates the action** — see [[customers-import-plan-gates]].
- **Concurrent-import lock + self-healing for stuck imports + cancel endpoint** — see [[customers-import-concurrency]].
- **Email uniqueness — silent dedup (in-CSV + email-match update)** — see [[customers-import-processing]].
- **Group auto-creation on per-row `group.name`** — see [[customers-import-processing]].
- **Background batch pipeline + temp-table mechanics** — see [[customers-import-processing]].
- **`app_import` tag is products-only — NOT customers** — see [[customers-import-side-effects]].
- **Webhooks + side effects per imported row** — see [[customers-import-side-effects]].

### File constraints (cross-aspect — summary)

- Format: CSV (comma-separated) OR `.txt`. Other delimiters auto-detected: comma `,`, semicolon `;`, tab `\t`, pipe `|`, colon `:` (Bulgarian semicolon-Excel exports work out of the box).
- Line endings: detected from `\r\n`, `\n\r`, `\n`, `\r`.
- Encoding: UTF-8. Non-UTF-8 files (Windows-1251, Latin-1) may show garbled characters.
- Maximum rows: NOT enforced in the customer-import path. Practical ceiling = the temp table holding the entire CSV before processing.
- Column count: variable per file; rows shorter than the detected count are padded with `null`, longer rows are truncated.

Full processing details live on [[customers-import-processing]].

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]) — full mechanics on [[customers-import-plan-gates]]:

- `customer_import` — Access gate (URL-level). Plans without the feature see the Import button trigger a paid-feature upgrade modal (after the 2FA gate, before Step 1).
- `customers` — Numeric (max customer records). Over-cap rows are silently rejected at insert time mid-import; the job does NOT pre-validate against the cap.

## Related

- [[customers]] — the parent list page that hosts the **Import** button in its header.
- [[customers-export]] — the inverse operation (download customer list as CSV).
- [[customers-custom-fields]] — defined custom fields are NOT importable via the standard customer CSV — only built-in customer fields plus group name.
- [[customers-custom-groups]] — where the merchant manages the groups the import assigns customers to (auto-created groups appear here).
- [[account-cc2fa]] / [[account-cc2fa-email]] — 2FA setup required before the import can run.
- [[settings-queue-view]] — track import-job progress and view past imports.
- [[settings-import-history]] — historical record of import runs (chronology).
- [[settings-hooks]] — `customer.created` / `customer.updated` webhooks fire for each row imported.
- [[settings-cart]] — "Convert guests into members" affects whether imported customers receive password emails.
- [[settings-staff]] — moderator permission grants for the import.
- [[plan-gates]] — `customer_import` is a plan-gated feature.
- [[background-queue-inventory]] — catalogue of all background processes; covers the async customer-CSV import job timing and how to spot a stuck import.
- [[api-customers]] — JSON-API v2 one-at-a-time create; see [[customers-import-api-alternative]].
- [[json-api-v2]] — auth, rate limit, side-effects principle.

## Open questions

(All resolved.)
