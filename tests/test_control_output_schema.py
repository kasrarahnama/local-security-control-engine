import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from pydantic import ValidationError

from control_output_schema import validate_control_output
from control_implementation_engine import enforce_binding_ids


def test_validate_control_output_accepts_valid_json():
    data = {
        "control_id": "SC-28",
        "control_name": "Protection of Information at Rest",
        "reason": "Database components exist in architecture",
        "architecture_binding": {
            "components": ["comp-2"],
            "roles": [],
            "users": [],
            "policies": [],
            "flows": [],
        },
        "implementation_guidance": [
            "Enable encryption at rest for database storage."
        ],
        "evidence_sources": [
            {
                "source_name": "security-pillar.pdf",
                "chunk_index": 67,
                "topic": "aws-well-architected",
            }
        ],
    }

    validated = validate_control_output(data)

    assert validated.control_id == "SC-28"
    assert validated.architecture_binding.components == ["comp-2"]
    assert validated.evidence_sources[0].source_name == "security-pillar.pdf"


def test_validate_control_output_rejects_invalid_json():
    bad_data = {
        "control_id": "SC-28",
        # control_name is missing
        "reason": "Database components exist in architecture",
        "architecture_binding": {
            "components": ["comp-2"],
            "roles": [],
            "users": [],
            "policies": [],
            "flows": [],
        },
        "implementation_guidance": [
            "Enable encryption at rest for database storage."
        ],
        "evidence_sources": [
            {
                "source_name": "security-pillar.pdf",
                "chunk_index": 67,
                "topic": "aws-well-architected",
            }
        ],
    }

    with pytest.raises(ValidationError):
        validate_control_output(bad_data)


def test_enforce_binding_ids_removes_invalid_references():
    context = {
        "applies_to": {
            "components": ["comp-2"],
            "roles": [],
            "users": [],
            "policies": [],
            "flows": [],
        }
    }

    generated_output = {
        "control_id": "SC-28",
        "control_name": "Protection of Information at Rest",
        "architecture_binding": {
            "components": ["comp-2", "comp-999"],
            "roles": ["role-1"],
            "users": ["user-1"],
            "policies": ["policy-1"],
            "flows": ["flow-1"],
        },
        "implementation_guidance": [
            "Enable encryption at rest."
        ],
        "evidence_sources": [
            {
                "source_name": "security-pillar.pdf",
                "chunk_index": 67,
                "topic": "aws-well-architected",
            }
        ],
    }

    cleaned = enforce_binding_ids(generated_output, context)

    assert cleaned["architecture_binding"]["components"] == ["comp-2"]
    assert cleaned["architecture_binding"]["roles"] == []
    assert cleaned["architecture_binding"]["users"] == []
    assert cleaned["architecture_binding"]["policies"] == []
    assert cleaned["architecture_binding"]["flows"] == []