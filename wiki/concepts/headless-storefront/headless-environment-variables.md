---
type: concept
nav_path: "Concept → Headless storefronts → Environment variables"
aliases: ["Nitrogen env vars", "System variables", "Read-only variables", "Custom variables", "Secret variables", "PUBLIC_STOREFRONT_API_TOKEN", "PRIVATE_STOREFRONT_API_TOKEN", "PUBLIC_STORE_DOMAIN", "PUBLIC_API_ORIGIN", "SESSION_SECRET", "max_env_variables_per_storefront", "batchSetNitrogenEnvironmentVariables", "cloudcart nitrogen env push", "Променливи на витрината"]
tags: [nitrogen, headless, environment-variables, configuration, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 5
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, deployment methods, Nova platform, Storefront API, customer accounts, legacy-vs-Nitrogen surfaces).

# Headless — environment variables

## Definition

Every Nitrogen storefront has an **Environments and variables** tab on [[nitrogen-storefront-overview]] that defines what the deployed worker reads from `env`. Variables are **read-only** (set by CloudCart) or **custom** (the merchant's), and a custom variable may be a **secret**.

The page says how they reach the storefront: *"The variables are bound to the storefront when it is deployed: a change takes effect with the next deploy."* Nothing is written to GitHub for them, whichever way the storefront deploys.

## Scope

Covered:

- The read-only names, and the rule that keeps them.
- The custom-variable rules: key format, the 50-variable cap, secrets.
- Setting many at once: `batchSetNitrogenEnvironmentVariables` and `cloudcart nitrogen env push`.
- Why `SESSION_SECRET` does not change.

Not covered:

- The deploy that binds them — see [[headless-deployment-methods]].
- The screen around them — see [[nitrogen-storefront-overview]].

## Contrasts

- **All environments vs Production** — the **Environment** select offers these two, and only production is served (see [[headless-nova-platform]]), so today they reach the same storefront.
- **Read-only vs custom vs secret** — read-only variables are the platform's. Custom variables are the merchant's. A secret is a custom variable with **Secret** on: *"Its value is hidden in the admin once saved."*
- **Read-only variables don't count toward the 50-variable cap.** Only custom ones do.

## Where it applies

### Read-only variables

*"Set by CloudCart for every environment of this storefront."*

| Name | What it is |
|---|---|
| `PUBLIC_STOREFRONT_API_TOKEN` | The public Storefront API token (see [[headless-storefront-api]]). |
| `PRIVATE_STOREFRONT_API_TOKEN` | The private Storefront API token. Shown masked. |
| `PUBLIC_STORE_DOMAIN` | The store's domain; the routed domain while one is routed. |
| `PUBLIC_API_ORIGIN` | Present only while a domain is routed: `https://` plus the store's main host, so the storefront's server calls the API directly rather than looping back into its own worker. |
| `SESSION_SECRET` | Generated once, at creation. Shown masked. |
| `PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID`, `PUBLIC_CUSTOMER_ACCOUNT_API_URL` | Only for a storefront whose customer account was set up before that tab was removed. Sign-in does not read them (see [[headless-customer-accounts]]). |

`PUBLIC_STOREFRONT_ID` and `SHOP_ID` are no longer written, and those names are free for a custom variable. A deployed storefront keeps them until its next deploy.

No custom variable takes a system name, in any environment. The save is refused with *"System variables cannot be modified"*.

### Custom variables

**Add variable** asks for **Key**, **Value**, **Environment** and **Secret**. The key's help reads *"Upper-case letters, digits and underscores, starting with a letter."*

The key is trimmed and upper-cased before it is checked, then must match `^[A-Z][A-Z0-9_]*$`, at most 255 characters:

- `stripe_key` is accepted and stored as `STRIPE_KEY`.
- `1KEY`, `_KEY`, `STRIPE-KEY` and `STRIPE.KEY` are refused: *"Variable key must start with a letter and contain only uppercase letters, numbers, and underscores"*.

A key that already exists in that environment has its value replaced. To rename a variable, delete it and add the new key. Deleting asks: *"Delete this variable? The deployed storefront keeps it until its next deploy."*

### 50 custom variables per storefront

A new key past the cap is refused: *"Maximum of 50 custom environment variables allowed per storefront"*. Every plan with Nitrogen has the same cap (see [[headless-nitrogen-overview]]).

### Secrets

The admin never shows a secret's value: not a custom secret, not `SESSION_SECRET`, not `PRIVATE_STOREFRONT_API_TOKEN`. The page says: *"A secret's value stays hidden here; cloudcart nitrogen env pull writes it to.env."* The deployed worker reads it from `env` like any other variable.

### `SESSION_SECRET` does not change

`SESSION_SECRET` is generated once and never overwritten, because changing it would end every active customer session on the deployed storefront. The admin cannot rotate it. Replacing it means deleting the storefront and creating a new one.

### Setting many at once

`batchSetNitrogenEnvironmentVariables(storefrontId, environment, variables)` on the Admin GraphQL API (`/api/gql`), with `environment` `ALL` or `PRODUCTION` and each variable as `{key, value, isSecret}`:

- All or none: a refused variable leaves every one as it was. A new key is created, an existing one's value replaced. The next deploy binds them.
- 1 to 50 variables a call, no key twice (after upper-casing), key at most 255 characters, value 1 byte to 5 KB.
- System names are refused, and so is going past 50 custom variables on the storefront.
- The keys set are logged, never the values. A secret's value comes back masked.
- It needs the **Nitrogen Storefronts** permission: staff permissions apply on Admin GraphQL, and a personal access token acts as the store owner. See [[settings-pat-tokens]].

The 5 KB limit is this mutation's. The admin page asks only that a value is not empty.

`cloudcart nitrogen env push` runs this mutation from a project's `.env`: it lists what changes, asks first (`--force` skips the question) and deletes nothing. `--env-file` picks another file. `cloudcart nitrogen env list` shows the variables with secrets masked.

## Related

- [[headless-storefront]] — hub.
- [[headless-nova-platform]] — the one environment served, and routing a domain.
- [[headless-deployment-methods]] — what a deploy binds, and what GitHub holds.
- [[headless-storefront-api]] — the tokens behind `PUBLIC_STOREFRONT_API_TOKEN` and `PRIVATE_STOREFRONT_API_TOKEN`.
- [[headless-customer-accounts]] — the two older customer-account variables.
- [[headless-nitrogen-overview]] — the platform's three caps.
- [[nitrogen-storefront-overview]] — the Environments and variables tab.

## Open Questions

_None._
