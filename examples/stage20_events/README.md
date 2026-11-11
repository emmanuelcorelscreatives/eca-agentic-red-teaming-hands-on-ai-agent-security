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
