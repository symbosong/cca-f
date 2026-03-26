# 模块 10：Streaming 与多模态深度 — 流式传输 + Vision + PDF + Citations + Files API

> **官方文档**：  
> - Streaming: https://docs.anthropic.com/en/docs/build-with-claude/streaming  
> - Vision: https://docs.anthropic.com/en/docs/build-with-claude/vision  
> - PDF: https://platform.claude.com/docs/en/build-with-claude/pdf-support  
> - Citations: https://platform.claude.com/docs/en/build-with-claude/citations  
> - Files API: https://platform.claude.com/docs/en/build-with-claude/files  
> - Token Counting: https://platform.claude.com/docs/en/build-with-claude/token-counting  
> **预计学习时间**：3-4 小时  
> **难度**：⭐⭐⭐

---

## 目录

- [一、Streaming 流式传输](#一streaming-流式传输)
- [二、Vision 图像理解](#二vision-图像理解)
- [三、PDF 文档处理](#三pdf-文档处理)
- [四、Citations 引用系统](#四citations-引用系统)
- [五、Files API 文件管理](#五files-api-文件管理)
- [六、Token Counting 预估](#六token-counting-预估)
- [七、综合实战：多模态文档分析系统](#七综合实战多模态文档分析系统)
- [练习题](#练习题)

---

## 一、Streaming 流式传输

### 1.1 为什么需要 Streaming

- **用户体验**：实时显示生成内容，避免长时间等待
- **HTTP 超时**：`max_tokens` 较大时，非流式请求可能超时
- **工具调用**：流式可以实时看到 Claude 调用了什么工具

### 1.2 基础流式传输

```python
import anthropic

client = anthropic.Anthropic()

# 方式 1：使用 SDK 的 stream 上下文管理器（推荐）
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "写一首关于编程的诗"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()  # 换行
```

### 1.3 获取最终完整消息

```python
# 方式 2：不处理流式事件，只获取最终结果
# 适合 max_tokens 很大的请求（SDK 底层用流式避免超时）
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=128000,
    messages=[{"role": "user", "content": "Write a detailed analysis..."}],
) as stream:
    message = stream.get_final_message()

print(message.content[0].text)
print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")
```

### 1.4 SSE 事件类型详解

流式响应通过 **Server-Sent Events (SSE)** 传输，事件流程如下：

```
message_start → content_block_start → [content_block_delta...] → 
content_block_stop → [更多块...] → message_delta → message_stop
```

| 事件 | 说明 |
|:-----|:-----|
| `message_start` | 包含 `content` 为空的 Message 对象 |
| `content_block_start` | 新内容块开始（text / tool_use / thinking） |
| `content_block_delta` | 内容增量（text_delta / input_json_delta / thinking_delta） |
| `content_block_stop` | 内容块结束 |
| `message_delta` | 顶级更新（stop_reason、累积 usage） |
| `message_stop` | 流结束 |
| `ping` | 心跳事件 |
| `error` | 错误事件（如 overloaded_error） |

### 1.5 流式工具调用

```python
import json

with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }],
    messages=[{"role": "user", "content": "What's the weather in Beijing?"}],
) as stream:
    for event in stream:
        # event 可能是 text_delta、input_json_delta 等
        if event.type == "content_block_start":
            if event.content_block.type == "tool_use":
                print(f"\n🔧 Calling tool: {event.content_block.name}")
        elif event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
            elif event.delta.type == "input_json_delta":
                print(event.delta.partial_json, end="", flush=True)
```

> **注意**：工具调用参数以 `input_json_delta` 形式流式传输，是**部分 JSON 字符串**，最终拼接成完整 JSON 对象。

### 1.6 流式 + Extended Thinking

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "分析这段算法的时间复杂度..."}],
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "thinking":
                print("\n💭 Thinking...", flush=True)
            elif event.content_block.type == "text":
                print("\n📝 Response:", flush=True)
        elif event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
            elif event.delta.type == "signature_delta":
                # 思考块的加密签名，用于多轮连续性
                pass
```

### 1.7 流式错误恢复

**Claude 4.5 及更早版本**：可以从中断处恢复

```python
# 1. 保存已接收的部分响应
# 2. 创建新请求，将部分响应作为助手消息的开头
# 3. 继续接收剩余部分

partial_response = "The algorithm has a time complexity of O(n log n) because"

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Analyze the time complexity of merge sort"},
        {"role": "assistant", "content": partial_response},  # 部分响应作为前缀
    ],
)
# Claude 会从 partial_response 末尾继续生成
```

**Claude 4.6**：需要添加用户消息提示继续

```python
messages = [
    {"role": "user", "content": "Analyze the time complexity of merge sort"},
    {"role": "assistant", "content": partial_response},
    {"role": "user", "content": f"Your previous response was interrupted and ended with: "
                                 f"'{partial_response[-100:]}'. Continue from where you left off."},
]
```

---

## 二、Vision 图像理解

### 2.1 图像输入方式

Claude 支持三种图像输入方式：

#### Base64 编码

```python
import base64
import httpx

# 从 URL 加载并编码
image_data = base64.standard_b64encode(
    httpx.get("https://example.com/image.jpg").content
).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data,
                }
            },
            {"type": "text", "text": "描述这张图片中的内容"}
        ]
    }]
)
```

#### URL 引用

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
                }
            },
            {"type": "text", "text": "Describe this image."}
        ]
    }]
)
```

