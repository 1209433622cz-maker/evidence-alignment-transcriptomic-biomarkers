# 400｜下一阶段目标：V4-S2 AVAglio A2定向执行与模型梯度诊断

**阶段：** `V4_S2_TARGETED_AVAGLIO_A2_EXECUTION_AND_MODEL_LADDER_DIAGNOSTICS`

## 唯一新增拟合

在冻结的333行分析集上，分别对Phillips和Verhaak deposited subtype labels拟合：

`OS ~ marker + treatment + marker×treatment`

不含协变量、不加惩罚、不替换患者。

## 必须输出

1. 两个A2模型的n、事件数、beta、SE、HR、95% CI和P值；
2. 收敛、Schoenfeld PH和interaction DFBETA诊断；
3. A0–A4十行统一结果表；
4. A1→A2（固定样本限制）与A2→A3（同一333行上的调整）差异表；
5. 输入、脚本、输出SHA-256及独立复算；
6. 无论方向或显著性如何全部报告；
7. 本轮详细行动记录及新Go/No-Go。

## 禁止事项

- 不更改333行集合；
- 不新增协变量或选择性删除影响点；
- 不把A2显著性解释为独立验证；
- 不用A2覆盖历史A0/A1/A3/A4；
- 不同时启动TRIO猜测性随机子集；
- 投稿与GitHub同步继续HOLD。

## 通过后的判断

若A2及诊断完整，进入V4-S3 TRIO可识别性终局确认，并同时评估完整22对象论文与TRIO/AVAglio双案例收缩路线；若A2不可估，按预设停止规则保存失败原因，仍可进入以“可识别性与来源对齐”为主的收缩路线评估。
