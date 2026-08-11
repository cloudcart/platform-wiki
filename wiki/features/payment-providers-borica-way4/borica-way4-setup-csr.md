---
type: feature
nav_path: "Payment Providers → Borica Way4 → Setup & CSR"
route_name: apps.borica_way4.overview
route_path: /admin/payment-providers/borica_way4
aliases: ["Borica CSR generation", "Borica certificate upload", "Borica Terminal ID", "Borica V1800001", "Borica test terminal", "Borica certificate"]
tags: [paymentproviders, payment-providers, borica-way4, csr, certificate, onboarding]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-borica-way4]]. See the hub for related aspects (settings fields, payment lifecycle, authorize/capture, save card, refund/sync).

# Borica Way4 — Setup & CSR

## Purpose

This aspect documents how a Bulgarian merchant goes from "I have a Borica e-commerce contract" to "my Borica Way4 terminal is fully signed and validated in CloudCart". The flow is: enter the Borica-issued **Terminal ID**, generate a **CSR (Certificate Signing Request)** server-side, download the CSR + email it to Borica, then upload the signed `.zip` certificates Borica returns. There is also a shared CloudCart test terminal `V1800001` for trial accounts that short-circuits the whole certificate dance.

## Where to find it

Sidebar → **Payment Providers** → click **Borica Way4** ("Pay with card"). Route: `/admin/payment-providers/borica_way4`. While no Terminal ID has been entered the page renders the **"Invalid"** onboarding state described below.

## What the merchant can do here

- **Enter the Borica-issued Terminal ID** and trigger CSR generation.
- **Download the test + live CSR files** (one click generates both).
- **Download the public certificate** (`.pem`) and the **P12 bundle** (PKCS#12) for backup.
- **Upload the test `.zip` archive** Borica returns into the **Test certificate** field.
- **Upload the live `.zip` archive** Borica returns into the **Live certificate** field.
- **Use the bundled test terminal `V1800001`** for trial transactions without any contract.

## Settings & fields

### Phase 1 — Invalid state (no Terminal ID yet)

The screen renders a single onboarding card titled *"Generating a Certificate Signing Request (CSR)"* with explanatory text *"Generate a certificate to configure the payment settings."*

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Terminal ID** | Borica-issued terminal identifier (e.g., `V1900145`). | Empty | Required, latin letters + digits. Special test terminal `V1800001` is pre-configured by the platform and works without uploading anything. |
| **Generate CSR** button | Generates an RSA private key + CSR for both test and live, server-side, signed for `OU=<terminal_id>` and `CN=<site host>`. | — | Posts to `/admin/api/payment_providers/borica_way4/csr/generate`. Disabled while `terminal_id` is empty. On error returns *"Invalid terminal ID"*. |

Submitting POSTs the terminal ID. On success the page emits `update:isValid=true` and re-renders into Phase 2. On error the input shows *"Invalid terminal ID"*. The standard rows (logo, mode, amount, discount, description, auth) render above this onboarding card.

### Phase 2 — Valid state (certificate management UI)

Once the CSR is generated, the **Borica Way4 environment** card (always-expanded `panel` edit method) renders these certificate-related controls:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Terminal ID** display | Read-only header `Terminal ID: <id>` followed by a horizontal line. | — | Once saved, immutable in the UI — to change it, uninstall and reinstall the provider. `(verify)` |
| **Download Test CSR** button | Downloads the CSR for the **test** environment. | — | Link to `/admin/api/payment_providers/borica_way4/csr/download/test`. Filename pattern `<terminal>_<YYYYMMDD>_D.csr`. |
| **Download Live CSR** button | Downloads the CSR for the **live** environment. | — | Link to `/admin/api/payment_providers/borica_way4/csr/download/real`. Filename pattern `<terminal>_<YYYYMMDD>_P.csr`. |
| **Download Public Cert** button | Downloads the public certificate generated from the CSR (`.pem`). | — | For sending to Borica with the contract. |
| **Download P12** button | Downloads the bundled key-pair in PKCS#12 format. | — | Backup format. |
| **Test certificate** file upload | Upload the `.zip` archive Borica returned for the **test** environment. | Empty | Must be a valid ZIP containing a `.cer` file. The platform extracts it, validates against the test private key, and stores. Error: *"Borica: test private key and certificate do not match"* if mismatched. |
| **Live certificate** file upload | Upload the `.zip` archive Borica returned for the **live** environment. | Empty | Same validation against the live private key. Error: *"Borica: real private key and certificate do not match"*. Required to switch to live mode. |
| **ViewJSON** (collapsible) | Decoded certificate viewer — Issuer, Subject, Valid From/To, Fingerprint. | Collapsed | Read-only inspection of the uploaded `.cer`. |

The certificate upload row visible at any moment depends on the active **Mode** radio (`Test` vs `Live`) via `dependField: configuration.mode`.

## Business rules

### CSR fixed organisation metadata (not merchant-editable)

The CSR is generated server-side with fixed organisation fields that the merchant cannot customise:

```
O = CloudCart AD
ST = Sofia
L = Sofia
emailAddress = support@cloudcart.com
OU = <terminal_id from merchant>
CN = <store primary host>
```

Two CSRs are generated in one call — one for test (`_D.csr` suffix) and one for live (`_P.csr` suffix). Each download link is environment-aware.

### Per-merchant key material — not shared

The merchant's own RSA private key + Borica-signed public certificate are generated and stored per-store. CloudCart never ships a shared per-merchant key for Borica Way4. (Contrast with Raiffeisen, which historically uses a CloudCart-wide bundled key — `(verify)`.)

### Per-environment files — separate test + live keys

Separate test and live private keys + certificates are stored. Test mode uses Borica's `MPI_OW_APGW_D_2026.cer` gateway certificate; live mode uses `MPI_OW_APGW_P_2026.cer`. These gateway certificates ship bundled with CloudCart and are rotated by year — a CloudCart release replaces them when Borica rotates.

### Special test terminal V1800001

The platform ships a fully-working **shared test terminal** with terminal ID `V1800001` and its private key bundled with CloudCart. When the merchant enters `V1800001`:

- The platform short-circuits the CSR / certificate flow entirely — no CSR generation, no certificate upload, just test mode.
- Activation in live mode is also allowed without a live certificate (the live-mode block in [[borica-way4-settings-fields]] makes a single exception for `V1800001`).
- Useful for trial accounts that want to see the gateway in action before signing a real contract with Borica.

### Cannot activate live without valid certificates

The activation switch is checked server-side. It refuses to flip the live activity flag when:
- The current mode is `live` AND
- No live certificate has been uploaded AND
- The terminal ID is **not** the bundled `V1800001`.

Error text shown to the merchant: *"Borica: cannot change to live mode if not all certificates are validated"* / Bulgarian: *"Borica: не можете да преминете към реален режим, ако всички сертификати не са валидни"*.

### Certificate-key mismatch detection

On upload, the platform extracts the `.cer` from the `.zip` and validates that its public key matches the previously generated private key for that environment. Mismatch triggers explicit errors (verbatim strings):

- Test: *"Borica: test private key and certificate do not match"*.
- Live: *"Borica: real private key and certificate do not match"*.

## Related

- [[payment-providers-borica-way4]] — hub.
- [[borica-way4-settings-fields]] — the rest of the fields on the same screen (MID, security, currency, wallets, save card).
- [[borica-way4-payment-lifecycle]] — what happens on the wire once setup is complete.
- [[settings-payment-providers]] — global payment-providers list where Borica Way4 is installed.

## Open questions

(none)
