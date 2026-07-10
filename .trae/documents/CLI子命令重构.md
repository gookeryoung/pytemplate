# iter-11：CLI 子命令重构收尾

## 摘要

将 coopie CLI 从旧接口（`coopie <name>` + `coopie -U`）完全迁移到子命令模式（`new`/`init`/`update`/`test`）。cli.py 和 test_cli.py 已在前序上下文中重写完成，本计划覆盖剩余工作：更新文档、验证、发布。

## 当前状态分析

### 已完成（前序上下文）

- **[src/coopie/cli.py](file:///home/zhou/coopie/src/coopie/cli.py)**：已完全重写为子命令模式
  - `new <project_name>`：copier copy 到子目录，传 project_name + author 数据
  - `init`：copier copy 到当前目录，project_name 从目录名派生，非空目录提示确认（y/N）
  - `update [-A] [-T]`：copier update + 可选 skip 标志
  - `test [-A] [-T]`：copier update --pretend（dry-run）+ 可选 skip 标志
  - `-V`/`--version`：版本号
- **[tests/test_cli.py](file:///home/zhou/coopie/tests/test_cli.py)**：已完全重写，约 30 个测试覆盖所有分支
  - ruff 配置（pyproject.toml L118）已忽略 tests 目录的 ARG001/ARG002，mock 辅助函数的未使用参数不会报错

### 待完成

- **README.md L25-60**：仍是旧用法（`uvx coopie my-new-project`、`coopie -U`、旧 CLI 选项表），需更新为子命令
- **docs/index.rst L54-70**：仍是旧用法（`uvx coopie my-new-project`、`coopie -U -A`），需同步更新
- 验证（ruff/pyrefly/pytest）尚未运行
- 迭代文档（.trae/docs/iter-11-CLI子命令重构.md）尚未创建
- 需求文件（req-11）未标记完成项
- bump + push 未执行
- memory 未更新

## 改动计划

### 1. 更新 README.md（L25-60）

将"用法"段和"CLI 选项"表替换为子命令模式：

**用法段**（替换 L25-60）：
- 简介：说明采用子命令模式，封装 copier copy/update，自动从 git 配置读取作者信息
- 创建新项目：`coopie new my-new-project`（替代 `uvx coopie my-new-project`）
- 在当前目录初始化：`coopie init`（新增，project_name 从目录名派生，非空目录提示确认）
- 更新已有项目：`coopie update`、`coopie update -A`、`coopie update -T`（替代 `coopie -U`）
- 模拟检查更新冲突：`coopie test`、`coopie test -A -T`（新增 dry-run 模式）

**CLI 子命令表**（替换旧"CLI 选项"表 L52-60）：
| 命令 | 说明 |
|------|------|
| `coopie new <project_name>` | 新建项目（建立子文件夹） |
| `coopie init` | 在当前目录初始化项目 |
| `coopie update [-A] [-T]` | 更新当前目录中的已生成项目模板 |
| `coopie test [-A] [-T]` | 模拟检查模板更新是否产生冲突 |
| `coopie -V` / `--version` | 显示版本号 |

### 2. 更新 docs/index.rst（L54-70）

RST 格式同步 README 的子命令用法：
- 创建新项目：`coopie new my-new-project`
- 在当前目录初始化：`coopie init`
- 更新已有项目：`coopie update`、`coopie update -A`
- 模拟检查更新冲突：`coopie test`

### 3. 验证

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run pyrefly check
uv run pytest -m "not slow" --cov=coopie --cov-fail-under=95
```

预期全绿，覆盖率 100%（cli.py 所有分支已覆盖）。

### 4. copier update 验证

```bash
uvx copier update -A
```

预期无冲突（本次仅改项目自身文档，模板未变，应输出 "Keeping template version 0.2.2"）。

### 5. 创建迭代文档

创建 `.trae/docs/iter-11-CLI子命令重构.md`，记录：迭代目标、改动文件清单（cli.py/test_cli.py/README.md/docs/index.rst）、关键决策（完全迁移、init 确认后生成、test 用 --pretend）、验证结果、遗留事项。

### 6. 更新需求文件

将 `.trae/req/req-11-CLI子命令重构.md` 中已完成的项标记为 `[x]`（项 1-8），未完成的保持 `[]`（项 9-11 待验证和发布后标记）。

### 7. bump + push

```bash
make bump   # 0.2.3 → 0.2.4（patch）
make push   # git push && git push --tags
```

commit message 遵循 rule-09（中文）：
```
refactor: CLI 重构为子命令模式（new/init/update/test）
```

### 8. 更新 memory

更新 project_memory.md：追加 iter-11 记录，更新"关键约定"段补充子命令模式说明。

## 假设与决策

- **完全迁移**：移除旧接口（`coopie <name>` 和 `coopie -U`），只支持子命令模式（用户已确认）
- **init 确认后生成**：非空目录时提示用户确认（y/N），默认取消（用户已确认）
- **test 命令用 --pretend**：copier update --pretend 是 dry-run，不修改文件，适合"模拟检查冲突"
- **README 不改"可配置选项"和"生成文件清单"段**：这些描述模板配置，与 CLI 接口无关
- **版本号 0.2.3 → 0.2.4**：CLI 接口重构是面向用户的变化，patch bump 合适（非破坏性 API 变更，因为旧用法本就是内部工具）

## 验证步骤

1. ruff check + format --check 全绿
2. pyrefly check 全绿
3. pytest 全绿，覆盖率 >= 95%（预期 100%）
4. copier update 无冲突
5. README/docs 内容与 cli.py 实际行为一致
