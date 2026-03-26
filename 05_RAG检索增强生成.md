# 模块 5：RAG 检索增强生成

> **对应课程**：Building with the Claude API — Module 5: Retrieval Augmented Generation  
> **视频数量**：9 个（约 66 分钟）  
> **GitHub Notebook**：无（本模块以架构设计和概念为主）  
> **预计学习时间**：2 小时  
> **难度**：⭐⭐⭐

---

## 本模块学习目标

完成本模块后，你将能够：
1. 理解 RAG 的核心概念和为什么需要它
2. 掌握 RAG 的完整架构：索引→检索→生成
3. 了解不同的 Embedding 模型和向量数据库选择
4. 实现基于 Claude 的 RAG 系统
5. 掌握 RAG 的优化策略（分块、检索增强、Re-ranking）
6. 了解上下文窗口 vs RAG 的权衡
7. 将 Prompt Caching 与 RAG 结合使用

---

## 第一节：为什么需要 RAG？

### 1.1 Claude 的知识局限

Claude 的知识来自训练数据，有以下局限：
- **知识截止日期**：不了解训练后发生的事件
- **无私有数据**：不了解你的公司文档、内部数据库
- **可能幻觉**：对不确定的信息可能"编造"答案

### 1.2 解决方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **RAG** | 灵活、成本低、数据实时更新 | 检索质量影响回答 | 大多数场景 |
| **Fine-tuning** | 深度学习领域知识 | 成本高、数据需求大、不易更新 | 特定风格/格式 |
| **长上下文窗口** | 简单直接 | 成本高、有 token 限制 | 小型知识库 |

### 1.3 RAG = 检索 + 生成

```
用户问题
    ↓
① 检索（Retrieval）：从知识库中找到相关文档片段
    ↓
② 增强（Augmented）：将找到的文档注入到提示中
    ↓
③ 生成（Generation）：Claude 基于上下文生成回答
```

---

## 第二节：RAG 架构详解

### 2.1 索引阶段（离线）

将文档处理成可检索的格式：

```
原始文档 → 分块(Chunking) → 向量化(Embedding) → 存入向量数据库
```

#### 文档分块策略

```python
def simple_chunk(text, chunk_size=500, overlap=50):
    """简单的固定大小分块（带重叠）"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # 重叠确保不丢失上下文
    return chunks

# 更智能的分块 — 按段落/标题分割
def semantic_chunk(text):
    """按段落分块，保持语义完整性"""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) < 1000:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
```

#### 分块最佳实践

| 策略 | 描述 | 适用场景 |
|------|------|---------|
| **固定大小** | 按字符/token 数分割 | 通用场景 |
| **段落分割** | 按 `\n\n` 分割 | 结构化文档 |
| **标题分割** | 按 Markdown/HTML 标题分割 | 技术文档 |
| **语义分割** | 用 AI 判断语义边界 | 高质量需求 |
| **递归分割** | 先大块再细分 | 长文档 |

**关键参数**：
- **chunk_size**：通常 200-1000 tokens
- **overlap**：通常 chunk_size 的 10-20%
- 太小：丢失上下文；太大：引入噪音

#### 文本向量化

```python
# 使用 Voyager（Anthropic 的 Embedding 模型）
# 注意：Anthropic 也推荐使用 Voyage AI 的 Embedding
import voyageai

voyage_client = voyageai.Client()  # 需要 VOYAGE_API_KEY

# 单条文本向量化
result = voyage_client.embed(
    ["This is a test sentence."],
    model="voyage-3"
)
embedding = result.embeddings[0]  # 1024 维向量

# 批量向量化
texts = ["chunk 1 text...", "chunk 2 text...", "chunk 3 text..."]
results = voyage_client.embed(texts, model="voyage-3")
embeddings = results.embeddings
```

```python
# 或使用 OpenAI Embedding（也很流行）
from openai import OpenAI

openai_client = OpenAI()

response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=["This is a test sentence."]
)
embedding = response.data[0].embedding  # 1536 维向量
```

### 2.2 检索阶段（在线）

