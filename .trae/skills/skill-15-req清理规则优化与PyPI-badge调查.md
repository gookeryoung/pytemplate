# skill-15：req 清理规则优化与 PyPI badge 调查（归档自 iter-15/req-15）

## 迭代目标

1. 分析 `.trae/req` 和 `.trae/docs` 未按 rule-01 定期清理的原因，优化规则为阈值触发式清理。
2. 调查 README.md 第 6 行 PyPI badge 未及时更新标签的原因。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `.trae/rules/rule-01-开发流程.md` | 修改 | "每 5 次迭代后清理" → "阈值触发：文件数 ≥ 5 时归档至 ≤ 4" |
| `.trae/skills/skill-07-bump目标默认patch.md` | 新建 | 归档自 iter-07/req-07 |
| `.trae/skills/skill-08-移除项目Dockerfile支持.md` | 新建 | 归档自 iter-08/req-08 |
| `.trae/skills/skill-09-修复Node20弃用警告.md` | 新建 | 归档自 iter-09/req-09 |
| `.trae/skills/skill-10-项目问题修复与优化.md` | 新建 | 归档自 iter-10/req-10 |
| `.trae/skills/skill-11-CLI子命令重构.md` | 新建 | 归档自 iter-11/req-11 |
| `.trae/docs/iter-07~11` | 删除 | 已归档至 skill-07~11 |
| `.trae/req/req-07~11` | 删除 | 已归档至 skill-07~11 |

## 关键决策与依据

### 1. req/docs 未定期清理根因

历史清理记录不一致：
- iter-05：归档 iter-01~04（4 个，5 倍数触发）
- iter-10：归档 iter-05（1 个，5 倍数触发但只归档 1 个）
- iter-12：归档 iter-06（1 个，非 5 倍数，偏离规则）
- iter-13/14/15：未清理

根因：
1. "每 5 次迭代后清理" 语义模糊：5 的倍数触发 vs 间隔 5 次触发
2. "仅保留最近未归档的记录" 无明确数量阈值
3. 一次归档多少不明确
4. 无强制触发机制

### 2. 阈值触发方案

用户授权选择阈值触发方案：
- 触发条件：`docs/` 或 `req/` 文件数 ≥ 5
- 归档动作：从最旧记录开始归档到 `skill-NN-<主题>.md`，docs 与 req 同步归档
- 目标状态：两个目录文件数均 ≤ 4

### 3. PyPI badge 滞后调查

- shields.io badge 缓存策略：`cache-control: max-age=10800`（3 小时）
- 结论：发布新版后 badge 最多延迟 3 小时刷新，属正常行为，无需处理

## 验证结果

- rule-01 规则文本已更新，语义明确
- docs/ 与 req/ 目录文件数 ≤ 4
- PyPI badge 正常显示

## 遗留事项

无。

---

## 原始需求（req-15）

### 任务 1：req/docs 清理规则优化

- [x] 分析 `.trae/req` 和 `.trae/docs` 未按 rule-01 定期清理的原因
- [x] 提出 rule-01 优化方案并征求用户授权（修改规则须先询问用户）
- [x] 获授权后修改 rule-01，执行清理归档

### 任务 2：PyPI badge 更新滞后调查

- [x] 确认 README.md 第 6 行 PyPI badge 未及时更新标签的原因（shields.io 缓存 3 小时，属正常滞后）
