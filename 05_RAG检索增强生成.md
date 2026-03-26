# 模块 5：RAG 检索增强生成

> **对应课程**：Building with the Claude API — Module 4: Retrieval Augmented Generation  
> **视频数量**：9 个（约 66 分钟）  
> **GitHub Notebook**：无（本模块以架构设计和概念为主）  
> **预计学习时间**：2 小时  
> **难度**：⭐⭐⭐

### 📌 原课程地址

| 平台 | 链接 |
|------|------|
| **Skilljar（官方）** | https://anthropic.skilljar.com/claude-with-the-anthropic-api |
| **Coursera（镜像）** | https://www.coursera.org/learn/building-with-the-claude-api |

### 📌 视频课时清单

| # | 视频标题 | 时长 | 核心知识点 |
|:-:|---------|:----:|-----------|
| 1 | Introduction to RAG | 6m | RAG 概念、为什么需要 RAG、基本流程图 |
| 2 | Text Chunking Strategies | 13m | 固定大小分块、递归字符分块、语义分块、重叠 |
| 3 | Text Embeddings | 4m | 文本向量化、余弦相似度、Voyage AI |
| 4 | Complete RAG Pipeline | 8m | 完整流程：加载→分块→嵌入→存储→检索→生成 |
| 5 | Implementing a RAG Pipeline | 5m | 代码实现走读 |
| 6 | BM25 Lexical Search | 10m | BM25 词法搜索、与向量搜索互补 |
| 7 | Multi-Index RAG Pipeline | 7m | 混合搜索架构、结果融合（RRF） |
| 8 | Re-ranking Results | 6m | 交叉编码器重排、提升相关性 |
| 9 | Contextual Retrieval | 6m | Anthropic 独创：为每个块添加上下文前缀 |

> **阅读材料**（2 篇，10 分钟）：Module Introduction / Next Steps

---

## 本模块学习目标

完成本模块后，你将能够：
1. 理解 RAG 的核心概念和为什么需要它
2. 掌握 RAG 的完整架构：索引→检索→生成
3. 了解不同的分块策略和 Embedding 模型
4. 实现基于 Claude 的 RAG 系统
5. 掌握混合检索和重排序优化策略
6. 理解上下文窗口 vs RAG 的权衡

---

## 第 1 课：RAG 概述

> 📹 视频：Introduction to RAG（6 min）

### 为什么需要 RAG？

Claude 的知识来自训练数据，有以下局限：
- **知识截止日期**：不了解训练后发生的事件
- **无私有数据**：不了解你的公司文档、内部数据库
- **可能幻觉**：对不确定的信息可能"编造"答案

### RAG = 检索 + 增强 + 生成

```
用户问题
    ↓
① 检索（Retrieval）：从知识库中找到相关文档片段
    ↓
② 增强（Augmented）：将找到的文档注入到提示中
    ↓
③ 生成（Generation）：Claude 基于上下文生成回答
```

### 解决方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **RAG** | 灵活、成本低、数据实时更新 | 检索质量影响回答 | 大多数场景 |
| **Fine-tuning** | 深度学习领域知识 | 成本高、不易更新 | 特定风格/格式 |
| **长上下文窗口** | 简单直接 | 成本高、有 token 限制 | 小型知识库 |

---

## 第 2 课：文本分块策略

> 📹 视频：Text Chunking Strategies（13 min）

### 分块策略对比

| 策略 | 描述 | 适用场景 |
|------|------|---------|
| **固定大小** | 按字符/token 数分割 | 通用场景 |
| **段落分割** | 按 `\n\n` 分割 | 结构化文档 |
| **递归分割** | 先大块再细分（推荐） | 长文档 |
| **语义分割** | 用 AI 判断语义边界 | 高质量需求 |

### 代码示例

```python
def simple_chunk(text, chunk_size=500, overlap=50):
    """固定大小分块（带重叠）"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # 重叠确保不丢失上下文
    return chunks

def semantic_chunk(text):
    """按段落分块，保持语义完整性"""
    paragraphs = text.split('\n\n')
    chunks, current_chunk = [], ""
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

**关键参数**：chunk_size 通常 200-1000 tokens，overlap 通常 10-20%。太小丢失上下文，太大引入噪音。

---

## 第 3 课：文本嵌入

> 📹 视频：Text Embeddings（4 min）

### 将文本转为向量

```python
# 使用 Voyage AI（Anthropic 推荐的 Embedding 模型）
import voyageai

voyage_client = voyageai.Client()
result = voyage_client.embed(["This is a test sentence."], model="voyage-3")
embedding = result.embeddings[0]  # 1024 维向量
```

### 余弦相似度计算

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

---

## 第 4 课：完整 RAG 流程

> 📹 视频：Complete RAG Pipeline（8 min）

### 索引阶段（离线）

```
原始文档 → 分块(Chunking) → 向量化(Embedding) → 存入向量数据库
```

### 检索阶段（在线）

```python
def retrieve(query, document_embeddings, documents, top_k=5):
    """检索最相关的文档块"""
    query_embedding = voyage_client.embed([query], model="voyage-3").embeddings[0]
    
    similarities = [(i, cosine_similarity(query_embedding, doc_emb))
                    for i, doc_emb in enumerate(document_embeddings)]
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return [{"text": documents[idx], "score": score} for idx, score in similarities[:top_k]]
```

### 生成阶段

```python
def rag_query(user_question, retrieved_docs):
    """RAG 生成回答"""
    context = "\n\n".join([
        f'<document index="{i+1}">\n{doc["text"]}\n</document>'
        for i, doc in enumerate(retrieved_docs)
    ])
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system="You are a helpful assistant. Answer based on provided documents. Cite sources.",
        messages=[{
            "role": "user",
            "content": f"<documents>\n{context}\n</documents>\n\nQuestion: {user_question}"
        }]
    )
    return response.content[0].text
