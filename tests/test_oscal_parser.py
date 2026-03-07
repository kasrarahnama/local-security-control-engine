import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from oscal_parser import (
    load_oscal_json,
    extract_components,
    extract_data_flows,
    extract_iam_constructs,
    generate_architecture_summary,
)

SAMPLE_JSON = Path("sample_oscal.json")


def test_load_oscal_json():
    data = load_oscal_json(SAMPLE_JSON)
    assert isinstance(data, dict)
    assert "system-implementation" in data


def test_extract_components():
    data = load_oscal_json(SAMPLE_JSON)
    components = extract_components(data)

    assert len(components) == 2
    assert components[0]["id"] == "comp-1"
    assert components[0]["name"] == "Web Application"
    assert components[1]["type"] == "database"


def test_extract_data_flows():
    data = load_oscal_json(SAMPLE_JSON)
    flows = extract_data_flows(data)

    assert isinstance(flows, list)
    assert len(flows) == 0


def test_extract_iam_constructs():
    data = load_oscal_json(SAMPLE_JSON)
    iam = extract_iam_constructs(data)

    assert len(iam["roles"]) == 1
    assert len(iam["users"]) == 1
    assert len(iam["policies"]) == 1

    assert iam["roles"][0]["id"] == "role-1"
    assert iam["users"][0]["name"] == "SecurityAdmin"
    assert iam["policies"][0]["name"] == "LeastPrivilegePolicy"


def test_generate_architecture_summary():
    data = load_oscal_json(SAMPLE_JSON)

    components = extract_components(data)
    flows = extract_data_flows(data)
    iam = extract_iam_constructs(data)

    summary = generate_architecture_summary(components, flows, iam)

    assert summary["architecture_id"] == "arch-summary-001"
    assert summary["component_count"] == 2
    assert summary["data_flow_count"] == 0
    assert summary["role_count"] == 1
    assert summary["user_count"] == 1
    assert summary["policy_count"] == 1

    assert "traceability" in summary
    assert "component_ids" in summary["traceability"]
    assert summary["traceability"]["component_ids"] == ["comp-1", "comp-2"]
