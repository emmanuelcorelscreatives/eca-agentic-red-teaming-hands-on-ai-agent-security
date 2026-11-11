"""A transparent local gateway demonstration, not a production authorization service."""
import copy

SCHEMAS = {
    'read_ticket': {'ticket_id'}, 'search_kb': {'query'},
    'draft_message': {'ticket_id', 'body'}, 'send_message': {'ticket_id', 'body'},
    'update_ticket': {'ticket_id', 'priority'}, 'write_memory': {'key', 'value'},
}

class Gateway:
    def __init__(self, fixtures, allowed):
        self.state = copy.deepcopy(fixtures)
        self.allowed = set(allowed)
        self.events = []
        self.outbox = []
        self.memory = {}

    def propose(self, tool, arguments, principal='learner-agent'):
        event = {'step': len(self.events) + 1, 'principal': principal, 'tool': tool,
                 'arguments': copy.deepcopy(arguments), 'decision': 'blocked',
                 'handler_invoked': False, 'effect': 'none'}
        self.events.append(event)
        if tool not in SCHEMAS:
            event['reason'] = 'unknown_tool'
            return event
        if not isinstance(arguments, dict) or set(arguments) != SCHEMAS[tool] or any(not isinstance(v, str) for v in arguments.values()):
            event['reason'] = 'invalid_arguments'
            return event
        if tool not in self.allowed:
            event['reason'] = 'not_granted_by_local_demo_policy'
            return event
        if 'ticket_id' in arguments and arguments['ticket_id'] not in self.state.get('tickets', {}):
            event['reason'] = 'unknown_synthetic_ticket'
            return event
        event.update(decision='executed', handler_invoked=True)
        if tool == 'read_ticket':
            event['result'] = copy.deepcopy(self.state['tickets'][arguments['ticket_id']])
        elif tool == 'search_kb':
            event['result'] = [copy.deepcopy(x) for x in self.state.get('knowledge', []) if arguments['query'].casefold() in x['topic'].casefold()]
        elif tool == 'draft_message':
            event['result'] = {'draft': arguments['body'], 'sent': False}
        elif tool == 'send_message':
            self.outbox.append(copy.deepcopy(arguments))
            event.update(result={'captured_locally': True, 'delivered': False}, effect='local_outbox_only')
        elif tool == 'update_ticket':
            self.state['tickets'][arguments['ticket_id']]['priority'] = arguments['priority']
            event['effect'] = 'in_memory_only'
        elif tool == 'write_memory':
            self.memory[arguments['key']] = arguments['value']
            event['effect'] = 'in_memory_only'
        return event
