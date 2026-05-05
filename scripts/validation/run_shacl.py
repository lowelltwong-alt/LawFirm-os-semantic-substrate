from __future__ import annotations

from pathlib import Path
import sys

from rdflib import Graph
from rdflib.namespace import RDF, SH
from rdflib.term import URIRef
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[2]
SHAPES = ROOT / "shapes"
PAIRS = [
    (SHAPES / "core.ttl", SHAPES / "core.shacl.ttl"),
]


def load_graph(path: Path) -> Graph:
    graph = Graph()
    graph.parse(path, format="turtle")
    return graph


def namespace_of(term) -> str | None:
    value = str(term)
    if not value.startswith(("http://", "https://")):
        return None
    if "#" in value:
        return value.rsplit("#", 1)[0] + "#"
    if "/" in value:
        return value.rsplit("/", 1)[0] + "/"
    return value


def format_term(graph: Graph, term) -> str:
    try:
        return graph.namespace_manager.normalizeUri(term)
    except Exception:
        return str(term)


def check_focus_nodes(data: Graph, shapes: Graph, data_graph: Path, shape_graph: Path) -> list[str]:
    messages: list[str] = []
    target_classes = {
        target for target in shapes.objects(None, SH.targetClass) if isinstance(target, URIRef)
    }
    if not target_classes:
        return messages

    focus_nodes = {
        subject
        for target in target_classes
        for subject in data.subjects(RDF.type, target)
    }
    if focus_nodes:
        return messages

    observed_types = {obj for obj in data.objects(None, RDF.type)}
    target_namespaces = sorted(
        {namespace for target in target_classes if (namespace := namespace_of(target))}
    )
    observed_namespaces = sorted(
        {namespace for obj in observed_types if (namespace := namespace_of(obj))}
    )

    messages.append(
        f"FAIL CLOSED: {data_graph.name} against {shape_graph.name} is not testable because the data graph has no focus nodes for the shape graph target classes."
    )
    messages.append(
        "Shape target classes: "
        + ", ".join(sorted(format_term(shapes, target) for target in target_classes))
    )
    if observed_types:
        messages.append(
            "Data graph rdf:type values: "
            + ", ".join(sorted(format_term(data, obj) for obj in observed_types))
        )
    else:
        messages.append("Data graph rdf:type values: <none>")

    sh_namespace = namespace_of(SH.NodeShape)
    if observed_types and sh_namespace and all(
        namespace_of(obj) == sh_namespace for obj in observed_types if isinstance(obj, URIRef)
    ):
        messages.append(
            "The current data graph is a SHACL/seed graph rather than a same-namespace focus-node data graph for the core ontology targets."
        )

    if target_namespaces and observed_namespaces and set(target_namespaces).isdisjoint(observed_namespaces):
        messages.append(
            "Observed type namespaces do not overlap the shape target namespaces."
        )
        messages.append("Target namespaces: " + ", ".join(target_namespaces))
        messages.append("Observed namespaces: " + ", ".join(observed_namespaces))

    messages.append(
        "Core SHACL conformance is not currently claimed until a trustworthy same-namespace focus-node data graph exists for these targets."
    )
    messages.append(
        "A pySHACL PASS here would be vacuous, so the gate stops instead of reporting conformance."
    )
    return messages


def run_pair(data_graph: Path, shape_graph: Path) -> int:
    data = load_graph(data_graph)
    shapes = load_graph(shape_graph)

    preflight_failures = check_focus_nodes(data, shapes, data_graph, shape_graph)
    if preflight_failures:
        for message in preflight_failures:
            print(message)
        return 1

    conforms, _, results_text = validate(
        data_graph=data,
        shacl_graph=shapes,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=False,
        js=False,
    )
    if conforms:
        print(f"PASS: {data_graph.name} against {shape_graph.name}")
        return 0
    print(f"FAIL: {data_graph.name} against {shape_graph.name}")
    print(results_text)
    return 1


def main() -> int:
    failures = 0
    for data_graph, shape_graph in PAIRS:
        if not data_graph.exists() or not shape_graph.exists():
            print(f"SKIP: missing pair {data_graph} / {shape_graph}")
            continue
        failures += run_pair(data_graph, shape_graph)

    if failures:
        print(f"SHACL validation failed with {failures} failing pair(s).")
        return 1

    print("SHACL validation completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
