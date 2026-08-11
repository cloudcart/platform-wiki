---
type: feature
nav_path: "Payment Providers → BNP Paribas Personal Finance"
route_name: apps.bnp.settings
route_path: /admin/payment-providers/bnp
aliases: ["BNP", "BNP Paribas", "BNP Personal Finance", "Postbank PF", "PF online shop", "Bulgarian retail credit", "Bulgarian leasing"]
tags: [paymentproviders, payment-providers, bnp, bulgaria, credit, leasing, installments, postbank, ecom]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# BNP Paribas Personal Finance

## Purpose

**BNP Paribas Personal Finance** (operated in Bulgaria through Postbank's `the provider's support address` channel) is a **retail credit / consumer-leasing provider** — not a card gateway. When a customer picks BNP at checkout, instead of charging a card the merchant submits a financing request to BNP, who underwrites the customer and issues a leasing / installment loan for the order. The customer pays BNP back in monthly installments; the merchant is paid by BNP (typically after delivery).

The integration is **Bulgarian-market-only** — BNP Paribas Personal Finance in Bulgaria uses BGN, all customer-facing copy is Bulgarian, and the financing terms map to Bulgarian leasing regulations.

This page is the **hub** for BNP. It covers what the merchant lands on (the provider overview + settings panel) and links out to the aspect pages that document the credit flow, the full settings/validation surface, product eligibility + promotions, and how BNP compares to the other Bulgarian consumer-credit providers.

## Where to find it

Sidebar → **Payment Providers** → click **BNP Paribas Personal Finance**.

The route is `/admin/payment-providers/bnp`. The internal provider key is `bnp`. The settings panel is rendered by the shared `SettingsFormPayments` Vue component. Additional promo / scheme configuration lives at the linked promo page (`route('admin.bnp.promo')`) — see [[bnp-eligibility-promotions]].

## What the merchant can do here

- **Install / Uninstall** the BNP payment method.
- **Toggle Active** on / off in the header.
- **Enter the credentials Postbank issues** — Merchant Code, POS ID, optional POS ID 2, contact email. See [[bnp-settings-fields]].
- **Choose the underwriting flow** — legacy email-request flow or the newer eCom API flow (`ecom_enabled`). See [[bnp-credit-flow]].
- **Set the minimum order price** below which BNP is hidden from checkout (default 75 BGN). See [[bnp-eligibility-promotions]].
- **Manage promotional financing schemes** and tag products / categories with their BNP type ID. See [[bnp-eligibility-promotions]].

## Settings & fields

This hub exposes the standard payment-provider controls (Logo / Title / Description, Min / Max amount, Discount). The full BNP-specific field list, the per-field validation table, the live-only UI layout, and the "no actual test mode" behaviour are documented on the aspect page:

| Area | Where it is documented |
|------|------------------------|
| Credentials (Merchant Code, POS ID, POS ID 2, email) | [[bnp-settings-fields]] |
| eCom API toggle + client ID / secret / certificate / password | [[bnp-settings-fields]] |
| `send_email_after_checkout` switch | [[bnp-settings-fields]] |
| Minimum order price + product / category eligibility | [[bnp-eligibility-promotions]] |
| Promotional financing schemes | [[bnp-eligibility-promotions]] |

## Business rules

- **BNP is a credit-application flow, not a charge.** At order placement CloudCart creates a pending-credit Payment row and either emails Postbank or calls BNP's eCom API; the order stays pre-completion until BNP confirms underwriting. Full flow + eCom error handling + certificate handling + storefront terms: [[bnp-credit-flow]].
- **Two parallel underwriting flows** — legacy email-request and the newer eCom API. The email path also fires as a record-keeping copy when `send_email_after_checkout` is on. See [[bnp-credit-flow]].
- **Minimum order price + two POS IDs.** BNP only applies above a configurable minimum (default 75 BGN) and routes BNP-branded-card schemes through a separate POS ID. See [[bnp-eligibility-promotions]].
- **Live-only configuration.** Despite a backend test-mode validator, the runtime hard-forces live mode and the Vue form renders only live cards. See [[bnp-settings-fields]].
- **Credit-payment grouping.** BNP is a `credit`-group payment type (not `regular`), reflected in the order's `order-payment-color-credit` class and storefront grouping. See [[bnp-market-positioning]].

## Sub-pages (in this cluster)

This provider is split into 4 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[bnp-credit-flow]] — the customer credit-application flow (email-request vs eCom API), order-placement steps, eCom failure short-circuit, certificate handling, and the email-mode storefront terms-acceptance links.
- [[bnp-settings-fields]] — the full settings field list, per-field validation messages, the live-only UI layout (no test card), and the "no actual test mode" hard-force.
- [[bnp-eligibility-promotions]] — minimum order price, the two-POS-ID routing for BNP cards, and the promo page (good categories / good types / financing schemes + `bnp_type_id` product tagging).
- [[bnp-market-positioning]] — why CloudCart ships three Bulgarian consumer-credit providers, how BNP compares to Fibank / DSK / UCF, and the credit-group plan-tier positioning.

## Related

- [[payment-providers]] — parent hub.
- [[bnp-credit-flow]] — credit-application flow, email vs eCom, error handling, certificate, terms.
- [[bnp-settings-fields]] — settings fields, validation, live-only UI, no-test-mode.
- [[bnp-eligibility-promotions]] — minimum price, two POS IDs, promo schemes, product tagging.
- [[bnp-market-positioning]] — Bulgarian-credit positioning vs Fibank / DSK / UCF, credit grouping.
- [[settings-payment-providers]] — global list where BNP is installed / uninstalled.
- [[payment-providers-fibank-bnpl]] — similar Bulgarian-market consumer credit (Fibank, BNPL flavour).
- [[payment-providers-dsk-bnpl]] — similar Bulgarian-market consumer credit (DSK).
- [[payment-providers-smart-ucf]] — UniCredit Bulbank-affiliated credit provider (UCF).
- [[payment-provider]] — entity definition.
- [[payment-status]] — credit-flow status mapping.
- [[checkout-flow]] — concept page on the storefront checkout.

## Open questions

- ⏸️ Exact enum of `Status` values BNP returns in the eCom protocol — passed through to `payment.status` unmodified. The authoritative list lives in BNP / Postbank's own eCom protocol docs, not in CloudCart. See [[bnp-credit-flow]].
