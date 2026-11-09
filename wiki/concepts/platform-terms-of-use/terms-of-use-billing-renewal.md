---
type: concept
nav_path: "Concept → CloudCart Terms of Use → Prices, payment, renewal and invoices"
aliases: ["Terms of Use billing", "Are prices with VAT", "Prices in EUR", "Refund policy", "No refunds", "When does my plan start", "Subscription term start", "Auto renewal notice", "7-day renewal notice", "Turnover rule", "Plan by turnover", "Automatic plan upgrade by turnover", "Price change notice", "Free trial terms", "Възстановяване на суми", "Цени без ДДС", "Автоматично подновяване", "Оборот и абонаментен план", "Пробен период"]
tags: [legal, terms-of-use, billing, subscription, renewal, refund, invoice, concepts]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[platform-terms-of-use]]. See the hub for the contracting entity and the other aspects.

# Terms of Use: prices, payment, renewal and invoices

## Definition

What section 11 of the Terms of Use (plus §6.2) says about paying CloudCart: currency and VAT, prepayment by card, refunds, the free trial, when a plan's term starts, renewal, the turnover rule, failed payments, price changes and invoices. How the platform carries this out is on [[merchant-subscription-lifecycle]].

## Scope

Payments the merchant makes **to CloudCart**: plans, packs, apps, functionalities and additional services. Payments the merchant's customers make in the store are in [[terms-of-use-third-parties-data]]. Ending the contract is in [[terms-of-use-termination-data]].

## Contrasts

- **Refund vs CloudCart's own early termination.** The merchant gets no refund for giving up a service. The single exception is when CloudCart itself ends the contract early under §19.4. CloudCart then either lets the prepaid period run out or refunds the unexpired part, at its choice.
- **Turnover upgrade vs voluntary upgrade.** §11.6 moves a merchant to a higher plan automatically when their turnover crosses the plan's limit. A voluntary upgrade is a purchase on [[plans]].
- **Contract currency vs store currency.** CloudCart charges in EUR whatever currency the store sells in.

## Where it applies

### Currency, VAT and prepayment (§11.1, §11.2)

All prices of plans, packs, functionalities, apps and additional services, on CloudCart's websites and in the admin, are **„в евро (EUR) и без включено ДДС“**. Every payment to CloudCart is made in EUR, automatically, by the merchant's payment card, and is **prepaid in full (100%)**.

### No refunds (§11.2, §11.13, §19.3)

> „В случай че Търговецът се откаже от Услугите преди изтичане на срока за който са платени, платената сума не подлежи на връщане от КлаудКарт.“ (§11.2)

§11.13 repeats this for plans, packs, apps, functionalities and additional services that the merchant gives up or does not use. It also covers a renewal the merchant did not cancel in time. On termination, fees already paid stay with CloudCart (§19.3, point 2), except in the §19.4 case above.

### Free trial (§11.3)

The trial lasts for the period stated on CloudCart's site and starts on the day the account is registered. If no plan is chosen and paid during the trial, access to the account is suspended when the trial ends. If no plan is paid within **3 months** after that, CloudCart may delete the merchant's information.

### When the plan's term starts (§11.4)

> „Срокът на абонаментния план започва да тече от момента, в който Онлайн магазинът/Уеб сайтът стане публичен. С изтичането на 30 (тридесет) дни от момента на заплащане на избрания абонаментен план, срокът на абонаментния план започва да тече, дори и Търговецът да не е направил Онлайн магазина/Уеб сайта публичен.“

So the term starts when the store goes public, and at the latest 30 days after the plan is paid.

### Automatic renewal and the 7-day notice (§11.5)

Plans and other services renew automatically at the end of the paid period, for a period of the same length. **A 7-day notice of the upcoming automatic payment is e-mailed to the merchant** („на и-мейла на Търговеца се изпраща 7-дневно предизвестие“). Unless the merchant explicitly cancels before the period ends, the amount is charged to their card. The platform's side, including the conditions under which the notice is sent, is on [[subscription-renewal-retry]].

### The turnover rule (§11.6)

The plan that applies to a merchant depends on their turnover. The turnover is recalculated **every month over the previous 6 months**. If, during a prepaid period, it exceeds the 6-month limit of the current plan, then:

- the merchant moves automatically to the plan for the higher turnover;
- the move applies from the month after the limit was crossed, for the rest of the current period;
- the merchant pays the new plan's price minus the current plan's price, pro rata for the remaining term.

### Card authorisation and payments on the merchant's behalf (§11.7–§11.9)

- The merchant authorises CloudCart to collect what is due from the card linked to the account. This covers renewals of plans, packs, apps and functionalities (§11.7).
- One authorisation is enough for every later plan, pack, app, functionality or additional service. It stays valid until the merchant revokes it in the admin (§11.8).
- The merchant may authorise a specific payment by e-mail or by phone. Phone calls are recorded and serve as proof of the authorisation (§11.9).
- Instructions from the account's e-mail address count as the merchant's own. If the e-mail or the card is hacked, the merchant must tell CloudCart at once. Transactions made before that notice remain valid (§11.9).

### Failed payment (§11.7)

If the automatic payment fails and the amount is not paid when due, CloudCart **may suspend access to the admin panel**. If it is still unpaid **30 days** after it fell due, CloudCart **may terminate the services**. The platform's actual retry schedule and grace period are on [[subscription-renewal-retry]] and [[subscription-expiration]].

### Fees charged by the merchant's bank (§11.12)

The merchant's bank or card issuer may add its own fees to a payment to CloudCart. A payment counts as made when CloudCart's account receives the full price. Any extra fee is owed to that provider separately.

### Price changes (§11.14)

CloudCart may change prices at any time by publishing them on its sites. A change does not affect anything already prepaid. It applies from the next period, and to services added after the change.

### Invoices (§11.10, §11.15, §6.2)

> „Фактурите за дължимите плащания към КлаудКарт се издават съгласно посочените от Търговеца данни в Административния панел на съответния онлайн магазин в платформата CloudCart. За всеки Онлайн магазин на Търговеца може се издава фактура на отделно дружество.“ (§11.15)

- Invoice details are set **per store**, and each store may be invoiced to a different company (§6.2, §11.15). See [[billing-invoicing]].
- CloudCart confirms a payment by activating the service (§11.10).
- CloudCart is not responsible if the merchant gave an invalid e-mail address or did not receive the invoice for another reason outside CloudCart's control. The Terms advise checking every mail folder, including SPAM (§11.10).
- The Terms say nothing about correcting or re-issuing an invoice that has already been issued. See [[subscription-invoices]].

## Related

- [[platform-terms-of-use]]: hub.
- [[subscription-renewal-retry]]: renewal, retries and the pre-billing notice on the platform.
- [[subscription-cancellation]]: cancelling without a refund.
- [[billing-invoicing]]: the per-store invoice details.
- [[subscription-invoices]]: the invoices CloudCart issues.
- [[plans]]: the plan catalogue and prices.

## Open Questions

- Whether the platform starts a plan's term at go-live as §11.4 says, or at payment (verify against the billing code).
- How a §11.6 turnover upgrade appears in the admin, and whether the *"This subscription has unpaid turnover amount"* guard on Cancel and Renew ([[subscription-cancellation]]) is that pro-rata difference. The wiki describes it as metered overage (verify).
- The length of the free trial. §11.3 refers to CloudCart's site.
