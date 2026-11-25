# Legal matter taxonomy reference candidate

A fictional example of an engagement record, practice vocabulary, and optional
crosswalk from a fictional firm's codes. The candidate keeps the firm code and
its version and distinguishes the represented party, payer, counsel, and
litigation role. A public service directory may help reviewers find practice
examples. The dictionary here does not describe any real firm's internal data.

The hotel example separates underlying liability defense from a coverage dispute
over the same incident. The property example shows coverage advice without
inferring litigation. The export makes proposed links to SALI LMSS v2.0.0;
existence of an identifier and its parent does not validate legal equivalence.

## Run the example

Use Python 3.12 and the repository's jsonschema dependency. Obtain the exact
LMSS.owl from the commit linked in sali-alignment.proposed.json. Keep the upstream
license with a downloaded copy. The runner checks the source checksum. Place the
file outside the checkout and set LAWFIRM_TAXONOMY_SALI_OWL to its path.

From this example directory:

    python -B -m unittest discover -s . -v
    python -B interop.py

Candidate version 0.1.0 keeps a fictional transcript mapping. Version 0.1.1 is
a rollback exercise that withdraws that mapping. It preserves source codes and
leaves other searches unchanged. The snapshot tool can verify the predecessor
and source checksum with the command below, where the archives are supplied
separately.

    python -B release.py verify release-0.1.1.candidate.zip --predecessor release-0.1.0.candidate.zip

The package is for technical and legal review. No canonical concept IDs or
runtime integrations change. Attorney-adjudicated evaluation and a comparative
search benchmark remain future work.

## Version 0.2.1

This review candidate uses the two prior snapshots as reproducibility examples.
It preserves the vocabulary and crosswalk truth of 0.1.0. The 0.1.1 snapshot
is a separate synthetic withdrawal exercise. The 0.2.1 packaging revision adds the repository's example addresses. No canonical concept changes.
