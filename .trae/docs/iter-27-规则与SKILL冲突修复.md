# iter-27：规则与 SKILL 冲突修复

## 需求清单

- [x] P0-C1：python-performance SKILL GitHub Actions 版本更新
- [x] P1-C3：python-testing SKILL 内部 pytest.ini 去重
- [x] P1-R1：python-project-structure SKILL 移除 .coveragerc 重复示例
- [x] P2-C2：测试目录结构在两 SKILL 间统一
- [x] P2-D1+P3-R2：rule-11 加 SKILL 反向引用
- [x] P3-D2：rule-12 加 python-gui-pyside SKILL 引用
- [x] P3-D3：rule-01 暂停条件补 `.pre-commit-config.yaml`
- [x] P4-S2：rule-01 加 rule-02 例外注解
- [x] 验证：copier copy 渲染测试 + SKILL 同步性检查

## 迭代目标

按上轮冲突检查报告的优先级（P0-P4）系统性修复 11 项规则与 SKILL 冲突，建立 rule ↔ SKILL 双向引用网，消除跨文档重复与目录结构不一致，使规则与 SKILL 形成清晰的"硬约束简表（rule）→ 详细模式与代码模板（SKILL）"层级关系。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `.trae/skills/python-performance/SKILL.md` | 修改 | GitHub Actions 版本更新（checkout@v5/setup-uv@v8.3.2）+ enable-cache + cache-dependency-glob |
| `template/.trae/skills/python-performance/SKILL.md` | 修改 | 同步根目录变更（Copy-Item 覆盖，无 Jinja 模板化） |
| `.trae/skills/python-testing/SKILL.md` | 修改 | 合并"标记注册"与"测试配置文件"章节（消除内部 pytest.ini 重复）；测试目录树补 `gui/` 与 `fixtures/` |
| `template/.trae/skills/python-testing/SKILL.md` | 修改 | 同步根目录变更（保留 `{{ package_name }}` 等 Jinja 变量） |
| `.trae/skills/python-project-structure/SKILL.md` | 修改 | pytest.ini 示例升级为完整版（addopts/gui marker）+ 引用 python-testing；.coveragerc 示例后加引用；测试目录树补 `gui/`；测试章节末尾加引用 |
| `template/.trae/skills/python-project-structure/SKILL.md` | 修改 | 同步根目录变更（`{% raw %}` 包裹保留） |
| `.trae/rules/rule-11-python-standards.md` | 修改 | 工具链章节末尾加"详细参考"引用块；文件末尾加「详细参考」附录表（rule → SKILL 章节对应表） |
| `template/.trae/rules/rule-11-python-standards.md` | 修改 | 同步根目录变更（保留 `{{ package_name }}`/`{{ coverage_fail_under }}` 等 Jinja 变量） |
| `.trae/rules/rule-12-pyside-dev.md` | 修改 | 末尾加「详细参考」章节（指向 gui-pyside SKILL 四文档） |
| `template/.trae/rules/rule-12-pyside-dev.md` | 修改 | 同步根目录变更 |
| `.trae/rules/rule-01-开发流程.md` | 修改 | 暂停条件第 2 条括号内补 `.pre-commit-config.yaml`；新增"修改 `.trae/rules/` 下规则文件（见 rule-02 规则变更约束）" |
| `template/.trae/rules/rule-01-开发流程.md` | 修改 | 同步根目录变更 |
| `.trae/req/req-27-规则与SKILL冲突修复.md` | 新建 | 需求记录 |

## 关键决策与依据

1. **P0-C1 升级到 actions/checkout@v5 + setup-uv@v8.3.2**：v5 是 2025 年最新稳定版（Node 24 runtime、sparse checkout 支持）；setup-uv@v8.3.2 是 astral-sh/setup-uv 当前最新稳定版，支持 `enable-cache` 与 `cache-dependency-glob` 参数；与 coopie 自身 CI 配置一致。

2. **P1-C3 合并而非删除**：python-testing SKILL 原有"标记注册"与"测试配置文件"两章节都展示 pytest.ini 示例。选择保留"测试配置文件"章节的完整示例（含 addopts/asyncio_default_fixture_loop_scope），“标记注册”章节改为只描述 markers 字段含义并加引用指向完整示例，避免删除信息。

3. **P1-R1 改为引用而非删除**：python-project-structure 的 `.coveragerc` 示例与 python-testing 重复。选择保留 python-project-structure 的示例（作为工具链配置拆分章节的完整骨架）+ 添加引用"详细说明见 python-testing"，而非完全删除（删除会让工具链拆分章节缺一个文件示例）。同时升级示例为完整版（含 `omit`/`exclude_lines`/`show_missing`）。

