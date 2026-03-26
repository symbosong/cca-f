# 模块 7：Agent 工作流与智能体

> **对应课程**：Building with the Claude API — Module 7: Agents and Workflows  
> **视频数量**：7 个（约 26 分钟）  
> **预计学习时间**：1-2 小时  
> **难度**：⭐⭐⭐

### 📌 原课程地址

| 平台 | 链接 |
|------|------|
| **Skilljar（官方）** | https://anthropic.skilljar.com/claude-with-the-anthropic-api |
| **Coursera（镜像）** | https://www.coursera.org/learn/building-with-the-claude-api |

### 📌 视频课时清单

| # | 视频标题 | 时长 | 核心知识点 |
|:-:|---------|:----:|-----------|
| 1 | AI Workflows | 4m | 工作流 vs Agent 的区别、何时选择哪种 |
| 2 | Parallelization Workflows | 4m | 并行化模式：拆分→并发→汇总 |
| 3 | Chaining Workflows | 5m | 链式模式：前一步输出→下一步输入 |
| 4 | Routing Workflows | 3m | 路由模式：先分类→再交给专业处理 |
| 5 | Agents and Tools | 5m | Agent 循环：stop_reason 驱动的核心 |
| 6 | Environment Inspection | 3m | Agent 如何感知当前环境状态 |
| 7 | Workflows vs Agents | 2m | 总结对比：简单用工作流，复杂用 Agent |

> **阅读材料**（2 篇，10 分钟）：Module Introduction / Next Steps

---

## 本模块学习目标

完成本模块后，你将能够：
1. 理解 Agent 与 Workflow 的区别
2. 掌握三种核心工作流模式：链式、路由、并行
3. 掌握两种 Agent 模式：工具循环 Agent、编排器 Agent
4. 使用 Anthropic Agent SDK 构建 Agent
5. 实现完整的 Agent Loop
6. 理解 Agent 的安全护栏和生产部署

---

## 第 1 课：AI 工作流

> 📹 视频：AI Workflows（4 min）

### Workflow vs Agent

| | Workflow（工作流） | Agent（智能体） |
|---|---|---|
| **定义** | 预定义的固定流程 | 动态决策的自主系统 |
| **控制流** | 代码控制，可预测 | 模型控制，灵活 |
| **适用** | 流程固定、需要可靠性 | 流程不确定、需要适应性 |
| **例子** | 数据管道、审批流程 | 客服机器人、研究助手 |

> 📏 **Anthropic 的建议**：如果能用 Workflow 解决，就不要用 Agent。Workflow 更可预测、更容易调试。

### 选择决策树

```
你的任务流程是固定的吗？
├── 是 → 用 Workflow
│   ├── 步骤是串行的？ → 链式（Chaining）
│   ├── 需要根据输入分流？ → 路由（Routing）
│   └── 步骤可以并行？ → 并行化（Parallelization）
│
└── 否 → 需要根据中间结果动态决定下一步？
    ├── 单个 Agent 就够？ → 工具循环 Agent
    └── 需要多个专家协作？ → 编排器-执行器 Agent
```

---

## 第 2 课：并行化工作流

> 📹 视频：Parallelization Workflows（4 min）

### 多个独立任务同时执行，然后汇总

```
          ┌→ [安全审查] ──┐
输入 ──→  ├→ [性能分析] ──┤→ [汇总报告]
          └→ [代码风格] ──┘
```

```python
import asyncio
import anthropic

async def parallel_workflow(code_to_review):
    """并行工作流：多维度代码审查"""
    async_client = anthropic.AsyncAnthropic()
    
    tasks = {
        "security": {"system": "You are a security expert.", "prompt": f"Review for security:\n\n{code_to_review}"},
        "performance": {"system": "You are a performance engineer.", "prompt": f"Review for performance:\n\n{code_to_review}"},
        "style": {"system": "You are a code quality expert.", "prompt": f"Review for readability:\n\n{code_to_review}"},
    }
    
    async def run_review(name, task):
        response = await async_client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=1024,
            system=task["system"],
            messages=[{"role": "user", "content": task["prompt"]}]
        )
        return name, response.content[0].text
    
    results = await asyncio.gather(*[run_review(n, t) for n, t in tasks.items()])
    reviews = {name: text for name, text in results}
    
    # 汇总
    combined = "\n\n".join([f"=== {n.upper()} ===\n{t}" for n, t in reviews.items()])
    summary = await async_client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1024,
        system="Summarize code review findings into a prioritized action plan.",
        messages=[{"role": "user", "content": combined}]
    )
    return {"reviews": reviews, "summary": summary.content[0].text}
```

