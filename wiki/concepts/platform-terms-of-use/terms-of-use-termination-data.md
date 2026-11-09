---
type: concept
nav_path: "Concept → CloudCart Terms of Use → Termination, suspension and data"
aliases: ["Terms of Use termination", "How to close my CloudCart account", "Close account", "End the contract", "CloudCart terminates my contract", "Notice of termination", "Account suspended for violation", "Objection to suspension", "Data export after cancellation", "How long is my data kept", "30 days to download my data", "Прекратяване на договора", "Закриване на акаунт", "Сваляне на данните", "Колко време се пазят данните", "Възражение срещу спиране"]
tags: [legal, terms-of-use, termination, cancellation, data-retention, suspension, concepts]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[platform-terms-of-use]]. See the hub for the contracting entity and the other aspects.

# Terms of Use: termination, suspension and data

## Definition

How the contract with CloudCart ends and what happens to the merchant's data, under section 19 of the Terms of Use, with §8.2–§8.10, §11.3, §11.7 and §11.11.

## Scope

Ending the whole contract, and suspending or restricting the services. Cancelling a single subscription on the platform is on [[subscription-cancellation]]. Refunds are on [[terms-of-use-billing-renewal]].

## Contrasts

- **Cancelling a subscription vs ending the contract.** The merchant ends the contract by cancelling **all** active subscriptions (§19.2). On the platform, each cancellation is soft: the service runs until its next billing date ([[subscription-cancellation]]).
- **Three notice regimes.** For the contract as a whole:
  - CloudCart may end it early with **one month's** written notice (§19.4);
  - a full termination of services carries an e-mail with the reasons **30 days** ahead (§8.6);
  - a breach allows termination **without notice** (§19.5).
- **The contractual window vs current practice.** The Terms promise **30 days** (§11.11, §19.3). The platform currently deletes an expired store's database in later cleanup sweeps: 3 months for a free store, 6 months for a paid one ([[expired-subscription-data-lifecycle]]). That is practice, not a promise. Support gives the merchant the 30 days as the time they can count on.

## Where it applies

### How the contract ends (§19.1)

The contract ends:

- when the plan's term runs out and is not renewed;
- by written mutual agreement;
- when a party is objectively unable to perform;
- when a party is dissolved or declared insolvent;
- in the other cases the Terms provide for.

### Ending it as the merchant (§19.2, §18.1)

> „Търговецът може по всяко време да прекрати едностранно договора, да закрие своя Акаунт, да спре всички абонаментни услуги, които са активирани, и да преустанови използването на своя Онлайн магазин, от Административния панел в секция Абонаменти, като ОТКАЖЕ всички активни абонаменти.“

The section is [[subscriptions]]. The merchant may also end the contract during the notice period of an announced change to the Terms (§18.1).

### What termination means (§19.3)

Whatever the reason, ending the contract and closing the account means:

1. CloudCart stops the services, and the merchant loses access to the account and the store.
2. Fees already paid are not refunded. They stay with CloudCart as compensation for early termination, except in the §19.4 case.
3. Everything owed to CloudCart becomes payable at once.
4. The merchant has **30 days** to download their data:

> „Търговецът има 30 дни, считано от датата на прекратяване на договора, да свали и съхрани своята база данни извън платформата CloudCart.“

After that the information is deleted, unless CloudCart must keep it to meet legal or contractual obligations. CloudCart is not liable for the loss.

### Ending it as CloudCart

- **With notice (§19.4):** at any time, with **one month's written notice**, which may be by e-mail. If a prepaid period is still running, CloudCart chooses one of two options: the termination takes effect when the prepaid period ends, or CloudCart refunds the part of the payment for the unexpired period.
- **Without notice (§19.5):** if CloudCart finds that the merchant breaches the Terms, the law or good morals. No compensation is owed.
- **For non-payment (§11.7):** CloudCart may suspend access to the admin when a payment is overdue, and may terminate the services after **30 days** unpaid.

### Suspension and restriction for breaches (§8.2–§8.5, §8.20)

CloudCart may:

- refuse services for objective reasons or for a breach (§8.2);
- restrict, suspend or terminate them on a suspected or established breach of the Terms, the law or good morals (§8.3);
- monitor accounts and stores, block access, remove unlawful content and suspend a whole store (§8.4);
- suspend services and investigate a suspected breach of the Anti-spam policy (§8.20).

Verbal or written aggression or disrespect towards CloudCart's employees, shareholders or partners, threats included, is a ground for termination (§8.5).

### Reasons and objection (§8.6–§8.9)

- **Restricting or suspending services for certain products:** CloudCart e-mails the reasons before the measure or when it is applied (§8.6).
- **Ending the services entirely:** CloudCart e-mails the reasons **30 days before**. There are three exceptions: a legal obligation that does not allow it, termination under mandatory Bulgarian law, and repeated breaches that CloudCart can prove (§8.6).
- **What the reasons contain:** the concrete facts, including third-party reports, and the clauses relied on (§8.7). They may be withheld where the law requires it, or after repeated breaches (§8.8).
- **Objection:** the merchant may object, describing the facts and giving evidence. If CloudCart accepts the objection, the service is restored to its earlier state (§8.9).

### How long data is kept (§11.11, §11.3)

> „КлаудКарт ще съхранява информацията, съдържаща се или свързана с Онлайн магазин/Уеб сайт или друга Услуга, за срок от 30 (тридесет) дни от датата на изтичане на периода, за който е извършено последното плащане за Услугата.“

If nothing is paid within those 30 days to restore the service, CloudCart deletes the information. There are two exceptions: CloudCart must keep it for legal or contractual reasons, or the merchant has paid for an archiving and storage service. After a free trial, the information may be deleted if no plan is paid within 3 months (§11.3).

## Related

- [[platform-terms-of-use]]: hub.
- [[subscription-cancellation]]: what the Cancel button does on the platform.
- [[expired-subscription-data-lifecycle]]: what the platform currently does with an expired store's data.
- [[subscription-expiration]]: the platform's grace period after a failed renewal.
- [[subscriptions]]: the Subscriptions section named in §19.2.

## Open Questions

- Whether the paid archiving and storage service in §11.11 exists in the catalogue (verify).
- How the merchant downloads "their database" within the 30 days. The Terms do not say which export is meant. The platform's own exports include [[orders-export]] and [[customers-export]] (verify).
