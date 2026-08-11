---
type: feature
nav_path: "Settings → Store settings → Language settings"
route_name: general.settings
route_path: /admin/settings/general
aliases: ["Storefront language", "Admin panel language", "Customer name display", "Language change", "the search engine reindex confirmation", "Език на магазина", "Език на админ панела"]
tags: [settings, general, language, multi-language, search, the search engine, customer-name]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[settings-general]]. See the hub for related aspects (store details, locale, maintenance, security key, product badges, operational toggles, industry multi-select).

# Store settings — Language settings

## Purpose

The Language settings box exposes three fields with **very different cost profiles** on save:

- **Storefront language** (`language`) — the heaviest change on the entire screen. Switching it triggers a synchronous translation rebuild, a JS-data regeneration, AND an asynchronous search-engine re-index that recreates ALL listing-engine indexes. Stores on the search engine see a confirmation modal warning about temporary maintenance during reindex.
- **Admin Panel language** (`language_cp`) — applies immediately with no rebuild; the admin UI just swaps the label translations.
- **Customer name display** (`customer_name_display`) — a template string controlling first/last name ordering across all customer-facing renders. Applies retroactively to all existing customers.

> The right-side info panel reads: *"Storefront Language — This is the language that your customers will see on your eshop. Admin Panel Language — Choose the language of your admin panel."*

## Where to find it

Sidebar → Settings → **Store settings** → Language settings box.

## What the merchant can do here

- Set the storefront language shown to customers on the public site.
- Set the admin panel language independently (the merchant's interface language, different from the customer's).
- Choose how customer names are displayed in the admin: `{first_name} {last_name}` or `{last_name} {first_name}`.

## Settings & fields

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Storefront Language** (`language`) | Language shown to customers on the public site. | Required. Searchable. Triggers heavy server-side rebuild on change — see Business rules. |
| **Admin Panel Language** (`language_cp`) | Language of the admin panel itself. Applies immediately on save (UI reloads in the new language). | Required. Searchable. |
| **Customer name display format** (`customer_name_display`) | How customer names are shown in the admin: `{first_name} {last_name}` or `{last_name} {first_name}`. | Two options only. Defaults to `{first_name} {last_name}` on a fresh store. |

## Modals and sub-flows

### Confirm storefront language change modal (the search engine only)

A confirmation popup that intercepts the Save action ONLY when:

- The merchant has changed the `language` field, AND
- The store's listing engine is `the search engine` (the platform's modern search backend).

The modal cannot be closed with Escape and is centred on the page.

| Element | Content |
|---------|---------|
| **Title** | *"Confirm storefront language change"* |
| **Warning body** | *"Warning: Proceeding with this action will temporarily place your website into maintenance mode while a new CloudCart search engine index is being generated."* (rendered as a warning block) |
| **Confirm action** | Marks the language change as acknowledged, closes the popup, then re-runs the save handler — this time the save proceeds past the language-change interception. |
| **Implicit cancel** | Closing the popup (via the X / backdrop click if allowed) reverts the language change in the form to the server value. |

Stores on any OTHER listing engine (the search index, the older default search backend, etc.) save the language change with no modal — but the same reindex-and-rebuild cost still applies; the merchant just doesn't see the upfront warning.

## Business rules

### Changing the Storefront language triggers heavy server-side work (exact order)

When `language` changes on save, the following runs in this order, in the same request:

1. The store's active locale is switched to the new language.
2. A synchronous translation rebuild appends the new language's translations to the store's stored translations.
3. The forced admin-language session flag is cleared.
4. Required-setting defaults are re-synced for the new language.
5. A storefront-language-change event fires. The search subsystem catches it and kicks off the indexer, which **recreates ALL search engine indexes** for the store (works for whatever listing engine is active — the search engine, the search index, etc.).
6. A synchronous rebuild regenerates the storefront's pre-built data files with new translations + currency.

**Merchant-visible effect:** the save can take several seconds (sometimes longer). The storefront may briefly show stale translations until JS data files refresh on next request. For the search engine stores, the confirmation modal documented above warns the merchant before the save runs. For other engines the modal does NOT appear but the reindex still runs.

The storefront-language-change event also broadcasts on a **private WebSocket channel** called `settings` — any live admin UI listening on that channel gets notified. It does NOT propagate to merchant-subscribed webhooks (those are a separate system entirely — see [[settings-hooks]]).

### Admin Panel language change applies immediately, but reload differs for CloudCart staff

When `language_cp` differs from the server's current admin language:

- **For regular merchants:** the translation files for the new language are dynamically swapped in (the script tags for translations and help boxes are re-inserted with the new locale's source). The page does NOT reload; the merchant just sees the labels update in place.
- **For CloudCart employees logged into the store:** a server-side language-switch request is made first, and on success the browser does a full page reload. This is because the employee's session needs the locale change persisted server-side.

### `customer_name_display` is a template used everywhere a customer name appears

The setting value is a template string with `{first_name}` and `{last_name}` tokens. The system applies it whenever a full name is assembled across multiple record types — so it controls how customer/order/subscriber names are rendered in:

- The admin's customer list and order list.
- Order details and the customer detail page.
- Outgoing transactional emails to customers (anywhere the template uses the customer's or order's full-name field).
- Shipping address rendering (via the shipping-address formatter).
- Subscriber lists in marketing.
- Invoices (which use the same name formatting).

Changing this value applies retroactively to all existing customers — there is no data migration; the formatting is computed on read.

### Hidden `customer_name_template` override for shipping waybills

There is a related hidden override setting `customer_name_template` (note: NOT `customer_name_display`) — when populated via API / back-channel, it overrides the display template specifically for the **shipping address full-name** sent to couriers. This setting is not exposed in any UI; it exists for stores that need a different name format on shipping waybills than in the admin (e.g., reversed last/first for postal services). Standard merchants should leave it unset — the shipping-address formatter falls back to `customer_name_display` when `customer_name_template` is empty.

### Required validation

`language`, `language_cp`, and `customer_name_display` are all required by the frontend before submit. Backend re-validates and rejects with a per-field error if anything is blank.

### Two options only for customer name display

The two options for `customer_name_display` are stored as literal template strings: `{first_name} {last_name}` and `{last_name} {first_name}`. These templates are then applied wherever a customer's full name is rendered.

## Related

- [[settings-general]] — hub.
- [[multi-language]] — concept page on how language is applied across the storefront and admin.
- [[settings-translations]] — where translations live after a language change.
- [[storefront-architecture]] — the search index / the search engine listing-engine read side that gets re-indexed on language change.
- [[settings-hooks]] — webhook system (NOT notified by the storefront-language-change event — that event is admin-internal only).
- [[settings-general-locale]] — sibling field group that also triggers JS regenerate (currency) but no search re-index.

## Open questions

None.
