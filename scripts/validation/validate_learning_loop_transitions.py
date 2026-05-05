from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "retrieval"
EX = ROOT / "examples"
ENUMS = ROOT / "schema" / "enums"

PROMOTION_STATUSES = {"approved_for_pilot", "promoted"}
ALLOCATION_ACTIONS = {"continue", "pivot", "scale", "sunset"}
GATE_OK = {"approved", "approved_with_monitoring"}
ALLOWED: dict[str, set[tuple[str, str]]] = {
    "hypothesis": {("proposed", "active"), ("active", "validated"), ("active", "invalidated"), ("validated", "archived"), ("invalidated", "archived")},
    "experiment": {("planned", "running"), ("planned", "aborted"), ("running", "completed"), ("running", "failed"), ("running", "aborted"), ("completed", "archived"), ("failed", "archived"), ("aborted", "archived")},
    "learning_event": {("captured", "analyzed"), ("captured", "accepted"), ("captured", "rejected"), ("analyzed", "accepted"), ("analyzed", "rejected"), ("accepted", "archived"), ("rejected", "archived")},
    "allocation_decision": {("proposed", "approved"), ("proposed", "enacted"), ("approved", "enacted"), ("enacted", "superseded"), ("superseded", "retired"), ("enacted", "retired")},
}
CONF = {"unknown": 0, "low": 1, "medium": 2, "high": 3}
EVID = {"thin_support": 1, "indirect_inference": 2, "mixed_support": 3, "strong_curated_secondary": 4, "direct_primary_text": 5}
THRESH: dict[str, tuple[str, str]] = {
    "scale": ("high", "strong_curated_secondary"),
    "continue": ("medium", "mixed_support"),
    "pivot": ("medium", "mixed_support"),
    "sunset": ("low", "thin_support"),
}


