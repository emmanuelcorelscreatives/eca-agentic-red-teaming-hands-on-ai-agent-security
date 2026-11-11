# Instrumentation and Event Schema

Emmanuel Corels Academy · Stage 20, lesson 2

## Saved lesson brief

Lesson 2 — Instrumentation and Event Schema
Stage 20 — Evaluation Harness, Replay, and Evidence Collection
Objective: Collect action-level evidence suitable for scoring.
Core: Capture per-step source, proposed action, validated arguments, policy outcome, executed side effect, state diff, agent identity, and correlation ID.
Practice / evidence: Create a minimal JSON event schema and validate a sample trace.

## Practice materials

Use the worksheet beside this file and the course [material index](../../../README.md). The brief above is retained from the course; this repository supplies supporting practice material rather than claiming that a proposed classroom example was already executed.

Record your own observations. Keep proposed actions, permitted actions, handler execution and durable effects separate. A blank evidence cell is not a pass. Use only synthetic data and an authorized local workspace.

## Deliverable

Complete `worksheet.json` for this lesson’s stated task. Link the exact fixture version, policy, trace and reviewed code revision you used. Do not invent measurements or results.

## Runnable schema exercise

The [event-schema example kit](../../../examples/stage20_events/README.md) supplies the unfinished event, completed event, final schema, three-event trace and correlation diagram. Install its pinned requirement in Python 3.12 and run the tests from the repository root. All sample records are constructed teaching data.
