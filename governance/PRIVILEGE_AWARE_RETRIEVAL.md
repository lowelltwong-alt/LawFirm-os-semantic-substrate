# Privilege-Aware Retrieval

## Core Rule

Authorization is a first-class retrieval invariant.

Every retrieval request must be evaluated against authenticated subject context,
target scope, source restrictions, and governing policy posture before results
are rendered to a user or downstream answer surface.

## Enforcement Pattern

- deny by default
- evaluate subject, object, action, and environment attributes
- filter before retrieval where possible
- enforce filters during retrieval when supported
- verify again after reranking and before response rendering

## Minimum Scope Checks

Privilege-aware retrieval must enforce:

- matter scope
- client restriction
- confidentiality class
- privilege class
- team or role eligibility
- purpose of use
- review posture for restricted or provisional artifacts

## Adapter Responsibilities

- Entra provides authenticated identity, group, and role claims.
- Purview DLP provides classification and restriction signals.
- Litify and iManage provide matter and document scope context.
- SharePoint and BillBlast source tags must remain subordinate to Law Firm access decisions.

No vendor adapter may override a deny decision issued under Law Firm policy posture.

Only the Law Firm `access-decision` contract is active for allow or deny control.
Vendor adapters may contribute scope and classification inputs, but they remain
draft or blocked until repo evidence or live payloads justify promotion.

## Retrieval Boundary

- Access decisions apply before retrieval and before answer rendering.
- Generated outputs inherit evidence and access boundaries.
- No unrestricted cross-matter memory is allowed.
- Quarantine material is excluded from default eligibility.

## Auditing Requirement

Every allow or deny decision used in retrieval must remain traceable through:

- `access-decision`
- `retrieval-trace`
- `retrieval-response`
- telemetry and logs defined by `standards/open-telemetry-fields.md`
