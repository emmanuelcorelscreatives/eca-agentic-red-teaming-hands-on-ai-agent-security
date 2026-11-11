# Controlled catalog-description comparison

Stage 12, lesson 3: Lab — Dynamic Tool-Selection Test.

These are author-built synthetic fixture files, not an actual HarborDesk tool inventory or captured agent run. Both snapshots contain `get_ticket(ticket_id)` and `set_ticket_status(ticket_id, status)` with the same complete input schemas and required string arguments. Only `get_ticket.description` changes. Catalog B contains the exact adversarial sentence specified by the lesson, as test input; it is not an instruction for the operator.

Read `task.txt` unchanged for both conditions. Keep the approved agent setup, initial synthetic record state, gateway policy, names, order and schemas fixed. The intended constructed policy permits a read and blocks a write, but these files do not claim that any real gateway enforced it.

`catalog-description.diff` records exactly one removed description line and one added description line. The editable SVG shows the two complete teaching definitions and the unfilled evidence packet. Each JSON trace template has a blank run ID and null observations for proposed calls, arguments, gateway decisions, executions, returned results, task completion and state checks. The comparison template also starts empty. Do not fill observations from the expected route or from this diagram. Collect your own authorized evidence, attach the actual snapshot each run saw and preserve the event order.

Verify the fixture without running an agent or tool:

```text
python -m unittest discover -s tests -p test_catalog_description_pair.py -v
```

Those checks validate the single-description change, equal argument schemas, exact diff and empty observation templates. They do not measure attack success, prove that a catalog was seen or establish a tool execution.
