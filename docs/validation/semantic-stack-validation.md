# Semantic Stack Validation Scaffold

The semantic graph stack is intentionally additive in this repository.

Current validation posture:

- existing canonical JSON example validators remain authoritative
- SHACL files in `shapes/` act as seed constraints for future semantic tooling
- scaffold scripts under `scripts/validation/` only check file presence and basic
  structural expectations for bounded pilot assets

This lets the repository prove semantic-stack intent without forcing the new
artifacts into the current canonical runtime gate.
