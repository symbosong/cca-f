# 模块 1：Claude 入门 — API 基础与核心概念

> **对应课程**：Building with the Claude API — Module 1: Getting Started with Claude  
> **视频数量**：10 个（约 56 分钟）  
> **GitHub Notebook**：`anthropic_api_fundamentals/` 目录（6 个 Notebook）  
> **预计学习时间**：2 小时  
> **难度**：⭐

### 📌 原课程地址

| 平台 | 链接 |
|------|------|
| **Skilljar（官方）** | https://anthropic.skilljar.com/claude-with-the-anthropic-api |
| **Coursera（镜像）** | https://www.coursera.org/learn/building-with-the-claude-api |
| **GitHub Notebook** | https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals |

### 📌 视频与 Notebook 对应关系

| # | 视频标题 | 时长 | 配套 Notebook |
|:-:|---------|:----:|:-------------|
| 1 | Claude Model Overview | 4m | 📓 `03_models.ipynb` |
| 2 | Making Requests | 6m | 📓 `01_getting_started.ipynb` / `02_messages_format.ipynb` |
| 3 | Multi-turn Conversations | 9m | 📓 `02_messages_format.ipynb` |
| 4 | Building a Simple Chatbot | 4m | 📓 `02_messages_format.ipynb`（聊天循环部分） |
| 5 | System Prompts | 6m | 📓 `04_parameters.ipynb`（system 参数部分） |
| 6 | Writing System Prompts Exercise | 1m | — 动手练习 |
| 7 | Temperature | 6m | 📓 `04_parameters.ipynb`（temperature 部分） |
| 8 | Streaming Responses | 8m | 📓 `05_Streaming.ipynb` |
| 9 | Structured Data | 6m | 📓 `06_vision.ipynb` |
| 10 | Structured Data Exercise | 5m | — 动手练习 |

> **阅读材料**（7 篇，65 分钟）：Module Introduction / Working with the API / Getting an API Key / Exploring the Claude Documentation / Setting up a Dev Environment / Controlled Model Output / Next Steps

---

## 本模块学习目标

完成本模块后，你将能够：
1. 了解 Claude 模型家族的特点与选择策略
2. 安装 Anthropic Python SDK 并完成 API 认证
3. 理解 Messages API 的请求/响应格式
4. 掌握多轮对话的消息结构
5. 构建简单的聊天机器人
6. 使用 System Prompt 设定 Claude 的行为
7. 熟练使用 `temperature`、`max_tokens` 等关键参数
8. 使用流式输出（Streaming）实现实时响应
9. 让 Claude 输出结构化数据（JSON 等）

---

## 第 1 课：Claude 模型概览

> 📹 视频：Claude Model Overview（4 min）  
> 📓 配套 Notebook：`03_models.ipynb`

### 1.1 Claude 模型家族

Claude 有三个主要系列，能力与成本递增：

| 模型系列 | 定位 | 特点 | 适用场景 |
|:--------:|------|------|---------|
| **Haiku** | 轻量级 | 最快、最便宜 | 简单分类、客服初筛、数据抽取 |
| **Sonnet** | 平衡型 | 性能与成本最佳平衡 | 大多数生产场景 |
| **Opus** | 旗舰级 | 最强推理能力 | 复杂分析、学术研究、高难度编码 |

### 1.2 当前最新模型标识符

```python
# Claude 4 系列（最新）
"claude-sonnet-4-20250514"    # Sonnet 4 — 目前最常用
"claude-haiku-4-20250514"     # Haiku 4 — 轻量快速

# Claude 3.5 系列
"claude-3-5-sonnet-20241022"  # Sonnet 3.5 v2
"claude-3-5-haiku-20241022"   # Haiku 3.5

# Claude 3 系列（较旧）
"claude-3-opus-20240229"      # Opus 3 — 最强但较慢
"claude-3-sonnet-20240229"    # Sonnet 3
"claude-3-haiku-20240307"     # Haiku 3
```

### 1.3 三维度选型：延迟 / 能力 / 成本

```
📊 选择决策树：

你的任务复杂吗？
├── 简单（分类/抽取/格式化） → Haiku（快且便宜）
├── 中等（写作/分析/代码）  → Sonnet（推荐默认选择）
└── 复杂（推理/学术/创意）  → Opus 或 Sonnet + Extended Thinking
```

