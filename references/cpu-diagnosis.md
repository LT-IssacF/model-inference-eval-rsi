# CPU 诊断、trace 与调度

同时记录顶层进程、worker、native 子进程、实际线程参数和启动速率。CPU 配额、活跃进程数、线程存量与创建速率用于描述不同的成本。先确认实际命令和工作量，再判断全局并发是否有收益。

## 按问题增加 trace

1. 找到慢分片或慢组件。采 Java 步骤或任务提交、开始、完成事件，配合 native 进程树的 CPU、RSS、状态和等待点。用 PID/TID 及启动时间区分任务身份。
2. 把排队、执行和下游合并画在同一时间轴。比较 native wall 与 CPU 时间，检查采样间隔、缺行及未配对事件。首末快照跨度说明观测到的区间，估算等待时标注采样边界。
3. 提交到执行有长间隔时，按 execution ID、消息 ID、consumer ID 补队列分派和领取记录。核对预取、在途任务和依赖。调度改进保持任务依赖与实际资源上限，重测其他组件是否接替长尾。
4. 短命进程和大量线程创建用实际调用入口或计数补证，保留调用、返回、错误及时间窗。节点总体计数有背景负载，容器与具体工具的归因需要身份和时间对齐。

IPR 的既有入口是项目 `scripts/ipr_length_parallel.py` 的 `--trace-masters` 与 `--trace-interval`，单分片使用 `ipr_worker_benchmark.py --trace-interval`。日志为 `interproscan.log` 和 `process_trace.jsonl`。`analyze_ipr_trace.py` 生成汇总和 Perfetto 时间线，broker 日志再细分提交后的长等。嵌套包装器的子进程事件与持续心跳支持中断复盘。对照入口、配置和样例见 [IPR 案例](../cases/ipr-trace-and-scheduling/README.md)。

在 ProteinArena 项目根目录，对已经归档的 case 可执行 `python3 -B scripts/analyze_ipr_trace.py CASE_DIR --output-dir ANALYSIS_DIR`。先检查输出的起止配对、最大采样间隔和缺行，再看 `java_queue_wait`、`java_step`、`process_sampled`。普通提交时间字段可能只有整秒精度，分派时刻需要定向 JMS 日志。当前采样器以 `PROTEIN_ARENA_IPR_CAPTURE_D=1` 开启线程 D 状态记录，项目特定的 Log4j2 配置由 `PROTEIN_ARENA_IPR_TRACE_CONFIG` 指定。启动新诊断实验时结合项目现有受保护入口使用这些参数。

## 性能与结果一起验收

改变分片、模型分块、线程模式或应用裁剪时，核对完整模型和输入覆盖、实际命令、版本、合并顺序及逐项结果。分数集合与完整注释可以有不同一致性。总条数之外还记录总长度、长度分布、去重率和组成特征，跨输入差异可用于提出假说。

trace 和同步写盘会影响调度与执行，记录采集条件，用有限的定向日志回答具体问题，再衡量开销。保留数据不支持的归因和权限缺口。
