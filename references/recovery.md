# Recovery and workload protection

## Preserve harness account access

Before an experiment that may lose the container or development environment, ask the user to prepare recovery for their Codex or other harness account. Under the authentication method in use, the user should copy the required API key, account credentials, or supported login backup to durable private storage that survives the experiment environment. A private location on the user's own device or an access-controlled persistent store can serve this purpose.

Have the user verify that the backup is accessible, its file access is restricted, and the account restoration steps are recorded privately. Retain a reauthorization route for credentials that expire or can be revoked. Follow the harness's supported authentication process, verify account access, and then resume from project progress. Actual credentials and their private backup location stay in the user's recovery channel.

The local case used a private `recover/` directory. The reusable method is preserving account access before the failure window; backup format and authentication steps depend on the selected harness.

See [project progress and task handoff](project-progress.md) for the goals, decisions, commands, state, and evidence needed after account access has been restored.

## Use operator evidence to narrow the incident

After reconnecting, inspect original process identities, last heartbeat, exit or guard status, and output completeness. Compare boot and container start identities to distinguish changes in the host and container.

Give operators a bounded incident window and the relevant node and container identifiers. Obtain the probe type, timeout sequence, and resulting platform action for health-check incidents. Obtain the affected CPU and call path for watchdog incidents. Inspect OOM and resource-pressure events for resource incidents. Align platform evidence with application submission, execution, creation, exit, and wait observations.

Keep candidate causes tied to their evidence. Establishing a lock instance or holder requires observations that identify it directly.

## Make protection events replayable

Bind launch and exit timers to a probe ID. Check active phase age and completed phase duration. Inspect every adjacent heartbeat interval as well as the age of the newest sample. Replay failure records to establish detection and success records to inspect false positives.

On a protection event, preserve the run and stop the affected workload under the agreed policy. Recheck host health and any independent task's progress before deciding whether it can continue. Partial output requires its own coverage and provenance acceptance.

## Overlap CPU and GPU work deliberately

Establish independent resource and timing baselines. GPU work also uses host CPU, memory, and storage. Gate an inserted workload on progressing workers, actual device activity, and a sustained healthy host window. Recheck before each wave and monitor throughout execution. Evaluate the total time to both accepted outputs.

The D-cluster case used particular readiness windows and protection limits. Its first staggered wave passed and its second wave exceeded the launch limit. See [the protection case](../cases/protection-controller/README.md) for the resulting applicability limits.
