---
type: feature
nav_path: "Settings → PAT Tokens → Advanced Settings (validity + IP allowlist)"
route_name: pat-tokens.settings
route_path: /admin/settings/pat-tokens
aliases: ["PAT IP restrictions", "PAT CIDR allowlist", "PAT expiration", "No expiration toggle", "Token Validity", "allowed_ips", "expires_at"]
tags: [settings, security, tokens, ip-allowlist, cidr, expiration]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-pat-tokens]]. See the hub for related aspects (list view, create flow, scopes, security, permissions, endpoints).

# PAT Tokens — expiration and IP allowlist

## Purpose

The **Advanced Settings** section of the create / edit modal hosts the two optional defence-in-depth controls on a PAT token: **Token Validity** (an expiration date or a "No expiration" toggle) and **IP Restrictions** (a per-token CIDR allowlist). Both are evaluated on every PAT-authenticated request — see [[settings-pat-tokens-endpoints]] for the validation chain.

## Where to find it

Inside the [[settings-pat-tokens-create-flow|Create / Edit modal]] → **Advanced Settings** section (collapsible `SettingsCard`). The section is collapsed by default; the merchant expands it to set expiration or IP restrictions.

## What the merchant can do here

### Token Validity

- **Date-range picker** (`CcTimePeriod`, `type=date`, `single=false`):
  - Start date defaults to today.
  - **No expiration** toggle — when ON, `expires_at` is set to `null` and the date picker is hidden. **Default for new tokens: ON.**
  - When OFF, the end date picker is enabled and the merchant picks an expiry date (must be in the future).

### IP Restrictions

`CliTokensIpRestrictions` component, inside the Advanced Settings panel. Default state: empty list (no restrictions = token works from any IP).

**UI elements**:

- Label *"IP Restrictions"* + grey *"(Optional)"* suffix.
- Help text: *"Restrict token usage to specific IP addresses or CIDR ranges. Leave empty to allow all IPs."*
- Per-IP row: a `CcInput` (placeholder *"e.g., 192.168.1.0/24 or 10.0.0.1"*) + a `DeleteComponent` (icon `fal fa-times-circle`) with the confirm message *"Remove this IP address?"*.
- **Add IP Address** button (secondary, with `+` icon-left). Disabled when `localIps.length >= maxIps`. When the cap is hit, shows the inline message *"Maximum 20 IPs allowed"*.
- **Help block** at the bottom (light-grey box) with examples:
  - `192.168.1.100` → *"Single IP address"*
  - `192.168.1.0/24` → *"CIDR range (256 addresses)"*
  - `10.0.0.0/8` → *"Large network range"*

## Settings & fields

| Field | Validation | Notes |
|-------|------------|-------|
| `expires_at` | `date \| after:now`, nullable | Must be a future date if set; null means no expiration. |
| `allowed_ips` | array of strings, nullable, ≤ 20 entries | Each entry must match IPv4 / IPv4-CIDR / IPv6 / IPv6-CIDR. |

### Per-row IP validation (client-side)

When the merchant types in an IP field, the value is regex-checked against:

- **IPv4** — `A.B.C.D` with octets 0–255.
- **IPv4-CIDR** — `A.B.C.D/N` with bits 0–32.
- **IPv6** — simplified pattern.
- **IPv6-CIDR** — bits 0–128.

Invalid format → red error text under the row: *"Invalid IP address or CIDR range"*. Empty rows are filtered out before emit (so the merchant can have an empty row while typing without it being committed to the saved list).

### Server-side validation (Form Request)

- `allowed_ips`: max **20** entries — *"Maximum of 20 IP addresses allowed"*.
- `expires_at`: must satisfy `date|after:now` — cannot create a token with an already-past expiration date.

The config sets `max_expiry_days: 365` as a default, but this is **NOT wired into the validation rules** — practically there is no maximum expiration window enforced at the request layer.

## Business rules

### Expiration

- **No expiration is the default.** New tokens default with the "No expiration" toggle ON. CloudCart's UX surfaces the expiration option prominently but does not require it.
- **Future-only.** `expires_at` must be `after:now` at both create and update time — you cannot retroactively expire a token by setting a past date. To revoke immediately, the merchant deletes the token (preferred) or toggles `active=false`.
- **Token rejected on expiry.** The `valid` scope used by `findByRawToken` filters out expired tokens — once `expires_at < now`, the API gateway returns 403 without further checks (no IP / scope evaluation needed). See [[settings-pat-tokens-endpoints]].
- **No expiration warning.** There is no automated reminder email when a token is about to expire (verify whether this exists).
- **Update can null out expiration.** On a partial PUT, the merchant can set `expires_at` to null to convert a time-bound token into a permanent one — see [[settings-pat-tokens-endpoints]] for the partial-update behaviour.

### IP allowlist

- **Empty = no restriction.** A token with `allowed_ips=[]` (or `null`) works from any IP. This is the default and matches the platform's "you may not know the IP at create time" reality.
- **CIDR for whole subnets.** The CIDR allowlist accepts up to 20 entries per token. CIDR notation (e.g., `192.168.1.0/24` for a 256-address subnet, `10.0.0.0/8` for a large internal network) lets the merchant lock a token to an entire office network with one entry — contrast with [[settings-banned-ip]] which requires individual IPs.
- **IPv6 supported throughout.** Both IP allowlist entries and the per-request IP check support IPv6:
  - The IP allowlist validator accepts IPv6 addresses and IPv6 CIDR (0–128 bits).
  - The middleware compares the request's IP against allowed entries using `filter_var(...FILTER_FLAG_IPV6)` + bytewise prefix match for CIDR.
  - The token's `last_used_ip` column stores either IPv4 or IPv6 — whichever the request came from.
- **20 entries per token.** Beyond that the Form Request rejects with *"Maximum of 20 IP addresses allowed"*. Plenty for typical CI / office subnet use, but merchants with fragmented IP situations (many small networks rather than one CIDR block) may need to consolidate into broader CIDR ranges or use multiple tokens.
- **Failed IP match returns 403 IP_NOT_ALLOWED.** The token is otherwise valid (hash matches, active, not expired) — the rejection is specifically because the request IP isn't in the allowlist. **Crucially: `recordUsage` is NOT called on this rejection** — so `last_used_at` stays unchanged, and "last used" remains a reliable proxy for "is this token actively in use and working", not just "is someone trying it".
- **Use case: CI / office lockdown.** A token for a build server is locked to that server's IP (or its NAT egress range). A token for a developer's office is locked to the office subnet via one CIDR entry. A token for an unknown future caller (e.g., a third-party integrator) is left unrestricted.

## Related

- [[settings-pat-tokens]] — hub.
- [[settings-pat-tokens-create-flow]] — modal that hosts Advanced Settings.
- [[settings-pat-tokens-endpoints]] — validation rules and the `valid` scope that gates auth.
- [[settings-pat-tokens-security]] — why these checks matter (no brute-force throttle at the PAT layer).
- [[settings-banned-ip]] — store-level IP blocklist; separate from per-token allowlist (requires individual IPs, not CIDR).

## Open questions

- Does the platform send any reminder email or notification when a token is about to expire? `(verify)`
- Is the `max_expiry_days: 365` config value ever wired into validation, or is it purely informational? `(verify)`
