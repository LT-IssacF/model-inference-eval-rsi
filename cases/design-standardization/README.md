# 从性能实验到标准 Design 评测

标准评测把优化得到的执行器接到固定数据、候选槽位和指标定义上。870 题与三个 100 题子集各有明确范围，输入、预测、配置和输出用来源与哈希关联。去重后的计算结果按候选出现次数回填，再从逐槽分数计算主指标。

全量 pLDDT 有 4,862 条不同有效序列，合并缓存额外包含一个空响应 NaN 哨兵。原生覆盖检查报告失败，定向验收只在内存副本中剔除这个已知空项，再核对全部 8,692 个有效候选。原生检查的状态与归一化边界同时保留。

旧模型三 seed 的后续复测沿用固定序列。有效候选 Repeat 与历史逐条记录一致，但旧总表包含超长候选，分母不同造成均值差异。文档 ProTrek 的 InterPro 功能文本与另一种 problem 文本分别标识。文档 ProTrek 和完整库序列 Novelty 的逐项重跑与历史同口径精确一致。Easy 越界按旧公式保留，Hard 用于主结果。

这条链改进了执行结果的解释与接续条件。新模型或新规模仍需要自己的生成来源和逐项验收。机器记录见 [case.json](case.json)，原始证据见 [全量 pLDDT 验收](../../../../experiments/d-standard-eval/step3300-plddt-ipr/plddt-acceptance.json) 和 [三 seed 复测报告](../../../../experiments/d-standard-eval/legacy-seeds-remaining-20261125/report.md)。
