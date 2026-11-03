---
type: feature
nav_path: "Customers → Import → Wizard UI"
route_name: admin.complete.import
route_path: /admin/import/complete-import/customers
aliases: ["Import customers wizard", "Customer import wizard", "Import customers modal", "Import customers Step 1", "Import customers Step 2", "Import customers success card", "Track importing progress"]
tags: [customers, import, csv, wizard, ui]
plan_gates: ["customer_import"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers-import]]. See the hub for related aspects (fields, concurrency, processing, side effects, plan gates, API alternative).

# Import customers — wizard UI (3 steps + success card)

## Purpose

This page covers the merchant-facing wizard for the customer CSV import: the 2FA gate, the two visible numbered steps (Upload + Map fields), and the success card that replaces the wizard content after Submit.

The wizard header (`StepsHeader.vue`) only renders **two** numbered step indicators (STEP 1 + STEP 2). After Submit on STEP 2, the modal body switches to the success card and the wizard buttons (Back / Next / Submit) are hidden because `step === 3` is outside the `step < 3` template guard. The merchant either clicks the **Track importing progress** link or closes the modal with the X.

## Where to find it

Sidebar → **Customers** → click **Import** in the page header (top-right, next to **Export customers** and **+ Add customer**). The modal is launched in-place — no route navigation.

## What the merchant can do here

### Step 0: 2FA authorisation

- Click the **Import** button in the Customers list header.
- A **Two-factor authentication** modal opens (the `CC2FaAction` component with `action="import_customers"`) with the standard authenticator-app or email code prompt (see [[account-cc2fa]], [[account-cc2fa-email]]).
- On valid code, the wizard modal opens and the 2FA hash is passed as a `v-model:hash` prop to scope subsequent API calls to this verified session.

Full 2FA + permission mechanics live on [[customers-import-plan-gates]].

### STEP 1: Upload file

The modal opens with the header *"Import with CSV file"*, a close-X (disabled while submitting), and a primary **Next** button (right). The body shows two stacked cards:

**Card 1: Upload CSV file**

| Element | Notes |
|---------|-------|
| Card title | *"Upload CSV file"* + subtitle *"Add your file with import data"*. |
| **CSV Template** button (right of card title) | Downloads `customer-template.csv` from `{img_url}sitecp/docs/customer-template.csv` — disabled during submit. Column layout on [[customers-import-fields]]. |
| **Dropzone** (renders when no file selected) | Big dashed-border drop area with cloud-up icon, label *"Click or Drop here to upload"*, and an inline **Upload CSV file** button that triggers a hidden `<input type="file" accept=".csv">`. UI-level validation **rejects everything except `.csv`** — error *"Invalid file type, please upload a valid csv file."* (the backend still accepts `.txt` if posted directly, but the UI dropzone blocks it). Drag-over highlights the dropzone purple. |
| **Selected-file row** (renders after file pick) | File icon + filename + a red trash icon. Clicking the trash opens a confirmation popover *"Remove uploaded file?"* with **Remove** / Cancel buttons. Removing un-selects the file and re-shows the dropzone. |

**Card 2: CSV file settings**

| Field | v-model | Type | Default | What it controls |
|-------|---------|------|---------|------------------|
| **Header line toggle** | `config.has_header_line` | ActiveSwitch | OFF | When ON, the platform treats the first CSV row as a header (column titles) and ignores it during import. Label: *"Check this if your file has a header line explaining the columns"*. |
| **Customer group** | `config.customer_group_id` | SelectWithAjax (searchable, request-on-open) | (empty — Default group used server-side fallback) | Populated from `GET /admin/api/core/customers/groups`. All imported customers are assigned to this group unless their row provides a per-row group name. |

**Next-button behaviour**: clicking **Next** on STEP 1 first POSTs the file + settings to `save/customers/import_customers/{hash}` (form-data: `import_file`, `has_header_line`, `customer_group_id`). On success the response carries an `id` (the temp-import id) — the wizard advances to STEP 2. If the merchant hasn't picked a file, the inline error *"Please upload a CSV file"* shows instead of submitting.

### STEP 2: Map fields

After the upload succeeds, the wizard fetches the columns + mapping options via `GET /admin/api/core/customers/csv/mapping/{importId}` and renders one **SettingsCard** per field group. For the customer import there is a single card titled per the field-group enum.

Inside the card each customer field is rendered as a **SelectWithAjax** dropdown. The full customer-field list + required-field rules + map-options derivation live on [[customers-import-fields]].

**Buttons**: header shows **Back** (returns to STEP 1, file + settings preserved) + **Submit** (commits the mapping).

**Submit behaviour**: POSTs `import_binds` (the `{customer_field: csv_column_index}` pairs) to `mapping/{importId}/{hash}`. On HTTP 400 with `response.data.message`, the modal shows the error inline at the bottom of the modal (red banner with exclamation icon). On HTTP 409 from a stuck running import, see [[customers-import-concurrency]]. On other errors the global `$errorResponse` handler runs. On success → wizard advances to STEP 3 (the success card).

### STEP 3: Import task created (success card)

A green check-mark SVG + heading *"Import task created"* + paragraph *"The file was successfully uploaded and the customers import task was added to the queue. If you wish, you could track the uploading in the queued jobs."* + a **Track importing progress** primary button.

- The Track-progress button is a `router-link` to `{name: 'apps.csv_import.settings', params: {type: 'customers'}}` — opens the CSV-import settings/history page in a NEW tab AND closes the modal on click.
- The wizard header no longer renders the Back / Next buttons at step 3 (template guard `v-if="step < 3"` hides them).
- The merchant can simply close the modal with the X — the import job is already queued and will run regardless. The job processes asynchronously per [[customers-import-processing]].

## Settings & fields

The Step 1 / Step 2 field map + validation strings live on [[customers-import-fields]] (kept centralised so the UI walkthrough doesn't duplicate the field reference).

## Business rules

- **Modal-only — no dedicated route.** Closing the X at any stage does NOT cancel a queued job (jobs queued at Step 2 Submit run regardless).
- **Back from STEP 2 preserves Step 1 state** (the file and the `has_header_line` / `customer_group_id` settings are kept in component state, NOT re-uploaded).
- **The 2FA hash threads through every API call.** If the 2FA session expires mid-wizard, subsequent calls return 401 and the wizard surfaces the error inline.
- **Session storage.** Step 1 settings (`has_header_line`, `customer_group_id`, mapped binds) are stored under the session key `customers_csv_import_settings`. Restarting Step 1 overwrites the stored config; the merchant doesn't need to clean session state manually.

## Related

- [[customers-import]] — hub.
- [[customers-import-fields]] — the field map + validation rules surfaced in the wizard.
- [[customers-import-concurrency]] — the 409 the wizard surfaces if another import is running.
- [[customers-import-processing]] — what happens after Submit (background batch pipeline).
- [[customers-import-plan-gates]] — the 2FA + plan-feature gates upstream of Step 0.
- [[customers]] — the parent list page that hosts the **Import** button.
- [[account-cc2fa]] / [[account-cc2fa-email]] — 2FA setup required.
- [[settings-queue-view]] — the page opened by **Track importing progress**.

## Open questions

(All resolved.)
