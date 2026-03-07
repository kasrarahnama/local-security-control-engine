import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from control_guidance import build_control_guidance


SAMPLE_JSON = "sample_oscal.json"


def test_build_control_guidance_returns_list():
    results = build_control_guidance(SAMPLE_JSON)

    assert isinstance(results, list)
    assert len(results) > 0


def test_each_guidance_item_has_required_fields():
    results = build_control_guidance(SAMPLE_JSON)

    for item in results:
        assert "control_id" in item
        assert "control_name" in item
        assert "reason" in item
        assert "applies_to" in item
        assert "guidance" in item


def test_guidance_contains_retrieved_text():
    results = build_control_guidance(SAMPLE_JSON)

    found_non_empty_guidance = False

    for item in results:
        if item["guidance"]:
            found_non_empty_guidance = True
            first = item["guidance"][0]
            assert "source_name" in first
            assert "topic" in first
            assert "text" in first

    assert found_non_empty_guidance is True