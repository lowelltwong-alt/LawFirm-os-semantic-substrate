"""
Canonical 8-part address system.

This is the authoritative implementation of:

/environment/authority_zone/layer/domain/module/object_type/object_id/version

All parsing, validation, and construction must use this model.
"""

import re


LOWER_SNAKE_CASE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
OBJECT_ID = re.compile(r"^[A-Z][A-Z0-9_]*-[a-z0-9_]+(?:-[a-z0-9_]+)*$")
VERSION = re.compile(r"^v[0-9]+$")

VALID_ENVIRONMENTS = {"example", "production"}
VALID_AUTHORITY_ZONES = {"public", "internal_general", "restricted", "experimental"}
VALID_LAYERS = {"governance", "ontology", "schema", "data", "retrieval"}


def parse_address(address):
    parts = address.strip("/").split("/")
    if len(parts) != 8:
        raise ValueError("Address must have 8 segments")

    return {
        "environment": parts[0],
        "authority_zone": parts[1],
        "layer": parts[2],
        "domain": parts[3],
        "module": parts[4],
        "object_type": parts[5],
        "object_id": parts[6],
        "version": parts[7],
    }


def _validate_segment(name, value, allowed=None, pattern=None):
    if not value:
        raise ValueError(f"Missing {name}")
    if allowed and value not in allowed:
        raise ValueError(f"Invalid {name}: {value}")
    if pattern and not pattern.fullmatch(value):
        raise ValueError(f"Invalid {name}: {value}")


def build_address(
    environment,
    authority_zone,
    layer,
    domain,
    module,
    object_type,
    object_id,
    version,
):
    address = (
        f"/{environment}/{authority_zone}/{layer}/{domain}/"
        f"{module}/{object_type}/{object_id}/{version}"
    )
    if not validate_address(address):
        raise ValueError("Invalid canonical address")
    return address


def validate_address(address):
    try:
        parsed = parse_address(address)
        _validate_segment("environment", parsed["environment"], VALID_ENVIRONMENTS)
        _validate_segment(
            "authority_zone", parsed["authority_zone"], VALID_AUTHORITY_ZONES
        )
        _validate_segment("layer", parsed["layer"], VALID_LAYERS)
        _validate_segment("domain", parsed["domain"], pattern=LOWER_SNAKE_CASE)
        _validate_segment("module", parsed["module"], pattern=LOWER_SNAKE_CASE)
        _validate_segment(
            "object_type", parsed["object_type"], pattern=LOWER_SNAKE_CASE
        )
        _validate_segment("object_id", parsed["object_id"], pattern=OBJECT_ID)
        _validate_segment("version", parsed["version"], pattern=VERSION)
        return True
    except Exception:
        return False
