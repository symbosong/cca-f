# 📚 Claude 课程详细学习教程

> 基于 **Anthropic 官方课程**（Skilljar / Coursera / GitHub）系统整理，涵盖从 API 基础到生产级 Agent 系统设计的完整知识体系。

**总规模**：17 个教程与分析文件 · 13,000+ 行 · 预计 55-80 小时完整学习（含认证备考）

---

## 🗺️ 课程导航

### 第一阶段：打地基（~6h）

| 文件 | 主题 | 核心内容 | 难度 |
|------|------|---------|:----:|
| [00_学习大纲与资源总览](00_学习大纲与资源总览.md) | 总览 | 学习路径、资源矩阵、环境准备、按角色推荐 | — |
| [01_Claude入门](01_Claude入门.md) | API 基础 | SDK 安装、Messages API、多轮对话、模型选择、temperature / max_tokens、流式输出、Vision | ⭐ |
| [02_提示工程与评估](02_提示工程与评估.md) | 提示工程 | 角色设定、思维链 CoT、Prefilling、XML 标签、Few-shot、评估管道 | ⭐⭐ |

### 第二阶段：核心能力（~7h）

| 文件 | 主题 | 核心内容 | 难度 |
|------|------|---------|:----:|
| [03_工具使用与高级特性](03_工具使用与高级特性.md) | 工具调用 | JSON Schema 定义工具、Agentic Loop、客服机器人实战、Extended Thinking、Prompt Caching | ⭐⭐⭐ |
| [04_MCP模型上下文协议](04_MCP模型上下文协议.md) | MCP 协议 | MCP 架构、Tools / Resources / Prompts 三大能力、Server 搭建、Claude Desktop 集成 | ⭐⭐ |

### 第三阶段：高级应用（~5h）

| 文件 | 主题 | 核心内容 | 难度 |
|------|------|---------|:----:|
| [05_RAG检索增强生成](05_RAG检索增强生成.md) | RAG | Embedding + 向量库、索引→检索→生成全流程、分块策略、Re-ranking | ⭐⭐⭐ |
| [06_Claude_Code与Computer_Use](06_Claude_Code与Computer_Use.md) | AI 编程 | Claude Code 安装与工作流、CLAUDE.md 配置、Computer Use 桌面操控 | ⭐⭐ |
| [07_Agent工作流与智能体](07_Agent工作流与智能体.md) | Agent | 链式 / 路由 / 并行工作流、工具循环 Agent、编排器 Agent、安全护栏 | ⭐⭐⭐ |

### 第四阶段：进阶深度（~25-35h）⭐ 生产级硬核内容

| 文件 | 主题 | 核心内容 | 难度 |
|------|------|---------|:----:|
| [08_进阶指南](08_进阶指南.md) | 快速参考 | 模块 8-13 的浓缩版，适合快速查阅 | ⭐⭐⭐ |
| [09_Agent_SDK深度指南](09_Agent_SDK深度指南.md) | Agent SDK | Agent Loop、内置工具、工具权限、上下文压缩、子智能体编排、Hooks、会话恢复 | ⭐⭐⭐⭐ |
| [10_Claude_Code高级特性](10_Claude_Code高级特性.md) | Claude Code 高级 | 三级配置体系、Hooks 钩子、CI/CD 集成、自定义命令、多 Agent 团队 | ⭐⭐⭐ |
| [11_Streaming与多模态深度](11_Streaming与多模态深度.md) | 流式 + 多模态 | Streaming 深度控制、Vision、PDF 处理、Citations 引用、Files API | ⭐⭐⭐ |
| [12_Prompt_Caching与Batch_API](12_Prompt_Caching与Batch_API.md) | 成本优化 | Prompt Caching 缓存复用、Batch API 批量处理、叠加优化方案 | ⭐⭐⭐ |
| [13_安全护栏与生产部署](13_安全护栏与生产部署.md) | 安全 + 部署 | 输入输出验证、注入防护、AI→人工升级、Rate Limiting、监控体系 | ⭐⭐⭐⭐ |
| [14_成本优化与模型选择策略](14_成本优化与模型选择策略.md) | 成本 + 选型 | Extended Thinking、模型定价、智能路由、预算管理、Token 优化 | ⭐⭐⭐ |

### 第五阶段：认证备考（~15-25h）⭐ CCA-F 官方认证

