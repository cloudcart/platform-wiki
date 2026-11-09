---
type: feature
nav_path: "Settings → Payment methods → + Add payment method"
route_name: admin.payments
route_path: /admin/settings/payment_providers
aliases: ["Add payment method modal", "Install payment provider", "Добави платежен метод", "Инсталирай платежен метод"]
tags: [settings, payments, providers, install, modal]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[settings-payment-providers]]. See the hub for related aspects (list, filtering, activation, uninstall, credentials shell, record fields).

# Payment methods — Add payment method modal

## Purpose

The **+ Add payment method** modal is how a merchant installs an additional payment provider. It lists every provider that is available for the store (per the filters in [[settings-payment-providers-filtering]]) but not yet installed. Each card shows the provider's icon, name, description, and any active "Recommended" / "Featured" marketing badge. Clicking a card does NOT install the provider in place — it opens the provider's own page. While the provider is not installed, that page shows only its install screen with an **Install** button; clicking **Install** installs the provider at once, switched off, and only then do its tabs (settings, credentials, schemes, onboarding) appear. Saving settings never installs a provider.

## Where to find it

Sidebar → Settings → **Payment methods** → click **+ Add payment method** in the top-right action slot. The button is described on [[settings-payment-providers-list]].

The modal also opens **automatically** on page mount if the URL contains the hash `#add-payment` — useful for deep-link CTAs elsewhere in the platform (e.g., dashboard widgets, onboarding checklists). The hash is cleared one second after the modal opens.

## What the merchant can do here

- **Browse all providers available for the store but not yet installed**, scrolling a vertical list of cards.
- **Click a provider card** to navigate to that provider's own settings page (`apps.<provider-map>.settings`), where the **Install** button is.
- **Close the modal** without installing, via the `×` icon (mobile) or the **Close** text button.
- **See "you have everything"** — when every provider available for the store is already installed, the modal renders an empty state with a graphic, the text *"You have installed all available payment methods"*, and a Close button.

What the merchant CANNOT do here:

- Install a provider directly from this modal — clicking a card is navigation only; the install happens with **Install** on the provider's page.
- See providers excluded by the store's operation country, the underlying app being soft-deleted, dev-only apps, or plan-feature gating — these are filtered out by the backend before the modal renders. See [[settings-payment-providers-filtering]] for what hides a provider from this list.
- Filter or search within the modal — the list is a single vertical scroll.

## Settings & fields

### Modal layout

| Element | What it shows |
|---------|---------------|
| **Header** | *"Add payment method — Add more payment methods for your store"* |
| **Provider list** | Vertical scroll of cards (one per available provider): icon (40px), name, settings description, plus optional **Recommended** / **Featured** badges. Each card navigates to `apps.<provider-map>.settings` on click — IF such a route exists in the Vue router. If not, the card is a no-op (defensive against routing changes). |
| **Close button** | Top-right `×` icon (mobile) and the regular `Close` text button. |
| **Empty state** | When no providers are available to install (everything is already installed): a graphic + the text *"You have installed all available payment methods"* + a Close button. |

### Per-card fields

| Field | Shows |
|-------|-------|
| **Icon** | 40 px provider logo, sourced from the underlying App row. |
| **Name** | Provider name (English / localised by the active admin-panel language). |
| **Description** | One-line marketing description from the App row (e.g., *"Accept card payments via 3-D Secure"*). |
| **Recommended badge** | Shown when an active CloudCart marketing campaign tags the underlying App with `recommended`. Driven by [[settings-payment-providers-filtering]]. |
| **Featured badge** | Shown when an active marketing campaign tags the App with `featured`. Same driver. |

## Business rules

### Clicking a card navigates, does NOT install

The card click takes the merchant to `apps.<provider-map>.settings` — the provider's own page. Every address of a provider that is not installed shows the same install screen (icon, description, **Install**) instead of the tabs; the provider's overview address and the address the card opens lead to the same result. Clicking **Install** installs the provider at once, inactive, and adds it to the [[settings-payment-providers-list]] table; the tabs then appear and the merchant enters credentials (varies by provider — see [[settings-payment-providers-credentials-shell]]) and switches it on. Saving settings is possible only once the provider is installed.

The per-provider page exists because each provider needs different credential shapes — Stripe needs Secret + Publishable keys, myPOS needs a single base64 Configuration package, Borica Way4 needs a Terminal ID + CSR exchange + certificate upload (see [[payment-providers-borica-way4]]), CloudCart Pay needs a KYC onboarding flow (see [[payment-providers-cloudcart-pay-onboarding]]). The Add modal can't capture all those shapes inline; it just routes the merchant to the right screen.

### Card is a no-op if the Vue router has no matching route

If a provider's `apps.<provider-map>.settings` route does not exist in the current Vue router (e.g., the provider's frontend module was renamed, or a partial migration is in progress), the card click does nothing. This is **defensive** — better a no-op than a crash. The merchant should see no broken cards in normal operation; if they do, the operations team has likely missed a router update during a deprecation.

### `#add-payment` hash deep-link

URLs containing the hash `#add-payment` (e.g., a "click here to add a payment method" link in a dashboard widget) auto-open this modal one second after page mount, then clear the hash. The one-second delay is to let the page finish initial mount before triggering the modal.

### Modal contents are filtered by the same rules as the list

The Add modal does not show every payment provider in CloudCart's catalogue — only those available to **this** store. Filters applied by the backend (full mechanics on [[settings-payment-providers-filtering]]):

- **Operation country** — only providers whose underlying App is available for the store's `operation_country` (from [[settings-general]]).
- **Soft-deleted apps** — providers whose underlying App was removed from the catalog by CloudCart are excluded.
- **Dev-only apps** — internal-only providers are excluded unless this store has explicitly installed them.
- **Already-installed providers** — providers shown in the installed list (see [[settings-payment-providers-list]]) are NOT in the Add modal; they're mutually exclusive.

### Closing or leaving installs nothing

Closing the modal, or opening a card and leaving the provider's page without clicking **Install**, installs nothing and leaves nothing half-installed. The provider stays in the Add modal until **Install** is clicked; after that, removing it is an uninstall ([[settings-payment-providers-uninstall]]).

## Related

- [[settings-payment-providers]] — hub.
- [[settings-payment-providers-list]] — the installed-providers table the modal complements.
- [[settings-payment-providers-filtering]] — what filters this modal's contents (country, plan, soft-deleted, dev-only, marketing badges).
- [[settings-payment-providers-credentials-shell]] — what credentials each downstream provider page asks for after the click-through.
- [[settings-payment-providers-uninstall]] — the reverse operation; uninstalled providers re-appear in this modal.
- [[apps]] — App Store; underlying Apps drive the modal's catalogue.
- [[settings-general]] — `operation_country` setting filters the modal.
- [[payment-providers-cloudcart-pay-settings]] / [[payment-providers-borica-way4]] / [[payment-providers-dsk-bnpl]] — example downstream destinations after a card click.

## Open questions

- Bulgarian labels of the modal's texts and of the **Install** button (production translation table).
