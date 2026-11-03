---
type: feature
nav_path: "Apps → Withdraw from contract → Compliance"
route_name: ""
route_path: ""
aliases: ["Aftercare compliance", "Right of withdrawal EU", "Directive 2023/2673", "Directive 2011/83/EU", "Article 11a", "Article 9 withdrawal", "14-day cooling-off", "withdrawal window", "cooling-off period", "terms snapshot", "durable medium acknowledgement", "withdrawal exemptions", "window starts on delivery"]
tags: [apps, aftercare, compliance, eu, withdrawal, legal]
plan_gates: []
created: 2026-07-24
updated: 2026-07-24
source_count: 1
---

> Part of [[apps-aftercare]]. See the hub for the other aspects (admin inbox, settings, free-vs-Pro, storefront flow).

# Aftercare — EU compliance basis

## Purpose

Why the [[apps-aftercare|Withdraw from contract]] app exists, which laws it implements, how the withdrawal window is timed, and what evidence it captures. Two EU instruments are in play:

- **Directive (EU) 2023/2673** — in force **19 June 2026** — requires online sellers to consumers to provide an **electronic withdrawal function** (Art. 11a): a prominent, easy on-site means to declare a withdrawal, not just a downloadable form.
- **Directive 2011/83/EU (Art. 9)** — the underlying **right of withdrawal** and its **14-day cooling-off period**.

The app delivers the function (the button + form + inbox) and the record-keeping both directives expect.

## Where to find it

Compliance is not a single screen — it is the behaviour of the storefront flow ([[storefront-withdrawal]]) and the admin inbox ([[aftercare-withdrawals-admin]]). The legally-relevant settings (the window length, the Terms / Return-policy pages) live on [[aftercare-settings-setup]].

## What the merchant can do here

Compliance is automatic — there is nothing to operate on this page. What the merchant controls that *affects* compliance is elsewhere: set a window of **≥ 14 days** and designate the Terms / Return-policy pages ([[aftercare-settings-setup]]), and apply any statutory **exemption** when resolving a request ([[aftercare-withdrawals-admin]]), since the app does not refuse exempt items up front.

## Settings & fields

No settings live on this aspect. The compliance-relevant settings (`withdrawal_window_days`, `terms_page_id`, `return_policy_page_id`, and the locked-on `notify_email`) are documented on [[aftercare-settings-setup]].

## Business rules

### The withdrawal window starts on DELIVERY, not the order date

The cooling-off clock starts on **physical possession**: `window_start` is the order's **delivery date**, falling back to the dispatch / fulfilment date (for digital lines, the auto-fulfilment date). It is **null until the order ships** — before that there is no deadline yet. `window_end` = `window_start` + `withdrawal_window_days` (default / minimum **14**; the merchant may extend to 365 but never shorten below 14).

The **right to withdraw exists from the moment the contract is concluded**, so a customer may withdraw **before** delivery too (Directive 2011/83/EU Art. 9). Only the countdown waits for delivery; the withdrawal function itself is available throughout.

### Statutory exemptions are NOT modelled

The app does **not** encode the directive's exemption categories (custom-made goods, unsealed hygiene / health items, downloaded digital content, dated travel / event services, etc.). Every still-withdrawable ordered line is offered to the customer; the merchant applies any legal exemption when **processing** the request — by moving it to `cancelled` with a note, rather than the app refusing it up front. See [[aftercare-withdrawals-admin]].

### Immutable terms snapshot (proof of content)

When the customer accepts the Terms / Return-policy pages, the app stores an **immutable content snapshot** of exactly the wording they agreed to — the full accepted text, deduped by content hash in a separate snapshot store, not just a reference to the page (`terms_version`). If the merchant later edits those pages, every past request still shows the wording the customer actually saw — a defensible record viewable from the request detail.

### Acknowledgement on a durable medium

Every confirmed request emails the customer an **acknowledgement of receipt** (`aftercare_withdrawal_acknowledgement`) — the Art. 11a durable-medium confirmation. This email is **always sent** (the `notify_email` channel is locked on) and cannot be disabled. Guest access to the function is likewise **always allowed** — ownership is proven by an emailed verification code instead of a login. See [[aftercare-withdrawals-admin]] for the full set of emails.

### The audit trail

Each request records the **submission IP and user-agent**, the **timestamps** (`submitted_at`, `acknowledged_at`, `window_start` / `window_end`), the **terms version**, and an **event log** of every status change — so the merchant can evidence when and how the customer exercised the right.

## Related

- [[apps-aftercare]] — hub.
- [[storefront-withdrawal]] — the customer-facing function that captures the acceptance + snapshot.
- [[aftercare-withdrawals-admin]] — the inbox where the evidence and the emails are surfaced.
- [[aftercare-settings-setup]] — the window length + the Terms / Return-policy page settings.
- [[page]] — the CMS pages designated as the Terms / Return policy.
- [[apps-gdpr-overview]] — sibling EU-compliance app.

## Open questions

None.
