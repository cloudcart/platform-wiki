---
type: reference
nav_path: "Resources"
aliases: ["wiki resources", "downloaded resources", "regulation copies"]
tags: [resources, references, regulations]
created: 2026-06-08
updated: 2026-06-08
source_count: 1
---
# wiki/resources/ — downloaded external references

This folder holds **searchable copies of external documents** that the wiki references — laws, ordinances, schemas, public specifications. Scope is narrow on purpose: only material the AI assistant needs to look up in the field, kept small enough to grep in one shot.

For the N18 Audit integration the only regulatory text we need is the **Alternative regime for registering and reporting sales** (Глава седма "г" of Наредба № Н-18/2006, articles Чл. 52о–52у, plus Приложение № 33 and Приложение № 38). The rest of the ordinance is not consulted by the integration and is left out.

## What lives here

| File | Source | What it is |
|---|---|---|
| [`naredba-n18-alt-rezhim.txt`](naredba-n18-alt-rezhim.txt) | https://lex.bg/laws/ldoc/2135540645 | Focused extract of Наредба № Н-18/2006 covering ONLY the alternative regime: articles **Чл. 52о – 52у** + **Приложение № 33** (e-shop registration form that issues the UIN) + **Приложение № 38** (audit-file schema description). UTF-8 plain text, ~33 KB, 711 lines. |
| [`dec_audit.xsd`](dec_audit.xsd) | NRA "Алтернативен режим" portal | XML Schema for the monthly audit file (Приложение № 38 към чл. 52т, ал. 2). Original Windows-1251. The CloudCart N18 Audit app produces files validating against this schema. |
| [`dec_audit.utf8.xsd`](dec_audit.utf8.xsd) | derived | UTF-8 copy of the schema — same structure, encoding normalized so Bulgarian `<xs:documentation>` strings are grep-friendly. |
| [`dec_audit-sample.xml`](dec_audit-sample.xml) | NRA "Алтернативен режим" portal | A minimal valid sample file (one paid order with two line items, no refunds). Original Windows-1251. |
| [`dec_audit-sample.utf8.xml`](dec_audit-sample.utf8.xml) | derived | UTF-8 copy of the sample. |
| [`dec_audit-schema-cheatsheet.md`](dec_audit-schema-cheatsheet.md) | derived from XSD | Human + agent-readable cheat-sheet of every element in the schema with Bulgarian field documentation and value enumerations (paym codes, r_paym codes, e_shop_type). |

## How to search

Grep markers for `naredba-n18-alt-rezhim.txt`:

- Articles → `^Чл\. <N>\.` (covers `Чл. 52о` to `Чл. 52у`)
- Annex 33 (e-shop registration form, issues the merchant's UIN) → `^Приложение № 33`
- Annex 38 (XML audit-file schema description) → `^Приложение № 38`

Grep markers for `dec_audit.utf8.xsd`:

- Element names → `<xs:element name="<name>"`
- Bulgarian field documentation → `<xs:documentation>`
- Allowed enumerations → `<xs:enumeration value=`
- Type constraints → `<xs:restriction base=`, `<xs:minLength`, `<xs:maxLength`, `<xs:pattern`

The cheat-sheet (`dec_audit-schema-cheatsheet.md`) is the first place to look — it lists every field with its Bulgarian description and value codes (paym 1–6, r_paym 1–4, e_shop_type 1 vs 2).

## When to refresh

Re-extract `naredba-n18-alt-rezhim.txt` only when the **Алтернативен режим** section of the ordinance is amended (typically announced in ДВ alongside changes to Чл. 52о–52у). Source URL: https://lex.bg/laws/ldoc/2135540645 — open in browser, copy text of Глава седма "г" + Приложения 33 and 38, replace the file.

The XSD schema and sample XML are refreshed only when NRA publishes a new Приложение № 38 version. Source page (JS-rendered, behind anti-bot challenge, NOT curl-friendly — open in browser):

- **NRA Alternative-regime portal page** — *Алтернативен режим за регистриране и отчитане на продажбите*: https://nra.bg/wps/portal/nra/fiskalni-ustroystva-supto-i-e-magazini/page.turgovia-v-internet-i-e-magazini/page.lternativen-rejim-za-registrirane-i-otchitane-na-prodajbite

## What does NOT belong here

- Internal CloudCart documents (those go under `wiki/concepts/` or `wiki/features/`).
- Source code, schemas under active development (those belong in the product repo, not the wiki).
- Anything proprietary or paywalled — only publicly accessible references.
- Articles / annexes of Наредба № Н-18 that are outside the alternative-regime scope — they're not consulted by the N18 Audit integration; consult lex.bg directly if needed.

## Related

- [[apps-n18-audit]] — uses [`naredba-n18-alt-rezhim.txt`](naredba-n18-alt-rezhim.txt), [`dec_audit.xsd`](dec_audit.xsd), and [`dec_audit-sample.xml`](dec_audit-sample.xml).
- [[apps-n18-audit-settings]] — same; the settings screen drives the file's `eik`, `e_shop_n`, `domain_name`, `paym`-mapping, and `r_paym` default.
- [[orders-receipt]] — receipts get aggregated into the monthly Annex 38 audit XML.
- [`dec_audit-schema-cheatsheet.md`](dec_audit-schema-cheatsheet.md) — element-by-element reference for the audit XML.
