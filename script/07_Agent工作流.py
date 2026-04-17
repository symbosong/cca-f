"""
Claude 课程 — 第七章演示脚本
Agent 工作流与智能体
===================================
使用方法：python 07_Agent工作流.py
依赖安装：pip install openai python-dotenv
"""

import os
import json
import time
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("LKEAP_API_KEY", "your-api-key-here"),
    base_url="https://tokenhub.tencentmaas.com/v1",
)
MODEL = "glm-5"
THINKING_OFF = {"thinking": {"type": "disabled"}}


def call(user_msg, system=None, max_tokens=2000, extra=None):
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user_msg})
    kwargs = dict(model=MODEL, messages=msgs, max_tokens=max_tokens)
    if extra:
        kwargs["extra_body"] = extra
    return client.chat.completions.create(**kwargs).choices[0].message.content


# ─────────────────────────────────────────────
# 演示 1：链式工作流（Chaining）
# 前一步输出 → 下一步输入，形成处理流水线
# ─────────────────────────────────────────────
def demo_chaining_workflow():
    print("=" * 55)
    print("演示 1：链式工作流（Chaining Workflow）")
    print("=" * 55)
    print("流程：原始需求 → 技术方案 → 实现代码 → 代码审查\n")

    raw_requirement = "开发一个用户登录接口，支持手机号+验证码登录"

    # Step 1：需求分析
    print("Step 1️⃣  需求分析...")
    tech_spec = call(
        f"将以下产品需求转化为技术规格说明（接口定义+数据结构+安全要求），100字以内：\n{raw_requirement}",
        extra=THINKING_OFF,
    )
    print(f"技术规格：{tech_spec}\n")

    # Step 2：代码实现（基于上一步输出）
    print("Step 2️⃣  生成实现代码...")
    code = call(
        f"根据以下技术规格，用 Python FastAPI 实现，只需核心代码片段：\n{tech_spec}",
        system="你是资深后端工程师，代码要简洁实用。",
    )
    print(f"代码实现：\n{code}\n")

    # Step 3：代码审查（基于上一步输出）
    print("Step 3️⃣  代码安全审查...")
    review = call(
        f"对以下代码进行安全审查，找出潜在风险点并给出修复建议（3条以内）：\n{code}",
        extra=THINKING_OFF,
    )
    print(f"审查结果：{review}\n")


# ─────────────────────────────────────────────
# 演示 2：路由工作流（Routing）
# 先分类，再交给专业处理器
# ─────────────────────────────────────────────
def demo_routing_workflow():
    print("=" * 55)
    print("演示 2：路由工作流（Routing Workflow）")
    print("=" * 55)
    print("流程：用户输入 → 路由分类 → 专业处理器\n")

    # 专业处理器
    handlers = {
        "技术问题": lambda q: call(q, system="你是腾讯云技术支持工程师，专业解答技术问题。", extra=THINKING_OFF),
        "计费问题": lambda q: call(q, system="你是腾讯云账单客服，专业解答费用和计费问题。", extra=THINKING_OFF),
        "投诉建议": lambda q: call(q, system="你是腾讯云客户成功经理，以同理心处理用户投诉。", extra=THINKING_OFF),
        "其他": lambda q: call(q, system="你是腾讯云通用客服助手。", extra=THINKING_OFF),
    }

    test_queries = [
        "我的 COS 存储桶上传文件一直超时是什么原因？",
        "上个月的账单怎么比之前多了500块？",
        "你们的服务真的太差了，都宕机3次了！",
    ]

    for query in test_queries:
        # 路由分类
        category = call(
            f"将以下用户咨询分类为：技术问题/计费问题/投诉建议/其他，只输出分类名称：\n{query}",
            extra=THINKING_OFF,
            max_tokens=50,
        ).strip()

        # 清理分类结果
        category = next((k for k in handlers if k in category), "其他")

        print(f"用户：{query}")
        print(f"路由 → 【{category}】")
        response = handlers[category](query)
        print(f"AI：{response}\n")


# ─────────────────────────────────────────────
# 演示 3：并行工作流（Parallelization）
# 多任务同时执行，最后汇总
# ─────────────────────────────────────────────
def demo_parallel_workflow():
    print("=" * 55)
    print("演示 3：并行工作流（Parallelization Workflow）")
    print("=" * 55)
    print("任务：同时分析一篇文章的多个维度，最后汇总报告\n")

    article = """
    腾讯云2025年全面推进AI原生战略，重点布局大模型API商业化。
    TokenHub平台已整合20+款主流大模型，月活开发者突破50万。
    在金融、政务、医疗三大行业，腾讯云AI解决方案合同额同比增长180%。
    公司预计AI业务将在2026年贡献30%以上的云业务收入。
    """

    tasks = {
        "摘要": f"用50字总结以下文章核心内容：\n{article}",
        "关键数据": f"提取文章中所有数字和具体指标，列表形式：\n{article}",
        "情感分析": f"分析文章情感倾向，输出：正面/负面/中性 + 一句理由：\n{article}",
        "标签提取": f"为文章提取5个关键词标签，逗号分隔：\n{article}",
    }

    results = {}
    start = time.time()

    # 并行执行所有分析任务
    def run_task(name_prompt):
        name, prompt = name_prompt
        return name, call(prompt, extra=THINKING_OFF, max_tokens=500)

    with ThreadPoolExecutor(max_workers=4) as executor:
        for name, result in executor.map(run_task, tasks.items()):
            results[name] = result

    elapsed = time.time() - start
    print(f"4个任务并行完成，耗时：{elapsed:.1f}s\n")

    # 汇总报告
    summary_prompt = f"""基于以下多维度分析结果，生成一份简洁的分析报告（150字以内）：

摘要：{results.get('摘要', '')}
关键数据：{results.get('关键数据', '')}
情感倾向：{results.get('情感分析', '')}
关键词：{results.get('标签提取', '')}"""

    final_report = call(summary_prompt, extra=THINKING_OFF)
    print("各维度分析结果：")
    for k, v in results.items():
        print(f"  [{k}] {v.strip()}")
    print(f"\n汇总报告：\n{final_report}\n")