用户查询时，将查询向量化并找到最相似的文档块：

```python
import numpy as np

def cosine_similarity(a, b):
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, document_embeddings, documents, top_k=5):
    """检索最相关的文档块"""
    # 向量化查询
    query_result = voyage_client.embed([query], model="voyage-3")
    query_embedding = query_result.embeddings[0]
    
    # 计算与所有文档的相似度
    similarities = []
    for i, doc_emb in enumerate(document_embeddings):
        sim = cosine_similarity(query_embedding, doc_emb)
        similarities.append((i, sim))
    
    # 排序并返回 Top-K
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    results = []
    for idx, score in similarities[:top_k]:
        results.append({
            "text": documents[idx],
            "score": score
        })
    
    return results
```

### 2.3 生成阶段

将检索到的文档注入提示，让 Claude 生成回答：

```python
def rag_query(user_question, retrieved_docs):
    """RAG 生成回答"""
    # 组装上下文
    context = "\n\n".join([
        f"<document index=\"{i+1}\">\n{doc['text']}\n</document>"
        for i, doc in enumerate(retrieved_docs)
    ])
    
    prompt = f"""Based on the following reference documents, answer the user's question.
If the answer cannot be found in the documents, say "I don't have enough information to answer this."
Always cite which document(s) you're using by referencing their index numbers.

<documents>
{context}
</documents>

<question>
{user_question}
</question>"""
    
    system_prompt = """You are a helpful assistant that answers questions based on provided documents.
You must ground your answers in the given documents and cite your sources.
If the documents don't contain relevant information, clearly state that."""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text
```

---

## 第三节：完整 RAG 系统实现

### 使用向量数据库

实际生产中，使用专业的向量数据库而非内存计算：

```python
# 方案 1：Chroma（轻量级，适合本地开发）
import chromadb

chroma_client = chromadb.Client()

# 创建集合
collection = chroma_client.create_collection(name="my_knowledge_base")

# 添加文档
collection.add(
    documents=["Document chunk 1...", "Document chunk 2...", "Document chunk 3..."],
    metadatas=[
        {"source": "manual.pdf", "page": 1},
        {"source": "manual.pdf", "page": 2},
        {"source": "faq.md", "page": 1}
    ],
    ids=["doc1", "doc2", "doc3"]
)

# 检索
results = collection.query(
    query_texts=["How to reset password?"],
    n_results=3
)

print(results["documents"])  # 相关文档
print(results["distances"])  # 距离分数
```

```python
# 方案 2：Pinecone（云端托管，适合生产）
from pinecone import Pinecone

pc = Pinecone(api_key="your-api-key")
index = pc.Index("my-index")

# 添加向量
index.upsert(vectors=[
    {"id": "doc1", "values": embedding1, "metadata": {"text": "chunk 1..."}},
    {"id": "doc2", "values": embedding2, "metadata": {"text": "chunk 2..."}},
])

# 查询
results = index.query(vector=query_embedding, top_k=5, include_metadata=True)
```

### 完整 RAG 管道