4. **P2-C2 测试目录树统一**：python-testing 原有 `gui/` 但缺 `fixtures/`；python-project-structure 原有 `fixtures/` 但缺 `gui/`。统一为 `unit/integration/gui/fixtures/` 四子目录，两 SKILL 完全一致。

5. **P2-D1+P3-R2 rule-11 加附录表**：rule-11 共 16 章节，原本只在 rule-03 单向引用 SKILL。在 rule-11 末尾加章节对应表，让规则读者一眼看到每个章节对应的 SKILL；同时在工具链章节末尾加 inline 引用（最常查阅的章节优先 inline 引用）。

6. **P3-D2 rule-12 末尾加引用**：与 rule-11 同样模式，简短一段指向 gui-pyside SKILL 四文档（SKILL.md / UI-DESIGN.md / LAYOUT.md / PATTERNS.md）。

7. **P3-D3 补 `.pre-commit-config.yaml` 文件名**：原 rule-01 第 2 条表述为"修改 pre-commit/工具链配置文件（ruff.toml/pytest.ini/.coveragerc/pyrefly.toml/.bumpversion.toml/uv.toml）"——"pre-commit"提了概念但括号内未列文件名，与括号内其他文件命名风格不一致。补 `.pre-commit-config.yaml` 让括号内列表完整。

8. **P4-S2 rule-02 例外注解**：rule-02 规则变更约束规定"修改 `.trae/rules/` 下文件必须先询问用户"，但 rule-01 暂停条件第 2 条未提及规则文件，导致 rule-01 与 rule-02 存在隐性冲突。在 rule-01 第 2 条补"修改 `.trae/rules/` 下规则文件（见 `rule-02-产物约束.md` 规则变更约束）"，建立跨规则引用，消除冲突。

9. **根目录与 template 双份同步**：coopie 同时维护根 `.trae/`（coopie 自身用）与 `template/.trae/`（copier 模板用）两份规则与 SKILL。所有修改均同步两份，Jinja 模板化 SKILL（python-testing/python-project-structure）保留 `{{ package_name }}`/`{% raw %}` 标记，非 Jinja SKILL（python-performance）直接 Copy-Item 覆盖。

## 代码实现情况

### P0-C1：python-performance SKILL GitHub Actions 版本更新

- `actions/checkout@v4` → `actions/checkout@v5`
- `astral-sh/setup-uv@v3` → `astral-sh/setup-uv@v8.3.2`
- 添加 `enable-cache: true` 与 `cache-dependency-glob: "uv.lock"` 参数

### P1-C3：python-testing SKILL 内部 pytest.ini 去重

原"标记注册"章节包含完整 pytest.ini 示例，与下文"测试配置文件"章节重复。改为：

```
### 标记注册
`pytest.ini` 的 `markers` 字段注册标记，配合 `--strict-markers` 在拼写错误时直接失败。
完整 `pytest.ini` 示例见下文「测试配置文件」章节。

要点：
- `slow`：慢测试（I/O、网络、集成），默认 `-m "not slow"` 跳过。
- `gui`：GUI 项目用，需 Qt 环境；CI 与无头环境用 `-m "not gui"` 隔离。
- 新增标记必须在此注册，否则 `--strict-markers` 直接报错。
- `--strict-config` 让解析阶段的配置错误也视为失败。
```

### P1-R1：python-project-structure SKILL .coveragerc 引用

`.coveragerc` 示例后添加引用块：

