
import unittest
from datetime import datetime

from src.log_parser import parse_log_line, analyze_logs


class TestLogParser(unittest.TestCase):

    def test_valid_log_line(self):
        line = (
            "2026-10-15T10:03:02 ERROR "
            "checkout-api Database connection failed"
        )

        event = parse_log_line(line)

        self.assertEqual(event["level"], "ERROR")
        self.assertEqual(event["service"], "checkout-api")
        self.assertEqual(
            event["message"], "Database connection failed"
        )
        self.assertEqual(
            event["timestamp"],
            datetime(2026, 10, 15, 10, 3, 2)
        )

    def test_malformed_log_line(self):
        with self.assertRaises(ValueError):
            parse_log_line("This is not a valid log line")

    def test_analyze_logs(self):
        events = [
            {
                "timestamp": datetime(2026, 10, 15, 10, 3, 2),
                "level": "ERROR",
                "service": "checkout-api",
                "message": "Database connection failed",
            },
            {
                "timestamp": datetime(2026, 10, 15, 10, 0, 0),
                "level": "INFO",
                "service": "checkout-api",
                "message": "Application started",
            },
        ]

        report = analyze_logs(events)

        self.assertEqual(report["total_events"], 2)
        self.assertEqual(report["error_count"], 1)
        self.assertEqual(
            report["first_event"]["level"], "INFO"
        )
        self.assertEqual(
            report["first_error"]["level"], "ERROR"
        )


if __name__ == "__main__":
    unittest.main()
