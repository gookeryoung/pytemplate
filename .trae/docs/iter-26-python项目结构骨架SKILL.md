# iter-26：Python 项目结构骨架设计 SKILL

## 需求清单

- [x] 创建 `python-project-structure` SKILL（根 + 模板两份）
- [x] 涵盖 12 个章节：项目布局/目录骨架/pyproject.toml/工具链拆分/包结构/测试目录/文档目录/CI-CD/项目类型差异/版本管理/构建发布/Makefile
- [x] 15 条常见陷阱
- [x] 更新 rule-03 注册新 SKILL 触发条目
- [x] 更新 project_memory.md

## 迭代目标

填补 SKILL 目录中"项目骨架设计总纲"的空白。coopie 现有 11 个 SKILL 覆盖具体技术领域，但缺少"项目骨架本身如何设计"的总纲性 SKILL。本次提炼 coopie 自身已实践的项目结构最佳实践（src layout + 工具链独立文件 + 4 种 project_type 差异化 + bump-my-version + OIDC 发布），形成系统性参考文档，供模板生成的项目与开发者参考。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `.trae/skills/python-project-structure/SKILL.md` | 新建 | 根目录 SKILL，896 行，12 章 + 15 条陷阱 |
| `template/.trae/skills/python-project-structure/SKILL.md` | 新建 | 模板目录 SKILL，898 行，与根目录内容一致 + `{% raw %}...{% endraw %}` 包裹避免 Jinja 误渲染 |
| `.trae/rules/rule-03-触发场景.md` | 修改 | 语言场景首位新增"项目骨架（src layout/pyproject.toml 元数据/PEP 631/735 依赖声明/工具链配置拆分/包内部结构/测试文档CI 目录组织/项目类型差异/版本管理与发布流程）→ `python-project-structure` SKILL" |
| `template/.trae/rules/rule-03-触发场景.md` | 修改 | 模板 rule-03 同步上述变更 |
| `.trae/docs/iter-21-gui设计规范与模板rule12填充.md` | 删除 | iter 文件数超 5，按 rule-02 清理最旧记录 |
| `.trae/req/req-26-python项目结构骨架SKILL.md` | 新建 | 需求记录 |

## 关键决策与依据

1. **SKILL 命名为 `python-project-structure`**：与现有 `python-*` 命名前缀一致；"project-structure" 准确表达项目骨架设计主题；不命名为 `python-project-template` 避免与 copier 模板概念混淆。

2. **rule-03 触发条目置于语言场景首位**：项目骨架是其他 SKILL 的基础（先有项目结构再谈类设计/并发/测试等），逻辑上应首先调用；rule-03 现有列表按主题组织，"项目骨架"作为最基础主题置首。

3. **template 版本用 `{% raw %}...{% endraw %}` 包裹全文**：SKILL 含 GitHub Actions YAML 示例（`${{ github.workflow }}`/`${{ github.token }}`）与 prose 中的 `{{ version }}` 占位符示例。`copier.yml` 配置 `_templates_suffix: ""` 使所有文件被 Jinja 渲染，这些模式会触发 `UndefinedError`。整体包裹 `{% raw %}` 比逐个转义更简洁可靠（参考 template/.github/workflows/*.yml 同样用 `{% raw %}` 转义 GitHub Actions 语法）。

4. **SKILL 用具体示例名（`my_package`/`my-package`）而非 Jinja 变量（`{{ package_name }}`）**：与 python-fastapi/python-cli SKILL 不同（它们用 `{{ package_name }}` 让 copier 替换为实际包名），本 SKILL 是设计指南，用具体示例名更直观；且避免与 `{% raw %}` 包裹冲突。

5. **15 条常见陷阱**：超过现有 SKILL 的 10 条惯例。因项目骨架涉及面广（布局/元数据/工具链/包结构/测试/文档/CI/版本/发布），15 条覆盖更全面；每条对应一个具体反模式与修复方案。

6. **iter-21 清理**：iter 文件数从 5 增至 6，按 rule-02"迭代文件数超过 5 时从最旧清理，保留最新 5 条"删除 iter-21。

## 代码实现情况

- `.trae/skills/python-project-structure/SKILL.md`：12 章主体内容
  1. 何时调用（10 个触发场景）
  2. 项目布局：src layout 首选（含目录树与 4 条要点）
  3. 完整目录骨架
  4. pyproject.toml 设计（完整骨架 + 动态版本可选 + 7 条要点）
  5. 工具链配置拆分（7 个文件职责表 + ruff.toml/pytest.ini/.coveragerc/pyrefly.toml 示例 + 6 条要点）
  6. 包内部结构（__init__.py/py.typed/__main__.py 模板 + 模块划分 + 5 条要点）
  7. 测试目录组织（目录结构 + conftest.py 层级示例 + 7 条要点）
  8. 文档目录组织（Sphinx 结构 + conf.py 完整配置 + ReadTheDocs + index.rst + 6 条要点）
  9. CI/CD 结构（ci.yml 4 jobs + release.yml OIDC + 9 条要点）
  10. 项目类型差异（library/cli/gui/web 4 种 src/ 入口与 dependencies + 3 条要点）
  11. 版本管理（.bumpversion.toml 配置 + bump 命令 + 5 条要点）
  12. 构建与发布（uv build + 本地验证 + PyPI 发布 + 6 条要点）
  13. Makefile（完整模板 + 5 条要点）
  14. 常见陷阱 15 条

- `template/.trae/skills/python-project-structure/SKILL.md`：与根目录内容一致，外加 `{% raw %}` / `{% endraw %}` 标记

## 整合优化情况

- 与 rule-11 工具链章节交叉引用：SKILL 提供完整示例与决策依据，rule-11 提供硬约束表（"配置文件"列）；二者互补不重复。
- 与 python-testing SKILL 交叉引用：SKILL 提供 tests/ 目录组织与 conftest 层级，python-testing 提供 fixture/mock/parametrize 细节。
- 与 python-cli/python-fastapi SKILL 交叉引用：SKILL 提供项目类型差异（cli/web 的 src/ 入口与 dependencies），具体框架开发调用对应 SKILL。
- 与 rule-12 PySide 规则交叉引用：SKILL 提供 gui 项目 src/ 骨架，rule-12 提供 GUI 开发硬约束。

## 测试验证结果

- `copier copy --trust --defaults --vcs-ref HEAD . .preview/lib`：渲染成功
- 渲染后 SKILL.md 行数：896（与根目录 894 行基本一致，多 2 行为 `{% raw %}` / `{% endraw %}` 剥离后留下的空行）
- Grep 验证：渲染后文件正确保留 `${{ github.workflow }}`/`${{ github.token }}`/`{{ version }}`/`{% if project_type == 'xxx' %}` 模式（未被 Jinja 渲染）
- 根目录与模板 SKILL.md 内容一致（仅模板版本多 `{% raw %}`/`{% endraw %}` 标记）
- 根目录与模板 rule-03-触发场景.md 内容一致

## 遗留事项

无。SKILL 完整覆盖项目骨架设计各方面，与现有 SKILL/rule 交叉引用清晰，渲染验证通过。

## 下一轮计划

无明确下一轮计划。当前 SKILL 目录共 12 个，覆盖项目骨架 + 9 个语言场景 + 2 个项目场景（GUI/Web），结构完整。后续可根据使用反馈补充或调整。
