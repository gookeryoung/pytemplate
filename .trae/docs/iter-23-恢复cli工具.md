# iter-23：恢复 cli 工具

## 需求清单

- [x] 恢复 `src/coopie/` 包结构（`__init__.py` + `py.typed`）
- [x] 实现 `src/coopie/cli.py`：Typer app + `init`/`update` 两个命令
- [x] 恢复 `tests/` 并编写 CLI 测试（13 个用例，覆盖率 100%）
- [x] 重构 `pyproject.toml`：恢复 build-system/scripts/hatch/pytest/coverage 配置
- [x] 更新 CI 工作流：新增 test job，lint job 扩展为全量检查
- [x] 更新 release.yml：恢复 PyPI 发布（OIDC trusted publishing）
- [x] 更新 Makefile：新增 `test`/`cov`/`build` 目标
- [x] 更新 README.md 与 docs/：新增 CLI 使用说明
- [x] 重新生成 `uv.lock` 并验证全套门禁全绿

## 迭代目标

反转 iter-22 的纯模板仓库决策，恢复 coopie 为 PyPI 包，提供 `coopie init`/`coopie update` CLI 封装 copier 命令，简化模板使用。CLI 框架选用 Typer（类型注解驱动），模板源默认 Gitee 国内源并支持 `--url` 切换。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/coopie/__init__.py` | 新建 | 恢复 Python 包，提供 `__version__` 供 CLI 与 bump-my-version 使用 |
| `src/coopie/py.typed` | 新建 | PEP 561 类型标记空文件 |
| `src/coopie/cli.py` | 新建 | Typer app + `init`/`update` 命令，封装 `copier copy`/`copier recopy` |
| `tests/__init__.py` | 新建 | 空文件 |
| `tests/test_cli.py` | 新建 | 13 个测试用例，覆盖率 100% |
| `pyproject.toml` | 重写 | 恢复 build-system/scripts/hatch/pytest/coverage；requires-python >=3.9；依赖 copier/jinja2-time/typer；ruff target py39；per-file-ignores 加 cli.py UP045 |
| `.python-version` | 修改 | 3.8 → 3.9 |
| `.github/workflows/ci.yml` | 重写 | lint job 全量检查；新增 test job（pytest --cov）；保留 render/docs job |
| `.github/workflows/release.yml` | 重写 | 恢复 PyPI 发布（OIDC trusted publishing）；`uv build` + `uv publish` |
| `Makefile` | 重写 | 新增 `test`/`cov`/`build` 目标；`lint` 改为全量 `ruff check` |
| `README.md` | 重写 | 新增"使用 coopie CLI（推荐）"章节；Python badge 3.9+ |
| `docs/usage.rst` | 重写 | 新增 CLI 使用说明；Python >= 3.9 |
| `docs/index.rst` | 重写 | 移除"不再发布 Python 包"；新增 CLI 示例 |
| `docs/changelog.rst` | 修改 | 新增 v0.9.0（未发布）条目 |
| `uv.lock` | 重新生成 | 新增 copier/jinja2-time/typer/pytest/pytest-cov 等依赖 |
| `.trae/req/req-23-恢复cli工具.md` | 新建 | 需求记录 |
| `.trae/docs/iter-23-恢复cli工具.md` | 新建 | 本迭代记录 |

## 关键决策与依据

### 1. CLI 框架选用 Typer 而非 Click/argparse

- **依据**：python-cli SKILL 推荐新项目首选 Typer（类型注解驱动、代码量少、自动生成帮助），与 rule-11 类型注解要求天然契合
- **实现**：`typer.Typer(name="coopie", no_args_is_help=True)` + `@app.command()` 定义 init/update

### 2. 模板源默认 Gitee 并支持 `--url` 切换

- **依据**：用户确认"两者都支持，提供 --url 参数，默认 Gitee"
- **实现**：`DEFAULT_URL = "https://gitee.com/gooker_young/coopie.git"`，`init` 命令 `--url`/`-u` 选项覆盖

### 3. `requires-python` 从 `>=3.8` 升至 `>=3.9`

- **依据**：copier 9.x 要求 Python >=3.9，`copier recopy` 是 9.0+ 特性
- **影响**：同步更新 `.python-version`、classifiers、ruff `target-version`、pyrefly `python-version`

### 4. subprocess 调用 copier CLI 而非 Python API

- **依据**：copier 作为依赖安装后其入口点在 PATH 中可用；subprocess 调用与用户使用 copier 原生命令的行为一致，且实现更简单
- **实现**：`subprocess.run(cmd, check=True)`，捕获 `FileNotFoundError`（copier 未安装）与 `CalledProcessError`（copier 失败）

### 5. ruff per-file-ignores 为 cli.py 添加 UP045

- **依据**：Typer 内部使用 `typing.get_type_hints()` 解析注解，会 `eval()` 注解字符串。Python 3.9 运行时不支持 `str | None` 语法（`TypeError: unsupported operand type(s) for |`），必须用 `Optional[str]`
- **影响**：ruff UP045 规则要求 `X | None`，与 Typer + Python 3.9 不兼容，需为 cli.py 单独忽略

### 6. `update` 命令校验 `.copier-answers.yml` 存在

- **依据**：`copier recopy` 只能在 copier 生成的项目中执行，提前校验给出友好错误提示
- **实现**：检查 `dst / ".copier-answers.yml"` 是否存在，不存在则 `typer.secho` 红色错误 + `raise typer.Exit(1)`

### 7. 恢复 OIDC trusted publishing 而非 API token

- **依据**：OIDC 是 PyPI 现代发布方式，无需管理 token，更安全；参考 template/ 下 release.yml 模式
- **实现**：`permissions: id-token: write` + `environment: pypi` + `uv publish`

### 8. 版本号保持 0.8.0（未 bump 到 0.9.0）

- **依据**：changelog 已记录 v0.9.0（未发布）条目，实际 bump 在 release 时由 bump-my-version 自动完成（git tag 触发）
- **状态**：当前版本 0.8.0，changelog 标注"未发布"，待用户执行 `bump-my-version bump minor` 后发布

## 代码实现情况

- `src/coopie/cli.py`（106 行）：Typer app + `_version_callback`（--version）+ `init`（copier copy）+ `update`（copier recopy）+ `_run_copier`（错误处理）+ `main`（入口）
- `tests/test_cli.py`（219 行）：13 个测试用例，覆盖 --version/无参数帮助/init 默认+自定义 url+vcs-ref+defaults/copier 未找到/copier 失败/update 默认+当前目录+vcs-ref+defaults/缺少 answers 文件
- `pyproject.toml`（143 行）：恢复 [build-system]/[project.scripts]/[tool.hatch.build]/[tool.pytest]/[tool.coverage]，新增 copier/jinja2-time/typer 依赖，ruff target py39

## 整合优化情况

- jinja2-time 作为 coopie 核心依赖：安装 coopie 时自动包含 jinja2-time，用户无需 `--with jinja2-time` 标志
- CI lint job 从仅检查 docs/ 扩展为全量检查（src/ + tests/ + docs/）
- Makefile `lint` 目标从 `ruff check docs` 改为 `ruff check`（全量）
- bump-my-version 配置新增 `src/coopie/__init__.py` 文件，确保版本号同步

## 测试验证结果

```
uv run ruff check           → All checks passed!
uv run ruff format --check  → 5 files already formatted
uv run pyrefly check        → 0 errors
uv run pytest --cov         → 13 passed, coverage 100.00%
```

覆盖率明细：
- src/coopie/__init__.py: 100%
- src/coopie/cli.py: 100%
- TOTAL: 100.00%（达标 fail_under=95）

uv.lock：87 packages（新增 copier/jinja2-time/typer/pytest/pytest-cov 及其依赖）

## 遗留事项

- 版本号尚未 bump 到 0.9.0（changelog 已标注"未发布"），待用户执行 `bump-my-version bump minor` 触发 release
- `.trae/req/` 下 req-19/20/21 已完成但未移动到 done/（沿用 iter-22 遗留，后续迭代逐步迁移）
- `.trae/docs/iter-18-Windows文件名兼容.md` 已清理（保留最新 5 条迭代记录）

## 下一轮计划

无。本次迭代已完整覆盖"恢复 cli 工具"的所有需求，全套门禁全绿。等待用户反馈或新需求。
