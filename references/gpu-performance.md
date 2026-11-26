# GPU performance

Measure startup, weight loading, host-to-device transfer, warmup or compilation, steady-state execution, and output collection separately. Record hardware, driver, framework, precision, batch shapes, and model-cache state. Observe host CPU, memory, and I/O while devices initialize.

Profile the actual model path before selecting a kernel target. Use matched shapes and precision for operator experiments. Synchronize device timing and state the warmup procedure. Measure normal execution separately from profiler overhead. Confirm which operators the runtime actually dispatches.

Balance work using the model's effective input length and padding behavior. Deduplicate computation where allowed, retain the original occurrence map, and reconstruct slot-level results. Give workers independent outputs and verify their coverage. Isolate device visibility when the runtime requires one device per process.

Evaluate operator time, complete-model time, numerical differences, and errors together. A faster operator can move the critical path or increase other costs. Keep the end-to-end results of rejected changes. Numerical acceptance should include the mean, tails, maximum difference, outliers, and undefined values under the user's agreed tolerance.

Use [the C550 case](../cases/plddt-c550/README.md) for an example of measured kernel gains, workload balancing, and numerical limits.
