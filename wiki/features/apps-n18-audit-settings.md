---
type: feature
nav_path: "Apps → N18 Audit → Settings"
route_name: apps.n18_audit.settings
route_path: /admin/apps/n18_audit/settings
aliases: ["N18 Audit Settings", "Naredba N-18 settings", "NAP fiscal config"]
tags: [apps, administration, n18-audit, fiscal, compliance, bulgaria, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-11-09
source_count: 3
---
# N18 Audit → Settings

## Purpose

The **Settings** tab is where the merchant configures their **N-18 Annex 38 (Bulgarian monthly audit XML)** integration — enters the NAP-assigned UIN (unique e-shop number), configures the store domain that appears in the XML, and maps payment providers to NAP payment-service-provider identifier types. See [[apps-n18-audit]] for the full feature set.

This integration generates monthly XML files for manual submission to NAP — it does NOT do real-time reporting.

## Where to find it

Sidebar → Apps → N18 Audit → **Settings tab**. Route: `/admin/apps/n18_audit/settings`.

## What the merchant can do here

The **Settings** tab has two boxes (English labels as in the admin's code; the Bulgarian ones come from the admin's translations and are not quoted here):

| Box / field | What it does |
|---|---|
| **N18 audit settings** → **Internet address of the store according to what you submitted to the NRA** | The `domain_name` of the file. Defaults to the store's primary address. |
| **N18 audit settings** → **UIN** | The NAP-issued e-shop number (`e_shop_n`). Required. |
| **N18 audit settings** → **How to return the amount** | **By bank** / **By credit/debit card** / **Cash** / **Other**: the `r_paym` written on every reversal. |
| **Terminal ID** | One field per active payment provider whose NAP type (`n18_type`) is 2 or 4, labelled with the provider's name. A type-2 provider whose own settings hold a terminal ID shows it pre-filled and locked. The value feeds `pos_n` and `proc_id` (see below). |

### What the merchant CANNOT do here
- Choose a payment provider's NAP payment type: `n18_type` is set by CloudCart on each provider and is not editable.
- Submit the file to NAP, or report in real time: the app only builds monthly XML files.
- Get the file in another format: it is XML only (Windows-1251), with no PDF or table view.

## Settings & fields

Per [[apps-n18-audit]]: app key is `n18_audit`.

## Business rules

### Who can open the files

Anyone with the admin's **apps** permission can open the app, its settings and its file list, so an accountant can be given a staff account with that permission ([[settings-staff]]); otherwise the merchant downloads the XML and passes it on.

### Through the Admin GraphQL API

An agent can list, download, create and delete audit files (`n18AuditFiles`, `n18AuditFileDownload`, `createN18AuditFile`, `deleteN18AuditFile`). The settings cannot be read there: the shared app-settings query answers *"Administration app not found: n18_audit"*. The UIN, the return method and the Terminal ID values are seen only on this tab.

### No fiscal-device settings

There are no fiscal-device, operator or real-time reporting fields. Each sale's document number comes from the store's invoicing — see [[apps-n18-audit]].

### Where `pos_n`, `trans_n` and `proc_id` come from

- **`pos_n`** (every sale except a wallet-only one): the terminal ID the gateway returned with the payment, if any, otherwise the provider's **Terminal ID** box.
- **`trans_n`**: CloudCart's own payment number, not the gateway's transaction ID.
- **`proc_id`**: an older separate type-4 value when one is stored, otherwise the same **Terminal ID** box, so a type-4 provider normally gets the same value in `pos_n` and `proc_id`. That is how the code works, not a fault of one store.
- Which `n18_type` each provider has (myPOS, CloudCart Pay, Stripe, Borica Way4, Paypercut, …) is held on CloudCart's provider records, not in the code (verify with CloudCart).

## Related

- [[apps-n18-audit]] — hub.
- [[apps-fgo]] — Bulgarian invoicing (sister compliance integration).
- [[apps-szamlazz]] — Hungarian counterpart (Online Számla).
- [[apps-smart-bill]] — Romanian counterpart (e-Factura).
- [[orders]] — orders that trigger reporting.
- **Regulation source** — Наредба № Н-18/2006, Глава седма "г" "Алтернативен режим" (consolidated, лекс.бг): https://lex.bg/laws/ldoc/2135540645
- **NRA portal page** — *Алтернативен режим за регистриране и отчитане на продажбите*: https://nra.bg/wps/portal/nra/fiskalni-ustroystva-supto-i-e-magazini/page.turgovia-v-internet-i-e-magazini/page.lternativen-rejim-za-registrirane-i-otchitane-na-prodajbite
- **Focused legal text** — [`wiki/resources/naredba-n18-alt-rezhim.txt`](../resources/naredba-n18-alt-rezhim.txt) (Чл. 52о–52у + Приложения 33 и 38, grep-friendly); grep `^Чл\. 52т\.` for the file-submission obligation, `^Приложение № 38` for the audit-file schema description, `^Приложение № 33` for the e-shop registration form.
- **XML schema + sample** — [`wiki/resources/dec_audit.xsd`](../resources/dec_audit.xsd), [`dec_audit.utf8.xsd`](../resources/dec_audit.utf8.xsd), [`dec_audit-sample.xml`](../resources/dec_audit-sample.xml), [`dec_audit-schema-cheatsheet.md`](../resources/dec_audit-schema-cheatsheet.md).

## How it works (verified against backend)

### Actual required setting: UIN only

ONLY `uin` is required (and only when `active = 1`). Everything else is optional:
- `uin` — NAP-assigned unique e-shop number (required).
- `domain` — defaults to the store's primary host URL. Placeholder hints `https://example.com`.
- `return_pay_type` — dropdown: how to return the amount (1 = By bank / 2 = By credit/debit card / 3 = Cash / 4 = Other). Selected value goes into the refund entries of the generated XML.
- `payment` (with the older `payment_two` / `payment_four`) — the **Terminal ID** values per provider; see the table above.
- **Where the payment type comes from.** A provider's `n18_type` (the NAP payment-type code its sales get in the XML) is part of CloudCart's catalogue entry for that provider, set when CloudCart adds the provider. No screen, here or in the provider's settings, changes it; for these providers the merchant only fills the Terminal ID box. The value for a given provider, e.g. CloudCart Pay, is not in the code (verify with CloudCart).

### Two-tab UI: Settings + List

The N18 Audit Settings view extends the standard app-settings layout with one extra tab — **List** — pointing at the generated-XML list (route `apps.n18_audit.list`). Save behaviour: after the merchant saves the Settings form, the platform pushes them straight to the List tab. The active-switch is hidden (`:show-active-button="false"`) — activation happens implicitly when `uin` is set and the merchant saves.

### Adaptive Terminal-ID box layout

With 3 or fewer providers the Terminal ID box opens as an inline slide panel; with 4 or more, as a separate full-width panel.

### NAP registration is prerequisite, not in-app

The merchant must register their e-shop with NAP via Annex 33 BEFORE installing this app. NAP issues the UIN — there's no in-app NAP registration workflow. For CloudCart Pay, the payment details Annex 33 asks for (provider, Merchant ID, virtual POS ID, receiving account) are on the **NRA declaration information** card ([[ccpay-onboarding-nra-declaration]]); for another provider they come from that provider.

### No sandbox / test mode

There is no test mode. Generating a file submits nothing to NAP (the merchant uploads it), so files for past periods can be generated freely to check them.

### Historical backfill IS supported

The merchant can generate XML for any past month after installing — see [[apps-n18-audit]]. There's no time-of-installation restriction.

### B2B-only stores

Annex 38 of Ordinance H-18/2006 applies to merchants using the **alternative regime for absentee payments**. Whether a B2B-only merchant falls under this regime depends on their NAP registration. Merchants should consult their accountant — installing the app is optional based on the merchant's regulatory status.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
