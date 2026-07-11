# iter-17 需求：回退工具配置拆分

## 背景

iter-16 将 ruff/pyrefly/coverage/pytest 工具配置从 pyproject.toml 拆分到独立文件（ruff.toml/pyrefly.toml/.coveragerc/pytest.ini），并添加 `_skip_if_exists: [pyproject.toml]` 保护项目元数据。

用户反馈方向错误：
- ruff 等工具配置相对标准、不需要拆分，反而被独立出来了
- `[project.optional-dependencies]`（pyproject.toml L23-39）是用户频繁定制的项目相关内容，需要 TOML 语义级解析合并，但 iter-16 没有提供任何措施
- `_skip_if_exists` 是文件级跳过（全有或全无），无法做 per-section 保护

用户选择**方案 D：回退拆分 + 接受原始状态**——工具配置放回 pyproject.toml，不用 `_skip_if_exists`，回到 iter-16 前的状态。

## 需求

- [x] 恢复 template/pyproject.toml 工具配置段（Jinja 变量版）
- [x] 恢复 pyproject.toml 工具配置段（渲染值版）
- [x] 移除 copier.yml 中的 `_skip_if_exists` 段
- [x] 删除 8 个独立配置文件（template/ 和项目根各 4 个）
- [x] make check 验证回退后状态正常
- [x] bump 版本 0.4.4 → 0.4.5 + push
- [x] 更新 memory 文件（移除 _skip_if_exists 约定）

## 约束

- 回退到 iter-16 前（commit 1693e92）的准确状态，不引入新变更
- `[project.optional-dependencies]` 的 TOML 语义合并问题暂不解决（接受 copier 行级 diff3 原始状态）
- 标准门禁：ruff + pyrefly + pytest 95% 覆盖率

## 验收标准

- pyproject.toml（项目根 + 模板）包含完整的工具配置段
- copier.yml 无 `_skip_if_exists` 段
- 8 个独立配置文件已删除
- make check 全绿
