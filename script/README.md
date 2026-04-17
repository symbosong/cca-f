# Claude 课程演示脚本 — 腾讯云 LKEAP 版

> 受限地区替代方案：使用腾讯云 LKEAP + OpenAI 兼容协议替代 Anthropic 官方 API

## 快速开始

### 1. 安装依赖

```bash
pip install openai python-dotenv
```

### 2. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入你的腾讯云 LKEAP API Key
```

API Key 获取地址：https://hunyuan.cloud.tencent.com/#/app/apiKeyManage

### 3. 运行脚本

```bash
python 01_基础调用演示.py
```

## 脚本说明

| 文件 | 对应课程模块 | 内容 |
|:---:|:---:|:---:|
| `01_基础调用演示.py` | 模块 1：Claude 入门 | 基础调用、System Prompt、多轮对话、流式输出、参数调节 |

## 模型切换

修改脚本中 `MODEL` 变量即可切换模型（同一个 API Key 和 base_url）：

| 模型 | 参数值 | 特点 |
|:---:|:---:|:---:|
| GLM-5 | `glm-5` | 智谱 AI 旗舰，默认开启思维链 |
| Kimi K2.5 | `kimi-k2.5` | 256K 超长上下文 |
| MiniMax M2.5 | `minimax-m2.5` | 200K 上下文 |

## 与原版 Anthropic SDK 的对比

| 对比项 | Anthropic 官方 SDK | 腾讯云 LKEAP |
|:---:|:---:|:---:|
| SDK | `anthropic` | `openai` |
| base_url | `api.anthropic.com` | `api.lkeap.cloud.tencent.com/v3` |
| 消息格式 | `client.messages.create()` | `client.chat.completions.create()` |
| API 核心概念 | 完全一致 | 完全一致 |
| 受限地区访问 | 不可用 | 可用 |
