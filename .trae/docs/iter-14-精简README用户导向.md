# iter-14：精简 README 用户导向

## 迭代目标

精简项目根 README（175 行），从技术特点罗列改为用户导向结构。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `README.md` | 重写 | 175→77 行；删除特性清单/文件树/设计依据；结构改为快速开始→CLI命令→可配置选项→生成后→许可证；修正 use_docker 默认值 true→false |

## 关键决策

1. **删除特性清单**：技术特点折叠到 intro 一句话（"构建工具链（uv + ruff + pyrefly + pytest）、CI/CD、文档与测试"），用户关心的是怎么用而非包含什么。
2. **删除文件树**：用户生成后自见，无需提前罗列 35 行树。
3. **删除设计依据**：内部决策（src layout 选型等）不属于用户导向内容。
4. **修正 use_docker 默认值**：copier.yml 为 `false`，README 误写 `true`，顺带修正。
5. **author_name/email 默认值改为"git 配置"**：更准确反映 CLI 自动填充行为。

## 验证结果

- pytest 42 passed, 100% coverage（README 不参与 lint，确认不破坏现有测试）
- 模板未变，无需 bump / copier update
