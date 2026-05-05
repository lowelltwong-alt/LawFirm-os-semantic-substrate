# Changelog

All notable changes to this repository will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- `scripts/run_full_audit.sh` — single-command audit entrypoint running all 35 validators
- `.secrets.baseline` — detect-secrets baseline; existing findings confirmed non-credential
- `address` and `address_struct` properties (optional) to 12 governed schemas
- `## Open Questions` section in `governance/ALIGNMENT_SCOREBOARD.md` (OQ-001 through OQ-012)

### Fixed
- `scripts/validate_governed_learning_examples.py` — added RefResolver for local $ref resolution
- `scripts/validate_examples.py` — rewrote to use Draft202012Validator + RefResolver, scope to claim:v3 only
- `scripts/validate_repository_vnext.py` — added RefResolver for address schema refs
- `governance/ALIGNMENT_SCOREBOARD.md` — corrected runtime posture row from Out-of-Alignment to Aligned

### Changed
- `governance/ALIGNMENT_SCOREBOARD.md` — Last updated to 2026-04-16

---

<!-- Prior release history: <<PLACEHOLDER:release-history — populated by maintainer from git tags and prior release notes>> -->
