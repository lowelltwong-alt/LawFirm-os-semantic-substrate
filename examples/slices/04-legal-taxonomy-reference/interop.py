"""Offline crosswalk and search demonstration for fictional firm data."""
from argparse import ArgumentParser
from collections import Counter
from copy import deepcopy
from datetime import date
from hashlib import sha256
from pathlib import Path
import json
import os
import xml.etree.ElementTree as ET

from jsonschema import Draft202012Validator, FormatChecker

from engagement import EngagementView, read_bundle

HERE = Path(__file__).resolve().parent
SCHEMA = read_bundle(HERE / "interop.schema.json")
PART_FACETS = {
    "practice-kind": "practice",
    "document-kind": "document",
    "event-kind": "work-event",
    "issue-kind": "issue",
}
SEARCH_RELATIONS = {"exact", "broader-target"}
OWL = "{http://www.w3.org/2002/07/owl#}"
RDF = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
RDFS = "{http://www.w3.org/2000/01/rdf-schema#}"


def shape(data, kind):
    Draft202012Validator({**SCHEMA, "$ref": f"#/$defs/{kind}"},
                         format_checker=FormatChecker()).validate(data)


def unique(rows, field):
    keys = [row[field] for row in rows]
    repeated = sorted(key for key, count in Counter(keys).items() if count > 1)
    if repeated:
        raise ValueError(f"duplicate {field}: {', '.join(repeated)}")
    return {row[field]: row for row in rows}


class Vocabulary:
    def __init__(self, data):
        data = deepcopy(data)
        shape(data, "vocabulary")
        self.id = data["id"]
        self.version = data["version"]
        self.concepts = unique(data["concepts"], "id")
        labels = [(row["facet"], row["label"].casefold()) for row in self.concepts.values()]
        if len(labels) != len(set(labels)):
            raise ValueError("duplicate preferred label within a facet")
        for key, concept in self.concepts.items():
            if concept["source"] not in data["sources"]:
                raise ValueError(f"unknown source for {key}")
            for relation in ("broader", "replacement"):
                if relation not in concept:
                    continue
                target = concept[relation]
                if target not in self.concepts or self.concepts[target]["facet"] != concept["facet"]:
                    raise ValueError(f"invalid {relation} for {key}: {target}")
                if target == key or relation == "replacement" and (
                    concept["status"] != "deprecated" or self.concepts[target]["status"] != "active"
                ):
                    raise ValueError(f"invalid {relation} for {key}: {target}")
            tuple(self.ancestors(key))

    def ancestors(self, key):
        seen = {key}
        parent = self.concepts[key].get("broader")
        while parent:
            if parent in seen:
                raise ValueError(f"hierarchy cycle from {key}")
            if parent not in self.concepts:
                raise ValueError(f"unknown broader target {parent}")
            seen.add(parent)
            yield parent
            parent = self.concepts[parent].get("broader")


def ontology_entities(path, expected_hash):
    raw = Path(path).read_bytes()
    if sha256(raw).hexdigest() != expected_hash:
        raise ValueError("SALI snapshot checksum mismatch")
    root = ET.fromstring(raw)
    entities = {}
    for element in root.findall(f"{OWL}Class"):
        iri = element.get(f"{RDF}about")
        if iri:
            label = element.findtext(f"{RDFS}label", "")
            parents = {parent.get(f"{RDF}resource") for parent in element.findall(f"{RDFS}subClassOf")}
            entities[iri] = (label, parents - {None})
    return entities


def verify_sali(data, vocabulary, owl_path):
    shape(data, "sali")
    entities = ontology_entities(owl_path, data["sha256"])
    identifiers, exact = set(), {}
    for row in data["terms"]:
        key, iri, parent = row["concept"], row["iri"], row["parent_iri"]
        if key not in vocabulary.concepts:
            raise ValueError(f"unknown candidate concept for SALI mapping: {key}")
        identity = (key, iri)
        if identity in identifiers:
            raise ValueError(f"duplicate SALI assertion: {identity}")
        identifiers.add(identity)
        actual = entities.get(iri)
        if actual is None or actual[0] != row["label"] or parent not in actual[1] or (
            entities.get(parent, ("", set()))[0] != row["parent_label"]
        ):
            raise ValueError(f"SALI identifier, label or named parent mismatch: {iri}")
        if row["relation"] == "exact":
            if iri in exact or key in exact.values():
                raise ValueError(f"exact SALI alignment is not one to one: {iri}")
            exact[iri] = key
    return list(data["terms"])


