---
type: feature
nav_path: "Products → Add product → Digital product"
route_name: products-edit.new
route_path: /admin/products-new/edit/:id
aliases: ["Digital product", "Downloadable product", "Downloadable files", "Sell files", "Digital download", "Landing pages product", "Дигитален продукт", "Сваляем продукт", "Продажба на файлове"]
tags: [products, digital, downloadable, membership, product-type]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 2
---
# Digital products (downloadable files & landing pages)

## Purpose

A **digital product** is sold and delivered **without shipping** — either a **downloadable file** (e-book, PDF, images, audio) the customer downloads after purchase, or a **landing page** that grants access to gated / exclusive content. The merchant picks **Digital product** as the product type when adding a product; the platform then removes shipping and delivers the file or page access instead of a parcel. For the cross-cutting model + delivery mechanics, see [[digital-products]].

## Where to find it

**Products → Add product** (the "Create product" popup) → choose **Digital product**, which expands into two sub-options:

- **Downloadable files** — *"E-book, PDF, images, audio files etc."* — native, no app required.
- **Landing pages** — *"Access to specified pages and exclusive content"*, marked **Extended**. This mode requires the **[[apps-membership|Membership]]** app (app key `subscriptions`); without it, the platform prompts the merchant to install it first.

After creation the merchant lands in the product editor ([[products-editor]]), where a downloadable product's files are managed in the **Files** section.

## What the merchant can do here

- Create a **Downloadable files** product and attach the file(s) the customer receives after purchase (the files surface on the product page).
- Create a **Landing pages** product (Membership app) that grants access to gated content Pages — the basis for [[apps-membership|membership tiers]].
- Set price, name, category, SEO, and images exactly like any product — only shipping is removed.

## Settings & fields

| Field / control | What it does | Notes |
|---|---|---|
| **Product type = Digital product** | Marks the product non-physical (`digital = yes`). | Chosen at creation; pick one of the two modes below. |
| **Downloadable files** (mode) | Sets `type_digital = file`. | The native digital mode. |
| **Landing pages** (mode) | Sets `type_digital = page`. | Requires the [[apps-membership]] app; used for membership tiers linked to Pages with a validity period. |
| **Files** (product-editor section) | Attach the downloadable file(s) for the product. | Files appear on the product page and are delivered after purchase. (verify exact upload limits / accepted types — the modern Files section is still being built out.) |
| **Shipping** | Disabled for digital products. | No weight, no courier waybill — shipping controls are read-only / skipped. |

## Business rules

- **No shipping step.** A digital product carries no weight and generates no waybill; a digital-only cart skips shipping at [[checkout-flow]]. A mixed cart (physical + digital) still ships its physical items.
- **Delivery after purchase.** Downloadable files are served through a **signed, order-scoped download link** rather than a public URL — the headless storefront exposes a signed `/api/sf/downloads/{id}` endpoint (see [[headless-storefront-api]]).
- **Landing pages = Membership.** The **page** mode is not a standalone feature — it is the [[apps-membership]] integration. A "membership tier" is just a differently-priced digital `page` product linked to gated content Pages with a validity period; installing the Membership app (`subscriptions`) is what surfaces the Landing-pages option.
- **Type is set at creation.** `digital` / `type_digital` are decided when the product is created — see [[product-entity-attributes]] for the stored flags.

## Related

- [[digital-products]] — the cross-cutting concept (file vs page, delivery model).
- [[apps-membership]] — the app behind the Landing-pages (page) mode + membership tiers.
- [[products-editor]] — the product editor that hosts the Files section.
- [[product-entity-attributes]] — the `digital` / `type_digital` fields.
- [[checkout-flow]] — how a digital-only order skips shipping.
- [[headless-storefront-api]] — the signed download endpoint.

## Open questions

- Exact file-upload limits, accepted file types, and per-file download caps / expiry for the Downloadable-files mode (verify — the modern Vue Files section is still being built out).
- Whether a single product can mix file + page delivery, or whether the two modes are mutually exclusive (verify).
