import json
from pathlib import Path
from datetime import datetime

def load_incident(file_path: str) -> dict:
    """Load an incident report from a JSON file."""

    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        incident = json.load(file)

    required_fields = [
        "incident_id",
        "title",
        "severity",
        "status",
        "reported_at",
        "description",
    ]

    for field in required_fields:
        if field not in incident:
            raise ValueError(f"Missing required field: {field}")

    # Validate severity
    allowed_severities = {"low", "medium", "high", "critical"}

    if incident["severity"] not in allowed_severities:
        raise ValueError("Invalid incident severity")

    # Validate timestamp format
    try:
        datetime.fromisoformat(incident["reported_at"])
    except ValueError:
        raise ValueError("Invalid reported_at timestamp")

    return incident


if __name__ == "__main__":
    incident = load_incident(
        "Evidence/data/incidents/INC-001.json"
    )

    print("Incident loaded successfully!")
    print("ID:", incident["incident_id"])
    print("Title:", incident["title"])
    print("Severity:", incident["severity"])
    print("Status:", incident["status"])
