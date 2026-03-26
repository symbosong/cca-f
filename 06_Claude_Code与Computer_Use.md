# 模块 6：Claude Code 与 Computer Use

> **对应课程**：Building with the Claude API — Module 6: Claude Code & Computer Use  
> **视频数量**：8 个（约 34 分钟）  
> **预计学习时间**：1-2 小时  
> **难度**：⭐⭐

---

## 本模块学习目标

完成本模块后，你将能够：
1. 理解 Claude Code 是什么以及它的核心能力
2. 安装和配置 Claude Code
3. 掌握 Claude Code 的日常工作流
4. 了解 CLAUDE.md 配置文件系统
5. 使用 Hooks 自定义 Claude Code 的行为
6. 理解 Computer Use（桌面操控）的概念和应用

---

## 第一部分：Claude Code

### 第 1 节：什么是 Claude Code？

Claude Code 是 Anthropic 推出的**命令行 AI 编程助手**。它直接在终端中运行，能够：

- 🔍 **理解代码库**：浏览文件、搜索代码、理解项目结构
- ✏️ **编辑代码**：直接创建、修改、删除文件
- 🖥️ **执行命令**：运行 shell 命令、测试、构建
- 🔄 **Git 操作**：提交、创建 PR、解决冲突
- 🤔 **推理规划**：分析问题、制定方案、执行复杂任务

### 第 2 节：安装和配置

```bash
# 安装 Claude Code（需要 Node.js 18+）
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version

# 启动 Claude Code（在项目目录中）
cd /path/to/your/project
claude

# 常用启动选项
claude --model claude-sonnet-4-20250514  # 指定模型
claude --verbose                         # 详细输出
claude --dangerously-skip-permissions    # 跳过权限确认（慎用）
```

### 第 3 节：核心功能

#### 日常使用场景

```bash
# 理解代码库
claude "这个项目的架构是什么？主要用了哪些技术栈？"

# 实现功能
claude "给 User 模型添加一个邮箱验证功能"

# 修复 Bug
claude "这个测试失败了，帮我修复：[粘贴错误信息]"

# 代码审查
claude "审查 src/auth/ 目录下的代码，关注安全问题"

# 重构
claude "将 utils.js 中的函数拆分成独立模块"

# Git 操作
claude "提交当前更改，写一个好的 commit message"
claude "创建一个 PR，描述我做了什么改动"
```

#### 斜杠命令

在 Claude Code 交互界面中，可以使用斜杠命令：

| 命令 | 功能 |
|------|------|
| `/help` | 查看帮助 |
| `/clear` | 清除对话上下文 |
| `/compact` | 压缩对话历史（减少 token 使用） |
| `/model` | 切换模型 |
| `/cost` | 查看当前会话的 token 费用 |
| `/permissions` | 查看和管理权限设置 |
| `/mcp` | 管理 MCP Server |
| `/bug` | 报告 Bug |

### 第 4 节：CLAUDE.md 配置系统

CLAUDE.md 是 Claude Code 的"项目记忆"——它告诉 Claude 关于你项目的重要信息。

#### 三级配置层次

```
优先级从高到低：
1. ~/.claude/CLAUDE.md          ← 全局配置（所有项目通用）
2. /project/CLAUDE.md            ← 项目根目录（项目级）
3. /project/src/CLAUDE.md        ← 子目录（模块级，可选）
```

#### CLAUDE.md 示例

```markdown
# Project: E-commerce API

## Tech Stack
- Python 3.11 + FastAPI
- PostgreSQL 15 with SQLAlchemy 2.0
- Redis for caching
- Docker for deployment

## Project Structure
```
src/
├── api/          # FastAPI routes
├── models/       # SQLAlchemy models
├── services/     # Business logic
├── schemas/      # Pydantic schemas
└── utils/        # Helper functions
```

## Code Conventions
- Use type hints everywhere
- Follow Google Python Style Guide
- All API endpoints must have OpenAPI docs
- Use async/await for all database operations

## Testing
- Run tests: `pytest tests/ -v`
- Minimum coverage: 80%
- Use fixtures from `tests/conftest.py`

## Important Notes
- NEVER hardcode credentials — use environment variables
- All database queries must use parameterized queries
- The /admin endpoints require JWT authentication
```

### 第 5 节：Hooks 系统

Hooks 让你在 Claude Code 的关键节点插入自定义逻辑：

#### Hook 类型

| Hook | 触发时机 | 用途 |
|------|---------|------|
| `PreToolUse` | 工具执行**前** | 审批、拦截危险操作 |
| `PostToolUse` | 工具执行**后** | 日志、自动格式化 |
| `Notification` | Claude Code 发出通知时 | 自定义通知方式 |
| `Stop` | Claude Code 停止时 | 自动运行测试、提交 |

#### 配置 Hooks

