# skill-13：PySide6 支持与版本区分（归档自 iter-13/req-13）

## 需求

- 模板 pyproject.toml gui 依赖按 Python 版本区分：
  - `PySide2>=5.15.2.1; python_version <= "3.10"`
  - `PySide6>=6.5.0; python_version >= "3.11"`
- main.py 模板兼容 PySide2/PySide6（try/except import + exec 兼容写法）
- copier.yml project_type=gui 的 help 文本和 choices 标签反映双绑定
- rule-12 规则更新（项目根 + 模板内），同时覆盖 PySide2 和 PySide6
- README 同步更新 project_type 说明
- bump 版本（feat → minor 0.3.0 → 0.4.0）+ 迁移 _commit v0.3.0 → v0.4.0

## 关键决策与依据

1. **按 Python 版本自动区分**：不增加 copier 变量让用户手选绑定，依赖环境标记 `python_version <= "3.10"` / `python_version >= "3.11"` 自动区分。pip/uv 按 Python 版本只安装其中一个。

2. **main.py 双兼容模式**：try/except import PySide2（首选，兼容旧 Python）→ 回退 PySide6。exec 用 `hasattr(app, "exec")` 检测，PySide2 用 `exec_()`，PySide6 用 `exec()`。

3. **API 差异速查表**：rule-12 新增 8 行表格列出 exec_/exec、枚举命名空间（Qt.AlignCenter → Qt.AlignmentFlag.AlignCenter 等）、import 路径差异，便于迁移参考。

4. **枚举兼容策略**：跨版本运行用短名（两代均支持，PySide6 发 DeprecationWarning）；仅 PySide6 用全路径。模板代码用短名。

5. **rule-12 文件名不变**：保持 `rule-12-pyqt-standards.md`，内容从 PySide2 专精扩展为 PySide2/PySide6 双覆盖。

## 验证结果

- ruff check / ruff format --check / pyrefly check：全绿
- pytest：42 passed, 100% coverage
- gui 模板渲染验证（rsync 副本 + copier copy --defaults）：dependencies 含两条环境标记、main.py try/except 兼容、rule-12 标题正确
- copier update -A：`Updating to template version 0.4.0`，无冲突

## 提交历史

```
8520df4 chore: 迁移 _commit v0.3.0 → v0.4.0（copier update 无冲突）
fdc8713 chore: 同步 uv.lock 至 0.4.0
b8874d7 chore: 更新版本 0.3.0 → 0.4.0  (tag: v0.4.0)
344343d feat: gui 项目类型增加 PySide6 支持，按版本版本区分绑定
```
