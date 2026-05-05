from __future__ import annotations

import json
from pathlib import Path

from referencing import Registry, Resource


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_local_schema_registry(base: Path) -> Registry:
    address_schema = load_json(base / "schemas" / "address.schema.json")
    address_struct_schema = load_json(base / "schemas" / "address_struct.schema.json")

    resources = [
        ("address.schema.json", Resource.from_contents(address_schema)),
        ("address_struct.schema.json", Resource.from_contents(address_struct_schema)),
        (
            "https://example.org/schemas/address.schema.json",
            Resource.from_contents(address_schema),
        ),
        (
            "https://example.org/schemas/address_struct.schema.json",
            Resource.from_contents(address_struct_schema),
        ),
        (
            "https://fmg.example/schemas/address.schema.json",
            Resource.from_contents(address_schema),
        ),
        (
            "https://fmg.example/schemas/address_struct.schema.json",
            Resource.from_contents(address_struct_schema),
        ),
    ]
    return Registry().with_resources(resources)
