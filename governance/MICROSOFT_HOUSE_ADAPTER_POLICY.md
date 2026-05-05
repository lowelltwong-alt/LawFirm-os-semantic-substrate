# Microsoft-House Adapter Policy

Law Firm remains AI-agnostic at the canonical layer.

Microsoft may be the preferred implementation path for enterprise deployment
surfaces such as:
- Entra identity and access
- Purview classification, DLP, and audit
- Power Automate / Logic Apps workflows
- Copilot Studio governed agent surfaces
- Azure AI / Foundry hosted model and agent execution
- Fabric and Power BI operational analytics

## Boundary rule

Microsoft implementation surfaces may be `implementation_preferred`.
They are not `semantic_authority`.

The canonical semantic authority remains the Law Firm repo's registries, governance,
ontology, shapes, and registered schemas.

## Profile rule

Any Microsoft profile without verified source payload evidence must remain
explicitly blocked or draft.
Do not upgrade a blocked profile to active based on vendor marketing or analogy.

## Portability rule

Prompts, evals, tool-calling expectations, and approval logic should remain
portable so that Law Firm can swap providers without rewriting its semantic control
plane.
