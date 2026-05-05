# ROADMAP

This roadmap captures **visible next-fit work** that should be designed into the LawFirm OS Semantic Substrate without forcing premature top-level restructuring.

The intent is to make future domain expansion explicit while preserving the current governance-first architecture.

---

## Build Order Principle

1. reconcile first  
2. validate second  
3. expand third  
4. automate fourth

This means future domain packs should enter the repository as **governed extensions** that reuse the existing identity, claim, evidence, authority, trust, retrieval, and fractal-address architecture.

---

## Near-Term Architecture Fit Work

### 1. Talent Intelligence / Attorney Market Intelligence extension

An implemented baseline/scaffold now exists for a governed attorney and law-firm talent-intelligence extension that fits **under** the current architecture rather than competing with it.

Current scaffold location:

- `schemas/extensions/talent_intelligence/`
- `examples/talent_intelligence/`

Implemented baseline intent:

- establish extension namespace + structure
- provide initial schema surfaces and example artifacts
- keep talent-intelligence modeling aligned with existing governance-first architecture

Remaining governance/validation integration gaps (future work):

- complete validation + CI integration for extension artifacts
- finalize governance constraints as enforceable policy checks
- deepen authority/trust-zone handling across extension objects
- formalize review/approval posture for inferred or scored signals

The extension pack should continue to include (and mature around):

- Attorney
- LawFirm
- Office
- PracticeArea
- EmploymentEpisode
- BarCredential
- ExternalProfile
- RelationshipEdge
- IntroducerEdge
- Recognition
- ThoughtLeadershipArtifact
- LeadershipRole
- CourtFilingActivity
- FirmInstabilitySignal
- PortableBookEvidence
- CandidateOpportunity

Design rule:
- stable Law Firm internal identity remains primary
- external IDs remain attached as source-linked identifiers
- analytics and scores do not become ontology truth
- all major signals should remain evidence-backed and provenance-aware

### 2. Attorney canonical identity resolution layer

Add a future identity-resolution pattern for attorneys where the ontology can support:

- stable opaque Law Firm attorney IDs
- source profile separation
- bar / registration identifiers as external identifiers, not canonical identity
- time-bounded employment episodes
- merge confidence and review posture
- common-name collision protection

Design rule:
- do not equate person identity with firm bio, LinkedIn profile, bar number, or recruiter-system record

### 3. Intake layer for external recruiting / market lists

Add a governed intake layer for structured list ingestion.

This should support sources such as:

- Leopard List
- recruiter spreadsheets
- vendor exports
- law firm target lists
- conference attendee lists
- internal relationship lists
- future purchased market datasets

This intake layer should normalize imported rows into governed objects rather than treating lists as ontology truth.

Recommended intake stages:

1. raw intake artifact  
2. mapped source rows  
3. provisional entities / claims  
4. validation + review  
5. promoted governed objects

Design rule:
- imported lists are artifacts and evidence inputs
- ontology truth emerges only after mapping, validation, and review

### 4. Recruiting CRM / ATS synchronization layer

Add a future synchronization pattern for systems such as Greenhouse or similar CRM / ATS tools.

This layer should support:

- Law Firm canonical IDs written back to downstream systems
- source-system IDs preserved as external identifiers
- controlled field mappings
- authority-aware note handling
- candidate / prospect status synchronization

Design rule:
- downstream systems remain systems of engagement
- the governed ontology remains the intelligence and identity spine

### 5. Derived talent signals layer

Future analytics may include:

- relationship warmth
- introducer strength
- market visibility
- probable portability evidence
- firm instability signals
- outreach readiness

Design rule:
- these remain assessments or claims with evidence, lineage, confidence, and review posture
- they should not be modeled as intrinsic person identity

---

## Governance Constraints For Future Talent-Intelligence Buildout

Any future implementation in this area should preserve the repository’s existing non-negotiables:

- claim container discipline
- authority / trust zones
- asserted / inferred / hypothesis separation
- fractal address placement
- validation + CI
- clear example / production separation

Additional constraints for talent intelligence:

- preserve provenance for all imported or inferred signals
- separate raw source text from normalized ontology objects
- require careful merge governance for common names
- keep sensitive notes, access levels, and authority zones explicit
- do not flatten vendor data into unquestioned fact

---

## Proposed Future Documentation

When expanded, this roadmap item should likely grow into:

- `governance/TALENT_INTELLIGENCE_EXTENSION.md`
- `governance/ATTORNEY_IDENTITY_RESOLUTION.md`
- `governance/INTAKE_LAYER_PATTERN.md`
- `schemas/extensions/talent_intelligence/`
- `examples/talent_intelligence/`

---

## Status

Partially implemented as a scaffolded baseline in `schemas/extensions/talent_intelligence/` and `examples/talent_intelligence/`, with explicit remaining governance/validation integration work still open.

Current state:

- implemented baseline: extension scaffolding and initial example footprint are present
- remaining gaps: governance hardening, validation enforcement, and CI-level integration are still in progress
