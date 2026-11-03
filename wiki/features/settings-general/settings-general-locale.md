---
type: feature
nav_path: "Settings → Store settings → Locale (Date/Time, Currency, Units, Country)"
route_name: general.settings
route_path: /admin/settings/general
aliases: ["Date format", "Time format", "Timezone", "Currency", "Unit system", "Operation country", "Standards and formats", "Часова зона", "Валута", "Държава на опериране"]
tags: [settings, general, locale, currency, timezone, country, units, date-format]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-general]]. See the hub for related aspects (store details, language, maintenance, security key, product badges, operational toggles, industry multi-select).

# Store settings — Locale (Date/Time, Currency, Units, Country)

## Purpose

This aspect covers the **regional defaults** that govern how dates, times, prices, weights, and country-dependent integrations behave across the platform. Three of the four boxes that touch this — *Date and Time Formats*, *Currency and units*, *Country of operations* — sit under a shared header label "Standards and formats — Choose your preferred language, currency and more". Each field's value is stored directly on the Site record (not in the main settings store), so changes take effect immediately everywhere on the next read.

Two notable side-effects: changing the **currency** triggers a synchronous JS-data regeneration; changing the **timezone** runs the value through a Windows-canonical normalizer before storage. Language has heavier side-effects and lives on [[settings-general-language]].

## Where to find it

Sidebar → Settings → **Store settings** → middle of the page (three adjacent boxes: *Date and Time Formats*, *Currency and units*, *Country of operations*).

## What the merchant can do here

- Set the date format and time format the admin will use everywhere (admin + storefront).
- Set the timezone — all stored timestamps are interpreted in this zone for display.
- Choose the store's display currency (affects how all prices are shown).
- Choose the unit system (metric / imperial) for weights and dimensions.
- Set the country of operation — affects shipping integration filtering, tax defaults, invoicing.

## Settings & fields

### Box: Date and Time Formats (`date_and_time`)

> "This is your store's date and time format. All dates will be displayed in this format."

Header label: "Standards and formats — Choose your preferred language, currency and more".

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Date format** (`date_format`) | How dates are rendered everywhere (admin + storefront). | Options derived from `dateFormatOptions`. **Backend accepts only the values `2` or `6`** — other DateTimeFormat options are blocked. |
| **Time format** (`time_format`) | How times are rendered. | Options derived from `timeFormatOptions`. **Backend accepts only `1`, `4`, `5`, or `7`** — other DateTimeFormat options are blocked. |
| **Time zone** (`timezone`) | The store's timezone. All stored timestamps are interpreted in this zone for display. | Grouped, searchable dropdown. **Normalized to Windows-canonical name on save** — see Business rules. |

### Box: Currency and units (`currency_and_mass`)

> "Currency — All prices that you enter will be displayed in this currency. Unit — Select your store's unit."

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Currency** (`currency`) | The store's display currency. Affects how all prices are shown. | Required. Searchable. Changing it **regenerates storefront JS data files** — see Business rules. |
| **Unit** (`unit_system`) | Metric or imperial unit system for weights/dimensions. | Required. Options from `meta.units`. |

### Box: Country of operations (`country_operation`)

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **The country in which your store operates** (`operation_country`) | The legal/operational country of the store. Affects defaults for tax, shipping, invoicing. | Required. Searchable. Options from `meta.countries`. |

## Business rules

### Changing the Currency regenerates storefront JS data

When `currency` changes on save, the `js:data-generate` artisan task runs synchronously inside the save request to regenerate the storefront's JS data files with the new currency. The save can take several seconds; the storefront may briefly show stale currency formatting until the new JS files load on the next request.

### Currency-vs-existing-orders alert is computed but not displayed

The backend exposes a flag `currencyAlertForExistingOrders` (true when the store has any completed orders), intended to warn the merchant that changing currency now will leave historical order amounts displayed in the old currency. **The current Vue page does not display this warning** — the flag is computed and shipped to the client but no UI consumes it. Practical merchant impact: a merchant who changes currency after taking orders gets no in-app warning, and historical orders keep their numeric values stored at the time of purchase (interpreted in the new currency at display time, which can be misleading). See [[multi-currency]] for the broader single-currency model.

### Timezone values are canonicalized to Windows-canonical names

When the merchant picks a timezone, the value passes through a Windows-canonical normalizer before being stored on `site.timezone`. Both raw IANA names (e.g., `Europe/Sofia`) and Windows Zone names (e.g., `FLE Standard Time`) are accepted and converted to the same canonical form. No merchant-visible effect — relevant only when comparing settings exports.

### `operation_country` filters shipping + payment integration lists

The country chosen here is used by [[settings-shipping]] to filter the "Browse shipping integrations" modal — a Bulgarian store sees Econt / Speedy / Bulgarian Posts; a Romanian store sees Fan Courier / Cargus / DPD Romania; etc. The merchant cannot override this filter from the list; to access integrations for other countries, they must change `operation_country` first. Several payment providers (NewPay, BGN2EUR, etc.) also gate activation by `operation_country`. See [[payment-providers-newpay]] / [[apps-bgn2eur-settings]] for examples.

### Date/time format enum values are non-contiguous

Date format accepts `2` or `6` only; time format accepts `1`, `4`, `5`, or `7` only. Other enum values that exist in the platform's DateTimeFormat catalogue are blocked by the validator. Practical effect: API automation that tries to set a different format value gets a "must be one of [...]" error.

### Fields stored directly on the Site record (not the settings store)

Unlike the Store Details fields, `timezone`, `currency`, `unit_system`, and `operation_country` live as columns on the Site record. They are visible **immediately** everywhere after save — no settings-cache flush needed. See the hub [[settings-general]] for the full storage-split table.

### Required validation

All five fields (`date_format`, `time_format`, `timezone`, `currency`, `unit_system`, `operation_country`) are required by the frontend before submit. Backend re-validates and rejects with a per-field error if anything is blank.

## Related

- [[settings-general]] — hub.
- [[settings-general-language]] — language change has heavier side-effects than currency (translation rebuild + search re-index in addition to JS regenerate).
- [[multi-currency]] — single-currency-by-design model; all prices stored in the chosen base currency.
- [[settings-shipping]] — filters integrations by `operation_country`.
- [[settings-invoicing]] — uses currency for invoice amounts.
- [[apps-bgn2eur-settings]] / [[payment-providers-newpay]] — examples of apps gated by `operation_country`.

## Open questions

None.
