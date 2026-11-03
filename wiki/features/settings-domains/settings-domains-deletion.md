---
type: feature
nav_path: "Settings → Domains → Deletion + uniqueness"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Delete domain", "Remove domain", "Deactivate domain", "Domain uniqueness", "Domain already exists", "Domain delete asymmetric", "Cleanup on host deletion"]
tags: [settings, domains, deletion, cleanup, uniqueness]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-domains]]. See the hub for related aspects (add flow, DNS / Cloudflare, SSL, primary, plan gates).

# Domains — Deletion + uniqueness

## Purpose

What happens when the merchant removes a domain from the table, what gets cleaned up automatically, why deletion behaves differently for external vs CloudCart-purchased domains, and why the same domain can never belong to two stores. Also covers the **Deactivate** toggle (a softer alternative to Remove that preserves the row but takes the domain out of service).

## Where to find it

Settings → Domains → per-domain row → **Remove** action (the trash / delete icon) and the **Active** toggle. Both open the shared `ConfirmModal` with action-specific titles before doing anything destructive.

## What the merchant can do here

- **Deactivate** (toggle Active off) — opens *"Deactivate domain?"* confirmation. Preserves the row but stops serving customers on this domain. The primary domain cannot be deactivated (see [[settings-domains-primary]]).
- **Remove** (trash icon) — opens *"Are you sure?"* — *"Removing the domain will deactivate its DNS records and SSL certificate."* with a danger-styled confirm button. On confirm, the platform performs the cleanup described in Business rules below.

If the backend returned a `confirmError` from a prior attempt, an inline `info-box-error` panel appears at the top of the ConfirmModal.

## Settings & fields

| Field / Toggle | Meaning |
|---|---|
| **Active** toggle | `is_active`. On = serves customers; off = preserved but not serving. |
| **Remove** action | Triggers the delete endpoint — behaviour depends on `external` value (see below). |

## Business rules

### Deletion safety — what the merchant must do first

A domain can be removed from this screen only if:

- It is NOT the current primary domain. The primary must be reassigned first — see [[settings-domains-primary]].
- It has no in-flight purchases / pending operations.

For CloudCart-purchased domains: removing the domain from this page does NOT automatically cancel the underlying registration with the registrar. The domain continues to exist at the registrar level. Merchants who want to fully cancel a purchase or transfer the domain elsewhere should contact CloudCart support — see "Domain delete is asymmetric" below for the underlying reason.

### Removing a domain also removes its DNS / certificate

When the merchant deletes a domain from this page, the platform automatically:

1. Removes the Cloudflare DNS records associated with that domain.
2. Removes the Cloudflare Custom Hostname binding if one existed (see [[settings-domains-dns-cloudflare]]).
3. Deletes the associated SSL certificate record (a row is also inserted into `deleted_certificates` for the audit trail — see [[settings-domains-ssl]]).
4. Invalidates the router cache for the site (the platform code).

Failures from Cloudflare during cleanup are swallowed silently — the local row is removed regardless. Practically: re-adding the same domain later starts from scratch (no DNS history is preserved), so **if the merchant has custom DNS records they want to keep, they should export / record them before removing the domain**.

### Domain delete is asymmetric — external vs CloudCart-purchased

The delete endpoint only actually performs the deletion when `host.external == 'yes'`:

- **External domains** (`external=yes`): full delete — model row deleted, Cloudflare DNS records removed, Cloudflare Custom Hostname binding removed (if any), certificate record deleted, route-cache invalidated. Cloudflare-side failures are swallowed (the local row is removed regardless).
- **CloudCart-purchased domains** (`external=no`, `cloudcart=1`): the delete endpoint is essentially a **no-op at the application level** — the host row is NOT removed (the code condition the platform code is false for a non-external CloudCart-purchased domain). Practical implication: **to remove a CloudCart-purchased domain the merchant must contact support.**

For a CloudCart-purchased domain that the merchant transferred externally (now `external=yes`, `cloudcart=1`), the delete will work normally.

### Cleanup also fires on model boot — bypass-resistant

When the platform deletes a host row, model lifecycle hooks fire to:

1. Remove the Cloudflare DNS / zone bindings.
2. Remove the Cloudflare Custom Hostname binding if one existed.
3. Cascade-delete the related Certificate row.
4. Invalidate the router cache for the site (the platform code).

So even if the application-level controller is bypassed (e.g., ops scripts manage host rows directly), deleting via the model still cleans up. The lifecycle is the same.

### Same domain can NOT belong to two stores — platform-wide uniqueness

Adding an existing domain runs the platform code against the global `hosts` table — any match (in any other store) blocks the add with *"Domain already exists in system"*. This is enforced platform-wide; the `hosts` table is shared.

The check also matches the `www.` variant against the bare form (and vice versa) — so a merchant can't sneak in `www.example.com` if another store has `example.com`. The same uniqueness applies after deletion: once a domain is removed from store A, it becomes available for store B to add (or for store A to re-add).

### Deactivate vs Delete — when to use which

| Scenario | Recommended action |
|---|---|
| Temporarily taking the domain out of service (e.g., during a brand migration) | **Deactivate** — preserves the configuration so re-activating is one click. |
| Permanently removing an external domain the merchant no longer owns or wants attached | **Remove** — full cleanup. |
| Removing a CloudCart-purchased domain | Contact support (Remove is a no-op for non-external domains). |
| Freeing the domain so another store can attach it | **Remove** — until removed, the platform-wide uniqueness check blocks the other store. |

### Confirmation modals — exact titles

| Action | Title | Message |
|---|---|---|
| **Deactivate** | *"Deactivate domain?"* | (Per-instance message text.) |
| **Remove** | *"Are you sure?"* | *"Removing the domain will deactivate its DNS records and SSL certificate."* — danger-styled confirm button. |

## Related

- [[settings-domains]] — hub.
- [[settings-domains-primary]] — primary cannot be deleted / deactivated.
- [[settings-domains-dns-cloudflare]] — Cloudflare bindings that get cleaned up.
- [[settings-domains-ssl]] — `DeletedCertificate` audit row written during cert cleanup.
- [[settings-domains-add-flow]] — the "Domain already exists" error that the platform-wide uniqueness check produces during Add.
- [[domain]] — entity page.

## Open questions

None.
