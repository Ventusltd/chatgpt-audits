#!/usr/bin/env python3
"""UNREVIEWED regression tests for top-level versus nested REPD identity."""
import json
from pathlib import Path
from reference_extractor import extract_top_level_repd_ref

fixture = json.loads(Path(__file__).with_name("binding-extractor-fixture.json").read_text())
assert extract_top_level_repd_ref(fixture["top_level_and_nested"]) == "13599"
assert extract_top_level_repd_ref(fixture["top_level_and_nested_reversed"]) == "17494"
try:
    extract_top_level_repd_ref(fixture["nested_only"])
except KeyError:
    pass
else:
    raise AssertionError("nested-only relationship must not establish project identity")
print(json.dumps({"review_status":"UNREVIEWED","tests":3,"passed":3,"classification":"observed"}))
