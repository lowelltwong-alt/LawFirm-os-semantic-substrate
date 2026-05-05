# Change Taxonomy

## Change types

- add
- split
- merge
- reorder
- reweight
- reinterpret
- remap
- deprecate
- promote
- retire

## Decision rules

### Non-breaking
- additive optional term or property
- extra synonym or mapping
- metadata improvements without semantic shift

### Soft-breaking
- hierarchy rearrangement that changes navigation or retrieval behavior
- preference changes that alter ranking or default labels

### Breaking
- semantic change to an existing identifier
- removal without replacement path
- tightened constraints that invalidate previously valid canonical data

## Required artifacts for high-impact changes

- change proposal
- reviewer list
- migration notes
- example diffs
- validation updates
- release note entry
