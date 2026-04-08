# 模块 5：RAG 检索增强生成

> **对应课程**：Building with the Claude API — Module 4: Retrieval Augmented Generation  
> **视频转录**：7 个（视频 37-43，已嵌入文字）  
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


> 🎬 **视频 37**：Introducing Retrieval Augmented Generation  
> 📁 文件：[37. Introducing Retrieval Augmented Generation.mp4](videos/37.%20Introducing%20Retrieval%20Augmented%20Generation.mp4)

**核心内容**：RAG（检索增强生成）概念入门。
**关键要点**：
- RAG 让 Claude 利用私有数据源增强回复
- 基本流程：用户查询 → 检索相关文档 → 将文档作为上下文发给 Claude → 生成增强回复
- 解决 Claude 无法访问私有/实时数据的问题

<details>
<summary>🇨🇳 查看中文翻译</summary>

在本模块中，我们将深入讨论一种叫做检索增强生成（RAG）的技术。在这个视频中，我想让你对 RAG 有一个非常清晰的认识。

为了帮助你理解 RAG，我们来看一个简单的例子。假设你有一份非常大的金融文档，可能有 100 到 1000 页。我们可能想问 Claude 关于文档中非常具体区域的非常具体的问题。例如，我们可能想问"这家公司有哪些风险因素？"这份文档中可能有相关信息，所以我们需要解决一个根本问题：如何把文档中的信息传给 Claude 以帮助我们回答问题？

**方案一**：我们可以把文档中所有文本直接放入提示中——包含用户问题和文档全部文本。但这不是最佳方案。首先，Claude 能接收的文本量有硬性限制，如果文档非常长，直接放入会报错。其次，随着提示变长，Claude 的理解效果会下降。最后，更大的提示意味着更高的处理成本和更长的等待时间。所以方案一在某些场景可以工作，在其他场景可能完全失败。

**方案二（RAG）**：分两步走。第一步，把文档所有文本拆分成小块。第二步，当用户提问时，我们把问题放入提示，但额外做一步——仔细分析用户问题，找到与问题最相关的文本块。例如，如果用户问"这家公司面临什么风险"，而我们有一个关于风险因素的文本块，就把这个块加入提示中。这样 Claude 就能聚焦在这一小段相关内容上，而不是整个金融文档。

方案二的优点是：Claude 可以聚焦于相关内容；能扩展到非常大的文档甚至多文档场景；提示通常更小，处理更快、成本更低。但缺点也很明显：复杂度更高——需要预处理步骤（拆分文档为块）；需要找到某种方式搜索这些块找到最相关的；找到的块不一定包含 Claude 回答问题所需的全部上下文；而且分块方式有很多种（等分、按标题分等），需要评估哪种最适合你的应用。

正如你猜到的，方案二就是 RAG。在考虑实现 RAG 时，我们需要分析所有这些步骤，判断它是否适合我们的特定用例。现在你已经对 RAG 有了非常高层的理解，接下来让我们开始看看实际的实现过程。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

In this module, we are going to discuss a tremendous amount about a technique referred to as retrieval augmented generation, or RAG for short. In this video in particular, I want to give you a really solid idea of what RAG is all about. To help you understand RAG, we're going to walk through a very quick example. So I want you to imagine that you have a very large financial document, like the one seen on the right-hand side. There might be a tremendous amount of text in this, and might have anywhere from who knows 100 to 1000 pages. And we might want to ask Claude, very specific questions about very specific areas of the document. For example, we might want to ask a question like, what risk factors does this company have? Now presumably, this document might have some relevant information inside of it. So we need to solve a very fundamental issue here. How do we get some information out of this document and into Claude so we can help us answer our question? I want to show you two possible ways that we could solve this problem. So option number one, we could take all of the text out of this document and just place it directly into a prompt, like the one you see on the right-hand side. So we might ask Claude to answer a user's question, we'll then put in the user question, and then take all the text out of the document and put it into the prompt as well. Now this is perhaps not the best solution. It might work, it also might not. Just so you know, there is a hard limit on how much text we can feed into Claude. So if this document is really, really long and we take all the text out of it and feed all the text into Claude, we might immediately end up getting an error, which means just right out the gate, this solution would not work if our document is really, really long. The second problem with this approach is that Claude gets a little bit less effective as your prompt gets longer. So if you start putting a tremendous amount of text into a prompt, Claude is going to have just harder time understanding exactly what you want and answering your question because there is just a tremendous amount of information inside the prompt. And then finally, larger prompts cost more money to process and take longer to process. So there is a financial burden here as well and a user experience burden because they just have to wait around longer to get back some kind of answer. So option number one might work in some scenarios, in other scenarios, it might fail entirely. So that mind, let's take a look at option number two. Option number two is a little bit more complex. So option number two has two separate steps. In step one, we'll take all the text out of the document and break it up into small chunks. Then whenever a user asks a question, we're going to take their question and put it into the prompt as before. But we're also going to go through an extra little step. We're going to examine the user's question very closely and we're going to find a chunk of text that seems most relevant to the user's question. In this case, if a user asks us what risk does this company face and we have a chunk of text right here that seems to be about risk factors, we would then take that chunk of text and include it inside of the prompt. So now we are focusing all of Claude's attention on just this very small snippet of the overall financial document and hopefully Claude can do a much better job of answering the user's question than before when we were just putting all of the text of the document into the prompt. So option number two has a distinct set of upsides and downsides. The upsides here are that Claude can focus on just the relevant content. Secondly, this can scale up to really, really large documents with a tremendous number of pages and it also works if we have multiple documents. We can take all these different documents, separate them all into chunks and then once again, only include chunks relevant to user's question inside of a prompt. This technique also generally leads to much smaller prompts, which means it's going to take less time to run and it's going to cost us a lot less. But there are some big downsides to this approach as well. First off, there's just naturally a lot more complexity. This requires a pre-processing step where we take all the text out of the document and split it into chunks. We also have to figure out some way of searching through all these chunks to find the ones that are most relevant to the user's question and we even need to define what it means to be relevant to the user's question. When we do find some relevant chunks and include them in the prompt, there's really no guarantee that they will contain all the context that Claude needs to actually answer the question. If the user asks what risk does this company face and include only the risk factor section, that might include some other important area of the document, maybe strategy outlook, where some of those risks get addressed in some way. And then finally, there are many different ways in which we can split the text up. So we could just take all the text of the document and divide it into equal portions. Or we could go through the document and find all these different headers and say for every header, we're going to make a new chunk. So we might have chunk one and then two and then three somewhere down here. There are many different ways in which we can define what a chunk is. And so we have to do a little bit of evaluation and decide which technique is the best for our particular application. So as you might guess, option number two is rag. It is retrieval augmented generation. As we just discussed, rag has many big upsides and many big downsides as well. There's a lot of technical challenges around it. It requires a pre-processing step. We also have to figure out some kind of searching mechanism to find those relevant chunks. We have to chunk documents. All in all, there's just a lot more work than option number one. So whenever we are considering implementing rag inside an application, we really have to analyze all these different steps and figure out whether or not it is right for our particular use case. All right, so now we have kind of a very, very high level understanding of what rag is all about. Let's start to take a look at the actual implementation of this process in just a moment.

</details>

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


> 🎬 **视频 38**：Text chunking strategies  
> 📁 文件：[38. Text chunking strategies.mp4](videos/38.%20Text%20chunking%20strategies.mp4)