**实用建议**：
- **从 Sonnet 开始**，它是性价比最高的模型
- 如果 Sonnet 效果不够好，升级到 Opus
- 如果成本敏感且任务简单，降级到 Haiku
- 对于需要深度推理的任务，使用 Extended Thinking（扩展思考）

### 1.4 代码示例：不同模型对比

```python
import anthropic

client = anthropic.Anthropic()

# 同一个问题，用不同模型回答
models = [
    "claude-3-haiku-20240307",
    "claude-sonnet-4-20250514",
]

question = "Explain quantum entanglement in simple terms."

for model in models:
    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[{"role": "user", "content": question}]
    )
    print(f"=== {model} ===")
    print(response.content[0].text)
    print(f"Tokens: {response.usage.input_tokens} in / {response.usage.output_tokens} out\n")
```

---

## 第 2 课：发起请求

> 📹 视频：Making Requests（6 min）  
> 📓 配套 Notebook：`01_getting_started.ipynb` / `02_messages_format.ipynb`

### 2.1 安装 SDK

```bash
# Python 3.7.1+ 必需
python --version

# 安装 Anthropic SDK
pip install anthropic
```

### 2.2 获取 API Key

1. 访问 [Anthropic Console](https://console.anthropic.com) 注册账号
2. 点击右上角头像 → **API Keys** → **Create Key**
3. 为 Key 命名后点击创建，**立即复制保存**（之后无法再查看）

> ⚠️ **安全提醒**：API Key 如同密码，切勿提交到 Git 或公开分享。Rate Limit 是在账户级别，不是 API Key 级别。

### 2.3 安全存储 API Key

**推荐方式：环境变量**

```bash
# 在 .bashrc / .zshrc 中添加
export ANTHROPIC_API_KEY="your-api-key-here"
```

**Python 中使用 dotenv（本地开发推荐）**

```python
# 安装
pip install python-dotenv

# 创建 .env 文件（记得加入 .gitignore！）
# ANTHROPIC_API_KEY=your-api-key-here
```

```python
from dotenv import load_dotenv
load_dotenv()  # 自动加载 .env 文件中的环境变量
```

### 2.4 第一次 API 调用

```python
import anthropic

# 方式一：自动读取环境变量 ANTHROPIC_API_KEY（推荐）
client = anthropic.Anthropic()

# 方式二：显式传入 Key（不推荐用于生产）
# client = anthropic.Anthropic(api_key="your-key-here")

# 发送第一条消息
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(response.content[0].text)
```

**三要素**：
- `model`：指定使用的模型（上一课已讲）
- `max_tokens`：**必填参数**，限制响应的最大 token 数
- `messages`：消息列表，消息的 `role` 只能是 `"user"` 或 `"assistant"`

### 2.5 响应结构

```python
# 响应对象的关键字段
print(response.id)            # 唯一请求 ID，如 "msg_01XFDUDYJgAACzvnptvVoYEL"
print(response.model)         # 实际使用的模型
print(response.role)          # 始终是 "assistant"
print(response.content)       # 内容列表（ContentBlock 对象）
print(response.content[0].text)  # 获取文本回复
print(response.stop_reason)   # 停止原因：end_turn / max_tokens / tool_use
print(response.usage)         # token 用量统计

# usage 详情
print(response.usage.input_tokens)   # 输入 token 数
print(response.usage.output_tokens)  # 输出 token 数
```

### 2.6 stop_reason 的三种值

| 值 | 含义 | 说明 |
|:--:|------|------|
| `end_turn` | 自然结束 | Claude 认为已完成回答 |
| `max_tokens` | 达到上限 | 输出被截断，可能需要增大 `max_tokens` |
| `tool_use` | 请求工具调用 | Claude 希望使用某个工具（模块 3 详讲） |

---

## 第 3 课：多轮对话

> 📹 视频：Multi-turn Conversations（9 min）  
> 📓 配套 Notebook：`02_messages_format.ipynb`

### 3.1 API 是无状态的

Claude 的 API 是**无状态**的——每次请求都是独立的。要实现多轮对话，必须手动维护完整的消息历史：

```python
# 多轮对话示例
conversation = [
    {"role": "user", "content": "My name is Alice."},
]

# 第一轮
response1 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=conversation
)

# 将 Claude 的回复加入对话历史
conversation.append({
    "role": "assistant",
    "content": response1.content[0].text
})

# 第二轮 —— Claude 能记住前面的对话
conversation.append({
    "role": "user",
    "content": "What is my name?"
})

response2 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=conversation
)

print(response2.content[0].text)  # Claude 会回答 "Alice"
```

### 3.2 消息格式规则

1. `messages` 列表必须以 `user` 消息开头
2. `user` 和 `assistant` 消息必须**交替出现**
3. 可以连续发送多个 `user` 消息（系统会自动合并），但不推荐
4. `system` 不在 `messages` 中，而是单独的参数
5. Claude 通过完整的消息历史来理解上下文

---

## 第 4 课：构建简易聊天机器人

> 📹 视频：Building a Simple Chatbot（4 min）  
> 📓 配套 Notebook：`02_messages_format.ipynb`（聊天循环部分）

### 4.1 交互式聊天循环

将多轮对话封装成一个 while 循环，维护 conversation 列表：

```python
import anthropic

client = anthropic.Anthropic()

conversation_history = []

def chat(user_message):
    """发送消息并获取 Claude 的回复"""
    conversation_history.append({
        "role": "user",
        "content": user_message,
    })
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8096,
        system="You are a helpful AI assistant.",
        messages=conversation_history,
    )
    
    assistant_message = response.content[0].text
    
    # 将 Claude 的回复追加到对话历史
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message,
    })
    
    return assistant_message

# 交互式聊天循环
def main():
    print("开始聊天（输入 'quit' 退出）")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
        response = chat(user_input)
        print(f"\nClaude: {response}")

# main()  # 取消注释运行
```

**关键设计**：
- 实时追加用户消息和助手消息到 `conversation_history`
- 每次请求发送完整历史，让 Claude 理解整个对话

---

## 第 5 课：System Prompts

> 📹 视频：System Prompts（6 min）  
> 📓 配套 Notebook：`04_parameters.ipynb`（system 参数部分）

### 5.1 什么是 System Prompt？

系统提示设置 Claude 的"人设"和行为规则，在整个对话中持续生效。它独立于 `messages`，不参与角色交替规则。

```python
# 基本用法
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a pirate. You always respond in pirate speak.",
    messages=[
        {"role": "user", "content": "How is the weather today?"}
    ]
)
print(response.content[0].text)
# 输出类似："Ahoy, matey! The skies be clear and the winds be fair today!"
```

### 5.2 System Prompt 最佳实践

- 用系统提示定义角色、语气、输出格式
- 把规则和限制放在系统提示中
- 系统提示中的指令优先级高于用户消息
- 保持简洁，避免过长（会消耗 token 和影响注意力）

---

## 第 6 课：System Prompt 练习

> 📹 视频：Writing System Prompts Exercise（1 min）  
> 本课为动手练习，无配套 Notebook

### 练习：为客服机器人编写系统提示

尝试为一个在线商城的客服机器人编写 System Prompt，要求：
- 专业但友好的语气
- 只回答与订单、退货、产品相关的问题
- 不泄露公司内部信息
- 超出能力范围时建议转人工

---

## 第 7 课：Temperature

> 📹 视频：Temperature（6 min）  
> 📓 配套 Notebook：`04_parameters.ipynb`（temperature 部分）

### 7.1 Temperature 参数

控制输出的随机性。取值范围 `0.0 ~ 1.0`：

| Temperature | 效果 | 适用场景 |
|:-----------:|------|---------|
| 0.0 | 最确定性，几乎每次相同 | 分类、数据抽取、代码生成 |
| 0.5 | 适度创意 | 一般写作、总结 |
| 1.0 | 最大随机性 | 头脑风暴、创意写作、诗歌 |

```python
# 低温度 — 确定性输出
response_low = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    temperature=0.0,  # 最确定
    messages=[{"role": "user", "content": "What is 2+2?"}]
)

# 高温度 — 多样性输出
response_high = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    temperature=1.0,  # 最随机
    messages=[{"role": "user", "content": "Write a haiku about programming."}]
)
```

### 7.2 其他关键参数

#### max_tokens

限制 Claude 输出的最大 token 数。**这是必填参数**。

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=50,  # 仅允许 50 个 token
    messages=[{"role": "user", "content": "Write a long essay about AI."}]
)

