---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → Configuration wizard"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Email setup wizard", "Email configuration modal", "Email channel 4-step setup", "Profile step", "Domain step", "Sender email step", "Edit Profile", "Edit Domain", "Edit Email"]
tags: [marketing, channels, email, setup, wizard, elastic-email]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-channels-email]]. See the hub for the other aspects (DNS records, Elastic Email sub-account, webhook feedback, send pipeline, suspend thresholds, settings pane).

# Email channel — Setup wizard

## Purpose

The **Configuration** modal (`MarketingChannelsEmailConfigurationModal`) is the merchant's onboarding flow for the Email channel. It is a **4-step wizard** plus a fifth "completed" review pane. The active step is computed by the backend's `current_step` field — the merchant cannot skip steps, only complete them sequentially.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → click the **Email** channel card → **Configuration** (cog icon) in the Actions band. Title — *"Email configuration"*.

The modal's size auto-grows depending on step (`lg` for profile/domain/email, `xll` for verify, `xl` for completed). Footer button label is dynamic: *"Save"* on profile/domain/email steps, *"Verify"* on the verify step, hidden on the completed step. The cancel button reads *"Cancel"* on all live steps and *"Close"* on completed.

## What the merchant can do here

### Step 1 — Profile (`MarketingChannelsEmailConfigurationStep1`)

Card title *"Profile information"*; help text *"Please fill out the information below. We need this information to set up your marketing email account."* All fields required except Company.

- **Name** (firstName, prefilled from `user.first_name` server setting)
- **Last name** (lastName, prefilled from `user.last_name`)
- **Country** (`CcCountries` dropdown — searchable, country-flag icons)
- **State** (free text)
- **City** (free text)
- **Zip code** (free text)
- **Address** (free text)
- **Phone** (`CcPhoneInput` — country-code aware, prefilled from `user.phone_number`)
- **Company** (free text, NOT required)

Endpoint: `POST /email/configuration/profile` (base `/admin/api/core/marketing/campaigns/channels`).

