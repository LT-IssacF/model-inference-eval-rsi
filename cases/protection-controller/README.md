# 从中断恢复到可重放的保护控制器

CPU 压力实验发生过容器中断，应用日志在中断后难以恢复。项目用持久 `.chat` 交接和用户维护的 `recover` 环境入口保留接续信息，记录 boot ID、PID 1、最后心跳和输出位置。运维的 liveness 连续超时事件缩小了排查时间窗，再与应用等待、创建和退出记录对齐。

首次 pLDDT/IPR 同时启动时，代理 launch 有五次超过 5 秒，heartbeat 有三段超过 5 秒。旧控制器的中间事件会刷新 launch 计时，新 heartbeat 也可能掩盖历史长间隔。实际运行由人工停止。

控制器修复后，按 probe ID 保留阶段起点，检查活动阶段与已完成耗时，逐条检查 heartbeat 历史间隔。回归重放检出原失败轮全部八项超时，原成功轮通过。随后独跑两波全量 IPR 正常完成，保护事件为零。

错峰复测继续采用修复后的保护，第一波通过，第二波 launch 超过阈值时自动停止。pLDDT 在主机恢复并确认健康后继续完成。最终核对通过，而全量并跑实验仍失败。它提供了保护产物被后续任务采用的直接证据，同时限制了“初始化结束后即可稳定并跑”的假说。

三个节点见 [case.json](case.json)，相关原始报告为 [同时启动](../../../../experiments/d-standard-eval/step3300-full870-plddt-ipr-concurrent-8gpu-8x8/concurrent-report.md)、[修复与独跑](../../../../experiments/d-standard-eval/step3300-full870-ipr-standalone-recheck-8x8/standalone-report.md)、[错峰复测](../../../../experiments/d-standard-eval/step3300-full870-plddt-ipr-staggered-8gpu-8x8-wave01/staggered-report.md)。恢复和运维方法见 [故障恢复](../../references/recovery.md)。

恢复方法还包括开跑前由用户私密备份账户访问材料，以及新 harness 会话读取项目进度后接续任务。见 [账户恢复](../../references/recovery.md) 与 [项目进度](../../references/project-progress.md)。
