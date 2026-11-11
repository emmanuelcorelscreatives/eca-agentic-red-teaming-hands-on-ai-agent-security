import copy
import json
import tempfile
import unittest
from pathlib import Path
from eca_lab.gateway import Gateway
from eca_lab.runner import load_manifest, run_case

class CourseLabTests(unittest.TestCase):
    def setUp(self):
        _, self.cases = load_manifest('fixtures/v1')
        self.fixtures = self.cases[0]['fixtures']

    def test_denied_send_never_calls_handler_or_changes_outbox(self):
        g = Gateway(self.fixtures, ['read_ticket'])
        e = g.propose('send_message', {'ticket_id':'T-104','body':'synthetic'})
        self.assertEqual(e['decision'], 'blocked')
        self.assertFalse(e['handler_invoked'])
        self.assertEqual(g.outbox, [])

    def test_extra_arguments_are_rejected_before_handler(self):
        g = Gateway(self.fixtures, ['read_ticket'])
        self.assertEqual(g.propose('read_ticket', {'ticket_id':'T-104','admin':'yes'})['reason'], 'invalid_arguments')
        self.assertFalse(g.events[0]['handler_invoked'])

    def test_non_string_argument_is_rejected(self):
        self.assertEqual(Gateway(self.fixtures,['read_ticket']).propose('read_ticket',{'ticket_id':104})['reason'], 'invalid_arguments')

    def test_unknown_tools_and_targets_are_rejected(self):
        g = Gateway(self.fixtures, ['read_ticket'])
        self.assertEqual(g.propose('invented_tool', {})['reason'],'unknown_tool')
        self.assertEqual(g.propose('read_ticket', {'ticket_id':'NOT-IN-FIXTURES'})['reason'],'unknown_synthetic_ticket')

    def test_read_returns_copy_of_fixture(self):
        g = Gateway(self.fixtures, ['read_ticket'])
        result = g.propose('read_ticket', {'ticket_id':'T-104'})['result']
        result['priority'] = 'changed'
        self.assertEqual(g.state['tickets']['T-104']['priority'], 'normal')

    def test_draft_does_not_send(self):
        g = Gateway(self.fixtures,['draft_message'])
        e = g.propose('draft_message', {'ticket_id':'T-104','body':'local draft'})
        self.assertFalse(e['result']['sent'])
        self.assertEqual(g.outbox, [])

    def test_explicitly_permitted_stub_send_is_only_local_capture(self):
        g = Gateway(self.fixtures,['send_message'])
        e = g.propose('send_message', {'ticket_id':'T-104','body':'local capture'})
        self.assertEqual(e['effect'],'local_outbox_only')
        self.assertFalse(e['result']['delivered'])
        self.assertEqual(len(g.outbox),1)

    def test_cases_reset_and_input_is_not_mutated(self):
        original = copy.deepcopy(self.fixtures)
        g = Gateway(self.fixtures,['update_ticket'])
        g.propose('update_ticket',{'ticket_id':'LAB-042','priority':'urgent'})
        self.assertEqual(self.fixtures, original)
        self.assertEqual(Gateway(self.fixtures,[]).state['tickets']['LAB-042']['priority'],'normal')

    def test_pair_changes_only_lower_trust_ticket_body(self):
        a,b=copy.deepcopy(self.cases)
        self.assertNotEqual(a.pop('ticket_body'),b.pop('ticket_body'))
        a.pop('id'); b.pop('id')
        self.assertEqual(a,b)

    def test_replay_step_limit_and_no_fabricated_scores(self):
        proposals=[{'tool':'read_ticket','arguments':{'ticket_id':'T-104'}}]*5
        r=run_case(self.cases[0],proposals,['read_ticket'],max_steps=2)
        self.assertEqual(len(r['events']),2)
        self.assertEqual(r['stop_reason'],'step_limit')
        self.assertFalse(r['agent_model_executed'])
        self.assertEqual(r['security_outcome'],'NOT_SCORED')

    def test_manifest_rejects_duplicate_ids_and_traversal(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            (p/'case.json').write_text(json.dumps(self.cases[0]))
            row={'id':self.cases[0]['id'],'path':'case.json'}
            (p/'manifest.json').write_text(json.dumps({'cases':[row,row]}))
            with self.assertRaises(ValueError):load_manifest(p)
            (p/'manifest.json').write_text(json.dumps({'cases':[{'id':'x','path':'../outside.json'}]}))
            with self.assertRaises(ValueError):load_manifest(p)

    def test_all_119_curriculum_worksheets_are_blank_and_present(self):
        lessons=json.loads(Path('course-index.json').read_text())['lessons']
        self.assertEqual(len(lessons),119)
        self.assertEqual(len({x['directory'] for x in lessons}),119)
        for lesson in lessons:
            folder=Path(lesson['directory'])
            self.assertTrue((folder/'README.md').is_file())
            w=json.loads((folder/'worksheet.json').read_text())
            self.assertEqual(w['decision'],'NOT_RUN')
            self.assertEqual(w['actual_observations'],[])
