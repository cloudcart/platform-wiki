---
type: feature
nav_path: "Apps → MicroBG → Troubleshooting"
route_name: apps.microbg.overview
route_path: /admin/apps/microbg/overview
aliases: ["MicroBG troubleshooting", "MicroBG support playbook", "MicroBG common errors", "MicroBG 503 errors", "Невалиден ЕИК", "ЕИК вече е регистриран", "MicroBG test environment"]
tags: [apps, erp, bulgaria, troubleshooting, support, errors]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-microbg]]. See the hub for the other aspects (architecture split, registration, prerequisites, sync mechanics, partner matching).

# MicroBG — troubleshooting + common support questions

## Purpose

This aspect collects the recurring MicroBG support patterns: the "stock differs", "orders aren't appearing", "customer EIK isn't being passed" complaints and the diagnostic step that resolves each. It also documents the Micro.bg-side error messages that bubble up as HTTP 503 from CloudCart's Settings tab, plus the test environment that exists in code but is unreachable from the merchant UI.

## Where to find it

Troubleshooting cuts across both sides:

- **CloudCart admin** → Apps → MicroBG → Settings (handshake errors).
- **CloudCart admin** → [[settings-hooks]] (webhook subscription health).
- **CloudCart admin** → [[settings-api-keys]] (API key validity).
- **CloudCart admin** → [[orders-history]] (ERP-sync events appear here).
- **Micro.bg admin** → CloudCart Control Panel → **Проверка съответствие на стоките** (product matching diagnostics) + auto-sync checkbox + webhook activation status.

## What the merchant can do here

The common support diagnostics the merchant can run themselves:

- Rerun **Проверка съответствие на стоките** in Micro.bg's Control Panel to surface mismatched codes.
- Toggle the auto-sync checkbox off → on to re-prime the 3-minute scheduler.
- Rerun **Активиране на известията** to re-subscribe the order webhooks.
- Check [[orders-history]] for `send_erp_success` / `send_erp_error` action strings on individual orders.
- Verify [[settings-api-keys]] hasn't had the first key deleted or rotated.

### What the merchant CANNOT do here

- View Micro.bg's internal logs from CloudCart's side. Diagnostics for "Micro.bg said X but didn't show Y" need access to Micro.bg's own logs.
- Route a specific merchant's handshake through the Micro.bg test environment. The test URL exists in code but isn't exposed in the UI.
- Manually retry a failed webhook delivery from CloudCart. [[settings-hooks]] handles retry, but the merchant can't kick off a per-order replay for Micro.bg specifically.

## Settings & fields

There are no troubleshooting-specific fields. The data points support reads are:

- **Settings tab Info card** — `PaymentToDate` (subscription valid?), `OrderId` (handshake completed?), `domain` (Micro.bg provisioned?), API key (still present?).
- **Order history entries** — `send_erp_success` and `send_erp_error` action strings record per-order ERP push outcomes.
- **HTTP response from the handshake POST** — the body's first error message when status is 503.

## Business rules

### Common support questions + answers

