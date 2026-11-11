"""Record local proposal replay; do not manufacture agent or security outcomes."""
import argparse
import hashlib
import json
import multiprocessing
import tempfile
import time
from pathlib import Path
from .gateway import Gateway

def load_manifest(directory):
    directory = Path(directory).resolve()
    manifest = json.loads((directory / 'manifest.json').read_text())
    cases, seen = [], set()
    for row in manifest['cases']:
        if row['id'] in seen:
            raise ValueError('Duplicate case ID')
        seen.add(row['id'])
        name = Path(row['path'])
        target = (directory / name).resolve()
        if name.is_absolute() or not target.is_relative_to(directory):
            raise ValueError('Case path escapes fixture version')
        case = json.loads(target.read_text())
        if case['id'] != row['id']:
            raise ValueError('Case identity mismatch')
        cases.append(case)
    return manifest, cases

def _replay(case, proposals, allowed, max_steps, work, connection):
    gateway = Gateway(case['fixtures'], allowed)
    stop = 'proposals_exhausted'
    for row in proposals:
        if len(gateway.events) >= max_steps:
            stop = 'step_limit'
            break
        gateway.propose(row['tool'], row['arguments'])
    connection.send({'case_id': case['id'], 'events': gateway.events, 'state_after': gateway.state,
                     'local_outbox': gateway.outbox, 'stop_reason': stop,
                     'observation_kind': 'local_proposal_replay', 'agent_model_executed': False,
                     'security_outcome': 'NOT_SCORED', 'utility_outcome': 'NOT_SCORED'})
    connection.close()

def run_case(case, proposals, allowed, max_steps=10, timeout=5):
    if max_steps < 1 or timeout <= 0:
        raise ValueError('Limits must be positive')
    with tempfile.TemporaryDirectory(prefix='eca-harbordesk-') as work:
        receiver, sender = multiprocessing.Pipe(duplex=False)
        process = multiprocessing.Process(target=_replay, args=(case, proposals, allowed, max_steps, work, sender))
        started = time.monotonic()
        process.start()
        sender.close()
        try:
            if not receiver.poll(timeout):
                process.terminate()
                return {'case_id': case['id'], 'stop_reason': 'wall_clock_limit', 'security_outcome': 'NOT_SCORED'}
            result = receiver.recv()
            result['elapsed_seconds'] = time.monotonic() - started
            return result
        finally:
            process.join(timeout=1)
            if process.is_alive():
                process.kill()
                process.join()
            receiver.close()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures', default='fixtures/v1')
    parser.add_argument('--proposals', default='examples/read-and-draft.json')
    parser.add_argument('--policy', default='policies/read-and-draft.json')
    parser.add_argument('--output', required=True)
    parser.add_argument('--max-steps', type=int, default=10)
    parser.add_argument('--timeout', type=float, default=5)
    args = parser.parse_args()
    manifest, cases = load_manifest(args.fixtures)
    proposals = json.loads(Path(args.proposals).read_text())
    policy = json.loads(Path(args.policy).read_text())
    if policy.get('network_delivery') is not False:
        raise ValueError('Only the non-delivering local demo policy is supported')
    report = {'fixture_version': manifest['version'], 'fixture_manifest_sha256': hashlib.sha256((Path(args.fixtures)/'manifest.json').read_bytes()).hexdigest(),
              'policy_sha256': hashlib.sha256(Path(args.policy).read_bytes()).hexdigest(),
              'proposal_sha256': hashlib.sha256(Path(args.proposals).read_bytes()).hexdigest(),
              'runs': [run_case(case, proposals, policy['allowed_tools'], args.max_steps, args.timeout) for case in cases]}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print('Saved local proposal-replay evidence to ' + str(output))

if __name__ == '__main__':
    main()