#### Files API（推荐用于多轮对话）

```python
# 先上传
file = client.files.create(file=open("chart.png", "rb"))

# 在消息中引用
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {"type": "file", "file_id": file.id}
            },
            {"type": "text", "text": "分析这个图表的趋势"}
        ]
    }]
)
```

### 2.2 图像限制与优化

| 限制项 | 值 |
|:------|:---|
| 单请求最大图片数 | 600 张（API）/ 20 张（Claude.ai） |
| 最大分辨率 | 8000×8000 px |
| 超 20 张时分辨率限制 | 2000×2000 px |
| 支持格式 | JPEG, PNG, GIF, WebP |
| 请求体大小限制 | 32 MB |

**Token 消耗估算**：

```
tokens ≈ (宽度 px × 高度 px) / 750
```

| 图片尺寸 | 约 Token 数 | Sonnet 4.6 成本/张 |
|:---------|:-----------|:-----------------|
| 200×200 | ~54 | $0.00016 |
| 1000×1000 | ~1334 | $0.004 |
| 1568×1568 | ~3278 | $0.0098 |

**优化建议**：
- 长边不超过 **1568 px**，否则会被自动缩放
- 图片总像素不超过 **1.15 兆像素**
- 任何边 < 200 px 的极小图片可能降低质量
- 先放图片，后放文字（提升理解质量）

### 2.3 Vision 限制

1. **不能识别人脸身份**——Claude 会拒绝此类请求
2. **空间推理有限**——精确定位（棋子位置、模拟时钟读数）可能出错
3. **大量物体计数不精确**——只能给出近似数
4. **不能判断 AI 生成图片**——不要用于伪造检测
5. **不适合复杂医学影像**——CT/MRI 需要专业工具

---

## 三、PDF 文档处理

### 3.1 PDF 处理原理

Claude 处理 PDF 的方式：
1. **每页转为图像** + **提取文本**
2. Claude **同时分析文本和视觉内容**（图表、图形、布局）
3. 响应时可以引用文本和视觉元素

### 3.2 输入方式

#### URL 引用

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "url",
                    "url": "https://example.com/report.pdf"
                }
            },
            {"type": "text", "text": "总结这份报告的关键发现"}
        ]
    }]
)
```

#### Base64 编码

```python
import base64

with open("report.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_data,
                }
            },
            {"type": "text", "text": "提取第 3 节的所有数据表格"}
        ]
    }]
)
```

#### Files API

```python
file = client.files.create(file=open("report.pdf", "rb"))

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {"type": "file", "file_id": file.id}
            },
            {"type": "text", "text": "分析这份文档的核心论点"}
        ]
    }]
)
```

### 3.3 PDF 限制与成本

| 限制项 | 值 |
|:------|:---|
| 最大请求体 | 32 MB |
| 最大页数 | 600 页（200K 上下文模型限 100 页） |
| 格式要求 | 标准 PDF（无密码/加密） |
| 每页 Token 消耗 | ~1,500-3,000 tokens（文本 + 图像） |

### 3.4 PDF 最佳实践

1. **PDF 放在文本之前**
2. 使用标准字体
3. 确保文本清晰可读
4. 将页面旋转到正确方向
5. 大型 PDF 拆分为多个小块
6. 对重复分析启用 Prompt Caching
7. 大批量使用 Batch API

---

## 四、Citations 引用系统

### 4.1 什么是 Citations

Citations 让 Claude 在回答文档相关问题时**自动提供引用**，标注信息来源的具体位置（页码、字符位置或内容块索引）。

### 4.2 启用引用

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "text",
                    "media_type": "text/plain",
                    "data": "The grass is green. The sky is blue. Water is essential for life."
                },
                "title": "Nature Facts",
                "citations": {"enabled": True}  # ← 启用引用
            },
            {"type": "text", "text": "What color is the grass and sky?"}
        ]
    }]
)
```

