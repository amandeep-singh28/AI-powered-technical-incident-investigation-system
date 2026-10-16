import json
import tempfile
import unittest

from pathlib import Path
from src.incident_loader import load_incident


class TestIncidentLoader(unittest.TestCase):

    def setUp(self):
        self.valid_incident = {
            "incident_id": "INC-001",
            "title": "Website Checkout Failure",
            "severity": "high",
            "status": "investigating",
            "reported_at": "2026-10-15T10:05:00",
            "description": "Checkout requests are failing."
        }

    def test_valid_incident_loads(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "incident.json"
            path.write_text(
                json.dumps(self.valid_incident),
                encoding="utf-8"
            )

            result = load_incident(str(path))

            self.assertEqual(result["incident_id"], "INC-001")

    def test_invalid_severity_is_rejected(self):
        self.valid_incident["severity"] = "super-high"

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "incident.json"
            path.write_text(
                json.dumps(self.valid_incident),
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                load_incident(str(path))

    def test_invalid_timestamp_is_rejected(self):
        self.valid_incident["reported_at"] = "not-a-date"

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "incident.json"
            path.write_text(
                json.dumps(self.valid_incident),
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                load_incident(str(path))


if __name__ == "__main__":
    unittest.main()
