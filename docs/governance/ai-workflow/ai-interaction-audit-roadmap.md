# AI Interaction Audit Roadmap

This roadmap defines the path for governed AI interaction audit records while keeping raw production conversation content out of this contract repository.

## Principle

Law Firm defines audit contracts and governance. Runtime implementations capture and persist audit events. Raw conversation content belongs only in a secure, encrypted, access-controlled, retention-governed audit store outside this repository.

## Phase 0  -  Governance docs

- Define audit-capture principles.
- Define envelope versus sealed transcript boundaries.
- Define retention, privacy, privilege, and legal-hold expectations.
- Keep all work docs-only.

## Phase 1  -  Draft audit contracts

Future Law Firm contract work may define draft schemas for:

- AI interaction audit event
- AI run or session audit envelope
- AI tool-call audit event
- AI output audit event
- transcript storage pointer
- retention classification

## Phase 2  -  Synthetic runtime audit capture

Runtime repos should first capture synthetic and dry-run events only:

- route and mode
- contract SHA
- content hashes
- policy decision
- tool-call metadata
- audit event hash
- no raw production conversation content

## Phase 3  -  Secure transcript vault design

Design an external secure store for sealed transcripts:

- encryption
- access control
- privilege classification
- retention class
- legal hold flag
- redaction and minimization
- audit-event pointer

## Phase 4  -  Production audit ledger

Only after governance approval, runtime systems may capture production AI interaction audit records using approved contracts and approved storage.

## Phase 5  -  Enforcement

After contracts and runtime patterns are stable:

- PR templates require AI audit impact disclosure.
- Validators check audit contract coverage.
- Runtime systems fail closed when a route lacks an audit policy.

## Non-goals now

- no production audit lake
- no raw transcript store
- no production conversation capture
- no connector implementation
- no schema authority change unless explicitly routed later
