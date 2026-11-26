# pLDDT on C550

The ESMFold investigation began with slow execution after hardware migration. Profiling connected the observed workload to triangle attention, explicit bias operations, softmax, and matrix multiplication. Kernel experiments used matched shapes and synchronized timing, followed by a same-input 50-candidate ablation and three 1,000-candidate runs.

The 50-candidate bucketed baseline took 1105.84 seconds. The batch-safe single-device path took 456.80 seconds. Eight devices with an in-memory model copy took 113.313 seconds. The latter step changed device count and model-cache location together.

Complete-model measurements constrained which operator changes were adopted. The selected configuration uses IEEE FP32 fused attention and Triton LayerNorm. Hardware-specific operator behavior and failed optimization candidates remain part of the experiment archive.

Aggregate agreement did not eliminate numerical tails. Maximum candidate-level differences across the three seeds were 2.178, 3.466, and 2.949 points. A seed1 fallback brought 999 of 1,000 candidates within 0.30 points, with the remaining boundary linked to the historical PDB cache path.

The three improvement records are in [case.json](case.json). [Evidence snapshots](../../evaluations/evidence.json) retain timing and numerical observations plus the selected precision and kernel flags. Full migration and ablation records remain in the ProteinArena archive under `agent-progress/acceleration/details/plddt-acceleration.md`.
