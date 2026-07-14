使用指南
========

前置要求
--------

- Python ≥ 3.8
- uv_ ≥ 0.5（推荐）
- copier_ ≥ 9（通过 ``uvx copier`` 免安装调用）

.. _uv: https://docs.astral.sh/uv/
.. _copier: https://copier.readthedocs.io/

创建新项目
----------

在希望生成项目的父目录中执行：

.. code-block:: bash

   # 国内用户推荐 Gitee 源（访问稳定）
   uvx copier copy --trust https://gitee.com/gooker_young/coopie.git my-project

   # 国外用户可使用 GitHub 源
   uvx copier copy --trust https://github.com/gookeryoung/coopie.git my-project

执行后 copier 会交互式询问项目名称、包名、Python 版本范围、项目类型（library/cli/gui/web）等参数，并在 ``my-project/`` 目录生成完整工程骨架。

常用选项：

- ``--trust``：允许模板中的 Jinja 扩展（如 ``jinja2-time``）执行。
- ``--defaults``：使用所有参数的默认值，跳过交互（适用于 CI/脚本化场景）。
- ``--vcs-ref v0.8.0``：指定模板版本（默认使用最新 tag）。
- ``--data project_name=foo``：在命令行预设参数值。

生成后的下一步
--------------

进入生成目录并初始化开发环境：

.. code-block:: bash

   cd my-project
   uv sync --extra dev
   git init && git add -A && git commit -m "feat: 初始化项目"

更新已有项目
------------

当模板版本升级后，在已生成的项目目录中执行：

.. code-block:: bash

   uvx copier update --trust --with jinja2-time

copier 会比对当前模板版本与 ``.copier-answers.yml`` 中记录的版本，交互式应用差异更新。如遇冲突，copier 会标记并询问保留哪一侧。

项目类型说明
------------

模板支持四种项目类型，通过 ``project_type`` 参数选择：

- ``library``：纯库项目，无入口脚本，src layout + py.typed。
- ``cli``：命令行工具，生成 ``cli.py`` 与 ``[project.scripts]`` 入口，基于 argparse。
- ``gui``：PySide2/PySide6 桌面应用，按 Python 版本自动选择（≤3.10 用 PySide2，≥3.11 用 PySide6），随模板分发 GUI 设计规范与代码模板。
- ``web``：FastAPI + uvicorn 服务，随模板分发 FastAPI SKILL 文档。

模板开发
--------

本仓库自身即 copier 模板，开发与验证流程：

.. code-block:: bash

   # 安装开发依赖（lint + docs 工具链）
   uv sync --extra dev

   # 校验 docs/conf.py 等非模板 Python 文件
   uv run ruff check docs
   uv run ruff format --check docs

   # 类型检查
   uv run pyrefly check

   # 本地构建文档
   make doc

   # 渲染验证（生成到临时目录检查输出）
   uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/preview-lib
   uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/preview-cli --data project_type=cli
   uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/preview-gui --data project_type=gui
   uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/preview-web --data project_type=web
