# Claude Code & Cowork 深度研究笔记

> **版本**：v3.0 — 2026年3月24日  
> **资料来源**：以 Anthropic 官方文档和产品页为主，第三方资料作为补充，明确标注来源可靠性

---

## 目录

- [第一部分：Claude Code 深度研究](#第一部分claude-code-深度研究)
- [第二部分：Claude Cowork 深度研究](#第二部分claude-cowork-深度研究)
- [第三部分：Claude Code vs Cowork 对比分析](#第三部分claude-code-vs-cowork-对比分析)
- [第四部分：统一引擎与产品矩阵](#第四部分统一引擎与产品矩阵)
- [第五部分：学习资料与参考链接](#第五部分学习资料与参考链接)

---

# 第一部分：Claude Code 深度研究

## 1.1 产品定位

**一句话**：面向开发者的代理式编码工具（Agentic Coding Tool）。

Claude Code 不是简单的代码补全工具，它是一个**能理解整个代码库、跨文件操作、自主规划和执行的编程代理**。它可以规划方案 → 编写代码 → 运行测试 → 验证结果，形成完整的自动化循环。

> **官方定义**（来源：[code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)）：  
> "Claude Code understands your entire codebase, works across files and tools, and connects to the same engine whether you're in a terminal, IDE, desktop app, or browser."

## 1.2 五种使用形态

Claude Code 不只是终端工具——它有 **5 种** 交互形态，共享同一个底层引擎：

| 形态 | 平台 | 特点 |
|------|------|------|
| **CLI（终端）** | macOS / Linux / Windows (WSL) | 最原始的形态，遵循 Unix 哲学，支持管道和脚本化 |
| **VS Code 扩展** | VS Code / Cursor / Trae 等 | 官方 GUI，内联差异、@提及、检查点、Plugins 管理器 |
| **JetBrains 插件** | IntelliJ IDEA / PyCharm / WebStorm 等 | 官方支持，交互式差异和上下文共享 |
| **Desktop 桌面应用** | macOS / Windows | 独立图形应用，支持计算机使用、PR 监控、并行会话 |
| **Web 浏览器版** | 任何浏览器 | 无需本地设置，云端运行，支持长任务和多任务并行 |

> **来源**：[code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview) + [code.claude.com/docs/en/desktop](https://code.claude.com/docs/en/desktop)

### CLI vs Desktop 功能差异

| 功能 | CLI | Desktop |
|------|-----|---------|
| 权限模式 | 所有模式（包括 dontAsk） | 询问权限、自动接受编辑、计划、绕过权限 |
| 第三方 LLM 提供商 | Bedrock、Vertex、Foundry | 不可用 |
| MCP 服务器 | 设置文件配置 | 连接器 UI |
| 文件附件 | 不可用 | 支持图片、PDF |
| 计算机使用 | 不可用 | macOS 上的屏幕控制 |
| 代理团队 | 支持 | 不可用 |
| 脚本和自动化 | `--print`、Agent SDK | 不可用 |
| 并行会话 | 分开终端窗口 | 侧边栏标签 + 自动 Worktrees |

## 1.3 核心功能详解

### 1.3.1 代码操作与构建

- **功能构建**：跨文件编写代码，理解项目完整上下文
- **Bug 修复**：分析错误信息 → 追踪根因 → 实施修复
- **自动化琐事**：编写测试、修复 Lint 错误、解决合并冲突、更新依赖、编写发布说明
- **Git 集成**：暂存更改、编写提交信息、创建分支、打开 PR

### 1.3.2 CLAUDE.md —— 项目记忆系统

CLAUDE.md 是 Claude Code 的**持久化上下文文件**，相当于给 Claude 的项目说明书。

**三级作用域**：

| 作用域 | 位置 | 用途 |
|--------|------|------|
| 组织级 | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | 全组织安全策略、合规要求 |
| 项目级 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 编码标准、架构决策、审查清单 |
| 用户级 | `~/.claude/CLAUDE.md` | 个人偏好设置 |

**最佳实践**：
- 每文件控制在 **200 行以内**
- 使用具体、可验证的指令（✅ "使用 2 空格缩进" ❌ "格式化代码"）
- 可用 `@path` 语法导入其他文件
- 用 `/init` 命令自动生成初始文件
- 大型项目可拆分到 `.claude/rules/` 目录

> **来源**：[code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

### 1.3.3 Hooks —— 自动化工作流

Hooks 是用户定义的 shell 命令、HTTP 端点或 LLM 提示，在 Claude Code 生命周期的特定点自动执行。

**四种 Hook 类型**：

| 类型 | 描述 | 适用场景 |
|------|------|----------|
| **command** | 运行 shell 命令 | 接收 JSON，通过退出码和 stdout 返回 |
| **http** | 发送 HTTP POST | 集成外部服务 |
| **prompt** | 发送提示给 Claude | 单轮是/否决策判断 |
| **agent** | 生成子代理 | 多轮验证，可读取文件和搜索代码 |

**核心事件**：PreToolUse（工具执行前，可阻止危险操作）、PostToolUse（工具执行后）、SessionStart/End、UserPromptSubmit 等。

**实用场景**：
- 阻止 `rm -rf` 等危险命令
- 编辑后自动运行测试
- 提交前自动 Lint
- 审计日志记录

> **来源**：[code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)

### 1.3.4 MCP（Model Context Protocol）

通过开放标准连接外部数据源和工具：
- Google Drive 设计文档
- Jira 工单
- Slack 数据
- 自定义 API 和工具

### 1.3.5 Agent Teams —— 多代理团队（实验性）

允许多个 Claude Code 实例协同工作，由一个"团队负责人"协调。

**与子代理的区别**：

| 特性 | Subagents（子代理） | Agent Teams（代理团队） |
|------|---------------------|------------------------|
| 上下文 | 独立窗口，结果返回调用者 | 完全独立运作 |
| 通信 | 仅向主代理汇报 | 队友之间直接消息传递 |
| 协调 | 主代理管理所有工作 | 共享任务列表，自我协调 |
| 适用场景 | 专注任务 | 需要讨论和协作的复杂工作 |

**最佳场景**：
- 多人研究和审查
- 竞争性假设调试
- 跨前端/后端/测试的协调开发

> **来源**：[code.claude.com/docs/en/agent-teams](https://code.claude.com/docs/en/agent-teams)

### 1.3.6 CI/CD 集成

**GitHub Actions**：
- 在 PR 或 Issue 评论中 `@claude` 即可触发
- 自动代码审查、Bug 修复、PR 创建
- 遵守 CLAUDE.md 中的项目规范
- 支持 AWS Bedrock 和 Google Vertex AI（通过 OIDC 安全连接）
- 已到 v1.0 GA 版本

> **来源**：[code.claude.com/docs/en/github-actions](https://code.claude.com/docs/en/github-actions)

### 1.3.7 Desktop 专属功能

| 功能 | 说明 |
|------|------|
| **视觉化差异审查** | 逐文件审查代码修改，支持行级注释 |
| **实时应用预览** | 嵌入式浏览器预览前端/后端，自动截图验证 |
| **计算机使用** | macOS 研究预览，可打开应用、控制屏幕（需 Pro/Max） |
| **GitHub PR 监控** | 自动监控 CI 检查、自动修复失败、自动合并 |
| **并行会话** | 侧边栏多会话，每会话自动 Git Worktree 隔离 |
| **Dispatch 集成** | Cowork 中的持久对话可直接请求 Code 会话 |
| **定期任务** | 本地或远程（Anthropic 云端托管）定时执行 |
| **连接器** | Google Calendar、Slack、GitHub、Linear、Notion 等 |

> **来源**：[code.claude.com/docs/en/desktop](https://code.claude.com/docs/en/desktop)

## 1.4 安全架构

### 1.4.1 沙箱化（Sandboxing）

Claude Code 的沙箱基于 **OS 级原语**，不是虚拟机：
- **macOS**：使用 Apple **Seatbelt**（沙箱配置文件）
- **Linux**：使用 **bubblewrap**

**双重隔离边界**：

1. **文件系统隔离**：限制只能访问当前工作目录，禁止访问 SSH 密钥等敏感文件
2. **网络隔离**：沙箱内进程不直接拥有互联网访问，必须通过 **Unix 域套接字**连接到外部代理服务器，该代理强制执行域名白名单

**Cloud 版额外安全**：
- Git 凭据**永远不会**进入沙箱
- 使用自定义代理服务验证 Git 操作内容
- 即使沙箱被攻破，攻击者也无法获取用户凭据

**效果**：权限提示减少了 **84%**。

> **来源**：[anthropic.com/engineering/claude-code-sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)（作者：David Dworken, Oliver Weller-Davies，2025年10月20日）

### 1.4.2 权限模式

| 模式 | 说明 |
|------|------|
| **询问权限** (default) | 每次编辑/执行前询问，推荐新用户 |
| **自动接受编辑** (acceptEdits) | 自动接受文件修改，命令仍需确认 |
| **计划模式** (plan) | 只分析和创建计划，不执行操作 |
| **绕过权限** (bypassPermissions) | 无提示运行，仅用于沙箱容器中 |

## 1.5 CLI 命令参考（精选）

| 命令 | 说明 |
|------|------|
| `claude` | 启动交互式会话 |
| `claude "query"` | 带初始提示启动 |
| `claude -p "query"` | 打印模式（脚本集成用） |
| `cat file \| claude -p "query"` | 管道处理 |
| `claude -c` | 继续最近的对话 |
| `claude -r "session" "query"` | 恢复指定会话 |
| `claude -w feature-auth` | 在隔离 Git Worktree 中启动 |
| `claude --remote "task"` | 在 claude.ai 上创建 Web 会话 |
| `claude --teleport` | 在本地终端恢复 Web 会话 |

> **来源**：[code.claude.com/docs/en/cli-reference](https://code.claude.com/docs/en/cli-reference)

---

# 第二部分：Claude Cowork 深度研究

## 2.1 产品定位

**一句话**：面向所有人的桌面知识工作代理（Agentic AI for Knowledge Work）。

Cowork 不是聊天机器人——它是一个**能直接操作本地文件、执行多步骤任务、跨应用自动化的桌面代理**。目标用户不是开发者，而是市场营销、数据分析、运营、法律、金融等领域的知识工作者。

> **官方定义**（来源：[anthropic.com/product/claude-cowork](https://www.anthropic.com/product/claude-cowork)）：  
> Cowork 旨在处理那些"重复、繁琐且耗时的任务"，让用户"专注于决策和判断"。

> **与 Chat 的核心区别**（来源：[claude.com/product/cowork](https://claude.com/product/cowork)）：  
> "Chat 仅回答消息，无法直接访问文件；Cowork 可以读取、编辑和创建指定文件夹中的文件。"

## 2.2 产品状态

- **发布日期**：2026年1月12日（研究预览版）
- **出品团队**：Anthropic Labs（Mike Krieger 领衔，Instagram 联合创始人）
- **当前状态**：Research Preview（研究预览）
- **平台支持**：macOS + Windows（位于 Claude 桌面应用中，与 Chat 和 Code 并列）

> **来源**：[anthropic.com/news/introducing-anthropic-labs](https://www.anthropic.com/news/introducing-anthropic-labs)（2026年1月13日）

## 2.3 核心功能详解

### 2.3.1 本地文件操作

| 能力 | 说明 |
|------|------|
| **文件整理** | 扫描文件夹（如 Downloads），按类型/日期分类、去重、归档 |
| **数据提取** | 收据、发票、截图 → 格式化电子表格 |
| **文档生成** | 结合公司模板和原始材料，按格式规范生成报告/演示文稿 |
| **研究综合** | 读取多来源资料，识别相关信息，生成可审阅的摘要 |
| **信息提取** | 从合同、报告等密集文档中提取关键信息，结构化呈现 |

### 2.3.2 跨端协作与持久会话

- **手机 ↔ 桌面同步**：手机上发送指令 → Claude 在桌面执行 → 结果发回手机
- **跨会话记忆**：Claude 能记住之前对话的上下文
- **定时任务**：设定频率（如"每天早上检查邮件"、"每周提取指标"），自动执行

### 2.3.3 计算机使用（Computer Use）

Claude 可以直接与屏幕交互：
- 打开应用程序
- 浏览网页
- 运行工具

**执行优先级**：连接器/集成工具 → 浏览器 → 屏幕交互（直接集成更快更精准）

> **来源**：[claude.com/product/cowork](https://claude.com/product/cowork)

### 2.3.4 插件系统

| 组件 | 说明 |
|------|------|
| **技能** | 内置领域知识和最佳实践 |
| **连接器** | 连接现有工具（Slack、Google Drive 等） |
| **子代理** | 处理特定端到端任务的专用代理 |

**角色化**：通过插件可以让 Claude 成为特定角色的专家——销售、财务、法务等。

### 2.3.5 Dispatch 与 Claude Code 联动

Dispatch 是 Cowork 标签页中的持久对话，可以直接请求 Claude Code 会话：
- 修复 Bug
- 更新依赖
- 运行测试
- 打开 PR

> **来源**：[code.claude.com/docs/en/desktop](https://code.claude.com/docs/en/desktop)

## 2.4 安全架构

### 2.4.1 用户控制权

| 机制 | 说明 |
|------|------|
| **显式访问授权** | 用户明确选择 Claude 可访问的文件夹和连接器 |
| **事前确认** | 处理财务/个人/关键任务前必须先询问 |
| **计划审批** | 重大操作前展示计划并等待批准 |
| **管理员控制** | 企业管理员可全局关闭 Cowork |

### 2.4.2 隔离环境

> **官方说法**（来源：[claude.com/product/cowork](https://claude.com/product/cowork)）：  
> "Cowork 在独立的虚拟机（VM）中运行，网络访问通过设置中的允许列表控制。"

⚠️ **注意**：与 Claude Code 使用的 OS 级沙箱（Seatbelt / bubblewrap）不同，Cowork 官方明确使用了"虚拟机"（VM）一词。但 Anthropic 没有公开 VM 的具体技术实现（是哪种虚拟化技术、是完整 VM 还是轻量级容器等）。

### 2.4.3 数据隐私

- **对话历史**存储在本地设备，**不**在 Anthropic 服务器
- 企业审计日志**当前不会**捕获 Cowork 活动
- **不适合** HIPAA、FedRAMP、FSI 等受监管的工作负载

## 2.5 工作模式

**三步操作**：
1. **描述需求** → 用户在桌面或手机上告知目标
2. **Claude 执行** → 自动选择最快路径（连接器 → 浏览器 → 屏幕操作），重大操作前确认
3. **结果交付** → 交付成品（格式化表格、备忘录），不是逐步更新

---

# 第三部分：Claude Code vs Cowork 对比分析

## 3.1 核心定位对比

| 维度 | Claude Code | Cowork |
|------|-------------|--------|
| **一句话定义** | 面向开发者的代理式编码工具 | 面向所有人的桌面知识工作代理 |
| **目标用户** | 开发者、DevOps、技术管理者 | 市场营销、数据分析、运营、法律、金融等 |
| **核心场景** | 写代码、Debug、代码审查、CI/CD | 整理文件、生成报告、数据提取、自动化办公 |
| **交互方式** | 终端 CLI + IDE 扩展 + 桌面应用 + Web | Claude 桌面应用中的标签页 |
| **操作对象** | 代码库、Git 仓库、开发工具链 | 本地文件、文件夹、日常办公应用 |

## 3.2 技术架构对比

| 维度 | Claude Code | Cowork |
|------|-------------|--------|
| **底层引擎** | Claude Execution Engine (CEE) | Claude Execution Engine (CEE) |
| **使用形态** | 5 种（CLI / VS Code / JetBrains / Desktop / Web） | 桌面应用中的标签页 + 手机远程发送 |
| **沙箱技术** | OS 级原语（macOS Seatbelt / Linux bubblewrap） | 独立虚拟机（VM）（官方说法） |
| **网络隔离** | Unix 域套接字代理 + 域名白名单 | 设置中的允许列表 |
| **扩展机制** | MCP + Hooks + Plugins + Agent SDK | 插件（技能 + 连接器 + 子代理） |
| **多代理** | Agent Teams（实验性，多实例协同） | Dispatch（可调用 Code 会话） |
| **CI/CD** | GitHub Actions v1.0 GA / GitLab | 不适用 |
| **Computer Use** | Desktop 版 macOS（研究预览） | 桌面端（连接器优先 → 浏览器 → 屏幕） |

## 3.3 安全模型对比

| 维度 | Claude Code | Cowork |
|------|-------------|--------|
| **隔离级别** | 进程级沙箱（OS 原语） | VM 级隔离 |
| **权限控制** | 4 种权限模式（default / acceptEdits / plan / bypassPermissions） | 显式文件夹授权 + 操作前确认 + 管理员开关 |
| **凭据安全** | 云端版凭据永不进入沙箱 | 对话存本地，审计日志不捕获 |
| **合规** | 未明确说明限制 | 明确不适合 HIPAA / FedRAMP / FSI |

## 3.4 功能矩阵对比

| 功能 | Claude Code | Cowork |
|------|:-----------:|:------:|
| 代码编写与编辑 | ✅ 核心能力 | ❌ |
| Git 操作 | ✅ 完整集成 | ❌ |
| 代码审查 | ✅ CI/CD 自动化 | ❌ |
| 本地文件整理 | ⚠️ 可以但非重点 | ✅ 核心能力 |
| 文档/报告生成 | ⚠️ 技术文档 | ✅ 各类商务文档 |
| 数据提取与结构化 | ⚠️ 代码层面 | ✅ 核心能力 |
| 屏幕控制（Computer Use） | ✅ Desktop macOS | ✅ 桌面端 |
| 定时任务 | ✅ 本地 + 云端 | ✅ |
| 手机远程发送 | ✅ Remote Control | ✅ |
| 跨会话记忆 | ✅ CLAUDE.md + Auto Memory | ✅ |
| 多代理协同 | ✅ Agent Teams | ✅ Dispatch → Code |
| MCP 连接 | ✅ | ✅ 通过连接器 |
| 管道/脚本化 | ✅ Unix 哲学 | ❌ |
| Agent SDK | ✅ | ❌ |

## 3.5 定价对比

两者共享 Claude 的订阅体系（来源：[claude.com/pricing](https://claude.com/pricing)）：

| 计划 | 月费 | Claude Code | Cowork | 说明 |
|------|------|:-----------:|:------:|------|
| **Free** | $0 | ❌ | ❌ | 不包含 |
| **Pro** | $20/月 | ✅ | ✅ | Cowork 消耗限额比 Chat 更快 |
| **Max 5x** | $100/月 | ✅ | ✅ | 5 倍于 Pro 的使用量 |
| **Max 20x** | $200/月 | ✅ | ✅ | 20 倍使用量，重度用户适用 |
| **Team** | $20-100/席/月 | ✅ | ✅ | 标准席位 vs 高级席位 |
| **Enterprise** | $20/席 + API | ✅ | ✅ | 管理员可全局控制开关 |
| **API** | 按 Token 付费 | ✅ | — | 开发者直接调用 |

> ⚠️ **注意**：Cowork 任务消耗的 Rate Limit 比普通 Chat 多得多，因为它需要协调多个子代理和工具调用。Pro 用户使用 Cowork 时可能很快就会触达限额。

## 3.6 选型建议

### 选 Claude Code 的场景
- 你是**开发者**或 DevOps
- 需要**写代码、Debug、做代码审查**
- 需要**CI/CD 自动化**
- 需要**管道脚本集成**和 Agent SDK
- 需要**多代理团队协同**开发

### 选 Cowork 的场景
- 你是**非技术岗**（市场、运营、法务、金融）
- 需要**整理文件、生成报告**
- 需要从**合同/发票/截图中提取数据**
- 需要**跨应用自动化办公**
- 需要**手机下达指令、桌面自动执行**

### 两者协同的场景
- Cowork 的 **Dispatch** 可以自动调用 Claude Code 处理技术任务
- 同一个桌面应用中，Cowork 和 Code 是并列的标签页，随时切换
- 用 Cowork 做需求分析和文档，用 Code 做实现

---

# 第四部分：统一引擎与产品矩阵

## 4.1 Claude Execution Engine (CEE)

Claude Code 和 Cowork 共享同一个底层引擎——**Claude Execution Engine**。这意味着：

- 配置（如 CLAUDE.md）在各端同步
- 记忆（Auto Memory）跨会话持久
- 会话可以在不同设备间传递（Teleport）
- 模型能力一致（Opus / Sonnet）

## 4.2 Anthropic 的完整代理产品矩阵

```
┌─────────────────────────────────────────────────────────┐
│                Claude Execution Engine (CEE)              │
├─────────────┬─────────────┬──────────────┬──────────────┤
│  Claude Code │   Cowork    │  Claude Chat  │  Agent SDK   │
│  (开发者)    │  (所有人)    │  (对话)       │  (自定义)    │
├─────────────┼─────────────┼──────────────┼──────────────┤
│ CLI         │ 桌面标签页    │ Web / App    │ API          │
│ VS Code     │ 手机远程      │              │ 自定义 Agent │
│ JetBrains   │              │              │              │
│ Desktop     │              │              │              │
│ Web         │              │              │              │
│ GitHub CI   │              │              │              │
└─────────────┴─────────────┴──────────────┴──────────────┘
```

## 4.3 发展时间线

| 时间 | 事件 |
|------|------|
| 2025 年中 | Claude Code 以 Research Preview 发布 |
| 2025年10月 | Claude Code 沙箱工程博客发布 |
| 2025年底 | Claude Code 成长为"十亿美元产品"（Anthropic 官方说法） |
| 2026年1月12日 | **Cowork 以 Research Preview 发布** |
| 2026年1月13日 | **Anthropic Labs 团队正式公布**（Mike Krieger 领衔） |
| 2026年2月 | Cowork 支持 Windows |
| 2026年2月24日 | "The Briefing: Enterprise Agents" 虚拟活动 |
| 2026年3月17日 | Claude Code with GUI JetBrains 插件上线 |
| 2026年3月23日 | Cowork Computer Use 更新 |

---

# 第五部分：学习资料与参考链接

## 5.1 Claude Code 官方资料

| 资料 | 链接 | 说明 |
|------|------|------|
| 📖 官方文档总览 | [code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview) | 核心概念、功能列表、架构 |
| 🖥 Desktop 文档 | [code.claude.com/docs/en/desktop](https://code.claude.com/docs/en/desktop) | 桌面应用完整功能 |
| ⌨️ CLI 参考 | [code.claude.com/docs/en/cli-reference](https://code.claude.com/docs/en/cli-reference) | 完整命令行参考 |
| 🔒 沙箱工程博客 | [anthropic.com/engineering/claude-code-sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) | 安全架构深度解析 |
| 🤖 Agent Teams | [code.claude.com/docs/en/agent-teams](https://code.claude.com/docs/en/agent-teams) | 多代理团队文档 |
| ⚙️ GitHub Actions | [code.claude.com/docs/en/github-actions](https://code.claude.com/docs/en/github-actions) | CI/CD 集成指南 |
| 🧠 Memory (CLAUDE.md) | [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) | 项目记忆系统 |
| 🪝 Hooks | [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) | 自动化工作流 |
| 💻 VS Code 扩展 | [code.claude.com/docs/zh-CN/vs-code](https://code.claude.com/docs/zh-CN/vs-code) | VS Code GUI 完整文档（中文） |

## 5.2 Cowork 官方资料

| 资料 | 链接 | 说明 |
|------|------|------|
| 🏠 官方产品页（Anthropic） | [anthropic.com/product/claude-cowork](https://www.anthropic.com/product/claude-cowork) | 产品定位和功能介绍 |
| 📋 官方产品页（Claude） | [claude.com/product/cowork](https://claude.com/product/cowork) | 技术细节、安全、FAQ |
| 🧪 Anthropic Labs 公告 | [anthropic.com/news/introducing-anthropic-labs](https://www.anthropic.com/news/introducing-anthropic-labs) | 发布背景和团队介绍 |
| 🎥 官方 Webinar | [anthropic.com/webinars/future-of-ai-at-work-introducing-cowork](https://www.anthropic.com/webinars/future-of-ai-at-work-introducing-cowork) | 官方介绍视频 |
| 💰 定价页面 | [claude.com/pricing](https://claude.com/pricing) | 各计划功能对比 |

## 5.3 第三方学习资料（补充参考）

| 资料 | 链接 | 说明 |
|------|------|------|
| CoWork vs Agent Team 选型指南 | [jzhix.com/article/2026-03/cowork-selection-guide](https://www.jzhix.com/article/2026-03/2026-03-18-cowork-selection-guide.md) | 含真实成本数据的选型分析 |
| Cowork 深度解析 | [blog.eimoon.com](https://blog.eimoon.com/p/claude-cowork-tutorial-anthropic-ai-desktop-agent/) | 三个完整实操案例 |
| CSDN 实操教程 | [csdn.net](https://blog.csdn.net/starzhou/article/details/158495620) | 步骤详细的入门教程 |
| CC GUI（开源） | [JetBrains 插件市场](https://plugins.jetbrains.com/plugin/29342-cc-gui-claude-or-codex-) | Claude Code + Codex 双引擎 GUI，MIT 开源 |

---

> **免责声明**：本文档基于 2026年3月24日可获取的公开资料编写。Claude Code 和 Cowork 均在快速迭代中，部分功能可能已更新。建议以官方文档为准。
