# TALENT_INTELLIGENCE_RETRIEVAL_NEIGHBORHOODS

## Purpose

This document defines the first retrieval-neighborhood guidance for the Talent Intelligence / Attorney Market Intelligence extension.

The goal is to keep recruiter and market-intelligence retrieval **governed** rather than reducing it to:

- raw keyword search
- flat vector similarity
- unconstrained graph adjacency
- loose CRM lookups

---

## Core Retrieval Rule

A talent-intelligence retrieval neighborhood should expand around a governed object in a way that is:

- claim-aware
- evidence-aware
- authority-aware
- review-aware
- structurally bounded

This means recruiter or strategy context should be assembled from the ontology's governed objects and claims, not improvised from whatever downstream fields happen to exist.

---

## Primary Retrieval Anchors

The current extension suggests three main retrieval anchors.

### 1. Attorney-centered neighborhood
Use when the focal question is about a specific attorney.

Typical expansion order:

1. canonical attorney identity  
2. current employment episode  
3. recent source profiles  
4. related talent signal claims  
5. external identifiers  
6. relationship / introducer context if authority permits  
7. supporting intake artifacts or evidence references

Typical questions:

- Who is this attorney?
- What firm are they at now?
- Why did they surface as a target?
- Is this identity stable or still provisional?

### 2. Firm-centered neighborhood
Use when the focal question is about a law firm or office.

Typical expansion order:

1. canonical law-firm identity  
2. office / practice context  
3. source profiles and public snapshots  
4. recent instability-related claims  
5. linked attorney nodes  
6. related intake artifacts and market evidence

Typical questions:

- Is this firm showing instability?
- Which practice groups look vulnerable?
- Which attorneys or offices are strategically relevant?

### 3. Intake-artifact-centered neighborhood
Use when the focal question is about a list import or incoming market dataset.

Typical expansion order:

1. intake artifact  
2. mapped source rows  
3. generated source profiles  
4. provisional entities / claims  
5. validation posture  
6. promoted governed objects where they exist

Typical questions:

- What came from Leopard List?
- Which rows have been promoted?
- Which rows remain provisional or blocked by review?

---

## Neighborhood Templates

### Template A. Recruiter quick-read neighborhood
Purpose: quick practical recruiter context.

Recommended contents:

- attorney identity summary
- current firm / office / title
- one or two most relevant source profiles
- top talent signal claims with review posture
- relationship warmth / introducer indicators if permitted
- any major validation caveats

Avoid over-expanding into every artifact or historic edge unless needed.

### Template B. Market-intelligence analytic neighborhood
Purpose: strategic review of firms, offices, or target clusters.

Recommended contents:

- firm identity
- instability claims
- recent talent movement evidence
- office / practice clustering context
- linked attorneys with high-relevance claims
- evidence and source provenance

### Template C. Identity-resolution review neighborhood
Purpose: merge / split review.

Recommended contents:

- compared attorney candidates
- name variants
- source profiles
- external identifiers
- employment episodes
- conflicting fields
- current review posture

This template should strongly favor caution in common-name scenarios.

---

## Bounded Expansion Rules

### 1. Expand recent and current context first
Prefer current employment, current source profiles, and active claims before deep historical context.

### 2. Expand reviewed signals before hypotheses where possible
If both exist, stronger-reviewed claims should surface ahead of weaker hypotheses.

### 3. Respect authority zones
Relationship and recruiter-note context may be more restricted than public-source context.

### 4. Keep evidence visible
Derived signals should remain connected to evidence or source profiles rather than appearing as orphan conclusions.

### 5. Keep identity uncertainty visible
If an attorney remains provisional or collision-prone, retrieval should not hide that uncertainty.

---

## Resting Place In The Layer Model

This document primarily extends:

- Layer 6. Retrieval layer

while depending on:

- Layer 1. Identity layer
- Layer 3. Claim layer
- Layer 5. Validation layer
- Layer 8. Artifact layer

This is one reason the talent-intelligence extension should end semantically in layers 1 through 8 and not in workflow tools.

---

## Status

Initial retrieval-neighborhood guidance only. Intended as the first bridge from talent-intelligence semantics into governed AI / recruiter context assembly.