print(response.stop_reason)  # "max_tokens" — 被截断了！
```

> 💡 **注意**：模型不知道 `max_tokens` 的值。它无法主动控制输出长度来避免截断。

#### stop_sequences（停止序列）

让 Claude 在遇到特定字符串时立即停止生成：

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    stop_sequences=["END", "---"],  # 遇到这些字符串就停止
    messages=[
        {"role": "user", "content": "Count from 1 to 10, then write END."}
    ]
)
```

#### top_p 和 top_k

进一步控制采样策略（通常不需要调整）：

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    temperature=0.7,
    top_p=0.9,   # 从概率总和 90% 的 token 中采样
    top_k=40,    # 从前 40 个最可能的 token 中采样
    messages=[{"role": "user", "content": "Write a creative story opening."}]
)
```

> 💡 **建议**：一般只调 `temperature` 就够了。`top_p` 和 `top_k` 是高级用法，两者通常不需要同时使用。

### 7.3 参数速查表

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|:----:|:----:|:------:|------|
| `model` | str | ✅ | — | 模型标识符 |
| `max_tokens` | int | ✅ | — | 最大输出 token 数 |
| `messages` | list | ✅ | — | 对话消息列表 |
| `system` | str | ❌ | 无 | 系统提示 |
| `temperature` | float | ❌ | 1.0 | 随机性（0~1） |
| `top_p` | float | ❌ | — | 核采样阈值 |
| `top_k` | int | ❌ | — | Top-K 采样 |
| `stop_sequences` | list | ❌ | [] | 停止序列 |
| `stream` | bool | ❌ | false | 是否流式输出 |
| `metadata` | dict | ❌ | — | 请求元数据 |

---

## 第 8 课：流式输出

> 📹 视频：Streaming Responses（8 min）  
> 📓 配套 Notebook：`05_Streaming.ipynb`

### 8.1 为什么需要流式输出？

默认情况下，API 会等 Claude 完整生成后才返回响应。对于长回复，用户可能等待几秒甚至几十秒。

流式输出让你**逐步接收** Claude 的回复，实现"打字机效果"，大幅提升用户体验。

### 8.2 基本流式输出

```python
import anthropic

