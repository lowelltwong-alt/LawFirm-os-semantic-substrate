Make the governed learning loop explicit

## Summary
- add an explicit learning-loop architecture doc
- add a governed learning and promotion model doc
- add bounded learning-loop use cases for the pilot layer
- add a learning-loop prompt supplement for outside AI systems and collaborators

## Why
The repository already had the scaffolding for governed recursive improvement, but it was still easier to read it as a semantic-governance system than as a living learning system.

This PR makes that architecture explicit without changing the core design authority.

## Design Position
The learning loop is best understood as a cross-cutting governed pattern across:
- governance
- validation
- retrieval
- evaluation
- promotion

For communication purposes, it can also be described as an optional ninth layer: a learning and adaptation layer.

## What This Preserves
- canonical spine first
- validation-aligned growth
- substrate-native operating semantics as design authority
- additive semantic stack posture
- explicit separation between feedback, inference, proposal, and promoted baseline
- no unsafe self-modification
