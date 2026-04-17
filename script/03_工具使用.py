"""
Claude 课程 — 第三章演示脚本
工具使用（Function Calling）
===================================
使用方法：python 03_工具使用.py
依赖安装：pip install openai python-dotenv
"""

import os
import json
import random
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("LKEAP_API_KEY", "your-api-key-here"),
    base_url="https://tokenhub.tencentmaas.com/v1",
)
MODEL = "glm-5"


# ─────────────────────────────────────────────
# 模拟工具函数（实际项目中会调用真实 API）
# ─────────────────────────────────────────────
def get_weather(city: str) -> dict:
    """模拟天气查询"""
    mock_data = {
        "北京": {"temperature": 22, "condition": "晴", "humidity": 45},
        "上海": {"temperature": 26, "condition": "多云", "humidity": 72},
        "广州": {"temperature": 30, "condition": "阵雨", "humidity": 88},
    }
    data = mock_data.get(city, {"temperature": random.randint(15, 35), "condition": "晴", "humidity": 60})
    return {"city": city, **data, "unit": "摄氏度"}


def calculate(expression: str) -> dict:
    """安全计算数学表达式"""
    try:
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return {"error": "不支持的字符"}
        result = eval(expression)
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


def get_current_time() -> dict:
    """获取当前时间"""
    now = datetime.now()
    return {
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "weekday": ["周一","周二","周三","周四","周五","周六","周日"][now.weekday()],
    }


# 工具定义（JSON Schema）
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称，如：北京、上海"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式，支持加减乘除括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式，如：(25 + 35) * 2"},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期和时间",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

# 工具调度映射
TOOL_MAP = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_current_time": get_current_time,
}


def run_tool_call(tool_name: str, tool_args: dict) -> str:
    """执行工具并返回结果字符串"""
    func = TOOL_MAP.get(tool_name)
    if not func:
        return json.dumps({"error": f"未知工具: {tool_name}"})
    result = func(**tool_args)
    return json.dumps(result, ensure_ascii=False)


def agent_loop(user_message: str, verbose: bool = True) -> str:
    """
    核心 Agent Loop：
    用户消息 → 模型决策 → 执行工具 → 将结果返回模型 → 最终回答
    """
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            max_tokens=2000,
        )

        choice = response.choices[0]
        msg = choice.message

        # 如果模型决定调用工具
        if choice.finish_reason == "tool_calls" and msg.tool_calls:
            # 将 assistant 的工具调用消息加入历史
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            })

            # 执行每个工具调用
            for tc in msg.tool_calls:
                tool_name = tc.function.name
                tool_args = json.loads(tc.function.arguments)

                if verbose:
                    print(f"  🔧 调用工具：{tool_name}({tool_args})")

                tool_result = run_tool_call(tool_name, tool_args)

                if verbose:
                    print(f"  📤 工具返回：{tool_result}")

                # 将工具结果加入历史
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": tool_result,
                })

        else:
            # 模型直接给出最终回答
            return msg.content


# ─────────────────────────────────────────────
# 演示 1：单工具调用 — 天气查询
# ─────────────────────────────────────────────
def demo_single_tool():
    print("=" * 55)
    print("演示 1：单工具调用 — 天气查询")
    print("=" * 55)
    question = "北京今天天气怎么样？"
    print(f"用户：{question}")
    answer = agent_loop(question)
    print(f"AI：{answer}\n")


# ─────────────────────────────────────────────
# 演示 2：工具 + 计算
# ─────────────────────────────────────────────
def demo_calculation():
    print("=" * 55)
    print("演示 2：工具调用 — 数学计算")
    print("=" * 55)
    question = "帮我算一下：(128 + 256) * 3 / 4 等于多少？"
    print(f"用户：{question}")
    answer = agent_loop(question)
    print(f"AI：{answer}\n")


# ─────────────────────────────────────────────
# 演示 3：多工具联合调用
# ─────────────────────────────────────────────
def demo_multi_tool():
    print("=" * 55)
    print("演示 3：多工具联合调用")
    print("=" * 55)
    question = "现在几点了？上海和广州哪个城市更适合出门，分别说说理由。"
    print(f"用户：{question}")
    answer = agent_loop(question)
    print(f"AI：{answer}\n")


# ─────────────────────────────────────────────
# 演示 4：结构化输出（工具作为格式化手段）
# ─────────────────────────────────────────────
def demo_structured_output():
    print("=" * 55)
    print("演示 4：结构化输出（用工具提取信息）")
    print("=" * 55)

    extract_tool = [
        {
            "type": "function",
            "function": {
                "name": "extract_order_info",
                "description": "从用户文本中提取订单信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product": {"type": "string", "description": "商品名称"},
                        "quantity": {"type": "integer", "description": "数量"},
                        "address": {"type": "string", "description": "收货地址"},
                        "urgency": {
                            "type": "string",
                            "enum": ["普通", "加急", "次日达"],
                            "description": "紧急程度",
                        },
                    },
                    "required": ["product", "quantity", "address", "urgency"],
                },
            },
        }
    ]

    user_text = "我要买3台笔记本电脑，发到北京朝阳区望京SOHO，要快，明天必须到。"
    print(f"原始文本：{user_text}")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是一个订单信息提取助手，从用户描述中提取结构化订单信息。"},
            {"role": "user", "content": user_text},
        ],
        tools=extract_tool,
        tool_choice={"type": "function", "function": {"name": "extract_order_info"}},
        max_tokens=500,
    )

    tool_call = response.choices[0].message.tool_calls[0]
    order_info = json.loads(tool_call.function.arguments)
    print("提取结果：")
    for k, v in order_info.items():
        print(f"  {k}: {v}")
    print()


# ─────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Claude 课程第三章 — 工具使用（Function Calling）")
    print(f"   模型：{MODEL}\n")

    demo_single_tool()
    demo_calculation()
    demo_multi_tool()
    demo_structured_output()

    print("✅ 第三章演示完成！")
