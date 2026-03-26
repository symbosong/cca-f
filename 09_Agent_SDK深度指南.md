# 模块 8：Agent SDK 深度指南 — 构建生产级自主智能体

> **官方文档**：https://platform.claude.com/docs/en/agent-sdk/overview  
> **GitHub 仓库**：https://github.com/anthropics/claude-agent-sdk-python / claude-agent-sdk-typescript  
> **前置要求**：已完成模块 1-7 的学习，熟悉 Claude API 基本调用  
> **预计学习时间**：5-6 小时  
> **难度**：⭐⭐⭐⭐

---

## 目录

- [一、Agent SDK 是什么](#一agent-sdk-是什么)
- [二、核心架构与 Agent Loop](#二核心架构与-agent-loop)
- [三、快速上手](#三快速上手)
- [四、内置工具体系](#四内置工具体系)
- [五、工具权限与安全控制](#五工具权限与安全控制)
- [六、上下文管理与自动压缩](#六上下文管理与自动压缩)
- [七、MCP 服务器连接](#七mcp-服务器连接)
- [八、子智能体与多 Agent 编排](#八子智能体与多-agent-编排)
- [九、Hooks 钩子集成](#九hooks-钩子集成)
- [十、会话管理与恢复](#十会话管理与恢复)
- [十一、结构化输出](#十一结构化输出)
- [十二、生产部署最佳实践](#十二生产部署最佳实践)
- [十三、Agent SDK vs 其他方案对比](#十三agent-sdk-vs-其他方案对比)
- [练习题](#练习题)

---

## 一、Agent SDK 是什么

Agent SDK（前身 Claude Code SDK）是 Anthropic 官方提供的**构建自主 AI 智能体**的开发工具包。它把 Claude Code 的完整能力——工具执行、智能体循环、上下文管理——以**库**的形式提供给你编程调用。

### 1.1 为什么需要 Agent SDK

你可能会问：我用 Messages API 手动编排工具不行吗？行，但 Agent SDK 帮你解决了这些痛点：

| 痛点 | Messages API（手动） | Agent SDK（自动） |
|:-----|:-------------------|:----------------|
| 工具调用循环 | 你自己写 while 循环判断 stop_reason | SDK 内置 Agent Loop 自动管理 |
| 文件读写 | 你自己实现 read/write/edit 逻辑 | 内置 Read/Edit/Write/Glob/Grep |
| Shell 命令 | 你自己实现 subprocess 调用 + 安全检查 | 内置 Bash 工具 + 权限控制 |
| 上下文溢出 | 你自己实现截断/压缩策略 | 自动压缩（compact），保留关键信息 |
| 权限管理 | 你自己实现审批逻辑 | 三种权限模式 + 工具白名单/黑名单 |
| 成本控制 | 你自己跟踪 token 用量 | 内置 max_budget_usd + 成本跟踪 |
| 会话持久化 | 你自己管理消息历史存储 | 内置会话 ID + 恢复机制 |

### 1.2 关键区别总结

```
┌──────────────────────────────────────────────────────┐
│  Messages API = 你是"交响乐指挥"，每个乐章都得你挥棒    │
│  Agent SDK   = 你是"项目经理"，下达目标，Agent 自己搞定  │
└──────────────────────────────────────────────────────┘
```

---

## 二、核心架构与 Agent Loop

### 2.1 架构总览

```
┌──────────────────────────────────────────────────────┐
│                    你的应用代码                         │
│  ┌─────────────────────────────────────────────────┐ │
│  │   query() / stream()   ← 主入口                  │ │
│  └──────────┬──────────────────────────────────────┘ │
│             │                                        │
│  ┌──────────▼──────────────────────────────────────┐ │
│  │           Agent Loop（智能体循环）                 │ │
│  │                                                  │ │
│  │  ┌────────────────────────────────────────────┐  │ │
│  │  │  1. 接收提示 → 构建完整上下文               │  │ │
│  │  │     (system prompt + CLAUDE.md + tools      │  │ │
│  │  │      + conversation history)                │  │ │
│  │  └──────────┬─────────────────────────────────┘  │ │
│  │             │                                    │ │
│  │  ┌──────────▼─────────────────────────────────┐  │ │
│  │  │  2. Claude 模型推理                         │  │ │
│  │  │     → 返回 text / tool_use / 两者兼有       │  │ │
│  │  └──────────┬─────────────────────────────────┘  │ │
│  │             │                                    │ │
│  │  ┌──────────▼─────────────────────────────────┐  │ │
│  │  │  3. 执行工具                               │  │ │
│  │  │     → 权限检查 → PreToolUse Hook           │  │ │
│  │  │     → 执行（只读并发/写入串行）             │  │ │
│  │  │     → PostToolUse Hook                      │  │ │
│  │  │     → 结果反馈给 Claude                     │  │ │
│  │  └──────────┬─────────────────────────────────┘  │ │
│  │             │                                    │ │
│  │  ┌──────────▼─────────────────────────────────┐  │ │
│  │  │  4. 重复步骤 2-3                           │  │ │
│  │  │     直到 Claude 返回无工具调用的响应         │  │ │
│  │  └──────────┬─────────────────────────────────┘  │ │
│  │             │                                    │ │
│  │  ┌──────────▼─────────────────────────────────┐  │ │
│  │  │  5. 返回 ResultMessage                     │  │ │
│  │  │     (最终文本 + token + cost + session_id)  │  │ │
│  │  └────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

### 2.2 Agent Loop 详解

每个 Agent 会话遵循相同的 **5 步循环**：

| 步骤 | 动作 | 产出消息 |
|:-----|:-----|:---------|
| 1. 接收提示 | Claude 接收 prompt + system prompt + 工具定义 + 对话历史 | `SystemMessage` (subtype: "init") |
| 2. 评估与响应 | Claude 决定返回文本、工具调用或两者 | `AssistantMessage` |
| 3. 执行工具 | SDK 运行每个工具，收集结果 | `UserMessage`（包含工具结果） |
| 4. 重复 | 步骤 2-3 作为循环重复（每次完整循环 = 一个"回合"） | 持续生成消息 |
| 5. 返回结果 | Claude 返回无工具调用的最终响应 | `ResultMessage` |

### 2.3 消息类型

SDK 在循环运行时生成 **5 种核心消息类型**：

```python
from claude_agent_sdk import (
    SystemMessage, AssistantMessage, UserMessage, 
    StreamEvent, ResultMessage
)

async for message in query(prompt="...", options=options):
    
    if isinstance(message, SystemMessage):
        # 会话生命周期事件
        # subtype: "init"（首条消息）, "compact_boundary"（压缩后触发）
        print(f"[System] {message.subtype}")
    
    elif isinstance(message, AssistantMessage):
        # Claude 的每次响应（含工具调用和文本）
        for block in message.content:
            if hasattr(block, "text"):
                print(f"[Claude] {block.text}")
            elif hasattr(block, "name"):
                print(f"[Tool Call] {block.name}({block.input})")
    
    elif isinstance(message, UserMessage):
        # 工具执行结果（自动反馈给 Claude）
        for block in message.content:
            print(f"[Tool Result] {block}")
    
    elif isinstance(message, StreamEvent):
        # 仅在启用部分消息时发出
        # 包含原始 API 流式事件
        pass
    
    elif isinstance(message, ResultMessage):
        # 最后一条消息
        print(f"[Done] {message.subtype}")
        print(f"  Result: {message.result}")
        print(f"  Cost: ${message.total_cost_usd:.4f}")
        print(f"  Tokens: {message.total_input_tokens} in / {message.total_output_tokens} out")
        print(f"  Session ID: {message.session_id}")
```

### 2.4 ResultMessage 终止状态

| 子类型 | 含义 | `result` 字段 |
|:-------|:-----|:-------------|
| `success` | Claude 正常完成任务 | ✅ 有 |
| `error_max_turns` | 达到 `max_turns` 限制 | ❌ 无 |
| `error_max_budget_usd` | 达到 `max_budget_usd` 限制 | ❌ 无 |
| `error_during_execution` | 执行出错中断 | ❌ 无 |
| `error_max_structured_output_retries` | 结构化输出验证失败 | ❌ 无 |

---

## 三、快速上手

### 3.1 安装

```bash
# Python
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk
```

### 3.2 设置 API Key

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### 3.3 最小示例：代码审查 Agent

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def code_review_agent():
    """只读代码审查 Agent — 分析代码但不修改"""
    
    async for message in query(
        prompt="Review all Python files in the current directory for bugs, "
               "security issues, and code quality. Provide a summary report.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep"],  # 只读工具
            permission_mode="bypassPermissions",      # 无需确认（因为只读）
            max_turns=20,
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"🔧 {block.name}")
        
        elif isinstance(message, ResultMessage):
            if message.subtype == "success":
                print(f"\n✅ 审查完成 | 成本: ${message.total_cost_usd:.4f}")
            else:
                print(f"\n❌ {message.subtype}")


asyncio.run(code_review_agent())
```

### 3.4 完整示例：Bug 修复 Agent

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def bugfix_agent(description: str):
    """自动 Bug 修复 Agent"""
    
    async for message in query(
        prompt=f"Find and fix this bug: {description}\n"
               "After fixing, run the tests to verify the fix.",
        options=ClaudeAgentOptions(
            # 工具控制
            allowed_tools=["Read", "Edit", "Write", "Glob", "Grep", "Bash"],
            permission_mode="acceptEdits",  # 自动批准文件编辑
            
            # 安全限制
            max_turns=30,          # 最多 30 个工具调用回合
            max_budget_usd=1.0,    # 最多花费 $1
            
            # 推理深度
            effort="high",         # 深入分析
            
            # 自定义系统提示
            system_prompt=(
                "You are a senior Python developer. "
                "Always follow PEP 8. Write comprehensive tests. "
                "Explain your reasoning before making changes."
            ),
            
            # 加载项目配置（CLAUDE.md）
            setting_sources=["project"],
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"\n🔧 Tool: {block.name}")
        
        elif isinstance(message, ResultMessage):
            print(f"\n{'='*50}")
            print(f"Status: {message.subtype}")
            print(f"Cost: ${message.total_cost_usd:.4f}")
            print(f"Tokens: {message.total_input_tokens} in / {message.total_output_tokens} out")


asyncio.run(bugfix_agent("Tests failing in auth module due to None user handling"))
```

---

## 四、内置工具体系

Agent SDK 内置了与 Claude Code 完全相同的工具集：

### 4.1 工具分类

| 类别 | 工具 | 功能 | 并发 |
|:-----|:-----|:-----|:----:|
| **文件操作** | `Read` | 读取文件内容 | ✅ |
| | `Edit` | 修改已有文件 | ❌ 串行 |
| | `Write` | 创建新文件 / 覆盖 | ❌ 串行 |
| **搜索** | `Glob` | 按模式查找文件 | ✅ |
| | `Grep` | 用正则搜索文件内容 | ✅ |
| **执行** | `Bash` | 运行 Shell 命令 | ❌ 串行 |
| **网络** | `WebSearch` | 搜索互联网 | ✅ |
| | `WebFetch` | 获取并解析网页 | ✅ |
| **发现** | `ToolSearch` | 动态查找和加载工具 | ✅ |
| **编排** | `Agent` | 生成子智能体 | ❌ 串行 |
| | `Skill` | 调用预定义技能 | ❌ 串行 |
| | `AskUserQuestion` | 向用户提问 | ❌ 串行 |
| | `TodoWrite` | 跟踪任务进度 | ❌ 串行 |

> **并发规则**：只读工具可以并发运行，修改状态的工具必须串行执行，避免冲突。

### 4.2 工具组合推荐

| 场景 | 推荐工具 | 说明 |
|:-----|:---------|:-----|
| 代码审查（只读） | `Read, Glob, Grep` | 安全，不修改任何文件 |
| Bug 修复 | `Read, Edit, Glob, Grep, Bash` | 分析 + 修改 + 测试 |
| 项目生成 | `Read, Write, Bash, Glob` | 创建新文件 + 初始化 |
| 研究任务 | `Read, Glob, Grep, WebSearch, WebFetch` | 代码分析 + 联网搜索 |
| 全自动开发 | 全部工具 | 端到端自动化 |
| 文档生成 | `Read, Write, Glob, Grep` | 分析代码 + 生成文档 |

### 4.3 ToolSearch：动态工具发现

当你连接了大量 MCP 服务器（可能几十上百个工具），**不要全部预加载**——使用 `ToolSearch` 让 Claude 按需查找：

```python
options = ClaudeAgentOptions(
    allowed_tools=[
        "Read", "Edit", "Glob", "Grep", "Bash",
        "ToolSearch",  # 启用动态工具发现
    ],
    # Claude 会在需要时自动搜索可用工具
    # 大幅减少上下文消耗
)
```

---

## 五、工具权限与安全控制

### 5.1 三层权限控制

```
┌─────────────────────────────────────────┐
│  第一层：allowed_tools（白名单）          │  ← 列出的工具自动批准
├─────────────────────────────────────────┤
│  第二层：disallowed_tools（黑名单）       │  ← 列出的工具无条件阻止
├─────────────────────────────────────────┤
│  第三层：permission_mode（默认行为）      │  ← 未在白/黑名单中的工具
└─────────────────────────────────────────┘
```

### 5.2 权限模式

| 模式 | 行为 | 适用场景 |
|:----|:-----|:---------|
| `default` | 未列出的工具触发审批回调；无回调 = 拒绝 | 需要人工审批的场景 |
| `acceptEdits` | 自动批准文件编辑，其他遵循 default | 日常开发（最常用） |
| `plan` | 不执行任何工具，Claude 只生成计划 | 方案评审、预览 |
| `bypassPermissions` | 所有工具自动批准 | 沙盒化 CI/CD 环境 |

### 5.3 生产环境权限配置示例

```python
# 场景 1：安全的代码审查服务
review_options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep"],         # 只允许只读
    disallowed_tools=["Bash", "Write", "Edit"],      # 明确禁止修改
    permission_mode="bypassPermissions",             # 只读安全，无需确认
)

# 场景 2：受控的自动修复服务
fix_options = ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Glob", "Grep"],  # 允许编辑
    disallowed_tools=["Bash", "Write"],               # 禁止命令执行和新建文件
    permission_mode="acceptEdits",                    # 自动批准编辑
    max_turns=10,                                     # 限制回合数
    max_budget_usd=0.5,                               # 限制成本
)

# 场景 3：CI/CD 全自动管道
ci_options = ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Write", "Bash", "Glob", "Grep"],
    permission_mode="bypassPermissions",  # CI 环境全自动
    max_turns=50,
    max_budget_usd=5.0,
    effort="high",
)
```

### 5.4 自定义审批回调

当使用 `default` 权限模式时，未列入白名单的工具会触发你的回调函数：

```python
async def approval_callback(tool_name: str, tool_input: dict) -> bool:
    """自定义审批逻辑"""
    
    # 危险命令检测
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        dangerous_patterns = ["rm -rf", "sudo", "chmod 777", "curl | sh"]
        for pattern in dangerous_patterns:
            if pattern in command:
                print(f"🚫 Blocked dangerous command: {command}")
                return False
    
    # 敏感文件保护
    if tool_name in ("Edit", "Write"):
        file_path = tool_input.get("file_path", "")
        protected_paths = [".env", "secrets", "credentials", "id_rsa"]
        for protected in protected_paths:
            if protected in file_path:
                print(f"🚫 Protected file: {file_path}")
                return False
    
    # 其他操作允许
    return True


options = ClaudeAgentOptions(
    permission_mode="default",
    permission_callback=approval_callback,
)
```

---

## 六、上下文管理与自动压缩

### 6.1 上下文窗口消耗

上下文窗口是 Claude 在会话期间可用的信息总量。它在回合之间**不重置**，而是累积增长：

| 来源 | 加载时间 | 影响 |
|:-----|:---------|:-----|
| 系统提示 | 每个请求 | 小的固定成本，始终存在 |
| CLAUDE.md | 会话开始 | 每个请求完整发送（但缓存后只有首次付全费） |
| 工具定义 | 每个请求 | 每个工具增加 schema 描述 |
| 对话历史 | 累积 | **随每个回合增长** |
| 技能描述 | 会话开始 | 简短摘要 |

### 6.2 自动压缩（Compaction）

当上下文窗口接近限制时，SDK **自动压缩**对话：

```
长对话积累 → 接近上下文限制 → 触发压缩 → 
总结旧历史 → 保留最近交换和关键决策 → 继续工作
```

SDK 会生成 `SystemMessage`（subtype: `"compact_boundary"`）通知你压缩已发生。

### 6.3 保持上下文高效的策略

```python
# 策略 1：为子任务使用子智能体
# 每个子智能体从新对话开始，只有最终结果返回给父智能体
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Glob", "Grep", "Bash", "Agent"],
)

# 策略 2：有选择地为子智能体配置工具
# 子智能体只需要完成子任务所需的最小工具集
# 减少工具定义对上下文的消耗

# 策略 3：使用 ToolSearch 替代预加载所有 MCP 工具
# 避免几十个工具定义一次性占用上下文

# 策略 4：对常规任务使用较低的 effort 级别
options = ClaudeAgentOptions(
    effort="low",  # 快速响应，减少 token 消耗
)
```

### 6.4 Effort 级别

| 级别 | 推理深度 | 适用场景 |
|:-----|:---------|:---------|
| `"low"` | 最小推理 | 文件查找、列出目录、简单编辑 |
| `"medium"` | 平衡 | 常规编辑、标准任务 |
| `"high"` | 深入分析 | 重构、调试、代码审查 |
| `"max"` | 最大推理 | 多步骤复杂问题、架构设计 |

---

## 七、MCP 服务器连接

Agent SDK 支持连接 MCP（Model Context Protocol）服务器，将外部数据源和服务暴露给 Agent：

### 7.1 配置 MCP 服务器

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Glob", "Grep", "Bash", "ToolSearch"],
    mcp_servers=[
        {
            "name": "database",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres", 
                     "postgresql://localhost:5432/mydb"],
        },
        {
            "name": "github",
            "command": "npx", 
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": "ghp_xxx"},
        },
        {
            "name": "slack",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-slack"],
            "env": {"SLACK_BOT_TOKEN": "xoxb-xxx"},
        },
    ],
)
```

### 7.2 MCP 工具与上下文成本

每个 MCP 服务器暴露的工具都会增加上下文消耗。当连接多个服务器时：

```python
# ❌ 不推荐：预加载所有工具
options = ClaudeAgentOptions(
    allowed_tools=[
        "Read", "Edit", "Bash",
        # 加上 3 个 MCP 服务器的 30+ 工具 = 大量上下文消耗
    ],
)

# ✅ 推荐：使用 ToolSearch 按需加载
options = ClaudeAgentOptions(
    allowed_tools=[
        "Read", "Edit", "Bash",
        "ToolSearch",  # Claude 需要时自动搜索可用工具
    ],
)
```

---

## 八、子智能体与多 Agent 编排

### 8.1 子智能体工作原理

```
主 Agent（协调者）
  ├── 子 Agent A（分析文件）── 独立上下文，完成后返回摘要
  ├── 子 Agent B（修复 Bug）── 独立上下文，完成后返回结果  
  └── 子 Agent C（写测试）── 独立上下文，完成后返回结果
```

**关键优势**：每个子智能体有独立的上下文窗口，只有最终结果传回父智能体，大幅节省主上下文。

### 8.2 使用子智能体

Agent SDK 内置 `Agent` 工具，Claude 可以自动决定何时生成子智能体：

```python
options = ClaudeAgentOptions(
    allowed_tools=[
        "Read", "Edit", "Write", "Glob", "Grep", "Bash",
        "Agent",  # 启用子智能体能力
    ],
    system_prompt=(
        "You are a tech lead managing a codebase. "
        "For complex tasks, spawn sub-agents to handle subtasks in parallel. "
        "For example, one agent for analysis, one for implementation, one for testing."
    ),
)
```

### 8.3 编排模式

| 模式 | 描述 | 适用场景 |
|:-----|:-----|:---------|
| **串行编排** | 主 Agent 按顺序调用子 Agent | 有依赖关系的任务 |
| **并行编排** | 主 Agent 同时调用多个子 Agent | 独立子任务 |
| **层级编排** | 子 Agent 可以再调用子 Agent | 超大规模复杂任务 |
| **专家编排** | 不同子 Agent 有不同的工具集和系统提示 | 多领域协作 |

### 8.4 实战：多 Agent 代码重构

```python
async def refactor_with_agents():
    """使用多 Agent 进行大规模代码重构"""
    
    async for message in query(
        prompt=(
            "Refactor the authentication module:\n"
            "1. Spawn a sub-agent to analyze the current auth code structure\n"
            "2. Spawn a sub-agent to implement the new auth service with OAuth2\n"
            "3. Spawn a sub-agent to write comprehensive tests\n"
            "4. Review all changes and ensure consistency"
        ),
        options=ClaudeAgentOptions(
            allowed_tools=[
                "Read", "Edit", "Write", "Glob", "Grep", "Bash",
                "Agent",  # 启用子智能体
            ],
            permission_mode="acceptEdits",
            max_turns=100,    # 多 Agent 需要更多回合
            max_budget_usd=5.0,
            effort="high",
        ),
    ):
        if isinstance(message, ResultMessage):
            print(f"Refactoring {'succeeded' if message.subtype == 'success' else 'failed'}")
            print(f"Total cost: ${message.total_cost_usd:.4f}")
```

---

## 九、Hooks 钩子集成

Hooks 是在 Agent Loop 特定节点触发的回调，运行在你的进程中，**不消耗上下文**。

### 9.1 可用 Hooks

| Hook | 触发时机 | 常见用途 |
|:-----|:---------|:---------|
| `PreToolUse` | 工具执行前 | 验证输入，阻止危险命令 |
| `PostToolUse` | 工具执行后 | 审计输出，触发副作用 |
| `UserPromptSubmit` | 发送提示时 | 注入额外上下文 |
| `Stop` | Agent 完成时 | 验证结果，保存会话状态 |
| `PreCompact` | 上下文压缩前 | 存档完整记录 |

### 9.2 在 SDK 中使用 Hooks

```python
async def pre_tool_use_hook(tool_name: str, tool_input: dict) -> dict:
    """工具执行前的安全检查"""
    
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        # 记录所有 Bash 命令到审计日志
        with open("audit.log", "a") as f:
            f.write(f"[{datetime.now()}] Bash: {command}\n")
        
        # 阻止 rm -rf
        if "rm -rf" in command:
            return {
                "decision": "deny",
                "reason": "rm -rf is blocked by security policy"
            }
    
    return {"decision": "allow"}


async def stop_hook(result: str) -> dict:
    """Agent 完成时验证结果"""
    
    # 运行测试确认修改没有破坏什么
    import subprocess
    test_result = subprocess.run(
        ["python", "-m", "pytest", "--tb=short"],
        capture_output=True, text=True
    )
    
    if test_result.returncode != 0:
        return {
            "decision": "continue",
            "reason": f"Tests failed:\n{test_result.stdout}\nPlease fix the failing tests."
        }
    
    return {"decision": "stop"}
```

---

## 十、会话管理与恢复

### 10.1 保存会话

```python
session_id = None

async for message in query(prompt="...", options=options):
    if isinstance(message, ResultMessage):
        session_id = message.session_id
        # 保存 session_id 以便后续恢复
        save_session_id(session_id)
```

### 10.2 恢复会话

```python
# 从上次中断的地方继续
saved_session_id = load_session_id()

async for message in query(
    prompt="Continue where you left off and complete the remaining tasks.",
    options=ClaudeAgentOptions(
        session_id=saved_session_id,  # 恢复之前的会话
        allowed_tools=["Read", "Edit", "Glob", "Grep", "Bash"],
    ),
):
    # 处理消息...
    pass
```

### 10.3 会话超限恢复

```python
async for message in query(prompt="...", options=options):
    if isinstance(message, ResultMessage):
        if message.subtype == "error_max_turns":
            print(f"Hit turn limit. Resuming session {message.session_id}...")
            # 自动恢复，继续完成
            async for msg in query(
                prompt="Continue and complete the remaining work.",
                options=ClaudeAgentOptions(
                    session_id=message.session_id,
                    max_turns=30,  # 再给 30 个回合
                ),
            ):
                pass
```

---

## 十一、结构化输出

Agent SDK 支持要求 Agent 返回符合特定 JSON Schema 的结构化输出：

```python
from pydantic import BaseModel
from typing import List


class BugReport(BaseModel):
    file_path: str
    line_number: int
    severity: str  # "critical" | "major" | "minor"
    description: str
    suggested_fix: str


class AuditResult(BaseModel):
    total_files_analyzed: int
    bugs_found: List[BugReport]
    overall_score: float  # 0-100
    summary: str


async for message in query(
    prompt="Audit all Python files in src/ for bugs and security issues.",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep"],
        permission_mode="bypassPermissions",
        output_schema=AuditResult,  # 要求输出匹配此 schema
    ),
):
    if isinstance(message, ResultMessage):
        # result 会是 AuditResult 的 JSON
        audit = AuditResult.model_validate_json(message.result)
        print(f"Score: {audit.overall_score}")
        for bug in audit.bugs_found:
            print(f"  [{bug.severity}] {bug.file_path}:{bug.line_number} - {bug.description}")
```

---

## 十二、生产部署最佳实践

### 12.1 安全检查清单

```
✅ 最小工具集：只授权 Agent 真正需要的工具
✅ 禁用危险工具：生产环境中禁止 Bash 或严格限制
✅ 设置 max_turns：防止无限循环
✅ 设置 max_budget_usd：防止成本爆炸
✅ 使用 PreToolUse Hook：审计和阻止危险操作
✅ 使用 Stop Hook：验证 Agent 输出质量
✅ 保护敏感文件：.env、credentials 等
✅ 日志审计：记录所有工具调用和结果
✅ 沙盒化：在容器中运行 Agent，限制文件系统访问
✅ 超时机制：为整个 Agent 运行设置外部超时
```

### 12.2 错误处理模式

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def resilient_agent(prompt: str, max_retries: int = 3):
    """带重试和错误恢复的生产级 Agent"""
    
    session_id = None
    
    for attempt in range(max_retries):
        try:
            async for message in query(
                prompt=prompt if session_id is None else "Continue and complete the task.",
                options=ClaudeAgentOptions(
                    session_id=session_id,
                    allowed_tools=["Read", "Edit", "Glob", "Grep"],
                    permission_mode="acceptEdits",
                    max_turns=30,
                    max_budget_usd=2.0,
                ),
            ):
                if isinstance(message, ResultMessage):
                    session_id = message.session_id
                    
                    if message.subtype == "success":
                        return message.result
                    elif message.subtype in ("error_max_turns", "error_max_budget_usd"):
                        print(f"Limit reached ({message.subtype}), attempt {attempt + 1}")
                        continue  # 重试，恢复会话
                    else:
                        print(f"Error: {message.subtype}")
                        break
        
        except Exception as e:
            print(f"Exception on attempt {attempt + 1}: {e}")
            await asyncio.sleep(2 ** attempt)  # 指数退避
    
    raise RuntimeError(f"Agent failed after {max_retries} attempts")
```

### 12.3 品牌限制

⚠️ **重要**：使用 Agent SDK 构建的应用**不能使用 "Claude Code" 品牌**。你可以说"Powered by Claude"，但不能说"使用 Claude Code 构建"。

---

## 十三、Agent SDK vs 其他方案对比

| 对比项 | Agent SDK | Messages API + 手动编排 | Claude Code CLI | LangChain/LlamaIndex |
|:------|:---------|:---------------------|:---------------|:-------------------|
| 定位 | 官方 Agent 框架 | 基础 API | 交互式编码工具 | 通用 Agent 框架 |
| 内置工具 | ✅ 文件/搜索/Bash/Web | ❌ 需自己实现 | ✅ 同左 | 🟡 需安装插件 |
| Agent Loop | ✅ 内置 | ❌ 需自己写 | ✅ 内置 | 🟡 不同实现 |
| 上下文管理 | ✅ 自动压缩 | ❌ 手动管理 | ✅ 自动 | 🟡 各有方案 |
| 权限控制 | ✅ 细粒度 | ❌ 自己实现 | ✅ 交互确认 | 🟡 各有方案 |
| 多模型支持 | ❌ 仅 Claude | ✅ 仅 Claude | ❌ 仅 Claude | ✅ 多模型 |
| 适合场景 | 自动化管道/产品集成 | 最大灵活性 | 个人开发 | 需要多模型 |

---

## 练习题

### 基础练习

1. **搭建只读审查 Agent**：创建一个 Agent，只使用 Read/Glob/Grep 工具，审查一个 Python 项目的代码质量，输出结构化报告。

2. **成本感知 Agent**：创建一个 Agent，设置 `max_budget_usd=0.5`，观察它在接近预算限制时的行为。

### 中级练习

3. **安全审批系统**：实现一个自定义 `permission_callback`，当 Agent 尝试修改 `*.config` 或 `*.env` 文件时弹出确认，记录所有 Bash 命令到审计日志。

4. **会话恢复**：创建一个大型重构 Agent（`max_turns=10`），让它在达到限制时保存 session_id，然后恢复会话继续完成。

### 高级练习

5. **多 Agent 编排**：构建一个"代码审查团队"：
   - 子 Agent A：负责安全审查
   - 子 Agent B：负责性能分析
   - 子 Agent C：负责代码风格检查
   - 主 Agent：汇总三个子 Agent 的报告

6. **MCP 集成**：连接一个 MCP 数据库服务器（PostgreSQL），创建一个 Agent 可以查询数据库、分析结果并生成报告。

---

> **下一步**：[10_Claude_Code高级特性.md](10_Claude_Code高级特性.md) — CLAUDE.md 配置 + Hooks + CI/CD
