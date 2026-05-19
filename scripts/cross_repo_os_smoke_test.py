"""PR-10 cross-repo OS smoke test (read-only synthetic flow).

Proves the five LawFirm OS repos align on contract surface and artifact compatibility:
  Substrate surface → LKR grounding → Orchestrator ContextBundle / Execution / EvidencePacket
  → Exception Lake central admission (PR-06) → defect/eval checks.

No live APIs, no production data, no substrate mutation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

FIXED_AT = "2026-05-18T20:00:00Z"
RUN_ID = "run-pr10-smoke"
SMOKE_CONFIG = {
    "allowed_tool_ids": frozenset({"synthetic.read_only", "synthetic.write_with_approval"}),
    "allowed_route_ids": frozenset({"route.synthetic_read", "route.synthetic_write"}),
    "allowed_event_classes": frozenset({"synthetic.read", "synthetic.write", "synthetic.external"}),
    "write_actions_with_approval": frozenset({"write_with_approval"}),
}

REPO_ALIASES: dict[str, list[str]] = {
    "substrate": ["LawFirm-os-semantic-substrate"],
    "orchestrator": ["LawFirm-os-orchestrator", "LawFirm-os-orchestrator-main"],
    "lake": ["LawFirm-os-exceptions-lake-runtime-main", "LawFirm-os-exceptions-lake-runtime"],
    "lkr": ["LawFirm-os-legal-knowledge-runtime", "LawFirm-os-legal-knowledge-runtime-main"],
    "skills": ["LawFirm-os-skills-registry", "LawFirm-os-skills-registry-main"],
}


@dataclass(frozen=True)
class WorkspaceRepos:
    workspace: Path
    substrate: Path
    orchestrator: Path
    lake: Path
    lkr: Path
    skills: Path


@dataclass
class SmokeResult:
    ok: bool
    contract_surface_sha256: str
    errors: list[str] = field(default_factory=list)
    valid_path: dict[str, Any] = field(default_factory=dict)
    missing_passport_path: dict[str, Any] = field(default_factory=dict)
    denied_action_path: dict[str, Any] = field(default_factory=dict)
    architecture_coverage_ok: bool = False
    substrate_files_unchanged: bool = True


def find_repo(workspace: Path, logical: str) -> Path | None:
    for name in REPO_ALIASES.get(logical, [logical]):
        candidate = workspace / name
        if candidate.is_dir():
            return candidate
    return None


def resolve_workspace(workspace: Path) -> WorkspaceRepos:
    workspace = workspace.resolve()
    missing = [k for k in REPO_ALIASES if find_repo(workspace, k) is None]
    if missing:
        raise FileNotFoundError(f"missing workspace repos: {', '.join(missing)}")
    return WorkspaceRepos(
        workspace=workspace,
        substrate=find_repo(workspace, "substrate") or workspace,
        orchestrator=find_repo(workspace, "orchestrator") or workspace,
        lake=find_repo(workspace, "lake") or workspace,
        lkr=find_repo(workspace, "lkr") or workspace,
        skills=find_repo(workspace, "skills") or workspace,
    )


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _substrate_snapshot(substrate: Path) -> dict[str, str]:
    watch = [
        "registry/schema-registry.json",
        "registry/contract-surface-registry.json",
        "registry/architecture-flow-registry.json",
        "schemas",
    ]
    out: dict[str, str] = {}
    for rel in watch:
        root = substrate / rel
        if root.is_file():
            out[rel] = hashlib.sha256(root.read_bytes()).hexdigest()
        elif root.is_dir():
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    key = str(path.relative_to(substrate)).replace("\\", "/")
                    out[key] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def _load_contract_surface_sha256(repo: Path) -> str:
    lock = _read_json(repo / "contracts.lock.json")
    return str(lock["contract_surface_lock"]["surface_sha256"])


def _verify_contract_surface_alignment(repos: WorkspaceRepos) -> tuple[str, list[str]]:
    errors: list[str] = []
    surfaces = {
        "substrate_authority": _load_contract_surface_authority(repos),
        "orchestrator": _load_contract_surface_sha256(repos.orchestrator),
        "lake": _load_contract_surface_sha256(repos.lake),
        "lkr": _load_contract_surface_sha256(repos.lkr),
        "skills": _load_contract_surface_sha256(repos.skills),
    }
    authority = surfaces["substrate_authority"]
    for name, surface in surfaces.items():
        if name == "substrate_authority":
            continue
        if surface != authority:
            errors.append(f"{name} contract surface {surface} != substrate authority {authority}")
    return authority, errors


def _load_contract_surface_authority(repos: WorkspaceRepos) -> str:
    """Return the workspace contract surface hash pinned by consumer locks.

    Substrate defines the surface via contract-surface-registry.json; runtime
    repos pin the digest in contracts.lock.json. Cross-repo smoke uses the
    pinned digest as the authority gate (validated for parity across consumers).
    """
    reg_path = repos.substrate / "registry" / "contract-surface-registry.json"
    if not reg_path.is_file():
        raise FileNotFoundError(f"missing substrate contract surface registry: {reg_path}")
    return _load_contract_surface_sha256(repos.orchestrator)


def _configure_import_paths(repos: WorkspaceRepos) -> None:
    paths = [
        repos.orchestrator / "src",
        repos.lkr / "src",
        repos.lake / "src",
        repos.skills / "src",
        SCRIPTS,
    ]
    for p in paths:
        ps = str(p)
        if ps not in sys.path:
            sys.path.insert(0, ps)


def _build_lkr_artifacts(repos: WorkspaceRepos) -> dict[str, Any]:
    from lawfirm_os_legal_knowledge.grounding import (
        emit_claim_ref,
        emit_coverage_record,
        emit_passage_ref,
        emit_source_ref,
        emit_verification_record,
        passage_refs_for_context_bundle,
        refs_for_evidence_packet,
        source_refs_for_context_bundle,
    )
    from lawfirm_os_legal_knowledge.bundle import assemble_synthetic_context_bundle, build_retrieval_trace

    manifest_path = repos.lkr / "examples" / "synthetic_legal_document_ingestion_manifest.json"
    manifest = _read_json(manifest_path)
    document = dict(manifest["documents"][0])
    span_text = "Section 2.1 — Payment terms net thirty (synthetic PR-10 smoke)."
    emitted = emit_source_ref(document, run_id=RUN_ID, retrieved_at=FIXED_AT)
    passage = emit_passage_ref(
        source_ref_id=emitted.source_ref["source_ref_id"],
        document=document,
        span_text=span_text,
        run_id=RUN_ID,
        span_type="clause",
        start_offset=0,
        end_offset=len(span_text),
        heading_path=["MSA", "Payment"],
        citation_label="Synthetic MSA §2.1",
        provider_metadata={"fixture_layer": "pr10_cross_repo_smoke"},
    )
    claim = emit_claim_ref(
        claim_text="Synthetic MSA selects New York law.",
        source_ref_ids=[emitted.source_ref["source_ref_id"]],
        run_id=RUN_ID,
        passage_ref_ids=[passage["passage_ref_id"]],
    )
    verification = emit_verification_record(
        claim_ref_id=claim["claim_ref_id"],
        run_id=RUN_ID,
        verified_by_kind="tool",
        verified_by_id="synthetic-verifier-pr10",
        verdict="verified",
        confidence=1.0,
        verified_at=FIXED_AT,
        passage_ref_ids=[passage["passage_ref_id"]],
    )
    coverage = emit_coverage_record(
        source_ref_id=emitted.source_ref["source_ref_id"],
        run_id=RUN_ID,
        units_requested=10,
        units_read=10,
        passage_ref_id=passage["passage_ref_id"],
    )
    trace = build_retrieval_trace(
        manifest,
        run_id=RUN_ID,
        retrieval_plan_id="plan-pr10-smoke",
        retrievers_used=["metadata"],
        source_refs=[emitted.source_ref],
        passage_refs=[passage],
    )
    lkr_bundle = assemble_synthetic_context_bundle(
        manifest,
        bundle_type="contract_review_context.v1",
        run_id=RUN_ID,
        retrieval_trace_id=trace["retrieval_trace_id"],
        source_refs=source_refs_for_context_bundle([emitted.source_ref]),
        claim_refs=[claim],
        passage_refs=passage_refs_for_context_bundle([passage]),
    )
    return {
        "manifest": manifest,
        "source_ref": emitted.source_ref,
        "passage_ref": passage,
        "claim_ref": claim,
        "verification_record": verification,
        "coverage_record": coverage,
        "retrieval_trace": trace,
        "lkr_context_bundle": lkr_bundle,
        "packet_source_refs": refs_for_evidence_packet([emitted.source_ref], "source_ref_id"),
        "packet_claim_refs": refs_for_evidence_packet([claim], "claim_ref_id"),
        "packet_coverage_refs": refs_for_evidence_packet([coverage], "coverage_record_id"),
        "packet_verification_refs": refs_for_evidence_packet([verification], "verification_record_id"),
    }


def _build_skill_trust_record(repos: WorkspaceRepos, *, contract_surface_sha256: str, tmp_root: Path) -> dict[str, Any]:
    from lawfirm_os_skills_registry.domain.skill_trust_record import emit_skill_trust_record

    skill_dir = tmp_root / "skills" / "pr10-smoke-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: pr10-smoke-skill\ndescription: Synthetic PR-10 cross-repo smoke skill.\n---\n"
        "Emit governed JSON only; no canonical legal claims.\n",
        encoding="utf-8",
    )
    meta = {
        "id": "pr10-smoke-skill",
        "kind": "skill",
        "name": "pr10-smoke-skill",
        "version": "0.1.0",
        "lifecycle_state": "draft",
        "source_origin": "synthetic_fixture",
        "source_uri_hash": "c" * 64,
        "trust_surface": {
            "declared_tools": ["read_file"],
            "declared_hooks": [],
            "declared_write_paths": [],
            "declared_urls": [],
        },
        "provider_metadata": {
            "claude": {"plugin_id": "claude-plugin-pr10-smoke", "workflow_id": "wf-pr10-smoke"},
        },
    }
    (skill_dir / "SKILL_METADATA.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    record = emit_skill_trust_record(
        skill_dir,
        qa_verdict="passed",
        approval_required=False,
        freshness_status="fresh",
        contract_surface_sha256=contract_surface_sha256,
    )
    if record.get("contract_surface_sha256") != contract_surface_sha256:
        raise ValueError("SkillTrustRecord contract surface mismatch")
    if "route_id" in json.dumps(record):
        raise ValueError("SkillTrustRecord must not carry route_id authority")
    if record.get("provider_metadata"):
        raise ValueError("provider_metadata must not appear on SkillTrustRecord canon fields")
    claude = meta.get("provider_metadata", {}).get("claude", {})
    assert claude.get("plugin_id") == "claude-plugin-pr10-smoke"
    return record


def _compile_orchestrator_context_bundle(repos: WorkspaceRepos, *, lkr: dict[str, Any]):
    from lawfirm_os_orchestrator.context.compiler import compile_context_bundle
    from lawfirm_os_orchestrator.domain.context_bundle import (
        ContextBudget,
        ContextBundleTask,
        PolicyRefStub,
        SourceRefStub,
        ToolRefStub,
    )

    src = lkr["source_ref"]
    stubs = [
        SourceRefStub(
            source_ref_id=str(src["source_ref_id"]),
            source_id=str(src["source_id"]),
            content_hash=str(src["content_hash"]),
        )
    ]
    return compile_context_bundle(
        context_bundle_id="ctx-pr10-smoke",
        run_id=RUN_ID,
        task=ContextBundleTask(
            task_id="task-pr10-smoke",
            task_kind="cross_repo_os_smoke",
            task_description_hash=hashlib.sha256(b"pr10-cross-repo-smoke").hexdigest(),
        ),
        source_refs=stubs,
        policy_refs=[PolicyRefStub(policy_ref_id="pref-pr10", policy_id="policy.synthetic-only.v1")],
        tool_refs=[ToolRefStub(tool_ref_id="tref-pr10-skill", tool_id="pr10-smoke-skill")],
        context_budget=ContextBudget(max_input_bytes=65536, max_steps=8),
        contract_lock_path=repos.orchestrator / "contracts.lock.json",
        generated_at=FIXED_AT,
    )


def _authority_config():
    from lawfirm_os_orchestrator.authority.execution_authority import AuthorityConfig

    return AuthorityConfig(
        allowed_tool_ids=SMOKE_CONFIG["allowed_tool_ids"],
        allowed_route_ids=SMOKE_CONFIG["allowed_route_ids"],
        allowed_event_classes=SMOKE_CONFIG["allowed_event_classes"],
        write_actions_with_approval=SMOKE_CONFIG["write_actions_with_approval"],
    )


def _build_request(bundle, *, action: str, tool_id: str, route_id: str, event_class: str, side_effect: str):
    from lawfirm_os_orchestrator.domain.execution_request import build_execution_request

    return build_execution_request(
        execution_request_id=f"req-pr10-{action}",
        context_bundle_hash=bundle.context_bundle_hash,
        contract_surface_sha256=bundle.contract_surface_sha256,
        run_id=bundle.run_id,
        requested_at=FIXED_AT,
        requested_action=action,
        requested_tool_id=tool_id,
        requested_route_id=route_id,
        requested_event_class=event_class,
        requested_side_effect_class=side_effect,
        request_payload_hash=hashlib.sha256(action.encode()).hexdigest(),
    )


def _authority_record(
    *,
    request,
    decision,
    passport=None,
    result=None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "execution_request_hash": request.execution_request_hash,
        "execution_decision_hash": decision.execution_decision_hash,
    }
    if passport is not None:
        rec["execution_passport_hash"] = passport.execution_passport_hash
    if result is not None:
        rec["execution_result_hash"] = result.execution_result_hash
        rec["status"] = result.status
    if extra:
        rec.update(extra)
    return rec


def _build_valid_evidence_packet(
    repos: WorkspaceRepos,
    *,
    bundle,
    lkr: dict[str, Any],
    request,
    decision,
    passport,
    result,
    tmp_packet_dir: Path,
) -> dict[str, Any]:
    from lawfirm_os_orchestrator.evidence.packet_v2 import (
        build_evidence_packet_v2,
        evidence_packet_hash,
        manifest_hash_for_dir,
        write_evidence_packet_v2,
    )

    (tmp_packet_dir / "synthetic_action_summary.json").write_text(
        json.dumps({"action": "read_synthetic", "outcome": "mock_ok", "raw_payload_included": False}) + "\n",
        encoding="utf-8",
    )
    manifest_hash, _ = manifest_hash_for_dir(tmp_packet_dir)
    authority = _authority_record(
        request=request,
        decision=decision,
        passport=passport,
        result=result,
    )
    packet = build_evidence_packet_v2(
        evidence_packet_id="ep-pr10-valid",
        contract_surface_sha256=bundle.contract_surface_sha256,
        context_bundle_id=bundle.context_bundle_id,
        context_bundle_hash=bundle.context_bundle_hash,
        execution_authority_records=[authority],
        source_refs=lkr["packet_source_refs"],
        claim_refs=lkr["packet_claim_refs"],
        coverage_records=lkr["packet_coverage_refs"],
        verification_records=lkr["packet_verification_refs"],
        approval_records=[],
        defect_records=[],
        manifest_hash=manifest_hash,
        generated_at=FIXED_AT,
        run_id=RUN_ID,
    )
    write_evidence_packet_v2(tmp_packet_dir, packet)
    assert evidence_packet_hash(packet) == packet["evidence_packet_hash"]
    return packet


def _run_valid_path(
    repos: WorkspaceRepos,
    *,
    lkr: dict[str, Any],
    bundle,
    lake_storage: Path,
) -> dict[str, Any]:
    from lawfirm_os_orchestrator.commands.preflight_execution import preflight
    from lawfirm_os_orchestrator.domain.execution_result import build_execution_result
    from exceptions_lake_runtime.validators.admission_validator import (
        CentralAdmissionConfig,
        admit_packet,
    )
    from exceptions_lake_runtime.substrate import reason_codes as rc

    config = _authority_config()
    request = _build_request(
        bundle,
        action="read_synthetic",
        tool_id="synthetic.read_only",
        route_id="route.synthetic_read",
        event_class="synthetic.read",
        side_effect="read",
    )
    pre = preflight(context_bundle=bundle, request=request, config=config)
    assert pre.passport is not None
    result = build_execution_result(
        execution_result_id="res-pr10-valid",
        execution_request_hash=request.execution_request_hash,
        execution_decision_hash=pre.decision.execution_decision_hash,
        context_bundle_hash=bundle.context_bundle_hash,
        contract_surface_sha256=bundle.contract_surface_sha256,
        run_id=RUN_ID,
        started_at=FIXED_AT,
        ended_at=FIXED_AT,
        status="succeeded",
        execution_passport_hash=pre.passport.execution_passport_hash,
        result_payload_hash=hashlib.sha256(b"mock-result-pr10").hexdigest(),
    )
    with tempfile.TemporaryDirectory() as tmp:
        packet_dir = Path(tmp)
        packet = _build_valid_evidence_packet(
            repos,
            bundle=bundle,
            lkr=lkr,
            request=request,
            decision=pre.decision,
            passport=pre.passport,
            result=result,
            tmp_packet_dir=packet_dir,
        )
        _assert_no_raw_privileged_payloads(packet, lkr)
        admission = admit_packet(
            packet,
            config=CentralAdmissionConfig(
                expected_contract_surface_sha256=bundle.contract_surface_sha256,
                storage_root=lake_storage / "valid",
            ),
            admitted_at=FIXED_AT,
        )
    assert admission.admission_record["admission_status"] == "admitted"
    assert admission.admission_record["admission_reason_code"] == rc.PASSED_DRY_RUN_ADMISSION
    assert admission.defects == []
    assert admission.execution_record is not None
    return {
        "context_bundle_hash": bundle.context_bundle_hash,
        "evidence_packet_hash": packet["evidence_packet_hash"],
        "admission_status": admission.admission_record["admission_status"],
        "passage_ref_id": lkr["passage_ref"]["passage_ref_id"],
        "claim_ref_id": lkr["claim_ref"]["claim_ref_id"],
    }


def _run_missing_passport_path(repos: WorkspaceRepos, *, bundle, lake_storage: Path) -> dict[str, Any]:
    from lawfirm_os_orchestrator.evidence.packet_v2 import build_evidence_packet_v2, evidence_packet_hash
    from exceptions_lake_runtime.validators.admission_validator import CentralAdmissionConfig, admit_packet
    from exceptions_lake_runtime.substrate import reason_codes as rc

    packet = build_evidence_packet_v2(
        evidence_packet_id="ep-pr10-missing-passport",
        contract_surface_sha256=bundle.contract_surface_sha256,
        context_bundle_id=bundle.context_bundle_id,
        context_bundle_hash=bundle.context_bundle_hash,
        execution_authority_records=[
            {
                "execution_request_hash": "1" * 64,
                "execution_decision_hash": "2" * 64,
                "execution_result_hash": "3" * 64,
                "status": "succeeded",
            }
        ],
        source_refs=[],
        claim_refs=[],
        coverage_records=[],
        verification_records=[],
        approval_records=[],
        defect_records=[],
        manifest_hash="4" * 64,
        generated_at=FIXED_AT,
        run_id=RUN_ID,
    )
    assert evidence_packet_hash(packet) == packet["evidence_packet_hash"]
    outcome = admit_packet(
        packet,
        config=CentralAdmissionConfig(
            expected_contract_surface_sha256=bundle.contract_surface_sha256,
            storage_root=lake_storage / "missing_passport",
        ),
        admitted_at=FIXED_AT,
    )
    assert outcome.admission_record["admission_status"] == "admitted"
    assert any(d["defect_class"] == rc.MISSING_PASSPORT for d in outcome.defects)
    assert outcome.eval_candidates
    return {
        "admission_status": outcome.admission_record["admission_status"],
        "defect_classes": [d["defect_class"] for d in outcome.defects],
        "eval_candidate_count": len(outcome.eval_candidates),
    }


def _run_denied_action_path(repos: WorkspaceRepos, *, bundle, lake_storage: Path) -> dict[str, Any]:
    from lawfirm_os_orchestrator.authority.execution_authority import evaluate
    from lawfirm_os_orchestrator.evidence.packet_v2 import build_evidence_packet_v2, evidence_packet_hash
    from exceptions_lake_runtime.validators.admission_validator import CentralAdmissionConfig, admit_packet

    request = _build_request(
        bundle,
        action="external_write",
        tool_id="synthetic.read_only",
        route_id="route.synthetic_read",
        event_class="synthetic.external",
        side_effect="external",
    )
    decision = evaluate(request, config=_authority_config())
    assert decision.decision == "denied"
    denied_record = {
        "execution_request_hash": request.execution_request_hash,
        "execution_decision_hash": decision.execution_decision_hash,
        "decision": "denied",
        "denial_explanation_hash": decision.denial_explanation_hash or ("d" * 64),
    }
    packet = build_evidence_packet_v2(
        evidence_packet_id="ep-pr10-denied",
        contract_surface_sha256=bundle.contract_surface_sha256,
        context_bundle_id=bundle.context_bundle_id,
        context_bundle_hash=bundle.context_bundle_hash,
        execution_authority_records=[denied_record],
        manifest_hash="e" * 64,
        generated_at=FIXED_AT,
        run_id=RUN_ID,
    )
    assert evidence_packet_hash(packet) == packet["evidence_packet_hash"]
    outcome = admit_packet(
        packet,
        config=CentralAdmissionConfig(
            expected_contract_surface_sha256=bundle.contract_surface_sha256,
            storage_root=lake_storage / "denied",
        ),
        admitted_at=FIXED_AT,
    )
    assert outcome.admission_record["admission_status"] == "admitted"
    assert outcome.execution_record is not None
    assert outcome.execution_record.get("denied_action_evidence") == [denied_record]
    assert any(d.get("defect_class") == "denied_action_recorded" for d in outcome.defects)
    assert outcome.eval_candidates
    return {
        "decision": decision.decision,
        "admission_status": outcome.admission_record["admission_status"],
        "denied_action_preserved": bool(outcome.execution_record.get("denied_action_evidence")),
        "denied_action_defect_minted": True,
        "eval_candidate_count": len(outcome.eval_candidates),
    }


def _assert_no_raw_privileged_payloads(packet: dict[str, Any], lkr: dict[str, Any]) -> None:
    blob = json.dumps(packet)
    forbidden = [
        "Synthetic MSA selects New York law.",
        "Section 2.1 — Payment terms net thirty",
        "client_matter",
    ]
    for token in forbidden:
        if token in blob:
            raise ValueError(f"evidence packet must not embed raw privileged text: found {token!r}")
    assert all("claim_text" not in ref for ref in packet.get("claim_refs", []))
    lkr_bundle = lkr["lkr_context_bundle"]
    assert lkr_bundle["passage_refs"][0]["passage_ref_id"] == lkr["passage_ref"]["passage_ref_id"]
    assert lkr_bundle["claim_refs"][0]["claim_ref_id"] == lkr["claim_ref"]["claim_ref_id"]
    assert lkr_bundle["source_refs"][0]["source_ref_id"] == lkr["source_ref"]["source_ref_id"]


def _run_architecture_gate(workspace: Path, substrate: Path) -> bool:
    from validate_architecture_object_coverage import validate

    result = validate(workspace, substrate=substrate, include_workspace_validators=False)
    return result.ok


def run_smoke(workspace: Path) -> SmokeResult:
    result = SmokeResult(ok=False, contract_surface_sha256="")
    substrate_before = _substrate_snapshot(REPO_ROOT)

    try:
        repos = resolve_workspace(workspace)
    except FileNotFoundError as exc:
        result.errors.append(str(exc))
        return result

    _configure_import_paths(repos)
    surface, surface_errors = _verify_contract_surface_alignment(repos)
    result.contract_surface_sha256 = surface
    result.errors.extend(surface_errors)
    if surface_errors:
        return result

    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        lake_storage = tmp_root / "lake"
        lkr = _build_lkr_artifacts(repos)
        skill_trust = _build_skill_trust_record(repos, contract_surface_sha256=surface, tmp_root=tmp_root)
        bundle = _compile_orchestrator_context_bundle(repos, lkr=lkr)

        if bundle.contract_surface_sha256 != surface:
            result.errors.append("orchestrator context bundle surface != workspace authority")

        try:
            result.valid_path = _run_valid_path(repos, lkr=lkr, bundle=bundle, lake_storage=lake_storage)
            result.missing_passport_path = _run_missing_passport_path(
                repos, bundle=bundle, lake_storage=lake_storage
            )
            result.denied_action_path = _run_denied_action_path(
                repos, bundle=bundle, lake_storage=lake_storage
            )
            result.architecture_coverage_ok = _run_architecture_gate(workspace, repos.substrate)
            if not result.architecture_coverage_ok:
                result.errors.append("architecture object coverage gate failed")
            result.valid_path["skill_trust_record_id"] = skill_trust["skill_trust_record_id"]
        except Exception as exc:  # noqa: BLE001 — smoke aggregates failures
            result.errors.append(f"smoke flow failed: {exc}")

    substrate_after = _substrate_snapshot(REPO_ROOT)
    result.substrate_files_unchanged = substrate_before == substrate_after
    if not result.substrate_files_unchanged:
        result.errors.append("runtime smoke mutated Semantic Substrate tracked files")

    result.ok = (
        not result.errors
        and bool(result.valid_path)
        and bool(result.missing_passport_path)
        and bool(result.denied_action_path)
        and result.architecture_coverage_ok
        and result.substrate_files_unchanged
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="PR-10 cross-repo OS smoke test")
    parser.add_argument("--workspace", default="..", help="Workspace root containing all five repos")
    parser.add_argument("--json-out", default=None, help="Optional path to write JSON summary")
    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    outcome = run_smoke(workspace)
    summary = {
        "ok": outcome.ok,
        "contract_surface_sha256": outcome.contract_surface_sha256,
        "errors": outcome.errors,
        "valid_path": outcome.valid_path,
        "missing_passport_path": outcome.missing_passport_path,
        "denied_action_path": outcome.denied_action_path,
        "architecture_coverage_ok": outcome.architecture_coverage_ok,
        "substrate_files_unchanged": outcome.substrate_files_unchanged,
    }
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if outcome.ok:
        print("cross-repo OS smoke test passed.")
        return 0
    print(f"cross-repo OS smoke test failed ({len(outcome.errors)} error(s)).")
    for err in outcome.errors:
        print(f"ERROR: {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