```python
import anthropic
import chromadb

class RAGPipeline:
    """完整的 RAG 管道实现"""
    
    def __init__(self):
        self.anthropic_client = anthropic.Anthropic()
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection("knowledge")
    
    def ingest_documents(self, documents: list[dict]):
        """
        索引文档
        documents: [{"id": "...", "text": "...", "metadata": {...}}]
        """
        texts = [doc["text"] for doc in documents]
        ids = [doc["id"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        
        # 分块
        all_chunks = []
        all_ids = []
        all_metadatas = []
        
        for i, text in enumerate(texts):
            chunks = semantic_chunk(text)
            for j, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_ids.append(f"{ids[i]}_chunk_{j}")
                all_metadatas.append({
                    **metadatas[i],
                    "original_doc_id": ids[i],
                    "chunk_index": j
                })
        
        # 存入向量数据库（Chroma 会自动做 Embedding）
        self.collection.add(
            documents=all_chunks,
            ids=all_ids,
            metadatas=all_metadatas
        )
        
        print(f"Indexed {len(all_chunks)} chunks from {len(documents)} documents.")
    
    def query(self, question: str, top_k: int = 5) -> str:
        """检索并生成回答"""
        # 1. 检索
        results = self.collection.query(
            query_texts=[question],
            n_results=top_k
        )
        
        # 2. 构建上下文
        context_parts = []
        for i, (doc, metadata) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0]
        )):
            source = metadata.get("source", "unknown")
            context_parts.append(
                f'<document index="{i+1}" source="{source}">\n{doc}\n</document>'
            )
        
        context = "\n\n".join(context_parts)
        
        # 3. 生成
        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system="""You are a knowledgeable assistant. Answer questions based on the provided documents.
Always cite your sources by document index. If you can't find the answer in the documents, say so clearly.""",
            messages=[{
                "role": "user",
                "content": f"""<documents>
{context}
</documents>

Question: {question}

Answer based on the documents above. Cite sources using [Document N] format."""
            }]
        )
        
        return response.content[0].text

# 使用示例
rag = RAGPipeline()

# 索引文档
rag.ingest_documents([
    {
        "id": "handbook_1",
        "text": "Our company offers 20 days of paid time off per year for full-time employees...",
        "metadata": {"source": "employee_handbook.pdf"}
    },
    {
        "id": "policy_1", 
        "text": "Remote work policy: Employees may work from home up to 3 days per week...",
        "metadata": {"source": "remote_work_policy.pdf"}
    }
])

# 查询
answer = rag.query("How many days of PTO do I get?")
print(answer)
```

---

## 第四节：RAG 优化策略

### 4.1 查询增强

```python
def enhanced_query(original_question: str) -> list[str]:
    """
    用 Claude 生成多个查询变体，提高检索覆盖率
    """
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""Generate 3 alternative search queries for the following question.
Each query should approach the topic from a different angle to maximize search coverage.

Original question: {original_question}

Return only the queries, one per line."""
        }]
    )
    
    queries = [original_question]  # 包含原始查询
    queries.extend(response.content[0].text.strip().split('\n'))
    return queries

# 使用多个查询检索，合并并去重结果
queries = enhanced_query("What's the refund policy for damaged items?")
# 可能生成：
# 1. What's the refund policy for damaged items?
# 2. How to return a damaged product?
# 3. Damage claim process and refund timeline
# 4. Policy for defective or broken merchandise
```

### 4.2 Re-ranking（重排序）

检索后用更精确的模型重新排序结果：

```python
def rerank_with_claude(query: str, documents: list[str], top_k: int = 3) -> list[dict]:
    """使用 Claude 对检索结果进行重排序"""
    doc_list = "\n".join([
        f"Document {i+1}: {doc[:200]}..." 
        for i, doc in enumerate(documents)
    ])
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""Given the query and documents below, rank the documents by relevance.
Return ONLY a JSON array of document numbers in order of relevance (most relevant first).

Query: {query}

{doc_list}

Return format: [most_relevant_doc_number, next_most_relevant, ...]"""
        }]
    )
    
    # 解析排序结果
    import json
    ranking = json.loads(response.content[0].text)
    
    reranked = []
    for doc_num in ranking[:top_k]:
        idx = doc_num - 1
        if 0 <= idx < len(documents):
            reranked.append({"index": idx, "text": documents[idx]})
    
    return reranked
```

### 4.3 混合检索（Hybrid Search）

结合向量检索和关键词检索：

```python
def hybrid_search(query, collection, top_k=5):
    """结合语义检索和关键词检索"""
    
    # 语义检索（向量相似度）
    semantic_results = collection.query(
        query_texts=[query],
        n_results=top_k * 2
    )
    
    # 关键词检索（BM25 或简单的全文搜索）
    keyword_results = collection.query(
        query_texts=[query],
        n_results=top_k * 2,
        where_document={"$contains": query.split()[0]}  # 简化的关键词匹配
    )
    
    # 合并并去重（可以用 Reciprocal Rank Fusion）
    seen = set()
    combined = []
    
    for results in [semantic_results, keyword_results]:
        for doc_id, doc_text in zip(results["ids"][0], results["documents"][0]):
            if doc_id not in seen:
                seen.add(doc_id)
                combined.append(doc_text)
    
    return combined[:top_k]
```

