from src.log_parser import load_logs


def build_timeline(*log_files: str) -> list[dict]:
    """Combine events from multiple log files chronologically."""

    all_events = []

    for file_path in log_files:
        events = load_logs(file_path)
        all_events.extend(events)

    return sorted(
        all_events,
        key=lambda event: event["timestamp"]
    )


if __name__ == "__main__":
    timeline = build_timeline(
        "Evidence/data/logs/INC-001.log",
        "Evidence/data/logs/deployment.log",
    )

    print("Total events:", len(timeline))
    print("\nUnified incident timeline:\n")

    for event in timeline:
        print(
            event["timestamp"].isoformat(),
            "|", event["level"],
            "|", event["service"],
            "|", event["message"],
        )
