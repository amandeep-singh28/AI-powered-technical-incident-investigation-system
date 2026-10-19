import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.investigation_schema import InvestigationReport

from src.incident_loader import load_incident
from src.timeline_builder import build_timeline
from pathlib import Path


llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

structured_llm = llm.with_structured_output(InvestigationReport)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an evidence-driven technical incident investigator.

Use only the supplied evidence.
Separate verified facts from possible causes.
Never claim a possible cause is confirmed without supporting evidence.
Identify unknowns and recommend concrete checks.
Cite the exact evidence filename in each verified finding.
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

        Produce an investigation report for this incident."""
    ),
])

investigation_chain = prompt | structured_llm



def investigate_incident(incident_id: str) -> InvestigationReport:
    root = Path("Evidence/data")

    incident = load_incident(
        root / "incidents" / f"{incident_id}.json"
    )

    timeline = build_timeline(
        str(root / "logs" / f"{incident_id}.log"),
        str(root / "logs" / "deployment.log"),
    )

    documentation = (
        root / "documentation" / "checkout_service.md"
    ).read_text(encoding="utf-8")

    return investigation_chain.invoke({
        "incident": incident,
        "timeline": timeline,
        "documentation": documentation,
    })


if __name__ == "__main__":
    report = investigate_incident("INC-001")
    print(report.model_dump_json(indent=2))