def ly(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def lj(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def enum(name: str) -> set[str]:
    data = ly(ENUMS / f"{name}.yaml")
    vals = data.get("values", []) if isinstance(data, dict) else []
    return {str(v) for v in vals}


def load_yaml(path: Path) -> Any:
    """Compatibility wrapper used by the unit test and older call sites."""
    return ly(path)


def load_enum(name: str) -> set[str]:
    """Compatibility wrapper used by the unit test and older call sites."""
    return enum(name)


def ne(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, (str, bytes, list, dict, tuple, set)):
        return len(v) > 0
    return True


def req_enum(f: list[str], p: Path, v: Any, vals: set[str], name: str) -> None:
    if not ne(v):
        f.append(f"{p}: missing '{name}'")
    elif str(v) not in vals:
        f.append(f"{p}: '{name}' value '{v}' is not in enum set")


def req_bool(f: list[str], p: Path, v: Any, exp: bool, name: str) -> None:
    if v is not exp:
        f.append(f"{p}: '{name}' must be {exp}")


def req_in(f: list[str], p: Path, vals: Any, exp: str, name: str) -> None:
    if not isinstance(vals, list) or exp not in vals:
        f.append(f"{p}: '{name}' must include '{exp}'")


def validate_exact_ref_set(
    failures: list[str],
    path: Path,
    values: Any,
    allowed: set[str],
    label: str,
) -> None:
    if not isinstance(values, list) or not values:
        failures.append(f"{path}: '{label}' must be a non-empty list")
        return
    for value in values:
        if str(value) not in allowed:
            failures.append(
                f"{path}: '{label}' value '{value}' must resolve to one of {sorted(allowed)}"
            )


def check_boundary(f: list[str], p: Path, data: dict[str, Any], extras: tuple[str, ...] = ()) -> None:
    b = data.get("mutation_boundary")
    if not isinstance(b, dict):
        f.append(f"{p}: missing 'mutation_boundary'")
        return
    req_bool(f, p, b.get("no_direct_canonical_mutation"), True, "mutation_boundary.no_direct_canonical_mutation")
    req_bool(f, p, b.get("promotion_decision_required_for_canonical_change"), True, "mutation_boundary.promotion_decision_required_for_canonical_change")
    for k in extras:
        req_bool(f, p, b.get(k), True, f"mutation_boundary.{k}")


def v_feedback(p: Path, d: dict[str, Any], f: list[str], review_status: set[str], reviewer_role: set[str], trust_zone: set[str]) -> None:
    review = d.get("review_metadata") or {}
    if ne(review):
        req_enum(f, p, review.get("review_status"), review_status, "review_metadata.review_status")
        req_enum(f, p, review.get("reviewer_role"), reviewer_role, "review_metadata.reviewer_role")
    if d.get("retrieval_feedback_status") == "actioned":
        if not isinstance(review, dict) or not review:
            f.append(f"{p}: feedback with status 'actioned' requires review_metadata")
        elif not ne(review.get("reviewed_by")) or not ne(review.get("reviewed_at")):
            f.append(f"{p}: feedback with status 'actioned' requires review_metadata.reviewed_by and review_metadata.reviewed_at")
    zone = d.get("authority_zone")
    if ne(zone) and str(zone) not in trust_zone:
        f.append(f"{p}: authority_zone '{zone}' is not a valid trust_zone enum value")


def v_proposal(p: Path, d: dict[str, Any], f: list[str], evidence: set[str], alignment: set[str], trust_zone: set[str]) -> None:
    if d.get("proposal_promotion_status") in PROMOTION_STATUSES:
        a = d.get("alignment_assessment") or {}
        if not isinstance(a, dict) or not a:
            f.append(f"{p}: proposal status '{d.get('proposal_promotion_status')}' requires alignment_assessment")
            return
        req_enum(f, p, a.get("evidence_sufficiency"), evidence, "alignment_assessment.evidence_sufficiency")
        req_enum(f, p, a.get("alignment_degree"), alignment, "alignment_assessment.alignment_degree")
    zone = d.get("authority_zone")
    if ne(zone) and str(zone) not in trust_zone:
        f.append(f"{p}: authority_zone '{zone}' is not a valid trust_zone enum value")


def wf_steps(path: Path, f: list[str]) -> list[dict[str, Any]]:
    data = ly(path)
    rel = path.relative_to(ROOT)
    if not isinstance(data, dict):
        f.append(f"{rel}: workflow must be a mapping")
        return []
    steps = data.get("steps")
    if not isinstance(steps, list):
        f.append(f"{rel}: workflow must include a list field 'steps'")
        return []
    return [s for s in steps if isinstance(s, dict)]


def v_step(p: Path, step: dict[str, Any], f: list[str], states: dict[str, set[str]]) -> None:
    kind = str(step.get("object_type", ""))
    src = step.get("from_state")
    dst = step.get("to_state")
    if kind not in ALLOWED:
        f.append(f"{p}: unsupported object_type '{kind}' in workflow step")
        return
    if not ne(src) or not ne(dst):
        f.append(f"{p}: step {step.get('id')} missing from_state/to_state")
        return
    vals = states.get(kind, set())
    if str(src) not in vals:
        f.append(f"{p}: step {step.get('id')} from_state '{src}' is outside {kind} state enum")
    if str(dst) not in vals:
        f.append(f"{p}: step {step.get('id')} to_state '{dst}' is outside {kind} state enum")
    if (str(src), str(dst)) not in ALLOWED[kind]:
        f.append(f"{p}: illegal {kind} transition {src} -> {dst} in step {step.get('id')}")


def v_alloc(p: Path, step: dict[str, Any], f: list[str], conf: set[str], evidence: set[str], action_types: set[str]) -> None:
    action = str(step.get("action_type", ""))
    c = str(step.get("confidence_level", ""))
    e = str(step.get("evidence_sufficiency", ""))
    refs = step.get("evidence_refs")
    if action not in action_types:
        f.append(f"{p}: allocation step {step.get('id')} has invalid action_type '{action}'")
        return
    if action not in ALLOCATION_ACTIONS:
        f.append(f"{p}: allocation step {step.get('id')} action_type '{action}' must be one of {sorted(ALLOCATION_ACTIONS)}")
        return
    if c not in conf:
        f.append(f"{p}: allocation step {step.get('id')} confidence_level '{c}' is invalid")
        return
    if e not in evidence:
        f.append(f"{p}: allocation step {step.get('id')} evidence_sufficiency '{e}' is invalid")
        return
    if not isinstance(refs, list) or not refs:
        f.append(f"{p}: allocation step {step.get('id')} requires non-empty evidence_refs before allocation changes")
        return
    rc, re = THRESH[action]
    if CONF[c] < CONF[rc]:
        f.append(f"{p}: allocation step {step.get('id')} action '{action}' requires confidence >= {rc}")
    if EVID[e] < EVID[re]:
        f.append(f"{p}: allocation step {step.get('id')} action '{action}' requires evidence_sufficiency >= {re}")


def v_policy(p: Path, d: dict[str, Any], f: list[str], action_types: set[str], conf: set[str], evidence: set[str], states: set[str]) -> None:
    for k in ("id", "object_type", "policy_rows"):
        if not ne(d.get(k)):
            f.append(f"{p}: transition policy missing required top-level key '{k}'")
    if d.get("object_type") != "learning_transition_policy":
        f.append(f"{p}: transition policy object_type must be 'learning_transition_policy'")
    rows = d.get("policy_rows")
    if not isinstance(rows, list) or not rows:
        f.append(f"{p}: transition policy must include a non-empty list 'policy_rows'")
        return
    for i, row in enumerate(rows):
        ref = f"policy_rows[{i}]"
        if not isinstance(row, dict):
            f.append(f"{p}: {ref} must be a mapping")
            continue
        if ne(row.get("action_type")):
            ref = f"{ref} ({row.get('action_type')})"
        act = row.get("action_type")
        if not ne(act):
            f.append(f"{p}: {ref} missing 'action_type'")
        elif str(act) not in action_types:
            f.append(f"{p}: {ref} action_type '{act}' is not in action_type enum")
        mc = row.get("min_confidence_level")
        if not ne(mc):
            f.append(f"{p}: {ref} missing 'min_confidence_level'")
        elif str(mc) not in conf:
            f.append(f"{p}: {ref} min_confidence_level '{mc}' is not in confidence_level enum")
        me = row.get("min_evidence_sufficiency")
        if not ne(me):
            f.append(f"{p}: {ref} missing 'min_evidence_sufficiency'")
        elif str(me) not in evidence:
            f.append(f"{p}: {ref} min_evidence_sufficiency '{me}' is not in evidence_sufficiency enum")
        allowed = row.get("allowed_states")
        if not isinstance(allowed, list) or not allowed:
            f.append(f"{p}: {ref} must include a non-empty list 'allowed_states'")
            continue
        for state in allowed:
            if str(state) not in states:
                f.append(f"{p}: {ref} allowed_state '{state}' is not in allocation_decision_state enum")


def validate_transition_policy(
    path: Path,
    data: dict[str, Any],
    failures: list[str],
    action_types: set[str],
    confidence: set[str],
    evidence: set[str],
    states: set[str],
) -> None:
    """Compatibility wrapper used by the unit test and older call sites."""
    v_policy(path, data, failures, action_types, confidence, evidence, states)


def validate_innovation_payloads(
    payloads: dict[str, dict[str, Any]],
    rel_paths: dict[str, Path],
    failures: list[str],
) -> None:
    required_keys = ("exc", "pv", "ap", "pd", "opp", "spr", "pil", "gate", "scale", "brief")
    missing = [key for key in required_keys if key not in payloads]
    for key in missing:
        failures.append(f"{rel_paths[key]}: required Innovation OS example is missing")
    if missing:
        return

    exc = payloads["exc"]
    pv = payloads["pv"]
    ap = payloads["ap"]
    pd = payloads["pd"]
    opp = payloads["opp"]
    spr = payloads["spr"]
    pil = payloads["pil"]
    gate = payloads["gate"]
    scale = payloads["scale"]
    brief = payloads["brief"]
    rp = rel_paths

    if exc.get("schema_type") != "exception-event":
        failures.append(f"{rp['exc']}: schema_type must be 'exception-event'")
    if (exc.get("route") or {}).get("promotion_gate_required") is not True:
        failures.append(f"{rp['exc']}: route.promotion_gate_required must be true")
    req_in(failures, rp["exc"], exc.get("pressure_vector_refs"), str(pv.get("pressure_vector_id")), "pressure_vector_refs")
    if pv.get("schema_type") != "pressure-vector":
        failures.append(f"{rp['pv']}: schema_type must be 'pressure-vector'")
    req_in(failures, rp["pv"], pv.get("derived_from_exception_ids"), str(exc.get("exception_id")), "derived_from_exception_ids")
    req_in(failures, rp["pv"], pv.get("suggested_follow_on_families"), "opportunity-object", "suggested_follow_on_families")
    check_boundary(failures, rp["pv"], pv)
    if ap.get("schema_type") != "adaptation-proposal":
        failures.append(f"{rp['ap']}: schema_type must be 'adaptation-proposal'")
    req_in(failures, rp["ap"], ap.get("source_exception_ids"), str(exc.get("exception_id")), "source_exception_ids")
    req_in(failures, rp["ap"], ap.get("source_pressure_vector_ids"), str(pv.get("pressure_vector_id")), "source_pressure_vector_ids")
    ap_boundary = ap.get("canonical_mutation_boundary") or {}
    req_bool(failures, rp["ap"], ap_boundary.get("direct_mutation_allowed"), False, "canonical_mutation_boundary.direct_mutation_allowed")
    req_bool(failures, rp["ap"], ap_boundary.get("promotion_decision_required"), True, "canonical_mutation_boundary.promotion_decision_required")
    if opp.get("schema_type") != "opportunity-object":
        failures.append(f"{rp['opp']}: schema_type must be 'opportunity-object'")
    opp_id = str(opp.get("opportunity_id", ""))
    spr_id = str(spr.get("sprint_id", ""))
    pil_id = str(pil.get("pilot_id", ""))
    opp_refs = opp.get("source_refs") or {}
    req_in(failures, rp["opp"], opp_refs.get("pressure_vector_ids"), str(pv.get("pressure_vector_id")), "source_refs.pressure_vector_ids")
    req_in(failures, rp["opp"], opp_refs.get("exception_event_ids"), str(exc.get("exception_id")), "source_refs.exception_event_ids")
    nxt = opp.get("next_step") or {}
    if nxt.get("action") != "prepare_sprint" or nxt.get("target_family") != "sprint-object":
        failures.append(f"{rp['opp']}: expected next_step to prepare a sprint-object in the active example chain")
    check_boundary(failures, rp["opp"], opp)
    if spr.get("schema_type") != "sprint-object":
        failures.append(f"{rp['spr']}: schema_type must be 'sprint-object'")
    req_in(failures, rp["spr"], (spr.get("source_refs") or {}).get("opportunity_ids"), opp_id, "source_refs.opportunity_ids")
    spr_refs = spr.get("source_refs") or {}
    validate_exact_ref_set(
        failures,
        rp["spr"],
        spr_refs.get("pressure_vector_ids"),
        {str(pv.get("pressure_vector_id"))},
        "source_refs.pressure_vector_ids",
    )
    check_boundary(failures, rp["spr"], spr, ("validation_gate_required_before_scale",))
    if pil.get("schema_type") != "pilot-object":
        failures.append(f"{rp['pil']}: schema_type must be 'pilot-object'")
    req_in(failures, rp["pil"], (pil.get("source_refs") or {}).get("opportunity_ids"), opp_id, "source_refs.opportunity_ids")
    req_in(failures, rp["pil"], (pil.get("source_refs") or {}).get("sprint_ids"), spr_id, "source_refs.sprint_ids")
    g = pil.get("gate_requirements") or {}
    if g.get("go_no_go_gate") != "validation-gate-record":
        failures.append(f"{rp['pil']}: gate_requirements.go_no_go_gate must be 'validation-gate-record'")
    req_bool(failures, rp["pil"], g.get("validation_gate_record_required"), True, "gate_requirements.validation_gate_record_required")
    check_boundary(failures, rp["pil"], pil, ("validation_gate_required_before_scale",))
    if gate.get("schema_type") != "validation-gate-record":
        failures.append(f"{rp['gate']}: schema_type must be 'validation-gate-record'")
    tgt = gate.get("target_ref") or {}
    if tgt.get("schema_type") != "pilot-object":
        failures.append(f"{rp['gate']}: target_ref.schema_type must be 'pilot-object'")
    if tgt.get("object_id") != pil_id:
        failures.append(f"{rp['gate']}: target_ref.object_id must reference the pilot example")
    if tgt.get("related_opportunity_id") != opp_id:
        failures.append(f"{rp['gate']}: target_ref.related_opportunity_id must reference the opportunity example")
    if gate.get("status") not in GATE_OK:
        failures.append(f"{rp['gate']}: status must be one of {sorted(GATE_OK)} for the active rollout example")
    check_boundary(failures, rp["gate"], gate, ("promotion_candidate_only",))
    if scale.get("schema_type") != "scale-package-object":
        failures.append(f"{rp['scale']}: schema_type must be 'scale-package-object'")
    req_in(failures, rp["scale"], (scale.get("source_refs") or {}).get("pilot_ids"), pil_id, "source_refs.pilot_ids")
    req_in(failures, rp["scale"], (scale.get("source_refs") or {}).get("validation_gate_record_ids"), str(gate.get("gate_record_id")), "source_refs.validation_gate_record_ids")
    req_in(failures, rp["scale"], (scale.get("source_refs") or {}).get("opportunity_ids"), opp_id, "source_refs.opportunity_ids")
    check_boundary(failures, rp["scale"], scale, ("human_approval_required_before_rollout",))
    if brief.get("schema_type") != "view-executive-brief":
        failures.append(f"{rp['brief']}: schema_type must be 'view-executive-brief'")
    if brief.get("schema_id") != "view-executive-brief-v1":
        failures.append(f"{rp['brief']}: schema_id must be 'view-executive-brief-v1'")
    if brief.get("schema_version") != "draft-v1":
        failures.append(f"{rp['brief']}: schema_version must be 'draft-v1'")
    validate_exact_ref_set(
        failures,
        rp["brief"],
        brief.get("evidence_refs"),
        {
            str(exc.get("exception_id")),
            str(pv.get("pressure_vector_id")),
            opp_id,
            spr_id,
        },
        "evidence_refs",
    )
    if pd.get("schema_type") != "promotion-decision":
        failures.append(f"{rp['pd']}: schema_type must be 'promotion-decision'")
    if pd.get("proposal_id") != ap.get("proposal_id"):
        failures.append(f"{rp['pd']}: proposal_id must reference the active adaptation-proposal example")
    inputs = pd.get("input_artifacts") or {}
    req_in(failures, rp["pd"], inputs.get("exception_event_ids"), str(exc.get("exception_id")), "input_artifacts.exception_event_ids")
    req_in(failures, rp["pd"], inputs.get("pressure_vector_ids"), str(pv.get("pressure_vector_id")), "input_artifacts.pressure_vector_ids")
    eb = pd.get("execution_boundary") or {}
    req_bool(failures, rp["pd"], eb.get("requires_reviewed_inputs"), True, "execution_boundary.requires_reviewed_inputs")
    req_bool(failures, rp["pd"], eb.get("raw_exception_direct_write_allowed"), False, "execution_boundary.raw_exception_direct_write_allowed")
    if eb.get("may_update_canonical_objects") is False and (not isinstance(eb.get("blocked_targets"), list) or not eb.get("blocked_targets")):
        failures.append(f"{rp['pd']}: blocked_targets must be populated when canonical updates are disallowed")


def v_innovation(f: list[str]) -> None:
    paths = {
        "exc": EX / "exceptions" / "events" / "EXC-000101.json",
        "pv": EX / "exceptions" / "pressure-vectors" / "PV-000101.json",
        "ap": EX / "exceptions" / "adaptation-proposals" / "AP-000001.json",
        "pd": EX / "exceptions" / "promotion-decisions" / "PD-000001.json",
        "opp": EX / "innovation-os" / "opportunity-object.example.json",
        "spr": EX / "innovation-os" / "sprint-object.example.json",
        "pil": EX / "innovation-os" / "pilot-object.example.json",
        "gate": EX / "innovation-os" / "validation-gate-record.example.json",
        "scale": EX / "innovation-os" / "scale-package-object.example.json",
        "brief": EX / "innovation-os" / "executive-brief-object.example.json",
    }
    miss = [p.relative_to(ROOT) for p in paths.values() if not p.exists()]
    for p in miss:
        f.append(f"{p}: required Innovation OS example is missing")
    if miss:
        return
    d = {k: lj(v) for k, v in paths.items()}
    rp = {k: v.relative_to(ROOT) for k, v in paths.items()}
    validate_innovation_payloads(d, rp, f)


def main() -> int:
    f: list[str] = []
    review_status = enum("review_status")
    reviewer_role = enum("reviewer_role")
    trust_zone = enum("trust_zone")
    evidence = enum("evidence_sufficiency")
    alignment = enum("alignment_degree")
    confidence = enum("confidence_level")
    action_types = enum("action_type")
    states = {
        "hypothesis": enum("hypothesis_state"),
        "experiment": enum("experiment_state"),
        "learning_event": enum("learning_event_state"),
        "allocation_decision": enum("allocation_decision_state"),
    }

    feedback: dict[str, tuple[Path, dict[str, Any]]] = {}
    proposals: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(DATA.glob("*.yaml")):
        data = ly(path)
        if not isinstance(data, dict):
            continue
        rel = path.relative_to(ROOT)
        kind = data.get("object_type")
        if kind == "retrieval_feedback":
            feedback[str(data.get("id"))] = (rel, data)
            v_feedback(rel, data, f, review_status, reviewer_role, trust_zone)
        elif kind == "proposal_promotion":
            proposals.append((rel, data))
            v_proposal(rel, data, f, evidence, alignment, trust_zone)

    for rel, prop in proposals:
        if prop.get("proposal_promotion_status") not in PROMOTION_STATUSES:
            continue
        src = str(prop.get("source_feedback_ref", ""))
        if src not in feedback:
            f.append(f"{rel}: source_feedback_ref '{src}' not found in data/retrieval")
            continue
        src_rel, src_data = feedback[src]
        review = src_data.get("review_metadata") or {}
        if not isinstance(review, dict) or not review:
            f.append(f"{rel}: promoted proposal references feedback {src} without review_metadata ({src_rel})")
            continue
        if not ne(review.get("review_status")):
            f.append(f"{src_rel}: missing review_metadata.review_status for feedback backing promoted proposal {prop.get('id')}")
        if not ne(review.get("reviewer_role")):
            f.append(f"{src_rel}: missing review_metadata.reviewer_role for feedback backing promoted proposal {prop.get('id')}")

    wfs = sorted(EX.glob("learning_loop_*.yaml"))
    if not wfs:
        f.append("examples/: expected learning_loop_*.yaml workflow examples")
    for path in wfs:
        rel = path.relative_to(ROOT)
        for step in wf_steps(path, f):
            v_step(rel, step, f, states)
            if step.get("object_type") == "allocation_decision":
                v_alloc(rel, step, f, confidence, evidence, action_types)

    pols = sorted(EX.glob("learning_transition_policy*.yaml"))
    if not pols:
        f.append("examples/: expected learning_transition_policy*.yaml policy examples")
    for path in pols:
        rel = path.relative_to(ROOT)
        data = ly(path)
        if not isinstance(data, dict):
            f.append(f"{rel}: transition policy must be a mapping")
            continue
        v_policy(rel, data, f, action_types, confidence, evidence, states["allocation_decision"])

    v_innovation(f)

    if f:
        print("LEARNING LOOP TRANSITION VALIDATION FAILURES:")
        for item in f:
            print(f"- {item}")
        return 1
    print("Learning-loop and Innovation OS transition validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
