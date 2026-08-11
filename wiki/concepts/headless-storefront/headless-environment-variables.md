---
type: concept
nav_path: "Concept → Headless storefronts → Environment variables"
aliases: ["Nitrogen env vars", "Production environment", "Preview environment", "System variables", "Custom variables", "Secret variables", "PUBLIC_STOREFRONT_API_TOKEN", "PUBLIC_STORE_DOMAIN", "SESSION_SECRET", "PUBLIC_STOREFRONT_ID", "SHOP_ID", "max_env_variables_per_storefront"]
tags: [nitrogen, headless, environment-variables, configuration, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, deployment methods, Nova platform, Storefront API, customer accounts, legacy-vs-Nitrogen surfaces).

# Headless — environment variables

## Definition

Every Nitrogen storefront has an **Environments & Variables** tab on [[nitrogen-storefront-overview]] that defines what runtime variables the deployed Worker sees. Variables come in two **environments** (production + preview) and three **kinds** (system, custom, secret) — see Where it applies for the matrix.

Variables flow to Nova on every deployment. For GitHub-mode storefronts, the same variables are also written as **repository secrets** so the GitHub Actions workflow can build with them — see [[headless-deployment-methods]].

## Scope

Covered:

- Production vs preview environments + the "All Environments" option.
- System (read-only), custom (merchant-managed), and secret (masked) variables.
- The full list of platform-managed system variables.
- The 50-custom-variable cap (`limits.max_env_variables_per_storefront`).
- The naming rules custom keys must follow.
- Why `SESSION_SECRET` is **never** rotated.

Not covered:

- How variables get pushed to Cloudflare KV / Workers — see [[headless-nova-platform]].
- How GitHub mode stores them as repo secrets — see [[headless-deployment-methods]].
- The Customer Account API client-id / API URL — see [[headless-customer-accounts]].

## Contrasts

- **Production vs preview** — production variables apply to the production-branch Worker; preview applies to all other branches' preview deployments. A variable set to "All Environments" covers both.
- **System vs custom vs secret** — system variables are platform-managed and read-only. Custom variables are merchant-managed and editable. Secret variables are custom variables with the "Secret" checkbox ticked — their values are masked in the admin UI after save.
- **System variables don't count toward the 50-var cap.** Only custom variables do.

## Where it applies

### Two environments

- **Production** — variables that apply to the production branch (typically `main`). The Worker on the production Cloudflare namespace reads these.
- **Preview** — variables that apply to all other branches' preview deployments. The Worker on the preview Cloudflare namespace reads these.
- **All Environments** — a single variable can cover both (set once, applies in both namespaces).

See [[headless-nova-platform]] for the namespace mechanics.

### Three variable kinds

**System variables** (read-only, platform-managed) — auto-populated when the storefront is created. The merchant cannot modify or delete these. Always include:

- `PUBLIC_STOREFRONT_API_TOKEN` — the public Storefront API token (see [[headless-storefront-api]]).
- `PUBLIC_STORE_DOMAIN` — the Nova hostname or the merchant's primary domain.
- `PUBLIC_STOREFRONT_ID`
- `SHOP_ID`
- `SESSION_SECRET` — 32-byte random secret, generated once at creation, NEVER rotated.

When customer accounts are enabled (see [[headless-customer-accounts]]), also:

- `PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID`
- `PUBLIC_CUSTOMER_ACCOUNT_API_URL`

**Custom variables** (merchant-managed) — variables the merchant adds for their app (e.g., `STRIPE_PUBLISHABLE_KEY`, `ALGOLIA_APP_ID`, `SENTRY_DSN`). Up to `limits.max_env_variables_per_storefront` per storefront (default **50**). Key naming rules:

- Must start with a letter.
- Must contain only uppercase letters, numbers, and underscores.

**Secret variables** — custom variables with the "Secret" checkbox ticked. Their values are masked in the admin UI (shown as `********************`) — the merchant can't see them after saving, only update or delete. The stored value itself IS recoverable by the deployed Worker at runtime (it's not hashed; it's encrypted at rest and decrypted into the Worker's env).

### `SESSION_SECRET` is NEVER rotated

The `SESSION_SECRET` system variable is generated **once** at storefront creation and is **NEVER overwritten** — rotating it would invalidate every active customer session on the deployed storefront. The merchant cannot rotate it from the admin (the variable is system-managed and read-only).

This makes `SESSION_SECRET` an exception to the usual "rotate-on-suspicion" pattern. If the merchant believes the SESSION_SECRET has leaked, the only recourse is to delete + recreate the storefront (which forces re-login of every customer).

### Variable push to Nova

Variables are pushed to Nova on the **next deployment** — not immediately when saved. So the order of operations is:

1. Merchant edits a variable on the Environments & Variables tab.
2. Save persists the value in CloudCart.
3. Next deploy (CLI or GitHub-triggered) pushes the updated value into the Cloudflare Worker.

For GitHub mode, the save also writes the variable into the merchant's repo as a GitHub repository secret — so the Actions workflow at the next push can build with the right value. See [[headless-deployment-methods]] for the GitHub-side mechanics.

### 50-variable cap — global, NOT per-plan

The platform enforces `limits.max_env_variables_per_storefront` (default 50) across **all** plans that have Nitrogen access. System variables don't count toward this limit. Same as the storefront-count cap, this is a global platform configuration, NOT plan-tier-tunable (see [[headless-nitrogen-overview]] for the three caps).

### Naming validation

Custom variable keys are validated server-side:

- Reject lowercase letters: `stripe_key` → error.
- Reject leading digit / underscore: `1KEY`, `_KEY` → error.
- Reject special chars: `STRIPE-KEY`, `STRIPE.KEY` → error.
- Accept: `STRIPE_KEY`, `API_URL_V2`, `MY_CUSTOM_THING_123`.

This matches the Cloudflare Workers env-var naming convention.

### Editing flow

The merchant can:

- **Add** a custom variable with key, value, environment (production / preview / all), and Secret flag.
- **Edit** the value of an existing custom variable (the key is immutable — to rename, delete and recreate).
- **Toggle Secret** on an existing variable.
- **Delete** a custom variable.

System variables show a lock icon and have no edit affordance — the value is visible (except `SESSION_SECRET`, which is masked) but read-only.

### When a custom variable shadows a system variable

If the merchant names a custom variable identically to a system variable, the platform rejects it at save time (key collision) (verify). The merchant cannot override the platform-managed values.

## Related

- [[headless-storefront]] — hub.
- [[headless-nova-platform]] — production vs preview Cloudflare namespaces.
- [[headless-deployment-methods]] — GitHub mode also writes vars as repo secrets.
- [[headless-storefront-api]] — `PUBLIC_STOREFRONT_API_TOKEN` is the auto-injected token.
- [[headless-customer-accounts]] — `PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID` + `_URL` system vars when customer accounts are enabled.
- [[headless-nitrogen-overview]] — the three `limits.*` platform caps.
- [[nitrogen-storefront-overview]] — Environments & Variables tab UI.

## Open Questions

- Whether secret values are encrypted at rest with the application framework's `encrypted` cast or a different mechanism (verify).
- Behaviour when a custom variable's name matches a system variable (assumed reject — verify).
- Whether key length has a server-side cap (Cloudflare Workers caps env values at 5 KB — verify if CloudCart enforces a tighter limit).
