#!/usr/bin/env python3
"""Validate and render the report-only adversarial review output."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures" / "claim-review-cases.json"
CATEGORIES = {"evidence_support", "attribution", "policy_status", "implications", "timing"}
SEVERITIES = {"high", "medium", "low"}
FINDING_FIELDS = {
    "sentence", "category", "assessment", "severity", "reason",
    "evidence_excerpt", "source_url", "suggested_correction",
}


def load_json(path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def validate(report, fixtures, evidence_by_area=None, expected_areas=None):
    errors = []
    evidence_by_area = evidence_by_area or {}
    if not isinstance(report, dict) or not isinstance(report.get("week"), str):
        return ["report must be an object with a week string"]
    reviews = report.get("reviews")
    results = report.get("fixture_results")
    if not isinstance(reviews, list) or not isinstance(results, list):
        return ["report must contain reviews and fixture_results arrays"]

    review_areas = set()
    for review in reviews:
        if not isinstance(review, dict) or not isinstance(review.get("area"), str):
            errors.append("each review must have an area string")
            continue
        area = review["area"]
        review_areas.add(area)
        evidence = evidence_by_area.get(area, [])
        excerpt_sources = {
            excerpt: source.get("url", "")
            for source in evidence
            if isinstance(source, dict)
            for excerpt in source.get("excerpts", [])
            if isinstance(excerpt, str)
        }
        findings = review.get("findings")
        if not isinstance(findings, list):
            errors.append("%s: findings must be an array" % review["area"])
            continue
        for finding in findings:
            if not isinstance(finding, dict) or FINDING_FIELDS - finding.keys():
                errors.append("%s: finding is missing required fields" % review["area"])
                continue
            string_fields = FINDING_FIELDS - {"category", "severity"}
            if any(not isinstance(finding[field], str) for field in string_fields):
                errors.append("%s: finding fields must use strings" % area)
                continue
            if not isinstance(finding["category"], str) or not isinstance(finding["severity"], str):
                errors.append("%s: category and severity must use strings" % area)
                continue
            if finding["category"] not in CATEGORIES:
                errors.append("%s: unknown finding category" % review["area"])
            if finding["severity"] not in SEVERITIES:
                errors.append("%s: unknown finding severity" % review["area"])
            if finding["assessment"] not in {"unsupported", "insufficient evidence"}:
                errors.append("%s: unknown finding assessment" % area)
            if not finding["sentence"].strip() or not finding["reason"].strip():
                errors.append("%s: finding needs an exact sentence and reason" % review["area"])
            if not finding["evidence_excerpt"].strip():
                if finding["assessment"] != "insufficient evidence":
                    errors.append("%s: empty evidence must be assessed as insufficient evidence" % review["area"])
            else:
                excerpt = finding["evidence_excerpt"]
                if excerpt not in excerpt_sources:
                    errors.append("%s: evidence excerpt does not match saved source evidence" % area)
                elif finding["source_url"] != excerpt_sources[excerpt]:
                    errors.append("%s: source URL does not match the cited evidence" % area)

    if expected_areas is not None:
        missing_areas = expected_areas - review_areas
        if missing_areas:
            errors.append("missing review entries: %s" % ", ".join(sorted(missing_areas)))

    expected = {fixture["id"]: fixture for fixture in fixtures}
    observed = {}
    for result in results:
        if not isinstance(result, dict) or not isinstance(result.get("id"), str):
            errors.append("each fixture result must have an id")
            continue
        if result["id"] in observed:
            errors.append("duplicate fixture result: %s" % result["id"])
        observed[result["id"]] = result
    if observed.keys() != expected.keys():
        missing = sorted(expected.keys() - observed.keys())
        extra = sorted(observed.keys() - expected.keys())
        if missing:
            errors.append("missing fixture results: %s" % ", ".join(missing))
        if extra:
            errors.append("unknown fixture results: %s" % ", ".join(extra))
    for fixture_id in expected.keys() & observed.keys():
        fixture = expected[fixture_id]
        result = observed[fixture_id]
        if result.get("flagged") is not fixture["expected_flag"]:
            errors.append("%s: expected flagged=%s" % (fixture_id, fixture["expected_flag"]))
        if result.get("category") != fixture["expected_category"]:
            errors.append("%s: expected category=%s" % (fixture_id, fixture["expected_category"]))
        excerpt = result.get("evidence_excerpt", "")
        if not isinstance(excerpt, str) or excerpt != fixture["evidence"]:
            errors.append("%s: must cite the exact fixture evidence passage" % fixture_id)
    return errors


def markdown(report, errors):
    if not isinstance(report, dict):
        return "### Claim challenger (report-only)\n\nInvalid report structure.\n"
    reviews = report.get("reviews", [])
    if not isinstance(reviews, list):
        reviews = []
    findings = []
    for review in reviews:
        if not isinstance(review, dict) or not isinstance(review.get("findings"), list):
            continue
        for finding in review["findings"]:
            if isinstance(finding, dict) and FINDING_FIELDS <= finding.keys():
                findings.append((review.get("area", "?"), finding))
    lines = ["### Claim challenger (report-only)", ""]
    if findings:
        lines += ["| Area | Severity | Category | Statement | Reason | Evidence | Suggested correction |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
        for area, finding in findings:
            values = [area, finding["severity"], finding["category"], finding["sentence"],
                      finding["reason"], finding["evidence_excerpt"] or "Insufficient evidence",
                      finding["suggested_correction"]]
            lines.append("| " + " | ".join(str(value).replace("|", "/").replace("\n", " ") for value in values) + " |")
    else:
        lines.append("No So what findings.")
    fixture_results = report.get("fixture_results", [])
    fixture_results = fixture_results if isinstance(fixture_results, list) else []
    lines += ["", "**Fixture results:** %d/%d expected outcomes recorded." %
              (len(fixture_results), len(load_json(FIXTURES)))]
    if errors:
        lines += ["", "**Report validation issues:**"]
        lines += ["- " + error for error in errors]
    lines += ["", "Findings are advisory; this review does not block publication."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--evidence-dir", type=Path)
    parser.add_argument("--annotate", action="store_true")
    args = parser.parse_args()
    try:
        report = load_json(args.report)
        fixtures = load_json(FIXTURES)
    except (OSError, json.JSONDecodeError) as exc:
        print("Claim review report could not be read: %s" % exc)
        return 1
    if not isinstance(report, dict):
        errors = ["report must be a JSON object"]
        evidence_by_area = {}
        expected_areas = set()
    else:
        errors = []
        evidence_dir = args.evidence_dir or args.report.parent
        evidence_by_area = {}
        expected_areas = set()
        week = report.get("week", "")
        if not isinstance(week, str):
            week = ""
        for area in ("ai-engineering", "healthcare"):
            draft = ROOT / area / (week + ".md")
            if draft.exists():
                expected_areas.add(area)
                evidence_path = evidence_dir / (area + "-evidence.json")
                if evidence_path.exists():
                    try:
                        evidence_doc = load_json(evidence_path)
                        if not isinstance(evidence_doc, dict) or not isinstance(evidence_doc.get("sources"), list):
                            errors.append("%s: evidence file must contain a sources array" % area)
                            evidence_by_area[area] = []
                        else:
                            evidence_by_area[area] = evidence_doc["sources"]
                            for source in evidence_by_area[area]:
                                if not isinstance(source, dict) or not isinstance(source.get("excerpts"), list):
                                    errors.append("%s: each evidence source needs an excerpts array" % area)
                                    continue
                                for excerpt in source["excerpts"]:
                                    if not isinstance(excerpt, str) or len(excerpt.split()) > 25:
                                        errors.append("%s: evidence excerpts must be text of 25 words or fewer" % area)
                    except (OSError, json.JSONDecodeError, AttributeError):
                        errors.append("%s: evidence file is invalid JSON" % area)
                        break
                else:
                    errors.append("%s: saved evidence file is missing" % area)
                    evidence_by_area[area] = []
    if isinstance(report, dict):
        errors += validate(report, fixtures, evidence_by_area, expected_areas)
    sys.stdout.write(markdown(report, errors))
    if args.annotate:
        for error in errors:
            print("::warning title=Claim review report::%s" % error, file=sys.stderr)
        for review in (report.get("reviews", []) if isinstance(report, dict) else []):
            if not isinstance(review, dict) or not isinstance(review.get("findings"), list):
                continue
            for finding in review.get("findings", []):
                if isinstance(finding, dict) and finding.get("severity") == "high":
                    print("::warning title=High-severity claim review::%s: %s" %
                          (review.get("area", "?"), finding.get("sentence", "")), file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())