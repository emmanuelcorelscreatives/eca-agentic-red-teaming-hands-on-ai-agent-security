"""Stage 3 Lesson 3: six local stubs, one permitted read, one denied send.

Synthetic demonstration only. Actor strings are supplied by this script;
authentication, durable logging and external effects are not implemented.
"""
TICKETS = {'T-104': {'subject': 'Access request', 'status': 'open'}}
KB = {'KB-7': {'topic': 'Account access', 'text': 'Use the lab checklist.'}}
FIELDS = {
    'read_ticket': {'ticket_id'},
    'search_kb': {'query'},
    'draft_message': {'ticket_id', 'body'},
    'send_message': {'ticket_id', 'body'},
    'update_record': {'ticket_id', 'status'},
    'write_memory': {'key', 'value'},
}


def read_ticket(ticket_id):
    return {'ticket_id': ticket_id, **TICKETS[ticket_id]}


def search_kb(query):
    return [{'id': key, **item} for key, item in KB.items()
            if query.lower() in item['topic'].lower()]


def draft_message(ticket_id, body):
    return {'ticket_id': ticket_id, 'draft': body}


def send_message(ticket_id, body):
    return {'simulated_send': True, 'ticket_id': ticket_id, 'body': body}


def update_record(ticket_id, status):
    return {'simulated_update': True, 'ticket_id': ticket_id, 'status': status}


def write_memory(key, value):
    return {'simulated_write': True, 'key': key, 'value': value}


TOOLS = {
    'read_ticket': read_ticket,
    'search_kb': search_kb,
    'draft_message': draft_message,
    'send_message': send_message,
    'update_record': update_record,
    'write_memory': write_memory,
}
POLICY = {
    'analyst': {'read_ticket', 'search_kb', 'draft_message'},
    'lab_operator': set(TOOLS),
}
LOG = []


def gateway(actor, tool, args):
    call_id = f'call-{len(LOG) // 2 + 1:03}'
    LOG.append({'call_id': call_id, 'phase': 'proposed', 'actor': actor,
                'tool': tool, 'args': args.copy()})
    if tool not in TOOLS or tool not in POLICY.get(actor, set()):
        LOG.append({'call_id': call_id, 'phase': 'blocked', 'reason': 'not permitted'})
        return None
    if set(args) != FIELDS[tool] or not all(isinstance(value, str) for value in args.values()):
        LOG.append({'call_id': call_id, 'phase': 'blocked', 'reason': 'invalid arguments'})
        return None
    if 'ticket_id' in args and args['ticket_id'] not in TICKETS:
        LOG.append({'call_id': call_id, 'phase': 'blocked', 'reason': 'outside lab fixtures'})
        return None
    result = TOOLS[tool](**args)
    LOG.append({'call_id': call_id, 'phase': 'executed', 'result': result})
    return result


# LOG lives in process memory; terminal output is not yet an evidence file.
if __name__ == '__main__':
    import json
    gateway('analyst', 'read_ticket', {'ticket_id': 'T-104'})
    gateway('analyst', 'send_message', {'ticket_id': 'T-104', 'body': 'Please check the lab note.'})
    for entry in LOG:
        print(json.dumps(entry, sort_keys=True))
