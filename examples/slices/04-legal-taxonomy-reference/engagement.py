"""Validate and query a synthetic engagement candidate bundle."""
from argparse import ArgumentParser
from datetime import date, timedelta
from pathlib import Path
import json

from jsonschema import Draft202012Validator, FormatChecker

HERE = Path(__file__).resolve().parent
SCHEMA = json.loads((HERE / "engagement.schema.json").read_text(encoding="utf-8"))
SHAPE = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
IDENTIFIED = ("matters", "parties", "evidence", "engagements", "proceedings", "policies")
PROCEEDING_ROLES = {"plaintiff", "defendant", "appellant", "appellee"}
ROLE_SOURCES = {
    "counsel": {"engagement-letter", "appearance"},
    "client": {"engagement-letter", "client-confirmation"},
    "payer": {"invoice"},
    "instructing-party": {"assignment", "engagement-letter"},
    "plaintiff": {"pleading", "court-docket"},
    "defendant": {"pleading", "court-docket"},
    "appellant": {"pleading", "court-docket"},
    "appellee": {"pleading", "court-docket"},
}
COVERAGE_EVIDENCE = {"position": {"carrier-notice"}, "outcome": {"judgment", "stipulation"}}
COVERAGE_VALUES = {"position": {"reserved", "denied", "accepted"},
                   "outcome": {"owed", "not-owed", "settled"}}
LITIGATED_SERVICES = {"underlying-defense", "coverage-litigation", "appellate-advocacy"}
COVERAGE_SERVICES = {"coverage-advice", "coverage-litigation"}


def read_bundle(path):
    def unique(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique)


def lint(data):
    errors = [f"schema:{'.'.join(map(str, error.absolute_path))}:{error.message}"
              for error in SHAPE.iter_errors(data)]
    if errors:
        return sorted(errors)

    ids = {}
    for collection in IDENTIFIED:
        ids[collection] = {}
        for row in data[collection]:
            key = row["id"]
            if key in ids[collection]:
                errors.append(f"duplicate_id:{collection}:{key}")
            ids[collection][key] = row

    def lookup(collection, identity, context):
        row = ids[collection].get(identity)
        if row is None:
            errors.append(f"dangling_reference:{context}:{collection}:{identity}")
        return row

    for engagement in data["engagements"]:
        lookup("matters", engagement["matter"], engagement["id"])
    for policy in data["policies"]:
        carrier = lookup("parties", policy["carrier"], policy["id"])
        if carrier and carrier["kind"] != "insurer":
            errors.append(f"noninsurer_carrier:{policy['id']}")
    for row in data["proceedings"]:
        key = row["id"]
        lookup("matters", row["matter"], key)
        for identifier in row["engagements"]:
            engagement = lookup("engagements", identifier, key)
            if engagement and engagement["matter"] != row["matter"]:
                errors.append(f"proceeding_matter_mismatch:{key}:{identifier}")
            if engagement and engagement["service"] not in LITIGATED_SERVICES:
                errors.append(f"proceeding_service_mismatch:{key}:{identifier}")
        if "prior" in row:
            prior = lookup("proceedings", row["prior"], key)
            if prior and prior["matter"] != row["matter"]:
                errors.append(f"prior_matter_mismatch:{key}")
            seen, cursor = {key}, prior
            while cursor:
                if cursor["id"] in seen:
                    errors.append(f"proceeding_cycle:{key}")
                    break
                seen.add(cursor["id"])
                cursor = ids["proceedings"].get(cursor.get("prior"))

    def check_period(period, context, parent=None):
        end = period.get("until")
        if end and end <= period["from"]:
            errors.append(f"invalid_period:{context}")
        if parent and (period["from"] < parent["from"] or
                       parent.get("until") and (end is None or end > parent["until"])):
            errors.append(f"outside_engagement_period:{context}")

    for row in data["engagements"]:
        check_period(row["period"], row["id"])
    for collection in ("roles", "coverage", "filing"):
        for index, row in enumerate(data[collection]):
            context = f"{collection}[{index}]"
            engagement = lookup("engagements", row["engagement"], context)
            source = lookup("evidence", row["evidence"], context)
            kind = source["kind"] if source else None
            check_period(row["period"], context, engagement["period"] if engagement else None)
            end_kind = None
            if "end_evidence" in row:
                ending = lookup("evidence", row["end_evidence"], context)
                end_kind = ending["kind"] if ending else None
                if "until" not in row["period"]:
                    errors.append(f"end_evidence_without_end:{context}")
            if collection == "roles":
                party = lookup("parties", row["party"], context)
                role = row["role"]
                if role == "counsel" and party and party["kind"] != "law-firm":
                    errors.append(f"nonfirm_counsel:{context}")
                if kind is not None and kind not in ROLE_SOURCES[role]:
                    errors.append(f"unsupported_role_evidence:{context}:{role}:{kind}")
                if end_kind is not None and end_kind not in ROLE_SOURCES[role]:
                    errors.append(f"unsupported_role_end_evidence:{context}:{role}:{end_kind}")
                if ("proceeding" in row) != (role in PROCEEDING_ROLES):
                    errors.append(f"role_scope:{context}:{role}")
                if "proceeding" in row:
                    proceeding = lookup("proceedings", row["proceeding"], context)
                    if proceeding and row["engagement"] not in proceeding["engagements"]:
                        errors.append(f"role_proceeding_mismatch:{context}")
                    if proceeding:
                        allowed = {"appellant", "appellee"} if proceeding["stage"] == "appeal" else {"plaintiff", "defendant"}
                        if role not in allowed:
                            errors.append(f"role_stage_mismatch:{context}:{role}")
            elif collection == "coverage":
                policy = lookup("policies", row["policy"], context)
                lookup("parties", row["actor"], context)
                if row["kind"] == "position" and policy and row["actor"] != policy["carrier"]:
                    errors.append(f"position_actor_mismatch:{context}")
                if engagement and engagement["service"] not in COVERAGE_SERVICES:
                    errors.append(f"coverage_service_mismatch:{context}")
                if kind is not None and kind not in COVERAGE_EVIDENCE[row["kind"]]:
                    errors.append(f"unsupported_coverage_evidence:{context}:{kind}")
                if end_kind is not None and end_kind not in COVERAGE_EVIDENCE[row["kind"]]:
                    errors.append(f"unsupported_coverage_end_evidence:{context}:{end_kind}")
                if row["value"] not in COVERAGE_VALUES[row["kind"]]:
                    errors.append(f"invalid_coverage_value:{context}:{row['value']}")
            elif kind is not None:
                if row["state"] in {"filed", "not-filed"}:
                    if kind != "court-docket" or row["scope"] == "engagement":
                        errors.append(f"unsupported_filing_evidence:{context}:{kind}")
                if row["state"] == "not-filed":
                    start = date.fromisoformat(row["period"]["from"])
                    end = row["period"].get("until")
                    if (start == date.max or end != (start + timedelta(days=1)).isoformat()
                            or source["date"] < row["period"]["from"]):
                        errors.append(f"negative_filing_snapshot_required:{context}")
                if row["state"] == "inapplicable" and (kind != "engagement-letter" or
                        row["scope"] != "engagement" or
                        engagement and engagement["service"] in LITIGATED_SERVICES):
                    errors.append(f"unsupported_filing_inapplicability:{context}")
    return sorted(errors)


