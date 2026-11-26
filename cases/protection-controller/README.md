# Recovery and protection control

Interrupted CPU experiments needed a way to recover both the development environment and task state. Persistent handoffs recorded run locations, process identities, boot state, and reconstruction steps. Operator incident evidence narrowed the platform timeout window before application tracing was interpreted.

A later CPU/GPU overlap attempt exposed a protection defect. Five probe launches and three heartbeat intervals exceeded their limits without an automatic stop. Intermediate events reset the launch timer, and newer heartbeats could hide historical long gaps.

The fix retained a phase start per probe ID and checked both completed duration and active age. Heartbeat checks inspected every historical interval. Regression replay detected all eight timeout observations in the failed run and accepted the historical successful waves. An independent IPR run subsequently completed both waves without a protection violation.

A staggered run then provided adoption evidence and a counterexample. The first IPR wave passed. The second exceeded its launch limit and was stopped by the repaired controller. The GPU evaluation completed after host recovery was checked. The final state audit passed while the full overlap experiment failed.

The three records are in [case.json](case.json). The bundled evidence retains an original platform error line, replay results, independent-run acceptance, and the staggered outcome. [Recovery](../../references/recovery.md) describes the operating method.

The reusable recovery guidance now covers private account backup before launch and project progress handoff for a fresh harness session. See [account recovery](../../references/recovery.md) and [project progress](../../references/project-progress.md).
