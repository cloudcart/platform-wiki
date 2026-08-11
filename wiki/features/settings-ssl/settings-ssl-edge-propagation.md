---
type: feature
nav_path: "Settings → Domains → SSL → Edge propagation"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["SSL edge propagation", "Cloudflare custom-hostname SSL", "gcloud_pending", "Pending SSL propagation", "CloudCart subdomain wildcard", "SSL after install delay"]
tags: [settings, ssl, certificate, cloudflare, gcloud, edge, infrastructure]
plan_gates: ["ssl_certificate"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-ssl]]. See the hub for the other aspects (automatic install, manual install, auto-renewal, expiry fallback, troubleshooting).

# SSL — Edge propagation (Cloudflare + GCloud)

## Purpose

When a certificate is installed (Automatic or Manual) or renewed, the **cert record is stored locally first** and then **pushed to the edge** — Cloudflare's custom-hostname API (for Cloudflare-mode domains) and Google Cloud's load balancer. Until propagation completes, HTTPS at the edge may still serve the OLD cert (or, for a fresh install, a generic edge cert that doesn't match the merchant's domain), causing brief HTTPS warnings.

This page explains what those propagation flags mean, how long they typically take, and how the CloudCart subdomain's own platform-managed wildcard cert relates.

## Where to find it

The propagation flags are NOT surfaced in the SSL modal — the merchant sees only "success" on install and may then wonder why HTTPS doesn't work immediately. This page exists to answer "why does my cert show installed but the storefront still has a warning?" tickets.

The merchant sees only:

- The install success toast.
- The Manage state of the modal showing the cert details immediately.
- The browser's HTTPS-warning behaviour during the brief propagation window.

## What the merchant can do here

### Wait briefly after install / renewal

Typical edge propagation: **under a minute** for Cloudflare custom-hostname push. The merchant should:

1. Install the cert (Automatic or Manual).
2. Wait roughly 30–60 seconds before testing HTTPS in a fresh browser (clear caches if needed).
3. If still warning after a few minutes, see [[settings-ssl-troubleshooting]] for diagnostic steps.

### Understand the CloudCart subdomain's role

The `*.cloudcart.net` subdomain (e.g., `mystore.cloudcart.net`) uses a **wildcard certificate managed by CloudCart's infrastructure**. The merchant does NOT manage that cert through the SSL modal — it is always automatically valid and renewed by CloudCart's platform team. This is what makes the expiry fallback (see [[settings-ssl-expiry-fallback]]) work seamlessly: when a custom-domain cert expires, the storefront falls back to the subdomain whose wildcard cert is always valid.

### Verify the cert is serving correctly

Once propagation has completed, the merchant can:

- Visit the custom-domain storefront in a fresh browser session — no warning expected.
- Use a third-party SSL checker (e.g., SSL Labs) to confirm the served cert matches the one installed in the modal.

There is **no in-modal "verify edge" button** — the merchant relies on out-of-band checking.

## Settings & fields

This aspect has no merchant-facing form fields. The relevant cert-record flags are:

| Flag | Set when | Cleared when | Meaning |
|------|----------|--------------|---------|
| `pending` | Cert installed/renewed. | Background worker confirms Cloudflare push. | Cloudflare custom-hostname API push is in flight. |
| `gcloud_pending` | Cert installed/renewed. | Background worker confirms GCloud LB push. | Google Cloud load-balancer push is in flight. |
| `free` | Cert installed. | (Cleared only on Remove.) | `1` = Let's Encrypt, `0` = external. Drives renewal eligibility — see [[settings-ssl-auto-renewal]]. |

These are internal — not shown in the modal — but they explain WHY a freshly installed cert may take seconds to serve at the edge.

## Business rules

### Cloudflare Custom-Hostname mode — separate push

When the domain is in Cloudflare's Custom-Hostname mode (see [[settings-domains]]'s Cloudflare-for-SaaS path), installing a cert on the SSL modal does NOT immediately make HTTPS work at the Cloudflare edge. The cert is stored locally with `pending=1` and `gcloud_pending=1`; a separate background process pushes it to Cloudflare's custom-hostname API.

