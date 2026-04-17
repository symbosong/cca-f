"""
Claude 课程 — 第五章演示脚本
RAG 检索增强生成
===================================
使用方法：python 05_RAG检索增强生成.py
依赖安装：pip install openai python-dotenv
注意：本脚本用简单的关键词匹配模拟向量检索，无需额外向量数据库
"""

import os
import re
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
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.extend(messages)
    kwargs = dict(model=MODEL, messages=msgs, max_tokens=max_tokens)
    if extra:
        kwargs["extra_body"] = extra
    return client.chat.completions.create(**kwargs).choices[0].message.content


# ─────────────────────────────────────────────
# 模拟知识库（真实项目中来自向量数据库）
# ─────────────────────────────────────────────
KNOWLEDGE_BASE = [
    {
        "id": "doc_001",
        "title": "腾讯云对象存储 COS 介绍",
        "content": "腾讯云对象存储（COS）是一种存储海量文件的分布式存储服务。COS 支持多种存储类型：标准存储、低频存储、归档存储、深度归档存储。COS 提供99.9999999999%（12个9）的数据持久性。计费方式按实际使用量付费，无最低消费。",
    },
    {
        "id": "doc_002",
        "title": "腾讯云云服务器 CVM 规格说明",
        "content": "腾讯云云服务器（CVM）提供安全可靠的弹性计算服务。标准型 S 系列适合中小型 Web 应用；计算型 C 系列适合高性能计算场景；内存型 M 系列适合大内存数据库。CVM 支持按量计费和包年包月两种计费模式。",
    },
    {
        "id": "doc_003",
        "title": "腾讯云 TokenHub 大模型平台",
        "content": "TokenHub 是腾讯云大模型服务平台，整合了混元、DeepSeek、GLM 等主流大模型。开发者通过 API Key 即可调用，支持 OpenAI 兼容协议。计费按 Token 使用量计算，输入和输出分别定价。GLM-5 支持 200K 上下文窗口。",
    },
    {
        "id": "doc_004",
        "title": "腾讯云数据库 TencentDB 产品线",
        "content": "腾讯云数据库产品线包括：TencentDB for MySQL（兼容MySQL协议）、TencentDB for PostgreSQL（兼容PostgreSQL）、TDSQL（分布式数据库，适合金融级场景）、MongoDB（文档数据库）。所有产品提供自动备份和高可用架构。",
    },
    {
        "id": "doc_005",
        "title": "腾讯云安全产品：AI 防护盾",
        "content": "AI 防护盾是腾讯云推出的新一代 Web 应用防火墙，基于大模型技术实现智能威胁检测。支持 SQL 注入、XSS、CC 攻击等防护。相比传统规则引擎，AI 防护盾能识别未知威胁，误报率降低 60%。适合金融、政务等高安全要求行业。",
    },
    {
        "id": "doc_006",
        "title": "腾讯云慧眼人脸核身",
        "content": "慧眼是腾讯云人脸核身解决方案，支持活体检测+人脸比对双重验证。适用场景：金融开户、政务认证、医疗实名制。准确率超过99.9%，单次核验仅需3秒。提供 H5、APP SDK、API 多种接入方式。",
    },
]


def simple_retrieval(query: str, top_k: int = 2) -> list:
    """
    简单关键词检索（模拟向量检索）
    真实项目中应使用 Embedding + 向量数据库（如腾讯云向量数据库）
    """
    query_words = set(re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', query.lower()))
    scores = []
    for doc in KNOWLEDGE_BASE:
        text = (doc["title"] + doc["content"]).lower()
        score = sum(1 for w in query_words if w in text)
        scores.append((score, doc))
    scores.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scores[:top_k] if score > 0]


