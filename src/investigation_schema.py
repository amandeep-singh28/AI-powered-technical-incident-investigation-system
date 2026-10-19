
from pydantic import BaseModel, Field


class EvidenceFinding(BaseModel):
    finding: str = Field(
        description="A factual observation from the evidence"
    )
    source: str = Field(
        description="The file or evidence source supporting the finding"
    )


class InvestigationReport(BaseModel):
    incident_id: str = Field(
        description="The incident identifier"
    )
    incident_summary: str = Field(
        description="A concise summary of the incident"
    )
    verified_facts: list[EvidenceFinding] = Field(
        description="Facts directly supported by available evidence"
    )
    possible_causes: list[str] = Field(
        description="Potential explanations that still need verification"
    )
    recommended_checks: list[str] = Field(
        description="Checks an engineer should perform next"
    )
    unknowns: list[str] = Field(
        description="Important questions the evidence cannot yet answer"
    )
