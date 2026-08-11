---
type: feature
nav_path: "Apps → N18 Audit → Settings"
route_name: apps.n18_audit.settings
route_path: /admin/apps/n18_audit/settings
aliases: ["N18 Audit Settings", "Naredba N-18 settings", "NAP fiscal config"]
tags: [apps, administration, n18-audit, fiscal, compliance, bulgaria, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 2
---
# N18 Audit → Settings

## Purpose

The **Settings** tab is where the merchant configures their **N-18 Annex 38 (Bulgarian monthly audit XML)** integration — enters the NAP-assigned UIN (unique e-shop number), configures the store domain that appears in the XML, and maps payment providers to NAP payment-service-provider identifier types. See [[apps-n18-audit]] for the full feature set.

This integration generates monthly XML files for manual submission to NAP — it does NOT do real-time reporting.

## Where to find it

Sidebar → Apps → N18 Audit → **Settings tab**. Route: `/admin/apps/n18_audit/settings`.

## What the merchant can do here

### Fiscal device credentials

| Field | Notes |
|---|---|
| **NAP fiscal device ID** | The merchant's registered fiscal device identifier (legal requirement). |
| **Operator credentials** | Authentication for NAP API. |
| **Tax representative ID** | When the merchant has a tax representative (счетоводител), their ID. |

### Reporting configuration

| Setting | Notes |
|---|---|
| **Real-time NAP reporting** | Toggle: report each sale to NAP immediately (recommended). |
| **Batch fallback** | When real-time fails, queue for batch retry. |
| **Receipt QR code** | Include NAP-verifiable QR on customer receipts (Bulgarian legal requirement after specific dates). |
| **Language** | Receipt language (BG / EN). |

### What the merchant CANNOT do here
- Bypass NAP reporting (legal requirement for Bulgarian e-commerce).
- Edit historical NAP reports — immutable audit per Bulgarian tax law.
- Use without N-18 compliance setup (fiscal device registration with NAP).

## Settings & fields

Per [[apps-n18-audit]]: app key is `n18_audit`.

## Business rules

### Bulgarian legal mandatory

For Bulgarian-operating merchants selling B2C goods/services online, N-18 compliance is required by law. Without this app active (or equivalent), the merchant is non-compliant.

### Real-time reporting recommended

NAP requires reporting within minutes of sale. Real-time is the safest setting; batch fallback exists for network resilience.

### Combined with FGO

Most merchants run [[apps-fgo]] + N18 Audit together:
- FGO handles formal invoice numbering.
- N18 Audit handles NAP real-time fiscal reporting.

Both required for full compliance.

### Permission
Standard apps permission scope.

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
- `payment_two` / `payment_four` / `payment` — mapping of CloudCart payment providers to NAP payment-service-provider identifier types (based on each payment provider's `n18_type` value of 2 or 4). The Settings form auto-builds a *Terminal ID* box: one input per active payment provider whose `n18_type` is 2 or 4. If a provider already has a `terminalId` saved, the field is pre-filled and disabled.
- `terminalId` — POS terminal IDs (for type-2 providers, populated from the provider config and not editable here).

There are no "fiscal device credentials" or "operator credentials" in this integration — those belong to a separate fiscal-device hardware/POS system that the merchant uses outside CloudCart.

### Two-tab UI: Settings + List

The N18 Audit Settings view extends the standard app-settings layout with one extra tab — **List** — pointing at the generated-XML list (route `apps.n18_audit.list`). Save behaviour: after the merchant saves the Settings form, the platform pushes them straight to the List tab. The active-switch is hidden (`:show-active-button="false"`) — activation happens implicitly when `uin` is set and the merchant saves.

### Adaptive Terminal-ID box layout

When there are 3 or fewer payment-provider mappings the Terminal-ID box renders as a `slide` panel inline with the main form. With 4+, it switches to a separate `panel` (full-width drawer). This auto-collapse keeps short stores readable and gives high-payment-count merchants room.

### Settings shape vs the previous wiki description

The earlier wording describing "operator credentials", "tax representative ID", "real-time NAP reporting toggle", "batch fallback", and "receipt QR code" does NOT correspond to fields the controller actually accepts. The N18 Audit settings are limited to UIN + domain + payment-provider mapping. The merchant configures fiscal-device + customer receipt behaviour separately (typically in a registered NAP fiscal-device system + their POS / receipt printer setup).

### NAP registration is prerequisite, not in-app

The merchant must register their e-shop with NAP via Annex 33 BEFORE installing this app. NAP issues the UIN — there's no in-app NAP registration workflow.

### No sandbox / test mode

The integration has no `environment` / `test_mode` toggle. The XML file is generated locally and downloaded; the merchant submits it to NAP manually. For testing, the merchant can generate XMLs for past periods without affecting their NAP record (the file submission is the regulatory action, not the XML generation).

### Historical backfill IS supported

The merchant can generate XML for any past month after installing — see [[apps-n18-audit]]. There's no time-of-installation restriction.

### B2B-only stores

Annex 38 of Ordinance H-18/2006 applies to merchants using the **alternative regime for absentee payments**. Whether a B2B-only merchant falls under this regime depends on their NAP registration. Merchants should consult their accountant — installing the app is optional based on the merchant's regulatory status.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
