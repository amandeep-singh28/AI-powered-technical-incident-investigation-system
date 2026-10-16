from pathlib import Path
from datetime import datetime


def parse_log_line(line: str) -> dict:
    """Convert one raw log line into structured data."""

    parts = line.strip().split(maxsplit=3)

    if len(parts) != 4:
        raise ValueError(f"Invalid log line: {line!r}")

    timestamp_text, level, service, message = parts

    timestamp = datetime.fromisoformat(timestamp_text)

    return {
        "timestamp": timestamp,
        "level": level,
        "service": service,
        "message": message,
    }


def load_logs(file_path: str) -> list[dict]:
    """Read a log file and parse each non-empty line."""

    events = []

    with Path(file_path).open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                events.append(parse_log_line(line))

    return events


def analyze_logs(events: list[dict]) -> dict:
    """Summarize log events for an incident."""

    sorted_events = sorted(
        events,
        key=lambda event: event["timestamp"]
    )

    errors = [
        event for event in sorted_events
        if event["level"] == "ERROR"
    ]

    return {
        "total_events": len(sorted_events),
        "error_count": len(errors),
        "first_event": sorted_events[0] if sorted_events else None,
        "first_error": errors[0] if errors else None,
        "timeline": sorted_events,
    }

if __name__ == "__main__":
    logs = load_logs("Evidence/data/logs/INC-001.log")
    report = analyze_logs(logs)

    print("Total events:", report["total_events"])
    print("Error count:", report["error_count"])
    print("First event:", report["first_event"])
    print("First error:", report["first_error"])

