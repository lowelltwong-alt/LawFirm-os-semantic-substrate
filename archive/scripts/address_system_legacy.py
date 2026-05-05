"""
DEPRECATED: Legacy 4-part address system.

This file is retained temporarily for migration purposes only.

All new development must use the canonical 8-part address system.
"""


def parse_address(address):
    parts = address.strip("/").split("/")
    if len(parts) < 4:
        raise ValueError("Invalid address structure")
    return {
        "layer": parts[0],
        "domain": parts[1],
        "object_type": parts[2],
        "object_id": parts[3],
    }


def build_address(layer, domain, object_type, object_id):
    return f"/{layer}/{domain}/{object_type}/{object_id}"


def validate_address(address):
    try:
        parsed = parse_address(address)
        for key in ["layer", "domain", "object_type", "object_id"]:
            if not parsed.get(key):
                return False
        return True
    except Exception:
        return False
