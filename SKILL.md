---
name: model-inference-eval-rsi
description: Improve the artifacts used for model inference and evaluation through evidence-based performance diagnosis, recovery, correctness checks, and feedback from later tasks. Use for GPU or CPU bottlenecks, mixed-workload scheduling, incident investigation, and evaluation-method development.
---

# Improve inference and evaluation artifacts

Establish the requested outcome, inputs, resources, metric definitions, numerical tolerances, and authorized actions. Read the current project's progress records before applying a historical method.

| Current problem | Reference |
| --- | --- |
| Slow inference, kernel changes, device imbalance | [GPU performance](references/gpu-performance.md) |
| CPU tails, queues, native tools, thread creation | [CPU diagnosis](references/cpu-diagnosis.md) |
| Unresponsive tasks, account recovery, probes, overlapping workloads | [Recovery](references/recovery.md) |
| Long tasks, fresh sessions, interrupted work | [Project progress](references/project-progress.md) |
| Score drift, denominators, deduplication, slot alignment | [Evaluation correctness](references/evaluation-correctness.md) |

## Work from observations to a verified change

1. Freeze a comparable baseline. Identify preparation, startup, warmup, computation, queueing, and collection costs. Prefer existing evidence before adding instrumentation.
2. Choose a change that tests a specific hypothesis. State the expected benefit and the correctness or stability properties it could affect. Adapt parameters to the present workload and the user's resource choices.
3. Preserve commands, identities, source fingerprints, outputs, and exit status in an independent run directory. Before experiments that can interrupt the environment, have the user preserve harness account access in durable private storage and keep direction progress, a current handoff, and run evidence in the consuming project. After account recovery, read those records and verify task state before continuing.
4. Verify item-level coverage, values, and occurrence weights. Then compare end-to-end time and resource use. State the assumptions behind simulations and comparisons across different inputs.
5. Observe adoption in a later authorized task. Record counterexamples and update the tool or method responsible for a demonstrated error. Add a replay or acceptance check that detects that class of error.

## Record the improvement

Use the case record fields `id`, `parents`, `problem`, `observation`, `artifact_change`, `validation`, `adoption`, `limits`, and `evidence`. A change can be `validated_in_scope`, `rejected`, `partial`, or `proposed`. Keep rejected changes and scope limits attached to the lineage.

Capture small observations in `evaluations/evidence.json` with source paths, source SHA256 values, selected fields, and snapshot SHA256 values. Run `scripts/check_repository.py`. Supply `--project-root` when the original archive is available. Assertions should concern actual result properties such as coverage, failure status, or numerical differences.

Historical cases support development and regression checks. To measure whether a method improves an agent's later work, use the [evaluation protocol](evaluations/README.md) with frozen tasks, comparable tools and budgets, and a separate record of observed outcomes.

## Make the evidence readable

Explain the task, execution flow, difficulty, change, validation, and later adoption in each case narrative. For complex work, a visual overview and filterable timeline can connect device activity, CPU tasks, protection events, and platform incidents. Label observations, hypotheses, and missing evidence. Generate presentation data from the same verified artifacts.
