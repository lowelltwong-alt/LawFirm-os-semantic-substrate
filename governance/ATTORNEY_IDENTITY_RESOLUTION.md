# ATTORNEY_IDENTITY_RESOLUTION

## Purpose

This document reserves a future governance and modeling pattern for **attorney canonical identity resolution** within the LawFirm OS Semantic Substrate.

The core design requirement is that a stable Law Firm attorney identity must survive changes in:

- firm affiliation
- office
- title
- public profile URLs
- recruiter-system records
- vendor records
- available identifiers

---

## Design Position

The ontology should mint and preserve a stable internal attorney identity that is:

- opaque
- durable
- governance-controlled
- independent from any single source system or public profile

Bar numbers, registration numbers, profile URLs, CRM record IDs, and vendor IDs should be treated as **external identifiers** or source-linked evidence, not as canonical identity.

---

## Layer Fit

### Layer 1. Identity layer
Primary concern.

This document primarily governs:

- Law Firm canonical attorney ID
- identifier attachment rules
- duplicate handling posture
- merge / split review posture

### Layer 2. Node layer
Future entities may include:

- Attorney
- ExternalIdentifier
- SourceProfile
- EmploymentEpisode
- BarCredential
- Alias / NameVariant

### Layer 3. Claim layer
Identity resolution should support claims such as:

- probable_same_as
- confirmed_same_as
- not_same_as
- works_at
- admitted_in
- known_as

### Layer 5. Validation layer
Critical validation concerns include:

- common-name collision controls
- minimum evidence thresholds
- merge confidence posture
- required review for ambiguous matches

### Layer 7. Fractal address layer
Identity objects and merge decisions should be structurally addressable inside the larger architecture.

### Layer 8. Artifact layer
Identity evidence may derive from artifacts such as:

- law firm bios
- bar directory pages
- recruiter notes
- imported spreadsheets
- CRM records
- vendor exports

### Optional Layer 9. Orchestration / workflow layer
If formalized later, identity resolution can feed:

- merge queues
- review workflows
- downstream system synchronization
- promotion from provisional to governed identity state

---

## Canonical Identity Rule

There should be exactly one stable **Law Firm attorney ID per human person** once governance determines that multiple records refer to the same individual.

That ID should not encode:

- firm
- state
- office
- practice
- source system

It should remain stable even when all of those change.

---

## Source Separation Rule

The ontology should preserve separation between:

1. canonical attorney identity  
2. source profiles  
3. external identifiers  
4. employment episodes  
5. claims or assessments about identity confidence

This prevents the system from collapsing identity into one contingent source record.

---

## Proposed Future Components

### Canonical Attorney
Stable Law Firm person identity.

### Name Variant
Different observed forms of name, including middle initials, suffixes, and formatting variations.

### External Identifier
Examples:

- bar number
- registration number
- LinkedIn URL
- firm-bio URL
- CRM candidate ID
- future vendor ID

### Source Profile
A record of what a given source claimed or displayed at a point in time.

### Employment Episode
A time-bounded relationship between attorney and firm / office / role.

### Match Decision
A governed record of merge, split, defer, or exclusion posture.

---

## Merge Governance Posture

Bias should favor **avoiding false merges**.

It is generally safer to:

- keep two provisional John Smith records apart
- review later with stronger evidence

than to:

- merge two different John Smiths
- pollute notes, relationships, and downstream recruiting signals

Likely decision postures:

- auto-merge only with strong evidence
- review queue for medium confidence
- do not merge when evidence is weak or contradictory
- preserve explicit `not_same_as` history where appropriate

---

## Common-Name Protection

Common names require elevated caution.

Potential corroborating dimensions include:

- jurisdiction / admission data
- law school
- graduation year if available
- office city
- practice area
- clerkship history
- title / seniority
- prior-firm history
- direct external identifier match

Name alone is insufficient.

---

## Future Validation Rules

Potential future validation rules include:

- no canonical identity promotion without minimum evidence set
- required provenance on all external identifiers
- required timestamping of source observations
- prohibition on using vendor data as unquestioned fact
- review requirement for conflicting active employment episodes

---

## Relationship To CRM / ATS Systems

CRM or ATS systems should not become the canonical attorney-identity authority.

Those systems should instead consume and reference the governed Law Firm identity spine through:

- Law Firm attorney ID writeback
- external ID crosswalks
- controlled field mappings
- match-status visibility

---

## Status

Reserved for future governed buildout.