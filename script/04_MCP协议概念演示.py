"""
Claude 课程 — 第四章演示脚本
MCP 模型上下文协议（概念演示）
===================================
说明：MCP 需要独立的 Server 进程，本脚本用模拟方式演示 MCP 三大核心能力：
      Tools / Resources / Prompts 的概念和使用场景
使用方法：python 04_MCP协议概念演示.py
依赖安装：pip install openai python-dotenv
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("LKEAP_API_KEY", "your-api-key-here"),
    base_url="https://tokenhub.tencentmaas.com/v1",
)
MODEL = "glm-5"
THINKING_OFF = {"thinking": {"type": "disabled"}}


def call(messages, system=None, max_tokens=2000, tools=None, extra=None):
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.extend(messages)
    kwargs = dict(model=MODEL, messages=msgs, max_tokens=max_tokens)
    if tools:
        kwargs["tools"] = tools
    if extra:
        kwargs["extra_body"] = extra
    return client.chat.completions.create(**kwargs)


# ─────────────────────────────────────────────
# 演示 1：MCP 核心概念讲解（让模型解释）
# ─────────────────────────────────────────────
def demo_mcp_concept():
    print("=" * 55)
    print("演示 1：MCP 是什么？（核心概念）")
    print("=" * 55)

    prompt = """请用"USB接口"类比，向一位软件工程师解释：
1. MCP（模型上下文协议）解决了什么问题？（N×M → N+M）
2. MCP的三大核心能力：Tools、Resources、Prompts 各自的作用
3. MCP Server 和 MCP Client 的关系

回答要求：简洁，每个点不超过2句话。"""

    r = call([{"role": "user", "content": prompt}], max_tokens=2000)
    print(r.choices[0].message.content)
    print()


# ─────────────────────────────────────────────
# 演示 2：模拟 MCP Tools 能力
# ─────────────────────────────────────────────
def demo_mcp_tools():
    print("=" * 55)
    print("演示 2：MCP Tools —— 模拟文件系统工具")
    print("=" * 55)
    print("（真实 MCP 中，这些工具由独立的 MCP Server 进程提供）\n")

    # 模拟 MCP Server 暴露的工具
    mcp_tools = [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "读取指定路径的文件内容（MCP Filesystem Server 提供）",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "文件路径"},
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_directory",
                "description": "列出指定目录的文件列表（MCP Filesystem Server 提供）",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "目录路径"},
                    },
                    "required": ["path"],
                },
            },
        },
    ]

    # 模拟工具返回值
    mock_results = {
        "read_file": '{"content": "# 项目说明\\n这是一个RAG演示项目，包含文档索引和检索功能。\\n作者：AI架构师团队"}',
        "list_directory": '{"files": ["main.py", "config.yaml", "README.md", "requirements.txt"]}',
    }

    question = "帮我看看项目根目录有哪些文件，然后读一下README说明。"
    print(f"用户：{question}")

    messages = [{"role": "user", "content": question}]

    # Agent Loop
    while True:
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=mcp_tools, max_tokens=2000
        )
        choice = response.choices[0]
        msg = choice.message

        if choice.finish_reason == "tool_calls" and msg.tool_calls:
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {"id": tc.id, "type": "function",
                     "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                    for tc in msg.tool_calls
                ],
            })
            for tc in msg.tool_calls:
                result = mock_results.get(tc.function.name, '{"error": "未知工具"}')
                args = json.loads(tc.function.arguments)
                print(f"  🔌 MCP Tool：{tc.function.name}({args})")
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        else:
            print(f"\nAI：{msg.content}\n")
            break


# ─────────────────────────────────────────────
# 演示 3：模拟 MCP Resources 能力
# ─────────────────────────────────────────────
def demo_mcp_resources():
    print("=" * 55)
    print("演示 3：MCP Resources —— 为模型注入上下文数据")
    print("=" * 55)
    print("（真实 MCP 中，Resources 由 Server 动态提供，这里用 System Prompt 模拟）\n")

    # 模拟从 MCP Resource 读取到的数据
    mock_resource = """
[MCP Resource: company_info://profile]
公司名称：腾讯云智能科技
当前产品线：TokenHub、LKEAP、混元大模型、向量数据库
2025年重点战略：AI原生应用、大模型API商业化
内部联系人：张工（AI架构师）、李总（产品总监）
"""

    system = f"你是公司的AI助手。以下是通过MCP Resource注入的公司背景信息，请基于此回答问题：\n{mock_resource}"

    question = "我们公司今年的重点战略是什么？有哪些AI相关产品？"
    print(f"用户：{question}")
    r = call([{"role": "user", "content": question}], system=system, max_tokens=2000)
    print(f"AI（基于MCP Resource上下文）：{r.choices[0].message.content}\n")


# ─────────────────────────────────────────────
# 演示 4：模拟 MCP Prompts 能力
# ─────────────────────────────────────────────
def demo_mcp_prompts():
    print("=" * 55)
    print("演示 4：MCP Prompts —— 复用预定义提示模板")
    print("=" * 55)
    print("（真实MCP中，Prompts模板存储在Server，客户端按需调用）\n")

    # 模拟 MCP Server 提供的提示模板库
    mcp_prompt_templates = {
        "code_review": {
            "description": "代码审查模板",
            "template": "请对以下{language}代码进行审查，重点关注：安全性、性能、可读性。\n\n代码：\n```{language}\n{code}\n```",
        },
        "meeting_summary": {
            "description": "会议纪要模板",
            "template": "请将以下会议记录整理为标准格式，包含：决议事项、负责人、截止时间。\n\n原始记录：\n{raw_notes}",
        },
    }

    # 使用 code_review 模板
    template = mcp_prompt_templates["code_review"]["template"]
    filled_prompt = template.format(
        language="Python",
        code="""
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return db.execute(query)
""",
    )

    print(f"调用 MCP Prompt 模板：code_review")
    print(f"填充参数：language=Python\n")

    r = call([{"role": "user", "content": filled_prompt}], max_tokens=2000)
    print(f"AI（使用MCP Prompt模板）：{r.choices[0].message.content}\n")


# ─────────────────────────────────────────────
# 演示 5：MCP vs 直接工具调用 对比总结
# ─────────────────────────────────────────────
def demo_mcp_vs_direct():
    print("=" * 55)
    print("演示 5：MCP vs 直接工具调用 —— 何时选择？")
    print("=" * 55)

    prompt = """请简要对比 MCP（模型上下文协议）和直接在代码中定义工具的区别，
从以下维度分析：
1. 复用性
2. 维护成本
3. 适合场景

最后给出一句话结论：什么时候用MCP，什么时候直接写工具。
输出格式用表格。"""

    r = call(
        [{"role": "user", "content": prompt}],
        max_tokens=2000,
        extra=THINKING_OFF,
    )
    print(r.choices[0].message.content)
    print()


# ─────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Claude 课程第四章 — MCP 模型上下文协议")
    print(f"   模型：{MODEL}")
    print("   注意：本章为概念演示，实际 MCP 需独立 Server 进程\n")

    demo_mcp_concept()
    demo_mcp_tools()
    demo_mcp_resources()
    demo_mcp_prompts()
    demo_mcp_vs_direct()

    print("✅ 第四章演示完成！")
