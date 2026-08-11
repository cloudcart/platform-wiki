---
type: feature
nav_path: "Design → Modules → Engagement → Contact information"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/contactInformation
aliases: ["Contact information module", "contactInformation module", "Contacts page text", "Модул контактна информация", "Контакти - текст"]
tags: [design, modules, engagement, contact, contact-info]
plan_gates: []
created: 2026-06-10
updated: 2026-06-24
source_count: 4
---

# Engagement module — contactInformation

> Part of [[design-modules-engagement]]. See the category page for the other engagement modules.

## Purpose

`contactInformation` renders the **prose block** around the contact form on the storefront's `/contacts` page — typically the store's address, phone, email, opening hours, and any extra context the merchant wants visible. It is **the master switch** for whether the [[design-module-contact-form]] is visible at all (via `show_form`), and it carries a second rich-text "Custom information" block (`custom_information`) that the merchant can toggle on for FAQs, return-policy snippets, or social links.

Like `contactForm`, `contactInformation` is in the platform's hard-coded system-module list — every theme that ships a `/contacts` page uses this module.

## Where to find it

Sidebar → **Design** → **Modules** → **Contacts** tab → card labelled *"Contact information"*.

Clicking the card opens the side panel with the four settings below.

## What the merchant can do here

- Decide whether the [[design-module-contact-form]] is visible (`show_form` = yes / no).
- Toggle the secondary custom-information block (`show_custom_information` = yes / no).
- Edit the **main contact prose** (`page_text`) — the typical place for address + phone + email + opening hours.
- Edit the **secondary prose block** (`custom_information`) — useful as a second prose section.
- Save / Reset / Cancel — standard module controls; success message *"Module successfully edited"*.

## Settings & fields

| Field | Type | Validation | Default | What it controls |
|-------|------|------------|---------|------------------|
| `show_form` | Select (yes / no) | `in:yes,no` | `yes` | Whether the [[design-module-contact-form]] slot renders on the page (label: *"Show form"*) |
| `show_custom_information` | Select (yes / no) | `in:yes,no` | `no` | Whether the **Custom information** rich-text block renders (label: *"Show custom information"*) — **also gates the contact details in the page's structured-data / microdata** (see Business rules) |
| `page_text` | TinyMCE rich text | `char:0,3000` | empty | Main copy shown above the form — typically address + phone + email + opening hours + intro text |
| `custom_information` | TinyMCE rich text | `char:0,3000` | empty | Optional second rich-text block (only rendered when `show_custom_information=yes`) |

**Allowed HTML tags in both rich-text fields:** `<b><a><p><br><s><em><hr><strong><small><code><kbd><samp><var><del><ins><cite><q><span><div><blockquote><ul><ol><li><font><pre><h1>` through `<h6>` — note `<img>` is NOT in the allowlist for either field. The merchant uploads contact graphics via the theme directly, not embedded here.

## Theme dependencies

Universal — every theme that ships a `/contacts` page uses this module. Some themes (e.g., a theme that ships it) ADDITIONALLY pull `contactInformation → page_text` into a sidebar or footer block (verify in the theme's templates). The auto-pulled fallback shown when `custom_information` is empty includes the store's saved address + phone formatted via the platform format helper — meaning even a brand-new store with an empty module shows SOMETHING usable on `/contacts`.

## Business rules

### `show_form` controls the form, not the slot

Setting `show_form = no` hides the [[design-module-contact-form]] from the rendered page. The form slot still exists in the template; it just renders empty. To re-enable the form, the merchant flips this back to `yes`.

### `show_custom_information` also gates the contact microdata

Beyond the visible Custom information block, this toggle also controls whether the store's contact details (**email**, **phone**, and the custom contact info) are emitted into the page's **structured data / microdata** — the schema.org `itemprop` contact markup. With `show_custom_information = no`, those contact `itemprop` values are dropped from the markup as well as from the visible block, so a merchant who hides the block also keeps their email / phone out of the page's structured data. Turn it on to expose the contact details to search engines via microdata.

### Falls back to store-general settings when empty

When `custom_information` is empty AND `show_custom_information = yes`, the template renders an auto-built block with the store's address (country / city / postal code / street) and phone, pulled from the platform's address-format helper. The merchant doesn't have to fill anything to get a usable contact page — the platform fills in the gaps from [[settings-general]].

### Phone / email links work inline

The TinyMCE allowlist includes `<a>`, so `tel:` and `mailto:` links work in both rich-text fields. A common pattern: `<a href="tel:+359888123456">+359 888 123 456</a>` — clicking on mobile dials the phone directly.

### Reset wipes everything

Clicking **Reset module** restores the defaults: `show_form=yes`, `show_custom_information=no`, both rich-text blocks empty. There is no undo — the merchant has to re-paste any custom prose.

### Localization

`page_text` and `custom_information` are stored as single strings per instance. With the multi-language app installed, both accept per-language sub-keys via the TinyMCE language switcher; otherwise they're single-string. See [[multi-language]] for the merge behaviour.

## How it works (verified against backend)

### Template path

The platform module template under the theme templates. Themes may override at the theme's own override.

### Storage

One `front_widget` row keyed by mapping `contact.information`, JSON blob containing the four fields above. The `_default_settings` in the module class are merged in on every read (so adding a new field via a deploy doesn't break existing stored rows).

### Cache

Save / Reset bump the per-site cache key via the platform cache helper — the next storefront request rebuilds. See the storage / cache mechanics documented under [[design-modules-utility-storage]] (same pipeline applies to engagement modules).

### Sanitisation (commented out)

The module class has a `saveSettings` override that would call the platform code with the allowlist above — but it is currently commented out. This means submitted HTML is stored as-is. The TinyMCE editor on the admin side filters most dangerous markup before submit, but a determined merchant pasting raw HTML can bypass it. (verify) whether the storefront output applies any escape filter; the template uses `nofilter` on both fields.

### Pulled into other slots

Some themes read `contactInformation → page_text` from the module facade and render it in a sidebar or footer slot in addition to the main `/contacts` page render. Switching themes can change where the SAME content appears.

## Related

- [[design-modules-engagement]] — hub.
- [[design-module-contact-form]] — sibling; `show_form` here controls its visibility.
- [[design-module-contact-google-map]] — sibling; the third block on the `/contacts` page.
- [[settings-general]] — store address / phone / contact-email defaults that this module falls back to.
- [[design-themes]] — theme picks where `page_text` renders (some themes also drop it in sidebar / footer).
- [[multi-language]] — per-language rich-text content via the `multylang` app.

## Open questions

- 📡 **Per-language `page_text` / `custom_information`.** With `multylang` installed, both fields accept per-language sub-keys. GraphQL-resolvable: query whether the `multylang` app is installed on this merchant's store.
- ⏸️ **HTML sanitisation.** The `saveSettings` override that would sanitise HTML is commented out — submitted HTML is stored verbatim. (verify) whether the storefront applies any escape filter on render; the template uses `nofilter`.
- ⏸️ **`<img>` in `page_text`.** Allowlist excludes `<img>` — the TinyMCE editor strips images on paste. (verify) whether the merchant can work around this by editing in HTML source view.
