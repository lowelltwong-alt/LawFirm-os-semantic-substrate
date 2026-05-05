# Answer Payload Format

This document defines the standard structure for answers produced by the pilot.

## Purpose

Ensure that every answer is:
- explainable
- governed
- traceable
- consistent

## Standard Output Shape

### Answer
A short, plain-language result.

Example: **Conditionally permitted**

### Status
Use one of:
- allowed
- restricted
- prohibited
- requires review

### Scope
Defines the boundary of the answer.

Example: **Permitted for internal intake summarization only.**

### Governing Basis
What determines the answer.

Possible sources of authority:
- firm baseline
- client restriction
- matter condition
- exception rule

### Supporting Sources
References to the semantic artifacts that support the answer.

Examples:
- semantic manifest
- retrieval feedback
- promotion records
- provenance-linked sources

### Restrictions
Explicit constraints that narrow the answer.

### Exceptions
Conditions under which the answer could change.

### Confidence
Use one of:
- high
- medium
- low

Confidence should be based on governance clarity and supporting evidence.

### Next Action
What the user should do next.

Examples:
- proceed using approved workflow
- escalate for exception review
- gather additional information

## Why This Matters

This format ensures that answers are not just outputs. They are governed, explainable decisions that can be reviewed, audited, and improved over time.
