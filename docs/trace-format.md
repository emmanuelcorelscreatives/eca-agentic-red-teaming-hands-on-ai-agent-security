# Local replay evidence

A report records fixture-manifest SHA256, proposal SHA256, policy SHA256 and separate case runs. Each event records a step number, supplied local principal label, tool name, arguments, gateway decision, whether a stub handler was invoked, and an effect label. A proposal is not execution; execution of a local stub is not external or durable effect.

The baseline gateway is a teaching implementation. Its local principal label is not cryptographic sender authentication, and its tool allowlist is not a complete target-, tenant- or session-scoped authorization service. Those are explicit extension exercises for the identity and delegation stages. No autonomous agent has run merely because local proposals were replayed.

Treat missing fields, missing traces and unrun checks as unknown. Keep timestamps, fixture versions, exact reviewed revision and scoring-rule identity with your own evidence. Use synthetic payloads and redact real credentials before sharing an authorized adapter trace.
