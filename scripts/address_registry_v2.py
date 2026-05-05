VALID_ENVIRONMENTS = {"example", "production"}
VALID_AUTHORITY_ZONES = {"public", "internal-general", "restricted", "experimental"}
VALID_LAYERS = {"governance", "ontology", "schema", "data", "retrieval"}
VALID_OBJECT_TYPES = {"artifact", "claim", "node", "source", "chunk", "decision", "learning_event"}


def validate_segment(value, allowed_set, name):
    if value not in allowed_set:
        raise ValueError(f"Invalid {name}: {value}")


def validate_address_struct(addr):
    validate_segment(addr["environment"], VALID_ENVIRONMENTS, "environment")
    validate_segment(addr["authority_zone"], VALID_AUTHORITY_ZONES, "authority_zone")
    validate_segment(addr["layer"], VALID_LAYERS, "layer")
    validate_segment(addr["object_type"], VALID_OBJECT_TYPES, "object_type")

    # basic presence validation for remaining fields
    for field in ["domain", "module", "version"]:
        if field not in addr or not addr[field]:
            raise ValueError(f"Missing or invalid {field}")

    return True
