
import unittest
from pydantic import ValidationError

from src.investigation_schema import (
    EvidenceFinding,
    InvestigationReport,
)


class TestInvestigationSchema(unittest.TestCase):

    def setUp(self):
        self.valid_report = {
            "incident_id": "INC-001",
            "incident_summary": "Checkout requests are failing.",
            "verified_facts": [
                EvidenceFinding(
                    finding="Database connection failed.",
                    source="Evidence/data/logs/INC-001.log",
                ).model_dump()
            ],
            "possible_causes": [
                "A database connectivity issue"
            ],
            "recommended_checks": [
                "Check database connectivity and credentials."
            ],
            "unknowns": [
                "Whether the deployment caused the failure"
            ],
        }

    def test_valid_report_is_accepted(self):
        report = InvestigationReport(**self.valid_report)

        self.assertEqual(report.incident_id, "INC-001")
        self.assertEqual(len(report.verified_facts), 1)
        self.assertIsInstance(
            report.verified_facts[0], EvidenceFinding
        )

    def test_missing_required_field_is_rejected(self):
        invalid_data = self.valid_report.copy()
        del invalid_data["incident_id"]

        with self.assertRaises(ValidationError):
            InvestigationReport(**invalid_data)

    def test_invalid_list_type_is_rejected(self):
        invalid_data = self.valid_report.copy()
        invalid_data["verified_facts"] = "No verified facts"

        with self.assertRaises(ValidationError):
            InvestigationReport(**invalid_data)


if __name__ == "__main__":
    unittest.main()
