import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
EXPORT_ROOT = ROOT / "generated" / "phase5"
CAPABILITY_TWIN_ROOT = ROOT / "data" / "capability-twins"
GRAPH_MANIFEST_ROOT = ROOT / "graphs" / "manifests"


RISK_SCORES = {
    "low": 0.2,
    "medium": 0.5,
    "high": 0.8,
    "critical": 1.0,
}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_capability_twins() -> list[dict]:
    if not CAPABILITY_TWIN_ROOT.exists():
        return []
    twins: list[dict] = []
    for twin_path in sorted(CAPABILITY_TWIN_ROOT.glob("*.yaml")):
        twin = load_yaml(twin_path)
        if isinstance(twin, dict):
            twin["_source_path"] = str(twin_path.relative_to(ROOT))
            twins.append(twin)
    return twins


def load_graph_manifests() -> dict[str, dict]:
    manifests: dict[str, dict] = {}
    for manifest_path in sorted(GRAPH_MANIFEST_ROOT.glob("*.yaml")):
        manifest = load_yaml(manifest_path)
        if isinstance(manifest, dict) and manifest.get("id"):
            manifest["_source_path"] = str(manifest_path.relative_to(ROOT))
            manifests[manifest["id"]] = manifest
    return manifests


def normalize_trace_map(twin: dict, manifests: dict[str, dict]) -> dict[str, dict]:
    trace_map: dict[str, dict] = {}

    for mapping in twin.get("mapped_graph_manifests", []):
        manifest_id = mapping.get("graph_manifest_id")
        for node_mapping in mapping.get("capability_node_mappings", []):
            node_id = node_mapping.get("capability_node_id")
            if not node_id:
                continue
            trace_map.setdefault(node_id, {"claims": set(), "artifacts": set(), "governance": set(), "manifests": set()})
            trace_map[node_id]["claims"].update(node_mapping.get("claim_refs", []))
            trace_map[node_id]["artifacts"].update(node_mapping.get("artifact_refs", []))
            trace_map[node_id]["governance"].update(node_mapping.get("governance_decision_refs", []))
            if manifest_id:
                trace_map[node_id]["manifests"].add(manifest_id)

    for manifest_id, manifest in manifests.items():
        for trace in manifest.get("capability_node_traces", []):
            if trace.get("capability_twin_id") != twin.get("id"):
                continue
            node_id = trace.get("capability_node_id")
            if not node_id:
                continue
            trace_map.setdefault(node_id, {"claims": set(), "artifacts": set(), "governance": set(), "manifests": set()})
            trace_map[node_id]["claims"].update(trace.get("claim_refs", []))
            trace_map[node_id]["artifacts"].update(trace.get("artifact_refs", []))
            trace_map[node_id]["governance"].update(trace.get("governance_decision_refs", []))
            trace_map[node_id]["manifests"].add(manifest_id)

    return trace_map


def compute_node_health(node_id: str, twin: dict, trace: dict, inbound_dependencies: int) -> dict:
    maturity = float(twin.get("maturity_posture", {}).get("current_level", 1))
    maturity_score = min(1.0, maturity / 5.0)

    overall_risk = str(twin.get("risk_posture", {}).get("overall_risk", "medium")).lower()
    risk_score = RISK_SCORES.get(overall_risk, 0.5)

    telemetry_hooks = [h for h in twin.get("telemetry_hooks", []) if h.get("capability_node_id") == node_id]
    evidence_coverage = 1.0 if telemetry_hooks else 0.0
    trace_coverage = 1.0 if trace and trace["claims"] and trace["artifacts"] and trace["governance"] else 0.0

    dependency_penalty = min(0.3, inbound_dependencies * 0.06)

    health = max(
        0.0,
        min(
            1.0,
            (0.45 * maturity_score)
            + (0.25 * evidence_coverage)
            + (0.20 * trace_coverage)
            + (0.10 * (1 - risk_score))
            - dependency_penalty,
        ),
    )

    bottleneck_score = round((1 - health) + dependency_penalty + (0.2 if not telemetry_hooks else 0.0), 3)
    investment_priority = round((1 - health) * 0.65 + risk_score * 0.25 + dependency_penalty * 0.10, 3)

    return {
        "node_id": node_id,
        "health_score": round(health, 3),
        "maturity_score": round(maturity_score, 3),
        "risk_score": round(risk_score, 3),
        "evidence_coverage": evidence_coverage,
        "trace_coverage": trace_coverage,
        "inbound_dependencies": inbound_dependencies,
        "bottleneck_score": bottleneck_score,
        "investment_priority": investment_priority,
        "telemetry_hooks": [h.get("telemetry_id") for h in telemetry_hooks],
        "trace_summary": {
            "claims": sorted(trace["claims"]) if trace else [],
            "artifacts": sorted(trace["artifacts"]) if trace else [],
            "governance": sorted(trace["governance"]) if trace else [],
            "manifests": sorted(trace["manifests"]) if trace else [],
        },
    }


def build_capability_report(twin: dict, manifests: dict[str, dict]) -> dict:
    trace_map = normalize_trace_map(twin, manifests)
    node_ids = [node.get("capability_node_id") for node in twin.get("capability_tree", {}).get("nodes", []) if node.get("capability_node_id")]

    inbound_count = {node_id: 0 for node_id in node_ids}
    for edge in twin.get("dependency_graph", {}).get("edges", []):
        target = edge.get("to")
        if target in inbound_count:
            inbound_count[target] += 1

    node_health = [
        compute_node_health(node_id=node_id, twin=twin, trace=trace_map.get(node_id), inbound_dependencies=inbound_count.get(node_id, 0))
        for node_id in node_ids
    ]

    bottlenecks = sorted(
        [n for n in node_health if n["bottleneck_score"] >= 0.55],
        key=lambda n: (-n["bottleneck_score"], n["node_id"]),
    )
    investment_ranking = sorted(node_health, key=lambda n: (-n["investment_priority"], n["node_id"]))

    return {
        "capability_twin_id": twin.get("id"),
        "capability_id": twin.get("capability_id"),
        "capability_name": twin.get("capability_name"),
        "source": twin.get("_source_path"),
        "capability_health": {
            "overall_health_score": round(sum(n["health_score"] for n in node_health) / len(node_health), 3) if node_health else 0.0,
            "nodes": node_health,
        },
        "bottlenecks": bottlenecks,
        "investment_priority_ranking": [
            {
                "rank": idx + 1,
                "node_id": n["node_id"],
                "investment_priority": n["investment_priority"],
                "health_score": n["health_score"],
                "top_gaps": {
                    "trace_coverage": n["trace_coverage"],
                    "evidence_coverage": n["evidence_coverage"],
                    "inbound_dependencies": n["inbound_dependencies"],
                },
            }
            for idx, n in enumerate(investment_ranking)
        ],
    }


def main() -> int:
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)

    manifests = load_graph_manifests()
    capability_twins = load_capability_twins()

    report = {
        "pilot_slice": load_yaml(ROOT / "data" / "pilot-slices" / "doctrinal_core_v1.yaml"),
        "action_definition": load_yaml(ROOT / "data" / "action-types" / "action_definition.template.yaml"),
        "object_set_definition": load_yaml(ROOT / "data" / "object-sets" / "object_set_definition.template.yaml"),
        "capability_reports": [build_capability_report(twin, manifests) for twin in capability_twins],
    }

    output = EXPORT_ROOT / "pilot_slice_report.json"
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"WROTE: {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