```

---

## 第 5 课：实现 RAG 管道

> 📹 视频：Implementing a RAG Pipeline（5 min）

### 使用向量数据库的完整实现

```python
import anthropic
import chromadb

class RAGPipeline:
    def __init__(self):
        self.anthropic_client = anthropic.Anthropic()
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection("knowledge")
    
    def ingest_documents(self, documents):
        """索引文档：分块 + 存储"""
        all_chunks, all_ids, all_metadatas = [], [], []
        for i, doc in enumerate(documents):
            chunks = semantic_chunk(doc["text"])
            for j, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_ids.append(f"{doc['id']}_chunk_{j}")
                all_metadatas.append({**doc.get("metadata", {}), "original_doc_id": doc["id"]})
        
        self.collection.add(documents=all_chunks, ids=all_ids, metadatas=all_metadatas)
        print(f"Indexed {len(all_chunks)} chunks from {len(documents)} documents.")
    
    def query(self, question, top_k=5):
        """检索 + 生成"""
        results = self.collection.query(query_texts=[question], n_results=top_k)
        
        context = "\n\n".join([
            f'<document index="{i+1}" source="{meta.get("source", "unknown")}">\n{doc}\n</document>'
            for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0]))
        ])
        
        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system="Answer based on provided documents. Cite sources using [Document N] format.",
            messages=[{"role": "user", "content": f"<documents>\n{context}\n</documents>\n\nQuestion: {question}"}]
        )
        return response.content[0].text
```

---

## 第 6 课：BM25 词法搜索

> 📹 视频：BM25 Lexical Search（10 min）

### BM25：基于关键词的传统搜索

BM25 基于 TF-IDF 原理，擅长精确的关键词匹配，与向量搜索形成互补：

- **向量搜索**：擅长语义相似（"汽车" 能匹配 "轿车"）
- **BM25**：擅长精确匹配（专有名词、型号、ID 等）

两者结合 = 混合搜索，效果 > 单独使用任一种。

---

## 第 7 课：混合搜索架构

> 📹 视频：Multi-Index RAG Pipeline（7 min）

### 向量索引 + BM25 索引并行检索

```python
def hybrid_search(query, collection, top_k=5):
    """结合语义检索和关键词检索"""
    semantic_results = collection.query(query_texts=[query], n_results=top_k * 2)
    keyword_results = ...  # BM25 检索
    
    # 使用 Reciprocal Rank Fusion (RRF) 合并结果
    # RRF_score = Σ 1/(k + rank_i)  对每个检索系统的排名求和
    ...
```

---

## 第 8 课：重排序

> 📹 视频：Re-ranking Results（6 min）

### 用交叉编码器重新排序检索结果

初步检索后，用更精确（但更慢）的模型重新排序，提升 Top-K 的相关性。

可以用 Cohere Reranker，也可以用 Claude 本身做重排：

```python
def rerank_with_claude(query, documents, top_k=3):
    """使用 Claude 对检索结果重排序"""
    doc_list = "\n".join([f"Document {i+1}: {doc[:200]}..." for i, doc in enumerate(documents)])
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"Rank these documents by relevance to the query. Return JSON array of doc numbers.\n\nQuery: {query}\n\n{doc_list}"
        }]
    )
    ranking = json.loads(response.content[0].text)
    return [documents[n-1] for n in ranking[:top_k]]
```

---

## 第 9 课：上下文检索

> 📹 视频：Contextual Retrieval（6 min）

### Anthropic 独创：存储前为每个块添加上下文前缀

普通分块的问题：块脱离了原文档上下文后，可能变得含糊不清（如"他在第三章提到了..."——谁是"他"？哪本书？）。

**解决方法**：在存储每个块之前，先用 Claude 为其生成一段上下文前缀，说明这个块来自哪里、讲的是什么主题。

---

## 补充：上下文窗口 vs RAG 选择策略

| 知识库大小 | 推荐方案 |
|-----------|---------|
| < 50K tokens | 直接放入上下文 + Prompt Caching |
| 50K-200K tokens | 直接放入上下文（注意力可能衰减） |
| > 200K tokens | RAG 是唯一选择 |
| 频繁更新的数据 | RAG（向量库易于更新） |
| 静态参考文档 | 长上下文 + 缓存 |

---

## 练习题

### 练习 1：基础 RAG

使用 ChromaDB 构建 RAG 系统：准备 5-10 篇文档，实现索引+检索+生成管道。

### 练习 2：RAG 优化

在练习 1 基础上实现查询增强和 Re-ranking，对比优化前后。

### 练习 3：长上下文 vs RAG

对同一组问题，分别用直接塞入 200K 上下文和 RAG top-5 检索，比较质量和成本。

---

## 扩展阅读

| 资源 | 链接 |
|------|------|
| Anthropic RAG 文档 | https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation |
| Prompt Caching 文档 | https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching |
| Voyage AI | https://www.voyageai.com/ |
| ChromaDB | https://docs.trychroma.com/ |

---

> **下一模块**：[06_Claude_Code与Computer_Use.md](06_Claude_Code与Computer_Use.md) — 学习 AI 编程助手和桌面操控
