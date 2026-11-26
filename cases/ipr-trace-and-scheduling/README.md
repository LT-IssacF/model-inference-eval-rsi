# IPR tracing and scheduling

IPR combines JVMs, Java workers, message queues, and native tools. The investigation connected step execution, message and consumer identity, and subprocess observations to distinguish queue delay from actual search time.

After PANTHER partitioning, one submitted search still waited about 66 minutes while its eventual worker ran Gene3D. Directed broker logging added dispatch and receipt evidence. A later comparison changed critical-path scheduling and prefetch together. Its same-input 4-by-8 workload fell from 5414.25 to 4610.76 seconds, with 1,000 of 1,000 matching InterPro ID sets and complete PANTHER matches.

Native counters exposed another cost. After HMMER thread creation had been reduced, pfscanV3 and HAMAP still contributed many creation calls. In the mixed workload, limiting pfscanV3 reduced its calls from 283,648 to 1,108 while complete annotation matches remained consistent. Sampled lock waits still occurred, so thread creation and restart causality required separate evidence.

The methods were adopted in later search and protection experiments. Partition coverage, successful execution, and equivalence to an original full-library configuration remain separate acceptance questions.

See [case.json](case.json) for the two records and [CPU diagnosis](../../references/cpu-diagnosis.md) for the reusable process. The release carries numerical queue and tool-attribution observations in [evidence.json](../../evaluations/evidence.json).
