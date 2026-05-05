# Repo Operating Model

## Purpose

Define how this repository should be maintained so that growth stays coherent, validated, and aligned to one design authority.

## Core Rule

The repository should evolve through this sequence:
- reconcile
- validate
- expand
- automate

## Design Authority

The canonical spine is the design authority.
All expansion should align to it rather than create a second operating model.

## Working Rules

- prefer additive changes over silent replacement
- keep canonical and derived layers distinct
- preserve validator alignment with the declared spine
- treat roadmaps as dependency-aware, not aspirational only
- document why new standards, layers, or artifacts are being introduced

The canonical boundary between first-order ontology truth and second-order
derived/probabilistic signals is defined in:
- `governance/ONTOLOGY_BOUNDARY_CONTRACT.md`

## Expansion Rules

A new layer is acceptable when it:
- preserves the canonical spine
- stays compatible with the validation path
- improves operational usefulness
- remains bounded in scope
- does not create a parallel truth system

## Validation Rules

Validation should remain layered:
- canonical validation
- structural validation
- alignment validation
- pilot validation

## Documentation Rules

Major changes should update:
- system map
- roadmap if dependencies change
- governance model if operating posture changes
- pilot docs if sponsor-facing meaning changes

## Codex / Automation Role

Automation should help with:
- reconciliation
- consistency checks
- cleanup
- cross-document alignment

Automation should not quietly redefine the canonical spine or design authority.

## Summary

This repository is intended to grow as a governed system. Coherence is a first-class requirement, not a cosmetic cleanup step.
