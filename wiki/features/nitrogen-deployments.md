---
type: feature
nav_path: "Nitrogen (Headless) → Deployments"
route_name: nitrogen.deployments
route_path: /admin/nitrogen/:storefrontId/deployments
aliases: []
tags: [nitrogen, deployments, owner-only]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Deployments

## Purpose

TODO — one paragraph: what this screen lets the merchant do.

## Where to find it

Nitrogen (Headless) → Deployments

## What the merchant can do here

TODO — bulleted list of actions a merchant can take on this screen.

## Sub-screens

Distinct routes within this feature, captured from `vuejs-sitecp/` route files.

| Label | Route name | Route path |
|-------|------------|------------|
| Deployments | `nitrogen.deployments` | `/admin/nitrogen/:storefrontId/deployments` |
| Deployments | `nitrogen.deployment.detail` | `/admin/nitrogen/:storefrontId/deployments/:deploymentId` |

## Settings & fields

TODO — table of visible fields, what each one does, defaults, validation.

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| TODO | TODO | TODO | TODO |

## Business rules

### Owner-only — moderators are blocked

The Deployments list and detail pages call `/admin/api/core/nitrogen/storefronts/{id}/deployments[/{deploymentId}]`, all wrapped in the `isOwner` middleware. **Only the store owner can list deployments, view a deployment's logs, or trigger a redeploy.** Moderators get HTTP 403 and never see the Nitrogen sidebar entry. See [[nitrogen]] for the pillar-wide owner-only rule.

TODO — non-obvious behavior, dependencies, plan-tier gates.

## Related

- [[nitrogen]]
- TODO — add more wikilinks to related feature, entity, and concept pages.

## Open questions

- ⏸️ Nitrogen Deployments page is a stub — full Purpose / Settings / Business rules pending first-pass ingest.