def rag_answer(question: str, verbose: bool = True) -> str:
    """RAG 完整流程：检索 → 注入上下文 → 生成"""
    # Step 1: 检索相关文档
    retrieved_docs = simple_retrieval(question, top_k=2)

    if verbose:
        print(f"  📚 检索到 {len(retrieved_docs)} 篇相关文档：")
        for doc in retrieved_docs:
            print(f"     - {doc['title']}")

    if not retrieved_docs:
        context = "暂无相关文档。"
    else:
        context = "\n\n".join(
            f"【{doc['title']}】\n{doc['content']}" for doc in retrieved_docs
        )

    # Step 2: 构造 RAG 提示（将检索结果作为上下文）
    system = """你是腾讯云的专业客服助手。
请严格基于提供的参考文档回答问题，不要编造文档中没有的信息。
如果文档中没有相关内容，请明确说明"暂无相关资料"。"""

    rag_prompt = f"""参考文档：
{context}

用户问题：{question}

请基于以上文档回答问题。"""

    # Step 3: 生成回答
    return call([{"role": "user", "content": rag_prompt}], system=system, max_tokens=2000)


# ─────────────────────────────────────────────
# 演示 1：RAG vs 直接问答 对比
# ─────────────────────────────────────────────
def demo_rag_vs_direct():
    print("=" * 55)
    print("演示 1：RAG vs 直接问答 对比")
    print("=" * 55)

    question = "腾讯云 COS 的数据持久性是多少？有哪些存储类型？"
    print(f"问题：{question}\n")

    # 直接问答（无上下文）
    direct = call(
        [{"role": "user", "content": question}],
        system="你是AI助手，请基于自身知识回答。",
        max_tokens=2000,
        extra=THINKING_OFF,
    )
    print("【直接问答（无RAG）】")
    print(direct)
    print()

    # RAG 问答
    print("【RAG 增强回答】")
    rag = rag_answer(question)
    print(rag)
    print()


# ─────────────────────────────────────────────
# 演示 2：多轮 RAG 对话
# ─────────────────────────────────────────────
def demo_rag_multi_turn():
    print("=" * 55)
    print("演示 2：多轮 RAG 对话")
    print("=" * 55)

    questions = [
        "TokenHub 支持哪些大模型？",
        "GLM-5 的上下文窗口有多大？",
        "慧眼人脸核身适合哪些行业？",
    ]

    for q in questions:
        print(f"用户：{q}")
        answer = rag_answer(q, verbose=True)
        print(f"AI：{answer}\n")


# ─────────────────────────────────────────────
# 演示 3：知识库外的问题（边界处理）
# ─────────────────────────────────────────────
def demo_out_of_scope():
    print("=" * 55)
    print("演示 3：知识库边界处理")
    print("=" * 55)

    question = "腾讯云的股价是多少？"
    print(f"问题：{question}")
    answer = rag_answer(question, verbose=True)
    print(f"AI：{answer}\n")


# ─────────────────────────────────────────────
# 演示 4：分块策略演示
# ─────────────────────────────────────────────
def demo_chunking_strategy():
    print("=" * 55)
    print("演示 4：文本分块策略对比（概念演示）")
    print("=" * 55)

    long_text = """
    腾讯云数据库产品线覆盖了关系型数据库、NoSQL数据库、时序数据库等多种类型。
    在关系型数据库方面，TencentDB for MySQL 提供高性能、高可用的MySQL兼容服务。
    TencentDB for PostgreSQL 则面向需要高级SQL特性的企业用户。
    TDSQL 是专为金融级场景设计的分布式关系型数据库，支持强一致事务。
    在NoSQL方面，腾讯云提供了 MongoDB 文档数据库服务。
    Redis 缓存数据库支持多种数据结构，适合高并发读写场景。
    此外还有专门面向AI向量检索的向量数据库产品。
    """

    prompt = f"""请演示两种文本分块策略的区别，用以下文本为例：

原文：{long_text}

策略A：固定大小分块（每块约50字，有20字重叠）
策略B：语义分块（按完整语义段落切分）

请分别展示两种策略的分块结果，并说明各自优缺点。"""

    r = call([{"role": "user", "content": prompt}], max_tokens=2000, extra=THINKING_OFF)
    print(r)
    print()


# ─────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Claude 课程第五章 — RAG 检索增强生成")
    print(f"   模型：{MODEL}")
    print(f"   知识库：{len(KNOWLEDGE_BASE)} 篇腾讯云产品文档\n")

    demo_rag_vs_direct()
    demo_rag_multi_turn()
    demo_out_of_scope()
    demo_chunking_strategy()

    print("✅ 第五章演示完成！")
