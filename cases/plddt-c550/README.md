# pLDDT 在 C550 上的性能与数值

ESMFold 迁移到 C550 后，实际 trace 把 triangle attention 的矩阵乘、显式 bias 加法和 softmax 连到性能瓶颈。优化先用匹配形状同步计时，再在同一批 50 个候选上消融，并用三组千候选验证数值。

同批 50 条从非 Triton 长度分桶的 1105.84 秒降到 batch-safe 单卡 456.80 秒。八卡与内存盘组合为 113.313 秒，该步同时改变设备数量和权重缓存位置。多卡分片按精确序列去重，以截断后长度的非线性成本均衡，各卡独立缓存，再回填候选。

triangle BMM 重排曾改善子图时间，但完整模型变慢。attention TF32 dot 收益很小且误差增大，最终采用 IEEE FP32 融合注意力和 Triton LayerNorm。相同 kernel 在 H200 的收益也随基线发生变化，跨硬件需要重新测量。

三 seed 汇总接近旧实现，逐候选最大差仍达 2.178、3.466、2.949 点。seed1 回退离群候选后 999/1,000 落入 0.30 点范围，余下一条关联旧 PDB 缓存边界。逐候选验收随后用于全量 Design，成为性能修改的采用条件。

本案例的三个节点见 [case.json](case.json)。小型数值快照见 [证据索引](../../evaluations/evidence.json)。原始解释见 [pLDDT 进度](../../../../agent-progress/acceleration/details/plddt-acceleration.md) 和 [原验收记录](../../../../ACCELERATION_ACCEPTANCE.md)。
