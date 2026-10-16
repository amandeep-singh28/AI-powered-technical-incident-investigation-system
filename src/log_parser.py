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


if __name__ == "__main__":
    logs = load_logs("Evidence/data/logs/INC-001.log")

    print(f"Loaded {len(logs)} log events")

    for event in logs:
        print(event)
