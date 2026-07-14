# iter-22：移除 cli 工具改为纯模板仓库

## 需求清单

- [x] 删除 `src/coopie/` 与 `tests/` 目录
- [x] 重构 `pyproject.toml`：移除 coopie 包相关配置
- [x] 重写 `README.md` 为 copier 模板使用说明
- [x] 调整 `docs/` 为模板说明文档
- [x] 调整 `Makefile` 为模板开发命令
- [x] 调整 CI 工作流：移除 pytest/coverage，新增 copier 渲染验证
- [x] 调整 release.yml：移除 PyPI 发布，仅 GitHub Release
- [x] 删除 `tox.ini`
- [x] 调整 `copier.yml`：移除 `use_cli` 字段
- [x] 清理 `.copier-answers.yml`
- [x] 重新生成 `uv.lock`
- [x] 验证四种 project_type 渲染
- [x] ruff/pyrefly/文档构建全绿

## 迭代目标

coopie 仓库此前以 `coopie` Python 包形式发布到 PyPI，封装 `coopie new/init/update/test` 子命令调用 `uvx copier`。用户已移除 `src/coopie/cli.py`，决定回归 copier 原生使用方式。本次迭代同步清理所有依赖 cli 工具的产物（src/、tests/、tox.ini、PyPI 发布、coopie 包元数据），重构仓库为纯 copier 模板仓库，并通过 `copier copy` 直接使用。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/coopie/__init__.py` | 删除 | coopie Python 包不再存在 |
| `src/coopie/py.typed` | 删除 | 同上 |
| `tests/__init__.py` | 删除 | 无包可测 |
| `tox.ini` | 删除 | 无包可测 |
| `pyproject.toml` | 重写 | 移除 `[project.scripts]`/`[tool.hatch.build]`/`[tool.coverage]`/`[tool.pytest]`/`[tool.bumpversion.files]` 中 src 路径；改 classifier 为 `Code Generators`；保留 lint/docs 工具链；bumpversion 增加 `.copier-answers.yml` 文件 |
| `README.md` | 重写 | 从"Python 包安装使用"改为"copier 模板使用说明"，含创建/更新/参数表/模板开发/目录结构 |
| `docs/index.rst` | 重写 | 移除 coopie 包导入示例，改为模板简介 + toctree 指向 usage/parameters/changelog |
| `docs/api.rst` | 删除 | coopie 包 API 不再存在 |
| `docs/usage.rst` | 新建 | 使用指南（前置要求/创建/更新/项目类型/模板开发） |
| `docs/parameters.rst` | 新建 | 模板参数说明（项目信息/Python 版本/许可证/功能开关/派生变量/模板配置） |
| `docs/conf.py` | 修改 | 版本号改为从 pyproject.toml 正则读取，移除 `from coopie import __version__` |
| `docs/changelog.rst` | 修改 | 新增 v0.8.0 条目 |
| `Makefile` | 重写 | 移除 `coopie` 包引用与 `pub`（PyPI）目标；新增 `render` 目标渲染四种 project_type 到 `.preview/`；`build` 目标改为提示信息 |
| `.github/workflows/ci.yml` | 重写 | 移除 test job（pytest/coverage）；新增 render job（矩阵渲染 library/cli/gui/web + 验证结构 + 验证 TOML 语法）；新增 docs job（Sphinx 构建） |
| `.github/workflows/release.yml` | 重写 | 移除 PyPI 发布步骤与 `id-token: write` 权限；仅保留 GitHub Release |
| `copier.yml` | 修改 | 移除 `use_cli` 字段（与 `project_type == 'cli'` 重复）；`project_type` help 补充"cli 启用 [project.scripts]"说明 |
| `template/pyproject.toml` | 修改 | `{% if use_cli or project_type == "cli" %}` 简化为 `{% if project_type == "cli" %}` |
| `.copier-answers.yml` | 修改 | 移除 `use_cli` 字段；`_commit` v0.7.12 → v0.8.0；`description` 同步新文案 |
| `uv.lock` | 重新生成 | 移除 pytest/tox/coverage 等 26 个包；coopie v0.7.12 → v0.8.0 |
| `.gitignore` | 修改 | 新增 `.preview/` 忽略 |
| `.trae/rules/rule-02-产物约束.md` | 修改 | 同步 template/ 下已提交的简化：归档清理段简化为"超过 5 时清理，保留最新 5 条"，"已完成 req 移到 done/"移到需求记录段（之前会话 staged，本次随提交） |
| `.trae/req/req-22-移除cli工具改为纯模板仓库.md` | 新建 | 需求记录 |
| `.trae/req/done/req-18-Windows文件名兼容.md` | 移动 | req-18 已完成，按新规则移动到 done/ |
| `.trae/docs/iter-22-移除cli工具改为纯模板仓库.md` | 新建 | 本迭代记录 |

## 关键决策与依据

### 1. 完全删除 `src/coopie/` 而非保留 `__init__.py` + `py.typed`

- **依据**：coopie 不再发布 Python 包，保留空包会让 pyproject.toml 仍需 `[tool.hatch.build]` 配置，且 conf.py 需要导入 coopie 取版本号——增加无意义维护成本
- **影响**：docs/conf.py 改为从 pyproject.toml 正则读取版本号；pyproject.toml 移除 `[build-system]`

### 2. 保留 `[project]` 元数据但移除 `[build-system]`

- **依据**：uv 支持无 build-system 的 PEP 621 项目（virtual project），仍可管理 optional-dependencies 与工具配置
- **效果**：`uv sync` 不再构建 coopie 包，仅安装 lint/docs 工具链；`uv run` 仍可调用 ruff/pyrefly/sphinx

### 3. CI 用矩阵渲染验证替代 pytest

- **依据**：模板仓库的核心质量指标是"渲染正确性"，而非 Python 包测试覆盖率
- **实现**：render job 矩阵跑 library/cli/gui/web 四种 project_type，验证关键文件生成（cli.py/main.py/app.py/fastapi SKILL）与 pyproject.toml 的 TOML 语法
- **保留**：lint job（ruff+pyrefly 校验 docs/conf.py）与 docs job（Sphinx 构建）

### 4. release.yml 移除 PyPI 发布

- **依据**：coopie 不再是 Python 包，无需发布到 PyPI
- **保留**：GitHub Release（基于 git tag 自动生成 release notes），供 copier `--vcs-ref` 引用

### 5. copier.yml 移除 `use_cli` 字段

- **依据**：`use_cli` 与 `project_type == 'cli'` 语义重复，且用户反馈"cli 类型自动启用入口"更直观
- **影响**：template/pyproject.toml 中 `{% if use_cli or project_type == "cli" %}` 简化为 `{% if project_type == "cli" %}`；`.copier-answers.yml` 同步移除 `use_cli` 字段

### 6. 版本号 0.7.12 → 0.8.0（minor bump）

- **依据**：移除 cli 工具与 PyPI 发布是 breaking change（用户从 `pip install coopie` 改为 `copier copy`）
- **bumpversion 配置**：新增 `.copier-answers.yml` 作为 bump 文件，确保版本号与 `_commit` 字段同步

### 7. Makefile `render` 目标用 `.preview/` 而非 `/tmp/`

- **依据**：Windows 无 `/tmp/`，用项目内 `.preview/`（已加入 .gitignore）兼容 Windows/Linux/macOS
- **实现**：`rm -rf .preview && mkdir .preview` 后 copier copy 到 `.preview/{lib,cli,gui,web}/`

## 代码实现情况

- pyproject.toml：113 行 → 99 行，移除 5 个工具段（scripts/hatch.build/coverage/pytest/bumpversion.files 中 src 路径）
- README.md：90 行 → 138 行，从"Python 包文档"转为"copier 模板使用文档"
- docs/：5 文件 → 5 文件（删 api.rst，新建 usage.rst + parameters.rst），从"包 API 文档"转为"模板使用指南"
- Makefile：56 行 → 55 行，移除 test/cov/pub 目标，新增 render 目标
- CI：3 jobs（lint/test/docs）→ 3 jobs（lint/render/docs），test 改为 render 矩阵
- copier.yml：197 行 → 192 行，移除 use_cli 段

## 整合优化情况

- 移除 `coopie[lint,test]` 自引用：dev 改为 `coopie[lint,docs]` + prek（不再有 test）
- bumpversion exclude 增加 `.trae/**`：避免 bump 误改迭代记录中的版本号引用
- ruff `extend-exclude` 增加 `.venv`：防止误检虚拟环境

## 测试验证结果

```
uv run ruff check docs         → All checks passed!
uv run ruff format --check docs → 1 file already formatted
uv run pyrefly check           → 0 errors
uv run sphinx-build -b html docs docs/_build/html → 构建成功（4 个源文件）
```

copier copy 渲染验证（`--vcs-ref HEAD`）：

| project_type | 关键产物 | 结果 |
|--------------|----------|------|
| library | src/my_project/{__init__.py, py.typed} | OK |
| cli | + src/my_project/cli.py + [project.scripts] | OK |
| gui | + src/my_project/main.py + PySide2/PySide6 deps | OK |
| web | + src/my_project/app.py + fastapi SKILL + fastapi/uvicorn deps | OK |

uv.lock：65 packages（移除 26 个 pytest/tox/coverage 相关包）

## 遗留事项

- `.trae/req/` 下 req-19/20/21 均已完成但未移动到 `done/`（本次仅移动 req-18 触发新规则的 done/ 目录创建），后续迭代可按新规则逐步迁移
- rule-02 归档规则已简化（不再归档到 skill-NN），与 template/ 下 rule-02 保持一致；`.trae/skills/` 下历史 skill-14/15 文件已不存在，无需清理

## 下一轮计划

无。本次迭代已完整覆盖"移除 cli 工具改为纯模板仓库"的所有需求，验证全绿。等待用户反馈或新需求。
