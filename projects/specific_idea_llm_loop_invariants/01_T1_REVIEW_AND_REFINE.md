# T1 审查与修复记录

阶段：S8　审核日期：2026-09-14 15:18:17　复审轮次：第 1 轮

## 逐卡判定

| 卡 ID | 审查项目 | 状态 | 证据位置 | 评估与理由 |
| --- | --- | --- | --- | --- |
| S8-C1 | 论文主线解释知识增量 (Narrative Explains Knowledge Increment) | **MET** | 手稿 Abstract, §1 Introduction (The Invariant Synthesis Bottleneck & Our Contributions) | 引言与摘要清晰交代了领域传统做法（Houdini/ICE 语法模板爆炸、抽象解释凸包过近似精度损失）与直接使用 LLM 生成不变量的根本障碍（表面 trace 看起来正确但缺失辅助约束导致 70%+ consecution 失败、以及向 LLM 喂入反例导致语义震荡），并明确指出本工作提供的认知转变：通过解耦核心不变量与辅助关系，并引入前向可达性滤波消除不可达虚假反例，将 BMC 不变验证解耦至常数阶。 |
| S8-C2 | 每个主要主张有范围匹配的证据 (Claims Match Evidence Scope) | **MET** | 手稿 §1 Contributions, §4.1-§4.3, §4 Limitations & Open Challenges | 所有主要论断均被严格限定在实验支持的有效范围内。主张明确限定在 ANSI-C 标量整数循环（SV-COMP 120 个任务）、线性整数算术（LIA）与 $k \in [50, 1000]$ 范围。手稿第 4 节明确排除了非线性整数算术（NIA）、指针别名与堆内存结构，并承认了 $k=10$ 滤波的不完备性，未发现超越实验范围的普适性夸大断言。 |
| S8-C3 | 数字、方法与证明相互一致 (Consistency Across Numbers, Text & Proofs) | **MET** | 手稿 Abstract, §4.2 Table 1, §5.1, §5.2 Table 2, §3 证据追溯索引 | 全文关键数字高度一致：基准总数 120 个；IPSR 78.3% (94/120)；首轮 Consecution 失败 87/120 (72.5%)，其中虚假不可达状态占 72.4% (63/87)；滤波前向抑制后震荡率由 48.3% (42/87) 降至 6.9% (6/87)；常数耗时 1.84s 以及内存削减 94.2% 在摘要、正文表格、消融分析与追溯索引中勾稽完全一致。 |
| S8-C4 | 相关工作与引用准确 (Accurate Citations and Fair Related Work) | **MET** | 手稿 §6 Related Work | 客观准确评述了经典 BMC 展开与 CBMC、经典不变量合成工具（Houdini, Daikon, ICE, Code2Inv）以及近期基于 LLM 的形式化不变量工作（Ryan et al., 2024; Pei et al., 2023）。清晰指出了现有 LLM 不变量生成处理 raw 反例时的震荡瓶颈，划定了前人贡献与本工作（引入前向可达性滤波进行真伪反例解耦）的创新分界线，无贬低或冒领情况。 |
| S8-C5 | 可复查性与局限完整 (Reproducibility and Transparent Limitations) | **MET** | 手稿 §3 证据追溯索引, §4 局限性说明, §5 T5 增补 §9-§10 | 可复现性与局限性披露详尽且诚恳。明确披露了工具链版本（CBMC v5.95.0, Z3 v4.12.2, Python 3.11）与硬件配置，给出了各表项对应的复现脚本与日志文件位置；第 4 节深度剖析了 NIA 引发求解器 unknown/超时的失效场景（8.1%）、$k=10$ 前向滤波因深度不足误判伪反例的不完备性，以及指针/动态堆未覆盖等核心局限。 |
| S8-C6 | 关闭的是实质问题 (Substantive Problem Closed) | **MET** | 手稿 Abstract, §1, §4.3, §7 Conclusion, §5 T5 增补 §8 | 交付成果完全回应了 S1 设定的核心问题：解决了 BMC 在面对大步长/无界循环展开时的状态爆炸瓶颈，克服了 LLM 产生非归纳断言及伪反例引发震荡的失效模式。在 120 个真实基准测试中将验证时间从标准 BMC 的 312.4s/超时缩减至常数阶 1.84s，切实推动了循环展开绕过这一关键问题的解决，闭环了最初承诺。 |

## 阻塞问题与发现 (Issues)

本轮无阻塞 Issue，所有适用卡项符合标准。

## 本轮结论与决策

- **转移动作**: **CONTINUE**
- **目标阶段**: 完成
- **决策理由**: All S1-S8 stages successfully completed. Research paper and audit finalized.
