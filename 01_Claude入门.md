# 模块 1：Claude 入门 — API 基础与核心概念

> **对应课程**：Building with the Claude API — Module 1: Introduction to Claude  
> **视频数量**：10 个（约 56 分钟）  
> **GitHub Notebook**：`anthropic_api_fundamentals/` 目录（6 个 Notebook）  
> **预计学习时间**：2 小时  
> **难度**：⭐

---

## 本模块学习目标

完成本模块后，你将能够：
1. 安装 Anthropic Python SDK 并完成 API 认证
2. 理解 Messages API 的请求/响应格式
3. 掌握多轮对话的消息结构
4. 了解不同 Claude 模型的特点与选择策略
5. 熟练使用 `temperature`、`max_tokens`、`system` 等关键参数
6. 使用流式输出（Streaming）实现实时响应
7. 利用 Vision 能力处理图片输入

---

## 第一节：环境搭建与第一次调用

> 📹 对应视频：Lesson 1 - Getting Started  
> 📓 对应 Notebook：`01_getting_started.ipynb`

### 1.1 安装 SDK

```bash
# Python 3.7.1+ 必需
python --version

# 安装 Anthropic SDK
pip install anthropic
```

### 1.2 获取 API Key

1. 访问 [Anthropic Console](https://console.anthropic.com) 注册账号
2. 点击右上角头像 → **API Keys** → **Create Key**
3. 为 Key 命名后点击创建，**立即复制保存**（之后无法再查看）

> ⚠️ **安全提醒**：API Key 如同密码，切勿提交到 Git 或公开分享。Rate Limit 是在账户级别，不是 API Key 级别。

### 1.3 安全存储 API Key

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

### 1.4 第一次 API 调用

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

**关键点**：
- `model`：指定使用的模型（后面会详细讲）
- `max_tokens`：**必填参数**，限制响应的最大 token 数
- `messages`：消息列表，消息的 `role` 只能是 `"user"` 或 `"assistant"`

---

## 第二节：Messages API 格式详解

> 📹 对应视频：Lesson 2 - Messages Format  
> 📓 对应 Notebook：`02_messages_format.ipynb`

### 2.1 请求结构

Messages API 是 Claude 交互的唯一接口。完整请求结构：

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",   # 必填：模型名称
    max_tokens=1024,                    # 必填：最大输出 token 数
    system="You are a helpful assistant.",  # 可选：系统提示
    messages=[                          # 必填：消息列表
        {"role": "user", "content": "Hello!"},
    ]
)
```

### 2.2 响应结构

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

### 2.3 stop_reason 的三种值

| 值 | 含义 | 说明 |
|:--:|------|------|
| `end_turn` | 自然结束 | Claude 认为已完成回答 |
| `max_tokens` | 达到上限 | 输出被截断，可能需要增大 `max_tokens` |
| `tool_use` | 请求工具调用 | Claude 希望使用某个工具（模块 3 详讲） |

### 2.4 多轮对话

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

**消息格式规则**：
1. `messages` 列表必须以 `user` 消息开头
2. `user` 和 `assistant` 消息必须**交替出现**
3. 可以连续发送多个 `user` 消息（系统会自动合并），但不推荐
4. `system` 不在 `messages` 中，而是单独的参数

### 2.5 实现简单的聊天循环

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

---

## 第三节：模型选择

> 📹 对应视频：Lesson 3 - Models  
> 📓 对应 Notebook：`03_models.ipynb`

### 3.1 Claude 模型家族

Claude 有三个主要系列，能力与成本递增：

| 模型系列 | 定位 | 特点 | 适用场景 |
|:--------:|------|------|---------|
| **Haiku** | 轻量级 | 最快、最便宜 | 简单分类、客服初筛、数据抽取 |
| **Sonnet** | 平衡型 | 性能与成本最佳平衡 | 大多数生产场景 |
| **Opus** | 旗舰级 | 最强推理能力 | 复杂分析、学术研究、高难度编码 |

### 3.2 当前最新模型标识符

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

### 3.3 如何选择模型？

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

### 3.4 代码示例：不同模型对比

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

## 第四节：关键参数调优

> 📹 对应视频：Lesson 4 - Parameters  
> 📓 对应 Notebook：`04_parameters.ipynb`

### 4.1 system（系统提示）

系统提示设置 Claude 的"人设"和行为规则，在整个对话中持续生效：

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

**系统提示最佳实践**：
- 用系统提示定义角色、语气、输出格式
- 把规则和限制放在系统提示中
- 系统提示中的指令优先级高于用户消息
- 保持简洁，避免过长（会消耗 token 和影响注意力）

### 4.2 temperature（温度）

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

### 4.3 max_tokens

限制 Claude 输出的最大 token 数。**这是必填参数**。

```python
# 限制为很少的 token — 可能导致输出被截断
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=50,  # 仅允许 50 个 token
    messages=[{"role": "user", "content": "Write a long essay about AI."}]
)