**核心内容**：文本分块策略——RAG 管道的数据预处理步骤。
**关键要点**：
- 固定大小分块：按字符/token 数量切分，可设置重叠区域
- 递归分块：按段落、句子、词语递归分割
- 语义分块：基于内容含义的智能分组
- 块大小需在上下文完整性和检索精度间权衡

<details>
<summary>🇨🇳 查看中文翻译</summary>

在这个视频和接下来几个视频中，我们将在一系列 Notebook 中实现自己的 RAG 工作流。我们首先构建最简单的基础 RAG，然后逐步添加额外步骤。

回顾一下，典型的 RAG 管道是这样的：取一个源文档，拆分成文本块，然后当用户提问时，找到相关的文本块放入提示中。第一步——把文档拆分成块——是整个 RAG 管道中最复杂的步骤之一，因为分块方式对 RAG 质量影响巨大。

举个例子来说明为什么分块如此重要。假设有一份源文档，包含三个区域：标题、医学研究部分和软件工程部分。如果我们按行分成五个块，会发现一个有趣的问题：第三个块全是关于医学研究的，但它包含"bug"这个词，看起来像是在谈软件工程；而软件工程部分提到了"infection vectors"（感染向量），这更像医学术语。

现在想象用户问"工程师今年修了多少 bug？"我们的 RAG 系统需要找到最相关的块——用户提到了"bug"，所以医学研究那个块看起来相关（因为包含"bug"），但这完全是错误的结果。**这就是分块策略如何轻易引入巨大错误的例子**。

我们将讨论三种分块策略来解决这个问题：

**1. 基于大小的分块（Size-based Chunking）**：把文档按等长字符串分割。这是最简单的技术，也是生产中最常见的。例如一个 325 字符的文档可以分成三个约 108 字符的块。但缺点是每个块可能有截断的单词，而且缺少上下文（比如丢失了章节标题）。解决方法是**重叠策略**——在块的两侧包含相邻块的部分字符，虽然有重复文本，但每个块有了更多上下文。

**2. 基于结构的分块（Structure-based Chunking）**：根据文档结构（标题、段落、章节）来分割。如果文档是 Markdown 格式，可以按 `##` 标记分割。这能得到格式最好的块，但前提是文档有明确的结构标记。对于纯文本 PDF 等没有格式保证的文档，实现起来很困难。

**3. 基于语义的分块（Semantic-based Chunking）**：把文本分成句子或段落，然后用自然语言处理技术判断相邻句子的相关性，将相关的句子组成块。这是最高级的技术，实现复杂度也最高。

在配套 Notebook（001_chunking）中，我实现了三种策略：`chunk_by_character`（按字符大小分块+重叠）、`chunk_by_sentence`（按句子分块+重叠）、`chunk_by_section`（按章节标记分块）。

测试结果：按字符分块默认设置（150字符/20重叠）效果不好，每个块缺少足够信息。调整到500字符/150重叠后好了很多。按句子分块（默认5句/1句重叠）看起来相当不错。按章节分块效果最强——每个块恰好是一个完整章节。

