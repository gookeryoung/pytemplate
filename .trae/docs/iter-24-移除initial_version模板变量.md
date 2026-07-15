# iter-24：移除 initial_version 模板变量

## 需求清单

- [x] 从 `copier.yml` 移除 `initial_version` 问题定义
- [x] 模板 `pyproject.toml` 硬编码 `version` 与 `current_version` 为 `0.1.0`
- [x] 模板 `__init__.py` 硬编码 `__version__` 为 `0.1.0`
- [x] 更新 `README.md` 与 `docs/parameters.rst` 移除 `initial_version` 说明
- [x] 从 `.copier-answers.yml` 移除 `initial_version` 字段
- [x] 验证：ruff/pyrefly/pytest 全绿 + 渲染测试通过

## 迭代目标

移除模板中的 `initial_version` 变量。每个项目的初始版本统一由模板硬编码为 `0.1.0`，用户创建项目后可自行修改；`copier update` 不再涉及版本号变量，避免覆盖用户 bump 后的版本号，也减少 update 时的交互负担。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `copier.yml` | 修改 | 移除 `initial_version` 问题定义段 |
| `template/pyproject.toml` | 修改 | `version` 与 `current_version` 由 `{{ initial_version }}` 改为硬编码 `"0.1.0"` |
| `template/src/{{ package_name }}/__init__.py` | 修改 | `__version__` 由 `{{ initial_version }}` 改为硬编码 `"0.1.0"` |
| `README.md` | 修改 | 参数表移除 `initial_version` 行 |
| `docs/parameters.rst` | 修改 | 移除 `initial_version` 段落 |
| `.copier-answers.yml` | 修改 | 移除 `initial_version: 0.8.0` 字段 |
| `.trae/req/req-24-移除initial_version模板变量.md` | 新建 | 需求记录 |
| `.trae/docs/iter-24-移除initial_version模板变量.md` | 新建 | 本迭代记录 |

## 关键决策与依据

### 1. 硬编码 `0.1.0` 而非保留问题

- **依据**：用户反馈"每个项目有所不同，每次 update 都会增加麻烦且容易出错"。保留问题无论设何默认值，都会在 `copier update` 时重新参与渲染，存在覆盖用户 bump 后版本号的隐患
- **实现**：模板三处（`pyproject.toml` 的 `version`/`current_version`、`__init__.py` 的 `__version__`）统一硬编码 `"0.1.0"`，与原 `copier.yml` 的 `default` 一致

### 2. 不引入 `_skip_if_exists` 配置

- **依据**：硬编码后 `pyproject.toml` 等文件不再含 `initial_version` 变量，`copier update` 三方合并时模板侧版本号恒为 `0.1.0`，不会因变量值变化触发覆盖；用户 bump 后的版本号作为本地修改被保留。引入 `_skip_if_exists` 会阻止模板对 pyproject.toml 其他字段的更新传递，得不偿失
- **实现**：不修改 `_skip_if_exists` 配置

### 3. 同步清理 `.copier-answers.yml`

- **依据**：coopie 自身是用本模板生成的项目，其 `.copier-answers.yml` 记录了 `initial_version: 0.8.0`。移除问题定义后，该字段成为孤儿数据，应同步清理保持一致
- **实现**：手动删除该字段（coopie 仓库自身不应运行 `copier update`）

## 代码实现情况

- `copier.yml`：删除 `initial_version` 问题定义段（5 行），保留 Python 版本配置段
- `template/pyproject.toml`：第 18 行 `version = "0.1.0"`、第 125 行 `current_version = "0.1.0"`
- `template/src/{{ package_name }}/__init__.py`：第 7 行 `__version__ = "0.1.0"`
- `README.md`：参数表移除 `initial_version` 行
- `docs/parameters.rst`：移除 `initial_version` 段落
- `.copier-answers.yml`：移除 `initial_version: 0.8.0` 行

## 整合优化情况

- 全仓库 Grep `initial_version` 确认零残留
- `docs/conf.py` 第 25 行 `version = "0.1.0"` 为 import 失败时的硬编码 fallback，与模板变量无关，未改动

## 测试验证结果

```
uv run ruff check           → All checks passed!
uv run ruff format --check  → 5 files already formatted
uv run pyrefly check        → 0 errors
uv run pytest --cov         → 13 passed, coverage 100.00%
```

渲染测试（`uv run copier copy --trust --defaults --vcs-ref HEAD . .preview/test-no-version`）：
- 未询问 `initial_version`
- 渲染产物 `pyproject.toml` `version = "0.1.0"`、`current_version = "0.1.0"`
- 渲染产物 `src/my_project/__init__.py` `__version__ = "0.1.0"`
- 渲染产物 `.copier-answers.yml` 不含 `initial_version` 字段

## 遗留事项

无。

## 下一轮计划

无。本次迭代已完整覆盖"移除 initial_version 模板变量"的所有需求，全套门禁全绿，渲染测试通过。等待用户反馈或新需求。