class Crosswalk:
    def __init__(self, data, vocabulary, engagements):
        data = deepcopy(data)
        shape(data, "crosswalk")
        if (data["target_scheme"], data["target_version"]) != (vocabulary.id, vocabulary.version):
            raise ValueError("crosswalk targets a different vocabulary revision")
        self.data = data
        self.vocabulary = vocabulary
        self.definitions = unique(data["codes"], "code")
        self.mappings = unique(data["maps"], "code")
        unique(data["maps"], "id")
        unique(data["assignments"], "id")
        for assignment in data["assignments"]:
            if assignment["engagement"] not in engagements:
                raise ValueError(f"assignment references unknown engagement: {assignment['id']}")
        for code, rule in self.mappings.items():
            if code not in self.definitions:
                raise ValueError(f"mapping has no code definition: {code}")
            components = unique(rule["components"], "part")
            parts = set(components)
            omitted = set(rule["unmapped"])
            if parts & omitted or parts | omitted != set(self.definitions[code]["components"]):
                raise ValueError(f"mapping component inventory incomplete or overlapping: {code}")
            for part, row in components.items():
                concept = self.vocabulary.concepts.get(row["target"])
                if concept is None or PART_FACETS.get(part) != concept["facet"]:
                    raise ValueError(f"invalid target facet for {code}/{part}: {row['target']}")
                if concept["status"] != "active" and rule["review_status"] == "synthetic-verified":
                    raise ValueError(f"active mapping targets deprecated concept: {row['target']}")

    def derive(self, assignment):
        result = {
            "assignment": dict(assignment),
            "source_scheme": self.data["id"],
            "dictionary_version": self.data["version"],
            "mapping_version": self.data["mapping_version"],
            "target_scheme": self.vocabulary.id,
            "target_version": self.vocabulary.version,
            "targets": [],
        }
        if assignment["source_revision"] != self.data["version"]:
            return {**result, "status": "source-version-unavailable"}
        code = assignment["code"]
        if code not in self.definitions:
            return {**result, "status": "unknown-code"}
        rule = self.mappings.get(code)
        if not rule:
            return {**result, "status": "unmapped"}
        if rule["review_status"] != "synthetic-verified":
            return {**result, "status": rule["review_status"], "mapping_id": rule["id"]}
        safe = [{**row, "usage": "search-only"} for row in rule["components"]
                if row["relation"] in SEARCH_RELATIONS]
        skipped = set(rule["unmapped"]) | {row["part"] for row in rule["components"]
                                         if row["relation"] not in SEARCH_RELATIONS}
        status = "partial" if safe and skipped else "mapped" if safe else "needs-review"
        return {**result, "status": status, "mapping_id": rule["id"], "targets": safe,
                "unmapped_components": sorted(skipped)}

    def reverse(self, target_ids):
        desired = set(target_ids)
        if not desired:
            return {"status": "needs-review", "candidates": []}
        candidates, complete = [], []
        for code, rule in self.mappings.items():
            if rule["review_status"] not in {"synthetic-verified", "proposed"} or not rule["components"]:
                continue
            targets = {row["target"] for row in rule["components"]}
            if targets != desired:
                continue
            candidates.append(code)
            rows = rule["components"]
            if (rule["review_status"] == "synthetic-verified" and not rule["unmapped"]
                    and len(targets) == len(rows) and all(row["relation"] == "exact" for row in rows)):
                complete.append(code)
        if len(candidates) == len(complete) == 1:
            return {"status": "exact-round-trip", "candidates": complete}
        return {"status": "needs-review", "candidates": sorted(candidates)}

    def search(self, concept, view, narrower=False, known_by=None):
        cutoff = date.fromisoformat(known_by).isoformat() if known_by else view.as_of
        target = self.vocabulary.concepts.get(concept)
        if not target or target["status"] != "active":
            return []
        hits = set()
        for assignment in self.data["assignments"]:
            if assignment["engagement"] not in view.engagements:
                continue
            if assignment["effective"] > view.as_of or assignment["observed"] > cutoff:
                continue
            for mapping in self.derive(assignment)["targets"]:
                actual = mapping["target"]
                if actual == concept or narrower and concept in self.vocabulary.ancestors(actual):
                    hits.add(assignment["engagement"])
        return sorted(hits)


def inputs(root=HERE):
    return tuple(read_bundle(root / name) for name in (
        "worked-matters.json", "practice-vocabulary.json",
        "fictional-firm-crosswalk.json", "sali-alignment.proposed.json",
    ))


def run(as_of, owl_path):
    bundle, vocab_data, source, sali = inputs()
    view = EngagementView(bundle, as_of)
    vocab = Vocabulary(vocab_data)
    crosswalk = Crosswalk(source, vocab, {row["id"] for row in bundle["engagements"]})
    proposed = verify_sali(sali, vocab, owl_path)
    mapped = [crosswalk.derive(assignment) for assignment in source["assignments"]]
    sali_candidates = [
        {"assignment_id": row["assignment"]["id"], "source_code": row["assignment"]["code"],
         "engagement": row["assignment"]["engagement"], "concept": tag["target"],
         "local_relation": tag["relation"], "iri": external["iri"],
         "external_relation": external["relation"], "status": "proposed",
         "usage": "comparison-only"}
        for row in mapped
        if row["assignment"]["engagement"] in view.engagements
        and row["assignment"]["effective"] <= as_of and row["assignment"]["observed"] <= as_of
        for tag in row["targets"] for external in proposed if external["concept"] == tag["target"]
    ]
    return {
        "as_of": as_of,
        "synthetic": True,
        "sali_reference": {k: sali[k] for k in ("release", "commit", "sha256", "ontology", "license")},
        "verified_external_identifiers_and_named_parents": len(proposed),
        "sali_semantic_matches": "proposed; identifier verification only",
        "mapped_sources": mapped,
        "sali_candidates": sali_candidates,
        "search": {
            "premises": crosswalk.search("practice-premises", view),
            "tort_with_narrower_practices": crosswalk.search("practice-tort", view, narrower=True),
            "insurance_with_narrower_practices": crosswalk.search("practice-insurance", view, narrower=True),
            "deposition_document": crosswalk.search("document-deposition", view),
            "deposition_event": crosswalk.search("work-deposition", view),
            "our_firm_insurer_representation": view.represented("our-firm", "carrier"),
        },
        "reverse": {
            "unique_event": crosswalk.reverse(["work-deposition"]),
            "transcript_with_local_alternative": crosswalk.reverse(["document-deposition"]),
        },
    }


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default="2026-06-20")
    parser.add_argument("--sali-owl", type=Path, default=Path(os.environ.get("LAWFIRM_TAXONOMY_SALI_OWL", "LMSS.owl")))
    options = parser.parse_args()
    try:
        print(json.dumps(run(options.as_of, options.sali_owl), indent=2, ensure_ascii=True))
    except (OSError, ValueError, ET.ParseError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
