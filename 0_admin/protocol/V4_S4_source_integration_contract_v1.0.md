# RPv4 V4-S4｜支持性结果分层与 Figure Source Freeze 合同 v1.0

**冻结日期：** 2026-10-11（派生表生成前）  
**阶段：** `V4_S4_SUPPORTIVE_RESULT_TRIAGE_AND_FIGURE_SOURCE_FREEZE`

## 1. 目标

将 V4-S0/S1 的 22 对象角色、历史 27 个主模型、23 个 absolute-effect 模型、13 个跨试验历史单元、V4-S2 的 AVAglio A0–A4 当前模型梯度和 V4-S3 的 TRIO 可识别性边界整合为稿件与 Figure 1–4 可消费的冻结源表。

本阶段不改变对象、主要标签、模型结果或既有历史文件，也不以增加统计分析为成功标准。

## 2. 输入版本

| 输入 | SHA-256 | 版本角色 |
|---|---|---|
| `published_predictive_claim_inventory_28rows.tsv` | `345767aac30a983fbeff0be596b3770dc57cb5c04b0c9da9995229e6ff3318dd` | 历史 28 candidate universe，只读 |
| `V4_claim_role_transition_22.tsv` | `afd26f...62d5` | S0/S1 当前对象角色 authority |
| `V4_selected_object_lineage.tsv` | `499e81...9eb7` | 28→22 对象谱系与 local-numeric 标记 |
| `Table2_local_IPD_primary_interactions_27rows.tsv` | `86d0ca...02ac` | 历史 27 模型只读快照 |
| `strict_denominator_provenance_crosswalk.tsv` | `56fc54...1542` | 历史 13 单元标签，只读 |
| `binary_absolute_effect_23models.tsv` | `cb3829...2bab` | 历史 23 absolute-effect 结果 |
| S0/S1 `V4_AVAglio_A0_A4_model_registry.tsv` | `490776...1124` | 计算前 registry 快照，A2 空值合法 |
| S2 `V4_S2_AVAglio_A0_A4_model_ladder.tsv` | `25ba4b...b101` | 当前派生 AVAglio 梯度 authority |
| S3 `V4_S3_TRIO_10object_role_update.tsv` | `382047...0061` | TRIO 对象传播 authority |
| S3 `V4_S3_TRIO_arm_phase_eligibility.tsv` | `522e6c...ee43` | TRIO 设计层/字段层分离 |
| S3 `V4_S3_TRIO_aggregate_compatibility_bounds.tsv` | `d030ad...f947` | 条件整数相容范围 |
| Q2-R2 13 单元当前重分类 | `b97cc9...27dd` | 当前 verified-strict 资格 authority |

完整哈希由 pre-execution JSON 和 source manifest 保存；上表为便于人工阅读的缩写。

## 3. 权威层级

发生字段冲突时按以下优先级处理：

1. RPv4 后续阶段已验收派生表（S2、S3）；
2. S0/S1 role transition 与 object lineage；
3. Q2-R2 当前资格重分类；
4. 历史 27/23/13 行文件，仅作为历史数值和标签快照。

历史表不得被静默覆盖。

## 4. 两个 P0 版本隔离规则

### 4.1 严格复制分母

S4 新表必须同时存在：

- `historical_strict_denominator_member`
- `current_verified_strict_denominator_member`

旧表的 13 个 `True` 只描述历史体系；当前 13 个单元均为 `False`。当前严格复制比例为 `NOT_ESTIMABLE`，不得写成 0/13、0% 或新的分母。

### 4.2 AVAglio A2

S0/S1 registry 的 A2 空值保持不变，标记为历史 pre-execution snapshot。S4 另建 derived current table，从 S2 ladder 引用 A2 结果并保存 source hash。不得反写旧 registry。

## 5. 冻结行数和不变量

- 22 个唯一 `claim_estimand_id`；原 primary label 修改数 0；
- 15 个 local-numeric 对象、7 个 source-audit 对象；
- 27 个历史主模型：TRIO 10、CHER-LOB 10、AVAglio 2、GLARIUS 2、BrighTNess 2、DOP 1；
- 23 个 absolute-effect 模型；
- 13 个历史跨试验单元、3 个 dependency clusters；
- 两个 AVAglio classifier 各 A0–A4 五行；
- 10 个 TRIO 对象继续 `POPULATION_UNVERIFIED`；
- RCC_04/05 继续 `NOT_CURRENTLY_EVALUABLE` 且 provenance open；
- TRIO 模拟继续取消；不创建患者级阶段映射。

## 6. 图件数据契约

- Figure 1：28、22、15、27 是不同计数单位，不画 PRISMA；展示 TRIO 解释资格变化与 AVAglio 数值重建两条纠错路线。
- Figure 2：22 对象的主张、实现、人群、估计量和 current role 分维展示；禁止 composite score。
- Figure 3：AVAglio 349→339→333 及 A0–A3；A4 作为替代规格分支，不伪装成单因素递进。
- Figure 4：13 个历史单元与 3 个依赖簇；同时显示历史成员资格和当前 verified-strict 不可估边界。

S4 只冻结 source tables、panel mapping 和文字语义；最终主图在 V4-S5 生成。

## 7. 停止规则

除非输入、人群、评分实现或模型规格真正改变，否则不重跑历史模型或 bootstrap。不开展 TRIO 模拟，不增加疾病、标志物、阈值或分母。
