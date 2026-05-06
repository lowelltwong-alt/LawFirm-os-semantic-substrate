# Harness Intensity Policy

Hardness controls harness depth. Risk color controls authority.

| Harness | Meaning |
|---|---|
| H0 | deterministic check only |
| H1 | single builder plus tests |
| H2 | planner plus builder plus tests |
| H3 | planner plus builder plus evaluator |
| H4 | planner plus builder plus evaluator plus adversarial critic plus specialist guards |
| H5 | full committee plus frontier judge plus rollback and human decision packet |

Hardness is useful only when routed through a harness. It does not permit:

- direct canonical mutation;
- route ID or event class creation;
- external writes;
- production release;
- yellow-to-green approval;
- legal, billing, or client-visible finality.

Leverage controls priority. High leverage may justify a deeper harness, but it cannot reduce required human authority for yellow or red work.