### 4.4 上下文窗口 vs RAG

Claude 的 200K token 窗口很大，有时可以直接塞入所有文档：

```python
# 当知识库较小时（< 100K tokens），可以直接使用长上下文
# 结合 Prompt Caching 效果更好

long_document = load_all_documents()  # 假设 < 100K tokens

# 使用缓存避免每次都发送整个文档
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    system=[
        {
            "type": "text",
            "text": f"You are an expert assistant. Here is the complete knowledge base:\n\n{long_document}",
            "cache_control": {"type": "ephemeral"}  # 缓存整个知识库
        }
    ],
    messages=[{"role": "user", "content": "What is the PTO policy?"}]
)
```

**选择策略**：

| 知识库大小 | 推荐方案 |
|-----------|---------|
| < 50K tokens | 直接放入上下文 + Prompt Caching |
| 50K-200K tokens | 直接放入上下文（长文档注意力可能衰减） |
| > 200K tokens | RAG 是唯一选择 |
| 频繁更新的数据 | RAG（向量库易于更新） |
| 静态参考文档 | 长上下文 + 缓存 |

---

## 第五节：生产级 RAG 注意事项

### 评估 RAG 系统

```python
def evaluate_rag(rag_pipeline, test_cases):
    """评估 RAG 系统的质量"""
    results = []
    
    for case in test_cases:
        answer = rag_pipeline.query(case["question"])
        
        # 用 Claude 评判答案质量
        evaluation = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"""Evaluate this answer against the ground truth.

Question: {case["question"]}
Expected Answer: {case["expected_answer"]}
Actual Answer: {answer}

Score on a scale of 1-5:
- Accuracy (does it match the expected answer?)
- Completeness (does it cover all key points?)
- Hallucination (does it include false information?)

Return JSON: {{"accuracy": N, "completeness": N, "hallucination_free": N}}"""
            }]
        )
        
        results.append({
            "question": case["question"],
            "answer": answer,
            "evaluation": evaluation.content[0].text
        })
    
    return results
```

### RAG 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 回答不相关 | 检索质量差 | 优化 Embedding、增加分块重叠 |
| 回答不完整 | Top-K 太小 | 增加检索数量、使用查询增强 |
| 幻觉 | 检索到的内容不够 | 加入"不知道"的约束、引用要求 |
| 延迟高 | 检索或生成太慢 | 使用 Prompt Caching、优化索引 |
| 过时信息 | 知识库未更新 | 建立定期更新机制 |

---

## 练习题

### 练习 1：基础 RAG

使用 ChromaDB，构建一个 RAG 系统：
1. 准备 5-10 篇技术文档（可以从项目的 README 或文档中获取）
2. 实现索引管道（分块 + 存储）
3. 实现检索 + 生成管道
4. 测试 5 个问题并评估回答质量

### 练习 2：RAG 优化

在练习 1 的基础上：
1. 实现查询增强（生成多个查询变体）
2. 实现 Re-ranking
3. 对比优化前后的回答质量

### 练习 3：长上下文 vs RAG

对同一组问题，分别使用：
1. 直接将所有文档放入 200K 上下文
2. 使用 RAG 检索 top-5 相关块

比较回答质量和成本。

---

## 扩展阅读

| 资源 | 链接 |
|------|------|
| Anthropic RAG 文档 | https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation |
| Prompt Caching 文档 | https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching |
| Voyage AI（Embedding） | https://www.voyageai.com/ |
| ChromaDB 文档 | https://docs.trychroma.com/ |
| Anthropic Cookbook - RAG | https://github.com/anthropics/anthropic-cookbook |

---

> **下一模块**：[06_Claude_Code与Computer_Use.md](06_Claude_Code与Computer_Use.md) — 学习 AI 编程助手和桌面操控
