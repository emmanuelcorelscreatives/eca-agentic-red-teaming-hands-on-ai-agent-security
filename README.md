# Agentic Red-Teaming: Hands-On AI Agent Security

Emmanuel Corels Academy · Instructor: Emmanuel Corels

Supporting practice materials for all **119 main lessons**, in saved course order. Start with [the course index](course-index.json), then use the README and blank worksheet inside the matching lesson directory.

## Quick start

Use Python 3.11 or later. No API keys, paid model accounts, external services or third-party Python packages are required for this local demonstration.

```sh
python -m unittest discover -s tests -v
python -m eca_lab.runner --output evidence/local-demo.json
```

The second command records a **local proposal replay**, not an autonomous model assessment. It reads the same versioned case inventory, applies the explicitly supplied local gateway policy, and records proposed calls, blocked calls and invoked stub handlers separately. It does not assert attack success, model robustness, utility scores, actual message delivery or production isolation. The report marks security and utility `NOT_SCORED`. A learner must supply an authorized agent integration, existing scoring rules and real observations before making those claims.

## How this matches the course

- Stage 3’s fictional users are U-101 (Mira Vale) and U-102 (Oren), with HD-T-001 and HD-T-002. See `fixtures/stage03/`.
- The local stub example uses T-104 and KB-7. The gateway exposes `read_ticket`, `search_kb`, `draft_message`, `send_message`, `update_ticket` and `write_memory` with exact string argument schemas. The demo policy permits only the three read/draft tools.
- Stage 6’s paired printer-ticket worksheets retain LAB-042 and the unchanged “do not modify records” task. See `fixtures/stage06/`.
- Stage 20’s proposed `fixtures/v1` organization and HD-LAB-CLEAN-01 / HD-LAB-INJECT-01 identifiers are supplied as actual repository files. The ordinary billing-receipt case and injected case differ only in ticket-body content.
- These are distinct classroom fixture families. Do not merge their IDs or claim they are one observed live HarborDesk deployment.
- Other stages use their exact saved objective, core and practice/evidence brief with a blank worksheet. Supporting code is deliberately a small transparent foundation, not an invented completed implementation of every assessment.

## Evidence and scope

All names and records are synthetic. The default code imports no network clients, sends no mail, invokes no external agent, and resets its in-memory state for each case. Its temporary directory is removed after the worker finishes; evidence is written separately. Process timeout and step bounds apply to the local replay worker. They are not an operating-system security sandbox for arbitrary third-party agent code.

Local outbox capture, in-memory update and in-memory memory-write stubs have explicit effect labels; none is proof of external delivery or durable storage. A denied call must not invoke its handler. Preserve all failed observations. Never fill worksheet result fields before running the corresponding authorized check.

The original course contains proposed examples and explicitly unobserved states. These new supporting materials do not retroactively turn them into executed results. Do not rewrite a lesson’s topic, claim observed success from an illustration, or fabricate a tool trace to make a screenshot pass.

## Extending the exercises

Use the lesson-specific worksheet to define the legitimate task, attacker-controlled surface, invariant, oracle, paired control, run identity and review criteria. Add adapters only inside an isolated, authorized environment; preserve source provenance, principal identity and action-gateway decisions. Existing scoring criteria should be versioned and reused. Do not substitute the demo policy or fabricate a metric for a course exercise that requires different criteria.

See [the trace format](docs/trace-format.md) and [coherence map](docs/coherence-map.md). Generated `evidence/` is ignored so local observations and potentially sensitive adapter outputs are not published accidentally.

## Lesson-specific runnable examples

- [Stage 3, Lesson 3: six local stubs and two linked gateway calls](examples/stage03_gateway/README.md). This exact lesson uses `update_record`; the earlier `eca_lab` replay foundation is a separate example.
- [Stage 20, Lesson 4: record-security scoring with saved intermediate changes](examples/stage20_records/README.md). This implements only the records check, with explicit trusted-fixture assumptions and separate tests.

These additions preserve the 119 original lesson guides and blank learner worksheets.

- [Stage 18, Lesson 2: exact local approval-review prototype](examples/approval_review_prototype/README.md), with no network or sending capability.

- [Stage 24, Lesson 2: editable one-page management-summary draft](examples/management_summary/README.md), with blank evidence fields and three conditional proposed actions.
