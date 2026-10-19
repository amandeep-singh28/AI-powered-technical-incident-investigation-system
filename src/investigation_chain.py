import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.investigation_schema import InvestigationReport
from src.incident_loader import load_incident
from src.timeline_builder import build_timeline


# Load environment variables from .env
load_dotenv()


# Initialize the LLM using Groq's OpenAI-compatible API
llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# Configure structured output
structured_llm = llm.with_structured_output(InvestigationReport)


# Define the investigation prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an evidence-driven technical incident investigator.

Use only the supplied evidence.
Separate verified facts from possible causes.
Never claim a possible cause is confirmed without supporting evidence.
Identify unknowns and recommend concrete checks.

For every verified finding:
- Cite the exact source filename.
- Use timestamps when applicable.
- Do not invent evidence or source references.
- Do not treat temporal correlation as proof of causation.

If evidence is insufficient, say so explicitly."""
    ),
    (
        "human",
        """Incident details:
{incident}

Combined event timeline:
{timeline}

Technical documentation:
{documentation}

Produce a structured investigation report for this incident."""
    ),
])

# LCEL chain: prompt -> structured LLM output
investigation_chain = prompt | structured_llm


def investigate_incident(incident_id: str) -> InvestigationReport:
    """Investigate an incident using its metadata, logs, and documentation."""

    root = Path("Evidence/data")

    # 1. Load incident metadata
    incident_path = root / "incidents" / f"{incident_id}.json"
    incident = load_incident(incident_path)

    # 2. Build a timeline while preserving each event's source filename
    log_files = [
        root / "logs" / f"{incident_id}.log",
        root / "logs" / "deployment.log",
    ]

    timeline_events = []

    for log_file in log_files:
        events = build_timeline(str(log_file))

        for event in events:
            timeline_events.append({
                **event,
                "source": log_file.as_posix(),
            })

    # Sort all events chronologically
    timeline_events.sort(
        key=lambda event: event["timestamp"]
    )

    # Convert events into readable, source-labelled text
    timeline = "\n".join(
        f"[Source: {event['source']}] "
        f"[{event['timestamp']}] "
        f"{event['level']} {event['service']}: "
        f"{event['message']}"
        for event in timeline_events
    )

    # 3. Load technical documentation
    documentation_path = (
        root / "documentation" / "checkout_service.md"
    )

    documentation = documentation_path.read_text(
        encoding="utf-8"
    )

    # 4. Invoke the LangChain investigation chain
    report = investigation_chain.invoke({
        "incident": incident,
        "timeline": timeline,
        "documentation": documentation,
    })

    return report


if __name__ == "__main__":
    report = investigate_incident("INC-001")
    print(report.model_dump_json(indent=2))
