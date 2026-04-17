# Claude 课程演示脚本 — 腾讯云 TokenHub 版

> 受限地区替代方案：使用腾讯云 TokenHub + OpenAI 兼容协议替代 Anthropic 官方 API

## 快速开始

### 1. 安装依赖

```bash
pip install openai python-dotenv
```

### 2. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入你的腾讯云 TokenHub API Key
```

**API Key 获取地址**：https://console.cloud.tencent.com/tokenhub/apikey

**模型广场（查看可用模型）**：https://console.cloud.tencent.com/tokenhub/models?regionId=1

### 3. 运行脚本

```bash
python 01_基础调用演示.py
```

## 脚本说明

| 文件 | 对应课程模块 | 内容 |
|:---|:---|:---|
| `01_基础调用演示.py` | 模块 1：Claude 入门 | 基础调用、System Prompt、多轮对话、流式输出、参数调节 |
| `02_提示工程与评估.py` | 模块 2：提示工程与评估 | 清晰指令、XML标签、Few-shot、思维链、自动评估管道 |
| `03_工具使用.py` | 模块 3：工具使用 | Function Calling、Agent Loop、tool_choice、Prompt Caching |
| `04_MCP协议概念演示.py` | 模块 4：MCP协议 | MCP三大能力 Tools/Resources/Prompts 概念演示 |
| `05_RAG检索增强生成.py` | 模块 5：RAG | 检索流程、知识库问答、边界处理、分块策略 |
| `06_AI编程助手演示.py` | 模块 6：Claude Code | 代码理解、生成、重构、调试、测试生成 |
| `07_Agent工作流.py` | 模块 7：Agent工作流 | 链式/路由/并行工作流、评估器-优化器、完整Agent Loop |

## 接入配置

| 配置项 | 值 |
|:---|:---|
| **base_url** | `https://tokenhub.tencentmaas.com/v1` |
| **默认模型** | `glm-5` |
| **SDK** | `openai`（OpenAI 兼容协议） |
| **API Key 管理** | https://console.cloud.tencent.com/tokenhub/apikey |

## 可用模型（TokenHub 模型广场）

修改脚本中 `MODEL` 变量即可切换，所有模型共用同一 API Key 和 base_url：

| 模型 | 参数值 | 特点 |
|:---|:---|:---|
| GLM-5 | `glm-5` | 智谱 AI，默认开启思维链，200K 上下文 |
| DeepSeek-V3.2 | `deepseek-v3.2` | MoE架构，支持深度思考 |
| DeepSeek-V3-0324 | `deepseek-v3-0324` | DeepSeek V3 稳定版 |
| DeepSeek-V3.1-Terminus | `deepseek-v3.1-terminus` | 支持 thinking 参数控制思维链 |

> 完整模型列表见：https://console.cloud.tencent.com/tokenhub/models?regionId=1

## 与原版 Anthropic SDK 的对比

| 对比项 | Anthropic 官方 SDK | 腾讯云 TokenHub |
|:---|:---|:---|
| SDK | `anthropic` | `openai` |
| base_url | `api.anthropic.com` | `tokenhub.tencentmaas.com/v1` |
| 消息格式 | `client.messages.create()` | `client.chat.completions.create()` |
| API 核心概念 | 完全一致 | 完全一致 |
| 受限地区访问 | 不可用 | ✅ 可用 |
