.PHONY: install test audit shacl drift release-snapshot non-authoritative-docs
install:
	python -m pip install "setuptools>=68" wheel
	python -m pip install -r requirements-dev.txt
	python -m pip install -e . --no-build-isolation
test:
	python -m unittest discover -s scripts/validation/tests -p 'test_*.py'
audit:
	bash scripts/run_full_audit.sh
shacl:
	python scripts/validation/run_shacl.py
drift:
	python scripts/check_repo_drift.py
release-snapshot:
	python scripts/build_release_snapshots.py --version 0.1.0-poc
non-authoritative-docs:
	python scripts/validation/validate_non_authoritative_docs.py