**选择哪种策略完全取决于你的文档性质和结构保证**。按章节分块效果最好，但需要文档有明确格式。如果接收用户上传的文档（格式不可控），按句子分块是好的退路。如果连句子分割都不靠谱（比如代码中的句号位置不规则），就退回到按字符分块——不保证最佳结果，但在绝大多数情况下都能合理工作。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Inside of this video and the next couple of videos, we're going to start to implement our own custom rag workflow Inside of a series of different notebooks. We're going to first focus on just making the most simple basic rag setup We can possibly make and then we're going to add in some additional steps over time now as a reminder a typical rag pipeline Looks a little bit like this to really simplify things We're going to take a source document break it up into chunks of text then whenever user asks us a question We're going to find some relevant chunk of text put it into a prompt and that's pretty much the entire thing So step one of this entire flow is to take a source document and break it up into chunks of text now Believe it or not this process of taking a document and breaking it up into separate chunks is one of the more complex steps of the entire rag pipeline simply because how we chunk our document up has a huge output on the quality of our rag pipeline And I want to give you an example right away to help you understand why that's the case So take a look at this source document It's just a couple of little lines and it's supposed to can represent some kind of report from a company or something like that and Just reading through it really quickly. We can see there's really three general areas We have a header we have a section about medical research and then a section about software engineering Now there are many ways in which we could divide this thing up into separate chunks But I'm just going to suggest one way I'm going to say for every kind of distinct line inside this document We're going to make a separate chunk so it would end up with about five separate chunks like the ones you see right here If you consider each of these different chunks now, you will notice something really interesting The third chunk of text right here is all about medical research That's what this text is about it was inside of the medical research section But it contains the word bug so at kind of a high level if you just glanced at this paragraph alone It is almost like it's kind of about software engineering just because it contains the word bug And then likewise down here we have the software engineering section and inside of it is the word infection vectors Infection vectors is a little bit more of a medical term So once again, we have a section that is about software engineering But the language inside of it is kind of about medical research So now we want you to think about what would happen if we took these chunks and we add them into our rag pipeline Let's imagine that user asked a question of something like how many bugs did engineers fix this year? So now our job as a part of the rag pipeline would be to find the chunks of text we have that are most relevant for the user's question Well, the user said something about bugs So well at first glance this chunk of text right here seems relevant just because it contains the word bug So we might decide to take this chunk of text and add it as context into the overall prompt and As you can tell right away, this is a huge error The user wants to understand something about software engineering from the report So we definitely wanted this section, but we erroneously got something about medical research instead So this is an example where a chunking strategy can easily introduce Huge errors and very bad context inserts into your prompt so to solve this problem We're going to spend a lot of time thinking about how we're going to take our original source document and break it up into different chunks of text In this video, we're going to cover three different chunking strategies or methods to divide our document into separate chunks of text Each of which have some feature or some technique meant to address the problem that we just saw So we are going to discuss size based chunking structure based and semantic based the first one We're going to cover is size based chunking. This is where we take our big old document So a big chunk of text and we just divide it into a number of strings of equal length This is by far the easiest technique to implement and in some also probably the one you're going to see most often in production implementations So let's take a look at how size based chunking is done with size based chunking We're going to take our original document and divide it into some number of strings of more or less equal length In our particular case, we have a source document with about three hundred and twenty five characters So we could decide just completely arbitrarily to divide that into three separate chunks That means each chunk would have about a hundred and eight characters or so So we might take the first hundred eight characters put them into chunk one the next hundred and eight put them into chunk two and Just repeat for the entire document Now very simple technique, but right away it has a big downside and that is that each chunk is probably going to end up with some Number of cutoff words inside of it. You could see right away the first chunk has the word significant cutoff So it's just significant in the first chunk and then it ends the word in the next one in addition each chunk ends up lacking context So for example the third chunk down here unfortunately does not really include the section header that was right above it And this section header would have provided a lot of context on what this text right here is really talking about So to solve this problem that starts to come up right away if you use size based chunking we can implement a overlap Strategy and overlap strategy is where we are still going to do size based chunking But we're also going to include a little bit of overlap from the neighboring chunks So for example, we have the original chunk one right here But we might decide to include just a number of characters from the next chunk down So in this case we might include the rest of the word significant plus the end of that entire sentence So we would end up with a chunk that looks like this that just has a little bit more meaning to it and then for chunk two We would still have the body be this area right here But we'd include an overlap of some number of characters from before the chunk and after the chunk So with the strategy we are going to end up with a decent amount of duplicated text for example in this case We have section one medical research inside the second chunk and that was also included inside the first one as well So there is duplication of text but the upside here is that each chunk of text has in general a little bit more context provided for it The next kind of strategy that you're going to see is structure based chunking This is where we are going to divide off the text based upon the overall structure of our document So we might try to find headers or paragraphs or general sections and use those as our dividing lines for each chunk Implementing this strategy of chunking with our document would be really easy because our document is written with markdown syntax We know that because it has a little pounds Right here the double hashes for each section So we might look for these little pound symbols and then say that every time we see this kind of symbol That means we must be starting a brand new section So we could very easily write out some code to programmatically split on the double hash characters And we would end up with some pretty well-formed sections like what you see right here Now this might sound like a fantastic strategy, but unfortunately reality just doesn't favor it quite so often In many cases you are going to be trying to ingest documents that are not formatted with markdown syntax at all They might be plain PDF documents that just contain plain text in which case you will not get these very clearly Delineated sections So again, even though this seems like a great technique Implementing it can be really challenging Especially if you do not have any guarantees around the structure of your different documents The last chunking strategy that we are going to discuss is semantic based chunking This is where you might take all of your text Divide it up into sentences or sections and then use some kind of natural language processing technique to figure out how related Each consecutive sentence is You'll then build up your chunks out of groups of these somehow related sentences or sections Now as you can tell just by the description This is by far Definitely more advanced technique So we're not going to look too closely into the actual implementation The only reason I mentioned it at all is just to make it clear that there's really no set finite fixed number of chunking strategies There's really an infinite number of ways in which we can decide to divide up our text And so deciding upon which method you use really comes down to your particular use case And what guarantees you have around the documents that you are trying to ingest Now before we move on I want to go over a very quick example with you So I've got a Jupyter notebook put together with three different chunking strategies implemented inside of it So I would encourage you to find the notebook called 001 chunking Also make sure that you download the accompanying report.md file and place it inside the same directory as that notebook This report.md file has a little sample kind of fictional report inside of it That we're going to use for testing purposes as we learn about how to implement a rag pipeline So inside of here you'll find a couple of different cells The first one contains a sample implementation of a chunk by character So this is an implementation based upon the size based strategy Where we are going to divide up our text into strings of equal length that also have some amount of overlap on them You'll notice that the arguments are going to be the text the size of each chunk and then some amount of chunk overlap So again, that is the number of characters we want to have on either side of the chunk The next cell shows how we might chunk by sentence So very similar idea, but now I'm using a regular expression to split the text up into individual sentences And then each chunk will be formed out of some number of sentences with optionally a little bit of overlap on each side And then finally if we have really strong guarantees around the structure of our document and its exact contents We might try to use a chunk by section which would be a example of structure based chunking So in this example, it's going to look for a new line character And then two pound signs and then a space and that is going to be our separation criteria So we would get kind of executive summary would be the first chunk, well technically the second one This would be the first chunk up here, but then we would get everything inside the executive summary All the way down to the table of contents that would start off our second chunk And then the next chunk would be the methodology and then section one and so on This will give us the best formatting for each chunk because each chunk will consist of exactly one section But it really only works because we have a guarantee around the structure of the document We know it is marked down and we know that we're only going to see that new line pound pound space In the case that we have a new section beginning Now let's test each of these really quickly So back inside my notebook, I'm going to go down to the bottom cell And I'm going to first try out the chunk by character So I'm opening up the file, getting all the text out of it I'm going to chunk by character and then just print out each chunk with a little separator between each one So I'll run that And now we'll see that we get our first chunk right here, second and so on And right away you can see that the default settings do not produce very good chunks So the default settings are a chunk length of 150 with a overlap of 20 So in this case each chunk Doesn't really provide a whole lot of meaning like what does this sentence right here really do for us And can we really use it to answer any user question? I don't know maybe not So we might decide to dramatically change our default settings here Maybe I want a chunk length of 500 with a overlap of 150 Let's see if that gives us something a little bit better Okay, that's a little bit better than what we had before So now I can start to see the formation of actual individual sections here That give us a little bit of information You'll also very quickly start to notice the overlaps So I can see addressing complex challenges Let's turns out that exact phrase is included inside of the chunk right above So that's an example of the overlapping that we get All right next up. Let's try our second strategy Which is chunk by sentence and again, I'm going to use the default arguments And this one actually looks like it's pretty strong So this should give us five sentences by default in each chunk with one sentence of overlap And we are using a regular expression to split up each sentence So there might be cases where it doesn't split a sentence correctly But at first glance, yeah, I'd say this looks pretty good Each chunk appears to give us a solid amount of information And then finally we can try out chunk by section Now run that And now we can see that the first chunk is not going to contain a lot of useful information But everything after that is really really strong Because we are getting exactly a single section each time I get just the executive summary And then the table of contents And then section one, section two, section three, and so on So once again, which strategy you use entirely comes down to the nature of your document And what guarantees you have around its structure For us, chunk by section looks fantastic But if we are expecting to receive a user-provided documents Where there are no guarantees around the formatting of each document Then using chunk by section is probably not going to work out in the long run In that case, we might fall back to chunk by sentence But even this might not work pretty well, work out pretty well Imagine that we are trying to chunk user-provided code, for example Well, if we try to split code up into individual sentences We are probably going to get a lot of unexpected results Because code tends to have periods in very unexpected places So that might mean that we just fall back to the old reliable standard Which is chunk by character Chunk by character is not guaranteed to give you the best results But it's going to work vast majority of the time And it's going to work out reasonably well

</details>

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


> 🎬 **视频 39**：Text embeddings  
> 📁 文件：[39. Text embeddings.mp4](videos/39.%20Text%20embeddings.mp4)

**核心内容**：文本嵌入（Text Embeddings）——将文本转为数值向量用于语义搜索。
**关键要点**：
- 嵌入将文本映射到高维向量空间
- 语义相似的文本向量距离更近
- 使用余弦相似度衡量文本相似程度
- Voyage AI 等模型可生成高质量嵌入向量

<details>
<summary>🇨🇳 查看中文翻译</summary>

从源文档中提取文本块之后，RAG 管道的下一步是等待用户提交问题，然后在所有文本块中找到与用户问题相关的那些块，将它们作为上下文添加到提示中。

这个"找到相关文本块"的过程本质上是一个**搜索问题**。RAG 管道中最常见的实现方式是**语义搜索**，它利用**文本嵌入（Text Embeddings）**来理解每个文本块的含义，并找到与用户问题最相关的块。

**什么是文本嵌入？** 文本嵌入是文本含义的数值表示——一长串数字的列表。我们把文本输入**嵌入模型**（如 Voyage AI），模型输出一个列表，列表中的每个数字在 -1 到 1 之间。

每个数字代表输入文本某个特质的评分。虽然实际上我们不知道每个数字具体对应什么特质，但可以这样想象：第一个数字可能是"这段文本有多开心"的评分，第二个是"这段文本多大程度在谈论水果"，等等。这些标签是虚构的，但这种思维方式非常有助于理解嵌入。

**如何生成嵌入？** Anthropic 目前不提供嵌入生成功能，推荐使用 **Voyage AI**（独立公司，需要单独注册和 API Key，但可以免费开始使用）。注册后将 API Key 添加到 `.env` 文件中，变量名为 `VOYAGE_API_KEY`。