# ─────────────────────────────────────────────
# 演示 4：评估器-优化器模式（Evaluator-Optimizer）
# 生产 → 评估 → 反馈 → 改进 → 循环
# ─────────────────────────────────────────────
def demo_evaluator_optimizer():
    print("=" * 55)
    print("演示 4：评估器-优化器模式")
    print("=" * 55)
    print("流程：生成初稿 → 评估打分 → 反馈改进 → 直到满分\n")

    task = "写一段腾讯云 TokenHub 的产品宣传文案，面向技术开发者，50字以内"
    max_iterations = 3

    # 初始生成
    draft = call(task, extra=THINKING_OFF, max_tokens=500)
    print(f"初稿：{draft}\n")

    for i in range(max_iterations):
        # 评估
        eval_prompt = f"""评估以下产品文案的质量（面向技术开发者），打分1-10：

文案：{draft}

评分标准：
- 技术准确性（3分）
- 开发者视角（3分）
- 简洁有力（2分）
- 有具体价值点（2分）

只输出JSON：{{"score": 数字, "feedback": "改进建议"}}"""

        eval_result = call(eval_prompt, extra=THINKING_OFF, max_tokens=300)

        try:
            json_str = eval_result[eval_result.find("{"):eval_result.rfind("}") + 1]
            eval_data = json.loads(json_str)
            score = eval_data.get("score", 0)
            feedback = eval_data.get("feedback", "")
        except Exception:
            score = 0
            feedback = eval_result[:100]

        print(f"第 {i+1} 轮评估：{score}/10 分")
        print(f"改进建议：{feedback}")

        if score >= 8:
            print(f"\n✅ 达到目标分数，停止优化")
            break

        # 优化
        draft = call(
            f"根据以下反馈改进文案：\n原文案：{draft}\n改进建议：{feedback}\n\n{task}",
            extra=THINKING_OFF,
            max_tokens=500,
        )
        print(f"优化后：{draft}\n")

    print(f"\n最终文案：{draft}\n")


# ─────────────────────────────────────────────
# 演示 5：完整 Agent Loop（工具驱动自主决策）
# ─────────────────────────────────────────────
def demo_agent_loop():
    print("=" * 55)
    print("演示 5：完整 Agent Loop —— 自主规划与执行")
    print("=" * 55)

    # 工具定义
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_docs",
                "description": "搜索腾讯云产品文档",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "搜索关键词"},
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "estimate_cost",
                "description": "估算腾讯云产品月费用",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product": {"type": "string", "description": "产品名称"},
                        "usage": {"type": "string", "description": "使用量描述"},
                    },
                    "required": ["product", "usage"],
                },
            },
        },
    ]

    # 模拟工具返回
    def mock_tool(name, args):
        if name == "search_docs":
            return json.dumps({
                "results": [
                    f"找到关于 {args.get('query')} 的文档3篇",
                    "推荐架构：CVM + COS + CDN 三层结构",
                    "高可用方案：多可用区部署 + 负载均衡",
                ]
            }, ensure_ascii=False)
        elif name == "estimate_cost":
            return json.dumps({
                "product": args.get("product"),
                "usage": args.get("usage"),
                "estimated_monthly_cost": "约 ¥800-1500/月",
                "suggestion": "建议先用按量计费测试，稳定后转包年包月节省30%",
            }, ensure_ascii=False)
        return json.dumps({"error": "unknown tool"})

    user_request = "我要搭建一个中小型电商网站，帮我规划腾讯云架构方案并估算成本"
    print(f"用户需求：{user_request}\n")

    messages = [
        {"role": "system", "content": "你是腾讯云解决方案架构师，帮助客户规划云架构方案。请主动使用工具获取信息。"},
        {"role": "user", "content": user_request},
    ]

    step = 0
    while step < 5:  # 最多5轮
        step += 1
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools, max_tokens=2000
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
                args = json.loads(tc.function.arguments)
                result = mock_tool(tc.function.name, args)
                print(f"  🤖 Agent 调用：{tc.function.name}({args})")
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        else:
            print(f"\nAgent 最终方案：\n{msg.content}\n")
            break


# ─────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Claude 课程第七章 — Agent 工作流与智能体")
    print(f"   模型：{MODEL}\n")

    demo_chaining_workflow()
    demo_routing_workflow()
    demo_parallel_workflow()
    demo_evaluator_optimizer()
    demo_agent_loop()

    print("✅ 第七章演示完成！")
