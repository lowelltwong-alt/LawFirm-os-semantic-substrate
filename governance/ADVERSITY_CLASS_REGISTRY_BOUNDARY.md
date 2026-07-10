# Candidate Adversity Class Registry Boundary

## Status

`candidate_synthetic_only`. This is a review surface, not active legal or
compliance policy.

## Source Basis

The candidate translates the synthetic PR-LL4 graph from LawFirm OS Intake PR
#74 into a Substrate-owned review contract. Brewer-Nash is a structural research
anchor named in the Fable handoff. It does not decide professional-responsibility
rules, conflicts doctrine, or firm policy.

## Authority

Semantic Substrate owns the candidate schema, registry shape, and future
promotion decision. Intake may propose a graph and Orchestrator may later consume
an approved contract read-only. Neither child repo may redefine classes, infer
edges, override holds, or convert local convenience into authority.

This candidate does not:

- define canonical adversity or conflict-of-interest classes;
- decide affiliate, former-client, prospective-client, positional-conflict, or
  firm-wide legal-imputation policy;
- clear conflicts, approve waivers or consent, open matters, fire lessons, or
  authorize representation;
- authorize real client, matter, carrier, private, privileged, or work-product
  data;
- authorize runtime execution, Exception Lake writes, connector writes,
  external actions, or automatic promotion.

## Context Contract

Applies when a synthetic-only consumer needs the exact digest-pinned PR-LL4
placeholder graph for deterministic contract tests.

Does not apply when any data is real or protected, or when a caller needs a
legal conclusion, clearance, waiver, engagement, representation, or
lesson-firing decision.

Danger if misapplied: placeholder classes could be mistaken for firm policy,
causing false clearance, improper blocking, or cross-matter disclosure.

## Candidate Invariants

- Only the exact digest-pinned synthetic fixture graph is accepted.
- Relationships come only from exact declared edges. Similarity and model
  inference are forbidden.
- Unknown and unreviewed relationships hold.
- Synthetic firm-wide evaluation is required for the fixture, but authoritative
  firm-wide provenance and legal imputation remain unverified.
- All legal, compliance, runtime, write, and promotion authority remains false.
- Runtime consumers are read-only and may not mutate or locally override this
  contract.

## Human Gates

- HD-4: counsel must decide authoritative adversity/CoI classes, affiliate scope,
  and firm-wide legal imputation.
- HD-7: privacy, counsel, data-owner, and Substrate governance approvals must
  exist before any real-data pilot.
- A later human promotion decision must compare the candidate against approved
  conflicts doctrine before changing any draft status or authority field.

## Risk Review

Risk tier: high. The schema and registry can affect Intake, Orchestrator,
Exception Lake evidence, and future agents.

Chosen option: a closed synthetic candidate pinned to the Intake graph digest.

Rejected option: define real adversity classes before HD-4. That would invent
legal authority.

Rejected option: let each child repo maintain local conflict classes. That would
permit policy drift and local overrides.

Bounded comparison: exact reviewed edge, exact unreviewed edge, and absent-edge
hold behavior only. No real-data or legal-outcome comparison is allowed.

Premortem: the registry could be read as canonical because it lives under
`registry/`; a child could change class IDs or graph edges; a digest could be
updated alongside an unsafe graph; a synthetic label could hide real data; or CI
could validate shape while missing discovery coverage. Literal candidate status,
constant authority flags, a fixed compatibility digest, semantic validation,
front-door/manifests, dependency-map coverage, and negative tests contain those
failures.

Fresh-eyes review found and closed three gaps:

- the five-case compatibility manifest is now present and independently rebuilt
  against the pinned graph digest, rather than trusting a declared digest;
- the local Exceptions Lake folder alias must satisfy its declared
  `skill-agent-manifest.json` identity contract, while the canonical folder still
  wins when both exist;
- every real/private/client/matter/carrier/privileged/work-product flag has an
  explicit negative test.

Rollback is removal of this unmerged branch and draft PR. Kill the candidate if
it admits non-synthetic data, arbitrary classes, inferred edges, local overrides,
legal authority, runtime mutation, or external writes.

## Routing Impact

- Intake PR #74 remains the source candidate and continues to fail closed.
- Orchestrator may add only a separate read-only synthetic enforcement adapter.
- Exception Lake admission remains outside this registry.
- `registry/adversity-class-registry.candidate.json` and
  `schemas/adversity-class-registry.schema.json` are the machine surfaces.
- `scripts/validate_adversity_class_registry.py` is the deterministic gate.

## Follow-Up

HD-4 and HD-7 remain open. PR-LL8 may later review broader candidate promotion,
but no status or authority field changes without explicit owner and counsel
decisions.

## Validation Evidence

- Candidate validator: passed.
- AI front-door validator: passed.
- Governance dependency-map validator: passed.
- Registry reference and repository drift checks: passed.
- Focused candidate/front-door tests: 17 passed.
- Full repo regression excluding four unchanged workspace blockers: 184 passed,
  4 deselected, 1 dependency deprecation warning.
- Full audit: every stage passed, including the truthful SHACL seed-only result;
  no conformance claim was made.
- The same four full-suite failures reproduce on untouched `main`: stale child
  contract locks, an unregistered Talent repo, missing Intake/Talent CI
  manifests, and pre-existing test-registration gaps. They were not bypassed or
  changed in this PR.
- DAD preflight: `dad:session:adedc2ec-2d9a-4199-9ff2-71e02ffcada1`.
- DAD postflight: `dad:handoff:02aa07f8-b29b-5d0f-8c24-42705cafa290`.
- DAD lesson: `dad:lesson:4b3a34fb-fbd0-5343-9f5b-b66461228289`.
