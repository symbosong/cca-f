# 模块 4：MCP 模型上下文协议

> **对应课程**：Building with the Claude API — Module 4: Model Context Protocol  
> **视频数量**：10 个（约 53 分钟）  
> **GitHub Notebook**：无（本模块以概念和动手实操为主）  
> **预计学习时间**：2 小时  
> **难度**：⭐⭐

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

## 第一节：MCP 概览

### 1.1 什么是 MCP？

**Model Context Protocol（模型上下文协议）** 是 Anthropic 发起的一个**开放标准**，目的是标准化 AI 模型与外部数据源和工具的连接方式。

类比理解：
- **USB 之于外设** → **MCP 之于 AI 工具集成**
- 没有 USB 之前，每个外设都需要专门的接口。没有 MCP 之前，每个 AI 工具集成都需要定制开发。

```
传统方式（N×M 问题）：
┌─────────┐     ┌───────────┐
│ Claude   │────▶│ GitHub API│  每个 AI × 每个工具 = 独立集成
│ GPT      │────▶│ Slack API │
│ Gemini   │────▶│ DB Query  │
└─────────┘     └───────────┘
  3个AI × 3个工具 = 9 个集成

MCP 方式（N+M 问题）：
┌─────────┐     ┌─────────┐     ┌───────────┐
│ Claude   │     │         │     │ GitHub    │
│ GPT      │────▶│  MCP    │────▶│ Slack     │
│ Gemini   │     │         │     │ DB Query  │
└─────────┘     └─────────┘     └───────────┘
  3个AI + 3个工具 = 6 个集成
```

### 1.2 MCP 的架构

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
| **Server** | 提供工具、数据、提示模板 | GitHub Server、Filesystem Server、Slack Server |

### 1.3 传输方式

MCP 支持两种传输方式：

| 方式 | 使用场景 | 说明 |
|------|---------|------|
| **stdio**（标准输入/输出） | 本地 Server | Server 作为子进程运行，通过 stdin/stdout 通信 |
| **SSE**（Server-Sent Events） | 远程 Server | 通过 HTTP 连接远程 Server |

---

## 第二节：MCP 的三大核心能力

### 2.1 Tools（工具）

让 AI 调用外部函数——与 Claude API 的 Tool Use 类似，但通过 MCP 标准化：

```python
# MCP Server 端定义工具
from mcp.server import Server
from mcp.types import Tool

server = Server("my-tools-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_database",
            description="Search the company database for records",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max number of results",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_database":
        # 实际执行数据库查询
        results = await db.search(arguments["query"], arguments.get("limit", 10))
        return results
```

### 2.2 Resources（资源）

让 AI 读取外部数据源——类似于给 AI 提供参考资料：

```python
@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="file:///data/company-handbook.pdf",
            name="Company Handbook",
            description="The company's employee handbook (2024 edition)",
            mimeType="application/pdf"
        ),
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

### 2.3 Prompts（提示模板）

预定义的提示模板，用户可以在 MCP Host 中选择使用：

```python
@server.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="code_review",
            description="Review code for bugs and best practices",
            arguments=[
                PromptArgument(
                    name="code",
                    description="The code to review",
                    required=True
                ),
                PromptArgument(
                    name="language",
                    description="Programming language",
                    required=False
                )
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
                        text=f"Please review this {arguments.get('language', '')} code:\n\n{arguments['code']}\n\nFocus on bugs, security issues, and best practices."
                    )
                )
            ]
        )
```

---

## 第三节：构建 MCP Server

### 3.1 使用 Python SDK 构建

```bash
# 安装 MCP Python SDK
pip install mcp
```

#### 完整的 MCP Server 示例

```python
# server.py — 一个简单的天气 MCP Server
import json
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 创建 Server 实例
server = Server("weather-server")

# 注册工具列表
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a city. Returns temperature, conditions, and humidity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g. 'London' or 'Tokyo'"
                    }
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="get_forecast",
            description="Get 5-day weather forecast for a city.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["city"]
            }
        )
    ]

# 实现工具调用
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather":
        city = arguments["city"]
        # 调用真实的天气 API（这里用模拟数据）
        weather_data = {
            "city": city,
            "temperature": "22°C",
            "conditions": "Partly Cloudy",
            "humidity": "65%"
        }
        return [TextContent(type="text", text=json.dumps(weather_data, indent=2))]
    
    elif name == "get_forecast":
        city = arguments["city"]
        forecast = {
            "city": city,
            "forecast": [
                {"day": "Monday", "temp": "22°C", "conditions": "Sunny"},
                {"day": "Tuesday", "temp": "20°C", "conditions": "Cloudy"},
                {"day": "Wednesday", "temp": "18°C", "conditions": "Rain"},
            ]
        }
        return [TextContent(type="text", text=json.dumps(forecast, indent=2))]

# 启动 Server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 3.2 使用 TypeScript SDK 构建

```bash
# 安装 MCP TypeScript SDK
npm install @modelcontextprotocol/sdk
```

```typescript
// server.ts
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

// 定义工具
server.tool(
  "search_files",
  "Search for files by name pattern in the workspace",
  {
    pattern: z.string().describe("File name pattern (glob syntax)"),
    directory: z.string().optional().describe("Directory to search in"),
  },
  async ({ pattern, directory }) => {
    // 实际的文件搜索逻辑
    const results = await searchFiles(pattern, directory || ".");
    return {
      content: [
        { type: "text", text: JSON.stringify(results, null, 2) },
      ],
    };
  }
);

// 定义资源
server.resource(
  "config",
  "config://app",
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        text: JSON.stringify(getAppConfig()),
        mimeType: "application/json",
      },
    ],
  })
);

// 启动
const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## 第四节：在客户端中使用 MCP

### 4.1 Claude Desktop 配置

编辑 Claude Desktop 配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/weather_server.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Documents"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-github-token"
      }
    }
  }
}
```

