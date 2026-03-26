# 模块 11：Prompt Caching 与 Batch API — 成本优化双利器

> **官方文档**：  
> - Prompt Caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching  
> - Batch API: https://platform.claude.com/docs/en/build-with-claude/batch-processing  
> **预计学习时间**：3-4 小时  
> **难度**：⭐⭐⭐

---

## 目录

- [一、Prompt Caching 提示词缓存](#一prompt-caching-提示词缓存)
- [二、Batch API 批量处理](#二batch-api-批量处理)
- [三、Caching + Batch 叠加优化](#三caching--batch-叠加优化)
- [四、生产实战案例](#四生产实战案例)
- [练习题](#练习题)

---

## 一、Prompt Caching 提示词缓存

### 1.1 核心原理

Prompt Caching 允许**缓存提示词的前缀部分**。后续请求如果前缀相同，直接复用缓存，跳过处理。

```
请求 1: [System Prompt] + [长文档] + [问题 1]
         ↓ 缓存写入（全价 + 25%）
         
请求 2: [System Prompt] + [长文档] + [问题 2]
         ↓ 缓存命中（仅 10% 价格）
         
请求 3: [System Prompt] + [长文档] + [问题 3]
         ↓ 缓存命中（仅 10% 价格）
```

### 1.2 三大收益

| 收益 | 数据 |
|:-----|:-----|
| **降低成本** | 缓存命中仅需基础价格的 **10%**（省 90%） |
| **降低延迟** | 跳过缓存部分的处理，首 token 更快 |
| **提高吞吐** | 缓存命中不计入速率限制 |

### 1.3 两种使用方式

#### 自动缓存（推荐用于多轮对话）

```python
import anthropic

client = anthropic.Anthropic()

# 顶层声明自动缓存，SDK 自动管理断点
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},  # ← 顶层声明
    system="You are a legal document analyzer...",
    messages=[
        {"role": "user", "content": "Summarize section 3.2"},
    ]
)
```

#### 显式缓存断点（精细控制）

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are a financial analyst specializing in quarterly reports.",
        },
        {
            "type": "text",
            "text": "<quarterly_report>... 50,000 tokens of report data ...</quarterly_report>",
            "cache_control": {"type": "ephemeral"}  # ← 在此处设置缓存断点
        }
    ],
    messages=[
        {"role": "user", "content": "What was Q3 revenue?"}
    ]
)
```

### 1.4 定价详解

#### 缓存写入价格

| TTL | 相对于基础输入价格 | 说明 |
|:----|:-----------------|:-----|
| 5 分钟（默认） | 1.25 倍 | 免费 TTL |
| 1 小时 | 2 倍 | 付费 TTL |

#### 缓存命中价格

**缓存命中 = 基础价格 × 0.1（省 90%）**

#### 具体价格（每百万 Token）

| 模型 | 基础输入 | 5min 写入 | 1h 写入 | **缓存命中** | 节省 |
|:----|:--------|:---------|:--------|:-----------|:----|
| Opus 4.6 | $5.00 | $6.25 | $10.00 | **$0.50** | 90% |
| Sonnet 4.6 | $3.00 | $3.75 | $6.00 | **$0.30** | 90% |
| Haiku 4.5 | $1.00 | $1.25 | $2.00 | **$0.10** | 90% |

### 1.5 缓存 TTL（生命周期）

| TTL | 使用场景 | 配置 |
|:----|:---------|:-----|
| 5 分钟（默认） | 高频对话（每 5 分钟内有请求即刷新） | `{"type": "ephemeral"}` |
| 1 小时 | Extended Thinking 任务、低频但重要的对话 | `{"type": "ephemeral", "ttl": "1h"}` |

**混合 TTL 策略**：

```python
system=[
    # 系统提示很少变化 → 1 小时缓存
    {
        "type": "text",
        "text": "You are an expert financial analyst...",
        "cache_control": {"type": "ephemeral", "ttl": "1h"}
    },
    # 每日报告数据 → 5 分钟缓存
    {
        "type": "text",
        "text": f"Today's market data: {market_data}",
        "cache_control": {"type": "ephemeral"}  # 默认 5 分钟
    }
]
```

> ⚠️ **约束**：1 小时 TTL 的条目必须在 5 分钟 TTL 之前。

### 1.6 最小可缓存长度

| 模型 | 最小 Token 数 |
|:----|:-------------|
| Opus 4.6 / 4.5 | 4096 |
| Sonnet 4.6 | 2048 |
| Sonnet 4.5 / 4 / Opus 4.1 / 4 | 1024 |
| Haiku 4.5 | 4096 |

**低于此长度即使标记了 `cache_control` 也不会被缓存。**

### 1.7 监控缓存性能

```python
response = client.messages.create(...)

# 关键指标
usage = response.usage
print(f"缓存写入 Token: {usage.cache_creation_input_tokens}")  # 首次请求
print(f"缓存命中 Token: {usage.cache_read_input_tokens}")      # 后续请求
print(f"未缓存 Token:  {usage.input_tokens}")                  # 非缓存部分

# 总输入 = cache_read + cache_creation + input
total_input = (
    usage.cache_read_input_tokens + 
    usage.cache_creation_input_tokens + 
    usage.input_tokens
)
print(f"总输入 Token: {total_input}")

# 计算实际成本
PRICING = {"input": 3.0, "cache_read": 0.3, "cache_write": 3.75}  # Sonnet 4.6
cost = (
    usage.input_tokens * PRICING["input"] / 1_000_000 +
    usage.cache_read_input_tokens * PRICING["cache_read"] / 1_000_000 +
    usage.cache_creation_input_tokens * PRICING["cache_write"] / 1_000_000
)
print(f"输入成本: ${cost:.6f}")
```

### 1.8 缓存命中率优化

```python
class CacheMonitor:
    """监控和优化缓存命中率"""
    
    def __init__(self):
        self.total_requests = 0
        self.cache_hits = 0
        self.cache_tokens = 0
        self.uncached_tokens = 0
    
    def track(self, usage):
        self.total_requests += 1
        cache_read = getattr(usage, 'cache_read_input_tokens', 0) or 0
        cache_write = getattr(usage, 'cache_creation_input_tokens', 0) or 0
        uncached = getattr(usage, 'input_tokens', 0) or 0
        
        if cache_read > 0:
            self.cache_hits += 1
        self.cache_tokens += cache_read
        self.uncached_tokens += uncached
    
    def report(self):
        hit_rate = self.cache_hits / max(self.total_requests, 1) * 100
        print(f"Cache hit rate: {hit_rate:.1f}%")
        print(f"Cached tokens: {self.cache_tokens:,}")
        print(f"Uncached tokens: {self.uncached_tokens:,}")
        if self.cache_tokens > 0:
            savings = self.cache_tokens * 0.9  # 90% savings
            print(f"Estimated token savings: {savings:,.0f}")
```

### 1.9 常见陷阱

| 陷阱 | 说明 | 解决方案 |
|:----|:-----|:---------|
| 断点在变化内容上 | 时间戳/随机数导致缓存永不命中 | 把断点放在稳定内容末尾 |
| JSON Key 顺序不稳定 | Swift/Go 可能随机化 Key 顺序 | 确保 JSON 序列化稳定 |
| 并发请求 | 第一个响应前缓存不可用 | 等第一个响应后再发后续请求 |
| 修改 tool_choice | 会使缓存失效 | 保持 tool_choice 一致 |
| 内容太短 | 低于最小长度不缓存 | 确保缓存内容达到最小阈值 |
| 多模型混用 | 不同模型的缓存不共享 | 同一场景用同一模型 |

---

## 二、Batch API 批量处理

### 2.1 核心价值

| 特性 | 值 |
|:-----|:---|
| **成本折扣** | 50%（所有 token 半价） |
| **最大批次** | 100,000 个请求 |
| **异步处理** | 不需要等待实时响应 |
| **结果保留** | 29 天内可下载 |

### 2.2 工作流程

```
创建批次 → 异步处理（每个请求独立） → 轮询状态 → 下载结果
   ↓              ↓                       ↓            ↓
 POST 请求    后台处理中              GET 查询     JSONL 格式
              通常 < 1 小时            可选 webhook
              最长 24 小时
```

### 2.3 完整工作流代码

```python
import anthropic
import time

client = anthropic.Anthropic()

# ==========================================
# 步骤 1：创建批次
# ==========================================

batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"eval-{i:04d}",
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": f"Analyze code snippet #{i}: {code}"}
                ]
            }
        }
        for i, code in enumerate(code_snippets)
    ]
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.processing_status}")

