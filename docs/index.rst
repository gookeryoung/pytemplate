coopie
======

基于 copier_ 的通用 Python 项目模板，通过 ``copier copy`` 一键生成开箱即用的工程骨架。

.. toctree::
   :maxdepth: 2
   :caption: 目录

   usage
   parameters
   changelog

简介
====

coopie 是一个 copier_ 模板仓库，用于生成符合现代 Python 工程实践的项目骨架。模板内置 hatchling + uv + ruff + pyrefly + pytest + coverage 工具链，支持 library / cli / gui（PySide2/PySide6）/ web（FastAPI）四种项目类型，并随模板分发完整的开发规则体系（``.trae/rules/``）与 SKILL 文档（``.trae/skills/``）。

本仓库**不再发布为 Python 包**，所有使用方式通过 copier 原生命令完成。

.. _copier: https://copier.readthedocs.io/

快速开始
========

创建新项目：

.. code-block:: bash

   # 国内用户推荐 Gitee 源
   uvx copier copy --trust https://gitee.com/gooker_young/coopie.git my-project

   # 国外用户可使用 GitHub 源
   uvx copier copy --trust https://github.com/gookeryoung/coopie.git my-project

更新已有项目：

.. code-block:: bash

   cd my-project
   uvx copier update --trust --with jinja2-time

详细用法见 :doc:`usage`，模板参数说明见 :doc:`parameters`。
