# 394｜本轮详细行动记录：RPv4 S0/S1科学冻结与角色量化

**日期：** 2026-10-11
**阶段：** `V4_S0_S1_BASELINE_FREEZE_CLAIM_ROLE_TRANSITION_AND_AVAGLIO_A2_PREFLIGHT`

## 1. 本轮输入

- RPv4正式MD/DOCX；
- Q2-R5候选稿、22对象主表、27/23/13历史结果表及来源审计表；
- Q2-R3 AVAglio代码、结果、metadata、census和349行源输入；
- TRIO 110行公开身份台账和10项原始主张台账；
- 28行历史对象inventory及RCC04/05候选来源链。

共冻结 **18** 个基线对象；所有文件记录绝对路径、字节数和SHA-256。

## 2. 实际执行

1. 独立计算所有冻结输入SHA-256，保留历史文件不改写。
2. 核对22个 `claim_estimand_id` 与RPv4固定对象集完全一致。
3. 建立22行角色迁移台账，分别记录原始用途、原始结论、证据设计、实现来源、人群、随机性、估计量、历史角色、当前角色和重跑必要性。
4. 建立双分类器A0–A4共10行模型登记表；A2保持空白结果。
5. 对AVAglio源输入只做行数、字段、编码、缺失规则和事件数预检；没有调用Cox拟合。
6. 验证TRIO 110行均为assignment phase UNKNOWN，且corrected randomized release均为NO。
7. 冻结A2诊断、停止及全报告规则。

## 3. 关键结果

- 角色表：22/22完整；角色分布 `{"POPULATION_UNVERIFIED": 10, "ROLE_REFRAMED": 7, "NOT_CURRENTLY_EVALUABLE": 2, "TARGETED_REANALYSIS": 2, "IMPLEMENTATION_LIMITED": 1}`。
- 15项有历史本地数值对象与7项来源审计对象均保留，未改变对象集合。
- A0/A1/A3/A4历史结果保留；A2是唯一未执行增量模型。
- A2预检：14/14 PASS；n=333，events=260。
- A2结果列为空；本轮无新HR、CI或P值。
- TRIO没有任何患者级阶段猜测。
- 历史27、23、13三个结果层未混合成新的统一分母。

## 4. 本轮发现并修正的表达风险

旧材料把333行简称为“complete case”。代码级核对表明，冻结规则实际是：在339名IDH1-WT参与者中排除6名至少一个来源协变量为字面值`NA`者，同时保留70个MGMT=`Missing`记录。因此本轮将其精确命名为“fixed six-row literal-NA source-covariate availability set”。这不改变患者集合或既有A3数值，只纠正方法表述。

## 5. 未执行及原因

- 未拟合A2：S0/S1的职责是预分析冻结，避免把结果反向写入规则。
- 未重跑其余历史模型：没有输入、公式或模型改变。
- 未开展TRIO纯随机纠正：缺少权威参与者级阶段映射。
- 未更新GitHub、未投稿、未生成新主图。

## 6. Gate

`READY_FOR_V4_S2_TARGETED_AVAGLIO_A2_EXECUTION__TRIO_IDENTITY_BRANCH_REMAINS_EVIDENCE_GOVERNED__HOLD_SUBMISSION`

## 7. 下一阶段

仅执行已冻结的两个A2模型及其预定诊断，生成A0–A4同口径结果与模型差异表；无论A2显著与否全部报告。下一阶段不得增加协变量、改变333行集合或据结果选择分类器。
