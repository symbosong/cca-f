# 模块 4：MCP 模型上下文协议

> **对应课程**：Building with the Claude API — Module 5: Model Context Protocol (MCP)  
> **视频数量**：10 个（约 53 分钟）  
> **GitHub Notebook**：无（本模块以概念和动手实操为主）  
> **预计学习时间**：2 小时  
> **难度**：⭐⭐

### 📌 原课程地址

| 平台 | 链接 |
|------|------|
| **Skilljar（官方）** | https://anthropic.skilljar.com/claude-with-the-anthropic-api |
| **Coursera（镜像）** | https://www.coursera.org/learn/building-with-the-claude-api |

### 📌 视频课时清单

| # | 视频标题 | 时长 | 核心知识点 |
|:-:|---------|:----:|-----------|
| 1 | Introduction to MCP | 5m | MCP 概念、USB 类比、N×M → N+M 问题 |
| 2 | MCP Clients | 5m | 客户端概念、Claude Desktop/Code 都是 MCP 客户端 |
| 3 | Project Setup | 3m | 安装 MCP SDK、项目结构、配置文件 |
| 4 | Server Inspector | 4m | MCP Inspector 调试工具、查看暴露的工具/资源/提示 |
| 5 | Implementing a Client | 7m | 编写 MCP 客户端、发现和调用工具 |
| 6 | Defining Resources | 10m | 资源定义、为 Claude 提供上下文数据 |
| 7 | Fetching Resources | 5m | 客户端读取资源、URI 模板和参数化 |
| 8 | Defining Prompts | 8m | 预定义提示模板、@mcp.prompt() 装饰器 |
| 9 | Prompts in the Client | 3m | 客户端使用提示模板 |
| 10 | MCP Review | 4m | 全模块总结、与直接工具调用对比 |

> **阅读材料**（3 篇，25 分钟）：Module Introduction / Defining Tools with MCP / Next Steps

---

## 本模块学习目标

完成本模块后，你将能够：
1. 理解 MCP 是什么、为什么需要它
2. 掌握 MCP 的架构和核心概念
3. 了解 MCP 的三大核心能力：Tools、Resources、Prompts
4. 搭建和配置 MCP Server
5. 在 Claude Desktop 和 Claude Code 中使用 MCP
6. 理解 MCP 在 API 中的使用方式
7. 了解 MCP 生态和社区 Server

---

## 第 1 课：MCP 概览

> 📹 视频：Introduction to MCP（5 min）

### 什么是 MCP？

**Model Context Protocol（模型上下文协议）** 是 Anthropic 发起的一个**开放标准**，目的是标准化 AI 模型与外部数据源和工具的连接方式。

类比理解：**USB 之于外设** → **MCP 之于 AI 工具集成**

```
传统方式（N×M 问题）：
  3个AI × 3个工具 = 9 个集成

MCP 方式（N+M 问题）：
  3个AI + 3个工具 = 6 个集成
```

### MCP 的三大核心原语

| 原语 | 作用 | 类比 |
|------|------|------|
| **Tools** | 让 AI 调用外部函数 | API 接口 |
| **Resources** | 让 AI 读取外部数据 | 数据库/文件 |
| **Prompts** | 预定义的提示模板 | 操作手册 |

---

## 第 2 课：MCP 客户端

> 📹 视频：MCP Clients（5 min）

### 架构：Host → Client → Server

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│   MCP Host     │     │   MCP Client   │     │   MCP Server   │
│ (如 Claude     │────▶│ (协议实现层)    │────▶│ (工具提供方)    │
│  Desktop)      │     │               │     │               │
└────────────────┘     └────────────────┘     └────────────────┘
```

| 组件 | 角色 | 示例 |
|------|------|------|
| **Host** | 运行 AI 的应用程序 | Claude Desktop、Claude Code、VS Code |
| **Client** | 管理与 Server 的连接 | 通常由 Host 内置 |
| **Server** | 提供工具、数据、提示模板 | GitHub Server、Filesystem Server |

### 传输方式

| 方式 | 使用场景 | 说明 |
|------|---------|------|
| **stdio** | 本地 Server | Server 作为子进程运行，通过 stdin/stdout 通信 |
| **SSE** | 远程 Server | 通过 HTTP 连接远程 Server |

---

## 第 3 课：项目搭建

> 📹 视频：Project Setup（3 min）

### 安装 MCP SDK

```bash
# Python SDK
pip install mcp

# TypeScript SDK
npm install @modelcontextprotocol/sdk
```

---

## 第 4 课：Server Inspector

> 📹 视频：Server Inspector（4 min）

### MCP Inspector：调试 MCP 服务器的可视化工具

Inspector 让你可以直观地查看 MCP Server 暴露的所有工具、资源和提示模板，方便开发调试。

---

## 第 5 课：实现客户端

> 📹 视频：Implementing a Client（7 min）

### 编写 MCP 客户端

连接服务器、发现工具、调用工具：

```python
# 客户端核心操作
# session.list_tools()    — 发现可用工具
# session.call_tool()     — 调用工具
```

---

## 第 6 课：定义资源

> 📹 视频：Defining Resources（10 min）

### Resources：为 Claude 提供上下文数据

```python
from mcp.server import Server

