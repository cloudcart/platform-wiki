---
type: entity
aliases: ["Primary domain", "Set as primary", "Set as primary verification", "Hard redirect on primary change", "External vs CloudCart-purchased", "External domain quota", "cname plan feature", "custom_hostname plan feature", "Add domain quota", "IDN support", "Punycode storage"]
tags: [settings, apps, domains, ssl, plan-gates, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[domain]]. See the hub for the other aspects (attributes, relationships, lifecycle, SSL, DNS / Cloudflare).

# Domain — Primary, plan gates & business rules

## Identity

The platform rules that constrain how the merchant chooses, switches, and pays for [[domain|Domains]] on a [[site|Site]]. Four families of rules sit on this aspect: (1) **exactly one primary** per Site + the verification gates that run on Set-as-primary + the hard-redirect side effect; (2) **external vs CloudCart-purchased** — two different billing models for what looks like the same domain; (3) **plan-gated quota** on how many external Domains the merchant can attach; (4) **deletion side effects** and **IDN support** (non-ASCII hostnames). This page is the reference the AI Assistant cites when a merchant asks *"Why did setting my new domain as primary log me out?"*, *"Who pays to renew my domain?"*, *"I can't add another domain — why?"*, or *"Does CloudCart support Cyrillic domains?"*.

## Aliases

- **Primary domain rules** — the exactly-one-per-Site + verification gates + hard-redirect.
- **External vs CloudCart-purchased** — the two billing models.
- **External domain quota** — the `cname` / `custom_hostname` plan-feature cap.
- **IDN support** — internationalised (non-ASCII) domain names.

## Key Attributes

### Exactly one primary Domain per Site

Only one Domain can be `is_primary=true` at a time. Setting another Domain as primary auto-unsets the previous primary. The primary Domain **CANNOT** be:

- Deactivated.
- Deleted.

To deactivate or delete the current primary, the merchant must first promote another Domain to primary. Setting a new primary causes a **hard redirect** — the admin SPA reloads on the new domain because admin session cookies are scoped to a specific Domain. The merchant may need to re-authenticate if the new cookie domain rules require it. The always-present `<handle>.cloudcart.net` subdomain can always be set as primary as a recovery option.

### Set-as-primary verification gates

When the merchant tries to set a Domain as primary, the platform checks three conditions and opens the relevant guidance modal if any fails:

1. **DNS pointing correctly**: if the Domain's Cloudflare DNS zone isn't yet `active`, the merchant is taken to the DNS modal to finish the nameserver change. See [[domain-dns-cloudflare]].
2. **SSL provisioned**: if no valid SSL certificate is in place, the merchant is taken to the SSL modal to install one. See [[domain-ssl]].
3. **External-domain "Powered-by" header check**: for externally-owned Domains, the platform fetches the Domain and looks for a CloudCart-identifying response header. If absent, the merchant sees an *"Invalid domain headers"* error — the DNS resolves but does not actually reach CloudCart servers.

All three gates must pass before the primary marker moves.

### External vs CloudCart-purchased — different billing models

Domains carry one of two `source` values that drive entirely different billing behaviour:

- **External** (`source = external`): the merchant brought the Domain from another registrar (GoDaddy, Namecheap, etc.). They change the nameservers to point at CloudCart's Cloudflare nameservers (or add a CNAME for Custom Hostname mode). **CloudCart does NOT manage renewal or pay for these** — the merchant continues to pay their original registrar. The renewal warning chip on [[settings-domains]] does not appear for external Domains.
- **CloudCart-purchased** (`source = cloudcart`): bought through the in-admin Buy a Domain flow via the integrated reseller. **CloudCart pays the registrar on the merchant's behalf** at registration; renewal is billed through the merchant's plan subscription. WHOIS Privacy is automatically enabled (the public WHOIS lookup shows the registrar's privacy proxy, not the merchant's real address). Renewal warnings appear 30 days before expiry. Renewal price may differ from the initial purchase price (reflects current registrar pricing).

### Plan-gated external-domain quota

The `cname` / `custom_hostname` plan-feature controls how many external (CNAME-attached) Domains the merchant can add. When trying to add a Domain beyond the quota:

- The Add Domain flow shows a plan-upgrade prompt, OR
- An offer to buy an additional external-domain slot from the pack checkout.

After payment, the slot is unlocked and the Domain can be attached. The current usage vs quota is shown in the "Other domains" usage chip in the [[settings-domains]] header. Without the external-domain plan feature, the merchant gets only the `<handle>.cloudcart.net` subdomain. See [[plan-gates]] for related feature caps and [[domain-dns-cloudflare]] for which Cloudflare mode each quota covers.

### Deletion side effects

Removing a Domain from [[settings-domains]] triggers:

- Cloudflare DNS records removal (failures swallowed silently).
- Cloudflare Custom Hostname binding removal (when applicable).
- SSL certificate record deletion.
- Domain row deletion.

Re-adding the same Domain later starts from scratch — no DNS history preserved. If the merchant has custom DNS records they want to keep, they should export / record them before removing the Domain. Removing the Domain does NOT auto-cancel the underlying registrar registration for CloudCart-purchased Domains — full cancellation / transfer requires CloudCart support. See [[domain-lifecycle]] for the full removal phase.

### IDN (internationalised domain names) are supported

Non-ASCII domains (Cyrillic / Greek / Arabic, etc.) are accepted by the Add Domain input. The platform converts to Punycode (UTS-46 variant) for storage and back to the display form for rendering. So `сайт.бг` is stored as `xn--80aswg.xn--90ae` and rendered back in the merchant's preferred form. SSL certificates and the hostname-resolution middleware both normalise via the same IDN conversion, so an IDN Domain works end-to-end. The SSL cert is issued against the Punycode form — see [[domain-ssl]] for the third-party-behaviour note on what merchants see in browser certificate inspectors.

## Where it appears

- [[settings-domains]] — the master screen surfaces the primary marker, the quota usage chip, the Set-as-primary action, and the renewal warning chip.
- [[settings-ssl]] — gate 2 (SSL provisioned) is enforced here.
- The DNS modal — gate 1 (DNS active) is enforced here.
- The Buy a Domain in-admin flow — entry point for CloudCart-purchased domains.

## Related

- [[domain]] — hub.
- [[site]] — Site-Domain scoping.
- [[plan]] — `cname` / `custom_hostname` plan-features.
- [[plan-gates]] — quota mechanics.
- [[settings-domains]] — master management surface.

## Open Questions

- ⏸️ Whether the CloudCart-purchased domain renewal price is shown to the merchant BEFORE renewal (so they can pre-empt the charge) or only AFTER as an invoice line. `(verify)`
