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
# 演示 5：tool_choice 精细控制
# auto=模型自行决定 / required=必须调用工具 / 指定函数=强制调用某个工具
# ─────────────────────────────────────────────
def demo_tool_choice():
    print("=" * 55)
    print("演示 5：tool_choice 精细控制")
    print("=" * 55)

    question = "今天北京天气如何？"

    # auto：模型自行判断是否调用工具（默认）
    r_auto = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        tools=TOOLS,
        tool_choice="auto",
        max_tokens=500,
    )
    auto_result = "调用了工具" if r_auto.choices[0].finish_reason == "tool_calls" else "直接回答"
    print(f"tool_choice='auto'   → {auto_result}")

    # required：强制必须调用至少一个工具
    r_required = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "你好"}],  # 普通问候，正常不会调工具
        tools=TOOLS,
        tool_choice="required",
        max_tokens=500,
    )
    req_result = "调用了工具" if r_required.choices[0].finish_reason == "tool_calls" else "直接回答"
    print(f"tool_choice='required'→ {req_result}（即使是问候也强制调用）")

    # 指定工具：强制调用 get_current_time
    r_specific = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "随便说点什么"}],
        tools=TOOLS,
        tool_choice={"type": "function", "function": {"name": "get_current_time"}},
        max_tokens=500,
    )
    if r_specific.choices[0].message.tool_calls:
        forced_tool = r_specific.choices[0].message.tool_calls[0].function.name
        print(f"tool_choice=指定函数 → 强制调用了 {forced_tool}")
    print()


# ─────────────────────────────────────────────
# 演示 6：多轮对话中持续使用工具（聊天机器人）
# ─────────────────────────────────────────────
def demo_multi_turn_chatbot():
    print("=" * 55)
    print("演示 6：多轮对话聊天机器人（工具贯穿全程）")
    print("=" * 55)

    conversation = [
        {"role": "system", "content": "你是一个智能助手，可以查天气、做计算、查时间。"},
    ]

    turns = [
        "现在几点了？",
        "上海天气怎么样？适合跑步吗？",
        "如果跑步5公里消耗350卡路里，我体重60公斤，跑完后还剩多少能量？（假设基础代谢一天2000卡）",
    ]

    for user_msg in turns:
        print(f"用户：{user_msg}")
        conversation.append({"role": "user", "content": user_msg})

        # Agent loop
        while True:
            response = client.chat.completions.create(
                model=MODEL, messages=conversation, tools=TOOLS, max_tokens=2000
            )
            choice = response.choices[0]
            msg = choice.message

            if choice.finish_reason == "tool_calls" and msg.tool_calls:
                conversation.append({
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [
                        {"id": tc.id, "type": "function",
                         "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                        for tc in msg.tool_calls
                    ],
                })
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    result = run_tool_call(tc.function.name, args)
                    print(f"  🔧 {tc.function.name}({args})")
                    conversation.append({"role": "tool", "tool_call_id": tc.id, "content": result})
            else:
                conversation.append({"role": "assistant", "content": msg.content})
                print(f"AI：{msg.content}\n")
                break


# ─────────────────────────────────────────────
# 演示 7：Extended Thinking（扩展思考）
# GLM-5 默认开启思维链，这里演示如何显式控制并观察思考过程
# ─────────────────────────────────────────────
def demo_extended_thinking():
    print("=" * 55)
    print("演示 7：Extended Thinking（扩展思考）")
    print("=" * 55)

    hard_question = """
    一家公司有3个部门：A、B、C。
    - A部门有20人，平均薪资15000元
    - B部门有35人，平均薪资12000元
    - C部门有15人，平均薪资18000元
    公司计划给所有人涨薪：A部门涨10%，B部门涨15%，C部门涨8%。
    请计算：涨薪后公司每月总薪资支出增加了多少？增幅百分比是多少？
    """

    print("问题：复杂薪资计算")
    print("（GLM-5 开启深度思考模式）\n")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": hard_question}],
        max_tokens=3000,
        # GLM-5 默认开启思维链，不传 thinking 参数即为开启
    )

    msg = response.choices[0].message

    # 显示思维链过程（如果有）
    reasoning = getattr(msg, "reasoning_content", None)
    if reasoning:
        print("【思考过程（摘要前200字）】")
        print(reasoning[:200], "...\n")

    print("【最终答案】")
    print(msg.content)
    print()


# ─────────────────────────────────────────────
# 演示 8：Prompt Caching 概念演示
# 通过对比有无缓存的响应时间，理解 Prompt Caching 的价值
# ─────────────────────────────────────────────
def demo_prompt_caching():
    print("=" * 55)
    print("演示 8：Prompt Caching（提示缓存）概念")
    print("=" * 55)

    import time

    # 模拟一个超长的系统提示（实际生产中可能是几千字的规则文档）
    long_system = """你是腾讯云的专业技术顾问。以下是你需要了解的完整产品知识库：

【计算产品】云服务器CVM提供弹性计算，支持按量/包年包月计费；容器服务TKE基于Kubernetes；
函数计算SCF实现Serverless架构，按调用次数和运行时长计费。

【存储产品】对象存储COS适合非结构化数据，持久性12个9；云硬盘CBS提供块存储；
文件存储CFS支持NFS/SMB协议；数据万象CI提供图片处理能力。

【数据库产品】TencentDB MySQL/PostgreSQL兼容开源协议；TDSQL面向金融级场景；
Redis缓存支持多种数据结构；MongoDB文档数据库；向量数据库支持AI检索。

【网络产品】私有网络VPC实现网络隔离；负载均衡CLB支持4/7层；CDN加速覆盖全球节点；
专线DC提供物理专线连接；SD-WAN实现软件定义广域网。

【安全产品】Web应用防火墙WAF防御OWASP TOP10；DDoS高防提供T级清洗；
主机安全CWP提供漏洞扫描；SSL证书管理支持自动续期；AI防护盾基于大模型检测。

【AI产品】TokenHub整合20+大模型；向量数据库支持RAG；慧眼人脸核身；
知识引擎LKEAP提供企业知识问答；语音识别ASR；自然语言处理NLP。""" * 2  # 重复使之更长

    questions = [
        "COS的数据持久性是多少？",
        "TDSQL适合什么场景？",
        "AI防护盾和WAF的区别是什么？",
    ]

    print("场景：用同一个超长系统提示连续提问（模拟Prompt Caching效果）")
    print(f"系统提示长度：约{len(long_system)}字符\n")

    times = []
    for i, q in enumerate(questions):
        start = time.time()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": long_system},
                {"role": "user", "content": q},
            ],
            max_tokens=300,
            extra_body={"thinking": {"type": "disabled"}},
        )
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"第{i+1}次请求（{elapsed:.1f}s）：{q}")
        print(f"  → {response.choices[0].message.content[:80]}...\n")

    print(f"响应时间：{times[0]:.1f}s → {times[1]:.1f}s → {times[2]:.1f}s")
    print("（实际生产中使用支持Caching的模型，重复的长提示词命中缓存后成本降低约90%）")
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
    demo_tool_choice()
    demo_multi_turn_chatbot()
    demo_extended_thinking()
    demo_prompt_caching()

    print("✅ 第三章演示完成！")
