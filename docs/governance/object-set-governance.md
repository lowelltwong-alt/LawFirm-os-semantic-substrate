# Object Set Governance

Object sets are governed operational objects that collect bounded groups of
objects for review, publication, slicing, or workflow control.

## Rules

- object sets should have stable identity
- object sets should declare kind and scope
- object sets should distinguish static membership from query-defined logic
- review queues and publication views should not be conflated

## Supported Kinds

- `static`
- `query_defined`
- `slice_manifest`
- `review_queue`
- `publication_view`
