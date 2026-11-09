---
type: concept
nav_path: "Concept → CloudCart Terms of Use → Changes, availability, liability and security"
aliases: ["Terms of Use liability", "Does CloudCart notify before changes", "Notice before feature changes", "Template support ending", "Changes to the Terms notice", "Uptime guarantee", "SLA", "Is there an SLA", "Liability cap", "Who is responsible for account security", "Hacked account responsibility", "Custom code responsibility", "My custom code broke the store", "Beta features terms", "Предизвестие за промени", "Гаранция за непрекъсваемост", "Отговорност на КлаудКарт", "Сигурност на акаунта", "Персонализиран код отговорност"]
tags: [legal, terms-of-use, liability, uptime, security, changes, custom-code, concepts]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[platform-terms-of-use]]. See the hub for the contracting entity and the other aspects.

# Terms of Use: changes, availability, liability and security

## Definition

What the Terms of Use say about:

- the notice CloudCart gives before it changes something;
- uptime;
- the limits of CloudCart's liability;
- who answers for the account's security;
- who answers for the merchant's own content and code;
- features still in development.

## Scope

§8.1, §8.15, §8.18, §8.22, §5.3, §5.7, §11.9, §11.14, §12, §13.4, §14.11, §16 and §18. Changes to CloudCart Pay's own terms are on [[cloudcart-pay-merchant-terms]].

## Contrasts

- **Ending support for a template vs changing it.** CloudCart may modify a stock design at any time. The one-month notice in §8.22 applies only to **ending support** for it.
- **"Appropriate notice" vs a fixed period.** Changes to additional services, apps and functionalities need notice "appropriate to the circumstances" (§8.1), with no number of days. Changes to the Terms themselves need at least 15 days (§18.1).
- **Core platform and checkout markup.** No clause promises notice before changes to the platform's core features or to the checkout's code. The checkout's classes and hooks are not a versioned interface ([[checkout-page-javascript]]).

## Where it applies

### Notice before changes

| What changes | What the Terms provide | Clause |
|---|---|---|
| Additional services, apps, functionalities | CloudCart may change, limit, suspend or end them at its discretion and at any time, „след отправяне на подходящо предизвестие според обстоятелствата“. Not all of them are offered in every country. | §8.1 |
| Stock designs (templates) | No guarantee that a template stays supported for the paid term. CloudCart may modify it or stop supporting it, and announces the end of support **at least 1 month** in advance. | §8.22 |
| Prices | Published on CloudCart's sites. Not applied to prepaid items; they apply from the next period ([[terms-of-use-billing-renewal]]). | §11.14 |
| Third-party services in the platform | CloudCart may remove them at any time, but must provide a similar or equivalent service. | §14.11 |
| Services in development (beta) | May be stopped at any time. | §16.3 |
| The Terms of Use | See below. | §18 |

**Changes to the Terms (§18):**

- The merchant is notified appropriately **at least 15 days** before a change takes effect. They may end the contract within that time, and continuing to use the services afterwards means acceptance (§18.1).
- The merchant may accept a change earlier, in writing or in another unambiguous way (§18.2).
- The notice may be shorter, or the change immediate, in two cases: a legal obligation that makes 15 days impossible, or an urgent need to protect the services, merchants or end customers from fraud, malware, spam, data-security breaches or other cybersecurity risks (§18.3).
- No retroactive changes, unless the law requires them or they favour merchants (§18.4).
- Editorial changes that do not alter the meaning apply at once, without notice (§18.5).

### Availability: no 100% guarantee (§12.4, §12.3)

> „КлаудКарт не може да гарантира, че Услугите ще бъдат 100% активни и няма да има прекъсвания или грешки при функционирането на платформата CloudCart.“

CloudCart is not liable for interruptions caused by force majeure, accidents, internet problems, unlawful acts of third parties (hacker attacks included), orders of authorities, or technical or other objective reasons. The Terms state no uptime percentage and no SLA. For third-party services integrated with the platform, the merchant can check their status on the status page shown in the admin (§12.3).

### Limits of liability (§12)

- No liability for direct or indirect, material or non-material damage, including lost profit and harm to reputation, from using or not using the platform (§12.1). No promise that the services bring revenue or profit (§12.2).
- No liability where the merchant or their customers entered wrong data, or did not follow the Terms, CloudCart's instructions or the law (§12.5). The merchant obtains every licence and permit their products need (§12.6).
- **Cap:** CloudCart's liability never exceeds the price the merchant paid for the services linked to the damage (§12.11).
- The merchant indemnifies CloudCart against third-party claims arising from the merchant's breaches, including lawyers' fees (§12.10).

### Security of the account (§5.3, §5.7, §11.9, §6.4)

> „Търговец ът е отговорен за опазването на потребителското име и парола на своя Акаунт, както и всяка друга информация, свързана със сигурността на Акаунта и платежните операции извършвани от Търговеца.“ (§5.7, spacing as published)

- The merchant declares that the e-mail, phone and card used with CloudCart are under their control. CloudCart is not liable for damage from a security breach of the merchant's e-mail, phone, card or account (§5.7).
- The e-mail and password identify the merchant, and a simple electronic signature counts as a handwritten one (§5.3).
- If the e-mail is hacked or someone gains access to the e-mail or card, the merchant must tell CloudCart at once. Transactions made before that remain valid (§11.9).
- The merchant answers for what the administrator and moderators do (§6.4).
- Personal data is protected under Bulgarian law and the GDPR (§17.2).
- The Terms say nothing about server software versions, patching, certifications or breach notification.

### The merchant's own content and code (§8.15, §8.18, §13.4)

> „Търговецът носи пълна отговорност за цялата дейност и съдържание на Онлайн магазина/Уеб Сайта, включително за всички снимки, изображения, видеоклипове, аудио файлове, графики, код и всяко друго съдържание, качено, събрано, генерирано, съхранявано, публикувано, разпространявано, предавано или изложено от него във връзка със създадения Акаунт.“ (§8.15)

- Code the merchant adds, for example in [[design-custom-assets]], is the merchant's content and responsibility.
- The merchant must not interfere with the platform's speed or proper functioning (§8.18).
- The merchant has no access to the platform's source code. An attempt to access, copy or change it is a material breach (§13.4).

### Services in development (§16)

CloudCart may invite a merchant to try features still in development, possibly under extra terms given beforehand (§16.1). Participation is confidential: no public statements without CloudCart's written consent (§16.2). There is no warranty that these features work, no liability for them, and CloudCart may change them, stop them, or never release them (§16.3).

## Related

- [[platform-terms-of-use]]: hub.
- [[design-custom-assets]]: where the merchant adds their own CSS / JS.
- [[checkout-page-javascript]]: the checkout's hooks, which are not a versioned interface.
- [[design-themes]]: the stock designs §8.22 refers to.

## Open Questions

- Which admin page §12.3 means by the status page for third-party services (verify).
