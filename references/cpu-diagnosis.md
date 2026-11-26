# CPU diagnosis and tracing

Track top-level processes, workers, native subprocesses, actual thread options, and creation rates. CPU quota, concurrent processes, resident threads, and thread creation rate describe different costs. Confirm the executed commands and input workload before increasing concurrency.

## Add instrumentation to answer a specific question

1. Locate the slow partition or component. Capture task submission, start, and completion events alongside native CPU time, RSS, process state, and wait channels. Identify tasks with PID or TID plus process start time.
2. Align queueing, execution, and downstream collection on one timeline. Inspect sampling gaps and unpaired events. A first-to-last sampled interval has observation boundaries that must be retained in the interpretation.
3. For long submission-to-start delays, correlate execution IDs, message IDs, and consumer IDs across dispatch and receipt. Inspect prefetch behavior, in-flight work, and dependencies before changing scheduling.
4. Add launch-site events or native counters for short-lived tools and creation bursts. Preserve calls, returns, errors, and time windows. Node-level counters include background work, so component attribution needs aligned identity and timing evidence.

In ProteinArena, `scripts/ipr_length_parallel.py` selects traced masters with `--trace-masters` and sampling with `--trace-interval`. Individual cases contain `interproscan.log` and `process_trace.jsonl`. Analyze an archived case from the project root with `python3 -B scripts/analyze_ipr_trace.py CASE_DIR --output-dir ANALYSIS_DIR`.

Inspect pairing statistics and sampling gaps before interpreting `java_queue_wait`, `java_step`, and `process_sampled` tracks. The ordinary submission field can have one-second precision. Directed broker logs provide dispatch and receipt detail. The project sampler accepts `PROTEIN_ARENA_IPR_CAPTURE_D=1` for blocked-thread observations and `PROTEIN_ARENA_IPR_TRACE_CONFIG` for a selected Log4j2 configuration.

## Validate changes in scheduling or native execution

Preserve dependencies and resource limits when changing queue order. After a change, measure whether another component becomes the tail. Verify full model and input coverage, actual command options, versions, merge order, and item-level results when changing partitioning, thread modes, or component selection.

Report sequence count, total residues, length distribution, deduplication, and relevant composition features. Differences between input batches can motivate a hypothesis. A causal estimate needs an appropriate controlled comparison.

Trace collection and synchronous logging can affect execution. Record the collection setup and measure its overhead. The [IPR case](../cases/ipr-trace-and-scheduling/README.md) shows queue diagnosis and tool-level creation attribution.