### 4.3 引用格式

根据文档类型不同，引用格式也不同：

| 文档类型 | 分块方式 | 引用格式 | 索引起始 |
|:---------|:---------|:---------|:---------|
| 纯文本 | 自动按句子 | 字符索引 | 0 |
| PDF | 自动按句子 | 页码 | 1 |
| 自定义内容 | 不额外分块 | 块索引 | 0 |

### 4.4 解析引用响应

```python
for block in response.content:
    if block.type == "text":
        print(block.text, end="")
        
        # 检查是否有引用
        if hasattr(block, "citations") and block.citations:
            for citation in block.citations:
                if citation.type == "char_location":
                    print(f" [来源: 字符 {citation.start_char_index}-{citation.end_char_index}]", end="")
                elif citation.type == "page_location":
                    print(f" [来源: 第 {citation.start_page_number}-{citation.end_page_number} 页]", end="")
                elif citation.type == "content_block_location":
                    print(f" [来源: 块 {citation.start_block_index}]", end="")
```

### 4.5 自定义内容文档（精细引用控制）

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "content",
                    "content": [
                        {"type": "text", "text": "Q1 revenue was $10M, up 25% YoY."},
                        {"type": "text", "text": "Q2 revenue was $12M, up 20% YoY."},
                        {"type": "text", "text": "Q3 revenue was $15M, up 30% YoY."},
                        {"type": "text", "text": "Q4 revenue was $18M, up 35% YoY."},
                    ]
                },
                "title": "Revenue Report",
                "context": "Annual financial data for FY2025",  # 不会被引用的上下文
                "citations": {"enabled": True}
            },
            {"type": "text", "text": "Which quarter had the highest growth rate?"}
        ]
    }]
)
```

### 4.6 Citations 优势

| 优势 | 说明 |
|:-----|:-----|
| **成本节约** | `cited_text` 不计入输出 token |
| **更可靠** | 引用保证指向源文档的有效位置 |
| **更高质量** | 比基于提示词的引用方案更准确 |
| **后续轮次免费** | `cited_text` 传回时不计入输入 token |

### 4.7 限制

- 不兼容 Structured Outputs（同时启用会返回 400 错误）
- 兼容 Prompt Caching、Token Counting、Batch Processing
- 仅支持文本引用，不支持图像引用
- Haiku 3 不支持

---

## 五、Files API 文件管理

### 5.1 核心功能

Files API 允许**上传一次，多次引用**，避免每次请求都发送完整文件内容。

> ⚠️ **Beta 版本**：需要在请求头添加 `anthropic-beta: files-api-2025-04-14`

### 5.2 支持的文件类型

| 类型 | MIME | 用途 |
|:-----|:-----|:-----|
| PDF | `application/pdf` | 文档分析 |
| 纯文本 | `text/plain` | 文本分析 |
| JPEG | `image/jpeg` | 图像分析 |
| PNG | `image/png` | 图像分析 |
| GIF | `image/gif` | 图像分析 |
| WebP | `image/webp` | 图像分析 |

### 5.3 完整工作流

```python
import anthropic

client = anthropic.Anthropic()

# 1. 上传文件
with open("report.pdf", "rb") as f:
    file = client.beta.files.create(file=f)
print(f"File ID: {file.id}")  # file_011CNha8iCJcU1wXNR6q4V8w

# 2. 在消息中使用
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    extra_headers={"anthropic-beta": "files-api-2025-04-14"},
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {"type": "file", "file_id": file.id}
            },
            {"type": "text", "text": "总结这份报告"}
        ]
    }]
)