在配套 Notebook（002_embeddings）中，我提供了一个 `generate_embedding` 函数，接收文本并返回嵌入向量。运行后可以看到，生成嵌入非常快速简单。**真正的挑战不是创建嵌入，而是理解它们如何融入整个 RAG 管道**——这是我们接下来要深入探讨的话题。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

After extracting some number of text chunks out of a source document, the next step inside of our rag pipeline is to wait for a user to submit a question or a query or something like that. And whenever that occurs, we need to take a look at all of our different text chunks and find some number that seem to be somehow related to the user's question, so that we can add them as context into our prompt. Now, this process of finding some number of text chunks that are related to the user's question, oh, there's a lot of complexity hidden there. But when we really think about it, this truly is a search problem. We want to take the user's question and search through all of our different chunks until we find some related content. And then surface those in some way. The most common way of implementing this inside of a rag pipeline is by implementing a system known as semantic search. Semantic search utilizes something called text embeddings to better understand what each chunk of text is all about and somehow find the chunk of text most related to the user's question. Now, we're going to spend a decent amount of time now to focus on text embeddings and really understand what they are doing for us. So let's take a look at a couple of diagrams. A text embedding is a numerical representation of the meaning contained in some text. These text embeddings are generated by something called an embedding model. We feed text into an embedding model, such as I'm very happy today, and the embedding model is going to spit out a long list of numbers. That long list of numbers is our actual embedding. The numbers inside the embedding can range from negative one up to positive one. So now the question is, what do these numbers really mean? Each number inside of an embedding represents a score of some quality of the input text. Now, this is where things get a little confusing because I'm showing two conflicting ideas in this diagram. Let me break this down for you and just be super clear. In reality, we do not know what quality each number inside the embedding is actually tied to. So when I label that first number and say, this is a score of how happy the text is, that's not entirely accurate. We simply don't know what that first number truly represents. Nonetheless, it is very helpful to think of these numbers in that way. It is helpful to imagine that the first number might be one score of how happy the text is. And the second is how much the text is talking about fruit, etc. Again, these labels are completely made up by me, and we don't actually know what each number represents, but it's extremely helpful to think about embeddings in this way. So that's how you really want to picture each of these numbers. They are kind of like scores of some different qualities of the input text. The last thing you need to understand is how to actually generate these embeddings. Anthropic does not currently provide embedding generation. Instead, the recommended provider is Voyage AI. This is a separate company, so requires sign up of a separate account and a different API key. However, it is free to get started and super easy to use. Attach to this lecture is a PDF that will walk you through the process of creating an account and getting an API key. Once you have generated the API key, you need to add it into your .env file right next to your existing Anthropic API key. Make sure you assign it to a variable named Voyage underscore API underscore key. So then right there, you'll put the generated key that you just got. Once you have updated the .env file, I would also encourage you to download attached to this lecture a new .env file called .002 embeddings. At the very top, you'll find a command that you need to run in order to install the Voyage AI SDK. So make sure you run that command to install the library. Lower on down inside this notebook, I've already put together a function for us called generate embedding. This function is going to take in some piece of text and then return in embedding for it, pretty much as simple as it gets. So if I run all the cells inside here and then run the bottom cell, which is currently opening up the report, chunking the reports, and then taking the first chunk and passing into generate embedding. If I then run the cell, I'll get back my list of embeddings. As you can see, generating embeddings is rather quick and rather painless. So the real challenge here is not creating embeddings, it's understanding how they actually fit into our overall rag pipeline. So that's going to be the next topic that we investigate.

</details>

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


> 🎬 **视频 40**：The full RAG flow  
> 📁 文件：[40. The full RAG flow.mp4](videos/40.%20The%20full%20RAG%20flow.mp4)

**核心内容**：端到端 RAG 流程——从数据预处理到查询回复。
**关键要点**：
- 预处理：文档分块 → 嵌入向量化 → 存入向量数据库
- 查询：用户查询嵌入 → 向量相似度检索 → 获取相关块 → 作为上下文发给 Claude
- 向量数据库实现高效的语义搜索
- Claude 基于检索到的上下文生成准确回复

<details>
<summary>🇨🇳 查看中文翻译</summary>

到目前为止，我已经给你高层概述了 RAG 管道的工作原理，我们讨论了文本分块，也初步接触了文本嵌入。现在我们要把这三个话题合并在一起，彻底理解整个 RAG 管道。我们将逐步详解一个完整的 RAG 示例。

**第一步：分块。** 和之前一样，我们把源文档拆分成文本块。这个例子中，假设我们有两个块——"医学研究"和"软件工程"。

**第二步：为每个块生成嵌入。** 我们用一个假想的"完美嵌入模型"来说明（这个模型只返回长度为 2 的嵌入，且我们知道每个数字代表什么）。第一个数字代表"文本在多大程度上谈论医学领域"，第二个代表"谈论软件工程的程度"。

医学研究块嵌入大约是 (0.97, 0.34)——绝对在谈医学，但"bug"这个词有一点软件工程的含义。软件工程块大约是 (0.3, 0.97)——绝对在谈软件工程，但"infection vectors"有医学含义。

生成嵌入后，我们要做一步**归一化**（Normalization），把每对向量的长度缩放到 1.0。这一步通常由嵌入 API 自动完成。归一化后，我们可以在单位圆上可视化这些嵌入。

**第三步：存入向量数据库。** 向量数据库是专门为存储、比较和查找长数字列表（即嵌入）而优化的数据库。存好后，我们就暂停等待用户提交查询。

**第四步：用户提问，生成查询嵌入。** 假设用户问"我想了解这家公司，特别是软件工程部门今年做了什么？"我们把这个问题通过同一个嵌入模型，得到类似 (0.1, 0.89) 的嵌入——明确在问软件工程。归一化后，我们用向量数据库搜索最相似的嵌入。

**背后的数学：余弦相似度。** 这是向量数据库内部计算相似度的方法——计算用户查询向量与每个存储向量之间角度的余弦值。结果在 -1 到 1 之间：接近 1 表示非常相似，接近 -1 表示完全不相似。在我们的例子中，用户查询与软件工程块的余弦相似度是 0.983，表示非常相似。

还有一个概念叫**余弦距离**（Cosine Distance），等于 1 减去余弦相似度。值接近 0 表示高相似度。你会在向量数据库文档中经常看到这个术语，注意区分。

**第五步：构建提示并调用 Claude。** 找到高相似度的文本块后，把用户问题和检索到的文本块一起放入提示，发送给 Claude。这就是整个 RAG 过程的完整细节。理解了从头到尾的所有技术和数学原理后，接下来我们就在 Notebook 中实现它。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

