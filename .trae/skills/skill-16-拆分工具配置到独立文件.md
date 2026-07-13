# skill-16：拆分工具配置到独立文件（归档自 iter-16 / req-16）

> 归档时间：2026-07-13（iter-20 结束时触发归档，docs/ 与 req/ 文件数 ≥ 5）
> 原始文档：`.trae/docs/iter-16-拆分工具配置到独立文件.md`、`.trae/req/req-16-拆分工具配置到独立文件.md`

## 背景

`coopie update` 时 copier 对 `pyproject.toml` 做行级三方合并，不支持 TOML 语义级合并。用户对 `pyproject.toml` 的定制内容（新增依赖、工具配置）容易被模板更新覆盖或产生难以理解的冲突。

## 方案

将工具配置从 `pyproject.toml` 拆到独立文件，`pyproject.toml` 加入 `_skip_if_exists`，copier 生成后不再覆盖。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `template/pyproject.toml` | 修改 | 移除 [tool.ruff/pyrefly/coverage/pytest] 四个工具配置段 |
| `template/ruff.toml` | 新建 | Ruff 独立配置（TOML，Jinja 渲染 target_py） |
| `template/pyrefly.toml` | 新建 | Pyrefly 独立配置（TOML，Jinja 渲染 min_python_version） |
| `template/.coveragerc` | 新建 | Coverage 独立配置（INI，Jinja 渲染 package_name/coverage_fail_under） |
| `template/pytest.ini` | 新建 | Pytest 独立配置（INI，无 Jinja 变量） |
| `copier.yml` | 修改 | 新增 `_skip_if_exists: [pyproject.toml]` |

## 工具配置文件格式

| 工具 | 格式 | 前缀变化 | Jinja 变量 |
|------|------|---------|-----------|
| ruff | ruff.toml | [tool.ruff] → 顶层, [tool.ruff.lint] → [lint] | target_py |
| pyrefly | pyrefly.toml | [tool.pyrefly] → 顶层 | min_python_version |
| coverage | .coveragerc | [tool.coverage.run] → [run], [tool.coverage.report] → [report] | package_name, coverage_fail_under |
| pytest | pytest.ini | [tool.pytest.ini_options] → [pytest] | 无 |

工具配置优先级：独立文件 > pyproject.toml 中的 [tool.xxx]，首个命中即用、不合并。

## 保留在 pyproject.toml 的段（_skip_if_exists 后不被 copier 覆盖）

- [project] + [project.optional-dependencies] + [project.scripts]
- [build-system]
- [tool.uv] + [[tool.uv.index]]
- [tool.hatch.build.targets.wheel]
- [dependency-groups]
- [tool.bumpversion]（current_version 由 bump-my-version 自动维护）

## 后续走向

iter-17 回退了本方案——工具配置相对标准不需要拆分，回到 pyproject.toml 统一管理。当前接受 copier 行级 diff3 原始行为，冲突时手动解决。
