---
type: feature
nav_path: "Marketing → Channels → Email notifications → Variables"
route_name: marketing-mails-list
route_path: /admin/marketing-new/omnichannel/mails/list
aliases: ["Customer mail variables", "Mail allowed_vars", "Mail allowed_subject_vars", "required_subject_vars", "Variable allow-list", "Имейл променливи", "Допустими променливи в шаблон"]
tags: [marketing, omnichannel, email, notifications, variables, templating]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-omnichannel-mails-list]]. See the hub for related aspects (mail labels, editor modal, toggles & gating, abandoned-cart, customisation limits).

# Email notifications — variables

## Purpose

Each [[omnichannel-mails-labels|mail label]] declares a fixed **allow-list of variables** that may appear in its body and subject. Variables outside the allow-list are stripped server-side before rendering, preventing data leakage and broken substitution. This page documents how the allow-list works, where it lives, how the merchant inserts variables, and the `required_subject_vars` validation rules.

## Where to find it

The variables legend appears in the right-hand panel of the **template editor modal** at `/admin/marketing-new/omnichannel/mails/list` (click any row's Name to open). See [[omnichannel-mails-editor-modal]].

## What the merchant can do here

- See the **2-column grid of `{variable, description}`** in the editor's variables legend.
- **Click any variable button** (`fa-copy` icon) to copy the variable code (e.g., `{$order_id}`) to clipboard, then paste into the Subject input or Unlayer body.
- The legend is **per-label** — opening `welcome` shows account variables; opening `order_status_change` shows order variables.

## Settings & fields

### Variable allow-list shape (verbatim from `App\Helper\Mail\Config::$customer_mail_type_vars`) (verify)

Per-label, three keys may be set:

| Key | Purpose |
|---|---|
| `allowed_vars` | Variables that may appear in the **HTML body**. Filtered server-side at send time. |
| `allowed_subject_vars` | Variables that may appear in the **subject line**. Filtered server-side at send time. |
| `required_subject_vars` | Variables that **MUST** be present in the subject (e.g., `{$order_id}` for some order mails). Validated at save (verify). |

The endpoint `GET /admin/api/core/marketing/customer-mails/{id}/variables` returns the body's `allowed_vars` list as `[{value, name}, ...]` — this populates the editor's variable-insert legend.

### Allowed variables — `order_product_fulfil` sampling

For the `order_product_fulfil` label (verify):

`{$logo}`, `{$shop_url}`, `{$shop_name}`, `{$customer_first_name}`, `{$customer_last_name}`, `{$customer_email}`, `{$product_list}`, `{$related_products}`, `{$best_sellers}`, `{$order_id}`, `{$purchase_date}`, `{$total}`, `{$subtotal}`, `{$order_discount}`, `{$order_status}`, `{$note}`, `{$site_order_link}`, `{$shipping_provider}`, `{$fulfillment_status}`, `{$billing_address}`, `{$shipping_address}`, `{$shipping_provider_description}`, `{$payment_provider_description}`, `{$desired_delivery_date}`, `{$admin_note}`, `{$delivery_date}`, `{$expedition_date}`, `{$tracking_link}`, `{$tracking_code}`, `{$shipping_price}`, `{$payment_status}`, `{$payment_provider}`, `{$tax}`.

### Variable groupings per label family

- **Account labels** (`welcome`, `email_confirmation`, `password_change`, …) — `{$customer_first_name}`, `{$customer_last_name}`, `{$customer_email}`, `{$shop_url}`, `{$shop_name}`, `{$logo}`. No order variables.
- **Order labels** (`order_add`, `order_status_change`, `order_product_fulfil`, `send_invoice`, …) — order + customer + shop variables. `{$order_id}`, `{$total}`, `{$tracking_link}` etc.
- **Abandoned cart** (`abandoned_restore_link`) — cart variables + `{$link}` (the restore-cart URL). See [[omnichannel-mails-abandoned-cart]].
- **Newsletter** (`customer_newsletter_subscribe`, `customer_newsletter_unsubscribe`) — subscriber + shop variables.
- **Product favourite labels** (`product_out_of_stock`, `product_quantity_low`) — product + customer + shop variables.

The exact per-label list is in `Config::$customer_mail_type_vars` (verify).

## Business rules

### Server-side filtering before template rendering

When an event fires, the variables passed to the template are filtered with the platform code. So even if the calling code passes extra context (e.g., `{$secret_internal_token}`), it's **stripped before** the template engine substitutes — preventing data leakage via merchant-edited templates. The subject is filtered with the same approach against `allowed_subject_vars` (verify).

### Variable insertion path — copy-from-legend, not free-type

The editor expects the merchant to **click variables in the legend** to copy them to clipboard, then paste. Copy-pasting an unsupported code (e.g., `{$secret_internal_token}` from outside the legend) into the body **does not error at save**, but the variable will be stripped at send time — the recipient sees the literal `{$secret_internal_token}` or it's blanked, depending on the template engine (verify exact behaviour).

### `required_subject_vars` — must-have variables in the subject

Some labels declare `required_subject_vars` (e.g., `{$order_id}` on `order_status_change` subjects). The Vue editor does **NOT currently surface** a "required variable missing" warning when saving (verify). A subject missing the required variable may pass save and silently send — Gmail / Outlook may then filter such mails as suspicious (no order reference). Merchants editing order subjects should always keep `{$order_id}` in the subject.

### Magic variables (cross-channel) — see the cross-channel reference

The cross-cutting `{$shop_name}`, `{$shop_url}`, `{$logo}`, `{$customer_first_name}` family are shared across customer mails AND campaigns — see [[marketing-channels-cross-magic-vars]] for the unified glossary.

### Variables in the body use `{$variable}` syntax

The template engine syntax for substitution is `{$variable_name}` — single curly braces with dollar prefix. Inserted-by-clipboard tokens follow this format. Variable names are case-sensitive (`{$order_id}` substitutes; `{$Order_ID}` does not) (verify).

### The legend list is fetched fresh per modal-open

`GET /admin/api/core/marketing/customer-mails/{id}/variables` runs on every modal open. Adding a variable to a label's `allowed_vars` server-side is reflected immediately to merchants without a Vue rebuild — the Vue component is label-agnostic.

## Related

- [[marketing-omnichannel-mails-list]] — hub.
- [[omnichannel-mails-labels]] — each label's allow-list scope.
- [[omnichannel-mails-editor-modal]] — the variables legend lives in the editor.
- [[omnichannel-mails-abandoned-cart]] — uses `{$link}` (restore-cart URL).
- [[marketing-channels-cross-magic-vars]] — shared variables across customer mails + campaign channels.
- [[email-template]] — Email template entity.

## Open questions

- 📡 **Save-time validation of `required_subject_vars`.** Whether the Vue editor adds a save-blocking warning when a required variable is missing (verify roadmap).
- 📡 **Behaviour of unallowed variables at render time.** Whether the template engine drops, blanks, or leaves raw `{$unallowed}` codes (verify with a template-engine test).
