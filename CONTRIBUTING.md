# Contributing

欢迎贡献代码！我们欢迎所有形式的贡献，包括代码修复、新功能、文档改进等。

## 开发流程

### 1. Fork 项目

首先，在 GitHub 上 Fork 此项目到您自己的账户。

### 2. 克隆仓库

```bash
git clone https://github.com/your-username/little-assistant.git
cd little-assistant
```

### 3. 创建分支

为您的功能或修复创建一个新分支：

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/issue-number
```

### 4. 开发

在本地进行开发，确保：
- 代码遵循 PEP 8 规范
- 添加适当的单元测试
- 更新相关文档

### 5. 提交

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式提交：

```bash
git add .
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update documentation"
```

### 6. 推送

```bash
git push origin feature/your-feature-name
```

### 7. 创建 Pull Request

在 GitHub 上创建 Pull Request，描述您的更改。

## 代码规范

### Python 代码规范

- 使用 Python 3.10+ 语法
- 遵循 PEP 8 规范
- 使用类型注解
- 使用 `black` 进行代码格式化
- 使用 `isort` 进行导入排序

### 提交信息格式

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**类型**：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `refactor`: 代码重构（不影响功能）
- `test`: 测试相关
- `chore`: 构建/工具更新
- `style`: 代码风格调整

**示例**：
```
feat(rag): add multi-query retrieval support

- 添加多查询检索功能
- 优化检索精度

Closes #123
```

## 测试

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_document_processor.py -v

# 带覆盖率报告
pytest tests/ -v --cov=core --cov-report=html
```

### 添加测试

所有新功能都应该有对应的单元测试。测试文件放在 `tests/` 目录下。

## 问题报告

如果您发现 Bug 或有功能建议，请在 GitHub Issues 中提交。

## 行为准则

请参考 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

---

感谢您的贡献！🎉
