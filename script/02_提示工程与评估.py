"""
Claude 课程 — 第二章演示脚本
提示工程与评估
===================================
使用方法：python 02_提示工程与评估.py
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


def call(messages, system=None, max_tokens=2000, extra=None):
    """统一调用封装"""
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.extend(messages)
    kwargs = dict(model=MODEL, messages=msgs, max_tokens=max_tokens)
    if extra:
        kwargs["extra_body"] = extra
    return client.chat.completions.create(**kwargs).choices[0].message.content


# ─────────────────────────────────────────────
# 演示 1：清晰直接 vs 模糊指令对比
# ─────────────────────────────────────────────
def demo_clear_vs_vague():
    print("=" * 55)
    print("演示 1：清晰直接 vs 模糊指令对比")
    print("=" * 55)

    task = "写一段关于人工智能的介绍"

    # 模糊提示
    vague = call([{"role": "user", "content": task}], max_tokens=2000)

    # 清晰提示（明确受众、字数、格式、禁止内容）
    clear_prompt = (
        "请为完全不懂技术的企业高管写一段人工智能介绍。"
        "要求：100字以内，使用类比帮助理解，不使用任何技术术语，"
        "结尾加一句对企业的实际意义。"
    )
    clear = call([{"role": "user", "content": clear_prompt}], max_tokens=2000)

    print("【模糊提示】输入：", task)
    print("输出：", vague[:200], "...\n")
    print("【清晰提示】输入：", clear_prompt)
    print("输出：", clear)
    print()


# ─────────────────────────────────────────────
# 演示 2：XML 标签结构化提示
# ─────────────────────────────────────────────
def demo_xml_tags():
    print("=" * 55)
    print("演示 2：XML 标签结构化提示")
    print("=" * 55)

    article = """
    腾讯云发布新一代大模型服务平台 TokenHub，整合了混元、DeepSeek、
    GLM 等多款主流大模型。平台支持按量计费，开发者无需部署即可调用。
    此次发布标志着腾讯云在 AI 基础设施领域的重要布局。
    """

    prompt = f"""请根据以下文章完成任务。

<article>
{article}
</article>

<tasks>
1. 用一句话总结文章主旨
2. 提取3个关键词
3. 判断文章情感倾向（正面/负面/中性）
</tasks>

请按照如下格式输出：
<summary>一句话总结</summary>
<keywords>关键词1, 关键词2, 关键词3</keywords>
<sentiment>情感倾向</sentiment>"""

    result = call([{"role": "user", "content": prompt}], max_tokens=2000)
    print("提示中使用 XML 标签分离数据与指令，引导结构化输出：")
    print(result)
    print()


# ─────────────────────────────────────────────
# 演示 3：Few-shot 示例学习
# ─────────────────────────────────────────────
def demo_few_shot():
    print("=" * 55)
    print("演示 3：Few-shot 示例学习（举例引导格式）")
    print("=" * 55)

    prompt = """请将以下客户反馈分类为：【功能建议】【Bug报告】【使用咨询】【投诉】

示例：
输入：能不能加个黑暗模式？
输出：【功能建议】

输入：点击保存按钮后页面直接崩溃了
输出：【Bug报告】

输入：请问怎么导出PDF？
输出：【使用咨询】

现在请分类以下反馈：
输入：你们客服态度太差了，等了半小时没人接！"""

    result = call(
        [{"role": "user", "content": prompt}],
        max_tokens=200,
        extra=THINKING_OFF,
    )
    print(result)
    print()


# ─────────────────────────────────────────────
# 演示 4：思维链（Chain of Thought）
# ─────────────────────────────────────────────
def demo_chain_of_thought():
    print("=" * 55)
    print("演示 4：思维链（Chain of Thought）推理")
    print("=" * 55)

    # 不用思维链
    direct_prompt = "一个项目有5名工程师，每人每天能完成3个任务单元。如果项目需要完成90个任务单元，需要多少天？"
    direct = call(
        [{"role": "user", "content": direct_prompt}],
        max_tokens=500,
        extra=THINKING_OFF,
    )

    # 引导思维链
    cot_prompt = direct_prompt + "\n\n请一步一步思考后再给出答案。"
    cot = call([{"role": "user", "content": cot_prompt}], max_tokens=2000)

    print("【直接回答】")
    print(direct)
    print()
    print("【引导思维链】")
    print(cot)
    print()


# ─────────────────────────────────────────────
# 演示 5：自动化评估管道（模型自评）
# ─────────────────────────────────────────────
def demo_evaluation_pipeline():
    print("=" * 55)
    print("演示 5：自动化评估管道（LLM-as-Judge）")
    print("=" * 55)

    test_cases = [
        {"question": "腾讯云的对象存储服务叫什么？", "expected_keyword": "COS"},
        {"question": "什么是云原生？", "expected_keyword": "容器"},
        {"question": "Serverless的优势是什么？", "expected_keyword": "按量"},
    ]

    results = []
    for i, case in enumerate(test_cases):
        # 被评估的回答
        answer = call(
            [{"role": "user", "content": case["question"]}],
            max_tokens=2000,
        )

        # 评估提示
        eval_prompt = f"""请评估以下回答的质量，打分1-5分。

问题：{case["question"]}
回答：{answer}

评分标准：
- 5分：准确、完整、清晰
- 3分：基本正确但不够完整
- 1分：错误或不相关

请只输出一个JSON：{{"score": 分数, "reason": "简短理由"}}"""

        eval_result = call(
            [{"role": "user", "content": eval_prompt}],
            max_tokens=300,
            extra=THINKING_OFF,
        )

        # 解析分数
        try:
            # 提取 JSON 部分
            json_str = eval_result[eval_result.find("{"):eval_result.rfind("}") + 1]
            eval_data = json.loads(json_str)
            score = eval_data.get("score", "?")
            reason = eval_data.get("reason", "")
        except Exception:
            score = "解析失败"
            reason = eval_result[:50]

        results.append({"问题": case["question"], "得分": score, "理由": reason})
        print(f"  问题 {i+1}：{case['question']}")
        print(f"  得分：{score} | {reason}\n")

    avg = sum(r["得分"] for r in results if isinstance(r["得分"], int)) / len(results)
    print(f"平均得分：{avg:.1f} / 5")
    print()


# ─────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Claude 课程第二章 — 提示工程与评估")
    print(f"   模型：{MODEL}\n")

    demo_clear_vs_vague()
    demo_xml_tags()
    demo_few_shot()
    demo_chain_of_thought()
    demo_evaluation_pipeline()

    print("✅ 第二章演示完成！")