Until propagation completes, HTTPS requests at the edge fall back to Cloudflare's own serving cert (which doesn't match the merchant's domain), causing browser warnings. The modal does NOT show the propagation flags — the merchant sees "success" on install and just has to wait briefly before testing.

### GCloud LB push runs in parallel

For domains routed through Google Cloud Load Balancer in addition to (or instead of) Cloudflare, the `gcloud_pending` flag tracks the GCloud-side propagation. The two pushes run in parallel; both flags must clear before the cert is fully propagated.

### Renewal also fires both pushes

A renewal ([[settings-ssl-auto-renewal]]) re-stores the cert with `pending=1` and `gcloud_pending=1` exactly as on first install. The previous-cycle cert is still valid (within 25 days of expiry), so the storefront stays serving without warnings during the brief push overlap.

### CloudCart subdomain wildcard — separate cert, platform-managed

The store's `*.cloudcart.net` subdomain (assigned at store creation) uses a wildcard cert that:

- Is provisioned and rotated by CloudCart's infrastructure team, NOT by anything in the SSL modal.
- Covers every store's subdomain simultaneously.
- Is not visible in the merchant's SSL modal — only the merchant's CUSTOM domains have rows on [[settings-domains]] with the SSL action.

This wildcard is what enables the seamless fallback when a custom-domain cert expires — the subdomain HTTPS endpoint is always valid, so [[settings-ssl-expiry-fallback]] can safely point the primary back at it without breaking the storefront.

### Side effects on install / remove at the edge

- **Install** — cert + chain + key stored locally; `pending=1` and `gcloud_pending=1` set; background push starts. Cloudflare custom-hostname binding is updated to use the new cert. Storefront serves HTTPS on next request once the push completes (typically under a minute).
- **Remove** — cert record deleted; the domain's `ssl` flag flips to no. Cloudflare's binding reverts (`(verify)` whether the binding is deleted or merely downgraded to no-SSL). Mis-cached edge nodes may briefly serve the OLD cert.

### Removing a free cert does NOT revoke at Let's Encrypt

When the merchant clicks Remove on a Let's Encrypt cert, the platform deletes its local DB record and flips the host's SSL flag off. But the issued cert remains valid at Let's Encrypt's CA (and in any certificate-transparency logs / cached infrastructure) until its natural 90-day expiry. There is no ACME `revokeCert` call.

Practical implication: a "removed" Let's Encrypt cert may still be served briefly by mis-cached infrastructure outside CloudCart's control. For **true revocation** (e.g., compromised private key on a manual cert export), the merchant needs to contact CloudCart support to perform an explicit ACME revoke for Let's Encrypt certs, or contact the external CA directly for manual certs.

### `gcloud_pending` is independent of `pending`

The two flags are independent — Cloudflare and GCloud propagation can complete in either order. Both must clear before the cert is considered fully propagated. The merchant cannot distinguish "pending at Cloudflare" from "pending at GCloud" in the UI; the symptom is identical (edge cert mismatch warning).

## Related

- [[settings-ssl]] — hub.
- [[settings-domains]] — where Cloudflare Custom-Hostname mode is configured per domain.
- [[settings-ssl-automatic-install]] — install path that triggers Cloudflare + GCloud push.
- [[settings-ssl-manual-install]] — Manual install also triggers the same push pipeline.
- [[settings-ssl-auto-renewal]] — every successful renewal re-triggers the push.
- [[settings-ssl-expiry-fallback]] — relies on the CloudCart subdomain wildcard being always-valid.

## Open questions

- On Remove, does Cloudflare's custom-hostname binding for the domain get fully deleted, or merely downgraded to a no-SSL state until a new cert is installed? `(verify)`
- Is there a merchant-visible diagnostic (or support-side button) to force-trigger an immediate edge push after install, rather than waiting for the background worker? `(verify)`
