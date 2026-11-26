# Evaluation correctness

Freeze the original data, predictions, parsing policy, metric implementation, and reference database identity. Identify the generation checkpoint and each scoring model separately. Define units, eligible inputs, total slots, candidate keys, empty values, and length handling before comparing results.

Verify every expected slot by key. Reject duplicate, missing, and misaligned records. Deduplicated computation must restore occurrence weights when results are mapped back. The validity denominator includes invalid slots. Other metrics use their declared eligible population. Preserve the identity of text conventions, length filters, and historical summaries.

Combine stage exit status, source and output fingerprints, code and configuration provenance, item-level coverage, and recomputed aggregates. Interpret a `passed` field within the scope it checks. A valid state audit, a completed wave, and a complete evaluation can have different outcomes.

Keep original values and native failure records when sentinels, NaNs, or out-of-range results appear. Normalize an identified placeholder only under an explicit rule, then validate the eligible records. For historical implementation behavior, retain anomaly counts and a declared primary comparison field. A formula change needs its own versioned result.

State whether a result covers candidates, a seed, a subset, or the full dataset. A reproduced subset validates that scoring path under its conditions. A new model or dataset size still needs its own provenance and coverage checks. See [Design standardization](../cases/design-standardization/README.md).
