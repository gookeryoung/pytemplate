"""Sphinx 配置.

ReadTheDocs 构建项目文档站。
"""

from __future__ import annotations

import re
from pathlib import Path

# -- 项目信息 --------------------------------------------------------------
project = "coopie"
author = "gooker_young"
copyright = "2026, gooker_young"

# 版本号从 pyproject.toml 读取，避免依赖 src 包导入
_pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
_match = re.search(r'^version\s*=\s*"([^"]+)"', _pyproject.read_text(encoding="utf-8"), re.MULTILINE)
release = _match.group(1) if _match else "0.0.0"
version = release

# -- Sphinx 配置 -----------------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

# -- 主题 ------------------------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- autodoc 配置 ----------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}
autodoc_type_hints = "description"
autodoc_typehints_format = "short"

# -- napoleon 配置 (Google/NumPy docstring 兼容) --------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# -- intersphinx -----------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- 全局选项 ---------------------------------------------------------------
language = "zh_CN"
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
