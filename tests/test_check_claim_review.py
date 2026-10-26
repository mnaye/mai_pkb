import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_claim_review


class ClaimReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = json.loads(check_claim_review.FIXTURES.read_text(encoding="utf-8"))

    def make_report(self):
        return {
            "week": "2026-W44",
            "reviews": [{"area": "healthcare", "findings": []}],
            "fixture_results": [
                {
                    "id": fixture["id"],
                    "flagged": fixture["expected_flag"],
                    "category": fixture["expected_category"],
                    "evidence_excerpt": fixture["evidence"],
                }
                for fixture in self.fixtures
            ],
        }

    def test_planted_errors_flag_and_supported_control_passes(self):
        report = self.make_report()
        errors = check_claim_review.validate(report, self.fixtures)
        self.assertEqual(errors, [])
        results = {result["id"]: result for result in report["fixture_results"]}
        self.assertTrue(all(results[fixture["id"]]["flagged"] for fixture in self.fixtures[:4]))
        self.assertFalse(results["supported-control"]["flagged"])

    def test_missing_fixture_result_fails(self):
        report = self.make_report()
        report["fixture_results"].pop()
        self.assertTrue(any("missing fixture results" in error
                            for error in check_claim_review.validate(report, self.fixtures)))

    def test_wrong_expected_category_fails(self):
        report = self.make_report()
        report["fixture_results"][0]["category"] = "timing"
        self.assertTrue(any("expected category" in error
                            for error in check_claim_review.validate(report, self.fixtures)))

    def test_draft_quote_must_match_saved_evidence(self):
        report = self.make_report()
        report["reviews"][0]["findings"] = [{
            "sentence": "This statement is unsupported.",
            "category": "evidence_support",
            "assessment": "unsupported",
            "severity": "medium",
            "reason": "No supplied passage supports it.",
            "evidence_excerpt": "Invented passage.",
            "source_url": "https://example.org/source",
            "suggested_correction": "Remove or qualify the statement.",
        }]
        errors = check_claim_review.validate(
            report, self.fixtures,
            {"healthcare": [{"url": "https://example.org/source",
                              "excerpts": ["Exact saved passage."]}]},
        )
        self.assertTrue(any("does not match saved source evidence" in error for error in errors))

    def test_matching_saved_passage_and_source_is_accepted(self):
        report = self.make_report()
        report["reviews"][0]["findings"] = [{
            "sentence": "This statement is unsupported.",
            "category": "evidence_support",
            "assessment": "unsupported",
            "severity": "medium",
            "reason": "The passage does not support the sentence.",
            "evidence_excerpt": "Exact saved passage.",
            "source_url": "https://example.org/source",
            "suggested_correction": "Remove or qualify the statement.",
        }]
        errors = check_claim_review.validate(
            report, self.fixtures,
            {"healthcare": [{"url": "https://example.org/source",
                              "excerpts": ["Exact saved passage."]}]},
        )
        self.assertEqual(errors, [])

    def test_non_string_finding_field_fails_cleanly(self):
        report = self.make_report()
        report["reviews"][0]["findings"] = [{
            "sentence": ["not", "text"],
            "category": "evidence_support",
            "assessment": "unsupported",
            "severity": "medium",
            "reason": "A reason.",
            "evidence_excerpt": "",
            "source_url": "",
            "suggested_correction": "Remove it.",
        }]
        errors = check_claim_review.validate(report, self.fixtures)
        self.assertTrue(any("finding fields must use strings" in error for error in errors))


if __name__ == "__main__":
    unittest.main()