**适用场景**：多维度分析、多模型投票、数据并行采集。

---

## 第 3 课：链式工作流

> 📹 视频：Chaining Workflows（5 min）

### 前一步的输出作为后一步的输入

```
输入 → [步骤1: 分析需求] → [步骤2: 生成代码] → [步骤3: 代码审查] → 输出
```

```python
def chain_workflow(user_request):
    """链式工作流：需求分析 → 代码生成 → 代码审查"""
    
    analysis = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1024,
        system="You are a software architect. Create a technical spec.",
        messages=[{"role": "user", "content": f"Analyze: {user_request}"}]
    ).content[0].text
    
    code = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096,
        system="You are an expert Python developer.",
        messages=[{"role": "user", "content": f"Implement based on this spec:\n\n{analysis}"}]
    ).content[0].text
    
    review = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1024,
        system="You are a code reviewer.",
        messages=[{"role": "user", "content": f"Review this code:\n\n{code}"}]
    ).content[0].text
    
    return {"analysis": analysis, "code": code, "review": review}
```

**适用场景**：数据管道、文档生成（大纲→初稿→编辑）、多阶段翻译。

---

## 第 4 课：路由工作流

> 📹 视频：Routing Workflows（3 min）

### 先分类，再交给专业处理

```
输入 → [分类器] → 技术问题 → [技术专家 Prompt]
                 → 账单问题 → [账单专家 Prompt]
                 → 一般咨询 → [通用助手 Prompt]
```

```python
def routing_workflow(user_message):
    """路由工作流：智能客服路由"""
    
    # 用 Haiku 做分类（快且便宜）
    category = client.messages.create(
        model="claude-haiku-4-20250514", max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"Classify as technical/billing/general:\n\n{user_message}\n\nRespond with one word."
        }]
    ).content[0].text.strip().lower()
    
    expert_prompts = {
        "technical": "You are a senior technical support engineer...",
        "billing": "You are a billing specialist...",
        "general": "You are a friendly customer service rep..."
    }
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=2048,
        system=expert_prompts.get(category, expert_prompts["general"]),
        messages=[{"role": "user", "content": user_message}]
    ).content[0].text
    
    return {"category": category, "response": response}
```

**适用场景**：多语言处理、客服系统、内容审核。

---

## 第 5 课：Agent 与工具循环

> 📹 视频：Agents and Tools（5 min）

### Agent 循环：stop_reason 驱动的核心模式

这是所有 Agent 的核心——循环执行工具调用直到 Claude 给出最终回答：

```python
import json

def agent_loop(user_message, tools, process_tool_fn, max_turns=20):
    """通用 Agent Loop"""
    messages = [{"role": "user", "content": user_message}]
    system = "You are a helpful assistant with access to tools."
    
    for turn in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=4096,
            system=system, tools=tools, messages=messages
        )
        
        if response.stop_reason == "end_turn":
            return "".join(b.text for b in response.content if hasattr(b, "text"))
        
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  🔧 {block.name}({json.dumps(block.input, ensure_ascii=False)})")
                    try:
                        result = process_tool_fn(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result", "tool_use_id": block.id,
                            "content": json.dumps(result) if not isinstance(result, str) else result,
                        })
                    except Exception as e:
                        tool_results.append({
                            "type": "tool_result", "tool_use_id": block.id,
                            "content": f"Error: {str(e)}", "is_error": True,
                        })
            messages.append({"role": "user", "content": tool_results})
    
    return "⚠️ 达到最大轮次限制"
```

---

## 第 6 课：环境审查

> 📹 视频：Environment Inspection（3 min）

### Agent 如何感知当前状态

Agent 可以通过工具来"感知环境"——读取文件、查看目录结构、获取系统信息。这些读取类工具让 Agent 在采取行动前先理解当前状态。

---

## 第 7 课：工作流 vs Agent 总结

> 📹 视频：Workflows vs Agents（2 min）

### 最终对比

| 维度 | Workflow | Agent |
|------|---------|-------|
| 可预测性 | ✅ 高 | ⚠️ 低 |
| 可调试性 | ✅ 容易 | ⚠️ 困难 |
| 灵活性 | ⚠️ 低 | ✅ 高 |
| 适用场景 | 流程固定的任务 | 复杂开放性任务 |

**核心原则**：简单任务用工作流（可预测/可调试），复杂开放任务用 Agent（灵活/自主）。

---

## 补充：编排器-执行器模式

一个"编排器" Agent 分解任务，多个"执行器" Agent 并行处理：