At this point in the module, I've given you a high-level overview of how the RagnPypline works. We've spoken a little bit about text chunking, and we've got just a taste of text embeddings. So now we're going to take these three different topics, our high-level overview of the Ragn process, text embeddings and text chunking, and we're going to merge them all together and really understand the entire RagnPypline. So we're going to go through a complete RagnExample and go through a lot of detail and really understand everything step by step. So let's get to it. Step number one, just as before, we're going to take some source document and chunk it into separate pieces of text. So for this example, I'm going to assume I just have two pieces of text here, just section one, medical research, and section two, software engineering. Step two, we're going to generate embeddings for each of these different chunks of text. Now in this example, we're going to pretend that we have this imaginary super perfect embedding model. And this embedding model has two very important characteristics. First, we're going to assume that always returns embeddings of length two, so just two separate numbers, and we're going to also assume that we know exactly what each number is really scoring about the source text. Remember, in reality, that is not the case, but in this scenario, we're going to imagine we know exactly what each number is really talking about. So we're going to say that the first number is how much the text is talking about the medical field, and the second is how much the text is talking about software engineering. So for the first chunk of text, when we embed it, this thing is definitely talking about medical research. So I would give it maybe a score of .97 to say, yes, absolutely, this is very much talking about the medical field. And then it also uses the term bug, which has a slight software engineering connotation. In addition, medical itself is pretty heavy on software engineering, so I'm going to give it a score of 344 software engineering. Then for the second piece of text here, well, it's definitely talking about software engineering, so I'm going to give it a score of .97 for that. And then it also mentions infection vectors, which has that connotation of medicine. So I'll give it a slightly higher medicine score as well of .3. Now that we have generated these embeddings, we're going to go through an extra little step of mathematics here, something referred to as normalization. Now you do not really have to understand normalization that much. This is already going to be done for you in the vast majority of cases by the embedding API that you are using. This normalization step is going to scale the magnitude of each of these pairs of vectors to 1.0. And if you don't understand that terminology, totally fine. Don't sweat it too much. Just understand that we're going to do a slight little adjustment to the actual magnitude of each number. Once we have generated these embeddings and normalize them, we can kind of visualize them on a plot like this. So on this plot, I've drawn a unit circle and each of our points representing both those embeddings will lie exactly on the circle because we have normalized their lengths to exactly one. So we've got the software engineering section up here and here is medical research over here. So now that we have these embeddings, we're going to move on to the next step. In this step, we are going to take these embeddings and store them inside of something called a vector database. This is a database that has been optimized for storing, comparing, and looking up long lists of numbers exactly like what our embeddings are. Now, at this point in time, we kind of pause. We take a break because this is all been pre-processing work that we did ahead of time. So at this point, we kind of just sit around and wait for a user to actually submit a query to our application. So we will imagine that at some point in time, finally a user will come to our app and maybe type into a chatbot or something like that. They're a question or they're query. Maybe in this case, their question is going to be something like, I'm curious about the company in particular, what did the software engineering department do this year? Now, at this point in time, we're going to take that user's question and we're going to run it through the exact same imaginary embedding model. In this scenario, because the user's question is asking specifically about software engineering, I'll give it a score of 0.89. And then because it's also talking about company and again, software engineering is kind of tied up in the medical field, I'll give it a very slight medical score as well of 0.1. Now that we have this embedding, we're going to go and go through that normalization step again. And then finally, we're going to make use of our vector database. We're going to take the user's query, we're going to feed it into the vector database and say, please search through all the vectors we have stored inside of you and give us the vector that is closest in nature to this one. So in our case, I would kind of expect to get back section two software engineering because that's kind of what the user asked about over here. But let me tell you exactly what is happening inside of the vector database that is able to give us this very closely related result. Okay, so a little bit of math here, don't worry, won't be too much. So when we take the user's query and add it onto this chart, we can see right away that visually, the user's query is just really close to software engineering. So you and I as humans, we could look this chart and say, oh, yeah, clearly these two things are very close. The user's query is very similar to software engineering. So obviously, if we want to find some chunks inside the vector database related to the user query, this would be the one that we want. But of course, we are using computers here. And our computer doesn't actually just make a chart like this and then look at it. There's some actual calculation going on behind the scenes. So let's examine exactly what that calculation is. And it's kind of important for you to know it because eventually when you start using vector databases, they're going to use a lot of terminology that's related to this kind of math going on behind the scenes and to actually interface well with the vector database, you kind of need to have at least a very basic understanding of the math. So that's why I want you to understand it. All right, here's a high level look at the math that is being done inside of your vector database to find which embeddings are most similar to the user's query. We want to calculate something called the cosine similarity. This is the cosine of the angle between the user's query and each of the other embedding stored in the database. So we'd want to find the angle A right here and take the cosine of it and angle B right here and take the cosine of it. The math for this is shown on the right hand side. The result of this calculation will be a number between negative one and one. If we get a result close to one as we did right here, then that means that we have found an embedding very similar to the user's query results closer to negative one. Meaning we have found an embedding that not at all similar to the user's query. In our case, the cosine similarity between our user query and the software engineering chunk is 0.983. Meaning that these two embeddings are very similar. So this is a sign to us that we would want to take the software engineering chunk of text and include it in our prompt with the user's question. Now before we move on, one other quick thing that's going to be a little confusing right now, but it's going to be very, very helpful to know later on when you start working with vector databases. In a lot of vector database documentation, you're going to see something referred to as a cosine distance. This is different than the cosine similarity. It is calculated as one minus the cosine similarity. As adjustment is often done, just to give us an easier to interpret number. With a cosine distance, values close to 0 mean you have a large similarity and larger values than that. Meaning we have less similarity. Again, this is going to be something you're going to see very often in vector database documentation. So just be aware of it whenever you see the term cosine distance and cosine similarity. So now that we understand some of this math at a very high level, let's get back on track. Once we have found a text chunk with a high similarity to the user's question, we're going to take the user's question, add it into our prompt and the text chunk that we found that's most relevant and put that into our prompt as well. We then take that prompt and send it off to clod. And that's the entire process in great, great detail. So now that we understand everything from start to finish with all the kind of tech behind the scenes going on and even some of the math, let's start to implement this inside of a notebook in just a moment.

</details>

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


> 🎬 **视频 41**：Implementing the RAG flow  
> 📁 文件：[41. Implementing the RAG flow.mp4](videos/41.%20Implementing%20the%20RAG%20flow.mp4)

**核心内容**：动手实现完整的 RAG 管道。
**关键要点**：
- 使用 ChromaDB 作为向量数据库
- 实现文档加载、分块、嵌入、存储的完整预处理流程
- 实现查询嵌入、相似度检索、上下文构建、Claude 调用的完整查询流程
- 端到端 RAG 应用演示

<details>
<summary>🇨🇳 查看中文翻译</summary>

现在我们理解了完整的 RAG 流程，接下来在另一个 Notebook（003_VectorDB）中走一遍实际实现。这个 Notebook 中我提供了一个向量数据库的示例实现，叫做 `VectorIndex` 类。

我们将通过五个步骤实现整个 RAG 流程：

**第一步：文档分块。** 打开 report.md 文件，用 `chunk_by_section` 函数按章节分块。测试一下——`chunks[2]` 应该显示目录，`chunks[3]` 显示下一个章节，依此类推。

**第二步：为每个块创建嵌入。** 我重写了嵌入函数，现在可以传入单个字符串或字符串列表。传入列表时，会为每个字符串创建嵌入并返回嵌入列表。调用 `embeddings = generate_embedding(chunks)` 即可。

**第三步：创建向量存储并插入数据。** 创建 store 实例，循环遍历所有块和嵌入的配对，逐个插入。代码是：`for embedding, chunk in zip(embeddings, chunks): store.add_vector(embedding, {"content": chunk})`。

这里有个重要细节——为什么我们在存入嵌入时还要附带原始文本？因为稍后查询时，只拿回嵌入向量对我们没用（嵌入本身没有可读意义），我们真正需要的是与嵌入关联的原始文本。所以存储时通常会把块文本（或至少块的 ID）一起存入。

**第四步：用户提问，生成查询嵌入。** 用户问题是"软件工程部门去年做了什么？"，调用 `user_embedding = generate_embedding("what did the software engineering department do last year?")`。

