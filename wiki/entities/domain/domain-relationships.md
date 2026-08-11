---
type: entity
aliases: ["Domain relationships", "Domain links", "Site-Domain relationship", "SSL certificate relationship", "Cloudflare zone relationship", "the store resolver"]
tags: [settings, apps, domains, ssl, dns, entity, relationships]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[domain]]. See the hub for the other aspects (attributes, lifecycle, SSL, DNS / Cloudflare, primary + plan gates).

# Domain — Relationships

## Identity

The relationship graph for the [[domain|Domain]] record — every other entity, infrastructure binding, and platform subsystem a Domain references or is referenced by. This page is the reference the AI Assistant cites when a merchant asks *"What else does this Domain affect?"* or *"Why did changing my primary Domain log me out of the admin panel?"*. The relationships fall into three groups: per-Domain bindings (Site, SSL cert, Cloudflare), platform-side consumers (the platform code middleware, admin cookies, checkout / invoice / waybill URL generation, the daily SSL sweep), and the things a Domain does NOT auto-affect.

## Aliases

- **Domain relationships** / **Domain links** — the cross-entity references a Domain participates in.
- **Site-Domain relationship** — the most important one; covered first below.

## Key Attributes

A Domain:

- **Belongs to one** [[site|Site]] — Site-scoped end-to-end; one Domain cannot serve multiple Sites. A Site can have many Domains (one primary, others as aliases, plus the always-present `<handle>.cloudcart.net`).
- **Has one** SSL certificate at any given time — either Let's Encrypt (auto-renewed via the [[apps-lets-encrypt]] app) OR external (merchant-managed). The two modes are mutually exclusive (switching requires Remove + reinstall) — see [[domain-ssl]].
- **References** a Cloudflare zone OR Cloudflare custom-hostname binding — depending on the add path. The merchant doesn't pick this; the platform chooses. See [[domain-dns-cloudflare]].
- **Is referenced by** [[settings-cart|cart/checkout]] URLs and [[orders-shipping-waybill|courier waybill]] / [[orders-invoice|invoice]] customer-facing URLs — all generated against the Site's primary Domain.
- **Is referenced by** admin session cookies — admin cookies are scoped to a specific Domain, which is why setting a new primary Domain triggers a hard redirect (the admin SPA reloads on the new URL because the cookie was scoped to the old one). See [[domain-primary-and-plan-gates]].
- **Is resolved by** the hostname-resolution middleware on EVERY storefront and admin-panel request — the request's `Host` header is matched against Domain rows to find the Site.
- **Triggers** an admin alert ([[admin-notification]]) via the daily SSL sweep when its certificate expires; if it was the Site's primary, the primary auto-falls-back to `<handle>.cloudcart.net` — see [[domain-ssl]].

A Domain does NOT:

- Get auto-detached from a Site on cancellation of a CloudCart-purchased registration — removing the Domain from [[settings-domains]] does NOT auto-cancel the underlying registrar registration. Full cancellation / transfer requires CloudCart support.
- Carry per-staff permissions — every staff member with the `settings.domains` permission sees all Domains. See [[merchant-roles]].
- Get cloned across Sites — each Domain belongs to exactly one Site; the same hostname cannot be attached to two Sites.

## Hostname resolution is the linchpin

The platform's hostname-resolution middleware runs on **every** storefront and admin-panel request. It takes the incoming `Host` header, normalises it (lowercasing, IDN-to-Punycode if needed), and looks up the matching Domain row. From that row it resolves the parent Site and uses it for all subsequent request scoping — which catalog, which orders, which staff users, which API keys, which webhooks.

This is why **the Domain → Site link is single-valued and non-cloneable**: if two Sites could share the same hostname, the resolver could not deterministically pick the right Site. It is also why **moving a Domain between Sites would break every URL** that points at it: cookies are scoped per-Domain, search-engine indexed URLs are tied to the Site that responded, etc.

## Where it appears

- [[settings-domains]] — shows the Domain-to-Site binding (always implicit because every Site has its own [[settings-domains]] screen).
- [[settings-ssl]] — shows the per-Domain SSL certificate currently attached.
- [[settings-cart]] — checkout URLs reference the primary Domain.
- [[orders-invoice]] / [[orders-shipping-waybill]] — invoice and waybill customer-facing URLs use the primary Domain.
- [[settings-admin-notifications]] — controls whether SSL expiry / fallback alerts (admin-notifications) are emailed.

## Related

- [[domain]] — hub.
- [[site]] — every Domain belongs to exactly one Site.
- [[plan]] — `cname` / `custom_hostname` plan-features cap how many Domains the merchant can attach — see [[domain-primary-and-plan-gates]].
- [[admin-notification]] — SSL expiry + fallback alerts.
- [[api-key]] / [[webhook]] — both Site-scoped; served per the Site resolved from the matched Domain.
- [[apps-lets-encrypt]] — the paid app that owns the automatic SSL path.
- [[merchant-roles]] — `settings.domains` permission grants access to this whole surface.

## Open Questions

None — relationship-level edges captured.