```
> 覆盖率排除规则与 `# pragma: no cover` 详细说明见 `python-testing` SKILL「覆盖率」章节。
```

同时升级 .coveragerc 示例为完整版（含 `omit = tests/*` / `exclude_lines` / `show_missing = true`）。

### P2-C2：测试目录结构统一

两 SKILL 测试目录树统一为：

```
tests/
├── __init__.py
├── conftest.py
├── unit/
│   ├── __init__.py
│   └── test_*.py
├── integration/
│   ├── __init__.py
│   └── test_*.py
├── gui/                  # GUI 测试（仅 GUI 项目，标 @pytest.mark.gui）
│   ├── __init__.py
│   └── test_main_window.py
└── fixtures/             # 测试数据（JSON/CSV/二进制）
    └── sample.json
```

### P2-D1+P3-R2：rule-11 SKILL 反向引用

工具链章节末尾添加 inline 引用：

```
详细参考：工具链配置拆分决策与完整示例见 `python-project-structure` SKILL「工具链配置拆分」章节；
覆盖率排除规则与 `# pragma: no cover` 见 `python-testing` SKILL「覆盖率」章节。
```

文件末尾添加附录表：

```
## 详细参考

本规则为硬约束简表，各领域详细模式与代码模板见对应 SKILL（调用指引见 `rule-03-触发场景.md`）：

| 章节 | 对应 SKILL |
|------|-----------|
| 工具链 | `python-project-structure`（工具链配置拆分）、`python-testing`（覆盖率） |
| 数据结构 | `python-class-design` |
| 并发 | `python-concurrency` |
| 测试 | `python-testing` |
| 日志 | `python-logging` |
| 路径与资源 | `python-file-io` |
| 安全（subprocess） | `python-subprocess` |
| 性能 | `python-performance` |
| 项目骨架 | `python-project-structure` |
| 配置管理 | `python-config` |
| CLI 入口 | `python-cli` |
```

### P3-D2：rule-12 末尾加引用

```
## 详细参考

本规则为硬约束简表，详细设计令牌、四区布局规范、UI 设计规范、实现模式与代码模板见 `gui-pyside` SKILL
（含 SKILL.md / UI-DESIGN.md / LAYOUT.md / PATTERNS.md 四文档，调用指引见 `rule-03-触发场景.md`）。
```

### P3-D3 + P4-S2：rule-01 暂停条件第 2 条补全

```
2. **高风险/不可逆**：删除非临时文件、重命名公共模块/包、`force-push`、`reset --hard`（工作区有未提交改动时）、
   `git clean -f`/`-fd`/`-fx`、修改 CI/git config、引入新依赖、
   修改 pre-commit/工具链配置文件（.pre-commit-config.yaml/ruff.toml/pytest.ini/.coveragerc/pyrefly.toml/.bumpversion.toml/uv.toml）、
   修改 `.trae/rules/` 下规则文件（见 `rule-02-产物约束.md` 规则变更约束）、
   卸载或降级既有依赖。**普通 commit/push 不属于此类**（自动执行）。
```

## 整合优化情况

- 建立 rule ↔ SKILL 双向引用网：rule-03（SKILL → rule 触发调度）+ rule-11/rule-12 末尾附录（rule → SKILL 详细参考），形成完整闭环。
- 消除跨文档重复：python-project-structure 的 .coveragerc/pytest.ini 示例通过引用方式与 python-testing 协同，避免维护时遗漏同步。
- 消除 SKILL 内部重复：python-testing 的"标记注册"与"测试配置文件"章节合并为引用关系。
- 统一测试目录结构：两 SKILL 测试目录树完全一致，便于跨文档引用。
- 修复 rule-01 与 rule-02 隐性冲突：暂停条件第 2 条显式列出 `.trae/rules/` 例外。
- 修复 rule-01 括号内列表不完整：补 `.pre-commit-config.yaml` 文件名。

## 测试验证结果

- `make render` 4 种 project_type（library/cli/gui/web）全部渲染成功，无 Jinja 错误。
- 渲染后 `.preview/lib/.trae/rules/rule-01-开发流程.md` 第 45 行包含 `.pre-commit-config.yaml` 与 `.trae/rules/` 例外注解 ✓
- 渲染后 `.preview/lib/.trae/rules/rule-11-python-standards.md` 末尾包含「详细参考」附录表 ✓
- 渲染后 `.preview/lib/.trae/rules/rule-12-pyside-dev.md` 末尾包含「详细参考」章节 ✓
- 根目录与 template 同步性检查：
  - rule-01/rule-12: 内容完全相同 ✓
  - rule-11: 仅 Jinja 变量差异（`{{ target_py }}` vs `"py38"` 等），符合预期 ✓
  - python-performance: hash 完全相同 ✓
  - python-subprocess: 仅 Jinja 变量差异（`{{ package_name }}` vs `coopie`），符合预期 ✓
  - python-config/python-logging: hash 不同但 Compare-Object 输出为空（CRLF/LF 历史遗留，不影响本轮）

## 遗留事项

- python-config 与 python-logging SKILL 在根目录与 template 目录存在 CRLF/LF 行尾差异（hash 不同但内容相同），是历史遗留问题，不在本轮修复范围。建议后续用 `.gitattributes` 强制 LF 统一处理。

## 下一轮计划

无明确下一轮计划。本轮修复完成后，规则与 SKILL 之间形成清晰的双向引用网，跨文档重复已消除，目录结构已统一。后续可根据使用反馈继续补充或调整。