### 4.2 Claude Code 配置

在 Claude Code 中使用 MCP：

```bash
# 添加 MCP Server
claude mcp add weather -- python /path/to/weather_server.py

# 列出已配置的 MCP Server
claude mcp list

# 从 Smithery 仓库安装社区 Server
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# 移除 MCP Server
claude mcp remove weather
```

### 4.3 在 API 中使用 MCP

通过 API 直接连接 MCP Server：

```python
import anthropic

client = anthropic.Anthropic()

# 在 API 中使用 MCP
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    mcp_servers=[
        {
            "type": "url",
            "url": "https://my-mcp-server.example.com/sse",
            "name": "my-server"
        }
    ],
    messages=[
        {"role": "user", "content": "Search for recent issues in the project."}
    ]
)
```

> ⚠️ **注意**：API 中的 MCP 支持仍在演进中，请查阅 [最新文档](https://docs.anthropic.com/en/docs/agents-and-tools/mcp) 获取最新 API。

---

## 第五节：常用 MCP Server

### 官方 Server（由 Anthropic/社区维护）

| Server | 功能 | 安装命令 |
|--------|------|---------|
| **Filesystem** | 读写本地文件 | `npx @modelcontextprotocol/server-filesystem` |
| **GitHub** | 操作 GitHub 仓库 | `npx @modelcontextprotocol/server-github` |
| **Brave Search** | 网页搜索 | `npx @modelcontextprotocol/server-brave-search` |
| **Google Maps** | 地图和位置 | `npx @modelcontextprotocol/server-google-maps` |
| **Slack** | Slack 消息和频道 | `npx @modelcontextprotocol/server-slack` |
| **PostgreSQL** | PostgreSQL 数据库 | `npx @modelcontextprotocol/server-postgres` |
| **SQLite** | SQLite 数据库 | `npx @modelcontextprotocol/server-sqlite` |
| **Puppeteer** | 浏览器自动化 | `npx @modelcontextprotocol/server-puppeteer` |
| **Memory** | 持久化知识图谱 | `npx @modelcontextprotocol/server-memory` |

### 发现更多 Server

- **MCP Server 目录**: https://github.com/modelcontextprotocol/servers
- **Smithery（社区市场）**: https://smithery.ai/
- **Awesome MCP Servers**: https://github.com/punkpeye/awesome-mcp-servers

---

## 第六节：MCP 安全最佳实践

### 权限控制

```json
// 限制文件系统 Server 只访问特定目录
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/me/safe-directory"  // 只允许访问此目录
      ]
    }
  }
}
```

### 安全原则

1. **最小权限原则**：只给 MCP Server 必要的权限
2. **审查 Server 代码**：使用社区 Server 前检查其源码
3. **环境变量管理**：不要在配置文件中硬编码敏感信息
4. **网络隔离**：远程 MCP Server 应使用 HTTPS
5. **日志监控**：在生产环境中记录所有工具调用

### 人工确认（Human-in-the-Loop）

对于高风险操作，应该加入人工确认步骤：

```python
# 在工具执行前请求用户确认
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "delete_file":
        # 高风险操作 — 应该在客户端层面要求用户确认
        # Claude Desktop 会自动弹出确认对话框
        file_path = arguments["path"]
        os.remove(file_path)
        return [TextContent(type="text", text=f"Deleted {file_path}")]
```

---

## 第七节：MCP vs 直接工具调用 对比

| 特性 | 直接 Tool Use (API) | MCP |
|------|---------------------|-----|
| 适用场景 | 自定义应用中嵌入 Claude | 标准化工具生态 |
| 工具定义方式 | 每次请求带 `tools` 参数 | Server 端统一注册 |
| 工具执行 | 你自己写代码执行 | Server 端自动执行 |
| 跨模型兼容 | 仅 Claude | 任何支持 MCP 的模型 |
| 额外能力 | 仅工具调用 | 工具 + 资源 + 提示模板 |
| 生态 | 自建 | 社区共享的 Server 生态 |

**什么时候用哪个？**
- **构建自己的应用** → 用 API Tool Use
- **增强 Claude Desktop/Code 的能力** → 用 MCP
- **构建可复用的工具服务** → 用 MCP Server
- **两者可以共存**：API 应用中也可以连接 MCP Server

---

## 练习题

### 练习 1：搭建 MCP Server

用 Python 或 TypeScript 构建一个 MCP Server，提供以下工具：
- `get_todos`：获取待办事项列表
- `add_todo`：添加待办事项
- `complete_todo`：完成待办事项

在 Claude Desktop 中配置并测试。

### 练习 2：使用社区 Server

安装 `@modelcontextprotocol/server-filesystem` 和 `@modelcontextprotocol/server-github`，在 Claude Desktop 中：
1. 让 Claude 读取你本地文件的内容
2. 让 Claude 查看你 GitHub 仓库的 issue

### 练习 3：资源与提示模板

扩展练习 1 的 Server，添加：
- 一个 Resource：返回所有待办事项的统计信息
- 一个 Prompt 模板：生成每日工作报告

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
