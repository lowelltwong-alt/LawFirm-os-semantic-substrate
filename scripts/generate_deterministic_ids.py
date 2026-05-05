import argparse
from hashlib import sha256


PREFIXES = {
    "exception-event": "EXC",
    "pressure-vector": "PV",
    "adaptation-proposal": "AP",
    "promotion-decision": "PD",
}


def make_id(kind: str, seed: str) -> str:
    prefix = PREFIXES[kind]
    digest = sha256(seed.encode("utf-8")).hexdigest()
    numeric = int(digest[:12], 16) % 1000000
    return f"{prefix}-{numeric:06d}"


def main():
    parser = argparse.ArgumentParser(description="Generate deterministic FMG governed-learning IDs")
    parser.add_argument("kind", choices=sorted(PREFIXES.keys()))
    parser.add_argument("seed", help="Stable seed string such as route|object|date")
    args = parser.parse_args()
    print(make_id(args.kind, args.seed))


if __name__ == "__main__":
    main()
