# Evidence checks and method evaluation

This release includes executable checks of archived evidence and a development task suite. The controlled agent comparison and held-out transfer evaluation have status `not_run`.

## Check archived evidence

Run `python3 scripts/check_repository.py` from the repository root. The bundled `evidence.json` holds selected observations and their source fingerprints. `checks.json` defines assertions about those observations. Add `--project-root /path/to/ProteinArena` to verify the original source bytes and extracted fields.

The checker validates the scope of the recorded conclusion. A failed experiment is a valid regression expectation. For example, the second staggered IPR wave must retain its failure status when the final state audit passes.

[repository-check.json](repository-check.json) records the release check. [checker-regression.json](checker-regression.json) covers a portable copy, evidence modification, cyclic lineage, a false success assertion, and source drift.

## Development tasks

[tasks.json](tasks.json) supplies task prompts, evidence, and expected output form. [rubric.json](rubric.json) supplies reviewer criteria. The tasks cover GPU adoption, queue diagnosis, protection logic, mixed-workload acceptance, recovery, and metric population differences. They derive from cases already used to write this Skill.

To compare methods, freeze the task package, input fingerprints, model and runtime, tools, time or token budget, and allowed side effects. Give both conditions the same raw task material. Give the candidate condition the selected Skill and tools as well. Preserve outputs, tool calls, elapsed time, resource use, human corrections, and failure reasons. Apply the same rubric and report correctness, cost, and stability together.

## Held-out transfer

Freeze a separate task package from work that did not inform this Skill. The reviewer retains expected answers and grading fields. The agent receives the material needed to complete the task. Run both conditions with comparable authorization and budgets in separate output directories.

Use subsequent failures to add an improvement record, change the responsible artifact, and replay affected development tasks. Freeze the transfer package before testing a new version. Report actual outcomes before claiming a measured method improvement.