在 `.claude/settings.json` 中配置：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "write_file",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'About to write file: $CLAUDE_FILE_PATH'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "write_file",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $CLAUDE_FILE_PATH 2>/dev/null || true"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "npm test 2>&1 | tail -20"
          }
        ]
      }
    ]
  }
}
```

#### Hook 实用示例

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "write_file",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ $CLAUDE_FILE_PATH == *.py ]]; then ruff format $CLAUDE_FILE_PATH && ruff check --fix $CLAUDE_FILE_PATH; fi"
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"$CLAUDE_NOTIFICATION\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### 第 6 节：Claude Code 最佳实践

#### 高效使用技巧

1. **写好 CLAUDE.md**：项目越复杂，CLAUDE.md 越重要
2. **给出上下文**：告诉 Claude 你想做什么、为什么这样做
3. **使用 `/compact`**：长对话中定期压缩历史，减少 token 消耗
4. **先理解再修改**：让 Claude 先解释代码，确认理解后再修改
5. **小步迭代**：复杂任务分步进行，每步确认后再继续

#### CI/CD 集成

```bash
# 在 GitHub Actions 中使用 Claude Code
# .github/workflows/ai-review.yml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code
      - name: Run AI Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --print "Review the changes in this PR. Focus on bugs, security issues, and code quality. The diff is:" < <(git diff origin/main...HEAD)
```

---

## 第二部分：Computer Use（桌面操控）

### 什么是 Computer Use？

Computer Use 让 Claude 通过**截屏 + 鼠标/键盘操作**来控制桌面应用——就像远程控制一样。

```
用户请求 → Claude 截屏查看桌面 → Claude 决定操作 → 移动鼠标/点击/输入 → 再截屏验证 → 继续...
```

### 核心工具

| 工具 | 功能 |
|------|------|
| `computer` | 截屏、移动鼠标、点击、输入文字、滚动 |
| `text_editor` | 查看和编辑文件 |
| `bash` | 执行 bash 命令 |

### API 示例

```python
import anthropic

client = anthropic.Anthropic()

# Computer Use 请求
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=[
        {
            "type": "computer_20250124",  # 特殊的内置工具类型
            "name": "computer",
            "display_width_px": 1920,
            "display_height_px": 1080,
            "display_number": 0
        },
        {
            "type": "bash_20250124",
            "name": "bash"
        },
        {
            "type": "text_editor_20250124",
            "name": "text_editor"
        }
    ],
    messages=[{
        "role": "user",
        "content": "Open Firefox and search for 'Claude AI' on Google."
    }]
)

# Claude 会返回 tool_use 请求，包含截屏和操作指令
for block in response.content:
    if block.type == "tool_use":
        print(f"工具: {block.name}")
        print(f"操作: {block.input}")
        # 例如: {"action": "screenshot"} 或 {"action": "click", "coordinate": [500, 300]}
```

### Computer Use 的工作流程

```
1. Claude 先截屏查看当前屏幕
2. 分析截屏，确定要点击/输入的位置
3. 执行操作（点击、输入文字等）
4. 再次截屏验证操作结果
5. 重复上述过程直到任务完成
```

### 适用场景

| ✅ 适合 | ❌ 不适合 |
|---------|---------|
| 自动化测试（UI 测试） | 高安全要求的操作 |
| 填写表单 | 需要人类判断的决策 |
| 网页浏览和数据采集 | 处理敏感信息 |
| 桌面应用操作自动化 | 实时系统操作 |
| 演示和教程录制 | 生产环境无人值守操作 |

### 安全考虑

> ⚠️ **Computer Use 仍处于 Beta 阶段**，使用时注意：

1. **在沙箱环境运行**：使用虚拟机或 Docker 容器
2. **限制网络访问**：避免 Claude 访问敏感系统
3. **人工监督**：始终监控 Claude 的操作
4. **避免敏感信息**：不要在 Claude 可见的屏幕上显示密码等

```bash
# 推荐：使用 Docker 运行 Computer Use（官方 Demo）
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your-key \
  ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo
```

---

## 练习题

### 练习 1：Claude Code 上手

1. 安装 Claude Code
2. 在你的项目中创建 CLAUDE.md
3. 使用 Claude Code 完成一个小功能（如添加一个 API endpoint）

### 练习 2：Hooks 配置

为你的项目配置：
1. `PostToolUse` Hook：自动格式化代码
2. `Stop` Hook：自动运行测试

### 练习 3：了解 Computer Use

阅读 [Computer Use 文档](https://docs.anthropic.com/en/docs/build-with-claude/computer-use)，运行官方 Demo 容器，体验 Claude 操控桌面。

---

## 扩展阅读

| 资源 | 链接 |
|------|------|
| Claude Code 官方文档 | https://docs.anthropic.com/en/docs/claude-code |
| Claude Code GitHub | https://github.com/anthropics/claude-code |
| Claude Code Hooks | https://docs.anthropic.com/en/docs/claude-code/hooks |
| CLAUDE.md 配置指南 | https://docs.anthropic.com/en/docs/claude-code/memory |
| Computer Use 文档 | https://docs.anthropic.com/en/docs/build-with-claude/computer-use |
| Computer Use Demo | https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo |

---

> **下一模块**：[07_Agent工作流与智能体.md](07_Agent工作流与智能体.md) — 学习 Agent 循环和工作流模式