# ==========================================
# 步骤 2：轮询状态
# ==========================================

while True:
    batch = client.messages.batches.retrieve(batch.id)
    counts = batch.request_counts
    
    print(f"Status: {batch.processing_status} | "
          f"Succeeded: {counts.succeeded} | "
          f"Errored: {counts.errored} | "
          f"Processing: {counts.processing}")
    
    if batch.processing_status == "ended":
        break
    
    time.sleep(60)  # 每分钟检查一次

# ==========================================
# 步骤 3：获取结果
# ==========================================

results = {}
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        text = result.result.message.content[0].text
        results[result.custom_id] = {
            "status": "success",
            "text": text[:200],
            "input_tokens": result.result.message.usage.input_tokens,
            "output_tokens": result.result.message.usage.output_tokens,
        }
    elif result.result.type == "errored":
        results[result.custom_id] = {
            "status": "error",
            "error": str(result.result.error),
        }
    elif result.result.type == "expired":
        results[result.custom_id] = {"status": "expired"}

# 统计
success = sum(1 for r in results.values() if r["status"] == "success")
print(f"\n✅ Succeeded: {success}/{len(results)}")
```

### 2.4 管理批次

```python
# 列出所有批次
for batch in client.messages.batches.list():
    print(f"{batch.id} | {batch.processing_status} | "
          f"Created: {batch.created_at}")

