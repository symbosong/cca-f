# 模块 6：Claude Code 与 Computer Use

> **对应课程**：Building with the Claude API — Module 6: Claude Code & Computer Use  
> **视频数量**：8 个（约 34 分钟）  
> **预计学习时间**：1-2 小时  
> **难度**：⭐⭐

### 📌 原课程地址

| 平台 | 链接 |
|------|------|
| **Skilljar（官方）** | https://anthropic.skilljar.com/claude-with-the-anthropic-api |
| **Coursera（镜像）** | https://www.coursera.org/learn/building-with-the-claude-api |

### 📌 视频课时清单

| # | 视频标题 | 时长 | 核心知识点 |
|:-:|---------|:----:|-----------|
| 1 | Anthropic Applications | 1m | Anthropic 产品矩阵概览 |
| 2 | Claude Code Setup | 2m | 安装配置、首次运行 |
| 3 | Claude Code in Action | 10m | 核心演示：代码理解、生成、重构、调试 |
| 4 | Enhancements with MCP Servers | 3m | 给 Claude Code 接入 MCP 服务器扩展能力 |
| 5 | Parallelizing Claude Code | 8m | 并行子代理、同时执行多个任务 |
| 6 | Automated Debugging | 4m | 自动调试：读取错误→分析→修复→验证 |
| 7 | Computer Use | 3m | Computer Use 概念：像人一样操作桌面 |
| 8 | How to Use Computer Use | 3m | 工作原理：截图→坐标→动作循环 |

> **阅读材料**（2 篇，10 分钟）：Module Introduction / Next Steps

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

## 第 1 课：Anthropic 产品矩阵

> 📹 视频：Anthropic Applications（1 min）

Anthropic 产品概览：
- **Claude.ai** — 对话界面
- **Claude Code** — 命令行 AI 编程助手
- **Claude API** — 开发者接口
- **Computer Use** — 桌面操控

---

## 第 2 课：Claude Code 安装配置

> 📹 视频：Claude Code Setup（2 min）

```bash
# 安装 Claude Code（需要 Node.js 18+）
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version

# 在项目目录中启动
cd /path/to/your/project
claude

# 常用启动选项
claude --model claude-sonnet-4-20250514  # 指定模型
claude --verbose                         # 详细输出
```

---

## 第 3 课：Claude Code 实战演示

> 📹 视频：Claude Code in Action（10 min）

### 核心能力

- 🔍 **理解代码库**：浏览文件、搜索代码、理解项目结构
- ✏️ **编辑代码**：直接创建、修改、删除文件
- 🖥️ **执行命令**：运行 shell 命令、测试、构建
- 🔄 **Git 操作**：提交、创建 PR、解决冲突

### 日常使用场景

```bash
claude "这个项目的架构是什么？"
claude "给 User 模型添加一个邮箱验证功能"
claude "这个测试失败了，帮我修复"
claude "审查 src/auth/ 目录下的代码，关注安全问题"
claude "提交当前更改，写一个好的 commit message"
```

### 斜杠命令

| 命令 | 功能 |
|------|------|
| `/help` | 查看帮助 |
| `/clear` | 清除对话上下文 |
| `/compact` | 压缩对话历史 |
| `/model` | 切换模型 |
| `/cost` | 查看 token 费用 |
| `/mcp` | 管理 MCP Server |

---

## 第 4 课：MCP 增强

> 📹 视频：Enhancements with MCP Servers（3 min）

### 给 Claude Code 接入 MCP 服务器

```bash
claude mcp add github -- npx -y @modelcontextprotocol/server-github
claude mcp add db -- npx -y @modelcontextprotocol/server-postgres postgresql://...
claude mcp list
```

接入后 Claude Code 可以直接查询数据库、操作 GitHub 等。

---

## 第 5 课：并行子代理

> 📹 视频：Parallelizing Claude Code（8 min）

### 让 Claude Code 同时执行多个任务

子代理（sub-agents）概念：Claude Code 可以启动多个并行任务分别处理不同问题，然后汇总结果。显著提升处理复杂任务的效率。

---

## 第 6 课：自动调试

