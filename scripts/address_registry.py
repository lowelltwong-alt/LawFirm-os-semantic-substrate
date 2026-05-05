# Address Registry
# Author: Lowell T. Wong

import re

# This starter registry keeps the canonical 8-part address vocabulary close to
# the enforcement code until a dedicated registry loader is introduced.

VALID_ENVIRONMENTS = {"example", "production"}
VALID_AUTHORITY_ZONES = {
    "public",
    "internal_general",
    "restricted",
    "experimental",
}
VALID_LAYERS = {"governance", "ontology", "schema", "data", "retrieval"}
VALID_OBJECT_TYPES = {
    "artifact",
    "claim",
    "node",
    "source",
    "source_ingestion_manifest",
    "chunk",
    "decision_record",
    "learning_event",
}
VALID_PREFIXES = {
    "CLM": "claim",
    "ART": "artifact",
    "NODE": "node",
    "SRC": "source",
    "SIM": "source_ingestion_manifest",
    "CHK": "chunk",
    "DEC": "decision_record",
    "LRN": "learning_event",
}

LOWER_SNAKE_CASE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
OBJECT_ID = re.compile(r"^(?P<prefix>[A-Z][A-Z0-9_]*)-[a-z0-9_]+(?:-[a-z0-9_]+)*$")
VERSION = re.compile(r"^v[0-9]+$")


def validate_segment(value, allowed_set, name):
    if value not in allowed_set:
        raise ValueError(f"Invalid {name}: {value}")


def validate_address_struct(addr):
    validate_segment(addr["environment"], VALID_ENVIRONMENTS, "environment")
    validate_segment(addr["authority_zone"], VALID_AUTHORITY_ZONES, "authority_zone")
    validate_segment(addr["layer"], VALID_LAYERS, "layer")
    validate_segment(addr["object_type"], VALID_OBJECT_TYPES, "object_type")

    for key in ["domain", "module", "object_type"]:
        if not LOWER_SNAKE_CASE.fullmatch(addr[key]):
            raise ValueError(f"Invalid {key}: {addr[key]}")

    object_id = addr["object_id"]
    match = OBJECT_ID.fullmatch(object_id)
    if not match:
        raise ValueError(f"Invalid object_id: {object_id}")

    prefix = match.group("prefix")
    if prefix not in VALID_PREFIXES:
        raise ValueError(f"Invalid object_id prefix: {prefix}")

    if VALID_PREFIXES[prefix] != addr["object_type"]:
        raise ValueError(
            f"object_id prefix {prefix} does not match object_type {addr['object_type']}"
        )

    if not VERSION.fullmatch(addr["version"]):
        raise ValueError(f"Invalid version: {addr['version']}")

    return True
