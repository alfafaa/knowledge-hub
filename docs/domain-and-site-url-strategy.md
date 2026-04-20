# Domain And Site URL Strategy

## Purpose

This document defines how the current knowledge hub should be exposed through real site URLs.

It answers:

- whether the hub can be shown through separate domains or subdomains
- how those URLs should map to current publish targets
- what the recommended production naming should be
- how staging and production should differ

## Short Answer

Yes.

The current system is already designed to expose the central hub through separate site URLs.

That is the correct model.

The filesystem content root remains:

- `hub/`

But users should access the system through audience-specific site URLs, not through the filesystem path itself.

## Recommended Production URLs

Based on your chosen naming, the recommended production mapping is:

| Publish target | Recommended URL | Purpose |
|---|---|---|
| `public-site` | `dox.alfafaa.com` | end-user and public docs |
| `engineering-site` | `engineering.alfafaa.com` | engineering docs, ADRs, RFCs, runbooks |
| `admin-site` | `admin-dox.alfafaa.com` | finance, leadership, restricted admin docs |
| `internal-site` | optional: `internal.alfafaa.com` | broader internal company docs if you want a separate internal portal |

## Recommended Naming Notes

Your proposed names are workable, but there is one naming decision to make clearly.

### `dox.alfafaa.com`

This is acceptable if you want a short branded docs URL.

Tradeoff:

- short and distinctive
- slightly less standard than `docs.alfafaa.com`

If the team likes `dox`, it is fine to keep it.

### `engineering.alfafaa.com`

This is a strong choice.

It is clear, specific, and easy to map to `engineering-site`.

### `admin-dox.alfafaa.com`

This is workable and clearer than overloading `admin.alfafaa.com` if you want to reserve that for application administration later.

It clearly signals:

- docs for admins and restricted internal roles
- not a product admin panel

### `internal-site`

You did not name this one explicitly.

There are two valid options:

1. keep it separate
   - `internal.alfafaa.com`
2. merge its role into `engineering.alfafaa.com` and `admin-dox.alfafaa.com`

Recommended default:

- keep `internal.alfafaa.com` available if non-engineering employees need a broader internal docs portal

## Recommended Final Mapping

If you want the cleanest long-term model, use:

- `dox.alfafaa.com` -> `public-site`
- `internal.alfafaa.com` -> `internal-site`
- `engineering.alfafaa.com` -> `engineering-site`
- `admin-dox.alfafaa.com` -> `admin-site`

That is the best balance of:

- clarity
- separation
- future RBAC
- low naming ambiguity

## Why Separate URLs Are Better Than One Giant Hub URL

A single portal URL can work, but separate audience URLs are better for this system because:

- access control is clearer
- deployment boundaries are cleaner
- public and restricted content do not mix
- TLS, auth, and proxy rules stay simpler
- future SSO group enforcement becomes easier

Analogy:

- one giant hub URL is one big building with many locked rooms
- separate audience URLs are separate buildings with the right front door for each audience

For this system, separate buildings are safer.

## How This Maps To The Current Implementation

The current implementation already separates:

- `public-site`
- `internal-site`
- `engineering-site`
- `admin-site`

That means the domain strategy does not require an architectural redesign.

It is mainly a delivery-layer mapping:

- build target
- deploy location
- nginx/Caddy host rule
- TLS
- auth policy

## Staging vs Production

Current staging uses raw IP and ports:

- `http://89.167.69.232:8088/`
- `http://89.167.69.232:8089/`

That is acceptable only for staging.

Production should move to hostnames with HTTPS.

Recommended production state:

- `https://dox.alfafaa.com`
- `https://internal.alfafaa.com`
- `https://engineering.alfafaa.com`
- `https://admin-dox.alfafaa.com`

## Access Strategy Per URL

Recommended access model:

- `dox.alfafaa.com`
  - public access
- `internal.alfafaa.com`
  - employee SSO required
- `engineering.alfafaa.com`
  - employee SSO required
  - engineering-related group restriction preferred
- `admin-dox.alfafaa.com`
  - employee SSO required
  - restricted group enforcement required

This matches the current RBAC design.

## Deployment Recommendation

Use one site root per publish target and one hostname per audience URL.

That means:

- one build output per publish target
- one deploy location per target
- one reverse-proxy server block per hostname

This is already compatible with the current packaging and staging runtime layout.

## Best Practice Recommendation

Use this final production naming:

- `dox.alfafaa.com`
- `internal.alfafaa.com`
- `engineering.alfafaa.com`
- `admin-dox.alfafaa.com`

If you do not want a separate internal employee docs portal yet, you can defer `internal.alfafaa.com` until later.

That would still leave a clean three-site rollout:

- `dox.alfafaa.com`
- `engineering.alfafaa.com`
- `admin-dox.alfafaa.com`

## Recommended Next Step

The next practical implementation step for this domain strategy is:

1. define the final hostname mapping in deployment config
2. generate host-based nginx or Caddy config
3. attach TLS
4. add SSO and group-based access for non-public sites