> 📹 视频：Automated Debugging（4 min）

### Claude Code 的自动调试循环

```
读取错误信息 → 分析原因 → 自动修复代码 → 运行测试验证 → 如仍失败则继续迭代
```

---

## 第 7 课：Computer Use 概念

> 📹 视频：Computer Use（3 min）

### 什么是 Computer Use？

Computer Use 让 Claude 通过**截屏 + 鼠标/键盘操作**来控制桌面应用——就像远程控制一样。

```
用户请求 → Claude 截屏查看桌面 → 决定操作 → 点击/输入 → 再截屏验证 → 继续...
```

---

## 第 8 课：Computer Use 工作原理

> 📹 视频：How to Use Computer Use（3 min）

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

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=[
        {
            "type": "computer_20250124",
            "name": "computer",
            "display_width_px": 1920,
            "display_height_px": 1080,
            "display_number": 0
        },
        {"type": "bash_20250124", "name": "bash"},
        {"type": "text_editor_20250124", "name": "text_editor"}
    ],
    messages=[{
        "role": "user",
        "content": "Open Firefox and search for 'Claude AI' on Google."
    }]
)
```

### 安全考虑

> ⚠️ **Computer Use 仍处于 Beta 阶段**：

1. **在沙箱环境运行**：使用虚拟机或 Docker 容器
2. **限制网络访问**：避免 Claude 访问敏感系统
3. **人工监督**：始终监控 Claude 的操作
4. **避免敏感信息**：不要在可见屏幕上显示密码

```bash
# 推荐：使用 Docker 运行（官方 Demo）
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your-key \
  ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo
```

---

## 补充：CLAUDE.md 配置系统

CLAUDE.md 是 Claude Code 的"项目记忆"。

### 三级配置层次

```
优先级从高到低：
1. ~/.claude/CLAUDE.md          ← 全局配置
2. /project/CLAUDE.md            ← 项目级
3. /project/src/CLAUDE.md        ← 模块级
```

### CLAUDE.md 示例

```markdown
# Project: E-commerce API

## Tech Stack
- Python 3.11 + FastAPI
- PostgreSQL 15 with SQLAlchemy 2.0

## Code Conventions
- Use type hints everywhere
- All database queries must use parameterized queries

## Testing
- Run tests: `pytest tests/ -v`
- Minimum coverage: 80%
```

---

## 补充：Hooks 系统

Hooks 在 Claude Code 的关键节点插入自定义逻辑：

| Hook | 触发时机 | 用途 |
|------|---------|------|
| `PreToolUse` | 工具执行前 | 审批、拦截危险操作 |
| `PostToolUse` | 工具执行后 | 日志、自动格式化 |
| `Notification` | 发出通知时 | 自定义通知方式 |
| `Stop` | 停止时 | 自动运行测试 |

```json
{
  "hooks": {
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
    ]
  }
}
```

---

## 补充：CI/CD 集成

```yaml
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
          claude --print "Review the changes in this PR." < <(git diff origin/main...HEAD)
```

---

## 练习题

### 练习 1：Claude Code 上手

安装 Claude Code，创建 CLAUDE.md，用它完成一个小功能。

### 练习 2：Hooks 配置

配置 PostToolUse Hook 自动格式化代码 + Stop Hook 自动运行测试。

### 练习 3：了解 Computer Use

运行官方 Computer Use Demo 容器，体验 Claude 操控桌面。

---

## 扩展阅读

| 资源 | 链接 |
|------|------|
| Claude Code 官方文档 | https://docs.anthropic.com/en/docs/claude-code |
| Claude Code GitHub | https://github.com/anthropics/claude-code |
| Claude Code Hooks | https://docs.anthropic.com/en/docs/claude-code/hooks |
| CLAUDE.md 配置 | https://docs.anthropic.com/en/docs/claude-code/memory |
| Computer Use 文档 | https://docs.anthropic.com/en/docs/build-with-claude/computer-use |

---

> **下一模块**：[07_Agent工作流与智能体.md](07_Agent工作流与智能体.md) — 学习 Agent 循环和工作流模式
