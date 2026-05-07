# Green Restoration Policy

Green restoration is a human authority decision.

When a green lane is downgraded to yellow or red, the system may prepare a `green-restoration-packet` containing:

- lane ID;
- source reclassification records;
- affected assumptions;
- evidence refs;
- proposed scope;
- rollback or monitoring requirements;
- human decision status.

Agents may draft restoration evidence and recommend green-candidate status. They may not restore green authority.

Restoration requires human review when:

- assumptions were broken or materially changed;
- a hard red trigger was involved;
- the lane scope would expand;
- the lane would authorize new external behavior;
- the lane would touch canon, route/event authority, legal, billing, client-visible, or production release surfaces.
