# IPR 的 trace、线程创建与调度

IPR 的长尾由多个 JVM、Java worker、消息队列和 native 工具共同构成。只观察顶层 CPU 占用无法区分消息排队、搜索和退出等待。按 step execution、消息与 consumer 身份连接日志，再用 PID 和启动 tick 连接实际子进程。

PANTHER 分块之后，一份任务仍曾提交约 66 分钟后才开始，前面同一 worker 在运行 Gene3D。定向 broker 日志补出分派和领取信息，之后采用依赖约束下的关键路径调度与预取 0。同批 4×8 作业墙钟从 5414.25 秒降到 4610.76 秒，InterPro ID 与完整 PANTHER match 都有 1,000/1,000 一致。该实验的调度与预取共同改变。

另一条诊断链发现 `hmmsearch --cpu 0` 后，pfscanV3 和 HAMAP 仍贡献大量线程创建。对实际混合负载进行入口插桩后，单独限制 pfscanV3 使其创建从 283,648 降到 1,108，完整 match 保持一致。采到的 percpu 等待仍存在，需要单独追踪锁和重启证据。

加速配置继续用于千条复测和全量注释，但不同配置的同输入结果保留差异。模型完整分块、执行完整和数值等价性分别验收。当前分块与原全库的三条计分 ID 差异，以及低复杂度输入改变搜索成本，都保留在 [原进度](../../../../agent-progress/acceleration/details/ipr-acceleration.md) 中。

两个改进节点见 [case.json](case.json)。采集与离线分析流程见 [CPU 诊断](../../references/cpu-diagnosis.md)，线程归因见 [真实混合负载对照](../../../../experiments/acceleration/ipr-debug-real-activity-A.i62m9jz0/analysis/pair_comparison.md)。
