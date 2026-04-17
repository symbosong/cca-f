"""
Claude 课程 — 第一章演示脚本
腾讯云 LKEAP + GLM-5 替代方案
===================================
适用场景：受限地区无法访问 Anthropic 官方 API
使用方法：python 01_基础调用演示.py
依赖安装：pip install openai python-dotenv
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# ─────────────────────────────────────────────
# 1. 初始化客户端（核心：只需修改 base_url）
# ─────────────────────────────────────────────
client = OpenAI(
    api_key=os.environ.get("LKEAP_API_KEY", "your-api-key-here"),
    base_url="https://tokenhub.tencentmaas.com/v1",
)

# 演示用模型，也可换为 deepseek-v3.2 / deepseek-v3-0324
MODEL = "glm-5"


# ─────────────────────────────────────────────
# 演示 1：最简单的 API 调用
# ─────────────────────────────────────────────
def demo_basic_call():
    print("=" * 50)
    print("演示 1：基础 API 调用")
    print("=" * 50)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "用一句话解释什么是大语言模型。"}
        ],
        max_tokens=2000,
    )

    print(response.choices[0].message.content)
    print()


# ─────────────────────────────────────────────
# 演示 2：System Prompt（系统提示词）
# ─────────────────────────────────────────────
def demo_system_prompt():
    print("=" * 50)
    print("演示 2：System Prompt 角色设定")
    print("=" * 50)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位专业的云计算架构师，擅长用简洁易懂的语言"
                    "向非技术人员解释复杂的技术概念。回答控制在 3 句话以内。"
                ),
            },
            {"role": "user", "content": "什么是 Serverless？"},
        ],
        max_tokens=2000,
    )

    print(response.choices[0].message.content)
    print()


# ─────────────────────────────────────────────
# 演示 3：多轮对话（保持上下文）
# ─────────────────────────────────────────────
def demo_multi_turn():
    print("=" * 50)
    print("演示 3：多轮对话")
    print("=" * 50)

    conversation_history = [
        {"role": "system", "content": "你是一个友好的 AI 助手。"}
    ]

    # 第一轮
    user_msg_1 = "我叫小明，我今年 28 岁。"
    conversation_history.append({"role": "user", "content": user_msg_1})

    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation_history,
        max_tokens=2000,
    )
    assistant_reply_1 = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_reply_1})

    print(f"用户：{user_msg_1}")
    print(f"AI：{assistant_reply_1}")
    print()

    # 第二轮（测试模型是否记住了上下文）
    user_msg_2 = "你还记得我的名字吗？我几岁了？"
    conversation_history.append({"role": "user", "content": user_msg_2})

    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation_history,
        max_tokens=2000,
    )
    assistant_reply_2 = response.choices[0].message.content

    print(f"用户：{user_msg_2}")
    print(f"AI：{assistant_reply_2}")
    print()


# ─────────────────────────────────────────────
# 演示 4：流式输出（打字机效果）
# ─────────────────────────────────────────────
def demo_streaming():
    print("=" * 50)
    print("演示 4：流式输出（Streaming）")
    print("=" * 50)
    print("AI 回答（实时流式）：", end="", flush=True)

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "请用 3 个要点介绍腾讯云的核心优势。"}
        ],
        max_tokens=2000,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        # GLM-5 可能包含思维链内容，这里过滤只展示最终回答
        content = getattr(delta, "content", None)
        if content:
            print(content, end="", flush=True)

    print("\n")


# ─────────────────────────────────────────────
# 演示 5：参数调节（temperature / max_tokens）
# ─────────────────────────────────────────────
def demo_parameters():
    print("=" * 50)
    print("演示 5：参数调节 — temperature 对比")
    print("=" * 50)

    prompt = "给我一个创意的新产品名称，只需回答名称本身，不要解释。"

    # 低 temperature = 更确定、更保守
    response_low = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=200,
        extra_body={"thinking": {"type": "disabled"}},
    )

    # 高 temperature = 更有创意、更随机
    response_high = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=200,
        extra_body={"thinking": {"type": "disabled"}},
    )

    print(f"temperature=0.1（低）：{response_low.choices[0].message.content.strip()}")
    print(f"temperature=0.9（高）：{response_high.choices[0].message.content.strip()}")
    print()


# ─────────────────────────────────────────────
# 主程序入口
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Claude 课程第一章 — 腾讯云 LKEAP + GLM-5 演示")
    print(f"   模型：{MODEL}")
    print(f"   接入点：https://tokenhub.tencentmaas.com/v1\n")

    demo_basic_call()
    demo_system_prompt()
    demo_multi_turn()
    demo_streaming()
    demo_parameters()

    print("✅ 所有演示完成！")
