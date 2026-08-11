---
type: feature
nav_path: "Apps → Multilang → Create → Step"
route_name: apps.multilang.create
route_path: /admin/apps/multilang/create/:type
aliases: ["Multilang Create", "Create sister site", "Link existing site", "Multilang wizard"]
tags: [apps, administration, multilang, wizard, create, sister-site]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 3
---
# Multilang → Create → Step

## Purpose

The **Create / Step** wizard adds a new **sister site** to a Multilang setup. The merchant arrives from [[apps-multilang-stores]] via the "+ Add language site" button. The `:type` URL parameter picks one of two sub-flows:

- **`type=new`** → provision a brand-new CloudCart store as the sister site.
- **`type=exist`** → link one of the merchant's own existing CloudCart stores as the sister.

After the type page, the wizard advances through the `apps.multilang.step` route. For the full feature set, see [[apps-multilang]].

## Where to find it

[[apps-multilang-stores]] → "+ Add language site" → one of:
- `/admin/apps/multilang/create/new` — new sister site.
- `/admin/apps/multilang/create/exist` — link existing.

The wizard then advances via `/admin/apps/multilang/create/step/:step`.

## What the merchant can do here

The wizard has **5 steps** (step 1 is the `new`/`exist` landing; steps 2–5 are the `apps.multilang.step` progression):

| Step | What the merchant configures |
|---|---|
| 1 (type) | `new` vs `exist`. New = create a brand-new CloudCart store as sister; Exist = link one of the merchant's existing CloudCart stores. |
| 2 | Pick which entity types to **copy** to the sister (products, categories, blog, pages, etc.) and whether to translate each. |
| 3 | Per-product copy settings — fine-grained per-entity flags. |
| 4 | Pick the **plan + add-on apps** for the sister (the new site needs its own plan). |
| 5 | Order summary + payment confirmation (HTTP `402` if the merchant hasn't yet paid for the plan + features). |

After step 5 + payment, the merchant lands on [[apps-multilang-progress]], which runs the actual sync. Steps 2–5 are gated by `started == 0`; once the sync has started, navigating to any step redirects to Progress (the merchant can no longer change copy / feature toggles).

### What the merchant CANNOT do here
- Skip the language code — sister-site language is mandatory.
- Use the master's domain — the sister needs its own.
- Re-enter the wizard after sync starts (`started = 1` redirects to Progress).
- Pick a different reseller / key account for the sister (inherited from master — see Business rules).

## Settings & fields

### `type=new` — required input fields

The `createNew` flow collects **exactly four** fields; there is **no theme/template field** here (the sister inherits the master's theme automatically — see Business rules):

| Field | Notes |
|---|---|
| `domain` | **Subdomain slug only**, not a full domain. Validation: `required\|regex:/^[a-z0-9\-]+$/i\|isAvailable`. The merchant enters e.g. `mystore-en`; the platform appends `.cloudcart.net` → sister provisioned at `<slug>.cloudcart.net`. Dots, slashes, protocol prefixes are **rejected**. |
| `language` | ISO code (en / bg / ro / de / …). Mandatory. |
| `currency` | Sister-site currency (may differ from master). |
| `unit_system` | Measurement unit system for the sister. |

A custom domain (e.g. `en.merchant.com`) is mapped **after** the site is live, via the sister's [[settings-domains]] + DNS + [[apps-lets-encrypt]] — that is a post-create step, not part of this wizard.

### `type=exist` — fields

| Field | Notes |
|---|---|
| Existing site | Dropdown of the **merchant's own** non-deleted CloudCart stores (ownership comes from the user-account model — the merchant can't link someone else's store). |
| Language | The existing site's language. |
| Bi-directional sync | Whether master ↔ sister both push changes. |

### Error handling

Field-level validation errors are surfaced inline on both the new-site and link-existing forms.

## Business rules

### `type=new` vs `type=exist`
- **New** — merchants starting fresh; CloudCart provisions the store, domain, and storefront.
- **Exist** — merchants already running multiple CloudCart stores; convert them into a master/sister setup.

### Linking an existing store keeps its own data — no conversion
Linking does **not** copy prices, products, or currency from the master; it only establishes the master/sister relationship. The existing sister **keeps its own currency and prices** — there is no auto-conversion. Mirroring the master's prices with currency conversion is a manual / custom workflow.

### Sister inherits the master's theme, commercial relationships, plan, and apps
At create time the install job copies these from the master onto the new sister:
- `template_id` (theme) — the sister's starting theme; afterwards it's a regular CloudCart site and can switch to any standard theme via its own Theme Marketplace catalogue (no Multilang-specific restriction).
- `user_id` (account owner), `reseller_id`, `key_account_id`, `cc_user_id`.
- `industry` / `main_industry`.
- `next_billing_date` (set to tomorrow).
- `apps.multilang.plan` set to the master's plan; `apps.multilang.apps` set to the full list of apps installed on the master.

Plan-feature **quotas** are independent per site (the sister gets its own `multilang_product_translate` quota etc.), but the plan tier and app stack mirror the master. The merchant cannot pick a different reseller / key account for the sister.

### Sister created locked + forced into the wizard
The sister is created with the Multilang `is_locked` flag set to `1` and `step = 2`, forcing it into the multilang wizard from the master's side. The master's owner record (password/salt) is copied to the sister so the same owner can log in to both.

### DNS / SSL is not verified inline
The `domain` slug is stored as entered; DNS is **not** auto-verified at submit. The downstream install workflow attempts SSL cert issuance via [[apps-lets-encrypt]]. If DNS isn't pointing yet, the sister sits in **Pending** on [[apps-multilang-stores]] until DNS resolves and the cert provisions.

### Initial sync runs in the background
Sync runs as a background queue task. The merchant is **freed to navigate** — they can close the browser and return; each refresh of [[apps-multilang-progress]] returns the latest `remaining` count.

### Plan cap on sister sites
Adding a new site is blocked once the plan's sister-site cap is reached.

### Payment bypass for CloudCart-internal sites only
Step 5 normally initialises a checkout cart with the plan + apps + features pricing and redirects to checkout. Sites on the internal **FREE_FOR** whitelist skip this and go straight to Progress with no payment. Regular merchants are never on this list and always pay (see [[settings-cart]]).

### Uninstall leaves the sister intact
When the master uninstalls Multilang, cleanup removes each sister's Multilang app instance, but the **site itself remains** a valid CloudCart store (catalog, customers, orders, theme retained). The link is severed and master→sister sync stops; the merchant can re-link later via `type=exist`.

### Permission
Standard apps permission scope.

## Related

- [[apps-multilang]] — Multilang hub.
- [[apps-multilang-stores]] — sister-sites list (parent + landing after the wizard).
- [[apps-multilang-settings]] — feature toggles.
- [[apps-multilang-progress]] — sync progress after wizard completion.
- [[apps-lets-encrypt]] — SSL cert provisioning for the sister-site domain.
- [[settings-domains]] — custom-domain mapping (post-create).
- [[settings-cart]] — checkout for the plan + features payment at step 5.

## Open questions