client = anthropic.Anthropic()

# 使用 stream=True 启用流式输出
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a short story about a robot."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()  # 换行
```

### 8.3 流式事件类型

使用底层事件 API 可以获得更细粒度的控制：

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
) as stream:
    for event in stream:
        # 不同事件类型
        if event.type == "message_start":
            print("开始生成...")
        elif event.type == "content_block_start":
            print("内容块开始")
        elif event.type == "content_block_delta":
            # 这里是实际的文本片段
            if hasattr(event.delta, 'text'):
                print(event.delta.text, end="", flush=True)
        elif event.type == "message_stop":
            print("\n生成完成！")
```

### 8.4 获取流式响应的最终消息

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a joke."}]
) as stream:
    # 消费流
    for text in stream.text_stream:
        print(text, end="", flush=True)
    
    # 获取完整的最终消息对象
    final_message = stream.get_final_message()
    print(f"\n\n使用的 token 数: {final_message.usage}")
```

### 8.5 异步流式输出

```python
import asyncio
import anthropic

async def stream_response():
    client = anthropic.AsyncAnthropic()
    
    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Write a poem about coding."}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

# asyncio.run(stream_response())
```

---

## 第 9 课：结构化数据输出

> 📹 视频：Structured Data（6 min）  
> 📓 配套 Notebook：`06_vision.ipynb`

### 9.1 让 Claude 输出 JSON

通过提示约束，让 Claude 返回结构化数据：

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": """Extract the following information from the text and return as JSON:
- name
- age
- city

Text: "John is 30 years old and lives in New York."

Return ONLY valid JSON, nothing else."""
    }]
)
print(response.content[0].text)
```

### 9.2 Vision（图片理解）

Claude 可以分析和理解图片内容，支持：
- **图片描述**：描述图片中的内容
- **OCR/文本识别**：提取图片中的文字
- **图表解读**：分析图表、数据可视化
- **代码截图**：理解代码截图的内容

