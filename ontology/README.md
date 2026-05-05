# Ontology Package

This directory is the canonical ontology package surface for the FMG fractal capability ontology.

## Purpose

The goal is to make ontology assets first-class at the repository root rather than leaving ontology meaning only in governance prose and examples.

## Structure

- `core/` — stable domain-neutral semantic primitives
- `extensions/fmg/` — FMG-specific semantic extensions
- `runtime-learning/` — governed runtime learning objects that should remain distinct from stable canonical meaning

## Design rule

Stable ontology meaning, FMG extension semantics, and governed runtime learning objects should be visible as separate layers even when they are tightly linked.
