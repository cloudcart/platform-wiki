---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Onboarding → Documents"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay documents upload", "Identity document upload", "Business registration document", "Proof of registration", "File view proxy"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, documents, uploads]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, KYB fields, verification, bank, status, connect/disconnect).

# Onboarding — Documents upload

## Purpose

Step 4 of the onboarding wizard collects two KYB documents: the representative's **government-issued identity document** and the **business registration document** (certificate of incorporation / commercial register extract). This aspect documents the upload slots, file constraints, attachment mechanics on the Paypercut side, and the inline file-view proxy.

## Where to find it

Payment Providers → CloudCart Pay → **Onboarding** tab → **Documents** (step 4).

## What the merchant can do here

- Upload an **identity document** for the representative (PDF, PNG, JPG, JPEG, max 10 MB).
- Upload a **business registration document** (same constraints).
- See a "Documents on file" panel listing already-uploaded files with file ID, size in KB and a clickable proxy link.
- Click a file ID to open the file inline in the browser via the proxy.
- See additional document slots when Paypercut returns specific `pending_requirements` containing the word `document` (dynamic slot list).

## Settings & fields

Backend: `POST /admin/cloudcart-pay/files` → Paypercut `POST /v1/files` with `multipart/form-data`.

Two upload slots (or a dynamic list of slots when Paypercut returns specific `pending_requirements` containing the word `document`):

| Slot | Required document | Constraints |
|------|-------------------|-------------|
| **Identity Document** | Representative's government-issued ID. Attached to the representative's `verification.document.front` on upload. | Allowed types: PDF, PNG, JPG, JPEG. Max 10 MB. |
| **Business Registration Document** | Certificate of incorporation / commercial register extract. Attached to the account's `documents.proof_of_registration.files`. | Same constraints. |

Both upload with `purpose=identity_document` (per the Paypercut spec; `account_requirement` is rejected for `proof_of_registration`). The slot is encoded in a separate `slot` field that the backend uses to decide which entity to attach the file to.

Already-uploaded files are listed in a **"Documents on file"** panel above the slots, showing the file ID, size in KB, and a clickable proxy link (`/admin/cloudcart-pay/files/{id}`) that streams the file inline with the correct Content-Type.

## Business rules

### Allowed extensions and size cap

`POST /admin/cloudcart-pay/files`:
1. Validates extension: `pdf`, `png`, `jpg`, `jpeg`.
2. Max size 10 MB.
3. Files outside these constraints are rejected before being forwarded to Paypercut.

### Filename sanitisation + MIME preservation

The backend **sanitises the filename** before forwarding to Paypercut: strips `[^A-Za-z0-9._-]`, preserves the extension, and forwards the real MIME type so the file is stored with the correct content-type. (Legacy uploads without an extension were stored as `bin` and downloaded as unrecognisable files — fixed.)

### `purpose=identity_document` is always sent

All uploads — both identity and business registration — go with `purpose=identity_document`. Paypercut rejects `account_requirement` for the documents this wizard collects. After upload, the wizard attaches the returned file ID to the correct entity:

- **Identity document** → `verification.document.front` on the representative person record.
- **Business document** → `documents.proof_of_registration.files` on the account record.

The wizard distinguishes the two via the `slot` field in the multipart payload — the backend uses `slot` to decide which Paypercut entity to attach the resulting file to.

### File view proxy

Clicking a file ID hits `GET /admin/cloudcart-pay/files/{file_id}` which:

1. Fetches the file from Paypercut's signed S3 URL.
2. **Sniffs the actual MIME type** (Paypercut's presigned URLs force a download with an extensionless temp name, so the proxy must re-detect the real content-type).
3. Streams it inline with these response headers:
   - `Content-Type` correctly inferred
   - `Content-Disposition: inline`
   - `X-Content-Type-Options: nosniff`
   - `Cache-Control: private, no-store`

The proxy keeps Paypercut's S3 URLs off the merchant's browser entirely — every read goes through the CloudCart admin host.

### Dynamic slot list

If Paypercut returns `pending_requirements` containing entries with the word `document`, the wizard renders **one extra upload slot per requirement** in addition to the two standard slots. This handles cases where Paypercut requests follow-up documents during review (e.g., proof of address, additional ID).

### Step 4 completion criterion

Step 4 is marked complete when `GET /v1/files` returns ≥1 uploaded file on the account — see [[ccpay-onboarding-wizard-flow]] for the live-state derivation logic. The merchant cannot "finish" step 4 by clicking past it without uploading at least one document.

### Re-upload to replace the representative's ID

The wizard does NOT expose a "delete file" action. To replace an identity document (e.g., after the original representative is changed in step 3 — see [[ccpay-onboarding-account-business-fields]]), the merchant re-uploads in the same slot; the new file ID is attached to the representative's `verification.document.front` and the old file remains in the Files API but no longer linked.

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-wizard-flow]] — step completion mechanics.
- [[ccpay-onboarding-account-business-fields]] — step 3 representative whose ID document is uploaded here.
- [[ccpay-onboarding-verification-attestation]] — step 5 where the identity document is checked.

## Open questions

(none)