def active(period, as_of):
    return period["from"] <= as_of and ("until" not in period or as_of < period["until"])


def resolve(rows, field):
    values = sorted({row[field] for row in rows})
    evidence = sorted({row["evidence"] for row in rows})
    if not values:
        return {"state": "unknown", "evidence": []}
    if len(values) > 1:
        return {"state": "disputed", "candidates": values, "evidence": evidence}
    if values[0] == "inapplicable":
        return {"state": "inapplicable", "evidence": evidence}
    return {"state": "known", "value": values[0], "evidence": evidence}


class EngagementView:
    def __init__(self, data, as_of, known_by=None):
        errors = lint(data)
        if errors:
            raise ValueError("\n".join(errors))
        self.data = data
        self.as_of = date.fromisoformat(as_of).isoformat()
        cutoff = date.fromisoformat(known_by or as_of).isoformat()
        self.sources = {row["id"] for row in data["evidence"] if row["date"] <= cutoff}
        self.engagements = {row["id"]: row for row in data["engagements"] if active(row["period"], self.as_of)}

    def known_period(self, row):
        period = row["period"]
        if row.get("end_evidence") and row["end_evidence"] not in self.sources:
            return {"from": period["from"]}
        return period

    def select(self, collection, **filters):
        return [row for row in self.data[collection]
                if row["engagement"] in self.engagements and row["evidence"] in self.sources
                and active(self.known_period(row), self.as_of)
                and all(row.get(key) == value for key, value in filters.items())]

    def party_role(self, engagement, party, role, proceeding=None):
        rows = self.select("roles", engagement=engagement, party=party, role=role, proceeding=proceeding)
        grouped = resolve(rows, "state")
        if any(row["state"] == "disputed" for row in rows):
            return {"state": "disputed", "evidence": grouped["evidence"]}
        return grouped

    def represented(self, firm, client):
        return [key for key in sorted(self.engagements)
                if self.party_role(key, firm, "counsel")["state"] == "known"
                and self.party_role(key, client, "client")["state"] == "known"]

    def litigation_role(self, engagement, proceeding, party):
        rows = self.select("roles", engagement=engagement, proceeding=proceeding, party=party)
        result = resolve(rows, "role")
        if any(row["state"] == "disputed" for row in rows):
            result = {"state": "disputed", "candidates": sorted({row["role"] for row in rows}),
                      "evidence": result["evidence"]}
        return result

    def coverage(self, engagement, policy, issue, actor, kind):
        return resolve(self.select("coverage", engagement=engagement, policy=policy,
                                   issue=issue, actor=actor, kind=kind), "value")

    def filing(self, engagement, scope):
        scoped = self.select("filing", engagement=engagement, scope=scope)
        if scope != "engagement":
            scoped += self.select("filing", engagement=engagement, scope="engagement")
        return resolve(scoped, "state")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("bundle")
    args = parser.parse_args()
    try:
        problems = lint(read_bundle(args.bundle))
    except (OSError, ValueError) as error:
        problems = [str(error)]
    print(json.dumps({"valid": not problems, "findings": problems}, indent=2))
    return bool(problems)


if __name__ == "__main__":
    raise SystemExit(main())