print(response.stop_reason)  # "max_tokens" — 被截断了！
```

**注意**：
- `max_tokens` 不是"精确控制输出长度"，而是"最大上限"
- 如果 `stop_reason == "max_tokens"`，说明输出被截断
- 一般英文 1 token ≈ 4 个字符，中文 1 token ≈ 1-2 个字

### 4.4 stop_sequences（停止序列）

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
# Claude 会在输出 "END" 之前停止
```

### 4.5 top_p 和 top_k

这两个参数进一步控制采样策略（通常不需要调整）：

- **top_p**（核采样）：只从累积概率达到 p 的最小 token 集合中采样
- **top_k**：只从概率最高的 k 个 token 中采样

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

### 4.6 参数速查表

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

## 第五节：流式输出（Streaming）

> 📹 对应视频：Lesson 5 - Streaming  
> 📓 对应 Notebook：`05_Streaming.ipynb`

### 5.1 为什么需要流式输出？

默认情况下，API 会等 Claude 完整生成后才返回响应。对于长回复，用户可能等待几秒甚至几十秒。

流式输出让你**逐步接收** Claude 的回复，实现"打字机效果"，大幅提升用户体验。

### 5.2 基本流式输出

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

### 5.3 流式事件类型

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

### 5.4 获取流式响应的最终消息

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

### 5.5 异步流式输出

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

## 第六节：Vision（图片理解）

> 📹 对应视频：Lesson 6 - Vision  
> 📓 对应 Notebook：`06_vision.ipynb`

### 6.1 Claude 的视觉能力

Claude 可以分析和理解图片内容，支持：
- **图片描述**：描述图片中的内容
- **OCR/文本识别**：提取图片中的文字
- **图表解读**：分析图表、数据可视化
- **代码截图**：理解代码截图的内容
- **文档扫描**：处理扫描的文档、研究论文

**支持格式**：JPEG、PNG、GIF、WebP  
**大小限制**：单张图片最大 5MB，长边不超过 8000px

### 6.2 方式一：URL 引用

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

### 6.3 方式二：Base64 编码

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

### 6.4 多图片输入

```python
# 同时发送多张图片
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                encode_image("./image1.png"),
                encode_image("./image2.png"),
                {
                    "type": "text",
                    "text": "Compare these two images. What are the differences?"
                }
            ]
        }
    ]
)
```

### 6.5 实战：论文 OCR + 摘要

这个例子展示了如何将多页研究论文图片转录并生成摘要：

```python
import base64
import mimetypes

def create_image_message(image_path):
    """将图片转为 API 可用的格式"""
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
    base64_string = base64.b64encode(binary_data).decode('utf-8')
    mime_type, _ = mimetypes.guess_type(image_path)
    
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": base64_string
        }
    }

def transcribe_single_page(page_path):
    """转录单页论文"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=5000,
        messages=[{
            "role": "user",
            "content": [
                create_image_message(page_path),
                {"type": "text", "text": "Transcribe the text from this page as accurately as possible."}
            ]
        }]
    )
    return response.content[0].text

def summarize_paper(page_paths):
    """转录所有页面并生成摘要"""
    complete_text = ""
    for page in page_paths:
        print(f"Transcribing {page}...")
        text = transcribe_single_page(page)
        complete_text += text
    
    # 生成摘要
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=5000,
        messages=[{
            "role": "user",
            "content": (
                f"This is a transcribed research paper:\n<paper>{complete_text}</paper>\n"
                "Please summarize this paper for a non-research audience in at least 3 paragraphs. "
                "Explain any abbreviations or technical jargon, and use analogies when possible."
            )
        }]
    )
    return response.content[0].text

# 使用示例
# pages = ["./page1.png", "./page2.png", "./page3.png"]
# summary = summarize_paper(pages)
# print(summary)
```

> 💡 **性能提示**：处理多页文档时，建议逐页转录再合并，而不是一次性发送所有页面。这样可以获得更准确的结果。

---

## 第七节：token 计数与成本

### 7.1 理解 Token

- Token 是模型处理文本的基本单位
- 英文约 1 token ≈ 4 个字符（约 0.75 个单词）
- 中文约 1 token ≈ 1-2 个汉字
- 成本 = 输入 token 费用 + 输出 token 费用

### 7.2 查看 Token 使用量

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

### 7.3 使用 count_tokens 预估

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