| Merchant complaint | Where to look first |
|---|---|
| *"Stock count differs between CloudCart and Micro.bg"* | Micro.bg Control Panel → **Проверка съответствие на стоките**. Look for code mismatches first. See [[apps-microbg-sync-mechanics]] for the matching rules. |
| *"New orders aren't appearing in Micro.bg"* | [[settings-hooks]] → check Micro.bg's `order.*` webhook subscriptions are active + the receiver is responding 2xx. Run **Активиране на известията** again if missing. |
| *"Customer EIK isn't being passed to Micro.bg"* | [[settings-cart]] → "Bulstat/EIK or EGN" — must be **Опционално**, not Hidden. See [[apps-microbg-partner-matching]]. |
| *"3-min sync didn't run"* | Sync is owned by Micro.bg's side; check Micro.bg's login + Control Panel auto-sync checkbox. Verify the API key in [[settings-api-keys]] is intact. |
| *"Payment method missing on the Micro.bg side"* | Add the matching `Тип на плащане` in Micro.bg via За фирмата → Типове плащания → Нов тип плащане. See [[apps-microbg-prerequisites]]. |
| *"Discount / fee / shipping line missing from operation in Micro.bg"* | Verify the service product exists in Micro.bg's Номенклатури → Стоки (Доставка, Отстъпка, Такса). See [[apps-microbg-prerequisites]]. |
| *"Two B2B buyers from the same company are split into separate Micro.bg partners"* | The orders were placed without EIK in the billing address (cascade fell through to email-based dedup). See [[apps-microbg-partner-matching]]. |
| *"Handshake fails with 'Невалиден ЕИК'"* | The merchant typed an EIK that doesn't pass Micro.bg's checksum. Verify against the Bulgarian Trade Registry. |
| *"Handshake fails with 'ЕИК вече е регистриран'"* | The merchant already has a Micro.bg account. They should pick *Existing user* instead of *New registration*. See [[apps-microbg-registration]]. |

### Error response handling

If Micro.bg's `Check` or `Create` endpoint fails, the controller surfaces the first upstream error message to the merchant as HTTP 503. Common merchant-facing errors:

- *"Невалиден ЕИК"* — the EIK doesn't pass Micro.bg's checksum.
- *"ЕИК вече е регистриран"* — the merchant already has a Micro.bg account; they should pick *Existing user* instead of *New registration*.
- *"Липсва задължително поле"* — the merchant skipped a required field; the Settings form should have caught this client-side but didn't.

For 503s without a clear merchant-facing message, support should check Micro.bg's status page first and the merchant's Micro.bg login second.

### Order history entries

When Micro.bg posts back order-status updates (after a Поръчка transforms to Продажба, for example), those acknowledgements appear in [[orders-history]] under the `send_erp_success` and `send_erp_error` action strings. This is the per-order audit trail support should consult when a specific order didn't make it through. See [[orders-history]] for the full action-string catalogue.

### Test environment is in the code but unused in production

The integration's HTTP client carries two constants — `TEST_URL = https://test.micro.bg/ExtApps/CloudCart/Company/` and `PROD_URL = https://micro.bg/ExtApps/CloudCart/Company/`. The constructor always uses `PROD_URL`; there is no toggle exposed to merchants. A support agent investigating an integration issue cannot route a specific merchant's handshake through the test endpoint without backend access.

## Related

- [[apps-microbg]] — hub.
- [[settings-hooks]] — webhook subscription health + retry behaviour.
- [[settings-api-keys]] — API key the integration depends on.
- [[orders-history]] — `send_erp_success` / `send_erp_error` entries per order.
- [[settings-cart]] — EIK field + decrement-status settings whose misconfiguration causes common tickets.
- [[platform-rate-limits]] — the per-receiver webhook delivery cap that can starve a chatty receiver under load.
- [[apps-microbg-partner-matching]] — the EIK / email cascade that explains many "customer missing" tickets.
- [[apps-microbg-prerequisites]] — the configuration checklist most failing installs missed.

## How it works (verified against backend)

The handshake controller surfaces upstream errors via HTTP 503 + the `response.Errors[0]` message string. There is no automatic retry on the CloudCart side — the merchant must fix the input and click Save again. The Micro.bg-side webhook receiver, by contrast, falls back on CloudCart's standard webhook retry logic (see [[settings-hooks]]).

For "stock changed and we didn't change it" tickets where Micro.bg is the cause, the diagnostic anchor is the [[products-change-log|Change log]] on the affected product. Micro.bg writes via the standard JSON-API v2, so its updates appear with the API-key Initiator — see [[inventory-debugging-playbook]] for the 6-step diagnostic that covers this case.

## Open questions

- The exact Micro.bg-side retry behaviour on `5xx` from CloudCart's webhook endpoints. `(verify)`
- Whether Micro.bg surfaces a clear error to the merchant when CloudCart rate-limits the every-3-min push (e.g. against [[platform-rate-limits]] caps). `(verify)`
