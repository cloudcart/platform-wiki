---
type: feature
nav_path: "Settings → Domains → SSL → Manual install"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Manual SSL install", "External SSL", "Paste SSL certificate", "CSR generation", "Upload SSL", "Replace SSL certificate", "Renew external SSL", "Own private key"]
tags: [settings, ssl, certificate, csr, manual]
plan_gates: ["ssl_certificate"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[settings-ssl]]. See the hub for the other aspects (automatic install, auto-renewal, expiry fallback, edge propagation, troubleshooting).

# SSL — Manual install (external provider)

## Purpose

The **Manual install** tab of the SSL Modal is for a certificate from an **external CA** (Comodo, DigiCert, GoDaddy SSL, Sectigo, etc.). Either the platform generates a CSR + private key that the merchant takes to the CA, or the merchant pastes the key (and CSR) of a certificate they already obtained elsewhere; then they paste the signed certificate + chain. [[settings-ssl-automatic-install]] is simpler when a paid certificate is not required.

## Where to find it

Sidebar → Settings → **Domains** → SSL action on a domain row → **Manual install** tab.

The install tabs work only on a domain with **no certificate**: an installed one (Let's Encrypt or external) shows its details with only **Remove**, so replacing means removing first (see Business rules).

## What the merchant can do here

### Step 1 — Fill in Domain details and generate the CSR

Fill in the **Domain details** form (see field table below; most fields pre-fill from [[settings-general]]) and click **Manual install** to generate the CSR + private key server-side.

### Step 2 — Copy the CSR and submit it to the external CA

After **Manual install** a panel shows the **CSR** box with **Copy CSR**, a **Show private key** disclosure with the **Private key** box (both boxes editable), and **My certificate is ready**. The merchant takes the CSR to the CA, completes its domain-control check, and receives the certificate (`.crt`) and CA-Bundle.

### Step 3 — Paste the cert + chain and install

Paste the `.crt` content (end-entity cert, PEM) into the **Certificate** textarea and the CA-Bundle into the **Paste your Chained Certificate here** textarea, then click **Install**. The platform runs the matched-set validation (see Business rules) and activates HTTPS on the domain.

### Regenerate the CSR (before install)

After generation, **Manual install** becomes **Regenerate** (confirm: the previous certificate request will be lost). It builds a new CSR from the private key in the box, so a CSR already sent to the CA stops matching unless the key was kept.

### A certificate bought elsewhere (own key)

Click **Manual install** once, paste the merchant's own private key into **Private key**, then either paste the CSR that was sent to the CA or click **Regenerate** to build one from that key. **My certificate is ready** → paste certificate + chain → **Install**.

## Settings & fields

### Domain details form

| Field | What it does | Pre-filled from |
|-------|--------------|-----------------|
| **Common Name (CN)** | Domain hostname (read-only). | (read-only) |
| **Organization (O)** | Business / legal name in the CSR Subject. | Company name from [[settings-general]] |
| **Email address** | Contact email in the CSR. | Store email from [[settings-general]] |
| **Country** | Country code (searchable dropdown). | Country from [[settings-general]] |
| **Locality** | City. | City from [[settings-general]] |
| **State/District Name** | State/region; required at **Install** (*"State required"*). | (blank) |
| **CSR** | Editable; **Copy CSR** button. | (generated server-side) |
| **Private key** | Editable, behind **Show private key**. | (generated server-side) |
| **Certificate** textarea | Merchant pastes the `.crt` PEM content. | (input) |
| **Paste your Chained Certificate here** textarea | Merchant pastes the CA-Bundle. | (input) |

### Buttons

**Manual install** (generate) → **Regenerate** (after generation) → **Install** (after **My certificate is ready**); **Remove** on an installed certificate.

## Business rules

### CSR + private key generated server-side

The form defaults to the [[settings-general]] values, editable per certificate. The key is stored server-side and shown under **Show private key** so the merchant can keep it.

### Strict cryptographic validation on Install

The Install endpoint performs strict matched-set validation: the **CSR**, the **private key**, the **certificate**, and the **chain** must all be cryptographically aligned. Mismatches return verbatim error strings like *"The CSR and private key do not match."*, *"The private key and certificate do not match."*, *"Invalid certificate applied. {expected} != {actual}"*, *"Self-signed certificates are not supported."*, and *"Invalid CA certificate/bundle applied."* — the full catalogue is in [[settings-ssl-troubleshooting]].

Practical implication: paste the **end-entity cert** (not the chain) into the **Certificate** field and the **chain alone** into the **Chained Certificate** field. A common error is pasting both into one field; this returns one of the validation errors above.

### Replacing an installed certificate

The admin has no replace button: **Remove**, then a new Manual install. In between the domain has no certificate, so the store serves it over plain http and redirects https visitors to http ([[settings-domains-ssl]]); on the primary domain the admin reloads. Have the new certificate, chain and key ready first. Through the Admin GraphQL API the install updates the existing certificate in place (certificate, chain, CSR and private key, checked to match), with no gap; on a Let's Encrypt certificate it stays marked as one, so the renewal sweep would later replace it.

The installed certificate covers the names the CA put in it; Install only checks that its name, without a leading `*.` or `www.`, matches the domain. `example.com` and `www.example.com` are one domain here and the other form is redirected, so request a certificate naming both (verify).

After install the expiry date is read from the certificate and the edge push starts ([[settings-ssl-edge-propagation]]).

### After install, the cert is marked `free=0`

The Manual install endpoint sets `free=0` on the cert record — this is the platform's marker that "this is an external cert and should NOT be picked up by the Let's Encrypt renewal sweep". The Manage-mode view then shows the purple **Manual** renewal badge plus the *"Managed by external provider. You should change it manually before the expiration date."* label.

### OU (Organizational Unit) not exposed in the form

The form has no OU input, so a CSR generated here has none. The Admin GraphQL CSR generation accepts an optional `unit`.

### Manual certs do not auto-renew

External certs do NOT participate in the daily Let's Encrypt sweep ([[settings-ssl-auto-renewal]]). Before expiry the merchant must obtain a renewed cert from the external CA, Remove the old cert, and re-run this flow. Forgetting triggers the automatic fallback — see [[settings-ssl-expiry-fallback]].

## Related

- [[settings-ssl]] — hub.
- [[settings-general]] — provides the CSR field defaults (Organization, Email, Country, Locality).
- [[settings-domains]] — DNS must be valid for the external CA to complete domain-control verification.
- [[settings-ssl-troubleshooting]] — full catalogue of the validation error strings emitted on Install.

## Open questions

- What the edge serves on the domain between **Remove** and a new install.
