---
type: entity
aliases: ["Domain lifecycle", "Domain phases", "Domain attach flow", "Domain activation", "Domain removal", "Add domain flow"]
tags: [settings, apps, domains, ssl, dns, entity, lifecycle]
created: 2026-06-10
updated: 2026-11-09
source_count: 1
---

> Part of [[domain]]. See the hub for the other aspects (attributes, relationships, SSL, DNS / Cloudflare, primary + plan gates).

# Domain — Lifecycle

## Identity

The end-to-end phases a [[domain|Domain]] moves through, from the moment the merchant first clicks "Add existing domain" on [[settings-domains]] to the moment the Domain is removed and its Cloudflare bindings are cleaned up. This page is the reference the AI Assistant cites when a merchant asks *"I added my domain yesterday but it still says pending — what's next?"* or *"What happens to my SSL cert when I remove the domain?"*. The lifecycle is **non-linear** — some phases (designation as primary, renewal warnings) are optional, and the SSL-expiry phase is triggered by a daily platform sweep rather than by a merchant action.

## Aliases

- **Domain lifecycle** / **Domain phases** — the sequence of states.
- **Add domain flow** — the merchant-facing entry point on [[settings-domains]].
- **Domain removal** — the terminal phase + its side effects.

## Key Attributes

A Domain moves through these phases:

1. **Attached** — the merchant added the Domain via "Add existing domain" on [[settings-domains]]. The row exists with no DNS method yet; the merchant picks CloudCart's nameservers (the zone is created then and stays `pending` until the nameserver change) or **Manage with CNAME** ([[settings-domains-external-dns]]). CloudCart-purchased domains get their zone and nameservers at purchase.
2. **Active (custom DNS in place)** — Cloudflare detects nameserver propagation; DNS status flips to `active`. The DNS records table unlocks for editing. The merchant can now configure A / AAAA / CNAME / MX / TXT / NS records — see [[domain-dns-cloudflare]].
3. **SSL provisioning** — nothing is issued when the Domain is added. The merchant clicks **Install SSL**: **Automatic install** issues a free Let's Encrypt certificate (needs the Let's Encrypt Manager app), **Manual install** takes an external one ([[settings-ssl]]). See [[domain-ssl]] for the two modes.
4. **Designated as primary** (optional) — when the merchant clicks "Set as primary" on a non-primary Domain, the platform checks three verification gates (DNS pointing correctly, SSL provisioned, external-domain "Powered-by" header). On pass, the previous primary is auto-unset and this Domain becomes primary. The admin SPA hard-redirects to the new URL. See [[domain-primary-and-plan-gates]] for the gate details.
5. **Renewal (CloudCart-purchased only)** — the row's **Renew** link works at any date and is the only thing that renews the registration (charged to the plan's card). A daily admin alert warns from one month before to one month after expiry. See [[settings-domains-add-flow]]. Domains registered elsewhere are renewed at their own registrar.
6. **SSL expiry → admin alert + automatic fallback** — a daily platform-wide sweep finds expired SSL certs. If the expired Domain was the Site's primary, the platform switches the primary back to `<handle>.cloudcart.net` and deactivates the custom Domain — the storefront keeps serving (no HTTPS warnings) on the CloudCart subdomain. If non-primary, the Domain is just deactivated. The merchant gets an alert: *"The SSL certificate for domain X is expired. Switched to main host: {mystore.cloudcart.net}."* OR *"The SSL certificate for domain X is expired. Domain is deactivated."* See [[domain-ssl]] for the full alert + fallback rule.

   **Pointed away.** When the nameservers or the A record are moved to another host, visitors reach that host and CloudCart no longer serves the storefront on the Domain. The status the row shows is the Cloudflare zone's own, and the DNS records table is offered only while that zone is active. Records kept in CloudCart's zone (for example the Email channel's tracking CNAME) stop counting once the nameservers leave ([[email-channel-dns-changes]]). Renewal of a free certificate can then be blocked, which leads to the expiry fallback above.
7. **Removed** — the merchant clicks the remove button on a non-primary Domain. The platform removes the Cloudflare Custom Hostname binding (if any), the SSL certificate record and the Domain row. The Domain's own Cloudflare zone is not deleted: it stays in CloudCart's account with its records, and re-adding the Domain reuses it.

## The CloudCart subdomain is always present

The `<handle>.cloudcart.net` Domain skips the lifecycle entirely — it is assigned at Site signup, cannot be removed from the admin panel, and cannot be deactivated. It serves as the permanent fallback URL: even after a custom Domain has been set as primary, the subdomain remains attached and can still serve the storefront if the custom Domain breaks. Renaming the handle requires CloudCart support intervention. See [[domain-attributes]] for the full list of subdomain-specific properties.

## Removal side effects

Removing a non-subdomain Domain from [[settings-domains]] triggers:

- No zone removal: the zone and its records stay in CloudCart's Cloudflare account.
- Cloudflare Custom Hostname binding removal (when applicable — see [[domain-dns-cloudflare]] for which Cloudflare mode applies).
- SSL certificate record deletion.
- Domain row deletion.

Re-adding the same Domain later reuses its zone, so its records come back. Neither plan expiry nor deleting the store deletes the zone either.

**The primary Domain cannot be removed.** To remove the current primary, the merchant must first promote another Domain to primary — see [[domain-primary-and-plan-gates]].

## Where it appears

- [[settings-domains]] — the master screen surfaces the lifecycle phase per row: DNS pending chip, SSL status chip, renewal warning chip, primary marker.
- [[settings-ssl]] — surfaces the SSL provisioning phase + expiry status.
- [[settings-admin-notifications]] — gates whether the SSL-expiry alert is emailed (in addition to appearing in the admin notification panel).

## Related

- [[domain]] — hub.
- [[site]] — Domain belongs to one Site; the always-present subdomain is created at Site signup.
- [[settings-domains]] — the master management screen.
- [[settings-ssl]] — SSL provisioning + expiry surface.
- [[apps-lets-encrypt]] — automatic SSL provisioning path.
- [[admin-notification]] — SSL expiry alert.

## Open Questions

- ⏸️ Whether removing a Domain mid-checkout (with active customer sessions) triggers any user-facing fallback, or whether the customer's session breaks abruptly.