**第五步：搜索相关文档。** 用 `store.search(user_embedding, 2)` 搜索最相关的两个块。打印结果后可以看到：第一个结果是"第二节"（距离 0.71），第二个是"方法论"部分（距离 0.72）。这就是与用户查询最相关的两个文本块。

这就是完整的 RAG 工作流实现。但目前仍有一两个场景不太理想，还有改进空间——接下来我们将讨论这些改进。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Now that we understand the entire rag flow, we're going to walk through an example inside of another notebook called 003 VectorDB. So in this notebook, I provided a sample implementation of a vector database, and I've called it, class vector index right here. If you want to, feel free to take a glance at it, but I'll walk through everything you need to understand about it. Now in this notebook, we're going to walk through the entire rag flow by implementing five different steps. The same five steps we just spoke about in the last video. So let's get to it. Step number one, I have already opened up the file and read the text from it. Specifically, our report.md file, which should be in the same directory as the notebook. So in step one, we're going to chunk the text by section. I've already added in a function to help with that, so the same chunk by section function we had previously. So to do our chunking process, I'll say chunks is chunk by section and pass in all that text. And now just to test things out and make sure I've got everything working correctly, I'll try printing out chunks at about two. And I should see a printout of the table of contents. And then if I go to three, I should see the next section down and then the next section and so on. Then on to step two, in step two, we're going to create an embedding for each chunk. Now, just so you know, I rewrote the embedding function slightly so that now we can pass in either a single string or a list of strings. And if we pass in a list of strings, it will create an embedding for each of them and then return that as a list of embeddings. So to implement step number two, we will call generate embedding and pass in all the chunks and then assign the result to embeddings. And then step three, we are going to create an instance of the vector store. Once the store has been created, we will then loop over all the different pairs of chunks and embeddings. We're going to zip them together and then as we take each pair, we're going to insert them into the store. We'll do that with a four embedding and chunk in zip embeddings and chunks. And again, for each of those different pairs of embeddings and chunks, we'll do a store, add, vector, with the embedding in. And then as the second argument, we'll put in a dictionary with content of chunk. Now I went over this step rather quickly. So let's do a quick aside and explain why we are looping over all these things, why we are chunking it, and why we are adding in this extra dictionary with the content of chunk. As we just discussed, eventually at some point in time, we're going to reach out to our vector database and give back a list of all the different related embeddings to the input. Now when we get back this list right here, just getting the number by itself, just getting the embedding is not really useful to us because the embedding doesn't really have a lot of meaning to you and I as developers. What we really care about is the text associated with that embedding. So usually whenever you store these different embeddings inside of your vector database, you're also going to include either the text from the chunk that the embedding was generated from or at least the ID of the chunk, something to at least point you back to the original chunk text. So in this case, I'm going to include the original chunk text along with each embedding. Again, just so when we do the look up later on and I get back the most similar chunks, I've got the actual text that I'm looking for now on to step four. So in step four, at some point in time in the future, a user is going to ask us question. We need to take that question and generate an embedding for it. So we'll make a user embedding by calling generate embedding and then my question here is going to be what did the software engineering department do last year? Finally, on to step five, where we are going to try to find some relevant documents. So I want to search the store with the embedding and I want to find the two most relevant chunks. Not just the most relevant, I want to get the two chunks that seem to be most relevant to this question right here. So for that, I'll do a results store.search. I'm going to pass in the user embedding and I'm going to pass in another argument here of two because I want to find the two most relevant chunks and then I will print out for doc and distance in results. I'm going to print out the distance, a new line and then the documents content and because each chunk here is really, really large, I'm going to print out just the first 200 characters. And then another new line like so. And I'll run this and there's our result. So we get back section two as our best result. We also see the cosine distance here. So it's 0.71 and the next closest chunk is at 0.72 and that was the methodology section. So these were the two chunks that were found most relevant for the user query that we just submitted. All right, so that is our entire rag workflow. Now all this works, but there is one or two scenarios where everything doesn't quite work as expected. There are still a couple of improvements we could add into our workflow and let's start to discuss those in just a moment.

</details>

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


> 🎬 **视频 42**：BM25 lexical search  
> 📁 文件：[42. BM25 lexical search.mp4](videos/42.%20BM25%20lexical%20search.mp4)

**核心内容**：BM25 词法搜索——基于关键词匹配的检索方法。
**关键要点**：
- BM25 基于词频(TF)和逆文档频率(IDF)排名
- 精确关键词匹配，与语义搜索互补
- 适合专业术语、产品名称等精确匹配场景
- 使用 `rank_bm25` 库实现

<details>
<summary>🇨🇳 查看中文翻译</summary>

我们已经搭建了 RAG 管道的第一版，一切看起来不错，但很快会发现搜索结果并不总是最优的。

举个例子。打开 report.md 文件，在软件工程部分你会看到一个事件编号"incident 2023-Q4-011"，在这个段落中出现了三次，在网络安全分析部分也提到了。

我用这个搜索词在之前的语义搜索 Notebook 中测试——搜索"what happened with incident 2023"。结果令人意外：第一名是第 10 节（网络安全，正确），但**第二名是第 3 节（财务分析）**——而第 3 节中根本没有提到这个事件！我们期望的是第 10 节和第 2 节（软件工程），但语义搜索给了一个完全无关的结果。

为了改进，我们引入**并行搜索策略**：用户提问时，同时送入语义搜索和另一个**词法搜索（Lexical Search）**系统。词法搜索更像经典文本搜索——把问题拆成单词，然后找包含这些词的文本块。两个系统各自返回结果，再合并。

实现词法搜索最常见的方法是 **BM25（Best Match 25）** 算法。它的工作原理：

1. **分词**：把用户查询拆成单独的词，去掉标点。比如"a incident 2023-Q4-011"变成"a"和"incident 2023"。

2. **统计词频**：看每个搜索词在所有文本块中出现的频率。"a"出现了 5 次，"incident 2023"只出现 1 次。

3. **分配相对重要性**："a"频繁出现 → 不太重要。"incident 2023"很少出现 → 非常重要（**逆文档频率**的核心思想）。

4. **评分排名**：找到使用高权重词更频繁的文本块。块一只有 2 个"a"但有 1 个"incident 2023"（高权重词），块二有 3 个"a"但没有高权重词——所以块一得分更高。

在配套 Notebook（004_BM25）中，我实现了一个 `BM25Index` 类。测试同样的搜索"what happened with incident 2023-Q4-011"——结果好多了！**软件工程排第一，网络安全第二，方法论第三**。现在搜索结果优先返回了包含重要搜索词的章节，而"what""happened""with"这些常见词权重很低，不会干扰结果。

注意两个搜索系统的 API 设计非常相似——都有 `add_document` 和 `search` 方法。这为下一步合并打下基础：接下来我们将把两个搜索系统整合在一起，用户提交查询时同时走两条路，然后合并结果，既获得语义搜索的优势，又获得词法搜索的精确匹配能力。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

