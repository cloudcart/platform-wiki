---
type: reference
nav_path: "Resources → dec_audit.xsd cheat sheet"
aliases: ["dec_audit cheat sheet", "Annex 38 schema fields", "N18 Audit XML fields"]
tags: [resources, reference, fiscal, bulgaria, n18, schema]
created: 2026-06-08
updated: 2026-06-08
source_count: 1
---
# dec_audit.xsd — field cheat sheet

Extracted from `dec_audit.xsd` (Приложение № 38 към чл. 52т, ал. 2 of Наредба № Н-18/2006). The schema lives in this folder both as the original (`dec_audit.xsd`, Windows-1251) and as a UTF-8 copy (`dec_audit.utf8.xsd`). A sample valid file is in `dec_audit-sample.xml` / `dec_audit-sample.utf8.xml`.

The CloudCart N18 Audit app ([[apps-n18-audit]]) generates a file in this exact schema, one file per reporting month, that the merchant then uploads to the NRA portal under the **Alternative regime for registering and reporting sales** ("Алтернативен режим за регистриране и отчитане на продажбите"): https://nra.bg/wps/portal/nra/fiskalni-ustroystva-supto-i-e-magazini/page.turgovia-v-internet-i-e-magazini/page.lternativen-rejim-za-registrirane-i-otchitane-na-prodajbite

## Root document

The XML file is wrapped in `<audit>` — "Стандартизиран одиторски файл, съдържащ информация за направените в електронния магазин поръчки, по които са извършени доставки на стоки/услуги през календарния месец". Encoding: `windows-1251`.

## Header fields (merchant + period identification)

| Field | Documentation | Constraint |
|---|---|---|
| `eik` | ЕИК на ЗЛ | string, 9–13 chars |
| `e_shop_n` | Уникален номер на електронния магазин (the **UIN** issued by NRA under Annex 33) | string, ≤ 10 chars |
| `domain_name` | Уеб адрес на електронния магазин | string |
| `e_shop_type` | Индикатор за собствен домейн или ползване на онлайн платформа за продажба на стоки / предоставяне на услуги | `1` or `2` |
| `creation_date` | Дата на създаване на файла | date `YYYY-MM-DD` |
| `mon` | Календарен месец, за който се подава информацията | `01`–`12` |
| `god` | Календарна година, за която се подава информацията | YYYY |

## Order body — `<order>` → list of `<orderenum>`

Each fulfilled (paid + delivered) order in the reporting month is a `<orderenum>` element with these fields:

| Field | Documentation |
|---|---|
| `ord_n` | Уникален номер на поръчка в софтуера на е-магазина |
| `ord_d` | Дата на поръчка |
| `doc_n` | Номер на документа по чл. 52о, ал. 1, т. 1 |
| `doc_date` | Дата на документа по чл. 52о, ал. 1, т. 1 |
| `art` | Артикули (wrapper) → list of `<artenum>` |
| `ord_total1` | Обща стойност на доставените стоки / предоставени услуги — **без ДДС** |
| `ord_disc` | Отстъпка (сума) — в лв. |
| `ord_vat` | ДДС — сума в лв. |
| `ord_total2` | Обща стойност на доставените стоки / предоставени услуги — **с ДДС** |
| `paym` | Начин на плащане (see codes below) |
| `pos_n` | Номер на виртуален ПОС терминал (when `paym = 2`) |
| `trans_n` | Референтен номер на финансовата транзакция |
| `proc_id` | Идентификатор на доставчика на платежни услуги |

### Per-article `<artenum>` fields

| Field | Documentation |
|---|---|
| `art_name` | Наименование на стоката / услугата |
| `art_quant` | Количество |
| `art_price` | Единична цена (без отстъпка) **без ДДС** — в лв. |
| `art_vat_rate` | ДДС-ставка |
| `art_vat` | ДДС — обща сума, в лв. |
| `art_sum` | Обща сума с ДДС — в лв. |

### `paym` codes (CloudCart maps payment providers to these via `n18_type`)

| Code | Meaning |
|---|---|
| `1` | Освободено по чл. 3 — плащане без ППП |
| `2` | Виртуален ПОС-терминал (requires `pos_n`) |
| `3` | Наложен платеж с ППП |
| `4` | Доставчик на платежни услуги (requires `proc_id`) |
| `5` | (see XSD enumeration in source — values 1–6 commonly observed) |
| `6` | (see XSD enumeration in source — values 1–6 commonly observed) |

In the CloudCart [[apps-n18-audit-settings]] screen, the merchant maps each active payment provider to one of these via the provider's `n18_type` value (2 or 4) and supplies the terminal IDs.

## Refunds — `<rorder>` → list of `<rorderenum>`

If any orders in the reporting month were fully or partially refunded, the file's `<r_ord>` count + `<rorder>` list summarise them:

| Field | Documentation |
|---|---|
| `r_ord` | Брой изцяло или частично върнати поръчки през периода |
| `r_total` | Обща стойност с ДДС на всички изцяло или частично върнати поръчки през периода |

Each refunded order is a `<rorderenum>`:

| Field | Documentation |
|---|---|
| `rorderenum` (the ord-n inside) | Номер на върната поръчка (уникален номер на поръчката в софтуера на е-магазина) |
| `r_amount` | Върната сума на клиента — в лв. |
| `r_date` | Дата на връщане на сумата |
| `r_paym` | Начин на връщане: `1` = по платежна сметка; `2` = по карта; `3` = в брой; `4` = Друг (matches the `return_pay_type` setting in [[apps-n18-audit-settings]]) |

## Filing window

Per Ordinance H-18/2006 article 52т:

- One file per reporting month.
- Submitted to NRA from the **1st to the 15th** of the month **following** the reporting month.
- Submitted through the NRA portal — **not** auto-submitted by CloudCart. The merchant downloads the XML from CloudCart and uploads it manually to NRA's portal.

## Related

- [[apps-n18-audit]] — the CloudCart app that produces files in this schema.
- [[apps-n18-audit-settings]] — settings that drive `eik`, `e_shop_n`, `domain_name`, `paym`-mapping, `r_paym` default.
- [[orders-receipt]] — per-order receipts are what get aggregated into the monthly Annex 38 audit XML.
- [`naredba-n18-alt-rezhim.txt`](naredba-n18-alt-rezhim.txt) — focused ordinance extract (Чл. 52о–52у + Приложения 33 и 38); grep `^Чл\. 52т\.` for the file-submission obligation and `^Приложение № 38` for the schema's regulatory anchor.
- [`dec_audit.xsd`](dec_audit.xsd) — the original schema (Windows-1251).
- [`dec_audit.utf8.xsd`](dec_audit.utf8.xsd) — UTF-8 copy for grep / human reading.
- [`dec_audit-sample.xml`](dec_audit-sample.xml) / [`dec_audit-sample.utf8.xml`](dec_audit-sample.utf8.xml) — a minimal valid file showing one paid order with two line items.
- [`README.md`](README.md) — the resources folder index.
- **NRA portal** — *Алтернативен режим за регистриране и отчитане на продажбите*: https://nra.bg/wps/portal/nra/fiskalni-ustroystva-supto-i-e-magazini/page.turgovia-v-internet-i-e-magazini/page.lternativen-rejim-za-registrirane-i-otchitane-na-prodajbite
