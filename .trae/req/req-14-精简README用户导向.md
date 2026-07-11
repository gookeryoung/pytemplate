# iter-14 需求：精简 README 用户导向

## 背景

项目根 README（1-175 行）偏技术特点罗列（特性清单、文件树、设计依据），
用户希望精简为用户导向：突出"怎么用"而非"包含什么技术"。

## 需求

- [x] 精简 README，删除/压缩非用户导向段落（特性清单、文件清单、设计依据）
- [x] 突出快速开始、CLI 命令、可配置选项、生成后步骤
- [x] 修正 use_docker 默认值（copier.yml 为 false，README 误写 true）
- [x] 提交并推送

## 约束

- 仅改项目根 README.md，不动模板 README
- 模板未变，无需 bump / copier update
- 标准门禁（README 不参与 lint，但确认不破坏现有测试）

## 验收标准

- README 行数显著减少（目标 ≤ 80 行）
- 结构：快速开始 → CLI 命令 → 可配置选项 → 生成后 → 许可证
- use_docker 默认值与 copier.yml 一致（false）
