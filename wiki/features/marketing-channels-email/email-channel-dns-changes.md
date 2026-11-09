---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → DNS records alongside other senders and after changes"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Merge SPF record", "Two SPF records", "Existing SPF record", "Existing DMARC record", "SPF include Elastic Email", "Verify propagation time", "Email DNS records removed", "Email channel after DNS move", "Обединяване на SPF записи", "Изтрити DNS записи за имейл"]
tags: [marketing, channels, email, dns, spf, dkim, dmarc, troubleshooting]
plan_gates: ["campaign.channel.email"]
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[marketing-channels-email]]. The four records themselves and the Verify step are on [[email-channel-dns-records]].

# Email channel — DNS records alongside other senders, and after changes

## Purpose

What to do with the Email channel's four DNS records when the domain already carries records for another sender, when **Verify** sees a newly added record, and what happens once the channel is verified and the records are later removed or the domain's DNS moves to another host.

## Where to find it

Step 3 (**Verify**) of the setup wizard shows the four records ([[email-channel-setup-wizard]]). The records are added where the domain's DNS is managed: in the store's DNS management for a domain on CloudCart's DNS ([[settings-domains-dns-cloudflare]]), otherwise at the merchant's own DNS host.

## What the merchant can do here

- Merge the channel's SPF into an existing SPF record.
- Keep a single DMARC record.
- Re-click **Verify** after a change.

## Settings & fields

### Records that already exist on the domain

- **SPF.** A domain may publish only one SPF record: with two, the SPF check fails for every sender. Add `include:_spf.elasticemail.com` to the existing record instead of creating a second one. CloudCart's hosted mailboxes (a discontinued service, [[settings-emails]]) write their own `v=spf1 mx ~all` as a separate record when the first mailbox is activated. The channel's value `v=spf1 a mx include:_spf.elasticemail.com ~all` already contains `mx`, so it covers the hosted mail too and takes that record's place.
- **DKIM.** Each sender signs with its own selector, so the channel's record at `api._domainkey` sits beside the others (a hosted mailbox uses `<domain>._domainkey`). Only a record already at `api._domainkey` is replaced, with the value on the **DKIM Record** card.
- **DMARC.** Only one record may exist at `_dmarc`, and hosted mailboxes write one too. Keep a single record rather than adding a second. Whether Elastic Email's check accepts an existing policy that differs from the value shown is Elastic Email's rule (verify).

## Business rules

### When Verify sees a new record

Every click of **Verify** asks Elastic Email to look all four records up again; CloudCart keeps no earlier result. On CloudCart's DNS a saved record is live within seconds. At another DNS host it is visible once that host publishes it and any older cached answer expires (the record's TTL). Lookup caching on Elastic Email's side is outside CloudCart.

### All four are required

None of the four is optional for the channel: Verify passes only when SPF, the tracking CNAME, DKIM **and** DMARC all pass ([[email-channel-dns-records]]).

### After verification: records removed or DNS moved

- The checks are never re-run after verification, so the channel stays verified and keeps sending when records are deleted, or when the nameservers move to a host where the records were not recreated. Nothing in the admin flags it.
- A tracking CNAME that CloudCart created lives in the domain's zone on CloudCart's DNS; it does not follow the domain to a new DNS host and has to be added there by hand.
- What changes is how receiving mail servers treat the mail: without passing SPF, DKIM and DMARC, more of it may be rejected or filed as spam, as each receiver decides. Rising bounce or spam rates can then suspend the channel ([[email-channel-suspend-thresholds]]). How Elastic Email's open and click tracking behaves without the tracking CNAME is Elastic Email's (verify).

### Order notifications do not use these records

Only campaign mails and the subscriber confirmation go through the Email channel. Order and account notifications are sent From noreply@cloudcart.com with the store's email as Reply-To, or through the store's own mail server when the [[apps-smtp|SMTP app]] is set up. Removing or breaking the channel's records does not affect them ([[marketing-channels-email]]).

## Related

- [[marketing-channels-email]] — hub.
- [[email-channel-dns-records]] — the four records and the Verify step.
- [[email-channel-setup-wizard]] — Step 3 where the records are shown.
- [[email-channel-suspend-thresholds]] — reputation thresholds that can suspend the channel.
- [[settings-domains-dns-cloudflare]] — DNS management for domains on CloudCart's DNS.
- [[settings-emails]] — hosted mailboxes and the records they write.
- [[apps-smtp]] — order notifications through the store's own mail server.

## Open questions

- Whether Elastic Email's DMARC check accepts a policy other than the one shown on the card (verify).
