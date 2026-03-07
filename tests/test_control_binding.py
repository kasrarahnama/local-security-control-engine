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
from control_binding import bind_controls


SAMPLE_JSON = Path("sample_oscal.json")


def build_summary():
    data = load_oscal_json(SAMPLE_JSON)
    components = extract_components(data)
    flows = extract_data_flows(data)
    iam = extract_iam_constructs(data)
    return generate_architecture_summary(components, flows, iam)


def test_bind_controls_returns_list():
    summary = build_summary()
    bindings = bind_controls(summary)

    assert isinstance(bindings, list)
    assert len(bindings) > 0


def test_bindings_include_iam_controls():
    summary = build_summary()
    bindings = bind_controls(summary)

    control_ids = [b["control_id"] for b in bindings]

    assert "AC-2/AC-3" in control_ids
    assert "LeastPrivilege" in control_ids


def test_bindings_include_database_control():
    summary = build_summary()
    bindings = bind_controls(summary)

    control_ids = [b["control_id"] for b in bindings]

    assert "SC-28" in control_ids


def test_bindings_include_application_control():
    summary = build_summary()
    bindings = bind_controls(summary)

    control_ids = [b["control_id"] for b in bindings]

    assert "SI-10" in control_ids