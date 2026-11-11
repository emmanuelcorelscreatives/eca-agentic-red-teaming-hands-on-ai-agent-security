import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / 'examples/stage03_gateway/lab.py'
spec = importlib.util.spec_from_file_location('stage03_gateway', PATH)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class Stage03GatewayTests(unittest.TestCase):
    def setUp(self):
        lab.LOG.clear()

    def test_exact_two_call_script_has_linked_local_outcomes(self):
        run = subprocess.run([sys.executable, str(PATH)], capture_output=True, text=True, check=True)
        rows = [json.loads(line) for line in run.stdout.splitlines()]
        self.assertEqual([(r['call_id'], r['phase']) for r in rows],
                         [('call-001', 'proposed'), ('call-001', 'executed'),
                          ('call-002', 'proposed'), ('call-002', 'blocked')])
        self.assertEqual(rows[1]['result'], {'ticket_id': 'T-104', 'subject': 'Access request', 'status': 'open'})
        self.assertEqual(rows[3]['reason'], 'not permitted')
        self.assertNotIn('result', rows[3])

    def test_denied_call_never_invokes_handler(self):
        with patch.dict(lab.TOOLS, send_message=lambda **kw: self.fail('Denied handler ran')):
            self.assertIsNone(lab.gateway('analyst', 'send_message', {'ticket_id': 'T-104', 'body': 'Synthetic'}))
        self.assertEqual(lab.LOG[-1]['phase'], 'blocked')

    def test_invalid_arguments_and_unknown_fixture_never_execute(self):
        for args, reason in [({'ticket_id': 'T-104', 'extra': 'x'}, 'invalid arguments'),
                             ({'ticket_id': 104}, 'invalid arguments'),
                             ({'ticket_id': 'T-900'}, 'outside lab fixtures')]:
            with patch.dict(lab.TOOLS, read_ticket=lambda **kw: self.fail('Invalid handler ran')):
                self.assertIsNone(lab.gateway('analyst', 'read_ticket', args))
            self.assertEqual(lab.LOG[-1]['reason'], reason)

    def test_action_shaped_stubs_do_not_change_fixtures(self):
        before = copy.deepcopy((lab.TICKETS, lab.KB))
        self.assertTrue(lab.gateway('lab_operator', 'send_message', {'ticket_id': 'T-104', 'body': 'Synthetic'})['simulated_send'])
        self.assertTrue(lab.gateway('lab_operator', 'update_record', {'ticket_id': 'T-104', 'status': 'closed'})['simulated_update'])
        self.assertTrue(lab.gateway('lab_operator', 'write_memory', {'key': 'demo', 'value': 'not persistent'})['simulated_write'])
        self.assertEqual((lab.TICKETS, lab.KB), before)

    def test_unknown_actor_or_tool_is_not_permitted(self):
        self.assertIsNone(lab.gateway('untrusted', 'read_ticket', {'ticket_id': 'T-104'}))
        self.assertIsNone(lab.gateway('lab_operator', 'unknown_tool', {}))
        self.assertTrue(all(r.get('reason') == 'not permitted' for r in lab.LOG if r['phase'] == 'blocked'))

    def test_proposal_copies_arguments_before_caller_changes_them(self):
        args = {'ticket_id': 'T-104'}
        lab.gateway('analyst', 'read_ticket', args)
        args['ticket_id'] = 'changed-later'
        self.assertEqual(lab.LOG[0]['args'], {'ticket_id': 'T-104'})
