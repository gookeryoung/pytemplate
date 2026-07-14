# coopie

> 基于 [copier](https://copier.readthedocs.io/) 的通用 Python 项目模板，通过 `copier copy` 一键生成开箱即用的工程骨架。

[![CI](https://github.com/gookeryoung/coopie/actions/workflows/ci.yml/badge.svg)](https://github.com/gookeryoung/coopie/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 简介

coopie 是一个 [copier](https://copier.readthedocs.io/) 模板仓库，用于生成符合现代 Python 工程实践的项目骨架。模板内置：

- **构建工具链**：hatchling + uv + ruff + pyrefly + pytest + coverage
- **Python 版本**：3.8 ~ 3.14（可配置最低/最高版本）
- **代码质量**：pre-commit 钩子 + ruff lint/format，可配置覆盖率阈值
- **CI/CD**：GitHub Actions（lint + typecheck + 多版本测试 + 自动发布到 PyPI）
- **文档**：Sphinx + ReadTheDocs（中文 zh_CN）
- **多版本测试**：tox + tox-uv
- **项目类型**：library / cli / gui（PySide2/PySide6）/ web（FastAPI）
- **项目结构**：src layout + py.typed 类型标记
- **开发规则**：内嵌 `.trae/rules/` 与 `.trae/skills/` 规则体系，配套 SKILL 文档

## 使用方式

### 前置要求

- Python ≥ 3.8
- [uv](https://docs.astral.sh/uv/) ≥ 0.5（推荐）
- [copier](https://copier.readthedocs.io/) ≥ 9（通过 `uvx copier` 免安装调用）

### 创建新项目

```bash
# 国内用户推荐 Gitee 源（访问稳定）
uvx copier copy --trust https://gitee.com/gooker_young/coopie.git my-project

# 国外用户可使用 GitHub 源
uvx copier copy --trust https://github.com/gookeryoung/coopie.git my-project
```

> `--trust` 用于允许模板中的 Jinja 扩展（如 `jinja2-time`）执行。如需指定模板版本，附加 `--vcs-ref v0.8.0`。

执行后 copier 会交互式询问项目名称、包名、Python 版本范围、项目类型（library/cli/gui/web）等参数，并在 `my-project/` 目录生成完整工程骨架。

### 模板参数速览

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `project_name` | str | `my-project` | 项目名称（用于 README/文档标题） |
| `package_name` | str | 由 `project_name` 派生 | Python 包名（小写+下划线） |
| `description` | str | `A Python project.` | 项目简短描述 |
| `author_name` / `author_email` | str | 空 | 作者信息 |
| `initial_version` | str | `0.1.0` | 初始版本号 |
| `min_python_version` / `max_python_version` | str | `3.8` / `3.14` | Python 版本范围 |
| `license` | str | `MIT` | 许可证（MIT/Apache-2.0/GPL-3.0/None） |
| `project_type` | str | `library` | 项目类型（library/cli/gui/web） |
| `use_docs` | bool | `true` | 是否包含 Sphinx 文档配置 |
| `use_docker` | bool | `false` | 是否包含 Dockerfile |
| `use_cicd` | bool | `true` | 是否包含 GitHub Actions CI/CD |
| `use_tox` | bool | `true` | 是否包含 tox 多版本测试 |
| `use_domestic_mirrors` | bool | `true` | 是否预置国内镜像源（pip/uv 清华源、apt 阿里云） |
| `coverage_fail_under` | int | `95` | 覆盖率阈值（百分比） |

完整参数说明见 [`copier.yml`](copier.yml)。

### 更新已有项目

当模板版本升级后，可在已生成的项目目录中执行：

```bash
uvx copier update --trust --with jinja2-time
```

copier 会比对当前模板版本与 `.copier-answers.yml` 中记录的版本，交互式应用差异更新。

## 模板开发

本仓库自身即 copier 模板，开发流程如下：

```bash
# 安装开发依赖（lint + docs 工具链）
uv sync --extra dev

# 校验 docs/conf.py 等非模板 Python 文件
uv run ruff check docs
uv run ruff format --check docs

# 类型检查
uv run pyrefly check

# 本地构建文档
make doc

# 渲染验证（不写入磁盘）
uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/preview-lib
```

### Make 快捷命令

```bash
make sync     # 安装开发依赖
make lint     # ruff 检查
make typecheck # pyrefly 类型检查
make doc      # 构建 Sphinx 文档
make check    # 全套门禁 (lint + typecheck)
make bump PART=patch  # 版本号 bump（创建 git tag，供 copier --vcs-ref 引用）
make push     # 推送到所有远程仓库
```

## 目录结构

```
coopie/
├── copier.yml              # Copier 模板配置（参数定义与渲染规则）
├── template/               # 模板内容（Jinja 渲染源，所有文件均参与渲染）
│   ├── src/{{ package_name }}/
│   ├── tests/
│   ├── .trae/rules/        # 开发流程规则（随模板分发）
│   ├── .trae/skills/       # SKILL 文档（类设计/并发/IO/测试/CLI/日志/配置/子进程/GUI）
│   ├── pyproject.toml      # 模板内的 pyproject.toml（含 Jinja 表达式）
│   ├── README.md           # 模板内的 README（含 Jinja 表达式）
│   └── ...
├── docs/                   # 本仓库的 Sphinx 文档
├── .trae/                  # 本仓库的开发规则与迭代记录
└── pyproject.toml          # 本仓库元数据与工具配置
```

## 文档

文档由 Sphinx 构建，托管在 ReadTheDocs：

```bash
make doc
```

## 许可证

MIT