# 3. 多次引用同一文件（无需重新上传）
response2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    extra_headers={"anthropic-beta": "files-api-2025-04-14"},
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {"type": "file", "file_id": file.id}  # 同一个 file_id
            },
            {"type": "text", "text": "提取所有数据表格"}
        ]
    }]
)

# 4. 列出所有文件
files = client.beta.files.list()
for f in files.data:
    print(f"{f.id}: {f.filename} ({f.size_bytes} bytes)")

# 5. 删除文件（不可恢复）
client.beta.files.delete(file.id)
```

### 5.4 存储限制

| 限制 | 值 |
|:-----|:---|
| 单文件大小 | 500 MB |
| 组织总存储 | 500 GB |
| 文件保留 | 直到手动删除 |
| 费用 | 免费（文件操作本身不收费） |

---

## 六、Token Counting 预估

### 6.1 免费的 Token 预估

在发送消息前预估 token 用量，帮助管理成本和速率限制：

```python
# 预估基础消息
count = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)
print(f"Input tokens: {count.input_tokens}")  # 14

# 预估包含工具的消息
count = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    tools=[{
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    }],
    messages=[{"role": "user", "content": "What's the weather?"}]
)
print(f"Input tokens (with tools): {count.input_tokens}")  # 403

# 预估包含图片的消息
count = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}},
            {"type": "text", "text": "Describe this image"}
        ]
    }]
)
print(f"Input tokens (with image): {count.input_tokens}")  # ~1551
```

### 6.2 速率限制

| 使用层级 | 每分钟请求数 (RPM) |
|:---------|:-----------------|
| Tier 1 | 100 |
| Tier 2 | 2,000 |
| Tier 3 | 4,000 |
| Tier 4 | 8,000 |

Token Counting 和消息创建有**独立的速率限制**，互不影响。

---

## 七、综合实战：多模态文档分析系统

```python
import anthropic
import base64

client = anthropic.Anthropic()


def analyze_document_with_citations(pdf_path: str, questions: list[str]):
    """多模态文档分析：PDF + Citations + 流式输出"""
    
    # 上传 PDF
    with open(pdf_path, "rb") as f:
        file = client.beta.files.create(file=f)
    
    print(f"📄 Uploaded: {pdf_path} → {file.id}")
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"❓ Question {i}: {question}")
        print(f"{'='*60}\n")
        
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            extra_headers={"anthropic-beta": "files-api-2025-04-14"},
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {"type": "file", "file_id": file.id},
                        "citations": {"enabled": True}
                    },
                    {"type": "text", "text": question}
                ]
            }]
        ) as stream:
            message = stream.get_final_message()
        
        # 解析带引用的响应
        for block in message.content:
            if block.type == "text":
                print(block.text, end="")
                if hasattr(block, "citations") and block.citations:
                    for c in block.citations:
                        if c.type == "page_location":
                            print(f" 📌[p.{c.start_page_number}]", end="")
        
        print(f"\n\n💰 Tokens: {message.usage.input_tokens} in / {message.usage.output_tokens} out")
    
    # 清理
    client.beta.files.delete(file.id)
    print(f"\n🗑️ Cleaned up file {file.id}")


# 使用示例
analyze_document_with_citations(
    "financial_report.pdf",
    [
        "What was the total revenue for Q4?",
        "Summarize the risk factors section.",
        "Extract all financial metrics from the tables.",
    ]
)
```

---

## 练习题

### 基础练习

1. **流式聊天应用**：创建一个终端聊天程序，支持多轮对话 + 流式输出。

2. **图片分析器**：编写一个脚本，接收图片 URL，输出 Claude 对图片的详细描述。

### 中级练习

3. **PDF 批量分析**：使用 Files API 上传多个 PDF，对每个提出相同的 3 个问题，将结果汇总到 CSV。

4. **带引用的文档问答**：构建一个文档问答系统，用户上传文本文件，系统返回带有精确字符位置引用的答案。

### 高级练习

5. **多模态对比分析**：上传两个版本的 PDF 报告，让 Claude 对比差异，为每个差异点提供引用来源。

6. **Token 成本估算器**：编写一个工具，在发送请求前预估所有内容（文本 + 图片 + PDF + 工具）的 token 成本。

---

> **下一步**：[12_Prompt_Caching与Batch_API.md](12_Prompt_Caching与Batch_API.md) — 成本优化双利器
