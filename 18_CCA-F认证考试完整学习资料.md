# CCA-F 认证考试完整学习资料

> **Claude Certified Architect – Foundations**  
> **整理日期**：2026年3月23日  
> **考试形式**：60 道单选题（4选1），及格分 720/1000  
> **核心原则**：每个知识点都标注了考试指南中的对应任务编号，方便精准复习

---

## 目录

- [领域 1：智能体架构与编排（27%）](#领域-1智能体架构与编排27)
- [领域 2：工具设计与 MCP 集成（18%）](#领域-2工具设计与-mcp-集成18)
- [领域 3：Claude Code 配置与工作流（20%）](#领域-3claude-code-配置与工作流20)
- [领域 4：提示工程与结构化输出（20%）](#领域-4提示工程与结构化输出20)
- [领域 5：上下文管理与可靠性（15%）](#领域-5上下文管理与可靠性15)
- [附录 A：技术速查表](#附录-a技术速查表)
- [附录 B：样题解题策略](#附录-b样题解题策略)
- [附录 C：考试范围内外速查](#附录-c考试范围内外速查)
- [附录 E：练习参考实现](#附录-e练习参考实现)
- [附录 F：学习资源清单](#附录-f学习资源清单)

---

# 领域 1：智能体架构与编排（27%）

> **这是考试权重最高的领域。** 核心考察使用 Claude Agent SDK 构建和编排智能体系统的能力。
>
> **官方学习资源**：
> - [Agent SDK 文档](https://platform.claude.com/docs/en/agent-sdk/overview)
> - [Introduction to subagents 课程](https://anthropic.skilljar.com/introduction-to-subagents)（20min）
> - [Introduction to agent skills 课程](https://anthropic.skilljar.com/introduction-to-agent-skills)（30min）
> - [Building agents with Agent SDK 博客](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)

---

## 1.1 智能体循环（Agent Loop）⟵ 任务 1.1

### 核心概念

智能体循环是 Agent SDK 的核心执行机制，遵循以下周期：

```
收集上下文 → 采取行动 → 验证工作 → 循环
```

**详细流程**：

```
1. 接收提示
   → Claude 收到你的提示、系统提示、工具定义和对话历史
   → SDK 生成 SystemMessage（子类型 "init"）

2. 评估并响应
   → Claude 评估当前状态，决定：
     a) 纯文本响应
     b) 请求工具调用
     c) 两者兼有
   → SDK 生成 AssistantMessage

3. 执行工具
   → SDK 运行每个请求的工具并收集结果
   → 工具结果反馈给 Claude 进行下一步决策
   → 可用钩子（Hooks）在工具运行前拦截/修改/阻止

4. 重复（步骤 2-3 构成一个"回合" Turn）
   → 循环持续直到 Claude 生成不含工具调用的响应

5. 返回结果
   → SDK 生成最终 AssistantMessage（纯文本）
   → 随后生成 ResultMessage（含文本、Token 用量、成本、会话 ID）
```

### stop_reason 处理 ⭐ 高频考点

| stop_reason 值 | 含义 | 处理方式 |
|:---|:---|:---|
| `end_turn` | 模型正常完成 | 循环终止，返回结果 |
| `tool_use` | 模型请求调用工具 | 执行工具，结果送回，继续循环 |
| `max_tokens` | 达到输出 Token 限制 | 循环终止，检查是否需要续写 |
| `stop_sequence` | 遇到自定义停止序列 | 循环终止，检查匹配的停止序列 |
| `refusal` | 模型拒绝请求 | 检测并处理拒绝原因 |
| `pause_turn` | 服务器工具循环达迭代上限（默认 10 次） | 可通过继续请求恢复，或终止 |

> **考试重点**：考试指南附录主要关注 `"end_turn"` 和 `"tool_use"` 两个值，但了解 `stop_sequence` 和 `pause_turn` 的存在有助于全面理解 API 行为。

**控制流实现**：

```python
# 正确的智能体循环控制流
while True:
    response = client.messages.create(
        model="claude-opus-4-6",
        messages=messages,
        tools=tools
    )
    
    # ✅ 检查 stop_reason 决定是否继续
    if response.stop_reason == "end_turn":
        break  # 模型完成，退出循环
    elif response.stop_reason == "tool_use":
        # 执行工具调用
        tool_results = execute_tools(response.content)
        # 将工具结果添加到对话上下文
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
    # 继续循环
```

### ⚠️ 必须避免的反模式

1. **❌ 解析自然语言信号确定循环终止**（如检查"我完成了"）
2. **❌ 任意迭代上限作为主要停止机制**（如最多循环 10 次）
3. **❌ 检查助手文本内容作为完成指示器**

**正确方式**：始终使用 `stop_reason` 字段驱动循环控制。

### 工具并发规则

| 工具类型 | 执行方式 | 示例 |
|:---|:---|:---|
| 只读工具 | 可并发运行 | Read, Glob, Grep, 标记只读的 MCP 工具 |
| 修改状态的工具 | 顺序运行 | Edit, Write, Bash |
| 自定义工具 | 默认顺序，标记只读可并发 | |

---

## 1.2 协调器-子智能体编排 ⟵ 任务 1.2

### 核心架构：中心辐射模式（Hub-and-Spoke）

```
          ┌──────────────┐
          │   协调器       │
          │ (Coordinator) │
          └──────┬───────┘
         ┌───────┼───────┐
         ▼       ▼       ▼
    ┌────────┐┌────────┐┌────────┐
    │ 子智能体 ││ 子智能体 ││ 子智能体 │
    │  搜索   ││  分析   ││  综合   │
    └────────┘└────────┘└────────┘
```

### 关键规则

1. **协调器管理所有通信** — 子智能体之间不直接通信，所有信息通过协调器路由
2. **子智能体隔离运行** — 不自动继承协调器对话历史
3. **上下文必须显式传递** — 子智能体不共享内存，需要的信息必须在创建时提供

### 协调器的四大职责

| 职责 | 说明 |
|:---|:---|
| **任务分解** | 将复杂任务拆分为子任务（注意避免过于狭窄） |
| **委托** | 选择合适的子智能体执行子任务 |
| **结果聚合** | 汇总子智能体结果 |
| **智能体选择** | 根据查询复杂性动态选择子智能体（不是总走完整流水线） |

### ⭐ 常见考点：过窄的任务分解

> **场景**（样题 7）：研究"AI 对创意产业的影响"，但最终报告仅涵盖视觉艺术。
> **根因**：协调器将"创意产业"仅分解为视觉艺术子类（数字艺术、平面设计、摄影），遗漏了音乐、写作、电影。
> **教训**：任务分解过于狭窄会导致覆盖不完整。

### 迭代细化循环

```
1. 协调器发起初始分解和委托
2. 评估综合输出的差距
3. 使用针对性查询重新委托
4. 循环直到覆盖充分
```

---

## 1.3 子智能体配置与上下文传递 ⟵ 任务 1.3

### Task 工具：生成子智能体的机制

```python
# Agent SDK 中的子智能体配置
agent_definition = AgentDefinition(
    description="专门搜索网络信息的子智能体",
    system_prompt="你是一个网络搜索专家...",
    allowed_tools=["WebSearch", "WebFetch", "Task"]  # ⚠️ 必须包含 "Task" 才能生成子智能体
)
```

**关键配置项**：

| 配置项 | 说明 |
|:---|:---|
| `description` | 子智能体描述 |
| `system_prompt` | 子智能体的系统提示 |
| `allowed_tools` | 工具限制列表（**必须包含 "Task" 才能嵌套子智能体**） |

### 上下文传递最佳实践

1. **在子智能体提示中直接包含先前智能体的完整发现**（不要假设子智能体知道上下文）
2. **使用结构化数据格式分离内容与元数据**：

```json
{
  "content": "AI 在视觉艺术中的应用...",
  "metadata": {
    "source_url": "https://example.com/article",
    "document_name": "AI Art Report 2025",
    "page_number": 12
  }
}
```

3. **设计目标导向的协调器提示**（指定研究目标和质量标准，而非逐步程序指令）

### 并行子智能体生成

在单个协调器响应中发出多个 Task 工具调用 → 并行执行子智能体：

```python
# 协调器一次性发出多个 Task 调用
# → SDK 并行执行这些子智能体
tasks = [
    Task(prompt="搜索音乐领域的 AI 影响", agent=search_agent),
    Task(prompt="搜索写作领域的 AI 影响", agent=search_agent),
    Task(prompt="搜索电影领域的 AI 影响", agent=search_agent),
]
```

### 基于分支的会话管理

- **fork_session**：从共享分析基线创建独立分支
- 用于探索不同方法时保持共享基础

---

## 1.4 强制模式与交接协议 ⟵ 任务 1.4

### 程序化强制 vs 提示引导 ⭐ 核心考点

| 方式 | 可靠性 | 适用场景 |
|:---|:---|:---|
| **程序化强制**（钩子、前置条件门） | ✅ 确定性保证 | 业务规则必须遵守时 |
| **提示引导**（系统提示指令） | ⚠️ 概率性合规（非零失败率） | 软性偏好 |

**考试场景**（样题 1）：
> 智能体跳过 `get_customer` 直接调用 `lookup_order`，导致错误退款。
> **正确答案**：程序化前置条件（阻止 `process_refund` 直到 `get_customer` 返回验证的客户 ID）
> **错误选项**：增强系统提示 / 添加少样本示例 → 概率性合规，有财务风险

### 结构化交接协议

中途升级给人工时的交接摘要：

```json
{
  "customer_id": "CUST-12345",
  "root_cause": "账单争议 - 重复扣款",
  "refund_amount": 49.99,
  "recommended_action": "全额退款",
  "investigation_summary": "确认两笔相同金额的交易..."
}
```

---

## 1.5 钩子（Hooks）⟵ 任务 1.5

> ⚠️ **重要区分**：考试中涉及的"钩子"存在两个不同层面，务必区分：
> - **Claude Code Hooks**：通过 JSON 配置文件（`settings.json`）定义，运行在 Claude Code CLI 环境
> - **Agent SDK Hooks**：通过 Python/TypeScript 代码定义，运行在自定义 Agent 应用中

### 一、Claude Code Hooks（JSON 配置方式）

**配置位置**：

| 配置文件 | 作用范围 | 可共享 |
|:---|:---|:---|
| `~/.claude/settings.json` | 所有项目（用户级） | 否 |
| `.claude/settings.json` | 当前项目 | 是（可提交到仓库） |
| `.claude/settings.local.json` | 当前项目 | 否（已 gitignore） |
| 管理策略设置 | 全组织 | 是（管理员控制） |

**配置格式**：三级嵌套 — Hook Event → Matcher Group → Hook Handler

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

**处理器类型（Handler Types）**：

| 类型 | 说明 | 示例场景 |
|:---|:---|:---|
| `command` | 运行 shell 命令 | 执行安全检查脚本 |
| `http` | 向 URL 发送 POST | 调用外部审计服务 |
| `prompt` | 发送 Prompt 给 Claude 评估 | LLM 辅助决策 |
| `agent` | 生成子代理执行验证 | 运行测试套件 |

**完整钩子事件列表** ⭐：

| 事件 | 触发时机 | 支持的处理器类型 |
|:---|:---|:---|
| `PreToolUse` | 工具执行前（可拦截） | command, http, prompt, agent |
| `PostToolUse` | 工具成功后 | command, http, prompt, agent |
| `PostToolUseFailure` | 工具失败后 | command, http, prompt, agent |
| `PermissionRequest` | 权限对话框出现时 | command, http, prompt, agent |
| `UserPromptSubmit` | 用户提交 Prompt 前 | command, http, prompt, agent |
| `Stop` | Claude 完成响应时 | command, http, prompt, agent |
| `StopFailure` | API 错误导致响应结束 | command |
| `SubagentStart` | 子代理生成时 | command |
| `SubagentStop` | 子代理结束时 | command, http, prompt, agent |
| `SessionStart` | 会话开始/恢复 | command |
| `SessionEnd` | 会话终止 | command |
| `PreCompact` | 上下文压缩前 | command |
| `PostCompact` | 上下文压缩后 | command |
| `Notification` | 发送通知时 | command |
| `TaskCompleted` | 任务标记完成 | command, http, prompt, agent |
| `ConfigChange` | 配置文件更改 | command |

**Matcher 语法**：正则表达式过滤触发条件

```json
"matcher": "Bash"              // 仅匹配 Bash 工具
"matcher": "Edit|Write"        // 匹配 Edit 或 Write 工具
"matcher": "mcp__.*"           // 匹配所有 MCP 工具
```

**输出控制**：

- Exit 0 → 成功，解析 stdout JSON
- Exit 2 → 阻塞错误，反馈给 Claude（如 PreToolUse 会阻止工具调用）
- 其他非 0 → 非阻塞错误

### 二、Agent SDK Hooks（代码方式）

在自定义 Agent 应用中，通过 Python/TypeScript 代码注册钩子函数：

```python
# Agent SDK 中的 PostToolUse 钩子：数据规范化
def post_tool_use_hook(tool_name, tool_result):
    if tool_name == "get_customer":
        # 将 Unix 时间戳转换为 ISO 8601
        if "created_at" in tool_result:
            tool_result["created_at"] = unix_to_iso(tool_result["created_at"])
        # 将数字状态码转换为可读字符串
        if "status" in tool_result:
            tool_result["status"] = STATUS_MAP.get(tool_result["status"], "unknown")
    return tool_result
```

```python
# Agent SDK 中的 PreToolUse 钩子：阻止未验证身份就退款
def pre_tool_use_hook(tool_name, tool_input, context):
    if tool_name == "process_refund":
        if not context.get("customer_verified"):
            return {"blocked": True, "reason": "必须先验证客户身份"}
    return {"blocked": False}
```

### 三、两者对比 ⭐ 考试重点

| 维度 | Claude Code Hooks | Agent SDK Hooks |
|:---|:---|:---|
| **运行环境** | Claude Code CLI | 自定义 Agent 应用 |
| **配置方式** | JSON 文件（`settings.json`） | Python/TypeScript 代码 |
| **钩子事件数量** | 20+ 种（含 Session、Config 等 CLI 特有事件） | 核心 6 种（PreToolUse、PostToolUse 等） |
| **处理器类型** | command/http/prompt/agent 四种 | 代码函数 |
| **Matcher** | 正则表达式 | 代码逻辑判断 |
| **共享方式** | `.claude/settings.json` 提交仓库 | 随应用代码一起 |

### 四、决策原则

**业务规则需要保证合规时 → 用钩子（确定性）**  
**软性偏好和风格指导 → 用提示指令（概率性）**

---

## 1.6 任务分解策略 ⟵ 任务 1.6

### 两种分解模式

| 模式 | 适用场景 | 特点 |
|:---|:---|:---|
| **提示链（固定顺序流水线）** | 可预测的审查/分析 | 顺序步骤，每步专注 |
| **动态自适应分解** | 开放式调查/研究 | 先映射 → 识别重点 → 自适应计划 |

### 提示链示例：代码审查

```
步骤 1: 按文件逐个分析本地问题（语法、逻辑、安全）
步骤 2: 跨文件集成遍历（数据流、接口一致性）
步骤 3: 汇总发现并排序优先级
```

### 动态分解示例：开放式调查

```
1. 映射结构 — 理解代码库整体架构
2. 识别高影响区域 — 聚焦关键模块
3. 创建自适应优先计划 — 根据发现调整后续调查方向
```

---

## 1.7 会话状态管理 ⟵ 任务 1.7

### 关键命令

| 命令/功能 | 用途 |
|:---|:---|
| `--resume <session-name>` | 恢复命名会话 |
| `fork_session` | 从共享基线创建独立分支 |
| `/compact` | 压缩上下文，减少 Token 使用 |
| `/memory` | 查看加载的记忆文件 |

### 恢复 vs 新会话的选择

| 场景 | 选择 | 原因 |
|:---|:---|:---|
| 继续之前的调查 | `--resume` | 保留完整上下文 |
| 工具结果已过时 | 新会话 + 摘要注入 | 避免基于过时数据推理 |
| 文件已更改 | `--resume` + 告知变更 | 触发针对性重新分析 |

---

# 领域 2：工具设计与 MCP 集成（18%）

> **官方学习资源**：
> - [Introduction to MCP 课程](https://anthropic.skilljar.com/introduction-to-model-context-protocol)（1h）
> - [MCP: Advanced Topics 课程](https://anthropic.skilljar.com/model-context-protocol-advanced-topics)（1.1h）
> - [MCP 官方规范](https://modelcontextprotocol.io/)
> - [Tool Use 文档](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)

---

## 2.1 工具接口设计 ⟵ 任务 2.1

### ⭐ 核心原则：工具描述是 LLM 工具选择的主要机制

**坏的描述 → 不可靠的工具选择：**

```json
// ❌ 过于简约的描述
{
  "name": "get_customer",
  "description": "检索客户信息"
}

// ❌ 与上面重叠的描述
{
  "name": "lookup_order",
  "description": "检索订单详情"
}
```

**好的描述 → 可靠的工具选择：**

```json
// ✅ 详细的描述，包含输入格式、示例、边界
{
  "name": "get_customer",
  "description": "根据客户 ID、邮箱或电话号码检索客户账户信息。返回姓名、联系方式、账户状态和历史。输入示例：'CUST-12345'、'user@email.com'。不返回订单数据——订单查询请使用 lookup_order。",
  "input_schema": {
    "type": "object",
    "properties": {
      "identifier": {
        "type": "string",
        "description": "客户 ID（CUST-XXXXX）、邮箱或电话号码"
      }
    }
  }
}
```

### 工具设计清单

- [ ] 工具描述清楚区分**用途、输入、输出和使用场景**
- [ ] 重命名工具消除功能重叠
- [ ] 拆分通用工具为目的特定工具
- [ ] 审查系统提示中可能覆盖工具描述的关键词敏感指令

---

## 2.2 MCP 错误响应 ⟵ 任务 2.2

### isError 标志模式

```json
// MCP 工具返回的结构化错误响应
{
  "content": [
    {
      "type": "text",
      "text": "{\"errorCategory\": \"transient\", \"isRetryable\": true, \"message\": \"数据库连接超时\"}"
    }
  ],
  "isError": true
}
```

### 错误分类 ⭐

| 错误类型 | isRetryable | 处理方式 |
|:---|:---|:---|
| **瞬态错误**（超时、网络波动） | `true` | 子智能体本地重试 |
| **验证错误**（参数无效） | `false` | 返回修正建议 |
| **业务规则违反** | `false` | 返回客户友好解释 |
| **权限错误** | `false` | 传播给协调器 |

### 关键区分 ⭐

**访问失败 ≠ 有效空结果**：
- 访问失败 → "数据库不可达" → 应重试或升级
- 有效空结果 → "该客户无订单" → 正常结果，继续处理

---

## 2.3 工具分配与 tool_choice ⟵ 任务 2.3

### 过多工具的问题

> 18 个工具 → 选择可靠性差  
> 4-5 个工具 → 选择可靠性高

### 工具分配原则

1. **限制子智能体工具集到其角色相关范围**
2. **用受限替代方案替换通用工具**（如用 `verify_fact` 替代完整的 `web_search`）
3. **为高频需求提供范围化跨角色工具**

### tool_choice 选项 ⭐

| 值 | 行为 | 适用场景 |
|:---|:---|:---|
| `"auto"` | 模型自动决定是否使用工具 | 默认行为 |
| `"any"` | 强制使用工具（从可用工具中选） | 保证结构化输出 |
| `"none"` | 不使用任何工具 | 纯文本回答（仍消耗工具定义 Token） |
| `{"type": "tool", "name": "xxx"}` | 强制使用特定工具 | 确保提取在富化前运行 |

> **注意**：即使设置 `tool_choice: "none"`，只要上下文中定义了 `tools`，仍会产生工具系统提示的 Token 消耗（如 Opus 4.6 为 346 tokens）。

### disable_parallel_tool_use 参数 ⭐ 补充

```python
# 禁止并行工具调用（强制串行执行）
response = client.messages.create(
    model="claude-opus-4-6",
    messages=[...],
    tools=[...],
    tool_choice={"type": "auto", "disable_parallel_tool_use": True}
    # 也可搭配 "any" 或指定工具使用
)
```

| 场景 | 是否禁用并行 |
|:---|:---|
| 工具间有依赖（B 的输入依赖 A 的输出） | ✅ 禁用 |
| 独立只读查询 | ❌ 保持并行（提高效率） |
| 状态修改操作需要严格顺序 | ✅ 禁用 |

> **考试提示**：考试指南没有直接提到此参数，但理解"只读工具可并发、修改状态工具需串行"的原则是核心考点。

**考试场景**（样题 9）：综合智能体验证声明需 2-3 往返。
**正确答案**：给综合智能体范围化 `verify_fact` 工具（最小权限原则），复杂验证走协调器。

---

## 2.4 MCP 服务器集成 ⟵ 任务 2.4

### MCP 三大原语

| 原语 | 说明 | 示例 |
|:---|:---|:---|
| **Tools（工具）** | 可执行的操作 | `search_web`, `query_database` |
| **Resources（资源）** | 可读取的数据 | 文件目录、数据库表结构 |
| **Prompts（提示）** | 预定义的提示模板 | 代码审查提示、翻译提示 |

### MCP 服务器配置范围 ⭐

| 范围 | 配置文件 | 特点 |
|:---|:---|:---|
| **项目级** | `.mcp.json` | 版本控制共享，团队可用 |
| **用户级** | `~/.claude.json` | 个人使用，跨项目 |

```json
// .mcp.json 示例
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"  // ⭐ 环境变量展开
      }
    }
  }
}
```

### 关键考点

- **所有已配置 MCP 服务器的工具同时可用**（注意工具数量控制）
- **MCP 资源暴露内容目录**以减少探索性工具调用
- **增强 MCP 工具描述**防止偏好内置工具

---

## 2.5 内置工具 ⟵ 任务 2.5

### 内置工具速查 ⭐

| 工具 | 用途 | 适用场景 |
|:---|:---|:---|
| **Grep** | 内容搜索（正则） | 搜索代码内容、查找字符串 |
| **Glob** | 文件路径模式匹配 | 查找匹配的文件路径 |
| **Read** | 读取完整文件 | 获取文件内容 |
| **Write** | 写入完整文件 | 创建新文件 |
| **Edit** | 有针对性修改 | 修改文件特定部分 |
| **Bash** | 运行 Shell 命令 | Git 操作、脚本执行 |
| **WebSearch** | 搜索网络 | 获取最新信息 |
| **WebFetch** | 获取解析页面 | 读取网页内容 |
| **Agent** | 生成子智能体 | 委托子任务 |

### 关键用法区分

- **Grep** 搜索代码内容 vs **Glob** 查找文件路径
- **Edit** 有针对性修改 vs **Read + Write** 后备方案（Edit 非唯一文本匹配失败时）
- **增量理解代码库**：Grep 找入口点 → Read 跟踪导入 → 追踪跨包装模块

---

# 领域 3：Claude Code 配置与工作流（20%）

> **官方学习资源**：
> - [Claude Code in Action 课程](https://anthropic.skilljar.com/claude-code-in-action)（1h）
> - [Claude Code 文档](https://code.claude.com/docs/en/overview)
> - [Memory 配置](https://code.claude.com/docs/en/memory)
> - [Hooks 参考](https://code.claude.com/docs/en/hooks)

---

## 3.1 CLAUDE.md 配置层级 ⟵ 任务 3.1

### 三级配置体系 ⭐⭐⭐ 高频考点

| 层级 | 位置 | 共享方式 | 用途 |
|:---|:---|:---|:---|
| **项目级** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 版本控制（团队共享） | 项目架构、编码标准 |
| **用户级** | `~/.claude/CLAUDE.md` | 不共享（仅个人） | 个人偏好 |
| **组织级** | `/Library/Application Support/ClaudeCode/CLAUDE.md`（macOS） | 组织管理员 | 公司安全策略 |

### ⭐ 常见考试场景

> **问题**：新团队成员加入后，Claude 没有遵循团队的编码标准。
> **根因**：配置写在了用户级（`~/.claude/CLAUDE.md`），新成员没有这个文件。
> **修复**：将配置移到项目级（`.claude/CLAUDE.md`），通过版本控制共享。

### @import 语法

```markdown
# CLAUDE.md 中导入外部文件
参见 @README 获取项目概述
参考 @package.json 获取可用命令
导入 @docs/git-instructions.md

# 导入个人配置（不提交到仓库）
@~/.claude/my-project-instructions.md
```

**限制**：最多 5 层递归导入。

### .claude/rules/ 模块化组织 ⭐

```
your-project/
├── .claude/
│   ├── CLAUDE.md              # 主项目指令
│   └── rules/
│       ├── code-style.md      # 代码风格
│       ├── testing.md         # 测试约定
│       └── security.md        # 安全要求
```

**路径特定规则**（YAML frontmatter）：

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规则
- 所有端点必须包含输入验证
- 使用标准错误响应格式
```

### /memory 命令

用途：验证加载的记忆文件，诊断不一致行为。

---

## 3.2 自定义斜杠命令与技能 ⟵ 任务 3.2

### 命令范围

| 类型 | 位置 | 共享方式 |
|:---|:---|:---|
| **项目命令** | `.claude/commands/` | 版本控制共享 |
| **个人命令** | `~/.claude/commands/` | 仅个人使用 |

**考试场景**（样题 4）：
> 创建 /review 命令让团队克隆后自动可用 → **答案：`.claude/commands/`**

### SKILL.md 配置 ⭐

```markdown
---
context: fork         # 在隔离子智能体上下文中运行
allowed-tools:        # 限制技能可用的工具
  - Read
  - Grep
  - Glob
argument-hint: "文件路径"  # 提示所需参数
---

# 代码审查技能
审查指定文件的代码质量...
```

### 技能 vs CLAUDE.md 的选择 ⭐

| 特性 | 技能（Skills） | CLAUDE.md |
|:---|:---|:---|
| 加载方式 | 按需调用 | 始终加载 |
| 适用场景 | 特定任务工作流 | 通用标准和约定 |
| context: fork | ✅ 支持隔离运行 | ❌ 不支持 |
| 工具限制 | ✅ allowed-tools | ❌ 不支持 |

---

## 3.3 路径特定规则 ⟵ 任务 3.3

### glob 模式规则

```markdown
---
paths:
  - "terraform/**/*"          # 所有 Terraform 文件
  - "**/*.test.tsx"           # 所有测试文件
  - "src/components/*.tsx"     # 特定目录组件
---
```

### 选择路径规则 vs 子目录 CLAUDE.md ⭐

**考试场景**（样题 6）：
> 测试文件分散在代码库各处（Button.test.tsx 在 Button.tsx 旁边），想要统一约定。
> **正确答案**：`.claude/rules/` + glob 模式（`**/*.test.tsx`）
> **错误选项**：每个子目录放 CLAUDE.md → 无法处理分散文件

---

## 3.4 计划模式 vs 直接执行 ⟵ 任务 3.4

### 选择标准 ⭐

| 使用计划模式 | 使用直接执行 |
|:---|:---|
| 大规模更改（45+ 文件） | 简单、范围明确的更改 |
| 多种有效方法 | 已理解的更改 |
| 架构决策 | 单文件修复 |
| 多文件修改 | bug 修复 |
| 微服务重构 | 添加日志语句 |

**考试场景**（样题 5）：
> 单体应用重构为微服务 → **计划模式**（允许安全探索和设计，防止昂贵返工）

### Explore 子智能体

用途：隔离冗长发现输出，防止上下文窗口耗尽，仅返回摘要。

### 组合使用

**计划模式调查** + **直接执行实现** = 最佳实践

---

## 3.5 迭代细化技术 ⟵ 任务 3.5

### 四大细化技巧

| 技巧 | 说明 | 适用场景 |
|:---|:---|:---|
| **具体示例** | 提供 2-3 个输入/输出示例 | 传达预期转换 |
| **测试驱动** | 先编写测试，通过失败引导改进 | 明确验证标准 |
| **面试模式** | 让 Claude 提问发掘考虑因素 | 发现未预见的问题 |
| **交互 vs 顺序** | 交互问题单消息处理，独立问题顺序修复 | 效率最大化 |

---

## 3.6 CI/CD 集成 ⟵ 任务 3.6

### 关键 CLI 标志 ⭐

| 标志 | 用途 |
|:---|:---|
| `-p` / `--print` | **非交互模式**（CI/CD 必须） |
| `--output-format json` | 生成 JSON 格式输出 |
| `--json-schema` | 强制输出符合指定模式 |

**考试场景**（样题 10）：
> 流水线脚本 `claude "分析 PR..."` 无限期挂起 → **答案：加 `-p` 标志**

### CI/CD 最佳实践

```bash
# ✅ 正确：CI 中使用 -p 标志
claude -p "分析这个 PR 的安全问题" --output-format json

# ❌ 错误：没有 -p 标志，会等待交互输入而挂起
claude "分析这个 PR 的安全问题"
```

### 会话上下文隔离

**⚠️ 同一会话审查自己的更改效果差** → 用独立会话/实例进行审查

### CLAUDE.md 中记录 CI 上下文

```markdown
# CI/CD 标准
- 测试框架：Jest + React Testing Library
- Fixture 约定：__fixtures__/ 目录
- 审查标准：仅标记 bug 和安全问题，跳过风格问题
```

---

# 领域 4：提示工程与结构化输出（20%）

> **官方学习资源**：
> - [Building with the Claude API 课程](https://anthropic.skilljar.com/claude-with-the-anthropic-api)（8.1h）
> - [提示工程文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
> - [Tool Use 文档](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)

---

## 4.1 明确标准的提示设计 ⟵ 任务 4.1

### 核心原则

**具体标准 >> 模糊指令**

```
❌ "检查代码是否准确"
❌ "保守一些"
✅ "仅在行为矛盾时标记；跳过次要风格问题"
```

### 审查标准示例

```markdown
## 报告的问题（标记为需要修改）
- Bug：逻辑错误、空指针、竞态条件
- 安全：SQL 注入、XSS、未验证输入

## 跳过的问题（不标记）
- 命名风格偏好
- 注释缺失
- 格式不一致
```

### 高误报率的修复

**临时策略**：暂时禁用高误报类别 → 恢复开发者信任 → 再逐步启用

---

## 4.2 少样本提示 ⟵ 任务 4.2

### 少样本示例是最有效的技术 ⭐

**适用场景**：
1. 实现一致格式化
2. 处理歧义案例
3. 减少提取任务中的幻觉
4. 泛化判断到新模式

### 示例：处理歧义场景

```xml
<examples>
  <example>
    <input>文档提到"服务费 $50"和"处理费 $50"</input>
    <output>
      {
        "service_fee": 50,
        "processing_fee": 50,
        "reasoning": "虽然金额相同，但文档明确区分了两种费用类型"
      }
    </output>
  </example>
  <example>
    <input>发票总额 $100，但逐项加起来是 $95</input>
    <output>
      {
        "stated_total": 100,
        "calculated_total": 95,
        "conflict_detected": true,
        "reasoning": "声明总额与计算总额不一致"
      }
    </output>
  </example>
</examples>
```

### 关键：解决必填字段空/null 提取问题

添加展示不同格式文档正确提取的少样本示例 → 减少空值提取

---

## 4.3 结构化输出（tool_use + JSON 模式）⟵ 任务 4.3

### 两种结构化输出方式 ⭐

> **方式一：tool_use + strict: true**（考试重点，学习资料已覆盖）  
> **方式二：output_config.format**（新功能，了解即可）

#### 方式一：工具使用 + 严格模式（考试核心）

保证模式兼容输出的最可靠方法：

```python
# 定义提取工具
tools = [{
    "name": "extract_invoice",
    "description": "从发票文档中提取结构化数据",
    "input_schema": {
        "type": "object",
        "required": ["vendor_name", "invoice_date", "total_amount"],
        "properties": {
            "vendor_name": {"type": "string"},
            "invoice_date": {"type": "string", "description": "ISO 8601 格式"},
            "total_amount": {"type": "number"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "amount": {"type": "number"}
                    }
                }
            },
            "notes": {"type": ["string", "null"]},  # ⭐ 可空字段防止捏造
            "category": {
                "type": "string",
                "enum": ["office_supplies", "software", "travel", "other"]  # ⭐ 枚举 + other
            },
            "category_details": {"type": ["string", "null"]}  # "other" 时的详情
        }
    },
    "strict": true  # ⭐ 严格模式确保模式匹配
}]
```

#### 方式二：output_config.format（了解即可）

直接控制 Claude 的**响应格式**（不经过工具调用）：

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[...],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"}
                },
                "required": ["name", "email"],
                "additionalProperties": False
            }
        }
    }
)
# 结果在 response.content[0].text 中（JSON 字符串）
```

#### 两种方式对比 ⭐

| 维度 | tool_use + strict | output_config.format |
|:---|:---|:---|
| **控制对象** | 工具参数（Claude 如何调用函数） | 响应格式（Claude "说"什么） |
| **结果位置** | `response.content[x].input`（tool_use 块） | `response.content[0].text`（JSON 字符串） |
| **适用场景** | Agent 工作流、函数调用 | 数据提取、生成报告 |
| **可组合** | ✅ 两者可在同一请求中结合使用 | ✅ |

> **考试提示**：考试指南只提到 `tool_use + JSON 模式`，大概率不直接考 `output_config.format`。但两者对比是加分项。

### 模式设计关键模式 ⭐

| 模式 | 用途 |
|:---|:---|
| **可空字段** `"type": ["string", "null"]` | 防止捏造不存在的值 |
| **枚举 + "other"** | 涵盖已知类别 + 未知情况 |
| **"unclear" 枚举值** | 允许模型表达不确定性 |
| **strict: true** | 消除语法错误（但不防止语义错误） |

### strict: true 的限制 ⭐ 补充

| 限制 | 说明 |
|:---|:---|
| 每个请求最多 20 个 strict 工具 | 超出会报错 |
| 最多 24 个可选参数 | Schema 复杂度限制 |
| 最多 16 个联合类型参数 | Schema 复杂度限制 |
| 编译超时 180 秒 | 首次使用新 Schema 需编译（缓存 24h） |
| 不支持 `minimum/maximum/pattern` 等约束 | 只保证结构，不保证值范围 |
| `refusal` 或 `max_tokens` 时可能输出不符合 Schema | 异常中断时无法保证 |
| 属性排序 | 必填字段在前，可选字段在后 |

> **考试核心**：只需记住"消除语法错误但不防止语义错误"这一核心概念。上述限制细节作为深度理解即可。

### tool_choice 用于结构化输出

```python
# 保证结构化输出（文档类型未知时）
response = client.messages.create(
    tool_choice={"type": "any"},  # ⭐ 强制使用工具 → 保证结构化输出
    tools=tools,
    ...
)

# 强制使用特定工具（确保提取在富化前运行）
response = client.messages.create(
    tool_choice={"type": "tool", "name": "extract_invoice"},
    ...
)
```

---

## 4.4 验证-重试-反馈循环 ⟵ 任务 4.4

### 重试模式

```
1. 初始提取
2. 验证结果（模式 + 语义）
3. 如果失败：附带原文档 + 失败提取 + 具体验证错误 → 重新请求
4. 如果成功：输出结果
```

### 重试的局限性

| 场景 | 重试是否有效 |
|:---|:---|
| 格式解析错误 | ✅ 有效 |
| 歧义需要推理 | ✅ 有效 |
| 信息不存在于源文档 | ❌ 无效（不要重试） |

### 自我修正验证字段

```json
{
  "calculated_total": 95.50,
  "stated_total": 100.00,
  "conflict_detected": true,
  "detected_pattern": "line_item_sum_mismatch"
}
```

`detected_pattern` 字段 → 启用误报模式分析

---

## 4.5 批处理策略 ⟵ 任务 4.5

### Message Batches API 核心参数 ⭐

| 参数 | 值 |
|:---|:---|
| **成本节省** | 50%（可与 Prompt Caching 叠加，见下方详情） |
| **最长处理时间** | 24 小时（大多数 1 小时内完成） |
| **结果保留** | 29 天 |
| **最大批次** | 100,000 请求或 256 MB |
| **延迟 SLA** | ❌ 无保证 |
| **多轮工具调用** | ❌ 不支持 |

### Prompt Caching 与批处理叠加 ⭐ 补充

批处理 50% 折扣与 Prompt Caching 的缓存命中折扣**可以叠加**，进一步降低成本。

**叠加最佳实践**：

| 要点 | 说明 |
|:---|:---|
| 缓存命中率 | 取决于请求前缀的一致性（需 100% 相同） |
| `cache_control` 位置 | 放在跨请求保持不变的**最后一个块**上 |
| TTL | 默认 5 分钟（高频）或 1 小时（低频，成本 2x） |
| 最小缓存 Token 数 | 需达到模型要求（如 Opus 4096 tokens） |
| 缓存前缀顺序 | Tools → System → Messages |
| 最多缓存断点 | 4 个 |

**Prompt Caching 配置方式**：

```python
# 方式 1：自动缓存（推荐用于多轮对话）
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},  # 自动缓存最后一个可缓存块
    system="你是一个有帮助的助手...",
    messages=[...]
)

# 方式 2：显式缓存断点（需要精细控制时）
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "大量静态系统指令...",
            "cache_control": {"type": "ephemeral"}  # 显式标记缓存点
        }
    ],
    messages=[...]
)
```

**失效注意事项**：修改工具定义、启用/禁用网络搜索、修改 `tool_choice`、添加/删除图像都会导致缓存失效。

> **考试提示**：考试大概率只考"批处理可与 Prompt Caching 叠加节省更多"这一事实，不会深入考缓存配置细节。

### 批处理 vs 同步 API 选择 ⭐⭐

**考试场景**（样题 11）：

| 任务类型 | 选择 | 原因 |
|:---|:---|:---|
| **阻塞合并前检查** | 同步 API | 不能等 24 小时 |
| **隔夜技术债务报告** | 批处理 API | 延迟容忍，省 50% |

### custom_id 的作用

- 关联请求和响应（结果不保证顺序）
- 识别失败文档并重新提交
- 使用有意义命名（如 `doc-invoice-001`）

### 最佳实践

**批量处理前先在样本集上细化提示** → 避免浪费大批量的 Token

---

## 4.6 多实例/多遍审查 ⟵ 任务 4.6

### 自我审查的局限 ⭐

> **自我审查保留了生成时的推理上下文 → 不太可能质疑自己的判断**

### 正确的审查架构

```
方案 1: 独立审查实例
  生成器实例 → 输出 → 独立审查实例（不带推理上下文）

方案 2: 多遍审查（代码审查场景）
  第一遍：按文件逐个分析本地问题
  第二遍：跨文件集成遍历（数据流、接口一致性）

方案 3: 置信度路由
  验证遍历中自报告置信度 → 低置信度路由到人工审查
```

**考试场景**（样题 12）：
> 14 文件 PR 单遍审查不一致 → **拆分为按文件分析 + 集成遍历**

---

# 领域 5：上下文管理与可靠性（15%）

> **官方学习资源**：
> - [Agent SDK 文档 - 智能体循环](https://platform.claude.com/docs/en/agent-sdk/agent-loop)
> - [Claude Code Memory 文档](https://code.claude.com/docs/en/memory)
> - [Building agents 博客](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)

---

## 5.1 上下文管理 ⟵ 任务 5.1

### 三大上下文风险

| 风险 | 说明 | 缓解措施 |
|:---|:---|:---|
| **渐进摘要失真** | 数值、日期被压缩为模糊摘要 | 将关键事实提取到持久"案例事实"块 |
| **迷失在中间** | 长上下文中间内容被忽视 | 关键发现放在开头 + 明确标题 |
| **工具结果膨胀** | 累积的工具输出消耗 Token | 修剪为仅相关字段 |

### 最佳实践

```markdown
## 案例事实块（持久化）
- 客户 ID: CUST-12345
- 订单金额: $49.99
- 争议日期: 2026-03-15
- 争议原因: 重复扣款

## 当前调查进展
[最新发现放这里]

## 历史上下文（可压缩）
[旧的对话摘要]
```

### 子智能体输出规范

- 包含元数据支持准确下游综合
- 返回**结构化数据**而非冗长推理链
- 上游智能体应返回精简结构，不是完整推理过程

---

## 5.2 升级与歧义解决 ⟵ 任务 5.2

### 适当升级触发器 ⭐

| 触发器 | 处理方式 |
|:---|:---|
| 客户明确要求人工 | **立即升级** |
| 策略例外/策略空白 | 升级 |
| 无法进展（尝试后仍失败） | 升级 |
| 客户表达不满 | 承认挫折 + 提供解决方案，仅在客户重申时升级 |
| 多客户匹配 | 要求额外标识符（**不要**启发式选择） |

### ⚠️ 不可靠的升级方式

- **❌ 基于情绪的升级** — 情绪与案例复杂性不相关
- **❌ 自我报告置信度** — LLM 的置信度校准很差

**考试场景**（样题 3）：
> 智能体升级简单案例却自主处理复杂情况 → **添加带少样本示例的明确升级标准**

---

## 5.3 错误传播策略 ⟵ 任务 5.3

### 结构化错误上下文 ⭐

```json
{
  "failure_type": "timeout",
  "attempted_query": "AI music industry impact 2025",
  "partial_results": ["找到 3 篇相关文章，但未完成分析"],
  "alternative_suggestions": ["缩小搜索范围", "使用不同数据源"],
  "is_recoverable": true
}
```

### 反模式

| 反模式 | 问题 |
|:---|:---|
| **静默抑制错误** | 导致不完整结果无人知晓 |
| **单一失败终止整个工作流** | 在恢复策略可能成功时过早放弃 |
| **通用错误状态** | 隐藏有价值的上下文 |

### 正确模式

- 子智能体本地恢复瞬态故障
- 仅传播无法解决的错误
- 综合输出使用覆盖注释（指示哪些区域有充分支持，哪些存在空白）

---

## 5.4 大型代码库上下文管理 ⟵ 任务 5.4

### 对抗上下文退化的策略

| 策略 | 说明 |
|:---|:---|
| **子智能体委托** | 生成子智能体调查特定问题，主智能体保持高级协调 |
| **草稿本文件** | 维护文件记录关键发现，跨上下文边界持久化 |
| **阶段间注入** | 总结关键发现注入初始上下文 |
| **结构化状态导出** | 导出检查点（清单）用于崩溃恢复 |
| **/compact** | 压缩上下文减少 Token 使用 |

---

## 5.5 人工审查与置信度校准 ⟵ 任务 5.5

### 关键考点

1. **总体准确率可能掩盖问题** — 某些文档类型/字段的性能可能很差
2. **分层随机抽样** — 测量错误率、检测新错误模式
3. **字段级置信度** — 使用标记验证集校准阈值
4. **按文档类型和字段分段验证**

### 审查工作流

```
高置信度（>0.95） → 自动通过 + 分层随机抽样检查
中等置信度（0.7-0.95） → 人工快速审查
低置信度（<0.7） → 人工完整审查
```

---

## 5.6 信息来源与不确定性 ⟵ 任务 5.6

### 声明-来源映射 ⭐

```json
{
  "claim": "AI 将在 2027 年影响 30% 的创意岗位",
  "source": {
    "title": "Creative Industry AI Report",
    "url": "https://example.com/report",
    "publication_date": "2025-11-15",
    "data_collection_date": "2025-Q3"
  },
  "confidence": "established",
  "supporting_sources": 3
}
```

### 冲突处理

- **❌ 不要**任意选择一个值
- **✅ 明确标注**冲突，让协调器/用户决定
- **✅ 使用源归属注释**（"来源 A 称 30%，来源 B 称 45%"）

### 时间数据

- 要求出版/收集日期
- 防止用旧数据做新结论

### 不同内容类型的呈现

| 内容类型 | 呈现方式 |
|:---|:---|
| 金融数据 | 表格 |
| 新闻内容 | 散文/叙述 |
| 技术发现 | 结构化列表 |

---

# 附录 A：技术速查表

## Agent SDK 速查

| 概念 | 要点 |
|:---|:---|
| 智能体循环 | 提示 → 评估 → 工具调用 → 结果返回 → 循环 |
| stop_reason | `"end_turn"` = 完成, `"tool_use"` = 继续, `"stop_sequence"` = 停止序列, `"refusal"` = 拒绝, `"pause_turn"` = 服务器工具迭代上限 |
| Task 工具 | 生成子智能体；allowedTools 必须包含 "Task" |
| Claude Code Hooks | JSON 配置（settings.json），20+ 种事件，command/http/prompt/agent 四种处理器 |
| Agent SDK Hooks | Python/TypeScript 代码定义，核心 6 种（PreToolUse、PostToolUse 等） |
| 钩子 vs 提示 | 钩子 = 确定性保证；提示 = 概率性合规 |
| 子智能体上下文 | 不继承父上下文，必须显式传递 |

## MCP 速查

| 概念 | 要点 |
|:---|:---|
| 三大原语 | Tools（操作）、Resources（数据）、Prompts（模板） |
| isError 标志 | 标记工具返回为错误 |
| 服务器范围 | `.mcp.json`（项目级）、`~/.claude.json`（用户级） |
| 环境变量 | `${GITHUB_TOKEN}` 展开语法 |

## Claude Code 速查

| 概念 | 要点 |
|:---|:---|
| CLAUDE.md 层级 | 项目级 > 用户级 > 组织级 |
| .claude/rules/ | YAML frontmatter paths 字段 + glob 模式 |
| 命令位置 | `.claude/commands/`（项目）、`~/.claude/commands/`（个人） |
| SKILL.md | context: fork, allowed-tools, argument-hint |
| CLI 标志 | `-p` 非交互, `--output-format json`, `--json-schema` |
| 计划模式 | 大规模/多方法/架构决策 → 计划；简单明确 → 直接执行 |

## API 速查

| 概念 | 要点 |
|:---|:---|
| tool_choice | "auto" / "any" / "none" / 强制特定工具 |
| disable_parallel_tool_use | 在 tool_choice 中设置，强制串行工具调用 |
| JSON Schema | required, optional, nullable, enum + "other" |
| strict: true | 保证模式匹配，不防语义错误；限制 20 工具/24 可选参数 |
| output_config.format | 直接控制响应 JSON 格式（与 tool_use strict 互补） |
| Batches API | 50% 省钱（可叠加 Prompt Caching）, 24h 窗口, custom_id, 不支持多轮工具调用 |
| Prompt Caching | TTL 5min/1h, 最多 4 断点, cache_control 放在不变的最后一个块上 |
| stop_reason | "end_turn", "tool_use", "max_tokens", "stop_sequence", "refusal", "pause_turn" |

---

# 附录 B：样题解题策略

## 解题框架

考试是**场景型**单选题，每题有 1 个正确答案和 3 个干扰项。核心解题思路：

### 1. 识别问题类型

| 类型 | 标志词 | 答题策略 |
|:---|:---|:---|
| **根因分析** | "最可能的根因"、"日志显示" | 从证据出发，锁定根因 |
| **最佳方案** | "最有效"、"最可靠" | 排除过度工程化和不足的方案 |
| **配置选择** | "应该在哪里"、"如何配置" | 匹配范围需求（项目/用户/组织） |
| **首要步骤** | "第一步"、"首先" | 选低成本高杠杆的方案 |

### 2. 排除干扰项的常见模式

| 干扰项模式 | 例子 |
|:---|:---|
| **过度工程化** | "部署独立分类器"、"训练 ML 模型" |
| **不存在的功能** | `CLAUDE_HEADLESS=true`、`--batch` 标志 |
| **解决错误问题** | 情绪分析解决升级问题（实际是复杂性问题） |
| **概率性方案解决确定性需求** | 用提示指令保证退款前验证 |
| **归咎下游** | 子智能体工作正确但被分配了错误的任务 |

### 3. 核心判断原则

- **确定性需求 → 程序化强制**（钩子、前置条件）
- **软性偏好 → 提示指令**（系统提示、少样本）
- **工具选择问题 → 先改描述**（低成本高杠杆）
- **大规模/架构 → 计划模式；简单明确 → 直接执行**
- **阻塞任务 → 同步 API；非阻塞 → 批处理 API**
- **审查质量 → 独立实例 > 自我审查**

---

# 附录 C：考试范围内外速查

## ✅ 考试范围内

- 智能体循环实现（stop_reason、工具结果处理）
- 多智能体编排（协调器-子智能体、任务分解、并行执行）
- 子智能体上下文管理（显式传递、状态持久化）
- 工具接口设计（描述质量、命名、拆分合并）
- MCP 工具和资源设计（资源目录、isError）
- MCP 服务器配置（.mcp.json、~/.claude.json）
- 错误处理和传播（结构化响应、错误分类）
- 升级决策（明确标准、客户偏好、策略空白）
- CLAUDE.md 配置（层级、@import、rules/ glob）
- 自定义命令和技能（范围、frontmatter 选项）
- 计划模式 vs 直接执行
- 迭代细化（示例、测试驱动、面试模式）
- 结构化输出（tool_use、tool_choice、可空字段）
- 少样本提示（歧义定位、格式一致性）
- 批处理（Batches API、custom_id）
- 上下文窗口优化（修剪、事实提取、位置感知排序）
- 人工审查（置信度校准、分层抽样）
- 信息来源（声明-来源映射、冲突注释）

## ❌ 不考的内容

- 微调 Claude 或训练自定义模型
- API 认证、计费、账户管理
- 特定编程语言/框架的实现细节
- 部署/托管 MCP 服务器（基础设施、容器）
- Claude 内部架构、训练过程
- Constitutional AI、RLHF、安全训练
- 嵌入模型、向量数据库实现
- 计算机使用（浏览器自动化）
- 视觉/图像分析能力
- 流式 API、服务器发送事件
- 速率限制、配额、API 定价
- OAuth、API 密钥轮换
- 特定云提供商配置（AWS、GCP、Azure）
- 性能基准测试、模型比较
- 提示缓存实现细节
- 令牌计数算法、分词细节

---

# 附录 E：练习参考实现

> 考试指南包含 4 个实操练习，以下提供每个练习的参考实现骨架和关键设计要点。

---

## 练习 1：构建带有升级逻辑的多工具智能体

**目标**：设计包含工具集成、结构化错误处理和升级模式的智能体循环。  
**强化领域**：1、2、5

### 参考实现

```python
import anthropic

client = anthropic.Anthropic()

# ⭐ 步骤 1: 定义 3-4 个 MCP 工具，包含功能相似的工具需要仔细描述
tools = [
    {
        "name": "get_customer",
        "description": "根据客户 ID、邮箱或电话检索客户账户信息。返回姓名、联系方式、"
                       "账户状态和历史。不返回订单数据——订单查询请用 lookup_order。",
        "input_schema": {
            "type": "object",
            "required": ["identifier"],
            "properties": {
                "identifier": {"type": "string", "description": "客户 ID（CUST-XXXXX）、邮箱或电话"}
            }
        }
    },
    {
        "name": "lookup_order",
        "description": "根据订单 ID 检索订单详情。需要已验证的客户 ID。"
                       "返回订单状态、金额、商品列表。不修改订单——退款请用 process_refund。",
        "input_schema": {
            "type": "object",
            "required": ["order_id", "customer_id"],  # ⭐ 要求 customer_id 作为程序化前置条件
            "properties": {
                "order_id": {"type": "string"},
                "customer_id": {"type": "string", "description": "已通过 get_customer 验证的客户 ID"}
            }
        }
    },
    {
        "name": "process_refund",
        "description": "处理退款。需要已验证的客户 ID 和订单 ID。金额不可超过订单总额。",
        "input_schema": {
            "type": "object",
            "required": ["customer_id", "order_id", "amount", "reason"],
            "properties": {
                "customer_id": {"type": "string"},
                "order_id": {"type": "string"},
                "amount": {"type": "number"},
                "reason": {"type": "string"}
            }
        }
    },
    {
        "name": "escalate_to_human",
        "description": "将案例升级给人工客服。用于：客户明确要求人工、策略例外/空白、尝试后仍无法解决。",
        "input_schema": {
            "type": "object",
            "required": ["customer_id", "reason", "summary"],
            "properties": {
                "customer_id": {"type": "string"},
                "reason": {"type": "string", "enum": ["customer_request", "policy_exception", "unable_to_resolve"]},
                "summary": {"type": "string", "description": "包含根因、已尝试步骤、建议操作的交接摘要"}
            }
        }
    }
]

# ⭐ 步骤 4: 程序化钩子强制业务规则（PreToolUse 拦截）
verified_customers = set()

def pre_tool_use_hook(tool_name, tool_input):
    """程序化前置条件：阻止未验证就退款"""
    if tool_name == "process_refund":
        cid = tool_input.get("customer_id")
        if cid not in verified_customers:
            return {"blocked": True, "reason": "必须先通过 get_customer 验证客户身份"}
    if tool_name == "lookup_order":
        cid = tool_input.get("customer_id")
        if cid not in verified_customers:
            return {"blocked": True, "reason": "必须先通过 get_customer 验证客户身份"}
    return {"blocked": False}

def execute_tool(tool_name, tool_input):
    """执行工具并返回结构化错误响应"""
    # 钩子检查
    hook_result = pre_tool_use_hook(tool_name, tool_input)
    if hook_result["blocked"]:
        return {"isError": True, "content": [{"type": "text", "text": json.dumps({
            "errorCategory": "precondition_failed",
            "isRetryable": False,
            "message": hook_result["reason"]
        })}]}
    
    try:
        result = call_backend(tool_name, tool_input)
        # PostToolUse: 记录已验证客户
        if tool_name == "get_customer" and result.get("status") == "verified":
            verified_customers.add(result["customer_id"])
        return {"isError": False, "content": [{"type": "text", "text": json.dumps(result)}]}
    except TimeoutError:
        # ⭐ 步骤 3: 结构化错误响应（瞬态错误可重试）
        return {"isError": True, "content": [{"type": "text", "text": json.dumps({
            "errorCategory": "transient",
            "isRetryable": True,
            "message": "后端服务超时，请重试"
        })}]}

# ⭐ 步骤 2: 智能体循环，检查 stop_reason
messages = [{"role": "user", "content": "我要退款，订单号 ORD-789，我叫张三，邮箱 zhang@example.com"}]

while True:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        system="你是客户支持智能体。必须先验证客户身份再处理任何操作。"
               "遇到策略例外或客户要求人工时，使用 escalate_to_human。",
        tools=tools,
        messages=messages
    )
    
    # ✅ 基于 stop_reason 驱动循环
    if response.stop_reason == "end_turn":
        print("完成:", response.content[0].text)
        break
    elif response.stop_reason == "tool_use":
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({"type": "tool_result", "tool_use_id": block.id, **result})
        messages.append({"role": "user", "content": tool_results})
    elif response.stop_reason == "max_tokens":
        print("输出截断，需要续写")
        break
```

**关键设计要点**：
1. ✅ 工具描述清楚区分用途（get_customer vs lookup_order vs process_refund）
2. ✅ 程序化前置条件（钩子）而非提示指令保证验证顺序
3. ✅ 结构化错误响应含 errorCategory + isRetryable
4. ✅ 基于 stop_reason 的循环控制
5. ✅ 升级工具含交接摘要

---

## 练习 2：为团队开发工作流配置 Claude Code

**目标**：配置 CLAUDE.md 层级、自定义斜杠命令、路径特定规则和 MCP 服务器集成。  
**强化领域**：3、2

### 参考项目结构

```
my-project/
├── .claude/
│   ├── CLAUDE.md                    # ⭐ 项目级主配置（团队共享）
│   ├── settings.json                # ⭐ 项目级 Hooks 配置
│   ├── rules/
│   │   ├── code-style.md            # 代码风格规则
│   │   ├── testing.md               # 测试约定（glob: **/*.test.tsx）
│   │   ├── api.md                   # API 规则（glob: src/api/**/*.ts）
│   │   └── terraform.md             # IaC 规则（glob: terraform/**/*）
│   └── commands/
│       └── review.md                # ⭐ 项目级命令（团队共享）
├── .mcp.json                        # ⭐ 项目级 MCP 配置（团队共享）
├── src/
│   ├── api/
│   └── components/
├── terraform/
└── package.json
```

### 步骤 1：项目级 CLAUDE.md

```markdown
# 项目配置

## 架构
- React + TypeScript 前端
- Express.js 后端
- PostgreSQL 数据库

## 编码标准
- 使用 TypeScript strict mode
- 组件使用函数式写法 + hooks
- 参考 @package.json 获取可用命令
- 参考 @docs/api-conventions.md 获取 API 设计规范

## CI/CD
- 测试框架：Jest + React Testing Library
- Fixture 约定：__fixtures__/ 目录
- 提交前必须通过 `npm run lint && npm test`
```

### 步骤 2：路径特定规则（.claude/rules/）

```markdown
---
paths:
  - "**/*.test.tsx"
  - "**/*.test.ts"
---

# 测试约定
- 使用 React Testing Library，不使用 Enzyme
- 测试用户行为而非实现细节
- Fixture 放在同级 __fixtures__/ 目录
- 每个组件至少一个快照测试 + 一个交互测试
```

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规则
- 所有端点必须包含输入验证（使用 zod）
- 使用标准错误响应格式 { error: { code, message } }
- 所有数据库查询使用参数化查询
- 添加请求日志中间件
```

### 步骤 3：带 context: fork 的技能

```markdown
---
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
argument-hint: "文件路径或目录"
---

# 安全审查技能

审查指定文件或目录的安全问题：
1. 检查 SQL 注入风险（字符串拼接查询）
2. 检查 XSS 风险（未转义用户输入）
3. 检查硬编码密钥
4. 检查未验证的输入
5. 生成结构化报告含严重级别和修复建议
```

> **context: fork 的意义**：技能在隔离的子智能体上下文中运行，不会污染主对话上下文。

### 步骤 4：MCP 服务器配置

```json
// .mcp.json（项目级，团队共享）
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

```json
// ~/.claude.json（用户级，仅个人）
{
  "mcpServers": {
    "notes": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_PATHS": "/Users/me/notes"
      }
    }
  }
}
```

### 步骤 5：Hooks 配置

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-dangerous-commands.sh",
            "statusMessage": "检查命令安全性..."
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx eslint --fix ${TOOL_INPUT_FILE}",
            "statusMessage": "自动修复代码风格..."
          }
        ]
      }
    ]
  }
}
```

**关键设计要点**：
1. ✅ 团队标准放项目级（版本控制共享），个人偏好放用户级
2. ✅ 分散文件用 `.claude/rules/` + glob 模式（而非每个子目录放 CLAUDE.md）
3. ✅ 技能用 `context: fork` + `allowed-tools` 隔离运行
4. ✅ MCP 服务器用环境变量展开，不硬编码密钥
5. ✅ 计划模式用于架构决策，直接执行用于简单修复

---

## 练习 3：构建结构化数据提取流水线

**目标**：设计 JSON 模式、tool_use 结构化输出、验证-重试循环、批处理策略。  
**强化领域**：4、5

### 参考实现

```python
import anthropic
import json

client = anthropic.Anthropic()

# ⭐ 步骤 1: 定义 JSON 模式（必填/可选/可空/枚举 + other）
extraction_tool = {
    "name": "extract_invoice",
    "description": "从发票文档中提取结构化数据。对于文档中不存在的信息，使用 null。",
    "input_schema": {
        "type": "object",
        "required": ["vendor_name", "invoice_date", "total_amount", "currency", "confidence"],
        "properties": {
            "vendor_name": {"type": "string", "description": "供应商/卖方名称"},
            "invoice_date": {"type": "string", "description": "发票日期，ISO 8601 格式"},
            "total_amount": {"type": "number", "description": "发票总金额"},
            "currency": {"type": "string", "description": "货币代码，如 USD, CNY"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": ["number", "null"]},
                        "unit_price": {"type": ["number", "null"]},
                        "amount": {"type": "number"}
                    },
                    "required": ["description", "amount"]
                }
            },
            "tax_amount": {"type": ["number", "null"]},       # ⭐ 可空：防止捏造
            "po_number": {"type": ["string", "null"]},          # ⭐ 可空：文档中可能没有
            "category": {
                "type": "string",
                "enum": ["office_supplies", "software", "consulting", "travel", "utilities", "other"]
            },
            "category_details": {"type": ["string", "null"]},   # "other" 时的说明
            "confidence": {
                "type": "string",
                "enum": ["high", "medium", "low", "unclear"]    # ⭐ 含 unclear 值
            },
            "calculated_total": {"type": ["number", "null"]},   # 自我验证字段
            "total_mismatch": {"type": "boolean"}               # 声明 vs 计算不一致标记
        }
    },
    "strict": True  # ⭐ 严格模式
}

# ⭐ 步骤 3: 少样本示例处理不同格式
few_shot_examples = """
<examples>
  <example>
    <input>INVOICE #2025-001\nAcme Corp\nDate: March 15, 2025\nItem: Laptop - $1,200\nItem: Mouse - $50\nSubtotal: $1,250\nTax: $100\nTotal: $1,350</input>
    <output>vendor_name: "Acme Corp", total_amount: 1350, tax_amount: 100, calculated_total: 1350, total_mismatch: false, confidence: "high"</output>
  </example>
  <example>
    <input>发票\n供应商：未明确\n日期：2025/3\n合计：约5000元</input>
    <output>vendor_name: "未明确", invoice_date: "2025-03", total_amount: 5000, confidence: "low"（日期不完整，供应商不明确）</output>
  </example>
</examples>
"""

# ⭐ 步骤 2: 验证-重试循环
def extract_with_retry(document_text, max_retries=2):
    messages = [{"role": "user", "content": f"{few_shot_examples}\n\n请提取以下发票信息：\n\n{document_text}"}]
    
    for attempt in range(max_retries + 1):
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            tools=[extraction_tool],
            tool_choice={"type": "tool", "name": "extract_invoice"},  # ⭐ 强制使用提取工具
            messages=messages
        )
        
        for block in response.content:
            if block.type == "tool_use":
                result = block.input
                
                # 语义验证
                errors = validate_extraction(result)
                if not errors:
                    return {"status": "success", "data": result, "attempts": attempt + 1}
                
                if attempt < max_retries:
                    # ⭐ 重试：附带原文档 + 失败提取 + 具体错误
                    messages = [{"role": "user", "content": (
                        f"原始文档：\n{document_text}\n\n"
                        f"上次提取结果：\n{json.dumps(result, ensure_ascii=False)}\n\n"
                        f"验证错误：\n{chr(10).join(errors)}\n\n"
                        f"请修正上述错误并重新提取。"
                    )}]
    
    return {"status": "failed", "data": result, "errors": errors}

def validate_extraction(result):
    """模式 + 语义验证"""
    errors = []
    # 检查必填字段
    if not result.get("vendor_name"):
        errors.append("缺少供应商名称")
    # 检查金额一致性
    if result.get("line_items") and result.get("calculated_total"):
        item_sum = sum(item["amount"] for item in result["line_items"])
        if abs(item_sum - result["calculated_total"]) > 0.01:
            errors.append(f"行项目总和 {item_sum} 与 calculated_total {result['calculated_total']} 不一致")
    # 信息不存在于源文档时不重试
    # （可空字段为 null 是正常情况，不算错误）
    return errors

# ⭐ 步骤 4: Message Batches API 批处理策略
def create_batch(documents):
    """批量处理前先在样本集上细化提示"""
    requests = []
    for doc_id, doc_text in documents.items():
        requests.append({
            "custom_id": f"invoice-{doc_id}",  # ⭐ 有意义的 custom_id
            "params": {
                "model": "claude-opus-4-6",
                "max_tokens": 4096,
                "tools": [extraction_tool],
                "tool_choice": {"type": "tool", "name": "extract_invoice"},
                "messages": [{"role": "user", "content": f"{few_shot_examples}\n\n{doc_text}"}]
            }
        })
    
    batch = client.messages.batches.create(requests=requests)
    return batch.id  # 异步处理，不等待结果

# ⭐ 步骤 5: 人工审查路由（基于 confidence 字段）
def route_for_review(result):
    confidence = result["data"].get("confidence", "unclear")
    if confidence == "high":
        return "auto_approve"       # 自动通过 + 分层随机抽样
    elif confidence == "medium":
        return "quick_review"       # 人工快速审查
    else:  # low 或 unclear
        return "full_review"        # 人工完整审查
```

**关键设计要点**：
1. ✅ 可空字段防止捏造 + 枚举含 "other" + "unclear" 置信度
2. ✅ 验证-重试循环：附带原文档 + 失败结果 + 具体错误
3. ✅ 区分"格式错误可重试"vs"信息不存在不重试"
4. ✅ 批处理用 custom_id 关联请求，先在样本上细化提示
5. ✅ 字段级置信度驱动人工审查路由

---

## 练习 4：设计和调试多智能体研究流水线

**目标**：编排子智能体、管理上下文传递、实现错误传播和含来源追踪的综合。  
**强化领域**：1、2、5

### 参考架构

```
          ┌──────────────────┐
          │     协调器         │
          │  研究编排器        │
          └────────┬─────────┘
         ┌─────────┼─────────┐
         ▼         ▼         ▼
   ┌──────────┐┌──────────┐┌──────────┐
   │ 搜索子智能体 ││ 搜索子智能体 ││ 搜索子智能体 │
   │  音乐领域  ││  写作领域  ││  电影领域  │
   └─────┬────┘└─────┬────┘└─────┬────┘
         └─────────┼─────────┘
                   ▼
          ┌──────────────────┐
          │   综合子智能体     │
          │ 汇总 + 冲突标注   │
          └──────────────────┘
```

### 参考实现

```python
# ⭐ 步骤 1: 协调器配置（allowedTools 含 "Task"）
coordinator_prompt = """
你是一个研究编排器。研究主题：{topic}

任务：
1. 将研究主题分解为 3-5 个子领域（注意避免过窄分解）
2. 为每个子领域生成搜索子智能体（并行执行）
3. 评估搜索结果的覆盖度
4. 如有空白，生成补充搜索
5. 将所有结果交给综合子智能体，要求保留来源归属

质量标准：
- 每个子领域至少 2 个独立来源
- 标注所有来源的出版日期
- 冲突信息必须保留双方来源
"""

# 搜索子智能体定义
search_agent = {
    "description": "搜索特定领域的信息",
    "system_prompt": "你是一个研究搜索专家。搜索时必须：\n"
                     "1. 返回结构化结果，分离内容和元数据\n"
                     "2. 标注出版/收集日期\n"
                     "3. 标明来源可信度",
    "allowed_tools": ["WebSearch", "WebFetch"]  # 不含 "Task"，不能嵌套
}

# 综合子智能体定义
synthesis_agent = {
    "description": "综合多个来源的研究发现",
    "system_prompt": "你是一个研究综合专家。综合时必须：\n"
                     "1. 保留所有声明的来源归属\n"
                     "2. 标注冲突信息（来源 A 称 X，来源 B 称 Y）\n"
                     "3. 标注覆盖度（哪些区域有充分支持，哪些存在空白）\n"
                     "4. 不任意选择冲突值",
    "allowed_tools": ["Read", "Write"]  # 只需读写草稿
}

# ⭐ 步骤 2: 并行子智能体执行
# 协调器在单个响应中发出多个 Task 调用 → 并行执行
parallel_tasks = [
    {"prompt": f"搜索音乐领域的 AI 影响。\n\n研究背景：{context}", "agent": search_agent},
    {"prompt": f"搜索写作领域的 AI 影响。\n\n研究背景：{context}", "agent": search_agent},
    {"prompt": f"搜索电影领域的 AI 影响。\n\n研究背景：{context}", "agent": search_agent},
]

# ⭐ 步骤 3: 子智能体返回结构化输出（分离内容与元数据）
search_result_format = {
    "findings": [
        {
            "claim": "AI 生成音乐工具的市场在 2025 年增长了 340%",
            "source": {
                "title": "Music Industry AI Report",
                "url": "https://example.com/music-ai",
                "publication_date": "2025-09-15",
                "credibility": "high"
            },
            "supporting_sources": 2
        }
    ],
    "coverage_gaps": ["缺少独立音乐人的视角"],
    "metadata": {
        "search_queries_used": ["AI music industry 2025", "AI generated music market"],
        "total_sources_reviewed": 8
    }
}

# ⭐ 步骤 4: 错误传播（模拟子智能体超时）
def handle_subagent_result(task_name, result):
    """处理子智能体结果，区分错误类型"""
    if result.get("error"):
        error = result["error"]
        if error.get("is_recoverable"):
            # 瞬态错误：本地重试
            return retry_task(task_name, max_retries=2)
        else:
            # 不可恢复：传播给协调器，附带部分结果
            return {
                "status": "partial_failure",
                "failure_type": error["type"],
                "partial_results": error.get("partial_results", []),
                "task_name": task_name
            }
    return {"status": "success", "data": result}

# ⭐ 步骤 5: 综合输出含来源追踪和冲突标注
synthesis_output_format = {
    "sections": [
        {
            "topic": "AI 对音乐产业的影响",
            "summary": "AI 音乐生成工具快速增长...",
            "claims": [
                {
                    "text": "市场增长率存在争议",
                    "sources": [
                        {"source": "Music AI Report", "value": "340%"},
                        {"source": "Industry Analysis", "value": "280%"}
                    ],
                    "conflict": True,  # ⭐ 标注冲突
                    "resolution": "两份报告使用不同的基准年和市场定义"
                }
            ],
            "coverage": "充分"  # ⭐ 覆盖注释
        },
        {
            "topic": "AI 对写作的影响",
            "coverage": "部分（缺少学术写作领域数据）"
        }
    ],
    "overall_gaps": ["缺少亚太地区数据", "表演艺术领域未覆盖"],
    "data_freshness": "所有来源均为 2024-2025 年"
}
```

**关键设计要点**：
1. ✅ 协调器提示避免过窄分解（明确要求 3-5 个子领域）
2. ✅ 搜索子智能体不含 "Task"（不能嵌套），综合子智能体工具受限
3. ✅ 子智能体返回结构化数据+元数据，不是冗长推理链
4. ✅ 错误传播区分瞬态（重试）vs 不可恢复（传播+部分结果）
5. ✅ 综合输出保留来源归属、标注冲突、注释覆盖度

---

# 附录 F：学习资源清单

## 必学课程（按优先级）

| 优先级 | 课程 | 时长 | 对应领域 |
|:---|:---|:---|:---|
| 🔴 P0 | [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action) | 1h | 领域 3 |
| 🔴 P0 | [Introduction to subagents](https://anthropic.skilljar.com/introduction-to-subagents) | 20min | 领域 1 |
| 🔴 P0 | [Introduction to agent skills](https://anthropic.skilljar.com/introduction-to-agent-skills) | 30min | 领域 1, 3 |
| 🟠 P1 | [Introduction to MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol) | 1h | 领域 2 |
| 🟠 P1 | [MCP: Advanced Topics](https://anthropic.skilljar.com/model-context-protocol-advanced-topics) | 1.1h | 领域 2 |
| 🟡 P2 | [Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api) | 8.1h | 领域 4 |

## 必读文档

| 文档 | 链接 | 对应领域 |
|:---|:---|:---|
| Agent SDK 概述 | [platform.claude.com](https://platform.claude.com/docs/en/agent-sdk/overview) | 领域 1 |
| 智能体循环 | [platform.claude.com](https://platform.claude.com/docs/en/agent-sdk/agent-loop) | 领域 1 |
| Claude Code Memory | [code.claude.com](https://code.claude.com/docs/en/memory) | 领域 3 |
| Claude Code Hooks | [code.claude.com](https://code.claude.com/docs/en/hooks) | 领域 1, 3 |
| Tool Use | [docs.anthropic.com](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) | 领域 2, 4 |
| Batch Processing | [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/batch-processing) | 领域 4 |

## 推荐阅读

| 资源 | 链接 | 说明 |
|:---|:---|:---|
| Building Agents 博客 | [claude.com/blog](https://claude.com/blog/building-agents-with-the-claude-agent-sdk) | 代理架构模式 |
| Anthropic Cookbook | [github.com/anthropics](https://github.com/anthropics/anthropic-cookbook) | 代码示例 |
| Agent SDK Demos | [github.com/anthropics](https://github.com/anthropics/claude-agent-sdk-demos) | 示例智能体 |

---

> **学习建议**：本资料覆盖了考试指南中所有 5 个领域的 26 个任务陈述和 4 个实操练习。每个知识点都标注了对应的任务编号（如 ⟵ 任务 1.1），可以对照考试指南逐条检查掌握程度。建议按领域权重分配学习时间：领域 1（27%）> 领域 3（20%）= 领域 4（20%）> 领域 2（18%）> 领域 5（15%）。
