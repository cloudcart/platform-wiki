---
type: feature
nav_path: "Settings → Domains → SSL → Troubleshooting"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["SSL errors", "SSL troubleshooting", "Invalid certificate applied", "SSL ERROR banner", "renew_error messages", "Self-signed certificates not supported"]
tags: [settings, ssl, certificate, errors, validation, troubleshooting]
plan_gates: ["ssl_certificate"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-ssl]]. See the hub for the other aspects (automatic install, manual install, auto-renewal, expiry fallback, edge propagation).

# SSL — Validation errors and SSL ERROR banner reference

## Purpose

A reference catalogue of every error string the SSL modal can show — both **form-validation errors** raised at install time (Manual install) and **`renew_error` banner messages** raised by the daily renewal sweep ([[settings-ssl-auto-renewal]]). The strings are verbatim — support agents and merchants should grep this page for an exact match when diagnosing a ticket.

## Where to find it

Inside the SSL Modal (Sidebar → Settings → **Domains** → SSL action on a domain row):

- **Form-validation errors** — shown inline on the field that failed, or as a top-level error toast after submission. Most fire on the Manual install **Install** click.
- **SSL ERROR banner** — red panel in the Manage-existing-certificate state. Renders the cert's `renew_error` text verbatim.

## What the merchant can do here

### Form-validation errors during Manual install

These fire BEFORE the cert is stored, so the merchant can correct and retry without state cleanup.

| Trigger | Exact message |
|---------|---------------|
| Missing organization | "Invalid organization" |
| Missing country | "Country is invalid" |
| Missing/invalid email | "Email is invalid" |
| Missing locality | "The locality field is required." |
| Missing state | "State required" |
| Bad cert paste / unparseable PEM | "Invalid certificate applied" |
| Cert already exists at install | "An existing certificate was found, please remove it and try again!" |
| No cert at modify | "Certificate was not found!" |
| Generic confirm dialog | "Are you sure?" |

For Domain-details validation: re-fill the missing/invalid field and retry **Manual install**.

For the cert-paste errors: see the cryptographic-validation rules below.

### Cryptographic validation errors at Manual install

The Install endpoint does **strict cryptographic validation** of the pasted certificate beyond just parsing. The CSR, private key, certificate, and chain must all be a matched set. Each rule and its verbatim error:

| Rule | Verbatim error string |
|------|------------------------|
| Private key's modulus must equal the CSR's public-key modulus | *"The CSR and private key do not match."* |
| Certificate's public-key modulus must equal the private key's modulus | *"The private key and certificate do not match."* |
| Certificate's `subject.CN` must contain (or be contained by) the domain | *"Invalid certificate applied. {expected} != {actual}"* |
| Certificate must NOT be self-signed (`subject == issuer`) | *"Self-signed certificates are not supported."* |
| CA bundle must parse as a valid x509 | *"Invalid CA certificate/bundle applied."* |

Common fix when *"Invalid certificate applied"* or *"Invalid CA certificate/bundle applied"* fires: the merchant pasted both the end-entity cert and the chain into ONE field. Re-paste with:

- **Certificate** textarea — end-entity cert only.
- **Paste your Chained Certificate here** textarea — chain alone.

See [[settings-ssl-manual-install]] for the full flow.

### Renewal errors (SSL ERROR banner)

In the Manage-existing-certificate state, a red banner with *"SSL ERROR: {error}"* appears whenever the cert's `renew_error` field is non-null. The verbatim messages the merchant may see:

| Trigger | Exact message |
|---------|---------------|
| Pre-renewal HTTP check can't find CloudCart header on apex OR `www.` | *"Header x-powered-by not found for domain X"* |
| Let's Encrypt Manager app subscription has lapsed | *"Renew error: no active subscription"* |
| ACME transient errors (timeout, rate-limit, verification failure) | Various ACME-protocol error texts — typically transient. The sweep retries daily. |

Fixes:

- *"Header x-powered-by not found for domain X"* → DNS isn't pointing at CloudCart. Fix DNS in [[settings-domains]] and re-attempt the install via [[settings-ssl-automatic-install]] (after waiting for DNS to propagate).
- *"Renew error: no active subscription"* → Re-purchase [[apps-lets-encrypt]]. The next daily sweep will retry.
- ACME transient errors → Wait one day for the next sweep. If persistent, contact support.

The banner is cleared automatically on the next successful renewal — see [[settings-ssl-auto-renewal]].

### Issuance errors (Automatic install)

For Automatic install, errors during ACME issuance return as validation errors against the `host` field on the modal (not as a `renew_error` banner — those are reserved for the daily sweep). Specific timeout errors during verification are **NOT logged to the platform exception store** (suppressed to reduce noise). The merchant sees the ACME-side error text inline.

## Settings & fields

This aspect doesn't introduce new fields — it documents the error strings that other aspects' fields can produce. See [[settings-ssl-manual-install]] for the field layout that generates the validation errors above, and [[settings-ssl-auto-renewal]] for the `renew_error` lifecycle.

## Business rules

### Validation rules are server-side

All cryptographic validation runs server-side at Install — the merchant cannot bypass by client-side tampering. Errors are returned to the modal and surfaced as inline form errors.

### "Invalid certificate applied. {expected} != {actual}" — the CN check is bidirectional

The check is: the cert's `subject.CN` must CONTAIN, or BE CONTAINED BY, the domain the merchant is installing for. Concretely:

- Installing for `shop.example.com` with a cert for `shop.example.com` — passes.
- Installing for `shop.example.com` with a wildcard cert `*.example.com` — passes (wildcard contains the domain).
- Installing for `example.com` with a cert for `shop.example.com` — fails.

The verbatim error includes both the expected (the domain) and the actual (the cert's CN) so the merchant can see the mismatch.

### Self-signed cert rejection — leaf only, not the chain

The validator parses the cert and checks `subject == issuer` — if true, it's self-signed and rejected. **The chain itself is not separately checked for self-signing**; only the leaf cert. So a chain that contains a self-signed root (which is normal — root CAs ARE self-signed) is fine, as long as the leaf isn't self-signed.

### Renewal errors are transient by nature

The `renew_error` text is just the most recent error from the daily sweep. The sweep retries daily; a transient ACME failure today clears tomorrow on a successful renewal. The banner is NOT a permanent state — it disappears the moment the next sweep succeeds. Merchants who fix DNS or app-subscription issues should check back the next day.

### `(verify)` items

- *"An existing certificate was found, please remove it and try again!"* — exact triggers between the Automatic and Manual install endpoints `(verify)` whether identical.
- ACME-protocol error catalogue — the exact set of strings depends on Let's Encrypt's responses; the modal surfaces them verbatim but is not enumerable.

## Related

- [[settings-ssl]] — hub.
- [[settings-ssl-manual-install]] — the flow that generates the form-validation errors above.
- [[settings-ssl-auto-renewal]] — the sweep that sets and clears `renew_error`.
- [[settings-ssl-automatic-install]] — issuance-time error handling.
- [[settings-domains]] — where DNS is configured (root cause of *"Header x-powered-by not found"* errors).
- [[apps-lets-encrypt]] — re-purchase path for *"Renew error: no active subscription"*.

## Open questions

- Is the *"An existing certificate was found, please remove it and try again!"* error fired identically by both the Automatic and the Manual install endpoints, or scoped to one? `(verify)`
- Are any of the ACME-protocol error strings normalised before surfacing to the merchant, or is the verbatim Let's Encrypt response always shown? `(verify)`
