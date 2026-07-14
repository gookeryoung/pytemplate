# req-22：移除 cli 工具改为纯模板仓库

## 背景

coopie 仓库此前以 `coopie` Python 包形式发布到 PyPI，包含 `src/coopie/cli.py`（封装 `coopie new/init/update/test` 子命令，内部调用 `uvx copier`）。用户已移除 `src/coopie/cli.py`，仅保留 `__init__.py` 与 `py.typed`，决定回归 copier 原生使用方式：

```bash
copier copy https://gitee.com/gooker_young/coopie.git my-project
```

仓库根目录不再发布 Python 包，所有 Python 工具链配置（pyproject.toml 的 `[project.scripts]`/`[tool.hatch.build]`/`[tool.coverage]` 等）、tests/、tox.ini、PyPI 发布流程均已失效或冗余，需同步清理与重构。

## 需求

- [x] 删除 `src/coopie/` 与 `tests/` 目录
- [x] 重构 `pyproject.toml`：移除 coopie 包相关配置（`[project.scripts]`/`[tool.hatch.build]`/`[tool.coverage]`/`[tool.bumpversion.files]` 中 src 路径），保留 lint/docs 工具链与版本号管理
- [x] 重写 `README.md`：从"Python 包安装使用"改为"copier 模板使用说明"
- [x] 调整 `docs/`：移除 `coopie` 包 API 文档，改为模板字段说明与使用指南
- [x] 调整 `Makefile`：移除 `coopie` 包相关目标，保留 lint/doc/build/push 等
- [x] 调整 CI 工作流：移除 pytest/coverage 测试任务，新增 copier 模板渲染验证
- [x] 调整 release.yml：移除 PyPI 发布步骤，仅保留 GitHub Release
- [x] 删除 `tox.ini`（无 Python 包可测）
- [x] 调整 `copier.yml`：移除 `use_cli` 字段（与 `project_type == 'cli'` 重复）
- [x] 清理 `.copier-answers.yml` 中 `use_cli` 等已废弃字段
- [x] 重新生成 `uv.lock`
- [x] 验证 `copier copy` 四种 project_type（library/cli/gui/web）渲染正确
- [x] ruff check / pyrefly / 文档构建全绿
- [x] 更新 `.trae/docs/iter-22-*.md` 迭代记录
