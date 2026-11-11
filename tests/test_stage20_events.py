import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1] / "examples" / "stage20_events"

def load(name):
    return json.loads((ROOT / name).read_bytes())

class EventSchemaExercise(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load("event.schema.json")
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def test_complete_constructed_event_has_the_required_shape(self):
        self.validator.validate(load("event.json"))

    def test_unfinished_null_placeholders_are_not_a_completed_event(self):
        with self.assertRaises(ValidationError):
            self.validator.validate(load("draft-event.json"))

    def test_trace_keeps_three_separate_valid_records(self):
        trace = load("trace.json")
        self.assertEqual([e["step_id"] for e in trace], ["step-01", "step-02", "step-03"])
        self.assertEqual(len({e["correlation_id"] for e in trace}), 1)
        for event in trace:
            self.validator.validate(event)
        denied = trace[1]
        self.assertEqual(denied["policy_outcome"]["decision"], "deny")
        self.assertEqual(denied["executed_side_effect"]["status"], "not_executed")
        self.assertEqual(denied["state_diff"]["status"], "not_observed")

    def test_missing_correlation_id_is_rejected(self):
        event = load("event.json")
        del event["correlation_id"]
        with self.assertRaises(ValidationError):
            self.validator.validate(event)

    def test_extra_validated_argument_is_rejected(self):
        event = load("event.json")
        event["validated_arguments"]["recipient"] = "outside.example"
        with self.assertRaises(ValidationError):
            self.validator.validate(event)

    def test_unknown_status_value_is_rejected(self):
        event = load("event.json")
        event["validated_arguments"]["status"] = "closed"
        with self.assertRaises(ValidationError):
            self.validator.validate(event)

    def test_schema_shape_does_not_establish_a_real_world_outcome(self):
        event = copy.deepcopy(load("event.json"))
        event["executed_side_effect"]["receipt"] = "fictional-label-only"
        self.validator.validate(event)
        self.assertEqual(event["executed_side_effect"]["receipt"], "fictional-label-only")

if __name__ == "__main__":
    unittest.main()