We've got the first iteration of our rag pipeline put together. And everything looks good right now, but we're going to very quickly realize that, well, maybe we are not getting the best search results. Let me show you an example. If you open up the report.md file and scroll down just a little bit to the software engineering section, here it is right here, you'll notice that it has the statement of I&C, which is short for incident 2023 Q4 011. And it looks like that search term occurs three times inside of this paragraph. So here's one right here, two right there, three right here. And if I continue searching throughout the document, I'll see that it is also mentioned down here inside of section 10, cyber security and analysis. It's mentioned inside the header and then one time inside the actual paragraph itself right there. Now, I want to try searching for this term, this incident 2023 Q4 011. And we're just going to see what happens. In other words, what search results do we actually get back using semantic search? So back inside of my notebook, I'm going to update the user query right here to be what happened with incident 2023. Then I'm going to rerun all cells and we'll see what result we get. All right, so take a look at this. It's a little bit surprising result. We get section 10, which is good. That's definitely the result we would want to see first in the list because section 10 is all about this incident. But then very surprisingly, the next result is section 3, financial analysis. Well, if you open up section 3, right here, you'll notice that nowhere inside of section 3 is that incident ever mentioned. So we're getting some output from our semantic search that is a little bit surprising here. What we really wanted to get back was section 10 and then section 2. But what we got was section 10 and then unfortunately section 3 and section 3 up here should be completely irrelevant when it comes to investigating this incident. So even though the semantic search technique we put together is really fantastic and it's going to work well a lot of the time, there are these corner cases where it really just doesn't quite work as expected. So let's take a look at a technique we can use to improve our search results and hopefully get the results we want, which is section 10 and then section 2. All right, so here's the general strategy we are going to use. Whenever a user asks a question, we're going to feed that question into our semantic search side of the equation, which is generating those embeddings and using the vector database. But then in parallel at the same time, we're also going to implement a separate lexical search system. Now lexical search is more like classic text search where we are going to break down the user's question into individual words and then trying to find chunks of text that seem to include those words. Once we go through the search process in both different systems, we'll get two sets results and then we will merge the results together. And the hope here is that we'll get a little bit better balance of search results where we get both the kind of semantic aspect and the plain text search aspect included in one result set. So hopefully we will eventually get a result that looks like this over here. Now to implement this lexical search, there are a tremendous number of methods for implementing text search, but a very common method that you're going to see used in rag pipelines, like the one we are building right now, is a technique referred to as VM25. Now this is short for best match 25. In the rest of this video, I'm going to give you a high level overview of how this algorithm works. And I'm going to take a look at a notebook that actually implements VM25. So we'll be able to play around with it directly and see what kind of search results we get. So here's the general idea behind the VM25 algorithm. Now again, I'm going to give you a high level overview and I'm going to leave out a couple of smaller steps just to simplify things and make it easier to understand. Everything is going to begin with us receiving a user's query. And let's imagine this case, they put in a search string like this right here, just A, so the word A, and then incident 2023-Q4011. In step one, we're going to tokenize the user's query. And that means we're going to break it up into separate chunks. There are different ways in which we can tokenize a user's query, but right now we're going to use a very simple method, which is to just remove punctuation and break up the turn all terms based upon spaces. So in this case, I would end up with separate search query terms of A and then incident 2023. Next, we're going to see how often each of these different search terms occurs across all of our different documents or in our case, really text chunks. So let's imagine that we only have two text chunks in this scenario. So we're going to see how often the word A and the word incident, blah, blah, blah occurs across each of these chunks. And it looks like this first chunk right here has A right there, A right there, and then the second one has A, A, A. So in total, I would count all those up and I would have five A's. And then I would see how often I have incident 2023. It looks like there's only one right here. So it end up with a frequency of one. Next up, we're going to assign a relative importance to each term based upon its usage frequency. So in the case of the word A, it was used five times. And because it was used rather often, we're going to say this term is not super important because it is used all the place across all of our different documents or again, our case, our text chunks. But incident 2023, that was used very infrequently, which means it is probably going to be of greater search importance. Then finally, in the last step, we're going to find the text chunk that uses the higher weighted terms more often. So in this case, the first text chunk right here, it only has two A's, whereas the second one has three A's. But A's are not super important because they're used rather frequently across all of our different chunks. However, text chunk one uses incident 2023 one time. And that is a highly weighted term. It's a really important term. So in this case, we would say this is probably our best text chunk. And we would want to return this as a prime search result. Now again, to see all this in action, let's take a look at a quick, Jupiter notebook. So back inside of my editor, I'm going to find a new notebook. This one is called 004 underscore BM25. Again, at the top, I've got some code relating to a chunking by section. I've then got a basic implementation of BM25 in the form of this class called BM25 index. So I'm going to collapse at cell, make sure I run it. I'm going to read the contents of our report file. And then we're going to go through three separate steps here. We're going to first chunk the text by section. We're going to create a BM25 index store. And we're going to add each text chunk to it. And then we're going to attempt to search the store. And once again, our hope here is that we're going to maybe get some search results that look a little bit closer to this. Maybe not exactly these results, but I definitely want to see the sections that use incident 2023 before I ever see some results that don't include that search term at all. So let's see how we do. Okay, let's take care of step one here. We need to chunk the text by section. So we've gone over this a couple times now. We'll say chunks is chunk by section with text. Next up, I'm going to create a store. And I'm going to loop over all my chunks and add them in as documents to the store. So I'll say for chunk in chunks store add document. And I'll pass an addictionary with a content of chunk. I'm going to run that. And I'll finally I'm going to search over the store. I'll say store search. And I'll use that same term that I used in the previous notebook that did not give us the very good results. So I'll ask what happened with incident 2023 Q4011. And I'm going to ask for the first three search results. And then I'm going to print up the results very nicely just so we can interpret them really well. We'll say for doc distance in results. And I'll print out the distance. A new line. Doc with content. And again, I'm only going to print out the first 200 lines. And then how about a new line? A couple of separators and another new line. I'm going to run this and we'll see what we get. All right. So that's a much better search result than what we had before. Now we're going to see software engineering first and then cybersecurity after that. And then methodology down here. So now I am actually prioritizing the sections that use the most important search term inside my query, which was the incident 2023. And you'll notice that I don't really have quite as much importance around the other terms like what happened with those aren't quite as important terms. And they might be used several times inside of the original report. So I would not weigh those as heavily in the output results. But this incident 2023. That's a very rare term inside of a report. So it should definitely have a much higher weighting. And we can see that reflected very clearly inside of our search results. All right. So now at this point in time, we have two separate search systems. We have semantic search put together. And we have this kind of more lexical, a little bit more classic tech search system. And you might notice that in the implementation of these two stores, back up here in the cell right here, I put them together with a rather similar API. They both have a ad document function and they both have a search function down here as well. So now that we have these two separate search systems, one which implements semantic search and one which implements lexical search, we're going to come back in the next video and we're going to merge these two search systems together. Whenever user submits a query, we're going to forward it off to both of these different search systems. We're going to get back a set of results from both and we're going to merge those results together. And hopefully we'll have all the best outcomes of semantic search along with some of the more classic results of lexical search as well.

</details>

### BM25：基于关键词的传统搜索

BM25 基于 TF-IDF 原理，擅长精确的关键词匹配，与向量搜索形成互补：

- **向量搜索**：擅长语义相似（"汽车" 能匹配 "轿车"）
- **BM25**：擅长精确匹配（专有名词、型号、ID 等）

两者结合 = 混合搜索，效果 > 单独使用任一种。

---

## 第 7 课：混合搜索架构

> 📹 视频：Multi-Index RAG Pipeline（7 min）


> 🎬 **视频 43**：A Multi-Index RAG pipeline  
> 📁 文件：[43. A Multi-Index RAG pipeline.mp4](videos/43.%20A%20Multi-Index%20RAG%20pipeline.mp4)