# 取消正在处理的批次
client.messages.batches.cancel(batch.id)
# 注意：已完成的请求不会回退
```

### 2.5 限制与规格

| 限制项 | 值 |
|:------|:---|
| 每批次最大请求数 | 100,000 |
| 每批次最大大小 | 256 MB |
| 每个组织活跃批次 | 取决于使用层级 |
| 典型处理时间 | < 1 小时 |
| 超时 | 24 小时未完成则过期 |
| 结果保留 | 创建后 29 天 |

### 2.6 Batch 定价

| 模型 | 标准输入 | 批处理输入 | 标准输出 | 批处理输出 | 节省 |
|:----|:--------|:---------|:--------|:---------|:----|
| Opus 4.6 | $5.00 | **$2.50** | $25.00 | **$12.50** | 50% |
| Sonnet 4.6 | $3.00 | **$1.50** | $15.00 | **$7.50** | 50% |
| Haiku 4.5 | $1.00 | **$0.50** | $5.00 | **$2.50** | 50% |

### 2.7 适用场景决策矩阵

| 场景 | 用 Batch? | 原因 |
|:----|:--------:|:-----|
| 大规模评估（1000+ 用例） | ✅ | 50% 折扣 + 并行 |
| 内容审核 | ✅ | 不需要实时 |
| 数据标注 | ✅ | 批量处理效率高 |
| 批量翻译 | ✅ | 不需要实时 |
| Prompt A/B 测试 | ✅ | 同一批次混合不同 prompt |
| 实时客服 | ❌ | 需要即时响应 |
| 交互式对话 | ❌ | 需要多轮实时交互 |
| 流式 UI 显示 | ❌ | 需要逐字输出 |

---

## 三、Caching + Batch 叠加优化

### 3.1 双重折扣

Batch API 支持 Prompt Caching，**两者折扣可叠加**：

```
标准价格:  $3.00/MTok（Sonnet 4.6 输入）
Batch 折扣: $1.50/MTok（-50%）
+ 缓存命中:  $0.15/MTok（-90% on batch price）

最终: 仅为标准价格的 5%！
```

### 3.2 实战：大规模评估 + 双重优化

```python
import anthropic

client = anthropic.Anthropic()

# 共享上下文（会被缓存）
SHARED_SYSTEM = """You are a code quality evaluator. Analyze the provided code 
for bugs, security issues, and best practice violations.

<evaluation_criteria>
... 5000 tokens of detailed criteria ...
</evaluation_criteria>

<scoring_rubric>
... 3000 tokens of scoring rules ...
</scoring_rubric>"""


def create_evaluation_batch(code_snippets: list[dict]):
    """创建带 Prompt Caching 的评估批次"""
    
    requests = []
    for i, snippet in enumerate(code_snippets):
        requests.append({
            "custom_id": f"eval-{i:05d}",
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 1024,
                "system": [
                    {
                        "type": "text",
                        "text": SHARED_SYSTEM,
                        "cache_control": {"type": "ephemeral"}  # ← 缓存共享上下文
                    }
                ],
                "messages": [
                    {
                        "role": "user",
                        "content": f"Evaluate this code:\n```\n{snippet['code']}\n```"
                    }
                ]
            }
        })
    
    batch = client.messages.batches.create(requests=requests)
    return batch


