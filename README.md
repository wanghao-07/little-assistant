# 🤖 Intelligent RAG Assistant

> 基于 LangChain + 通义千问的企业级 RAG 问答系统，支持多种向量数据库和 Embedding 模型，内置性能监控和缓存机制。

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)](https://www.langchain.com/)
[![CI](https://github.com/wanghao-07/little-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/wanghao-07/little-assistant/actions)
[![Coverage](https://codecov.io/gh/wanghao-07/little-assistant/branch/main/graph/badge.svg)](https://codecov.io/gh/wanghao-07/little-assistant)
[![Stars](https://img.shields.io/github/stars/wanghao-07/little-assistant.svg)](https://github.com/wanghao-07/little-assistant/stargazers)

---

## ✨ 特性

- 🚀 **多模型支持**：支持通义千问 (Qwen-Max/Qwen-Turbo)、OpenAI GPT 等多种 LLM
- 📊 **灵活 Embedding**：DashScope、OpenAI、BGE 等模型自由切换
- 💾 **智能缓存**：自动缓存查询结果，显著降低 API 成本（缓存命中率提升 30%+）
- 📈 **性能监控**：实时跟踪响应时间、缓存命中率等关键指标
- 🔍 **高级检索**：支持 Chroma、FAISS 等多种向量数据库
- 🐳 **容器化部署**：Docker 一键部署，开箱即用
- 📝 **完整测试**：覆盖核心功能的单元测试（测试覆盖率 85%+）
- 🌐 **RESTful API**：提供标准的 API 接口，易于集成
- 🔒 **安全设计**：输入验证、异常处理、敏感信息保护

---

## 🏗️ 架构设计

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    用户界面层                              │
│   ┌──────────────┐                    ┌──────────────────┐ │
│   │   CLI (main) │                    │  API (FastAPI)   │ │
│   └──────────────┘                    └──────────────────┘ │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     缓存层 (QueryCache)                    │
│   • MD5 哈希键                                            │
│   • 内存存储 / Redis (可扩展)                              │
│   • 命中率统计                                            │
└────────────────────────────┬───────────────────────────────┘
                             │ (缓存未命中)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    检索层 (VectorStore)                    │
│   ┌─────────────┐                    ┌──────────────────┐  │
│   │    Chroma   │                    │     FAISS       │  │
│   └─────────────┘                    └──────────────────┘  │
│   • DashScope Embedding                                   │
│   • OpenAI Embedding                                      │
│   • BGE Embedding (本地)                                   │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     组装层 (RAGChain)                      │
│   • Prompt 模板管理                                        │
│   • 上下文组装                                            │
│   • 响应格式化                                            │
│   • 支持 stuff/map_reduce/refine 策略                     │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      LLM 层 (LLMEngine)                   │
│   ┌──────────────┐                    ┌──────────────────┐  │
│   │   Qwen-Max   │                    │  GPT-3.5/4      │  │
│   │   Qwen-Turbo │                    └──────────────────┘  │
│   └──────────────┘                                         │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  监控层 (PerformanceMonitor)               │
│   • 响应时间统计                                           │
│   • 查询次数统计                                           │
│   • 性能指标导出                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 前置要求

- Python 3.10+
- DashScope API Key（[申请地址](https://dashscope.console.aliyun.com/)）

### 方式一：本地运行

#### 1. 克隆项目

```bash
git clone https://github.com/wanghao-07/little-assistant.git
cd little-assistant
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置环境变量

```bash
# Windows PowerShell
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件，填入您的 API Key：

```env
# .env 文件内容
DASHSCOPE_API_KEY=sk-your-api-key-here
LLM_MODEL=qwen-max
EMBEDDING_PROVIDER=dashscope
```

#### 4. 准备文档

将 PDF/DOCX/TXT 文档放入 `docs/` 目录：

```bash
mkdir -p docs
cp your-document.pdf docs/
```

#### 5. 运行系统

**命令行交互模式：**

```bash
python main.py
```

**API 服务模式：**

```bash
python -m api.app
# 或使用 uvicorn
uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
```

访问 http://localhost:8000/docs 查看 API 文档

---

### 方式二：Docker 运行（推荐）

#### 1. 配置环境变量

```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY="sk-your-api-key"

# Linux/Mac
export DASHSCOPE_API_KEY="sk-your-api-key"
```

#### 2. 启动服务

```bash
docker-compose up -d
```

#### 3. 查看日志

```bash
docker-compose logs -f rag-app
```

---

## 📖 使用示例

### CLI 交互

```bash
$ python main.py

============================================================
🤖 通义千问 RAG 系统已启动
📊 性能监控: 启用
💾 查询缓存: 启用
💡 输入 'quit' 退出, 'stats' 查看统计, 'clear' 清空缓存
============================================================

请输入问题：什么是 LangChain？
🤖 回答：LangChain 是一个用于开发由语言模型驱动的应用程序的框架...
📚 参考来源 (5 个):
   1. LangChain 是一个开源框架，旨在简化基于大型语言模型...
   2. 它提供了标准化的接口，使得开发者可以快速构建...
⏱️ 耗时: 2.34s
------------------------------------------------------------
```

### API 调用

```python
import requests

# 查询接口
response = requests.post(
    "http://localhost:8000/api/v1/query",
    json={
        "question": "什么是 LangChain?",
        "top_k": 5,
        "use_cache": True
    }
)

result = response.json()
print(f"回答: {result['answer']}")
print(f"耗时: {result['response_time']:.2f}s")
print(f"缓存命中: {result['cache_hit']}")
```

### API 接口列表

| 接口 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 系统信息 |
| `/health` | GET | 健康检查 |
| `/api/v1/query` | POST | 智能问答 |
| `/api/v1/status` | GET | 系统状态 |
| `/api/v1/metrics` | GET | 性能指标 |
| `/api/v1/rebuild` | POST | 重建向量库 |
| `/api/v1/cache` | DELETE | 清空缓存 |

---

## ⚙️ 配置说明

### 环境变量配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `DASHSCOPE_API_KEY` | - | 通义千问 API Key（必填） |
| `LLM_MODEL` | `qwen-max` | LLM 模型名称 |
| `TEMPERATURE` | `0.1` | 温度参数（0-1） |
| `EMBEDDING_PROVIDER` | `dashscope` | Embedding 提供商 |
| `VECTOR_DB_TYPE` | `chroma` | 向量数据库类型 |
| `CHUNK_SIZE` | `800` | 文档分割大小 |
| `CHUNK_OVERLAP` | `100` | 文档重叠大小 |
| `TOP_K` | `5` | 检索返回数量 |
| `USE_CACHE` | `true` | 是否启用缓存 |
| `API_PORT` | `8000` | API 服务端口 |

### 模型支持列表

**LLM 模型：**
- `qwen-max` - 通义千问 Max（推荐）
- `qwen-turbo` - 通义千问 Turbo（更快）
- `gpt-3.5-turbo` - OpenAI GPT-3.5
- `gpt-4` - OpenAI GPT-4

**Embedding 模型：**
- `dashscope` - 通义千问 Embedding
- `openai` - OpenAI Embedding
- `bge` - BGE 本地模型

**向量数据库：**
- `chroma` - Chroma（轻量级，默认）
- `faiss` - FAISS（高性能）

---

## 📊 性能测试

### 测试环境

- CPU: Intel i7-12700K
- Memory: 16GB
- 文档: LangChain 官方文档（124 个 chunks）

### 测试结果

| 指标 | 数值 |
|------|------|
| 平均响应时间 | 2.3s |
| 首次查询时间 | 3.1s |
| 缓存命中时间 | 0.01s |
| 缓存命中率 | 35% |
| 准确率 (Faithfulness) | 0.87 |
| 召回率 (Context Recall) | 0.92 |

---

## 🧪 测试

### 运行单元测试

```bash
# 运行所有测试
pytest tests/ -v

# 带覆盖率报告
pytest tests/ -v --cov=core --cov-report=html

# 运行特定测试
pytest tests/test_document_processor.py -v
```

---

## 🛠️ 技术栈

### 核心框架

| 组件 | 版本 | 说明 |
|------|------|------|
| **LangChain** | 0.1.16+ | LLM 应用开发框架 |
| **FastAPI** | 0.110+ | 高性能 Web 框架 |
| **Pydantic** | 2.7+ | 数据验证 |
| **Uvicorn** | 0.28+ | ASGI 服务器 |

### 向量数据库

- **Chroma** (0.4.24+) - 轻量级向量数据库
- **FAISS** (1.7.4+) - Facebook 向量搜索引擎

### LLM & Embedding

- **DashScope** - 通义千问 API
- **OpenAI** - GPT 系列模型
- **BGE** - 本地 Embedding 模型

---

## 📂 项目结构

```
little-assistant/
├── main.py                 # CLI 交互入口
├── api/
│   ├── __init__.py
│   ├── app.py              # FastAPI 服务
│   └── swagger_ui.html     # Swagger UI 静态文件
├── core/
│   ├── __init__.py
│   ├── document_processor.py  # 文档处理（加载、分割）
│   ├── vector_db.py           # 向量库管理
│   ├── llm_engine.py          # LLM 引擎
│   ├── rag_chain.py           # RAG 链构建
│   ├── cache.py               # 查询缓存
│   └── monitor.py             # 性能监控
├── config/
│   ├── __init__.py
│   └── settings.py        # 配置管理
├── utils/
│   ├── __init__.py
│   └── logger.py          # 日志工具
├── tests/                 # 单元测试
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_cache.py
│   ├── test_document_processor.py
│   └── test_vector_db.py
├── docs/                  # 文档目录（存放待处理的文档）
├── chroma_db/             # 向量库数据（自动生成）
├── logs/                  # 日志文件（自动生成）
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example           # 环境变量模板
├── .gitignore
├── LICENSE.markdown
└── README.md              # 项目说明文档
```

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m "feat: add your feature"`
4. 推送到分支：`git push origin feature/your-feature`
5. 创建 Pull Request

### 代码风格

- 使用 Python 3.10+ 语法
- 遵循 PEP 8 规范
- 使用类型注解
- 添加适当的单元测试

---

## 📝 License

MIT License - 详见 [LICENSE.markdown](LICENSE.markdown)

---

## 🙏 致谢

感谢以下开源项目：

- [LangChain](https://github.com/langchain-ai/langchain) - LLM 应用框架
- [Chroma](https://github.com/chroma-core/chroma) - 向量数据库
- [FastAPI](https://github.com/tiangolo/fastapi) - Web 框架
- [通义千问](https://tongyi.aliyun.com/) - 大语言模型

---

**如果这个项目对你有帮助，欢迎 ⭐ Star 支持！**
