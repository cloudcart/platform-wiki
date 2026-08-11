---
type: feature
nav_path: "Settings → Domains → SSL → Manual install"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Manual SSL install", "External SSL", "Paste SSL certificate", "CSR generation", "Upload SSL"]
tags: [settings, ssl, certificate, csr, manual]
plan_gates: ["ssl_certificate"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-ssl]]. See the hub for the other aspects (automatic install, auto-renewal, expiry fallback, edge propagation, troubleshooting).

# SSL — Manual install (external provider)

## Purpose

The **Manual install** tab of the SSL Modal is for merchants who already have (or want to buy) an SSL certificate from an **external CA** — Comodo, DigiCert, GoDaddy SSL, Sectigo, etc. The flow is two-step: (1) fill in Domain details so the platform can generate a CSR + private key on the server, (2) take the CSR to the external CA, receive the signed cert + chain, paste them back into this modal.

Use this tab when the merchant prefers a paid commercial cert (extended-validation badges, organisation-validated branding) or specifically must NOT use Let's Encrypt — otherwise [[settings-ssl-automatic-install]] is simpler.

## Where to find it

Sidebar → Settings → **Domains** → SSL action on a domain row → **Manual install** tab.

The tab is only available when no certificate is already installed on the domain. If a Let's Encrypt cert exists, the merchant must remove it before starting the Manual install flow.

## What the merchant can do here

### Step 1 — Fill in Domain details and generate the CSR

Fill in the **Domain details** form (see field table below; most fields pre-fill from [[settings-general]]) and click **Manual install** to generate the CSR + private key server-side.

### Step 2 — Copy the CSR and submit it to the external CA

After Manual install is clicked, a slide-down panel appears below the form with a read-only **CSR textarea** + **Copy CSR** button, a **Show private key** disclosure (expands a read-only PEM textarea), and a **My certificate is ready** action that expands the final install step.

The merchant takes the CSR to their external SSL issuer, completes the CA's domain-control verification, and receives the signed certificate (`.crt`) and a CA-Bundle (`.ca` or chain file).

### Step 3 — Paste the cert + chain and install

Paste the `.crt` content (end-entity cert, PEM) into the **Certificate** textarea and the CA-Bundle into the **Paste your Chained Certificate here** textarea, then click **Install**. The platform runs the matched-set validation (see Business rules) and activates HTTPS on the domain.

### Regenerate the CSR (before install)

After CSR generation but BEFORE install, the **Manual install** button is replaced with a white **Regenerate** button (redo icon). Clicking it opens an *"Are you sure?"* confirm warning that the previous certificate will be lost.

This is destructive — if the CSR has already been sent to the external CA, the cert the CA returns will not match the new private key.

### Remove an existing Let's Encrypt cert first (if any)

If a Let's Encrypt cert (`free=1`) is installed and the merchant wants to switch to manual, they must click **Remove** on the Manage-mode view first. The platform shows no warning in this direction (only in Manual → Automatic).

## Settings & fields

### Domain details form

| Field | What it does | Pre-filled from |
|-------|--------------|-----------------|
| **Common Name (CN)** | Domain hostname (read-only). | (read-only) |
| **Organization (O)** | Business / legal name in the CSR Subject. | Company name from [[settings-general]] |
| **Email address** | Contact email in the CSR. | Store email from [[settings-general]] |
| **Country** | Country code (searchable dropdown). | Country from [[settings-general]] |
| **Locality** | City. | City from [[settings-general]] |
| **State/District Name** | State/region. | (blank) |
| **CSR** | Read-only after generation. **Copy CSR** button. | (generated server-side) |
| **Private key** | Hidden behind **Show private key** disclosure. | (generated server-side) |
| **Certificate** textarea | Merchant pastes the `.crt` PEM content. | (input) |
| **Paste your Chained Certificate here** textarea | Merchant pastes the CA-Bundle. | (input) |

### Buttons

- **Manual install** — primary; generates the CSR + private key. Visible BEFORE generation.
- **Regenerate** — white, redo icon; replaces Manual install AFTER generation but BEFORE install. Destructive — see above.
- **Install** — primary; commits the pasted cert + chain. Visible only after **My certificate is ready** is expanded.
- **Remove** — danger styled; appears when a `free=0` cert needs to be cleared first.

## Business rules

### CSR + private key generated server-side

The CSR form defaults to the merchant's [[settings-general]] values (Organization, Email, Country, Locality), all editable per-cert if the merchant wants different legal-entity details. The platform generates the private key + CSR pair from the filled-in Domain details. The private key is stored server-side AND exposed via the **Show private key** disclosure so the merchant can save it for portability.

### Strict cryptographic validation on Install

The Install endpoint performs strict matched-set validation: the **CSR**, the **private key**, the **certificate**, and the **chain** must all be cryptographically aligned. Mismatches return verbatim error strings like *"The CSR and private key do not match."*, *"The private key and certificate do not match."*, *"Invalid certificate applied. {expected} != {actual}"*, *"Self-signed certificates are not supported."*, and *"Invalid CA certificate/bundle applied."* — the full catalogue is in [[settings-ssl-troubleshooting]].

Practical implication: paste the **end-entity cert** (not the chain) into the **Certificate** field and the **chain alone** into the **Chained Certificate** field. A common error is pasting both into one field; this returns one of the validation errors above.

### Pasting parses three new tracking fields

When the cert is committed, the platform parses it and stores `validTo` on the cert record (used by [[settings-ssl-auto-renewal]] for the expiry display, even though manual certs don't auto-renew). The pasted CSR, private key, and chain are also stored verbatim. The platform flags `pending=1` and `gcloud_pending=1` to signal the cert needs propagating to the edge — see [[settings-ssl-edge-propagation]].

### After install, the cert is marked `free=0`

The Manual install endpoint sets `free=0` on the cert record — this is the platform's marker that "this is an external cert and should NOT be picked up by the Let's Encrypt renewal sweep". The Manage-mode view then shows the purple **Manual** renewal badge plus the *"Managed by external provider. You should change it manually before the expiration date."* label.

### OU (Organizational Unit) not exposed in the form

The Manual-install form does NOT expose an OU (`organizationalUnitName`) input, so the OU stays blank on certs generated here. Merchants migrating a cert that included an OU should know re-issuing here drops it. Rarely matters; compliance audits may flag the difference. `(verify)`

### Manual certs do not auto-renew

External certs do NOT participate in the daily Let's Encrypt sweep ([[settings-ssl-auto-renewal]]). Before expiry the merchant must obtain a renewed cert from the external CA, Remove the old cert, and re-run this flow. Forgetting triggers the automatic fallback — see [[settings-ssl-expiry-fallback]].

## Related

- [[settings-ssl]] — hub.
- [[settings-general]] — provides the CSR field defaults (Organization, Email, Country, Locality).
- [[settings-domains]] — DNS must be valid for the external CA to complete domain-control verification.
- [[settings-ssl-troubleshooting]] — full catalogue of the validation error strings emitted on Install.

## Open questions

- Is there any admin / support path to set the OU (`organizationalUnitName`) on a generated CSR without code changes? `(verify)`
