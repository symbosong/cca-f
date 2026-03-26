# 模块 9：Claude Code 高级特性 — CLAUDE.md + Hooks + CI/CD + 自定义命令

> **官方文档**：https://code.claude.com/docs/en/overview  
> **前置要求**：已完成模块 6（Claude Code 基础）  
> **预计学习时间**：4-5 小时  
> **难度**：⭐⭐⭐

---

## 目录

- [一、CLAUDE.md 三级配置体系](#一claudemd-三级配置体系)
- [二、Hooks 钩子系统](#二hooks-钩子系统)
- [三、CI/CD 集成：GitHub Actions](#三cicd-集成github-actions)
- [四、自定义命令（Skills / Commands）](#四自定义命令skills--commands)
- [五、多 Agent 团队模式](#五多-agent-团队模式)
- [六、权限与安全](#六权限与安全)
- [七、高级配置与调优](#七高级配置与调优)
- [练习题](#练习题)

---

## 一、CLAUDE.md 三级配置体系

CLAUDE.md 是 Claude Code 的「记忆」系统。不同于每次对话重新描述需求，CLAUDE.md 让 Claude **自动加载**你的项目规范、编码标准和工作偏好。

### 1.1 三级配置层次

```
优先级从高到低：

┌─────────────────────────────────────────────────────┐
│  管理策略级（Enterprise — 组织统一规则）                │  ← IT/DevOps 管理
│  位置：/Library/Application Support/                  │
│        ClaudeCode/CLAUDE.md                          │
│  特点：不可被个人覆盖，强制执行                        │
│  用途：安全合规要求、统一编码标准                       │
├─────────────────────────────────────────────────────┤
│  项目级（Project — 团队共享）                          │  ← 提交到 Git
│  位置：./CLAUDE.md 或 ./.claude/CLAUDE.md             │
│  特点：通过源代码控制共享，团队所有成员生效              │
│  用途：项目架构、技术栈规范、测试要求                   │
├─────────────────────────────────────────────────────┤
│  用户级（User — 个人偏好）                             │  ← 仅自己
│  位置：~/.claude/CLAUDE.md                            │
│  特点：适用于所有项目，仅影响自己                       │
│  用途：个人编码风格、偏好语言、快捷方式                 │
└─────────────────────────────────────────────────────┘
```

### 1.2 项目级 CLAUDE.md 完整模板

```markdown
# 项目规范

## 架构
- 使用 Clean Architecture，分为 domain / application / infrastructure 三层
- API 路由在 src/routes/ 下，每个资源一个文件
- 数据模型在 src/models/ 下，使用 SQLAlchemy 2.0+ 风格
- 服务层在 src/services/ 下，禁止直接操作数据库

## 编码标准
- TypeScript strict 模式
- 使用 Zod 做运行时类型校验
- 错误处理使用自定义 AppError 类，禁止裸 catch
- 所有 public 方法必须有 JSDoc 注释
- 变量命名：camelCase，类名：PascalCase，常量：UPPER_SNAKE_CASE

## 测试
- 单元测试使用 Vitest
- 运行测试：pnpm test
- 测试覆盖率阈值：80%
- 每个 PR 必须包含对应测试
- Mock 外部依赖，不要在测试中调用真实 API

## Git 规范
- Commit message 遵循 Conventional Commits
- PR 标题格式：[类型] 简短描述
- 分支命名：feature/xxx, fix/xxx, refactor/xxx

## 禁止操作
- 不要修改 .env 文件
- 不要直接操作数据库
- 不要删除 migrations 文件
- 不要修改 CI/CD 配置（.github/ 目录）
- 不要在代码中硬编码密钥或敏感信息
```

### 1.3 用户级 CLAUDE.md 示例

```markdown
# 个人偏好

## 编码风格
- 优先使用函数式编程风格
- 注释用中文
- 优先使用 async/await 而非回调

## 交互偏好
- 修改前先说明原因
- 每次只改一个文件
- 用简短的中文解释改动

## 常用别名
- "测试" = pnpm test
- "构建" = pnpm build
- "检查" = pnpm lint && pnpm typecheck
```

### 1.4 路径特定规则

对于大型项目，可以在 `.claude/rules/` 目录下创建针对特定文件路径的规则：

**`.claude/rules/api-rules.md`**：
```yaml
---
paths:
  - "src/api/**/*.ts"
  - "src/routes/**/*.ts"
---
# API 层规则
- 所有端点必须有速率限制
- 响应必须包含 request_id
- 错误响应遵循 RFC 7807 格式
- 所有输入必须通过 Zod schema 验证
- 敏感数据字段必须在日志中脱敏
```

**`.claude/rules/test-rules.md`**：
```yaml
---
paths:
  - "**/*.test.ts"
  - "**/*.spec.ts"
---
# 测试规则
- 使用 describe/it 结构组织测试
- 每个 it 只测一个行为
- Mock 命名：mock + 被 Mock 的模块名
- 测试数据使用 factory 模式生成
```

> 💡 **路径特定规则只在相关文件被读取时加载**，不会消耗不必要的上下文。

### 1.5 自动记忆（Auto Memory）

Claude Code 会在工作过程中**自动学习**你的模式和偏好：

- 存储位置：`~/.claude/projects/<project>/memory/MEMORY.md`
- 每次会话自动加载前 200 行
- 可用 `/memory` 命令查看和编辑
- 记忆包含：你的偏好模式、项目特定知识、常见错误修复方式

### 1.6 CLAUDE.md 最佳实践

| 实践 | 说明 |
|:-----|:-----|
| **控制在 200 行以内** | 过长会降低 Claude 的遵循度 |
| **使用 Markdown 标题分组** | 清晰的结构提升理解 |
| **写可验证的具体指令** | "使用 2 空格缩进" ✅ vs "正确格式化代码" ❌ |
| **大型项目拆分到 rules/** | 路径特定规则减少上下文消耗 |
| **用 `@path` 引入外部文件** | 避免重复内容 |
| **定期审查和更新** | 移除过时规则，添加新发现 |

---

## 二、Hooks 钩子系统

> **官方文档**：https://code.claude.com/docs/en/hooks

Hooks 是 Claude Code 生命周期中**自动执行的用户定义命令**。它们在你的进程中运行，不消耗 Claude 的上下文。

### 2.1 Hook 类型

| 类型 | 说明 | 示例 |
|:-----|:-----|:-----|
| `command` | 执行 Shell 命令 | 运行 linter、阻止危险操作 |
| `http` | 发送 HTTP POST 到端点 | 通知 Slack、记录审计日志 |
| `prompt` | 向 Claude 发送提示词进行单轮评估 | 验证任务完成质量 |
| `agent` | 生成一个子代理进行验证 | 深度检查代码质量 |

### 2.2 完整事件列表

| 事件 | 触发时机 | 可阻止？ | 典型用途 |
|:-----|:---------|:--------:|:---------|
| `SessionStart` | 会话开始 | ❌ | 设置环境变量、加载配置 |
| `UserPromptSubmit` | 用户提交提示词后 | ✅ | 输入校验、敏感信息过滤 |
| `PreToolUse` | 工具执行前 | ✅ | 阻止危险命令、审计日志 |
| `PostToolUse` | 工具执行成功后 | ❌ | 自动运行测试、格式化代码 |
| `Stop` | Claude 完成响应时 | ✅ | 验证任务完成质量 |
| `TaskCompleted` | 任务标记完成时 | ✅ | 强制测试通过才允许完成 |
| `SubagentStart` | 子代理启动时 | ❌ | 监控子代理数量 |
| `SubagentStop` | 子代理结束时 | ❌ | 收集子代理结果 |
| `PreCompact` | 上下文压缩前 | ❌ | 存档完整对话记录 |
| `PostCompact` | 上下文压缩后 | ❌ | 记录压缩后的上下文大小 |

### 2.3 配置 Hooks

Hooks 在 `.claude/settings.json` 中配置：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-dangerous-commands.sh"
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/audit-file-changes.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run-tests-async.sh",
            "async": true,
            "timeout": 300
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review the conversation. Did Claude complete all requested tasks? Are there any errors or loose ends? Respond with JSON: {\"ok\": true} or {\"ok\": false, \"reason\": \"explanation\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 2.4 示例 1：阻止危险 Shell 命令

**`.claude/hooks/block-dangerous-commands.sh`**：

```bash
#!/bin/bash
# 从 stdin 读取 Hook 输入（JSON 格式）
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

# 定义危险模式
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "rm -rf ~"
    "rm -rf \$HOME"
    "sudo rm"
    "chmod 777"
    "curl .* | sh"
    "curl .* | bash"
    "wget .* | sh"
    "> /dev/sda"
    "mkfs"
    ":(){:|:&};:"  # Fork 炸弹
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qE "$pattern"; then
        # 输出 JSON 阻止执行
        jq -n '{
            hookSpecificOutput: {
                hookEventName: "PreToolUse",
                permissionDecision: "deny",
                permissionDecisionReason: "Blocked by security hook: potentially dangerous command"
            }
        }'
        exit 0
    fi
done

# 允许执行
exit 0
```

### 2.5 示例 2：文件修改后自动运行测试

**`.claude/hooks/run-tests-async.sh`**：

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# 仅对源代码文件运行测试
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.tsx && "$FILE_PATH" != *.js ]]; then
    exit 0
fi

# 异步运行测试
RESULT=$(npm test -- --reporter=dot 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "{\"systemMessage\": \"✅ Tests passed after editing $FILE_PATH\"}"
else
    # 将测试失败信息反馈给 Claude，让它自动修复
    TRUNCATED=$(echo "$RESULT" | tail -30)
    echo "{\"systemMessage\": \"❌ Tests FAILED after editing $FILE_PATH:\\n$TRUNCATED\\nPlease fix the failing tests.\"}"
fi
```

### 2.6 示例 3：审计所有文件变更到日志

**`.claude/hooks/audit-file-changes.sh`**：

```bash
#!/bin/bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# 写入审计日志
echo "[$TIMESTAMP] $TOOL_NAME: $FILE_PATH" >> .claude/audit.log

# 不阻止，允许继续
exit 0
```

### 2.7 示例 4：HTTP Hook — 通知 Slack

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX",
            "headers": {
                "Content-Type": "application/json"
            },
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### 2.8 示例 5：LLM 验证任务完成质量

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Analyze the conversation and determine if:\n1) All tasks from the original request are complete\n2) No errors need addressing\n3) No follow-up work is needed\n\nRespond with JSON:\n{\"ok\": true} to allow stopping\n{\"ok\": false, \"reason\": \"explanation\"} to continue working",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 2.9 Hook 最佳实践

| 实践 | 说明 |
|:-----|:-----|
| **脚本要轻量** | Hook 在关键路径上，过慢会影响体验 |
| **处理 stdin** | Hook 输入通过 stdin 以 JSON 传入 |
| **输出 JSON** | 阻止决策通过 stdout JSON 返回 |
| **异步执行长任务** | 测试等耗时操作用 `"async": true` |
| **设置超时** | 避免 Hook 卡死整个流程 |
| **错误处理** | Hook 脚本退出码非 0 不会阻止操作，只会记录 |
| **不要修改 Claude 上下文** | Hook 在进程外运行，无法直接影响对话 |

---

## 三、CI/CD 集成：GitHub Actions

> **官方文档**：https://code.claude.com/docs/en/github-actions

Claude Code 可以直接集成到 GitHub Actions 中，实现自动化代码审查、Issue 到 PR 转化等。

### 3.1 功能概览

| 功能 | 触发方式 | 说明 |
|:-----|:---------|:-----|
| **@claude 提及** | Issue/PR 评论中 @claude | 自动分析代码并回复 |
| **自动代码审查** | PR 创建/更新时 | 自动运行 Claude 审查 |
| **Issue → PR** | 在 Issue 中 @claude | 自动创建完整 PR |
| **自定义提示** | 配置 prompt 参数 | 定制审查规则 |

### 3.2 基础配置

**`.github/workflows/claude.yml`**：

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    # 仅当评论包含 @claude 时触发
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### 3.3 自动代码审查

**`.github/workflows/code-review.yml`**：

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this PR thoroughly. Focus on:
            1. Security vulnerabilities (injection, auth bypass, data exposure)
            2. Performance issues (N+1 queries, memory leaks, unnecessary computations)
            3. Code quality (DRY, SOLID, error handling)
            4. Test coverage gaps
            
            For each issue found, rate severity as Critical/Major/Minor.
            Post findings as review comments on specific lines.
          claude_args: "--max-turns 10"
```

### 3.4 Issue 自动处理

在 Issue 中评论 `@claude fix this`，Claude 会：
1. 读取 Issue 描述
2. 分析相关代码
3. 自动创建 PR 修复问题
4. 在 Issue 中回复进展

### 3.5 AWS Bedrock / Google Vertex AI 集成

企业场景可通过自己的云基础设施运行，实现数据驻留和计费控制：

```yaml
# AWS Bedrock 版本
- uses: anthropics/claude-code-action@v1
  with:
    github_token: ${{ steps.app-token.outputs.token }}
    use_bedrock: "true"
    claude_args: '--model us.anthropic.claude-sonnet-4-6 --max-turns 10'

# Google Vertex AI 版本
- uses: anthropics/claude-code-action@v1
  with:
    github_token: ${{ steps.app-token.outputs.token }}
    use_vertex: "true"
    claude_args: '--model claude-sonnet-4-6 --max-turns 10'
```

### 3.6 高级配置

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    
    # 自定义提示
    prompt: "Review focusing on our coding standards in CLAUDE.md"
    
    # Claude Code 参数
    claude_args: >
      --max-turns 15
      --model claude-sonnet-4-6
    
    # 允许的工具（安全限制）
    allowed_tools: "Read,Glob,Grep,Edit"
    
    # 项目 CLAUDE.md（自动加载）
    # Claude 会读取仓库中的 CLAUDE.md 和 .claude/rules/
```

### 3.7 Headless 模式

Claude Code 支持无交互的 Headless 模式，适用于 CI/CD 管道：

```bash
# 非交互式运行
claude --print --max-turns 10 "Review the latest changes for security issues"

# 输出 JSON 格式
claude --print --output-format json --max-turns 5 "Summarize the diff"

# 带超时
timeout 300 claude --print --max-turns 15 "Fix the failing tests"
```

---

## 四、自定义命令（Skills / Commands）

### 4.1 创建自定义命令

在 `.claude/commands/` 目录下创建 Markdown 文件：

**`.claude/commands/review-security.md`**：

```markdown
Review the current codebase for security vulnerabilities:

1. Check for SQL injection in all database queries
2. Verify authentication on all API endpoints  
3. Look for hardcoded secrets or API keys
4. Check for XSS vulnerabilities in frontend code
5. Verify CORS configuration
6. Check for insecure deserialization
7. Review file upload handling for path traversal

Output a summary table:
| Severity | File | Line | Issue | Recommendation |
```

使用时在 Claude Code 中输入 `/review-security`。

### 4.2 带参数的命令

**`.claude/commands/create-endpoint.md`**：

```markdown
Create a new REST API endpoint for the resource: $ARGUMENTS

Follow the project's architecture:
1. Add route handler in src/routes/
2. Add service logic in src/services/
3. Add Zod validation schema
4. Add unit tests
5. Update API documentation

Reference existing endpoints as examples.
```

使用：`/create-endpoint users`

### 4.3 代码生成命令

**`.claude/commands/scaffold-feature.md`**：

```markdown
Scaffold a new feature module: $ARGUMENTS

Create the following files:
- src/features/{name}/index.ts (barrel export)
- src/features/{name}/{name}.service.ts
- src/features/{name}/{name}.controller.ts
- src/features/{name}/{name}.model.ts
- src/features/{name}/{name}.validator.ts
- src/features/{name}/__tests__/{name}.test.ts

Follow existing feature modules as reference.
Include proper TypeScript types, error handling, and JSDoc.
```

### 4.4 团队共享命令 vs 个人命令

| 类型 | 位置 | 共享范围 |
|:-----|:-----|:---------|
| 项目命令 | `.claude/commands/` | 整个团队（提交到 Git） |
| 个人命令 | `~/.claude/commands/` | 仅自己 |

---

## 五、多 Agent 团队模式

Claude Code 支持在单个会话中生成多个 Agent 协作工作：

### 5.1 工作原理

```
主 Agent（你在对话中交互的）
  │
  ├── 生成 子 Agent A ── 分析 src/auth/ 目录
  │   └── 完成后返回分析报告给主 Agent
  │
  ├── 生成 子 Agent B ── 实现新功能
  │   └── 完成后返回修改清单给主 Agent
  │
  └── 主 Agent 汇总结果，继续工作
```

### 5.2 子 Agent 特点

- **独立上下文**：每个子 Agent 从新对话开始，不共享主 Agent 的完整历史
- **结果传递**：只有最终结果作为工具结果返回给主 Agent
- **上下文高效**：大幅减少主 Agent 的上下文消耗
- **并行可能**：某些场景下子 Agent 可以并行执行

---

## 六、权限与安全

### 6.1 Claude Code 权限系统

```
┌──────────────────────────────────────┐
│  需要批准的操作                        │
│  ├── 编辑文件                         │
│  ├── 创建新文件                       │
│  ├── 执行 Bash 命令                   │
│  └── 安装包（npm/pip）               │
├──────────────────────────────────────┤
│  不需要批准的操作                      │
│  ├── 读取文件                         │
│  ├── 搜索文件                         │
│  ├── 列出目录                         │
│  └── 网络搜索                         │
└──────────────────────────────────────┘
```

### 6.2 安全最佳实践

1. **为生产环境创建专用 CLAUDE.md**：明确列出禁止操作
2. **使用 PreToolUse Hook**：自动阻止危险命令
3. **CI/CD 中限制工具集**：只开放必要工具
4. **审计日志**：使用 PostToolUse Hook 记录所有操作
5. **在容器中运行**：CI/CD 环境使用 Docker 隔离

---

## 七、高级配置与调优

### 7.1 `.claude/settings.json` 完整配置

```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "Stop": [...]
  },
  "permissions": {
    "allow": [
      "Read", "Glob", "Grep"
    ],
    "deny": [
      "WebFetch"  
    ]
  },
  "model": "claude-sonnet-4-6",
  "maxTurns": 30
}
```

### 7.2 性能调优

| 配置 | 说明 | 推荐值 |
|:-----|:-----|:-------|
| CLAUDE.md 长度 | 过长降低遵循度 | < 200 行 |
| 规则拆分 | 路径特定规则减少加载 | 用 `.claude/rules/` |
| 工具数量 | 过多工具降低选择准确性 | 控制在 15 个以内 |
| 子 Agent | 大任务拆分降低上下文压力 | 复杂任务使用 |
| effort 级别 | 简单任务用低，复杂用高 | 按需调整 |

---

## 练习题

### 基础练习

1. **创建项目 CLAUDE.md**：为你当前的项目编写一份完整的 CLAUDE.md，包含架构说明、编码标准、测试要求和禁止操作。

2. **创建 3 个自定义命令**：在 `.claude/commands/` 中创建：
   - `/review`：代码审查命令
   - `/test`：生成测试命令
   - `/doc`：生成文档命令

### 中级练习

3. **实现安全 Hook 系统**：
   - PreToolUse Hook：阻止 `rm -rf`、`sudo` 等危险命令
   - PostToolUse Hook：所有文件修改后自动运行 linter
   - Stop Hook：用 prompt 类型验证任务完成质量

4. **配置 GitHub Actions**：为你的项目添加 Claude Code 自动代码审查。

### 高级练习

5. **完整 Hook 管道**：实现一个包含审计日志、安全检查、自动测试、Slack 通知的完整 Hook 管道。

6. **路径特定规则**：为一个多模块项目创建至少 4 个路径特定规则文件，覆盖 API 层、数据层、测试层和前端层。

---

> **下一步**：[11_Streaming与多模态深度.md](11_Streaming与多模态深度.md) — 流式传输 + Vision + PDF + Citations
