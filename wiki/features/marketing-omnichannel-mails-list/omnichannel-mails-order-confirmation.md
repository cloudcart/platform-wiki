---
type: feature
nav_path: "Marketing → Channels → Email notifications → Order confirmation"
route_name: marketing-mails-list
route_path: /admin/marketing/omnichannel/mails/list
aliases: ["Order confirmation email", "New order email", "Order confirmation per payment method", "Product list in email", "product_list", "VAT line in order email", "Email product list colour", "Потвърждение на поръчка имейл", "ДДС в имейла за поръчка", "Производител в имейла", "Количество в имейла"]
tags: [marketing, omnichannel, email, notifications, orders, vat, product-list]
plan_gates: ["change_email_notifications"]
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[marketing-omnichannel-mails-list]]. See the hub for related aspects (mail labels, editor modal, toggles & gating, variables, customisation limits).

# Email notifications — order confirmation and the product list

## Purpose

The order-confirmation email exists as **four separate templates**, one picked by the order's payment method. This page says which one is sent when, what the VAT line is, what the `{$product_list}` block renders (its captions, the brand line, its colours) and which language the email goes out in.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Email notifications** (`/admin/marketing/omnichannel/mails/list`). Each of the four templates is its own row; click its name to open the editor ([[omnichannel-mails-editor-modal]]).

## What the merchant can do here

- Edit the wording, layout and VAT row of each confirmation template separately.
- Not possible: change what the product list shows, rename its captions or recolour it.

## Settings & fields

### Four confirmation templates, chosen by payment method

| Label | Sent for | Extra variable |
|---|---|---|
| `order_payment_via_bwt` | Bank transfer | `{$bank_details}` — the payment method's description |
| `order_payment_via_cod` | Cash on delivery | `{$cod_details}` — the payment method's description |
| `order_payment_via_voucher` | Voucher | `{$voucher_details}` — the payment method's description |
| `order_add` | Everything else: card and other online payments (only once the payment is authorised or completed, otherwise the payment-error mail goes out), leasing by UniCredit, TBI or BNP (the provider's consent PDF is attached), Pay on place, and every [[apps-fast-order\|fast order]] | — |

All four allow the same order variables, `{$tax}` included (full lists: [[omnichannel-mails-variables]]). When an invoicing provider is active, the invoice and receipt PDFs are attached ([[settings-invoicing]]); with [[apps-garan-label]] installed, each line carries its durability badge.

### The VAT line

- In CloudCart's default design of all four templates (and of the status-change and fulfilment mails) the totals carry a typed caption **"ДДС:"** (English "Tax:") followed by `{$tax}`.
- `{$tax}` is the sum of the order's tax lines (VAT and any other tax, before and after shipping) as a money amount. An order with no tax lines shows a zero amount.
- The caption is ordinary text in the template, not a translation. No setting hides the row: rename or delete it in the editor, separately in each of the four templates.
- `{$subtotal}` also lists, under the subtotal, each discount and tax counted before shipping, by name.

### What `{$product_list}` renders

The block is built by the platform at send time; the editor only holds the variable. One row per product:

- image (150 px box), linked to the product page;
- the name, bold, linked, in dark grey (#4d4d4d);
- the variant's parameters ("Size: M, Colour: Red");
- the **brand line**: caption plus the product's brand ([[products-vendors]]) as recorded on the order line when the order was placed; left out when the product has no brand;
- **"Количество: N"** (English "Quantity:");
- options with their prices, then discount and discount-code lines;
- on the right, the price in bold; when discounted, the old price struck through in grey.

### Captions are fixed platform strings

- **"Производител"** (English "Brand") and **"Количество"** ("Quantity") come from the platform's own language files, in the store's language.
- They are **not** on [[settings-translations]]: that screen holds the storefront's labels and the theme's own labels, and the email does not read them. Renaming the storefront's brand label (`global.label.vendor`, section `global`) changes the product page, not the email.
- The merchant cannot rename them. The only choice is to keep `{$product_list}` or remove it.
- The one exception is the [[apps-garan-label]] badge text, which is a storefront label and so follows an override on that screen (verify).

### Colours

- The name's dark grey and the old price's grey are fixed. All other text in the block has no colour of its own and takes the colour of the text block that holds `{$product_list}` (verify per email client).
- No control recolours the block, per template, per mail type or store-wide. On a dark template, give the row or column holding `{$product_list}` a light background in the editor; the product name stays dark grey whatever the template.
- The editor is the embedded Unlayer designer; its row and column background panels are its own, and CloudCart does not pass it a language (verify which language its panels show).

## Business rules

### Which language is sent

Each template keeps one version per language. The email is built in the **store's language** (the storefront language in [[settings-general]]): that language's version of the template, or the English version when there is none. The product-list captions follow the same language. Neither the shopper's language nor the admin panel's language is used, and the editor opens the same store-language version. A store run in another language through [[apps-multilang]] is a separate store with its own templates.

### When it is not sent

The store-wide **Send notifications to customers** switch and the template's own on/off both apply ([[omnichannel-mails-toggles-gating]]). For orders paid through a gateway, the confirmation goes out from the checkout return page, once per order ([[checkout-return-emails-tracking]]). A wallet top-up or gift-card purchase gets none of the four: it gets its own email when the credit is added ([[virtual-wallet-emails]]).

## Related

- [[marketing-omnichannel-mails-list]] — hub.
- [[omnichannel-mails-labels]] — the full label catalogue.
- [[omnichannel-mails-variables]] — what each template may use.
- [[omnichannel-mails-customisation-limits]] — what can and cannot be edited.
- [[settings-translations]] — storefront labels only.
- [[products-vendors]] — the brand shown on the brand line.
- [[tax-computation]] — where the order's tax lines come from.

## Open questions

- The language of the Unlayer designer's own panels.
