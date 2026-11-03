---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Documents → Requests from compliance"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["Additional documents requested by our compliance team", "CloudCart Pay document rejected", "Compliance asked for a document", "Replace document CloudCart Pay", "Document provided", "Submitted waiting for review", "Допълнителни документи, изискани от нашия екип за съответствие", "Отхвърлен документ CloudCart Pay", "Липсващи документи"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, documents, compliance]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, fields, people, documents, verification, bank, status, review and alerts).

# Onboarding — document requests from compliance

## Purpose

What the Documents step shows after the account was submitted and the compliance team rejects or asks for a document: the panel of requested documents, the rule that they go in together, how a sent document stays listed, and **Replace document**. The first submission and the checklist are on [[ccpay-onboarding-documents-upload]]. This is the page for "they rejected a document, what do I upload?" and "I uploaded it, why is it still there?".

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab → step 4, **Documents** (Документи) → **Additional documents requested by our compliance team** (Допълнителни документи, изискани от нашия екип за съответствие). The **Status** step links to it from each rejected item ([[ccpay-onboarding-status-capabilities]]).

## What the merchant can do here

- **Read what was asked for**, with the reviewer's message and the person it concerns.
- **Upload every requested document** in one go.
- **Replace** a document that is already waiting for review, after a confirmation.

## Settings & fields

| Element | What it shows |
|---|---|
| A row per owed document | The person, the document's name, for example **Proof of current address**, **Company licence** or **Proof of company registration** (Удостоверение за актуално състояние), and the reviewer's own message. |
| **Submitted — waiting for review** | Shown in place of the upload box: *"Submitted on <date> · <file>"*. |
| **Document provided** | A document already accepted, with **Replace document**. |
| **Missing documents** (Липсващи документи) | The list of what is still owed, kept current as files are picked. |

Files: PDF, PNG, JPG or JPEG, up to **10 MB**.

## Business rules

### The checklist steps aside

When compliance rejects or re-requests a document, the step hides the company and person checklist cards and lists every owed document in this panel, including ones the checklist would otherwise cover, such as the bank statement.

### All requested documents go together

Send every requested document in the same submit; a request can otherwise be dropped once one file is attached. An earlier attached file does not count while a document is being requested again, because that is the file that was rejected.

### Sent and not yet reviewed

A request that was answered and not yet reviewed stays listed on the Documents step as well as the Status step, so **Replace document** from Status has something to replace. Uploading the same document again does not speed up the review, which is done by a person. See [[ccpay-onboarding-review-alerts]].

### A request covering several people

When one request covers several people, for example proof of address for two people, a person-card upload keeps each person's file. The submitted panel shows the request text and every file with its person.

### Replace document

**Replace document** first asks: *"This document is already with our compliance team. Upload a new one only if it is a different document, for example when the one you sent was wrong or unreadable. Sending the same document again does not speed up the review."* — buttons **Upload a different document** and **Cancel**.

### Accepted documents

An accepted document shows **Document provided** with **Replace document**, and counts as provided after a reload.

### The review team is told

The review team is told when a request is answered and when a document is uploaded again in the same round, and is chased automatically. See [[ccpay-onboarding-review-alerts]].

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-documents-upload]] — the checklist and the first submission.
- [[ccpay-onboarding-status-capabilities]] — rejected items and the **Resolve** link.
- [[ccpay-onboarding-review-alerts]] — waiting for review, approval time.

## Open questions

(none)