**核心内容**：混合搜索架构——结合语义搜索和 BM25 的多索引 RAG 管道。
**关键要点**：
- 语义搜索捕捉含义，BM25 捕捉精确关键词
- 同时运行两种搜索，用 RRF 算法融合排名结果
- 去重后选取最相关的块作为上下文
- 混合搜索在大多数实际场景中表现最佳

<details>
<summary>🇨🇳 查看中文翻译</summary>

现在我们有了语义搜索和词法搜索的实现，需要把它们连接在一起。

首先注意，两个搜索实现有几乎相同的公共 API——`VectorIndex` 和 `BM25Index` 都有 `add_document` 和 `search` 方法。为了连接它们，我们创建一个新类叫 **Retriever**。Retriever 接收用户问题，转发给两个索引的搜索方法，然后合并两方的结果。

**合并结果的方法：倒数排名融合（Reciprocal Rank Fusion，RRF）。** 这个公式看起来很复杂，但其实不难理解。来看一个例子：

假设向量索引返回结果排名是：Section 2（第1名）、Section 7（第2名）、Section 6（第3名）。BM25 返回：Section 6（第1名）、Section 2（第2名）、Section 7（第3名）。

我们把所有结果放到一个表中，记录每个文本块在各索引中的排名。然后对每个块应用 RRF 公式：对每一列（每个索引），计算 `1 / (1 + rank)`。

以 Section 2 为例：向量索引排名第 1，得分 `1/(1+1) = 0.5`；BM25 排名第 2，得分 `1/(1+2) = 0.333`。总分 = 0.5 + 0.333 = 0.833。

计算所有块的得分后，按得分从高到低排序。Section 2 得分最高（两边都排名靠前），Section 6 居中（一好一差），Section 7 最低（两边都排名靠后）。用视觉直觉验证——结果确实合理。

在配套 Notebook（005_hybrid）中，我实现了 `Retriever` 类。它的 `add_document` 方法会把文档同时传给所有内部索引。`search` 方法把查询传给所有索引，收集结果，然后用 RRF 合并。

**关键测试**：还记得之前纯语义搜索的问题吗？搜索"incident 2023"时，第一名是第 10 节（正确），第二名却是第 3 节（不相关）。我们期望第二名是第 2 节（软件工程）。

现在用混合搜索测试同样的查询——结果：**第 10 节排第一，第 2 节排第二**，完全符合预期！通过结合两种不同的搜索技术，我们得到了好得多的输出。

这种设计的优美之处在于，每个索引可以独立开发（各自是单独的类），只要有相同的 `search` 和 `add_document` API，就能轻松包装到 Retriever 中。如果想添加其他搜索方法（比如全新的搜索功能），只要实现同样的接口就能即插即用。

好，我们取得了成功，但还没完——还有其他技术可以进一步提升 RAG 管道的准确性。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

We now have an implementation for semantic search and an implementation for lexical search. So now we need to wire these things up together. Let me show you how we're going to do that. The first thing to notice is that the implementation for both these searching functionalities have the almost exact same public API. So we have a vector index class on the left hand side that has methods like add document and search. And we have almost identical methods inside of our BM25 index as well. So to connect these two things together into a single search pipeline, we're going to wrap them up inside of a new class that we will call retriever. This retriever is going to receive a user's question and then forward it on to the search methods of vector index and BM25 index. The retriever will then receive the results from both them and figure out some way of actually emerging the results together. Now it turns out that the merge operation is actually a little bit tricky. So I want to go into all bit of detail on how you can merge results that are coming out of these different search methodologies to combine the results together. We're going to use a technique known as reciprocal rank fusion. The easiest way to understand this technique is to go through an example. So let's do that right now. Let's imagine that we run a search on the vector index and we get outputs of section 27 and then 6. And then we do the same exact search on BM25 and we get 6, 2 and 7. So now we need to take these two list results and combine them together in some way to do so. I'm going to take all the search results and put them together on a single table like so. So now I've got text chunk 27 and 6 and I've recorded the rank from the vector index output and the rank from the BM25 index output. And to be clear, when I'm talking about rank, I just mean kind of search output position. So rank one, two, three, rank one, two, three. I'm just kind of putting those same exact numbers on this chart down here. Once I have all those ranks in place, I'm then going to apply a formula. Here's the exact formula right here and I know it looks really terrible, but don't worry. It's not as complicated as it looks. Here's how it works for every rank column we have. So like that column right there and that column right there, we're going to write out a separate term. So here's the term for the first column. Here's the term for the second column. In the first term, we're going to write out one over one plus whatever number is right there. So we end up with one over one plus one. And in the second term, we'll be one over one plus whatever number is right there. So one over one plus two. Once we have calculated the score for each text chunk, we're then going to sort the table based upon score from greatest to least. So we would end up with something like this. So we'd end up with text chunk for section two as being the most relevant search result. Section six would be the second most and section seven will be the least relevant. And this kind of makes sense. We can kind of visually confirm that these outputs make sense. If you just look at the individual rank outputs from each search methodology. So section two was rank one and two. That means hey, the general it's trending up towards the top. Section six is one and three. That's kind of like in the middle. It has a good score in a bad score. And then section seven is two and three. And so it trends down towards the bottom. So with a visual inspection, the results I think do make a decent amount of sense. All right, so now that we understand how we're going to combine the results together, let's go back over to our Jupyter notebook. And we're going to take a look at a sample implementation of a retriever class and a sample implementation of merging the results. Okay, so back over here, I move on to the next notebook, which is zero zero five hybrid. Once again, there's a lot of setup up here. So I've got the vector database implementation, the BM25 implementation. And now I've added in a implementation for the retriever class as well. The retriever has method of add document. And if you call add document, she's going to take whatever document you pass in and pass it off to each of the different indexes that are contained inside the retriever. So in our case, our indexes are the vector index and the BM25 index. Then the retriever also has a search function. If you pass in some query text to it, that query text will be passed off to each of the different indexes that are contained inside the retriever. We then take all the results that come back and combine them together. So here is the merge logic that implements that reciprocal rank fusion. All right, so time to do a little test here. Now I want you to recall what led us down this entire path was back on our vector database implementation. So this notebook over here, we found that if we search for something like what happened with incident 2023, we got back some unexpected results where we had section 10, which was good as the first result. And then section three was the second result. And that was really unexpected. We want that second result to be software engineering. So when we now run this hybrid approach that combines together multiple different indexes, my hope is that we're going to get first section 10 and then whatever section the software engineering one is. I think it's section two. So let's test this out inside of our new notebook. I'm going to go down to the bottom and I'll do a results is retriever search what happened with incident 2023 Q4011. And I'm going to get the first three search results. And then once again, I'm going to print them all out like so. And I'll do the score, a new line, the content of the document, but just the first 200 lines. And then just a little separator between each chunk. So I'm going to run this. And now we get a some much better search results than what we had before. So I've got section 10 and then section two, exactly what we wanted. And then section five, but that one's not super relevant here. So we now have a much better output by combining together these two different search techniques. And the nice thing about this is we were able to author each of these indexes kind of in isolation. They're their own separate classes. And because we made each implementation have the same exact API with that search function and the ad document function, we were able to easily wrap them up into this larger retriever class. So if you wanted to, we could absolutely add in some additional search index here that maybe implements some other completely different searching functionality. And as long as it has that search function and the ad document function, we can very easily add it, have it generate some results, and then merge the results along with the results coming from the other search methodologies as well. Okay, so let's say this is a good success, but we're not quite done yet. There's still some other techniques that we're going to go over to improve the accuracy of our rag pipeline.

</details>

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
