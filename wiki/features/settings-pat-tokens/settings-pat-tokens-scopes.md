---
type: feature
nav_path: "Settings → PAT Tokens → Permissions / Scopes"
route_name: pat-tokens.settings
route_path: /admin/settings/pat-tokens
aliases: ["PAT scopes", "CLI token scopes", "Read Only token", "Full Access token", "Custom Permissions token", "cli_scopes.php", "Scope selector wizard"]
tags: [settings, security, tokens, scopes, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[settings-pat-tokens]]. See the hub for related aspects (list view, create flow, restrictions, security, permissions, endpoints).

# PAT Tokens — scope selector and scope catalog

## Purpose

The **Permissions** section of the create / edit modal lets the merchant pick the token's authorisation surface. Backed by the `CliTokensScopeSelector.vue` component, it surfaces three Access Levels as large clickable cards (Read Only / Full Access / Custom Permissions) and translates the merchant's selections into the platform's two-tier scope model defined in the platform code.

It also lists the scope catalog.

## Where to find it

Inside the [[settings-pat-tokens-create-flow|Create / Edit modal]] → **Permissions** section (`SettingsCard "Permissions"`). The scope selector is required: validation rejects any token with zero scopes.

## What the merchant can do here

### Three Access Level cards (radio behaviour)

| Card | Visual badge | Description |
|------|--------------|-------------|
| **Read Only** (default) | Green *"Recommended"* pill | *"View-only access to all resources. No modifications allowed. Safe for monitoring and reporting."* |
| **Full Access** | none | *"Complete read and write access to all store resources. Best for CI/CD pipelines and full automation."* |
| **Custom Permissions** | none | *"Select specific resources and permissions. Best for limited access scenarios."* |

Picking **Read Only** emits `['read-only']`; **Full Access** emits `['full-access']`; **Custom Permissions** opens an inline expansion below the cards.

### Custom Permissions panel (visible only when Custom is selected)

9 resource rows: Products, Orders, Customers, Inventory, Discounts, Blog, Settings, **Metaobjects** (*"Manage metaobject entries"*), Webhooks, each with a description and a **None** / **Read** / **Read & Write** control. **Read** is offered on every row, but Inventory and Discounts have no read-only scope: picking it there makes **Generate Token** fail with *"The given data was invalid."* and no field message ([[settings-pat-tokens-create-flow]]). Use **Read & Write** or **None** for those two.

**Quick actions** at the bottom (ghost buttons): **Select all as Read**, **Select all as Read & Write**, **Clear all**.

### How selections translate to emitted scopes

The component emits scopes as an array: *None* → no entry for that resource; *Read* → emits `<resource>:read` (e.g., `products:read`); *Read & Write* → emits `<resource>` (no suffix, e.g., `products`). If the merchant clears every resource to None, the component **defensively emits `['read-only']`** to ensure ≥1 scope is always present.

**UX detail**: clicking the **Custom Permissions** card initially does NOT emit anything — it initialises the grid to all-None and waits for the merchant to pick. Submitting without picking would emit only the defensive fallback.

## Settings & fields — the full scope catalog

The platform defines two scope tiers in the platform code:

### Primary scopes (mutually exclusive — pick ONE)

| Key | Name | Description | Allows write? |
|-----|------|-------------|---------------|
| `full-access` | Full Access | Complete read/write access to all resources | yes |
| `read-only` | Read Only | Only GET requests allowed across all resources | no |

A token with a primary scope behaves like a global key constrained by HTTP method.

### Granular scopes (combine multiple)

| Key | Name | Resource | Read-only variant |
|-----|------|----------|-------------------|
| `products` | Products (full) | `products` | `products:read` |
| `orders` | Orders (full) | `orders` | `orders:read` |
| `customers` | Customers (full) | `customers` | `customers:read` |
| `settings` | Settings (full) | `settings` | `settings:read` |
| `blog` | Blog (full) | `blog` | `blog:read` |
| `webhooks` | Webhooks (full) | `webhooks` | `webhooks:read` |
| `metaobjects` | Metaobjects | `metaobjects` | `metaobjects:read` |
| `inventory` | Inventory | `inventory` | none |
| `discounts` | Discounts | `discounts` | none |

9 resource families, 7 with both read+write variants, 2 (`inventory`, `discounts`) with full-access only. A token can mix granular scopes (e.g., `orders:read + customers:read + products`) for narrow least-privilege automation.

### Resource → scope mapping (URL path prefix → required scope)

When the API gateway authenticates a request, it maps the URL path to the required scope via `config('cli_scopes.resource_mapping')`. Examples:

- `products`, `categories`, `tags`, `vendors`, `variant-parameters`, `properties`, `bundles` → `products` scope.
- `product-inventory`, `inventory`, `stock` → `inventory` scope.
- `orders`, `order` → `orders` scope.
- `customers`, `customer-groups`, `subscribers` → `customers` scope.
- `discounts`, `promotions`, `coupons` → `discounts` scope.
- `blog`, `articles` → `blog` scope.
- `settings/general`, `settings/payments`, `settings/shipping`, `settings/taxes`, `settings/notifications`, `settings/languages`, `settings/legal`, `domains`, `admins`, `api_keys` / `api-keys`, `seo` → `settings` scope.
- `notifications`, `account`, `cli-tokens`, `auth`, `dashboard` → `null` (any authenticated token).


### On the Admin GraphQL API

The same scopes hold on `/api/gql`. There the scope follows the operation's permission section rather than the address. The table and the refusals are on [[admin-graphql-api]].

## Business rules

- **Mutually exclusive tiers.** A token MUST pick exactly one mode: a primary scope (full or read-only across everything), OR one-or-more granular scopes (combine specific resource family permissions). The validator (both in the Form Request `withValidator` and in the service's `validateScopes`) rejects:
  - `full-access` AND `read-only` together → error.
  - Any primary scope mixed with any granular scope → error.
  - Conflicting `full-access` + specific granular scopes → error (same rule).
- **At least one scope.** Empty arrays fail validation. The defensive fallback in `CliTokensScopeSelector` ensures the emitted array is never empty even when Custom mode has all resources set to None.
- **Read-Only is the default.** The first card is pre-selected and tagged *"Recommended"* — CloudCart's design encourages minimum-privilege tokens.
- **No owner-permission filter.** Earlier wiki text suggested moderators could only grant scopes they themselves have. This is **not** how the platform actually works — moderators cannot create tokens at all (see [[settings-pat-tokens-permissions]]). The owner can grant **any** scope from the full catalog.
- **No `:read` variant for `inventory` and `discounts`.** A token that only reads stock or discounts still needs the full scope. The selector's **Read** on those rows is refused at save.

## Related

- [[settings-pat-tokens]] — hub.
- [[settings-pat-tokens-create-flow]] — modal that hosts the scope selector.
- [[settings-pat-tokens-endpoints]] — `/scopes` endpoint returns the catalog; validation rules reject illegal combinations.
- [[settings-pat-tokens-permissions]] — owner-only creation; no per-permission scope filtering.
- [[settings-api-keys]] — store-level keys with NO scope model (every API key has full store access within its rate limit) — contrast with PAT scopes.

## Open questions

- Are there any scope changes planned for additional resources (e.g., `themes`, `apps`, `domains`-management beyond settings)? `(verify)`
- How is the `notifications` → `null` mapping intended to interact with rate-limit-sensitive notification endpoints? `(verify)`
