---
type: entity
nav_path: "Entity → Credit Note → External providers"
aliases: ["External Credit Note providers", "Szamlazz credit note", "FGO credit note", "SmartBill credit note", "FlixFacts credit note", "Gensoft credit note", "ERP credit note", "External Invoicing App"]
tags: [entity, finance, invoicing, refund, credit-note, integrations, erp]
created: 2026-06-10
updated: 2026-08-06
source_count: 0
---

> Part of [[credit-note]]. See the hub for the other aspects (attributes, lifecycle, numbering, send flow, template rendering).

# Credit Note — External providers

## Identity

This page documents **how Credit Note issuance changes when an external accounting App is the active Invoicing provider**. Only an App that actually takes over invoicing does this — **Szamlazz** is the documented case: activating it makes it the store's Invoicing provider, and CloudCart's own invoicing switch is then locked out ([[settings-invoicing-activation-modes]]). When active, the external system assigns the Credit Note number, stores the document on its side, and reports back a reference. CloudCart's own number formatting (per [[credit-note-numbering]]) is **bypassed** and its internal series is not advanced, so the merchant manages most of the Credit Note's audit trail in the external system's UI.

Other accounting Apps (**Gensoft**, **SmartBill**, **FlixFacts**, **FGO**) do **not** take invoicing over. CloudCart keeps issuing its own documents; each of those Apps has its own settings screen and its own sync behaviour. Gensoft additionally supplies invoice **numbers** when the store is in external numbering mode — see [[settings-invoicing-external-systems]].

## Aliases

- **External Invoicing provider** — an App that replaces platform invoicing (Szamlazz).
- **ERP credit note** — informal merchant phrasing when the external system is an ERP.
- **Sub-provider** — when the App contains multiple invoicing engines.

## Key Attributes

| Provider | Role | Where the Credit Note lives | Number source | Partial-credit support |
|----------|------|----------------------------|---------------|------------------------|
| **Szamlazz** | Replaces platform invoicing | Szamlazz online | Szamlazz sequence | Full reversal always; partial (corrective invoice) depends on the account — verify |
| **Gensoft** | Supplies invoice numbers only | CloudCart | CloudCart credit-note series | Same as platform |
| **SmartBill** / **FlixFacts** / **FGO** | Own settings screen; do not take invoicing over | CloudCart | CloudCart credit-note series | Same as platform |
| (none) | CloudCart built-in | Re-rendered on the fly | CloudCart credit-note series | Whole-order note, plus one per credited return |

## How activation changes the flow

When an App that replaces invoicing is the active provider:

1. **Eligibility check** is delegated to the App — the App reports whether the Order qualifies for a Credit Note. Provider-specific rules may apply (e.g., the original invoice must be at least X days old) — see [[credit-note-lifecycle]] for the typical eligibility shape.
2. **Issuance** makes an API call to the external system. The external system:
   - Assigns the Credit Note number from its own sequence.
   - Stores the Credit Note document on its side.
   - Returns a reference (ID, URL, or document identifier) to the platform.
3. **The platform records which provider issued the note**, together with the external number and date, for reconciliation. CloudCart's own credit-note series is left untouched — external numbers are kept apart from it.
4. **Failures bubble back** as errors with the *"Could not create credit note"* toast on [[orders-credit]]. API-down, invalid order state, and external-rule violations all surface through this same path.
5. **The merchant's primary audit surface is the external system**, not CloudCart. To search, filter, or download Credit Notes in bulk, the merchant uses the external system's UI.

## External Apps assign their own numbers

When the active Invoicing provider is an external accounting App, the **Issue** action makes an API call to the external system. The external system assigns the number AND stores the Credit Note there; the platform stores a reference for reconciliation.

This means:

- CloudCart's own credit-note prefix / padding / suffix settings on [[settings-invoicing]] are **bypassed** when an external provider is active.
- The merchant cannot control the Credit Note number format from CloudCart — they configure it in the external system.
- The Credit Note may also be visible in the external system's own admin UI, with its own document history, sequence audit, and re-print options.

## Partial Credit Notes via external Apps

CloudCart's own Invoicing layer **does** support partial Credit Notes — through returns ([[orders-returns-lifecycle]]). An external provider may not: a full reversal (storno) is always available, but issuing a **partial** note requires the provider to support a corrective document, and CloudCart falls back to "not issued" when it cannot. Szamlazz's corrective-invoice path is the documented case.

Verify per active provider — the partial-Credit-Note behaviour is App-specific and may also depend on the merchant's contract with the external system.

## Configuration touchpoints per provider

Each external Invoicing App has its own settings sub-screen, typically under Apps → (provider name) → Settings. Examples documented in the wiki:

- [[apps-szamlazz]] — main Szamlazz App settings.
- [[apps-szamlazz-orders-credit-note]] — the Szamlazz per-order Credit Note action surface.
- [[apps-fgo-settings]] — FGO App settings.

A replacement provider is activated by installing and enabling its App (which sets the store's invoicing provider), then configuring the App-specific credentials (API key, account number, default series) on the App's own sub-screen. It is not selected from the **External system** dropdown on [[settings-invoicing]] — that dropdown only picks the invoice-number source.

## Reference field visibility

When the active provider is an external App, the **external system's Credit Note ID** is stored as a reference on the Order. Visibility of this reference in the merchant UI varies:

- May appear on [[orders-details]] near the **View credit note** dropdown.
- May appear on the rendered PDF.
- May only be visible in the external system itself.

This is a known open question — see "Open Questions" below.

## Mid-issuance failure handling

When the API call to the external system fails after the platform has begun the issuance flow:

- The toast surfaces as *"Could not create credit note"*.
- No credit-note number gets stamped on the Order or the return — a failed issuance consumes nothing.
- The external system may or may not have created a partial document — the merchant should verify in the external UI before retrying.
- Retrying the **Create credit note** action is safe in most cases; some Apps may treat a retry as a new document.

## Where it appears

- [[settings-invoicing]] — invoicing configuration; note the **External system** dropdown there picks the invoice-*number* source, not the provider.
- [[settings-invoicing-external-systems]] — the dedicated external-systems configuration sub-page.
- [[apps-szamlazz]] — Szamlazz App settings.
- [[apps-szamlazz-orders-credit-note]] — the Szamlazz per-order Credit Note action when active.
- [[apps-fgo-settings]] — FGO App settings.
- [[orders-credit]] — the per-order Credit Note flow that delegates to the active provider.

## Related

- [[credit-note]] — hub.
- [[settings-invoicing-activation-modes]] — the provider mutex that locks platform invoicing out.
- [[orders-returns-lifecycle]] — the platform's own partial-Credit-Note path.
- [[settings-invoicing]] — provider activation + per-App configuration.
- [[settings-invoicing-external-systems]] — the dedicated external-systems configuration sub-page.
- [[apps-szamlazz]] — Szamlazz external accounting App.
- [[apps-szamlazz-orders-credit-note]] — Szamlazz's per-order Credit Note action.
- [[apps-fgo-settings]] — FGO external accounting App.
- [[invoice]] — sibling document subject to the same external-provider delegation.

## Open Questions

- Pending: **External-system reference visibility** — when the active provider is an external App, where does the merchant see the external system's Credit Note ID? On the Order detail, on the PDF, or only in the external system itself?
- Pending: **Partial Credit Notes via external Apps** — verify per active provider (Szamlazz, FGO, SmartBill, FlixFacts) whether the App allows multiple staged Credit Notes against the same Invoice, or whether one-per-Order is platform-wide.
