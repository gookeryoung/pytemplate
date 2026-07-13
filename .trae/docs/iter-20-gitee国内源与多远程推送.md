# iter-20：Gitee 国内源与多远程推送

## 迭代目标

1. 将 CLI 默认模板源从 GitHub 切换为 Gitee（国内访问稳定）
2. Makefile `push` 目标改为遍历 `git remote`，不硬编码远程名（用户项目模板需兼容自定义远程名）
3. 同步更新测试、文档、`.copier-answers.yml`

## 改动文件清单

| 文件 | 改动 |
|------|------|
| `src/coopie/cli.py` | docstring "GitHub" → "Gitee"（`_DEFAULT_TEMPLATE_REPO` 已在 69465fa 切到 Gitee） |
| `Makefile` | `push` 目标改为 `for remote in $$(git remote)` 遍历，不硬编码远程名 |
| `template/Makefile` | 同上（用户项目模板同步） |
| `.copier-answers.yml` | `_src_path` 改为 Gitee URL；`_commit` 迁移 v0.5.0 → v0.6.0 |
| `tests/test_cli.py` | 4 处 GitHub URL 断言改为 Gitee URL（`.git` 后缀） |
| `README.md` | 默认源说明改为 Gitee，GitHub 作为 `--template` 备选 |
| `docs/index.rst` | 同上 |

## 关键决策与依据

### 1. 默认源选 Gitee 而非 GitHub

- **依据**：国内访问 GitHub 不稳定，iter-19 已确认会导致 `coopie new` 卡死
- **Gitee URL 形式**：`https://gitee.com/gooker_young/coopie.git`（带 `.git` 后缀，与 git clone 兼容）
- **保留 `--template`/`COOPIE_TEMPLATE_REPO`**：用户可覆盖默认源走 GitHub 或本地路径

### 2. Makefile push 遍历 `git remote` 不硬编码远程名

- **用户反馈**："作为模板需要考虑远程名称可能不是gitee的情况，不要硬编码"
- **实现**：`for remote in $$(git remote); do git push $$remote; git push $$remote --tags; done`
- **优点**：
  - 自动发现所有远程，无需维护远程名列表
  - 适用于远程名不叫 "gitee"/"origin" 的用户场景
  - 无远程时循环体不执行（无错误）
- **`set -e`**：任一远程推送失败立即停止

### 3. 版本 bump 0.5.0 → 0.6.0（minor）

- 默认源切换是行为变更（breaking change for users expecting GitHub default）
- Makefile push 行为变更（从单远程到多远程）
- 故用 minor bump 而非 patch

## 验证结果

- `make check`：ruff + pyrefly + pytest 全部通过，覆盖率 100%
- `copier update --pretend -A`：`Keeping template version 0.6.0`（无冲突）
- `git remote` + `make -n push`：正确展开为遍历所有远程的命令

## 遗留事项

- **Gitee 仓库仍为私有**：用户已确认将设为公开，但当前 HTTPS 匿名 clone 仍被拒（`Authentication failed`）。设为公开后 `coopie new` 默认源才能正常工作。临时方案：`coopie new my-project --template https://github.com/gookeryoung/coopie`
- **GitHub Actions badge**：README/docs 中的 CI badge 仍指向 GitHub Actions（合理，因为 CI 跑在 GitHub）
