# Autonomy Red Yellow Green Policy

Risk color controls authority.

## Green

Green means a preapproved autonomous lane. Green work may proceed only while its registered assumptions remain true.

Typical green work includes:

- synthetic fixture generation;
- opportunity draft creation;
- opportunity scoring;
- Codex task packet drafting;
- local-only tests and validators;
- low-risk local artifacts.

Humans are required to create or restore non-preapproved green authority.

## Yellow

Yellow means bounded autonomous evidence-building. Yellow work may continue with drafts, tests, evals, review records, rollback plans, and human decision packets.

Yellow work must not:

- auto-merge protected branches;
- create production releases;
- mutate canonical schemas or governance;
- create route IDs or event classes;
- perform external writes;
- activate real-data connectors;
- finalize legal, billing, or client-visible authority.

## Red

Red means stop or human approval required. Agents may prepare evidence, but they may not execute final authority.

Hard red triggers include:

- real client data;
- real matter data;
- privileged content;
- secret or credential exposure;
- direct canonical mutation;
- new route ID or event class;
- external write, send, or publish;
- client-visible output;
- filing, signature, or disclosure;
- billing or legal finality;
- missing audit record for material action;
- human approval bypass;
- destructive operation risk.

Hard red triggers override hardness and leverage.