server = Server("my-server")

@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="db://users/schema",
            name="Users Table Schema",
            description="Database schema for the users table",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri == "db://users/schema":
        schema = await db.get_schema("users")
        return json.dumps(schema)
```

---

## 第 7 课：读取资源

> 📹 视频：Fetching Resources（5 min）

### 客户端读取资源

```python
# session.list_resources()           — 发现可用资源
# session.read_resource("uri://...")  — 读取资源内容
```

资源支持 URI 模板和参数化。

---

## 第 8 课：定义提示模板

> 📹 视频：Defining Prompts（8 min）

### Prompts：预定义的交互模式

```python
@server.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="code_review",
            description="Review code for bugs and best practices",
            arguments=[
                PromptArgument(name="code", description="The code to review", required=True),
                PromptArgument(name="language", description="Programming language", required=False)
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    if name == "code_review":
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Please review this {arguments.get('language', '')} code:\n\n{arguments['code']}"
                    )
                )
            ]
        )
```

---

## 第 9 课：客户端使用提示

> 📹 视频：Prompts in the Client（3 min）

### 将模板实例化为消息

```python
# session.list_prompts()                           — 发现可用提示模板
# session.get_prompt("code_review", {"code": ...}) — 获取实例化的消息
```

---

## 第 10 课：MCP 总结

> 📹 视频：MCP Review（4 min）

### MCP vs 直接工具调用

| 特性 | 直接 Tool Use (API) | MCP |
|------|---------------------|-----|
| 适用场景 | 自定义应用中嵌入 Claude | 标准化工具生态 |
| 工具定义方式 | 每次请求带 `tools` 参数 | Server 端统一注册 |
| 工具执行 | 你自己写代码执行 | Server 端自动执行 |
| 跨模型兼容 | 仅 Claude | 任何支持 MCP 的模型 |
| 额外能力 | 仅工具调用 | 工具 + 资源 + 提示模板 |

**什么时候用哪个？**
- **构建自己的应用** → 用 API Tool Use
- **增强 Claude Desktop/Code 的能力** → 用 MCP
- **构建可复用的工具服务** → 用 MCP Server
- **两者可以共存**

---

## 补充：完整 MCP Server 示例

### Python SDK

```python
# server.py — 天气 MCP Server
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("weather-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a city.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather":
        weather_data = {"city": arguments["city"], "temperature": "22°C", "conditions": "Sunny"}
        return [TextContent(type="text", text=json.dumps(weather_data, indent=2))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 在 Claude Desktop 中配置

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/weather_server.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Documents"]
    }
  }
}
```

### 在 Claude Code 中配置

```bash
claude mcp add weather -- python /path/to/weather_server.py
claude mcp list
claude mcp remove weather
```

---

## 补充：常用 MCP Server

| Server | 功能 | 安装命令 |
|--------|------|---------|
| **Filesystem** | 读写本地文件 | `npx @modelcontextprotocol/server-filesystem` |
| **GitHub** | 操作 GitHub 仓库 | `npx @modelcontextprotocol/server-github` |
| **Brave Search** | 网页搜索 | `npx @modelcontextprotocol/server-brave-search` |
| **PostgreSQL** | PostgreSQL 数据库 | `npx @modelcontextprotocol/server-postgres` |
| **Memory** | 持久化知识图谱 | `npx @modelcontextprotocol/server-memory` |

**发现更多**：[MCP Server 目录](https://github.com/modelcontextprotocol/servers) / [Smithery 社区市场](https://smithery.ai/)

---

## 补充：MCP 安全最佳实践

1. **最小权限原则**：只给 MCP Server 必要的权限
2. **审查 Server 代码**：使用社区 Server 前检查其源码
3. **环境变量管理**：不要在配置文件中硬编码敏感信息
4. **网络隔离**：远程 MCP Server 应使用 HTTPS
5. **日志监控**：在生产环境中记录所有工具调用

---

## 练习题

### 练习 1：搭建 MCP Server

用 Python 构建一个 MCP Server，提供待办事项管理工具（get_todos / add_todo / complete_todo）。

### 练习 2：使用社区 Server

安装 Filesystem 和 GitHub Server，在 Claude Desktop 中测试。

### 练习 3：资源与提示模板

扩展练习 1 的 Server，添加一个 Resource（返回统计信息）和一个 Prompt 模板（生成日报）。

---

## 扩展阅读

| 资源 | 链接 |
|------|------|
| MCP 官方文档 | https://modelcontextprotocol.io/ |
| MCP 规范 | https://github.com/modelcontextprotocol/specification |
| Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk |
| 官方 Server 集合 | https://github.com/modelcontextprotocol/servers |
| Anthropic MCP 文档 | https://docs.anthropic.com/en/docs/agents-and-tools/mcp |

---

> **下一模块**：[05_RAG检索增强生成.md](05_RAG检索增强生成.md) — 学习如何让 Claude 基于你的数据生成精准回答
