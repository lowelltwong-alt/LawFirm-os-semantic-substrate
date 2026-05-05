# Slice 03 — Azure Document to Grounded Answer

## Goal

Show how structured output from Azure Document Intelligence is normalized into the canonical document model, retrieved through governed contracts, and returned as a grounded answer with evidence references.

## Flow

1. Azure parsing output is normalized into canonical text, components, and span selectors.
2. Retrieval request is issued with access context.
3. Retrieval trace records ranking and index versions.
4. Answer event references the exact evidence spans used.

## Success condition

A reviewer can trace the grounded answer back to canonical spans and parser provenance without relying on opaque index artifacts.
