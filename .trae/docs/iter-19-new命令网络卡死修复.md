# iter-19：`new` 命令网络卡死修复

## 迭代目标

修复 `coopie new` 因国内访问 GitHub 不稳定导致 `git clone` 模板仓库超时卡死的问题。附带修复 `RUST_LOG=info`（Trae IDE 设置）导致 `uv` 输出大量 PubGrub 解析日志污染输出的现象。

## 根因分析

证据链：
- `uvx copier --version` 0.9 秒返回 → uvx/依赖解析不卡
- `copier copy <github> ...` 60 秒超时无输出 → 卡在 copier copy 阶段
- `git clone https://github.com/gookeryoung/coopie` 30 秒超时 → 卡在 git clone GitHub

直接原因：[cli.py](../../src/coopie/cli.py) 硬编码 `_TEMPLATE_REPO = "https://github.com/gookeryoung/coopie"`，且 `subprocess.run(cmd, check=True)` 无 timeout，国内网络下拉取 GitHub 仓库无限等待。
附带原因：环境变量 `RUST_LOG=info` 让 `uv`（Rust 实现）输出 `INFO add_decision` PubGrub 解析日志，干扰诊断。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `src/coopie/cli.py` | 重构 | `_TEMPLATE_REPO` → `_DEFAULT_TEMPLATE_REPO` 常量；新增 `_TEMPLATE_ENV_VAR`/`_COPIER_TIMEOUT`；新增 `_resolve_template_repo()` 解析优先级；新增 `_run_copier()` 统一处理 timeout + env 覆盖；`new`/`init` 加 `--template` 选项 |
| `tests/test_cli.py` | 扩展 | 新增 15 个测试覆盖 `_resolve_template_repo`/`--template` 解析/`_run_copier` timeout+env/`main` 模板源传递 |
| `README.md` | 文档 | CLI 命令段补充 `--template` 和 `COOPIE_TEMPLATE_REPO` 用法（含国内镜像示例） |
| `docs/index.rst` | 文档 | 用法段补充 `--template` 和环境变量说明 |
| `.trae/skills/skill-15-req清理规则优化与PyPI-badge调查.md` | 新建 | 归档自 iter-15/req-15（阈值触发） |

## 关键决策与依据

1. **方案选择：支持自定义模板源（非默认改镜像）**：默认仍用 GitHub 不影响国外用户；国内用户通过 `--template` 或 `COOPIE_TEMPLATE_REPO` 指定镜像/本地路径。优先级：`--template` > 环境变量 > 默认。

2. **`_run_copier` 统一封装**：`new`/`init`/`update`/`test` 四个子命令都调用 `uvx copier`，统一通过 `_run_copier` 注入 `timeout=600` 和 `env={**os.environ, "RUST_LOG": "warning"}`，避免重复且保证一致。

3. **timeout 取 600 秒**：git clone 慢网络通常 1-2 分钟内能完成或失败，600 秒足够宽容；超时后提示用户用 `--template` 指定本地/镜像源，给出可操作建议。

4. **`RUST_LOG=warning` 覆盖而非删除**：`env = {**os.environ, "RUST_LOG": "warning"}` 保留父进程其他环境变量，仅降级 RUST_LOG。用户显式设 `RUST_LOG=debug` 调试时会被覆盖，但符合"在 coopie 内静默 uv 日志"的需求。

5. **空环境变量忽略**：`os.environ.get()` 返回空字符串时 `if env_value:` 为 False，退回默认，避免 `COOPIE_TEMPLATE_REPO=""` 误用空值。

## 验证结果

- ruff check / ruff format --check / pyrefly check：全绿
- pytest：57 passed（新增 15 个），100% coverage
- 实际验证：
  - `coopie new --template /home/zhou/coopie`：1.08 秒返回，不再卡住
  - `copier copy --defaults --template /home/zhou/coopie`：1.04 秒生成完整项目结构
  - RUST_LOG 日志已静默（无 `INFO add_decision` 输出）
- 单元测试覆盖 `subprocess.TimeoutExpired` 捕获与 `sys.exit(1)` 提示路径

## 遗留事项

- `coopie new` 在 stdin 非 tty 时（如 CI）会因 copier 要求交互而失败，需透传 `--defaults` 或提供所有 `--data`。当前未暴露 `--defaults` 选项，CI 场景暂未要求，记为后续可扩展点。
- 默认 GitHub 源在国外网络正常，国内用户需手动指定镜像或本地路径。未来可考虑自动探测或内置镜像回退，但当前手动配置足够。