# 1000 个代码片段的批量评估
# 成本估算（假设共享上下文 8000 tokens，每个问题 500 tokens）：
# - 无优化:  8500 × 1000 × $3.00/MTok = $25.50
# - Batch:   8500 × 1000 × $1.50/MTok = $12.75 (省 50%)
# - Batch + Cache: (500 × $1.50 + 8000 × $0.15) × 1000 / 1M = $1.95 (省 92%!)
```

### 3.3 成本优化总结

| 策略组合 | 输入成本（vs 标准） | 适用场景 |
|:--------|:-----------------|:---------|
| 标准 API | 100% | 实时单次请求 |
| + Prompt Caching | 10%（命中部分） | 多轮对话、重复前缀 |
| + Batch API | 50% | 大规模离线处理 |
| + Batch + Caching | **5%**（命中部分） | 大规模评估、数据处理 |

---

## 四、生产实战案例

### 4.1 多轮对话缓存优化

```python
class CachedConversation:
    """自动管理缓存的多轮对话"""
    
    def __init__(self, system_prompt: str, model: str = "claude-sonnet-4-6"):
        self.client = anthropic.Anthropic()
        self.system = [
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}
            }
        ]
        self.model = model
        self.messages = []
    
    def chat(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.system,
            messages=self.messages,
        )
        
        assistant_text = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_text})
        
        # 打印缓存状态
        usage = response.usage
        cached = getattr(usage, 'cache_read_input_tokens', 0) or 0
        written = getattr(usage, 'cache_creation_input_tokens', 0) or 0
        print(f"  💾 Cache: {cached} read / {written} written / {usage.input_tokens} uncached")
        
        return assistant_text


# 使用示例
conv = CachedConversation(
    system_prompt="You are an expert Python developer. Here is the project codebase:\n"
                   + open("src/main.py").read()  # 假设有几千 token
)

# 第 1 轮：缓存写入
print(conv.chat("What does the main function do?"))
# 💾 Cache: 0 read / 5000 written / 50 uncached

# 第 2 轮：缓存命中！
print(conv.chat("Any bugs in the error handling?"))
# 💾 Cache: 5000 read / 0 written / 100 uncached  ← 省了 90%
```

### 4.2 大规模内容审核

```python
def batch_content_moderation(contents: list[str]) -> dict:
    """使用 Batch API 进行大规模内容审核"""
    
    MODERATION_PROMPT = """Analyze the following content for policy violations.
    
Categories to check:
- Hate speech or discrimination
- Violence or threats
- Explicit content
- Misinformation
- Spam

Respond in JSON: {"safe": true/false, "category": "none"|"hate"|"violence"|"explicit"|"misinfo"|"spam", "confidence": 0.0-1.0}"""
    
    # 创建批次
    batch = client.messages.batches.create(
        requests=[
            {
                "custom_id": f"mod-{i:06d}",
                "params": {
                    "model": "claude-haiku-4-5",  # 审核用 Haiku 更经济
                    "max_tokens": 200,
                    "system": [
                        {
                            "type": "text",
                            "text": MODERATION_PROMPT,
                            "cache_control": {"type": "ephemeral"}
                        }
                    ],
                    "messages": [
                        {"role": "user", "content": content}
                    ]
                }
            }
            for i, content in enumerate(contents)
        ]
    )
    
    # 等待完成
    while True:
        batch = client.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            break
        time.sleep(30)
    
    # 收集结果
    import json
    results = {}
    for result in client.messages.batches.results(batch.id):
        if result.result.type == "succeeded":
            try:
                moderation = json.loads(result.result.message.content[0].text)
                results[result.custom_id] = moderation
            except json.JSONDecodeError:
                results[result.custom_id] = {"safe": None, "error": "parse_error"}
    
    return results
```

---

## 练习题

### 基础练习

1. **缓存效果对比**：发送 10 个不同问题给同一个长系统提示（>4096 tokens），对比第一次和后续请求的 token 用量和延迟。

2. **简单 Batch**：创建一个包含 10 个翻译请求的批次，将一段英文翻译成 10 种不同语言。

### 中级练习

3. **缓存监控仪表板**：编写 `CacheMonitor` 类，跟踪缓存命中率、节省的 token 数和估计节省的费用。

4. **Batch 重试逻辑**：实现一个 Batch 管理器，自动重试失败和过期的请求。

### 高级练习

5. **Batch + Cache 叠加**：对 500 个代码片段进行质量评估，使用 Batch API + Prompt Caching，计算双重折扣后的实际成本。

6. **混合 TTL 策略**：实现一个对话系统，系统提示用 1 小时 TTL，文档内容用 5 分钟 TTL，监控两种缓存的命中率。

---

> **下一步**：[13_安全护栏与生产部署.md](13_安全护栏与生产部署.md) — 输入输出验证 + 升级决策 + 限流重试
