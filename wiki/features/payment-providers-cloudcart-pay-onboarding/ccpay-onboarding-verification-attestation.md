---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Agreements & Identity Verification"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay agreements step", "Accept & Submit", "Identity verification CloudCart Pay", "Verification link", "Verification unavailable", "Споразумения и верификация на самоличността", "Приемане и изпращане", "Започване на верификация на самоличността"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, verification, agreements]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 3
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, fields, people, documents, bank, status, review and alerts, connect/disconnect).

# Onboarding — Agreements & Identity Verification (step 5)

## Purpose

Step 5 does two things once the account has been submitted for review in step 4: the merchant **accepts the agreement documents**, and the company's **legal representative verifies their identity** through a link. After that the account waits for approval, which takes from a few hours to 2 business days after submission, longer for a complicated company structure (operator statement).

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab → step 5, **Verification** (Верификация); screen title **Agreements & Identity Verification** (Споразумения и верификация на самоличността).

Intro: *"Review and accept the required agreements, then verify the identity of the account representative. This creates a verification session that can be completed by the representative."*

## What the merchant can do here

- **Open, tick and accept** every agreement document with **Accept & Submit** (Приемане и изпращане).
- **Start the identity verification** with **Start Identity Verification** (Започване на верификация на самоличността).
- **Open or copy the verification link** and send it to the legal representative.
- **Continue** to the bank step.

## Settings & fields

### Before the account is submitted

The step shows a warning instead of the agreements:

- no person yet — *"Please create a representative in the previous step first."*
- not submitted — *"Submit the account for review in the Documents step first. Once review starts, the agreements to accept will appear here."*

### Agreements

Heading **Review and accept the agreement documents** (Прегледайте и приемете документите със споразуменията). One checkbox per required document, each title opening the document. The operator's list of the six documents, all required:

1. Tri-Party Merchant Agreement
2. Tri-Party Merchant DPA
3. Payment Instruction
4. Fee Schedule to the Tri-Party Merchant Agreement
5. Nominee Agreement
6. Paynetics Privacy Policy

**Accept & Submit** stays disabled until every box is ticked. What the agreement says is summarised in [[cloudcart-pay-merchant-terms]]; the prices in the Fee Schedule are in [[cloudcart-pay-pricing]].

### Identity verification

Notice: *"Identity verification must be carried out by a legal representative of the company being registered. Any other person completing it will not be accepted."*

After **Start Identity Verification** a **Verification Session** panel shows **Open Verification Link** (Отваряне на връзката за верификация), the text *"Share this link with the company's legal representative to complete identity verification:"*, the link itself and **Copy**.

Buttons at the bottom: **Back** (Назад) and **Continue** (Продължете).

## Business rules

### Agreements appear only after submission

The documents to accept are prepared for the account once it has been submitted for review in step 4, which is why this step asks for the submission first. The list on screen comes from the account itself, so the exact titles shown are the ones that apply; only the required ones are listed.

### Acceptance

**Accept & Submit** records the acceptance on behalf of the company in the name of its legal representative. The item then leaves the **Compliance Tasks** list on the Status step. Until it is accepted, that list shows the agreement with a **Resolve** button leading back here — see [[ccpay-onboarding-status-capabilities]].

### Identity verification

- It is done by the **legal representative** chosen in step 3 ([[ccpay-onboarding-people-roles]]), through the link, on their own device.
- Each click on **Start Identity Verification** creates a new verification link.
- Errors: *"Complete the remaining account details first (business information, representative and documents in the previous steps). Identity verification becomes available once all required information has been submitted."* and *"Identity verification is not available yet. Please make sure all required business and representative details have been submitted, then try again."*
- If the verification service is down while the account has nothing outstanding, the merchant is not blocked: *"Identity verification is temporarily unavailable from the payment provider. Your account details have been submitted and the account is active — you can continue now and the representative can complete identity verification later from this step."*

### When step 5 counts as done

When the account has been submitted for review (or a verification link was created). **Continue** always moves on to step 6.

### What happens next

The account is reviewed by a person. Approval takes from a few hours to 2 business days after submission; it can take longer when the company's structure is complicated (operator statement). Progress shows on the **Status** step, and changes arrive as an admin notification and an email — see [[ccpay-onboarding-review-alerts]].

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[cloudcart-pay-merchant-terms]] — what the accepted agreement contains.
- [[cloudcart-pay-pricing]] — the Fee Schedule.
- [[ccpay-onboarding-documents-upload]] — step 4, where the account is submitted.
- [[ccpay-onboarding-people-roles]] — the legal representative.
- [[ccpay-onboarding-status-capabilities]] — compliance tasks and capabilities.
- [[ccpay-onboarding-review-alerts]] — waiting for approval.

## Open questions

- Whether an earlier verification link stops working once a new one is created.