Per-field validation surfaces via `errorStore.getError('{field}')` from the backend's 422 response. The form is reset to empty values on unmount so re-opening starts clean unless data was saved. Profile defaults auto-populate from the store's existing settings: owner first/last name, country (mapped to Elastic Email's country ID), site city, postal code, site street, site phone (normalised to E.164 via libphonenumber), and `company_name` setting.

### Step 2 — Domain (`MarketingChannelsEmailConfigurationStep2`)

Card title *"Domain selection"*; help text *"You can select one of all the domains that have been added in the Settings > Domains section."* One field:

- **Domain** (`CcSelect` — sourced from `/admin/api/core/settings/domains`, transformed so each option's `id` and `name` are the `host` value). Prefilled with the current site host (`server settings host`, stripped of protocol). Cannot be cleared. The dropdown lists every host attached to the store — see [[settings-domains]].

Endpoint: `POST /email/configuration/domain`. Selecting the domain registers it with Elastic Email and (on Cloudflare-managed zones) auto-creates the tracking CNAME — see [[email-channel-dns-records]].

### Step 3 — Verify (`MarketingChannelsEmailConfigurationStep3`)

Title — *"Verification for domain '{domain}'"* with help text *"You will need to add the following DNS records to your domain to send emails"*. The body shows **four DNS-record cards** fetched from `apiMarketingChannels.emailVerification.useQuery` — one card per record type (SPF / DKIM / Tracking / DMARC). Each card has a copy-to-clipboard icon next to the value (toast *"Copied to clipboard"*) and an inactive "Status" badge until verification succeeds. Below the four cards is a **Change Domain** button that returns to Step 2 without losing the entered profile.

Endpoint: `GET /email/configuration/verify-domain` (+ `/verify-domain/info`). The full record table and per-method verification calls live on [[email-channel-dns-records]].

Clicking the modal's footer **Verify** button on success: toast *"Verified successfully"* + the wizard auto-advances to Step 4. On failure: toast *"Domain verification failed. Please check the DNS settings and try again."* and the modal stays open on Verify.

### Step 4 — Send email (`MarketingChannelsEmailConfigurationStep4`)

Card title *"Send email"*; help text *"This is the email address from which marketing emails will be sent to your customers."* One field:

- **Email address** — the merchant types only the **mailbox local part** (e.g., `marketing`), and the input shows the verified domain as a non-editable **unit suffix** to the right (e.g., `@example.com`). The full send address is built server-side as `{prefix}@{domain}`.

Endpoint: `POST /email/configuration/email`. Validation on the prefix only — RFC-email-valid against a synthetic `{prefix}@gmail.com` via the custom `email_prefix` rule. The save then:

1. Builds `send_email = '{prefix}@{domain}'`.
2. Calls `Domain.SetDefault(send_email)` on Elastic Email — marks this mailbox as the account's default sender.
3. **Flips `configured = true` AND `active = true` simultaneously.** The Email channel is the only channel where Step 4 of setup also turns the channel ON automatically.

### Completed step (`MarketingChannelsEmailConfigurationPreview`)

After Step 4 succeeds the modal flips to a review pane (size grows to `xl`, footer Save button hidden, Cancel becomes *"Close"*). Card title *"Verified domain '{domain}'"*. Body shows three sub-cards, each with an inline **pencil-edit** icon that resets the relevant step to incomplete:

- **Sender email** card — shows the configured `send_email`; pencil → reopens Step 4.
- **Profile** card — shows all 8 profile fields read-only (First name, Last name, Country, State, City, Zip code, Address, Company); pencil → reopens Step 1.
- **Domain** card — shows `{domain} ({send_email})`; pencil → reopens Step 2.

## Settings & fields

### Step-keyed endpoints (`current_step` advances on save)

| Step | Step key | Endpoint | Footer button |
|---|---|---|---|
| Profile | `profile` | `POST /email/configuration/profile` | Save |
| Domain | `domain` | `POST /email/configuration/domain` | Save |
| Verify | `verify` | `GET /email/configuration/verify-domain` | Verify |
| Sender email | `email` | `POST /email/configuration/email` | Save |
| Completed | (review) | — | (hidden) |

The configuration state is loaded via `GET /email/configuration`.

### Validation rules

| Field | Validation | Source |
|---|---|---|
| First name / Last name / Country / State / City / Zip / Address | `required` | Step 1 form |
| Phone | the application framework `phone_number` rule (libphonenumber, country-aware) | Step 1 form |
| Company | Not required | Step 1 form |
| Mailbox prefix | Custom `email_prefix` rule: `{prefix}@gmail.com` against PHP's `FILTER_VALIDATE_EMAIL` | Step 4 form |

## Business rules

### Profile save is transactional with Elastic Email

The profile-form data flows into Elastic Email's `Account.UpdateProfile` call inside a single DB transaction together with the channel-settings update. If Elastic Email rejects any field (e.g., invalid country code, malformed phone), the **entire setting save rolls back**. The merchant sees the upstream error message inline on the offending field.

### Changing the domain wipes verification state

Re-editing the domain via **Edit Domain** wipes `verify`, `email`, `send_email`, and `configured` settings — the merchant must re-verify the new domain. The old domain stays registered on the Elastic Email sub-account but is no longer the sender. See [[email-channel-dns-records]] for what the verify flow re-runs and [[email-channel-elastic-email-account]] for how the sub-account behaves across this change.

### Step 4 completion also activates the channel

The only channel in the platform where wizard completion auto-flips `active = true`. Other channels require a separate explicit activation. For merchants, this means: finish Step 4 and campaigns can target Email immediately, no second click required.

### Domain dropdown is bounded by [[settings-domains]]

The merchant cannot type a free-form domain. The dropdown lists exactly the hosts attached to the store. To add a new sender domain the merchant first adds the host in [[settings-domains]], then returns to **Edit Domain** to pick it.

## Related

- [[marketing-channels-email]] — hub.
- [[email-channel-dns-records]] — what Step 3 verifies + the four DNS records.
- [[email-channel-elastic-email-account]] — Step 2 provisions the sub-account; Reset configuration wipes the settings written by this wizard.
- [[email-channel-settings-pane]] — the **Settings - Email** modal (separate from this wizard).
- [[settings-domains]] — sender domains are picked from this list in Step 2.
- [[marketing-channels]] — multi-channel framework.

## Open questions

None.
