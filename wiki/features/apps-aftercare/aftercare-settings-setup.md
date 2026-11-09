---
type: feature
nav_path: "Apps → Withdraw from contract → Settings"
route_name: apps.aftercare.settings
route_path: /admin/apps/aftercare
aliases: ["Aftercare settings", "Aftercare setup", "withdrawal wizard", "aftercare onboarding", "withdrawal_window_days", "floating button withdrawal", "terms page", "return policy page", "aftercare 4-step wizard", "cc-aftercare-button", "withdrawal button style", "withdrawal menu link", "Отказ от договора в менюто"]
tags: [apps, aftercare, settings, setup, orders, withdrawal]
plan_gates: ["aftercare_pro"]
created: 2026-07-24
updated: 2026-11-09
source_count: 2
---

> Part of [[apps-aftercare]]. See the hub for the other aspects (compliance, admin inbox, free-vs-Pro, storefront flow).

# Aftercare — setup & settings

## Purpose

The onboarding wizard and every setting: the storefront button, the Terms / Return-policy pages, the withdrawal window, and the notification channels.

## Where to find it

Sidebar → Apps → **Withdraw from contract** → Settings (`apps.aftercare.settings`), presented as a **4-step wizard**: **Install · Confirm the data · Set the rules · Activate**. `onboarding_step` tracks the furthest step the merchant has reached (step 1 = install done). The Settings tab shares one interface with the [[aftercare-withdrawals-admin|Withdrawals inbox]].

## What the merchant can do here

- Walk the 4-step wizard to go live: confirm store data, designate the Terms / Return-policy pages, set the rules, and activate.
- Enable and style the storefront button (or rely on a menu link), or — on Pro — point the button at a custom page.
- Set the withdrawal window (≥ 14 days) and the notification channels.

## Settings & fields

| Field | Notes |
|---|---|
| `floating_button_enabled` | **Show floating button**. Off by default; while off, a warning asks to add the withdrawal link to a navigation menu (see *The menu link* below). |
| `button_text` | **Button text** (≤ 255 chars); empty → the official translated Art. 11a wording is used. |
| `floating_position` | **Button position**: left / right (default right). |
| `font_size` | **Button's font size in px**: whole number 8–48 (default 14). |
| `text_color` / `background_color` | **Text color** / **Background color**: colour pickers (defaults white / black). |
| `terms_page_id` / `return_policy_page_id` | The store CMS pages ([[page]]) shown as the withdrawal Terms / Return policy the customer must accept. |
| `withdrawal_window_days` | The withdrawal window in days — **required, 14–365** (14 = EU minimum). The clock starts on delivery — see [[aftercare-compliance]]. |
| `notify_email` | Customer email notifications — **locked on** (the Art. 11a acknowledgement must always send). |
| `auto_create_return` *(Pro)* | On each new withdrawal, auto-create a matching PENDING core order-return (on by default for Pro). |
| `use_custom_page` / `custom_page_id` *(Pro)* | **Use a custom page for the withdrawal form** + **Withdrawal page**: the floating button opens that page instead of `/withdrawal`. A menu link to the withdrawal section still opens `/withdrawal`; to put the custom page in a menu, link the page itself. |
| `notify_viber` *(Pro)* | Viber notification on withdrawal events. |
| `voucher_bonus_enabled` / `voucher_bonus_percent` *(Pro)* | A store-credit voucher (with a bonus %) as a refund alternative — **declared but not yet operational** in this release. |

## Business rules

- The window (`withdrawal_window_days`) is **required** and bounded **14–365** — 14 is the EU minimum and cannot be undercut (see [[aftercare-compliance]]).
- `notify_email` is **locked on** — the acknowledgement of receipt must always send; the toggle is forced on and `accepted`-validated.
- The Pro settings (`auto_create_return`, `use_custom_page`, `notify_viber`, `voucher_bonus_*`) stay disabled behind a "paid service / Buy here" prompt without the `aftercare_pro` plan feature — see [[aftercare-free-vs-pro]].
- The labels above are the English admin labels; the Bulgarian ones come from the admin's translations and are not quoted here.

### Confirm the data (step 2)

The company fields are the store's **invoicing data**: saving them here also updates [[settings-invoicing]]. Company name, phone, country, city, street and postal code are required; for Bulgaria also the ЕИК (format-checked) and the МОЛ. The Terms and Return-policy pickers list the store's pages except page-builder pages, and suggest a page whose address looks like terms / returns while nothing is chosen.

### How the floating button is drawn

The button appears only while the app is active and **Show floating button** is on. It is a rounded, bold pill fixed 20 px from the bottom and from the chosen side, above other page content, with a light shadow. It is drawn in an isolated layer of the page, so the theme's CSS and custom styles cannot restyle it: its look comes only from the font size and the two colours set here.

The colours are saved as text of up to 9 characters, with no colour-format check on the server, and are written into the button's style as they are. An empty colour falls back to white text on black. A value the browser does not read as a colour is ignored by the browser (verify how it then renders). Saving rebuilds the store's apps script, which carries the button (verify how soon visitors see it).

### The menu link

The settings have no menu field. The link is added under **Design → Navigation** ([[design-navigation]]): on the menu's tab click **Add link**, choose **Link to a specific store section**, and pick **Withdraw from contract** (in a Bulgarian admin „Отказ от договора“) in the **Theme section** list. It opens `/withdrawal`. A **Web link** item also works, but only with the full address (`https://<store-domain>/withdrawal`); a bare `/withdrawal` is rejected — see [[design-navigation-item-types]]. The entry is listed on every store, so a link added while the app is inactive leads to a 404 page.

Whether a menu link alone, with the button off, meets Art. 11a is a legal assessment for the merchant; the app treats either the button or a menu link as the way to keep the function reachable.

### Activating before setup is complete

Both legal pages are **required**: activation needs a Terms page, a Return-policy page and the company name, country and city. Otherwise it is refused with: *"Complete the setup before activating: confirm the company data and select the Terms & Conditions and Return policy pages."* / *"Завършете настройката преди активиране: потвърдете фирмените данни и изберете страниците с Общи условия и Политика за връщане."* While the app is inactive, `/withdrawal` answers 404 and the button is not shown.

## Related

- [[apps-aftercare]] — hub.
- [[aftercare-compliance]] — why the window minimum is 14 days and starts on delivery.
- [[aftercare-free-vs-pro]] — the Pro-gated settings.
- [[storefront-withdrawal]] — where the button + Terms / Return-policy pages appear to the customer.
- [[page]] — the CMS pages designated as Terms / Return policy.
- [[design-navigation]] — where the menu link is added.

## Open questions

None.
