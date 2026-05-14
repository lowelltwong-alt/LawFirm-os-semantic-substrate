# Legal Document Ingestion Boundary

Legal document ingestion starts with a metadata-only manifest. The manifest must identify the source, access policy, privilege label, confidentiality label, retention class, parser profile, and permitted index types before the runtime touches document content.

## MVP authorization

The seed authorizes only synthetic ingestion preflight.

## Forbidden in MVP

- real client document ingestion;
- real matter file ingestion;
- broad DMS crawling;
- indexing without access labels;
- indexing without retention class;
- raw payload fanout to Exception Lake;
- automatic promotion of extracted legal meaning.

## Future production requirements

A future production path must add:

- connector approval;
- matter/user authorization;
- legal hold and retention checks;
- privilege review workflow;
- DMS claim-check references;
- deletion/supersession policy;
- audit and appeal path.