| 文件 | 主题 | 核心内容 | 难度 |
|------|------|---------|:----:|
| [15_CCA-F认证考试备考指南](15_CCA-F认证考试备考指南.md) | 认证备考 | 五大考试领域精讲、六大场景解析、样题与解题策略、备考路线、课程覆盖度分析 | ⭐⭐⭐⭐⭐ |

### 第六阶段：深度产品研究 💡 拓展阅读

| 文件 | 主题 | 核心内容 | 难度 |
|------|------|---------|:----:|
| [WorkBuddy与Claude_Cowork深度对比分析](WorkBuddy与Claude_Cowork深度对比分析.html) | 产品对比 | 腾讯 WorkBuddy vs Anthropic Claude Cowork 深度对比（网页版深度解析报告），涵盖架构、协作机制与场景选型 | ⭐⭐⭐ |

---

## 🚀 快速开始

### 环境准备

```bash
# 安装 SDK
pip install anthropic

# 设置 API Key
export ANTHROPIC_API_KEY="your-api-key-here"

# 克隆官方课程仓库（含 35+ Jupyter Notebook）
git clone https://github.com/anthropics/courses.git
```

### 按角色选择学习路径

| 角色 | 推荐路径 | 预计时间 |
|------|---------|:--------:|
| **架构师** | 全部 01-15 | 55-80h |
| **后端开发** | 01-03 → 07 → 09 → 11 → 12 | 25-30h |
| **前端开发** | 01-03 → 11 → 13 | 15-18h |
| **DevOps** | 01-02 → 10（CI/CD）→ 12 | 15-18h |
| **产品经理** | 01-02 → 14（成本部分） | 8-12h |

### 4.5 小时速成路线

```
1h → 阅读 01-03 文档（建立全景认知）
1h → 跑 GitHub courses 的 anthropic_api_fundamentals/ Notebook
1h → 跑 GitHub courses 的 tool_use/ Notebook
1h → 读官方 Agent SDK 文档
30m → 读官方 MCP 文档
```

---

## 📖 学习资源

| 资源 | 链接 | 说明 |
|------|------|------|
| **Skilljar 视频课** | [anthropic.skilljar.com](https://anthropic.skilljar.com/claude-with-the-anthropic-api) | 84 个视频 / 8.1h（免费） |
| **Coursera 镜像** | [coursera.org](https://www.coursera.org/learn/building-with-the-claude-api) | 含 AI Coach 互动助手 |
| **GitHub 课程仓库** | [anthropics/courses](https://github.com/anthropics/courses) | 35+ Jupyter Notebook（⭐ 19.7k） |
| **Cookbook 实战** | [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 生产级代码示例 |
| **官方 API 文档** | [docs.anthropic.com](https://docs.anthropic.com) | API 参考 + 最佳实践 |
| **Agent SDK** | [GitHub](https://github.com/anthropics/agent-sdk) | Agent SDK 框架源码 |
| **MCP 规范** | [GitHub](https://github.com/modelcontextprotocol/specification) | 模型上下文协议规范 |

---

## 📁 文件结构

```
├── 00_学习大纲与资源总览.md        ← 开始这里：总览 + 环境准备
├── 01_Claude入门.md               ← API 基础
├── 02_提示工程与评估.md            ← 提示工程 + 评估管道
├── 03_工具使用与高级特性.md        ← 工具调用 + Extended Thinking
├── 04_MCP模型上下文协议.md         ← MCP 协议
├── 05_RAG检索增强生成.md           ← RAG 系统
├── 06_Claude_Code与Computer_Use.md ← AI 编程 + 桌面操控
├── 07_Agent工作流与智能体.md       ← Agent 模式与工作流
├── 08_进阶指南.md                  ← 进阶内容浓缩参考
├── 09_Agent_SDK深度指南.md         ← ⭐ Agent SDK 生产级指南
├── 10_Claude_Code高级特性.md       ← Claude Code 高级配置
├── 11_Streaming与多模态深度.md     ← 流式传输 + Vision + PDF
├── 12_Prompt_Caching与Batch_API.md ← 成本优化双利器
├── 13_安全护栏与生产部署.md        ← 生产安全基线
├── 14_成本优化与模型选择策略.md    ← 模型选型 + 成本控制
├── 15_CCA-F认证考试备考指南.md     ← ⭐ CCA-F 认证备考
└── WorkBuddy与Claude_Cowork深度对比分析.html ← 💡 网页版产品对标分析报告
```

---

> **维护**：AI 架构师团队 · 2026年3月 · 基于 Anthropic 官方文档最新版
