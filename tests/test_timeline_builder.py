
import unittest
import tempfile

from pathlib import Path
from src.timeline_builder import build_timeline


class TestTimelineBuilder(unittest.TestCase):

    def test_combines_and_sorts_multiple_log_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            app_log = temp_path / "app.log"
            deployment_log = temp_path / "deployment.log"

            app_log.write_text(
                "2026-10-15T10:03:02 ERROR checkout-api "
                "Database connection failed\n",
                encoding="utf-8",
            )

            deployment_log.write_text(
                "2026-10-15T10:02:00 INFO deployment-service "
                "Deployment started\n",
                encoding="utf-8",
            )

            timeline = build_timeline(
                str(app_log),
                str(deployment_log),
            )

            self.assertEqual(len(timeline), 2)
            self.assertEqual(
                timeline[0]["service"], "deployment-service"
            )
            self.assertEqual(
                timeline[1]["level"], "ERROR"
            )

    def test_empty_log_files_produce_empty_timeline(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_log = Path(temp_dir) / "empty.log"
            empty_log.write_text("", encoding="utf-8")

            timeline = build_timeline(str(empty_log))

            self.assertEqual(timeline, [])


if __name__ == "__main__":
    unittest.main()
