# Instrumentation and event schema

Use these fixtures with Stage 20 Lesson 2 in Python 3.12 and jsonschema 4.23.0.

```sh
python -m pip install -r examples/stage20_events/requirements.txt
python -m unittest discover -s tests -p 'test_stage20_events.py' -v
```

- `draft-event.json` is the unfinished field-walkthrough state. Its later null placeholders intentionally fail the completed schema.
- `event.json` is the completed standalone field-walkthrough example.
- `event.schema.json` checks the nine required fields, their structures and allowed values.
- `trace.json` provides the later three-event reading exercise: a proposed allowance without execution, a constructed denial, and a constructed executed/observed example.
- `correlation-map.md` links separate step IDs through a shared correlation ID.

All records are constructed teaching data. Values such as `allow`, `executed`, `observed` and the `sim-*` references describe fictional examples. They are not records from a HarborDesk deployment. Schema acceptance establishes document shape and allowed values; identity, authorization, execution and lasting state changes need their own evidence. Preserve each event rather than combining its claims with another event.


## Drafting states and intentional negative input

`draft-event-allow.json` is the progressive draft after the allow decision and synthetic reason have been written. Later action, state, identity and correlation fields remain null. It is deliberately unfinished and must not be presented as a schema-valid final event or an executed run.

`trace-invalid.json` is copied from the full three-event `trace.json`. Only step-03 has two deliberate edits: `correlation_id` is removed, and `validated_arguments.status` is changed from `pending` to unsupported `approved`. Compare these files in the native editor and run the lesson validator yourself; no saved validator output is provided.

`reference-notes.md` labels sim-write-17 and sim-read-18 as synthetic fixture references, not supplied run evidence. Their presence in JSON does not establish that supporting run records exist.