```python
async def orchestrator_agent(user_request):
    """编排器-执行器 Agent"""
    async_client = anthropic.AsyncAnthropic()
    
    # 编排器分解任务
    plan = await async_client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1024,
        system="Break down complex requests into independent subtasks.",
        messages=[{"role": "user", "content": f"Break into subtasks (JSON array):\n{user_request}"}]
    )
    subtasks = json.loads(plan.content[0].text)
    
    # 并行执行子任务
    async def execute(subtask):
        r = await async_client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=2048,
            system=f"You are a {subtask['role']}.",
            messages=[{"role": "user", "content": subtask["task"]}]
        )
        return subtask["id"], r.content[0].text
    
    results = await asyncio.gather(*[execute(t) for t in subtasks])
    
    # 汇总
    results_text = "\n\n".join([f"=== Subtask {id} ===\n{text}" for id, text in results])
    final = await async_client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096,
        system="Synthesize subtask results into a comprehensive response.",
        messages=[{"role": "user", "content": f"Original: {user_request}\n\nResults:\n{results_text}"}]
    )
    return final.content[0].text
```

---

## 补充：Anthropic Agent SDK

```bash
pip install anthropic-agent-sdk
```

```python
from agent_sdk import Agent, tool

agent = Agent(
    name="research-assistant",
    model="claude-sonnet-4-20250514",
    instructions="You are a research assistant.",
)

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"

agent.tools = [search_web]
# result = agent.run("Research quantum computing.")
```

---

## 补充：安全护栏

### 输入/输出过滤

```python
def input_guard(user_message):
    """检查输入是否安全"""
    response = client.messages.create(
        model="claude-haiku-4-20250514", max_tokens=50,
        messages=[{"role": "user", "content": f"Is this safe for a customer service bot?\n\n{user_message}\n\nSAFE or UNSAFE"}]
    )
    return "SAFE" in response.content[0].text.upper()
```

### 升级决策（Human-in-the-Loop）

```python
ESCALATION_TRIGGERS = ["legal action", "speak to manager", "data breach"]

def should_escalate(message):
    for trigger in ESCALATION_TRIGGERS:
        if trigger.lower() in message.lower():
            return True
    return False
```

---

## 补充：生产部署检查清单

```
✅ 架构选择
  □ Workflow 还是 Agent（优先 Workflow）
  □ 选择合适的工作流模式
  □ 确定工具集合和权限

✅ 安全
  □ 输入过滤 / 输出过滤 / 升级机制 / 工具权限最小化 / 审计日志

✅ 可靠性
  □ 错误处理 / 最大轮次限制 / 超时设置 / 降级方案

✅ 成本控制
  □ Prompt Caching / 模型选择 / 监控 token / 预算告警
```

---

## 练习题

### 练习 1：链式工作流

构建"博客生成器"：主题→大纲→初稿→编辑→摘要+SEO标题。

### 练习 2：路由 + Agent

构建智能助手，根据输入自动路由到计算器/翻译器/搜索/代码助手。

### 练习 3：安全护栏

为练习 2 添加完整的安全护栏：输入过滤+升级决策+输出检查+审计日志。

---

## 扩展阅读

| 资源 | 链接 |
|------|------|
| Anthropic Agent 文档 | https://docs.anthropic.com/en/docs/build-with-claude/agentic |
| Agent SDK | https://github.com/anthropics/agent-sdk |
| Building Effective Agents | https://www.anthropic.com/research/building-effective-agents |
| 安全护栏文档 | https://docs.anthropic.com/en/docs/build-with-claude/safety-guardrails |

---

## 🎓 课程总结

恭喜你完成了所有 7 个模块的学习！

| 模块 | 核心能力 |
|------|---------|
| 1. Claude 入门 | API 调用、消息格式、模型选择、参数 |
| 2. 提示工程与评估 | 提示技巧、思维链、评估管道 |
| 3. 工具使用与高级特性 | 工具调用、Agent Loop、缓存、Extended Thinking |
| 4. MCP 协议 | 标准化工具连接、MCP Server 开发 |
| 5. RAG | 检索增强生成、向量数据库、分块策略 |
| 6. Claude Code & Computer Use | AI 编程助手、桌面操控 |
| 7. Agent 工作流 | 工作流模式、Agent 架构、安全护栏 |

### 下一步

1. **动手实践**：把学到的知识应用到实际项目中
2. **深入文档**：阅读 [Anthropic 官方文档](https://docs.anthropic.com)
3. **关注生态**：关注 MCP 生态和 Agent SDK 的发展
4. **（可选）备考 CCA-F** 验证掌握程度

---

> 📖 返回 [学习大纲](00_学习大纲与资源总览.md)
