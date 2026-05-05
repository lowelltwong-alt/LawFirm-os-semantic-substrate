# Security Model

## Default Posture

- zero trust
- deny by default
- least privilege
- auditable policy decisions
- provenance and logs for sensitive operations

## Authorization Model

Use attribute-based access control over:

- subject
- object
- action
- environment

## Required Security Inputs

Security decisions may draw from:

- Entra identity and group claims
- Purview DLP classifications
- Litify matter and client scope
- iManage workspace and document scope
- SharePoint library and site restrictions
- Law Firm review posture and lifecycle state

Vendor signals may inform decisions, but Law Firm remains the authority for whether
retrieval and answer output are allowed.

## Retrieval And Generation

- access controls apply at retrieval time
- generated outputs inherit evidence and access boundaries
- no unrestricted cross-matter memory
- quarantine and client-restricted artifacts are excluded from default retrieval
- privilege-aware filtering must be enforced before response rendering
- the active Law Firm access control contract is `access-decision`; vendor identity or DLP outputs only inform that decision

## Canonical Boundary

Security tools, identity providers, and source systems do not define canonical
semantics locally. They map into Law Firm access and scope controls.

## Observability Requirement

Security-relevant retrieval activity should emit traceable, derived telemetry
using `standards/open-telemetry-fields.md`.