**支持格式**：JPEG、PNG、GIF、WebP  
**大小限制**：单张图片最大 5MB，长边不超过 8000px

#### URL 引用

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
                    }
                },
                {
                    "type": "text",
                    "text": "What do you see in this image?"
                }
            ]
        }
    ]
)
print(response.content[0].text)
```

#### Base64 编码

```python
import base64
import mimetypes

def encode_image(image_path):
    """将本地图片编码为 base64"""
    with open(image_path, "rb") as f:
        binary_data = f.read()
    
    base64_string = base64.b64encode(binary_data).decode("utf-8")
    mime_type, _ = mimetypes.guess_type(image_path)
    
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": base64_string
        }
    }

# 使用本地图片
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                encode_image("./my_photo.png"),
                {"type": "text", "text": "Describe this image in detail."}
            ]
        }
    ]
)
```

### 9.3 stop_reason 判断输出完整性

当让 Claude 输出结构化数据时，务必检查 `stop_reason`：
- `end_turn`：正常结束，输出完整
- `max_tokens`：被截断了，JSON 可能不完整

---

## 第 10 课：结构化数据练习

> 📹 视频：Structured Data Exercise（5 min）  
> 本课为动手练习

### 练习：情感分析 + 关键词提取

从非结构化文本中提取情感、关键词和评分：

```python
review = """I bought this wireless keyboard last month. The typing experience is amazing - 
the keys are quiet and responsive. Battery life is incredible, lasting over 3 months. 
However, the Bluetooth connection sometimes drops when my phone is nearby. 
The price of $79 feels fair for the build quality. Would recommend to others."""

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"""Analyze the following product review and return a JSON object with:
- sentiment: "positive", "negative", or "mixed"
- keywords: array of key topics mentioned
- rating_estimate: estimated rating out of 5
- pros: array of positive points
- cons: array of negative points

Review:
{review}

Return ONLY valid JSON."""
    }]
)
print(response.content[0].text)
```

---

## Token 计数与成本（补充知识）

### 理解 Token

- Token 是模型处理文本的基本单位
- 英文约 1 token ≈ 4 个字符（约 0.75 个单词）
- 中文约 1 token ≈ 1-2 个汉字
- 成本 = 输入 token 费用 + 输出 token 费用

### 查看 Token 使用量

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hi!"}]
)

print(f"输入 tokens: {response.usage.input_tokens}")
print(f"输出 tokens: {response.usage.output_tokens}")
print(f"总计 tokens: {response.usage.input_tokens + response.usage.output_tokens}")
```

### 使用 count_tokens 预估

```python
# 在发送请求前预估 token 数
count = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(f"预估输入 tokens: {count.input_tokens}")
```

---

## 练习题

### 练习 1：基础对话

创建一个简单的命令行聊天程序，要求：
- 支持多轮对话
- 设置一个有趣的系统提示（如"你是一位诗人"）
- 显示每轮对话的 token 使用量
- 输入 `quit` 退出

### 练习 2：参数实验

对同一个提示，分别使用 `temperature=0.0` 和 `temperature=1.0`，各运行 3 次，观察输出的差异。

### 练习 3：图片分析

找一张包含文字的图片（如菜单、海报、截图），用 Vision 功能提取其中的文字内容。

### 练习 4：模型对比

对一个复杂问题（如"解释量子纠缠"），分别用 Haiku 和 Sonnet 回答，对比：
- 回答质量
- Token 使用量
- 响应速度

---

## 常见问题

**Q: API Key 泄露了怎么办？**  
A: 立即在 Console 中删除该 Key 并创建新 Key。

**Q: 如何处理 Rate Limit？**  
A: 使用指数退避重试。SDK 内置了自动重试机制。

**Q: 多轮对话越来越慢怎么办？**  
A: 随着对话变长，每次请求的 input tokens 增加。可以定期裁剪对话历史，或使用 Prompt Caching（模块 3 讲解）。

**Q: 图片消耗多少 Token？**  
A: 取决于图片大小。大致估算：小图约 1,000 tokens，大图可达 10,000+ tokens。具体参见 [官方文档](https://docs.anthropic.com/en/docs/build-with-claude/vision)。

---

> **下一模块**：[02_提示工程与评估.md](02_提示工程与评估.md) — 学习提示工程的核心技巧和评估方法
