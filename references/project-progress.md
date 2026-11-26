# Project progress and task handoff

A long-running inference or evaluation task can outlive its terminal, agent session, or container. Preserve enough state in the consuming project's durable workspace for a fresh Codex or other harness session to continue.

## Keep a durable direction record

Organize `agent-progress/` by long-running work direction, such as GPU performance, CPU diagnosis, or evaluation integrity. Maintain a principal record for each direction and a short navigation page. Update current goals, user decisions, accepted findings, applicability limits, open questions, and reproduction entry points.

Store raw commands, configurations, logs, and results with their experiment directories. Link them from the progress record. When feedback changes an earlier conclusion, update its adoption status and retain the counterexample's evidence.

## Write the current handoff before launching

For an experiment that can interrupt the environment, write a task handoff under the consuming project's `agent-progress/.chat/`. Include the task scope and user decisions, input and configuration identity, launch command, run directory, process identity, log and output locations, protection limits, and the first recovery checks.

A compact handoff can follow this order.

```text
Goal and authorized run scope
Input, configuration, and execution entry point
Run directory, process identities, logs, and outputs
Completed checks and current stage
Protection and stop conditions
First checks after reconnecting
```

Update that handoff with launch confirmation, checkpoints, failures, and changes. When the task finishes or stops, promote reusable findings to the direction record and archive the handoff with the experiment. Keep the current handoff directory focused on active work.

## Resume through a fresh harness session

Restore account access using the user's private [account recovery route](recovery.md). Read the direction record and current handoff before acting. Verify original processes, recent logs and heartbeat, protection events, output completeness, and host or container identity. Record the new observations, then decide whether to wait, stop, resume, or create a new attempt.
