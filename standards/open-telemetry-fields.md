# OpenTelemetry Fields

## Purpose

Define the minimum derived telemetry fields used for retrieval, access, parsing,
indexing, and answer orchestration observability.

These fields support tracing and auditability. They are not canonical semantic
truth and may not be used to redefine document, policy, or ontology meaning.

## Required Cross-Cut Fields

- `trace_id`: distributed trace identifier for the end-to-end request
- `span_id`: span identifier for the current operation
- `parent_span_id`: parent span identifier when present
- `correlation_id`: cross-system correlation key when multiple vendor adapters participate
- `event_time`: ISO-8601 timestamp
- `service_name`: adapter or service emitting the event
- `profile_id`: Law Firm vendor profile governing the adapter behavior
- `source_system`: upstream system name such as `azure-ai-search`, `litify`, `imanage`, or `sharepoint`

## Retrieval Fields

- `retrieval_request_id`
- `retrieval_trace_id`
- `retrieval_response_id`
- `index_build_id`
- `query_activity_id`
- `adapter_filter_expression`
- `result_count`
- `reranker_score`
- `fusion_score`

`retrieval_trace` and `retrieval_response` are complementary derived artifacts:
the trace records execution and observability lineage, while the response
records ranked governed results returned to downstream surfaces.

## Security And Access Fields

- `access_decision_id`
- `decision_outcome`
- `reason_code`
- `subject_id`
- `matter_scope_id`
- `client_scope_id`
- `confidentiality_class`
- `purpose_of_use`

## Document And Evidence Fields

- `document_id`
- `document_version_id`
- `component_id`
- `span_selector_id`
- `chunk_id`
- `citation_target_id`
- `source_artifact_id`

## Vendor Guidance

- Vendor-native trace fields may be preserved, but substrate field names should be emitted in parallel when possible.
- Telemetry should reference governed IDs rather than local labels wherever governed IDs exist.
- Telemetry may describe derived operations and policy outcomes, but it must not stand in for canonical provenance or promotion records.
