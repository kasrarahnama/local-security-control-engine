from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field, ValidationError


class ArchitectureBinding(BaseModel):
    components: List[str] = Field(default_factory=list)
    roles: List[str] = Field(default_factory=list)
    users: List[str] = Field(default_factory=list)
    policies: List[str] = Field(default_factory=list)
    flows: List[str] = Field(default_factory=list)


class EvidenceSource(BaseModel):
    source_name: str
    chunk_index: int
    topic: str


class ControlImplementationOutput(BaseModel):
    control_id: str
    control_name: str
    reason: str
    architecture_binding: ArchitectureBinding
    implementation_guidance: List[str]
    evidence_sources: List[EvidenceSource]


def validate_control_output(data: Dict[str, Any]) -> ControlImplementationOutput:
    return ControlImplementationOutput.model_validate(data)