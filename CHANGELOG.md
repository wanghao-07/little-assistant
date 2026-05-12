# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 添加 API 接口 `/api/v1/metrics` 用于获取性能指标
- 添加缓存机制，支持查询结果缓存
- 添加性能监控模块，跟踪响应时间和查询次数

### Changed
- 优化文档分割算法，提高检索准确性
- 改进错误处理，提供更详细的错误信息

### Fixed
- 修复 PDF 文件加载编码问题
- 修复向量库重建时的内存泄漏问题

## [1.0.0] - 2024-01-15

### Added
- 初始版本发布
- 支持通义千问 (Qwen-Max/Qwen-Turbo) 模型
- 支持 OpenAI GPT 模型
- 添加文档加载功能（PDF/DOCX/TXT）
- 实现向量数据库管理（Chroma/FAISS）
- 添加 RAG 问答链
- 实现 FastAPI RESTful API
- 添加单元测试（测试覆盖率 85%+）

### Changed
- 使用 Pydantic 2.x 进行数据验证
- 升级 LangChain 到 0.1.x 版本

### Fixed
- 修复文档分割时的空片段问题
- 修复缓存键生成的大小写敏感问题
