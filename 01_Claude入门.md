# 模块 1：Claude 入门 — API 基础与核心概念

> **对应课程**：Building with the Claude API — Module 1: Getting Started with Claude  
> **视频转录**：11 个（视频 01-11，已嵌入文字）  
> **GitHub Notebook**：`anthropic_api_fundamentals/` 目录（6 个 Notebook）  
> **预计学习时间**：2 小时  
> **难度**：⭐

### 📌 原课程地址

| 平台 | 链接 |
|------|------|
| **Skilljar（官方）** | https://anthropic.skilljar.com/claude-with-the-anthropic-api |
| **Coursera（镜像）** | https://www.coursera.org/learn/building-with-the-claude-api |
| **GitHub Notebook** | https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals |

### 📌 视频与 Notebook 对应关系

| # | 视频标题 | 时长 | 配套 Notebook |
|:-:|---------|:----:|:-------------|
| 1 | Claude Model Overview | 4m | 📓 `03_models.ipynb` |
| 2 | Making Requests | 6m | 📓 `01_getting_started.ipynb` / `02_messages_format.ipynb` |
| 3 | Multi-turn Conversations | 9m | 📓 `02_messages_format.ipynb` |
| 4 | Building a Simple Chatbot | 4m | 📓 `02_messages_format.ipynb`（聊天循环部分） |
| 5 | System Prompts | 6m | 📓 `04_parameters.ipynb`（system 参数部分） |
| 6 | Writing System Prompts Exercise | 1m | — 动手练习 |
| 7 | Temperature | 6m | 📓 `04_parameters.ipynb`（temperature 部分） |
| 8 | Streaming Responses | 8m | 📓 `05_Streaming.ipynb` |
| 9 | Structured Data | 6m | 📓 `06_vision.ipynb` |
| 10 | Structured Data Exercise | 5m | — 动手练习 |

> **阅读材料**（7 篇，65 分钟）：Module Introduction / Working with the API / Getting an API Key / Exploring the Claude Documentation / Setting up a Dev Environment / Controlled Model Output / Next Steps

---

## 本模块学习目标

完成本模块后，你将能够：
1. 了解 Claude 模型家族的特点与选择策略
2. 安装 Anthropic Python SDK 并完成 API 认证
3. 理解 Messages API 的请求/响应格式
4. 掌握多轮对话的消息结构
5. 构建简单的聊天机器人
6. 使用 System Prompt 设定 Claude 的行为
7. 熟练使用 `temperature`、`max_tokens` 等关键参数
8. 使用流式输出（Streaming）实现实时响应
9. 让 Claude 输出结构化数据（JSON 等）

---

## 第 1 课：Claude 模型概览

> 📹 视频：Claude Model Overview（4 min）  
> 📓 配套 Notebook：`03_models.ipynb`


> 🎬 **视频 01**：Overview of Claude models  
> 📁 文件：[01. Overview of Claude models.mp4](videos/01.%20Overview%20of%20Claude%20models.mp4)

**核心内容**：介绍 Claude 的三个模型系列（Opus、Sonnet、Haiku）及其各自特点和选择策略。

**关键要点**：
- **Opus**：最高智能水平，支持推理，适合复杂任务，但延迟较高、成本较贵
- **Sonnet**：智能、速度、成本的最佳平衡点，编码能力强，推荐作为默认选择
- **Haiku**：最快速度、最低成本，不支持推理，适合实时交互的面向用户应用
- 模型选择本质上是智能水平与速度/成本之间的权衡
- 实际项目中可以组合使用多个模型，各取所长

<details>
<summary>🇨🇳 查看中文翻译</summary>

在这个视频中，我们将了解 Claude 的三个模型系列，并搞清楚哪个最适合你的具体使用场景。为了帮助你理解这些模型之间的区别，我将带你了解每个模型的关键特性，然后给你一个简单的框架来选择合适的模型。在深入具体细节之前，让我先说明一点：这三个模型都共享 Claude 的核心能力，它们都能处理文本生成、编码、图像分析和许多其他任务。它们之间的真正区别在于各自的优化方向——一个专注于智能水平，一个专注于速度和成本效率，还有一个是在智能和速度之间取得平衡。

第一个是 Opus。Opus 是 Claude 最强大的模型。当我说"强大"时，我想说的是，这个模型能提供你从 Claude 中获得的最高水平的智能。在实际应用中，这意味着 Opus 是为那些需要高水平智能和规划才能完成的复杂需求场景而设计的。它可以在较长时间内独立完成复杂项目，比如一个需要运行数小时的任务，模型需要自行管理多步骤流程并处理大量不同的需求，而不需要太多的人工干预。Opus 支持我们所说的推理能力，这意味着对于简单任务它可以快速响应，对于更复杂的任务它可以花一些时间来思考。缺点是 Opus 有一定的延迟和较高的成本，这就是你需要权衡的。所以，你获得了非常高的智能水平，但每次请求也需要多一些时间和费用。

接下来是 Sonnet。Sonnet 处于 Claude 产品线中的一个"甜蜜点"。它在智能、速度和成本之间有很好的平衡，这使它对大多数实际使用场景都非常有用。Sonnet 的突出优势是其强大的编码能力和快速的文本生成。许多开发者喜欢它能精确编辑复杂代码库的能力，也就是说它可以在不破坏大量现有代码的情况下对项目进行修改。

最后是 Haiku。Haiku 是 Claude 最快的模型，专门为响应时间至关重要的应用而设计。关于 Haiku 需要注意的一个重要点是，它不支持 Opus 和 Sonnet 所具有的推理能力。相反，Haiku 针对速度和成本效率进行了优化，这使得 Haiku 非常适合需要实时交互的面向用户的应用。

现在让我们谈谈如何为你的特定应用决定使用这三个模型中的哪一个。思考模型选择的方式其实就是理解这些不同模型之间的权衡。一方面你有非常高的智能水平，另一方面你有更多的成本和速度考量。Opus 位于智能端——它非常聪明，但更贵，延迟也更高。Haiku 位于成本和速度端——它有中等智能水平、低成本和最高的速度。Sonnet 则在中间位置，在这些不同特质之间取得了良好的平衡。

所以这是你决定使用哪个模型的方法：你需要确定或弄清楚对于你的具体使用场景什么最重要。如果智能是你的首要考量，意味着你有一个需要非常强推理能力的复杂任务，那你可能想使用 Opus——你选择的是质量而不是速度和成本。如果速度是你的优先考量，意味着你有实时用户交互或需要尽快得到响应的大量处理任务，那你应该选择 Haiku。如果你需要在智能、速度和成本之间取得更好的平衡——这通常是大多数应用的情况——那 Sonnet 可能是你的最佳选择。

这里需要注意的一个重要事项是，许多团队并不只是选择一个模型然后一直用它。相反，你可能在同一个应用中使用多个不同的模型。你可能用 Haiku 来处理对速度要求很高的面向用户的交互，用 Sonnet 来处理主要的业务逻辑，用 Opus 来处理需要更深层推理的真正复杂的任务。

以上就是 Claude 三个模型系列的介绍以及如何在它们之间做选择。顺便说一下，在本课程中我们大多数时候会使用 Claude 的 Sonnet，因为它在这三种不同特质之间给了我们非常好的平衡。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

In this video, we are going to examine Claude's three model families and understand which one is right for your specific use case. To help you understand how these models differ, I'm going to walk you through each model's key characteristics and then show you a simple framework for picking the right one. Before we dive into the specifics, let me make one thing clear. All three of these models share Claude's core capabilities, so they can all handle text generation, coding, image analysis, and many other tasks. The real difference between them is how they are optimized. One is built to focus on intelligence, one for speed and cost efficiency, and one for more of a balance between intelligence and speed. The first is Opus. Opus is Claude's most capable model. And when I say capable, I need to say that this is a model that delivers the highest level intelligence that you can get out of Claude. In practice, that means that Opus is designed for scenarios where you have complex requirements that need a high level of intelligence and planning to complete. It can work independently on complex projects for a long period of time, like a task that can run on for several hours, where the model needs to manage multi-step processes and navigate a lot of different requirements on its own without a lot of human intervention. Opus supports what we call reasoning, which means it can provide a quick response for simple tasks, or it can spend some time thinking for a more complex task. The downside is that Opus has a moderate latency and a higher cost, and that's really the trade-off that you are making. So, you get really high intelligence, it also takes a little bit more time and cost for every request that you make. Next up is Sonnet. Sonnet sits in a kind of sweet spot in Claude's lineup. It has a good balance of intelligence, speed, and cost that makes it really useful for most practical use cases. What makes Sonnet great is its strong coding ability, along with its fast text generation. Many developers like its ability to make precise edits to complex code bases, meaning it can make changes to a project without breaking a lot of existing code. Finally, we have Haiku. Haiku is Claude's fastest model, and it's made specifically for applications where response time is really important. One important thing to note around Haiku is that it doesn't support the reasoning capabilities that Opus and Sonnet have. Instead, Haiku is optimized for speed and cost efficiency, and this makes Haiku a really good choice for user-facing apps that need some real-time interactions. Now let's talk about how you decide which of these three models to use for your particular application. The way to think about model selection really comes down to understanding the trade-off between these different models. On the one hand side, you've got a really high intelligence, and on the other side, you've got more cost and speed. Opus sits on the intelligence side. It's really intelligent, more expensive, and also has higher latency. Haiku sits on the cost and speed side. It has moderate intelligence, low cost, and the highest speed, and Sonnet is right there in the middle, striking a good balance between these different qualities. So here's how you decide which model to use. You really need to identify or figure out what matters most for your specific use case. If intelligence is your top priority, meaning you have a complex task that needs really strong reasoning, then you probably want to make use of Opus. You're choosing quality over speed and cost. If speed is your priority, meaning you have real-time user interactions or you've got some high-volume processing where you need to get some responses back as fast as possible, then you want to choose Haiku. If you need more of a balance between intelligence, speed, and cost, which is often the case for most applications, then Sonnet is probably your best choice. One important thing to note here is that many teams don't just pick one model and stick with it. Instead, you might use multiple different models in the same application. You might use Haiku for user-facing interactions where speed is really important, maybe Sonnet for your main business logic, and Opus for the really complex tasks that need some deeper reasoning. So that covers Claude's three model families and how to choose between them. Just so you know, we are most often going to use Claude's Sonnet in this course just because it gives us a really fantastic balance of these three different qualities.

</details>

### 1.1 Claude 模型家族

Claude 有三个主要系列，能力与成本递增：

| 模型系列 | 定位 | 特点 | 适用场景 |
|:--------:|------|------|---------|
| **Haiku** | 轻量级 | 最快、最便宜 | 简单分类、客服初筛、数据抽取 |
| **Sonnet** | 平衡型 | 性能与成本最佳平衡 | 大多数生产场景 |
| **Opus** | 旗舰级 | 最强推理能力 | 复杂分析、学术研究、高难度编码 |

### 1.2 当前最新模型标识符

```python
# Claude 4 系列（最新）
"claude-sonnet-4-20250514"    # Sonnet 4 — 目前最常用
"claude-haiku-4-20250514"     # Haiku 4 — 轻量快速

# Claude 3.5 系列
"claude-3-5-sonnet-20241022"  # Sonnet 3.5 v2
"claude-3-5-haiku-20241022"   # Haiku 3.5

# Claude 3 系列（较旧）
"claude-3-opus-20240229"      # Opus 3 — 最强但较慢
"claude-3-sonnet-20240229"    # Sonnet 3
"claude-3-haiku-20240307"     # Haiku 3
```

### 1.3 三维度选型：延迟 / 能力 / 成本

```
📊 选择决策树：

你的任务复杂吗？
├── 简单（分类/抽取/格式化） → Haiku（快且便宜）
├── 中等（写作/分析/代码）  → Sonnet（推荐默认选择）
└── 复杂（推理/学术/创意）  → Opus 或 Sonnet + Extended Thinking
```

**实用建议**：
- **从 Sonnet 开始**，它是性价比最高的模型
- 如果 Sonnet 效果不够好，升级到 Opus
- 如果成本敏感且任务简单，降级到 Haiku
- 对于需要深度推理的任务，使用 Extended Thinking（扩展思考）

### 1.4 代码示例：不同模型对比

```python
import anthropic

client = anthropic.Anthropic()

# 同一个问题，用不同模型回答
models = [
    "claude-3-haiku-20240307",
    "claude-sonnet-4-20250514",
]

question = "Explain quantum entanglement in simple terms."

for model in models:
    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[{"role": "user", "content": question}]
    )
    print(f"=== {model} ===")
    print(response.content[0].text)
    print(f"Tokens: {response.usage.input_tokens} in / {response.usage.output_tokens} out\n")
```

---

## 第 2 课：发起请求

> 📹 视频：Making Requests（6 min）  
> 📓 配套 Notebook：`01_getting_started.ipynb` / `02_messages_format.ipynb`


> 🎬 **视频 02**：Accessing the API  
> 📁 文件：[02. Accessing the API.mp4](videos/02.%20Accessing%20the%20API.mp4)

**核心内容**：讲解通过 Anthropic API 访问 Claude 的完整请求流程和文本生成原理。

**关键要点**：
- API 请求必须通过后端服务器发送，绝不应从客户端直接访问（保护 API 密钥安全）
- 请求需要包含：API 密钥、模型名称、消息列表、max_tokens 参数
- 官方提供 Python、TypeScript、JavaScript、Go、Ruby 五种 SDK
- 文本生成四阶段：分词(Tokenization) → 嵌入(Embedding) → 上下文化(Contextualization) → 生成(Generation)
- 生成停止条件：达到 max_tokens 限制 或 产生序列结束 token
- API 响应包含：生成文本、token 用量统计、停止原因

<details>
<summary>🇨🇳 查看中文翻译</summary>

在本模块中，我们将了解如何访问 Claude 并使用它来生成文本。为了帮助你理解其工作原理，我将带你走过向 Anthropic API 发送请求的完整生命周期，我们还将简要了解 Claude 内部的运作机制。

首先，让我们考虑一个简单标准的聊天机器人应用。假设你正在构建一个 Web 应用，想在浏览器中向用户展示一个聊天窗口。当用户输入消息并点击发送时，他们期望某个回复会神奇地出现。我想深入了解生成这段文本并将其显示在屏幕上的幕后过程。我们将把这个过程分解为五个独立的步骤，逐一讲解。

当用户输入文本并点击发送时，该文本会被发送到你作为开发者实现的服务器上。我提到这一步是为了说明一件重要的事情：你不应该直接从 Web 或移动应用访问 Anthropic API。每次向 API 发送请求时，你都需要包含一个秘密 API 密钥。确保这个密钥保持秘密的最佳方式是永远不要将它包含在客户端应用中，只通过你自己实现的服务器来访问 API。

第二步，一旦你的服务器接收到来自客户端的请求，服务器将直接向 Anthropic API 发送请求。通常，你会通过 Anthropic 发布的 SDK 来发送请求。有 Python、TypeScript、JavaScript、Go 和 Ruby 的官方 SDK 实现。当然，你也可以不使用 SDK，直接发送普通的 HTTP 请求。发送请求时，你需要传递几项数据：API 密钥、要运行的模型名称、消息列表（包含用户提交的文本），以及 max tokens 值（限制 Claude 生成的文本长度）。

接下来是 Anthropic API，这是文本实际生成的地方。我会给你一个简化的高层概述来解释文本生成过程。我们将把文本生成过程分为四个阶段。

第一阶段，用户输入会被分解成更小的字符串，每个文本块被称为一个 token。这些 token 可以是完整的单词、单词的一部分，甚至是空格或符号。每个 token 会被转换成一个嵌入向量（embedding）——一个长数字列表，你可以把它想象成一个单词的数字化定义。

书面语言的一个有趣特性是，一个词可以有多种含义，只有通过它在句子中的位置和周围的其他词才能确定其具体含义。同样，每个嵌入向量可以被认为包含了每个词所有可能的含义。为了将每个嵌入向量精确到单一含义，会使用一种叫做上下文化的过程，其中每个嵌入向量会根据周围其他嵌入向量进行调整。

最后一步是生成，这是文本实际被写出的阶段。此时每个嵌入向量已经从相邻向量中吸收了大量信息。最终处理过的嵌入向量会传递给输出层，产生每个可能下一个词的概率。模型不会自动选择最高概率的词，而是使用概率和随机性的混合来选择，这有助于生成更自然、更多样化的回复。选定的词被添加到嵌入向量列表的末尾，整个过程重新开始。

在生成每个输出 token 后，模型会暂停并检查是否应该停止生成：首先检查已生成的 token 数量是否超过了 max tokens 参数；另外还有一个特殊的序列结束 token，模型用它来表示已到达它认为的自然结束点。

生成完成后，API 会将响应发送回你的服务器。响应中包含一条消息（包含生成的文本）、usage（输入和输出 token 的计数）和 stop reason（告诉你模型停止生成的确切原因）。一旦服务器收到响应，就会将生成的文本发送回你的应用进行显示。

这就是整个流程。本视频涵盖了很多主题，目前不需要你记住所有内容。唯一的目标是让你开始熟悉通过 API 访问 Claude 的一些常见术语。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

In this module, we are going to examine how we access Claude and use it to generate some text. To help you understand how this works, I'm going to walk you through the full lifecycle of requests to the Anthropic API. We are going to also take a brief look at what is going on behind the scenes inside of Claude. To get started with this walkthrough, we are going to consider a straightforward, standard chatbot app. Let's imagine that you are building a web app and want to show a chat window to a user in the web browser. When the user enters a message and clicks send, their expectation is that some response will just magically appear. Like I said, I want to examine what is going on behind the scenes here to generate this text and display it on the screen. We are going to break this down into five separate steps, which I have outlined at the top of this diagram. And we're going to walk through each step one by one. When a user enters some text and clicks send, that text is going to be sent off to a server that you, the developer, implement. I mentioned this step just to make one thing clear. You should not attempt to access the Anthropic API directly from a web or mobile app. Whenever you make a request to the API, you are required to include a secret API key. And the best way to make sure that this key stays secret is by never including it inside of your client-side app and only making requests to the API through a server that you implement. On to step two. Once your server has received a request from the client, the server will make a request directly to the Anthropic API. Usually, you'll make this request through one of the SDKs that Anthropic has published. There are official SDK implementations for Python, TypeScript, JavaScript, Go, and Ruby. Now, you don't have to use an SDK if you don't want to. You can also make a plain HTTP request if you wish. When you make this request, you are required to pass along several pieces of data. In particular, you need to include an API key, the name of the model you wish to run, a list of messages, which will include the text that your user submitted, and a max tokens value, which limits the length of the text that Claude will generate. Next up is the Anthropic API, which is where our text will actually be generated. This is where we are going to go into a little bit of detail on the text generation process within the language model. This process is complex, so I'm going to give you a simplified high-level overview. We are going to break down the text generation process into four separate stages. In the first stage, the user's input will be broken down into smaller strings. Each of these text chunks are referred to as a token. These tokens can be whole words, or a part of word, or even a space or a symbol. To keep things clear, we are going to assume that each word forms one single token. Each token is then converted into an embedding. An embedding is a long list of numbers, and you can think of these lists as being like a number-based definition of a given word. Now, an interesting aspect of written language is that a single word can have many possible meanings, and it is only the word's position in a sentence and presence of other words around it that narrates the definition down to one particular meaning. For example, quantum is a word that has many different definitions, and when we see this word, we don't really know what it means until we see other words around it. Likewise, each embedding can be thought of as containing all possible meanings of each word. To refine each embedding down to a single precise definition, a process known as contextualization is used. In contextualization, each embedding is adjusted based upon other embeddings around it. This process helps highlight the meaning of each embedding that makes the most sense given its neighbors. The last step is generation, which is where the text actually gets written. By this point, each of the embeddings has absorbed a tremendous amount of information from their neighbors. The final processed embeddings are then passed to an output layer, which produces probabilities for each possible next word. Now, the model doesn't automatically pick the highest probability. Instead, it uses a mix of probability and randomness to select words, which helps create more natural and varied responses. The selected word is then added onto the end of our list of embeddings, and the entire process repeats itself all over. After generating each output token, the model will then pause and ask itself several questions to decide if it is done generating text. First, it will count the number of tokens it has generated, and see if it is larger than the max tokens parameter that was provided with the input request. This max tokens parameter will limit the total number of tokens that the model will generate. There is also a special end of sequence token that the model can generate. This is not a regular word. It is a special signal that the model uses to indicate that it has reached what it considers to be a natural end to its generation and that it should stop. Once the generation is complete, the API will send response back to your server. The response will contain a message, which has the generated text inside of it, along with usage and stop reason. The usage is a count of the number of tokens that you fed into the model and the number of tokens that were generated. The stop reason will tell you exactly why the model decided to stop generating text, whether it hits a natural end of sequence token, or maybe it exceeded the allotted number of tokens. Once your server has received this response, it will send the generated text back to your web or mobile app, where you will display it on the screen. So that is the entire flow. Now, we covered many topics in this video. I don't expect you to memorize any of this just yet. The only goal is to start to get you familiar with some common terminology around accessing Claude through the API.

</details>


> 🎬 **视频 03**：Making a request  
> 📁 文件：[03. Making a request.mp4](videos/03.%20Making%20a%20request.mp4)

**核心内容**：手把手演示如何用 Python 向 Anthropic API 发送第一个请求。

**关键要点**：
- 安装两个包：`anthropic`（SDK）和 `python-dotenv`（管理环境变量）
- 使用 `.env` 文件安全存储 API 密钥，务必加入 `.gitignore`
- 通过 `client.messages.create()` 发送请求，三个必需参数：model、max_tokens、messages
- max_tokens 是安全上限，Claude 不会刻意写满这个长度
- 消息分两种类型：user message（用户/开发者编写）和 assistant message（模型生成）
- 通过 `message.content[0].text` 提取纯文本回复

<details>
<summary>🇨🇳 查看中文翻译</summary>

前面我们已经聊了不少理论，所以在这个视频中，我们将换种方式，动手写一些代码。我们将学习如何向 Anthropic API 发送一个简单的基础请求。我将带你完成四个设置步骤。

第一步，我们将打开一个 Jupyter notebook 并安装 Anthropic Python SDK 和一个叫做 python-dotenv 的包。我已经在 notebook 中添加了一些注释来引导自己完成这个过程。在第一步中，我会加入一个魔法安装命令：`%pip install anthropic python-dotenv`。如果你和我一样在 Visual Studio Code 中编写 notebook，你可能会注意到百分号那里有红色语法提示，这完全没问题，可以忽略它。写好命令后，运行它来安装这些包。

接下来，我们将使用 python-dotenv 包来存储和加载我们的 API 密钥。我会在与 notebook 相同的目录中创建一个名为 `.env` 的特殊文件，在里面放入之前生成的 API 密钥。写法是：`ANTHROPIC_API_KEY="你的密钥"`。创建这个文件的原因是，当我们使用版本控制时可以忽略这个文件，这样就不会意外将它提交到 Git 并推送到公共仓库，让任何人都能看到。如果你使用 Git 或类似的版本控制系统，请确保在提交时忽略这个文件。

然后回到 notebook 中，我们可以安全地加载那个环境变量。第三步，我们将使用 Anthropic 包创建 API 客户端。在这个单元格中，我还会声明一个名为 model 的变量，这是一个字符串，包含我们要在 Anthropic API 中运行的模型名称，我们将使用 Claude Sonnet 4。

最后一步，我们将使用刚创建的客户端实际发送请求。在写代码之前，我想先介绍一些术语。首先要了解的是，我们将通过 Anthropic SDK 中的 create 函数来访问 Claude。这个函数需要三个必需的关键字参数：model（模型名称）、max_tokens（设置 Claude 可生成的最大 token 数量上限，比如设为 1000，Claude 生成超过这个长度时会自动停止）和 messages（消息列表）。

需要注意的是，Claude 不会试图达到你的 max tokens 数量，它只会写出它认为合适的回复。所以你应该把 max tokens 视为一种安全机制，确保不会生成过多文本。

现在重点来了——messages。想象一下之前讨论的聊天应用场景。用户输入问题给 Claude，期望得到回答。我们传入 create 函数的 messages 就是用来表示这些交流的。有两种类型的消息：user message（用户消息）包含我们要输入给 Claude 的文本，内容是由用户或开发者编写的；assistant message（助手消息）包含模型生成并返回给我们的文本。

有了这些知识，让我们发送第一个请求。回到 notebook 中，我声明一个 message 变量，调用 `client.messages.create`，传入 model、max_tokens（设为 1000），以及一个输入消息列表。在列表中放入一个用户消息，创建一个字典，包含 role 为 "user" 和 content 为我们要发送的问题，比如"什么是量子计算？用一句话回答"。

运行后，打印 message 变量，我们会看到返回了很多内容，其中包含了量子计算的定义。但在 message 变量中，我们的文本嵌套得很深。通常我们只想获取 Claude 生成的文本而不关心其他属性，所以要访问纯文本，我们可以写 `message.content[0].text`，这样就只会看到生成的文本了。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

We have done quite a bit of talking, so in this video, we're going to change things and get our hands dirty by writing it out a little bit of code. We're going to learn how to make a simple and basic request off to the Anthropic API. I'm going to walk you through four setup steps. So step one, we're going to open up a Jupyter notebook and install the Anthropic Python SDK, along with a package called python-dotenv. To get started, I'm going to open up a notebook on my own. I've already added in some comments to my notebook just to guide myself through this process. In step one up here, I'm going to add in a magic install command, so percent, pip install, Anthropic, python-dotenv. If you're writing your notebook inside a Visual Studio code as I am, you might notice a red syntax here coming from the percent over here. If you see that syntax here, it is totally fine. You can ignore it. Once I've written out this command, I'm going to run it to install these packages. I'm then going to clear the output just so you can see what's going on my screen a little bit more easily. Next, we are going to use that python-dotenv package to store and load our API key. As a reminder, I put in some directions on creating API key in the previous lecture. So if you did not create an API key, I would encourage you to go back to the previous lecture and find those directions. To store this key inside of my editor, I'm going to create a file in the same directory as my notebook with a very special name. I'm going to name this file.nv. And then inside of here, I'm going to place the API key that I generated a moment ago. I will write out exactly Anthropic underscore API underscore key and then an equal sign. And then inside of double quotes, I will put in that key. As a quick side note, the whole reason that we are creating this file and putting our key inside of here is so that we can now ignore this file when we are making use of version control. So that we do not accidentally commit this file, say to get, and then accidentally push it up to some public repository where anyone can see this file. So again, if you're making use of Git or a similar version control system, I would encourage you to make sure that you ignore this file anytime you are committing your work. Now, back inside of my notebook, I can securely load up that environment variable. Then onto set number three, where we will create our API clients using the Anthropic package. Inside the cell, I'm also going to declare a variable name model. This will be a string. It's going to contain the name of the model that we want to run inside of the Anthropic API. We are going to use Claude Sonnet 4. Now onto the last step where we are going to actually make a request using that client that we just created. Before we write out any code, however, I want to show you a little bit of terminology, just some stuff that's going to make things a little bit easier down the line. So the first thing to understand here is that we are going to access Claude by using the create function inside the Anthropic SDK. This function requires three different keyword arguments, a model, max tokens, and messages. The model keyword argument is just going to be the name of the model we want to run. We already defined that variable ahead of time in our previous cell. The second required keyword argument is max underscore tokens. This sets a maximum budget on a number of tokens that Claude can generate. For example, if we pass in a max tokens of 1000, if Claude tries to generate anything longer than that, then the generation will be automatically stopped. And we will receive back the first 1000 tokens that were generated. One thing to note here is that Claude doesn't try to target your number of max tokens. In other words, Claude won't try to write a response of 1000 tokens. It'll just write whatever response it thinks is appropriate. And as such, you should really view max tokens as being like a safety mechanism to ensure that you're not generating too much text. Finally, messages. And this is the part that I really want to focus on because messages are going to be a huge focus for us in the coming videos. To understand what messages are all about, I would like you to think back to the chat application we discussed a moment ago. So a user might type in some question to Claude and then expect to get an answer back. The messages that we're talking about when we pass these things into this create function are meant to represent exchanges like this. There are two types of messages, a user message and a assistant message. User messages contain text that we want to feed into Claude. The content inside of a user message is text that either a user or you and I as developers have authored. So in other words, a user message will contain text that has been written by some person. The second type of message is an assistant message. These messages contain text that have been produced by a model and sent back to us. At this point, I think we have enough knowledge to at least make our first request. So let's do that and then discuss messages a little bit more back inside of my notebook. In the very last cell, I'm going to declare a variable of message that will come from client messages create. And I'm going to pass in those different arguments that we just discussed. So I'll put in a model of model, a max tokens and I'll use 1000 here, which I think is definitely a safe limit. And then a list of input messages. So inside here, I'm going to put in one single user message and it will contain my question or my query that I want to send off to Claude. To create a user message, we'll create a dictionary that will have a role of user and then a content that will contain the actual string that we want to send into Claude. So in this case, I'm going to ask Claude to define quantum computing with something like what is quantum computing answer in one sentence. Then I'm going to run this and we'll take a moment or two to run because we are actually accessing Claude here. And then in the next cell down, I'm going to try to print out the message variable. We'll see what we get. All right, so inside of here, we can see there's a lot of stuff coming out, but noticeably we have a definition right around here of what quantum computing actually is. So inside of this message variable that we got back, our text is kind of deeply nested. We very often want to get just the text that Claude has generated and very often we don't really care about any of these other properties that are contained inside this thing. So to access just the generated text, we would write out message.content0.text like so. And if I run that cell again, now I'll see just the generated text and nothing else.

</details>

### 2.1 安装 SDK

```bash
# Python 3.7.1+ 必需
python --version

# 安装 Anthropic SDK
pip install anthropic
```

### 2.2 获取 API Key

1. 访问 [Anthropic Console](https://console.anthropic.com) 注册账号
2. 点击右上角头像 → **API Keys** → **Create Key**
3. 为 Key 命名后点击创建，**立即复制保存**（之后无法再查看）

> ⚠️ **安全提醒**：API Key 如同密码，切勿提交到 Git 或公开分享。Rate Limit 是在账户级别，不是 API Key 级别。

### 2.3 安全存储 API Key

**推荐方式：环境变量**

```bash
# 在 .bashrc / .zshrc 中添加
export ANTHROPIC_API_KEY="your-api-key-here"
```

**Python 中使用 dotenv（本地开发推荐）**

```python
# 安装
pip install python-dotenv

# 创建 .env 文件（记得加入 .gitignore！）
# ANTHROPIC_API_KEY=your-api-key-here
```

```python
from dotenv import load_dotenv
load_dotenv()  # 自动加载 .env 文件中的环境变量
```

### 2.4 第一次 API 调用

```python
import anthropic

# 方式一：自动读取环境变量 ANTHROPIC_API_KEY（推荐）
client = anthropic.Anthropic()

# 方式二：显式传入 Key（不推荐用于生产）
# client = anthropic.Anthropic(api_key="your-key-here")

# 发送第一条消息
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(response.content[0].text)
```

**三要素**：
- `model`：指定使用的模型（上一课已讲）
- `max_tokens`：**必填参数**，限制响应的最大 token 数
- `messages`：消息列表，消息的 `role` 只能是 `"user"` 或 `"assistant"`

### 2.5 响应结构

```python
# 响应对象的关键字段
print(response.id)            # 唯一请求 ID，如 "msg_01XFDUDYJgAACzvnptvVoYEL"
print(response.model)         # 实际使用的模型
print(response.role)          # 始终是 "assistant"
print(response.content)       # 内容列表（ContentBlock 对象）
print(response.content[0].text)  # 获取文本回复
print(response.stop_reason)   # 停止原因：end_turn / max_tokens / tool_use
print(response.usage)         # token 用量统计

# usage 详情
print(response.usage.input_tokens)   # 输入 token 数
print(response.usage.output_tokens)  # 输出 token 数
```

### 2.6 stop_reason 的三种值

| 值 | 含义 | 说明 |
|:--:|------|------|
| `end_turn` | 自然结束 | Claude 认为已完成回答 |
| `max_tokens` | 达到上限 | 输出被截断，可能需要增大 `max_tokens` |
| `tool_use` | 请求工具调用 | Claude 希望使用某个工具（模块 3 详讲） |

---

## 第 3 课：多轮对话

> 📹 视频：Multi-turn Conversations（9 min）  
> 📓 配套 Notebook：`02_messages_format.ipynb`


> 🎬 **视频 04**：Multi-Turn conversations  
> 📁 文件：[04. Multi-Turn conversations.mp4](videos/04.%20Multi-Turn%20conversations.mp4)

**核心内容**：讲解如何通过手动维护消息列表实现与 Claude 的多轮对话。

**关键要点**：
- Anthropic API 不存储任何消息——每次请求都是独立的，没有对话记忆
- 实现多轮对话的两个必要步骤：手动维护消息列表 + 每次请求传入完整历史
- 三个核心辅助函数：`add_user_message`、`add_assistant_message`、`chat`
- 必须将助手的回复也追加到消息列表中，才能保持上下文连贯
- 这三个辅助函数将贯穿整个课程后续内容

<details>
<summary>🇨🇳 查看中文翻译</summary>

到目前为止，我们编写的代码模拟了与模型之间非常简单的交互，我们可以把这个对话想象在一个聊天框里。我们发送了一个请求，比如"什么是量子计算？用一句话回答"，然后得到了一个简单的单句回复。自然地，我们可能想在某个时候继续这个对话，比如发送一个后续消息说"再写一句"，然后期望得到一个以某种方式扩展量子计算内容的回复。

要进行这样的多消息对话，你需要理解关于 Anthropic API 和 Claude 本身的一个非常关键的事实：Anthropic API 和 Claude 不会存储你发送给它的任何消息。你发送的消息不会以任何方式被存储，你收到的回复也不会被存储。所以如果你想要有某种对话——多条消息保持着上下文和连贯性——你需要做两件事：第一，在你的代码中手动维护一个包含所有交换消息的列表；第二，确保在每次后续请求中提供完整的消息列表。

让我先写一些示例代码来证明 Claude 不存储任何消息。我可以通过模拟一个对话来证明这一点——先问什么是量子计算，然后说"再写一句"。回到 notebook 中，我在最初问量子计算的单元格后粘贴了第二个请求，让 Claude "再写一句"。运行后，我们会发现得到的内容与量子计算完全无关。

为什么会这样？因为第二个请求中只有一条消息"再写一句"，而 Claude 对之前的对话或交换的消息没有任何记忆，所以它只能尽力满足请求，写出某个句子，但肯定不会是关于量子计算的。

那如何解决这个问题呢？首先，我们还是像之前一样发送只有一条用户消息的初始请求。然后把收到的助手消息追加到消息列表中。接着，当我们想继续对话时，在底部追加一条新的用户消息。这样我们可以把它读作一个完整的对话：我请求定义量子计算，得到了回复，现在我又加入了另一个请求。当我们把这个完整的消息列表发送给 Claude 时，它就拥有了整个对话的完整上下文和历史。

为了在代码中实现这一点，我在 notebook 中创建了三个辅助函数，这些函数在课程的其余部分会经常使用：

第一个函数 `add_user_message`：接受一个消息列表和一些文本，创建一个角色为 "user" 的消息字典并追加到列表中。

第二个函数 `add_assistant_message`：类似地，创建角色为 "assistant" 的消息字典并追加到列表中。

第三个函数 `chat`：接受一个消息列表，调用 `messages.create` 函数并返回 `message.content[0].text`。

现在来演示如何使用它们。首先创建一个空的消息列表来存储整个对话历史。然后调用 `add_user_message` 添加第一条消息"用一句话定义量子计算"。接着调用 `chat` 函数得到回复，打印出来。然后调用 `add_assistant_message` 将回复追加到对话历史中。最后再添加一条用户消息"再写一句"，再次调用 `chat`，这次应该能得到一个确实是关于量子计算的后续回复，因为我们正确地维护了完整的对话历史。

运行之后，我们确实得到了一个关于量子计算的后续消息。看起来我们已经正确地维护了整个对话历史。现在我们有了三个可重用的辅助函数，将在课程的其余部分继续使用。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

The code we've written out so far simulates a very simple exchange with our model, and we can kind of visualize this conversation inside of a chat box like this. We sent in a request asking something like what's quantum computing answer in one sentence, and we got a very simple single sentence reply. Naturally, we might want to continue this conversation at some point in time. So we might want to be able to send in a follow-up asking something like write another sentence, and we would then expect to get back a response that expands on quantum computing in some way. To have a multi-message conversation like this, there's something really critical that you need to understand around the Anthropic API and Claude itself. And that is that the Anthropic API and Claude do not store any messages that you send to it. None of the messages you send get stored in any way, and none of the responses that you get back are stored in any way. So if you ever want to have some kind of conversation going on, where you have multiple messages that kind of maintain a context or flow, then there are two things that you need to do. You need to manually, inside of your code, maintain a list of all the messages that you are exchanging. And second, you need to make sure that you provide that entire list of messages with every follow-up request that you make. So let's go into some detail on this entire idea, just to make sure it's really clear and you understand what's going on here. The first thing I want to do is write out a little bit of sample code just to prove to you that Claude doesn't store any messages or anything like that. And I can prove this by trying to simulate this kind of conversation, where I first ask what quantum computing is, and then ask write another sentence. So back inside of my notebook, I'm going to go to the cell where I initially asked what is quantum computing, and I'm going to paste in a second request to Claude that I wrote out ahead of time. So in this second request, I'm asking Claude to write another sentence, and I'm going to print out the text inside of that follow-up request. So now we've kind of got a simulation of what's going on right here, where we asked that first question, and then send in a follow-up. And we're going to see that we don't get back any kind of legible or any usable text here. So I'm going to run this, and we'll see what happens. So back over here, I'm going to run that cell now, and we're going to see that we get back something that has absolutely nothing to do with quantum computing at all. So again, to make sure that it's really clear why we are seeing this result and not seeing something about quantum computing, let's go over a couple of diagrams. All right, so in this diagram, I'm going to first show you exactly what's going on with the current code that I've written out, where we are getting back a response that has nothing to do with quantum computing. So initially, I make a singular request to Claude, where I have one user message, and I'm asking Claude to define quantum computing in one sentence. I then get back a response that is exactly what I would expect. Cloud gives me back a one-sense definition of quantum computing. Then I make a second request, where I have only one message inside the body, and the only message is asking Claude to write another sentence. When I send this in, Claude has no memory of any past conversation or any previous messages that I exchanged with it. So Claude is just going to do the best it can to fulfill my request. It's going to write out some sentence, but it definitely is probably not going to be about quantum computing. So now let me show you what we need to do to fix this problem. Here's how we're going to solve the issue. First, we're going to once again make that initial request with just one user message. Then we're going to take that assistant message that we get back, and append it into a list of messages. So we're going to take the assistant right there, and we can imagine we're going to add it into our list on the left-hand side. Then when we want to follow up on this conversation or continue it in some way, we're going to append on a user message at the bottom. So now we can read this as like a real conversation. I asked to find quantum computing. I got back a response, and now I'm adding in another question or another query that I want to ask Claude. In this case, write another sentence. Now when I send in this list of messages to Claude, it will have the entire context and history of the whole conversation. It's seen all the previous messages that we've exchanged around this line of questioning. And hopefully, Claude will be able to give us back a more reasonable answer, hopefully a one sentence follow up that's going to extend its previous answer a little bit more. To see this entire flow in action, I'm going to go back over to my notebook, and we're going to try to write out some code that will allow us to maintain the full context for a conversation. Back inside of my notebook, I'm going to get started by making three different helper functions that are going to aid us in maintaining the history or context of a conversation. We're going to end up using these helper functions quite a bit throughout the remainder of this course. So in this cell right here, I'm going to give myself a little bit of space at the top and then define our first helper function that will aid us in maintaining this history. I'm going to name this function add user message. It's going to take in a list of messages and some text. I'm then going to make a variable of user message. That's going to have a role of user and some content of whatever text we pass in. And then I'm going to append this new user message into the list of messages. Next, I'm going to add in a second helper function that's going to specialize in adding in assistant messages to a history. So I'm going to copy this function right here just to save a little bit of time. I'll rename it to add assistant message. And I'll go through and wherever I see the word user, I'm going to change it out to assistant. So right there, right there, and right there. Okay, now on to our third helper function. I'm going to take our messages.create function call down here. And I'm going to rename it to chat whenever I call chat, I'm going to pass in a list of messages. So this is going to be like my message history. Then I'm going to indent our call right here. I'm going to replace messages with the messages argument. And then return from this function is going to be message content at zero dot text. All right, so here are the three helper functions. And again, we're going to use these quite a bit throughout the remainder of this entire course. These helper functions are going to make it significantly easier for us to have a conversation that maintains some history or context over time. So now let me give you a demonstration of how we're going to put them to use. All right, so down here in the next cell down, I'm going to write in a couple of comments that she's going to guide us through the process of maintaining a conversation that has some history tied to it. I'll first begin by making an empty list of messages. So this message is variable right here. We can imagine is storing our entire conversation history over time. We're going to add in a collection of different user and assistant messages to it. Next, I'm going to add in my initial user message. So I will call the add user message function. I'll pass in the list of messages that I'm appending messages to. And then my user text is going to be defined quantum computing in one sentence. Now, just to make sure we're going down the right path here, I'm going to print out the list of messages and run the cell. And then we can see right away that we have a correct structure of messages. So I have a list. It has a dictionary inside of it with a role of user and a content that contains something that I want to feed into Claude. So now we can easily call a cloud by making use of that chat function that we just put together. I'm going to call chat and pass in my list of messages. And then out of that, we'll get back some kind of answer. I'm going to print out the answer and run the cell again. So we get the response. We should see a sentence here about quantum computing. So now we are in this situation. We have sent an initial message into Claude and gotten an assistant message back in response. Now we need to take this answer and append it into our conversation history. So we need to add in or append it in by making use of the add assistant message function that we just defined. So back over here, I'm going to call add assistant message. I want to add into our list of messages and I want to add in specifically the content out of the answer that we just got back. So now let's do another check and make sure that our list of messages is looking correct. If I print out messages, I should see my user message, then the follow up assistant with the content that we got back from Claude. Okay, so that looks good. So now onto the last step. We're going to append in one last user message and send the entire conversation history into Claude once again. So for that, I'll do another add user message with my list of messages. And then my follow up question here or my follow up request is going to be right another sentence. I'm then going to call chat again with the updated list of messages. I'll assign that to answer and then I will print answer out. So let's now run this and see how we are doing. All right, after a brief pause, we get what is definitely a follow up message that is definitely still about quantum computing. And so it appears that we have correctly maintained our entire conversation history. All right, so this is looking pretty good. We now have three reusable helper functions that we're going to continue to make use of throughout the remainder of the course.

</details>

### 3.1 API 是无状态的

Claude 的 API 是**无状态**的——每次请求都是独立的。要实现多轮对话，必须手动维护完整的消息历史：

```python
# 多轮对话示例
conversation = [
    {"role": "user", "content": "My name is Alice."},
]

# 第一轮
response1 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=conversation
)

# 将 Claude 的回复加入对话历史
conversation.append({
    "role": "assistant",
    "content": response1.content[0].text
})

# 第二轮 —— Claude 能记住前面的对话
conversation.append({
    "role": "user",
    "content": "What is my name?"
})

response2 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=conversation
)

print(response2.content[0].text)  # Claude 会回答 "Alice"
```

### 3.2 消息格式规则

1. `messages` 列表必须以 `user` 消息开头
2. `user` 和 `assistant` 消息必须**交替出现**
3. 可以连续发送多个 `user` 消息（系统会自动合并），但不推荐
4. `system` 不在 `messages` 中，而是单独的参数
5. Claude 通过完整的消息历史来理解上下文

---

## 第 4 课：构建简易聊天机器人

> 📹 视频：Building a Simple Chatbot（4 min）  
> 📓 配套 Notebook：`02_messages_format.ipynb`（聊天循环部分）


> 🎬 **视频 05**：Chat exercise  
> 📁 文件：[05. Chat exercise.mp4](videos/05.%20Chat%20exercise.mp4)

**核心内容**：动手练习——在 Jupyter notebook 中构建一个简单的循环聊天机器人。

**关键要点**：
- 使用 `while True` 循环实现持续对话
- 利用 Python 内置 `input()` 函数获取用户输入
- 复用之前定义的三个辅助函数：`add_user_message`、`add_assistant_message`、`chat`
- 完整流程：获取输入 → 添加用户消息 → 调用API → 添加助手消息 → 打印回复 → 循环
- 通过中断按钮(Interrupt)停止无限循环

<details>
<summary>🇨🇳 查看中文翻译</summary>

让我们做一个快速练习，确保到目前为止的内容都理解了。在这个练习中，我们将构建一个在 Jupyter notebook 中运行的小型聊天机器人。工作方式如下：每次运行单元格时，我们会使用内置的 `input` 函数提示用户输入文本。然后我们把用户输入的内容添加到消息列表中，将消息列表通过我们刚才编写的 `chat` 函数传递给 API。API 会给我们来自 Claude 的回复，也就是生成的文本。我们将把生成的文本添加到消息列表中，打印出来，然后循环回到第一步重复整个过程。

我先给你快速演示一下最终效果。我已经准备好了一个解决方案，隐藏在单元格中。每次运行单元格时，会立即提示用户输入。我输入"1加1等于几"，应该看到我的消息被打印出来，然后使用 `chat` 函数获取 Claude 的回复并打印出来。然后会再次提示我输入更多文本。我可以说"把那个答案加上去"，然后应该看到对话历史被正确维护了——我应该得到一个回复说，拿之前的答案2再加上去应该得到4。这个循环会一直进行，直到我最终点击中断按钮并按下 Escape 来停止。

如果你不熟悉内置的 `input` 函数，没关系。我给你一个小提示和模板代码。基本结构是这样的：初始化一个空的消息列表，然后有一个 `while True` 循环永远运行。在循环内部，使用内置的 `input` 函数请求用户输入文本，用户输入的内容会被赋值给 `user_input` 变量。

你可以在这里暂停视频自己尝试一下，或者继续看解决方案。

实现起来只需按照注释的步骤来：首先，用 `add_user_message` 函数把用户输入添加到消息列表中。然后，调用 `chat` 函数并传入消息列表，得到回复。接着，用 `add_assistant_message` 将回复作为助手消息添加到消息列表中。最后，打印出生成的文本，可选地加一些分隔线让输出更清晰。

测试一下：运行单元格，问 Claude "1加1等于几"，得到回复。再问"再加两个"，应该看到加上两个应该得到4。很好，这就是我们的简单循环聊天机器人实现。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Let's go through a quick exercise just to make sure everything is making sense so far. In this exercise, we're going to be building a very small chatbot that is going to run out of our Jupyter notebook. Here's how it's going to work. Whenever we run a cell, we're going to prompt the user to enter in some text using the built-in input function. We're then going to take whatever the user enters and add it into a list of messages. We'll then take the list of messages and pass it off to the API through the use of our chat function that we just put together. That's going to give us some feedback from Claude, so some generated text. We're going to take that generated text and add it into our list of messages. We'll print that generated text and then we will loop and go back to step one so that we repeat the entire process all over again. I'm going to show you how this thing is intended to work very quickly. So I've already put a solution together. I've hidden it inside the cell and I'm going to run this cell again just so you can see how I intend for this thing to work. Whenever I run the cell, I'm going to immediately prompt the user for some inputs using the built-in input function. I'll show you how to use that in just a moment in case you're not familiar with it. Then I'm going to enter in something like what's one plus one. I should see my message printed right away and then I should make use of the chat function to get a response from Claude and print that up as well. Then I should be prompted once again to add in some more text. Now I could say something like add to that answer. Then I should see that I'm maintaining the history or the context of my conversation. So I should now get a response back that says taking the previous answer to and adding to it should result in four. Again, this should go on forever until I eventually interrupt the process by clicking the interrupt button right here and hitting escape. Now as I mentioned, if you're not familiar with the built-in input function, no problem. I'm going to give you a little hint right now and just make sure that it's really clear what we want to do. So I'm going to paste in a little bit of code that you can use as a little template. All right, so here's the general structure that we want to use. We want to initialize a starting list of messages that's going to start off entirely empty and then we're going to have a while true loop that is going to run forever. And then inside the while loop, we're going to ask the user to enter in some text, making use of the again built-in input function. Whatever the user types into the displayed input will be assigned to this user input variable. And then I put some comments in here just to guide you through the steps of what we need to do. All right, so go ahead and pause the video right here. I would encourage you to give this exercise a shot. Otherwise, stick around and we'll go over a solution right now. So let's get to it. Let me show you how we would put this together. So to implement the rest of this, we really just have to follow the different comments that I put in here. The first thing we're going to do is take that user input and add it into our list of messages using the add user message function that we just put together a moment ago. So I'm going to call add user message. I'll pass in the list of messages and my user input. Then I'm going to call a clause using the built-in chat function and pass in my list of messages. That's going to give me back some answer. I'm going to take that answer and add it in as an assistant message to my list of messages. So add assistant message. Like so. And then I just need to print out the generated text. And optionally, I can put in some delimitators in the form of little dashes. Just make sure that it's clear to whoever's using this application that it's being generated by our AI. So I'll print a dash dash dash. And in between two of those, I'll print out my answer. That's why I got back. And that's it. So now to test this out, I'm going to run the cell. And then I should see some output up here underneath the cell after I start chatting with Claude. So I'm going to ask Claude what's one plus one. And I'll get my response back and two more. And I should see adding two more to one plus one should give us four. All right, very good. So there is our very simple implementation of a looping chatbot.

</details>

### 4.1 交互式聊天循环

将多轮对话封装成一个 while 循环，维护 conversation 列表：

```python
import anthropic

client = anthropic.Anthropic()

conversation_history = []

def chat(user_message):
    """发送消息并获取 Claude 的回复"""
    conversation_history.append({
        "role": "user",
        "content": user_message,
    })
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8096,
        system="You are a helpful AI assistant.",
        messages=conversation_history,
    )
    
    assistant_message = response.content[0].text
    
    # 将 Claude 的回复追加到对话历史
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message,
    })
    
    return assistant_message

# 交互式聊天循环
def main():
    print("开始聊天（输入 'quit' 退出）")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
        response = chat(user_input)
        print(f"\nClaude: {response}")

# main()  # 取消注释运行
```

**关键设计**：
- 实时追加用户消息和助手消息到 `conversation_history`
- 每次请求发送完整历史，让 Claude 理解整个对话

---

## 第 5 课：System Prompts

> 📹 视频：System Prompts（6 min）  
> 📓 配套 Notebook：`04_parameters.ipynb`（system 参数部分）


> 🎬 **视频 06**：System prompts  
> 📁 文件：[06. System prompts.mp4](videos/06.%20System%20prompts.mp4)

**核心内容**：讲解如何使用系统提示（System Prompt）自定义 Claude 的回复风格和语气。

**关键要点**：
- 系统提示是一个纯字符串，用于设定 Claude 的角色和回复风格
- 第一行通常给 Claude 分配角色（如"耐心的数学辅导员"），引导其行为模式
- 系统提示通过 `system` 关键字参数传入 `create()` 函数
- 当 system 为 None 时不能传入该参数，需动态组装参数字典
- chat 函数重构：system 参数默认为 None，使用 `**params` 解包方式灵活传参

<details>
<summary>🇨🇳 查看中文翻译</summary>

在这个视频中，我们将了解如何自定义 Claude 生成回复的语气和风格。为了帮助你理解这为什么重要，我想让你想象我们正在制作某种数学辅导聊天机器人。用户会使用这个聊天机器人来寻求解题帮助。例如，用户可能会请求帮助解 5x + 2 = 3。

有几件事情我们希望数学辅导员去做，也有几件事我们绝对不希望它做。比如，我们可能希望 Claude 最初只给学生一些提示，也许只给他们一两个关于如何入手的小建议。然后如果学生还是不太理解如何解题，才逐步引导学生完成解答。我们可能还希望 Claude 展示类似题目的解法，给学生一点灵感。同样，有些事情我们绝对不希望 Claude 做——比如，我们不希望 Claude 直接给出完整答案，也不希望 Claude 告诉学生去用计算器来解题之类的。

为了解决这个问题，我们将使用一种叫做系统提示（System Prompting）的技术。系统提示用于自定义 Claude 回复的风格和语气。我们将系统提示定义为一个纯字符串，然后传入 create 函数调用中。系统提示的第一行通常会给 Claude 分配一个角色。比如我们可以直接告诉 Claude 它是一个耐心的数学辅导员。这会鼓励 Claude 以真正的数学辅导员的方式来回应——可能会很耐心，提供很多解释，但不会直接回答学生的问题，而是引导他们找到解决方案。

现在让我们回到 notebook 看看实际效果。我在新的 notebook 中保留了客户端创建代码和三个辅助函数。首先，我不使用任何系统提示，直接问 Claude 解 5x + 3 = 2。运行后，我可能会看到一个精确的逐步解题过程。这对学生来说可能有用，但不是我们想要的效果。我们希望让学生思考，让他们自己得出答案，只给他们小步骤并引导他们走正确方向。

所以我们要使用系统提示来自定义 Claude 的回复方式。在 chat 函数中，我添加一个系统提示变量，告诉 Claude "你是一个耐心的数学辅导员，不应该直接回答学生的问题，而是给他们一些解题指导"，然后将系统提示作为 system 关键字参数传入 create 函数。

重新运行后，看到的回答好多了。Claude 不再直接告诉学生如何解题，而是引导用户逐步思考——先尝试将 x 隔离到等式一边，然后问学生该怎么做。这样学生就有了更好的互动式学习体验。

最后，我对 chat 函数做了一些重构。与其在函数内硬编码系统提示，不如让它作为参数传入。我添加了一个默认为 None 的 system 参数。但需要注意的是，不能传入 None 值的系统提示，所以我们需要更动态地组装参数——创建一个 params 字典，只在系统提示不为 None 时才将其添加进去，然后用 `**params` 解包传入 create 调用。这样，无论是否提供系统提示，chat 函数都能正常工作。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

In this video, we're going to take a look at how we can customize the tone and style of response that Claude generates. To help you understand why this is important, I want you to imagine that we are making some kind of math tutor chatbot. So a user will use this chatbot to ask for help in solving math problems. For example, a user might ask for help in solving 5x plus 2 equals 3. Now there's a couple of things that we would want our math tutor to do and a couple of things that we would definitely not want it to do. So for example, we might want Claude to initially only give the students some hints. Maybe just give them a little tip or two in how they might initially approach the problem. And then if the student still doesn't quite understand how to solve the problem, only then maybe walk the student through a solution step by step. We might also want Claude to show solutions for a similar problem to give the student a little bit of inspiration on how they might approach this particular problem. Likewise there are some things that we would definitely not want Claude to do. For example, we would not want Claude to just immediately respond with a complete answer. And we would also not want Claude to tell the student to just go use a calculator to solve the problem or something like that. So to solve this problem, we're going to use a technique known as system prompting. System prompts are used to customize the style and tone that Claude will respond with. We define a system prompt as a plain string and then pass it into the create function call. The first line of a system prompt will usually assign Claude a role. So we might directly tell Claude that they are a patient math tutor. This will encourage Claude to respond in the same way that a real math tutor was respond. It would probably end up being patient, provide a lot of explanation, but probably not directly answer a student's question. They'll instead guide them to a solution. Now to see some action, let's go back and return a notebook and see how Claude responds to math questions with and without a system prompt. So back inside of my notebook, I've made a new notebook and I've carried over just our initial client creation and those three helper functions. You do not have to create a new notebook. I'll just let you know that I did just to organize my code. Then down here inside the next cell, I'm going to ask Claude a very simple question. I'm going to ask it to solve a simple math problem. And we'll see how it initially responds. It will probably just give us a direct answer. And then we'll go back and add in a system prompt to encourage it to give us a little bit more explanation, kind of a tutor approach. So let's see how Claude responds to us without a system message at all. I'm going to make a list of messages. I'll add in a user message to my list of messages and I'm going to ask it to solve 5x plus 3 equals 2 for x. I'll then get an answer by calling chat with my list of messages and print out the answer. And then if I run the cell, I'm probably going to see an exact step-by-step solution on how to solve this. Now this probably is going to be useful for a student because it's going to show them a step-by-step solution, but it's not quite what we are going for. We want to make a student think and we want them to arrive at the solution on their own. We just want to give them small steps and kind of guide them in the right direction. So we're going to customize the way in which Cloud responds by using a system prompt. Let me show you how we do that. Up inside my chat function, I'm going to make a new variable of system. I'm going to assign to it a multi-line string. And inside there, I'm going to put together a system prompt that I wrote ahead of time. So I'm going to tell Claude that it is a patient math tutor. It should not directly answer student's questions. Instead, give them a little bit of guidance on how to solve the problem. And then I'm going to make sure that I pass in the system prompt as the system keyword argument to the create function. I'm then going to rerun the cell. I'll then go back down and let's see how Claude responds now. All right, this looks like a much better answer. Rather than just directly telling the student how to solve the problem, Claude is now prompting the user to go through a solution step-by-step. Claude is asking the student to first maybe isolate x on one side of the equation and then ask the student how we might go about that. So now we've got a much more interactive experience for the student. And this will help them learn what's going on here a little bit better than just giving them a direct answer. All right, so clearly using a system prompt is a powerful tool for steering Cloud in a particular direction on how it should answer a given user input. Before we move on, I want to do a little bit of a refactor to our chat function. Rather than having a hard-coded system prompt inside of here, I want to be able to specify a system prompt whenever we call the chat function. So in other words, I want to cut this right here, put it down inside this cell underneath, and then I want to be able to pass in a system prompt like so. So now we have a much more reusable chat function that we can use on a wide variety of different problems in the future without having a hard-coded system prompt inside of it. So now we need to make sure that we take this system argument and pass it into the create function. Now, doing so is going to require just a little bit more work than you might think. Let me show you why. I'm going to very quickly add in a system keyword argument to the chat function and I'll default it to be none. If I now run the cell and then run the cell down here, everything is going to work fine, exactly as expected. However, if I go down to the chat function and I decide that I do not want to provide a system prompt here at all, so if I delete that and then run the cell, I'll end up getting an error message. So we are not allowed to pass in a system prompt of none. So we need to assemble our parameters that are going to pass into the create function a little bit more dynamically. And if we have a system of none, we do not want to include this parameter at all. So let me show you how we are going to do that with a small refactor. First, I'm going to make a param's dictionary right above. I'm going to cut and paste in model, max tokens and messages. I'm going to convert this to dictionary syntax. So I use double quote, double quote, colon's like so. I'll then check and see if a system prompt was passed in. So if one was passed in, then I want to add it in as the system key inside the param's dictionary like so. Then I'm going to update the create call down here to star star params. And that's it. So now I'm going to rerun that cell. I'll go back down to the next one. And if I call chat without any system keyword argument being passed in, no problem. Everything is going to work just fine. And if I decide that I do want to provide a system prompt, yep, that's going to work just fine as well. Okay, so this looks good. So we now got support for a system prompt inside of our chat function.

</details>

### 5.1 什么是 System Prompt？

系统提示设置 Claude 的"人设"和行为规则，在整个对话中持续生效。它独立于 `messages`，不参与角色交替规则。

```python
# 基本用法
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a pirate. You always respond in pirate speak.",
    messages=[
        {"role": "user", "content": "How is the weather today?"}
    ]
)
print(response.content[0].text)
# 输出类似："Ahoy, matey! The skies be clear and the winds be fair today!"
```

### 5.2 System Prompt 最佳实践

- 用系统提示定义角色、语气、输出格式
- 把规则和限制放在系统提示中
- 系统提示中的指令优先级高于用户消息
- 保持简洁，避免过长（会消耗 token 和影响注意力）

---

## 第 6 课：System Prompt 练习

> 📹 视频：Writing System Prompts Exercise（1 min）  
> 本课为动手练习，无配套 Notebook


> 🎬 **视频 07**：System prompts exercise  
> 📁 文件：[07. System prompts exercise.mp4](videos/07.%20System%20prompts%20exercise.mp4)

**核心内容**：系统提示练习——通过设定角色让 Claude 生成更简洁的代码。

**关键要点**：
- 不加系统提示时，Claude 倾向于生成大量代码和详细解释
- 通过系统提示分配"编写简洁代码的 Python 工程师"角色，可显著减少输出量
- 系统提示能有效控制 Claude 的输出风格和详略程度

<details>
<summary>🇨🇳 查看中文翻译</summary>

让我们做一个关于系统提示的快速练习。我更新了 notebook，现在让 Claude 写一个检查字符串中重复字符的 Python 函数。运行并打印结果后，我会看到生成了大量代码——不仅有代码，还有很多解释和注释。

所以我想通过这个练习来减少生成的代码量，得到尽可能简洁的函数实现。为此，我想写一个系统提示并传入 chat 函数调用中。你的系统提示应该给 Claude 分配一个角色，鼓励它尽可能简洁地回复。

你可以在这里暂停视频自己试试，否则我们马上来看解决方案。

解决方法是：向 chat 函数调用传入一个系统提示，给 Claude 分配一个鼓励它写非常简洁代码的角色。我会说："你是一个编写非常简洁代码的 Python 工程师。"

现在运行单元格看看回复。好的，这绝对更符合我的期望了。你会看到实现这个唯一性检查的实际代码非常短，比之前看到的代码短得多。希望你在这个练习中也取得了成功。如果没有也完全没关系，在整个课程中还会有很多其他练习可以测试你的能力。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Let's go through a quick exercise on system props. I've updated my notebook and I'm now asking Claud to write out a Python function that is going to check a string for duplicate characters. If I run this and print out the answer, I'm going to see a tremendous amount of code gets generated here. So some of it is going to be a little bit of code, but there's also going to be a lot of explanation and a lot of comments as well. So I would like to go through an exercise here where we try to reduce the amount of code that's being generated. I want to get down to as concise and implementation of this function as possible. To do so, I would like to write out a system prompt and pass it into the chat function call. Your system prompt should assign a role to Claud and encourage it to respond as concisely as possible. So again, go ahead and pause the video here, go ahead and give it a shot, and we'll go over solution right about now. To solve this, I'm going to pass in a system prompt to the chat function call. And inside of that, I'm going to assign a role to Claud that will encourage it to write very concise code. I'll say you are a Python engineer who writes very concise code. So let's now run the cell and see what kind of response we get back now. All right, that is definitely much more in line with what I was looking for. You'll see that the actual code we had to write to implement this uniqueness check is very, very short, much shorter than the code we saw a moment ago. Hopefully you had some success with this exercise. And if you didn't, that is totally fine. We're going to be many other exercises throughout the course where you can test out your skills.

</details>

### 练习：为客服机器人编写系统提示

尝试为一个在线商城的客服机器人编写 System Prompt，要求：
- 专业但友好的语气
- 只回答与订单、退货、产品相关的问题
- 不泄露公司内部信息
- 超出能力范围时建议转人工

---

## 第 7 课：Temperature

> 📹 视频：Temperature（6 min）  
> 📓 配套 Notebook：`04_parameters.ipynb`（temperature 部分）


> 🎬 **视频 08**：Temperature  
> 📁 文件：[08. Temperature.mp4](videos/08.%20Temperature.mp4)

**核心内容**：讲解 Temperature（温度）参数如何影响 Claude 的文本生成概率分布。

**关键要点**：
- 文本生成流程：分词 → 概率预测 → 采样选择
- Temperature 是 0 到 1 之间的十进制值
- 温度越低，输出越确定和可预测；温度越高，输出越随机和多样
- 可在模型调用时通过 temperature 参数设置

<details>
<summary>🇨🇳 查看中文翻译</summary>

在课程前面，我们简要讨论了 Claude 实际生成文本的方式。回忆一下，我们将一些文本输入 Claude，比如"what do you think"。Claude 首先会对文本进行分词或将其分解成更小的块。然后 Claude 会经历一个预测阶段，决定哪些可能的词可以出现在后面，并为每个选项分配一个概率。最后在采样阶段，基于这些概率实际选择一个 token。

所以在图中，给定输入"what do you think"，可能的下一个 token 可能是 "about"、"wood" 等等。每个都被分配了一个概率，然后也许 Claude 选定 "about" 作为最佳的下一个 token。这整个过程会重复进行以完成句子或整条消息。

为了更清楚地理解这些概率，我将在本视频的其余部分使用图表来展示它们，从左到右按概率从高到低排列。

现在我想向你展示一种我们可以直接影响这些概率、控制 Claude 选择哪个 token 的方法。我们可以通过一个叫做 Temperature（温度）的参数来控制这些概率。Temperature 是一个在零到一之间的十进制值，我们在调用模型时提供它。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Earlier on inside this course, we spoke very briefly about how Claude actually generates text. Remember, we feed some amount of text into Claude, like the words, what do you think? Claude is then going to tokenize this text or break it up into smaller chunks. Claude is then going to go through a prediction phase where it decides what possible words could come next, and assign a probability to each of those different options. Finally, in the sampling phase, a token is actually chosen based upon these probabilities. So in this diagram I have on the screen, given inputs of what do you think possible next tokens might be about, wood, and so on. Everything you see here on the right hand side. Each of these gets assigned a probability, and then maybe in this case, Claude settles on about as being the best possible next token. So we would end up with a phrase, what do you think about? This entire process is then repeated to complete the sentence or complete the entire message. Now just to make sure things are really clear, the numbers I'm showing here are probabilities, the percentage chance of each token being selected. Just to make things a little bit more clear with these probabilities, I'm going to display them in a chart for the rest of this video. So still the same probabilities just in a format that's easier for us to understand. You'll also notice I've kind of sorted them from left to right. There's no actual internal sorting going on. I'm just sorting them greatest to these probability just to make this chart a little bit easier to understand. So now that we have a reminder on how Claude generates text, I want to show you one way that we can directly influence these probabilities and control which token Claude might actually decide to select. So we can control these probabilities using a parameter called temperature. Temperature is a decimal value between zero and one that we provide when we make our model call.

</details>

### 7.1 Temperature 参数

控制输出的随机性。取值范围 `0.0 ~ 1.0`：

| Temperature | 效果 | 适用场景 |
|:-----------:|------|---------|
| 0.0 | 最确定性，几乎每次相同 | 分类、数据抽取、代码生成 |
| 0.5 | 适度创意 | 一般写作、总结 |
| 1.0 | 最大随机性 | 头脑风暴、创意写作、诗歌 |

```python
# 低温度 — 确定性输出
response_low = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    temperature=0.0,  # 最确定
    messages=[{"role": "user", "content": "What is 2+2?"}]
)

# 高温度 — 多样性输出
response_high = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    temperature=1.0,  # 最随机
    messages=[{"role": "user", "content": "Write a haiku about programming."}]
)
```

### 7.2 其他关键参数

#### max_tokens

限制 Claude 输出的最大 token 数。**这是必填参数**。

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=50,  # 仅允许 50 个 token
    messages=[{"role": "user", "content": "Write a long essay about AI."}]
)

print(response.stop_reason)  # "max_tokens" — 被截断了！
```

> 💡 **注意**：模型不知道 `max_tokens` 的值。它无法主动控制输出长度来避免截断。

#### stop_sequences（停止序列）

让 Claude 在遇到特定字符串时立即停止生成：

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    stop_sequences=["END", "---"],  # 遇到这些字符串就停止
    messages=[
        {"role": "user", "content": "Count from 1 to 10, then write END."}
    ]
)
```

#### top_p 和 top_k

进一步控制采样策略（通常不需要调整）：

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    temperature=0.7,
    top_p=0.9,   # 从概率总和 90% 的 token 中采样
    top_k=40,    # 从前 40 个最可能的 token 中采样
    messages=[{"role": "user", "content": "Write a creative story opening."}]
)
```

> 💡 **建议**：一般只调 `temperature` 就够了。`top_p` 和 `top_k` 是高级用法，两者通常不需要同时使用。

### 7.3 参数速查表

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|:----:|:----:|:------:|------|
| `model` | str | ✅ | — | 模型标识符 |
| `max_tokens` | int | ✅ | — | 最大输出 token 数 |
| `messages` | list | ✅ | — | 对话消息列表 |
| `system` | str | ❌ | 无 | 系统提示 |
| `temperature` | float | ❌ | 1.0 | 随机性（0~1） |
| `top_p` | float | ❌ | — | 核采样阈值 |
| `top_k` | int | ❌ | — | Top-K 采样 |
| `stop_sequences` | list | ❌ | [] | 停止序列 |
| `stream` | bool | ❌ | false | 是否流式输出 |
| `metadata` | dict | ❌ | — | 请求元数据 |

---

## 第 8 课：流式输出

> 📹 视频：Streaming Responses（8 min）  
> 📓 配套 Notebook：`05_Streaming.ipynb`


> 🎬 **视频 09**：Response streaming  
> 📁 文件：[09. Response streaming.mp4](videos/09.%20Response%20streaming.mp4)

**核心内容**：讲解流式传输（Streaming）技术，实现实时逐块显示 Claude 的回复。

**关键要点**：
- 非流式请求可能需要 10-30 秒才能返回完整响应，用户体验差
- 流式传输让文本逐块到达，用户几乎立即开始看到回复
- 方式一：`client.messages.create(stream=True)` + 遍历事件流
- 方式二（推荐）：`client.messages.stream()` + `stream.text_stream` 直接获取文本
- 关键事件类型：`raw_content_block_delta` 包含实际生成的文本
- 使用 `stream.get_final_message()` 获取完整组装后的消息用于存储

<details>
<summary>🇨🇳 查看中文翻译</summary>

我想让你回想一下我们在本节前面看过的聊天界面示例。记住，思路是我们在 Web 应用或移动应用中运行一个聊天窗口。用户输入一个问题，发送到我们的服务器，我们把它封装成一条用户消息并发送给 Claude。Claude 然后会返回一条助手消息，我们提取其中的文本并发送回应用，希望内容能显示在屏幕上。

这一切听起来都很简单，但有一个小问题我们还没有解决。从发送用户消息到最终收到助手消息回复之间的时间，很可能比我们预期的要长得多。在某些情况下，可能需要 10 秒甚至长达 30 秒，具体取决于输入的用户消息和输出的助手消息的大小。在用户等待回复的整个过程中，我们可以只在屏幕上显示一个加载动画，但这不是很好的用户体验。大多数用户的期望是，当他们输入某条消息后，几乎应该立即在屏幕上开始看到回复。

为了获得更好的用户体验，我们将使用一种叫做流式传输（Streaming）的技术。我来告诉你流式传输是如何工作的。我们的服务器仍然会发送初始用户消息给 Claude，但 Claude 会几乎立即发回一个初始响应。这个初始响应实际上不包含任何文本内容，它只是向我们的服务器发出信号，表示 Claude 已收到请求并即将开始生成文本。然后我们将开始接收一个事件流。每个事件包含生成响应的一小部分，我们需要将其发送回来并最终显示给用户。

接收的事件数量取决于生成多少文本。每个事件只包含整体消息的一小部分。比如第一个事件可能只有文本"quantum"，第二个是"computing"，第三个是其他内容。每个事件不一定只包含一个词，可能包含多个词甚至整个句子。

回到 notebook 中，我们会忽略之前的 chat 函数，因为流式传输不太适合我们当前实现的 chat 函数。我创建一个消息列表，手动调用 `client.messages.create` 函数，传入模型名、max_tokens、消息列表，以及一个额外的关键字参数 `stream=True`。这不会给我们最终答案，而是返回一个不同事件的流。我们可以用 for 循环遍历它。

运行后，我们会很快看到一系列不同的事件：`raw_message_start` 事件、`raw_content_block_start`、多个 `raw_content_block_delta`，然后是 `content_block_stop`、`message_delta` 和 `message_stop`。这些都是在单个请求中 Claude 发送给我们的事件。

我们通常最关心的事件类型是 `raw_content_block_delta`——这个事件包含 Claude 逐块生成的实际文本。我们通常想收集所有这些事件并提取文本发送回应用。

不过 Anthropic SDK 提供了一种更简单的流式方式。使用 `with client.messages.stream(model=..., max_tokens=..., messages=...) as stream:` 语法块，然后用 `for text in stream.text_stream:` 迭代，这样 text 就直接是那些事件中的文本部分了。这几乎总是我们真正关心的内容。打印时设置 `end=""` 确保打印语句不添加换行符，这样每段文本会相邻显示。

最后还有一个功能：流式传输完成后，我们经常想获取完整的消息并存储到数据库中。使用 `stream.get_final_message()` 可以将所有单独的事件组装成一条最终消息。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

I want to think back to the original chat interface example that we looked at earlier on inside this section. So remember, the thought process here is that we've got a chat window running inside of a web app or a mobile app. A user is going to enter a question, that's going to be submitted to our server, we're thinking of stuff that into a user message and send it off to Claude. Claude is then going to send us back an assistant message, we are going to extract the text from it and send it back down to our mobile app or web app, and hopefully that content is going to appear on the screen. Now, this all sounds pretty straightforward and easy at this point in time, but there's one little issue here that we haven't really addressed just yet. You see, the time between sending that user message to Claude and then eventually getting an assistant message back can very easily take a lot more time than we expect. In some cases, it might take 10 seconds or all the way up to 30 seconds depending upon the size of the input user message and the output assistant message. Now, during this entire time that the user is waiting for a response, we could just show a spinner on the screen, but that's not really a great user experience. Most users' expectations are that whenever they enter in some kind of initial message, like what is quantum computing, they should almost immediately start to see some response up here on the screen. To get this better user experience, we are going to use a technique known as streaming. So let me tell you a little bit about how streaming works. Our server is still going to send an initial user message off to Claude, but then Claude is going to almost immediately send back an initial response to us. This initial response doesn't actually contain any text content. Instead, it is really just a sign to our server that Claude has received our initial request and that Claude is about to start to generate some amount of text. We are then going to start to receive a stream of events. We're going to go into a lot of detail around exactly what these events are, but for right now, just understand that they contain pieces of the generated response that we want to send back and eventually display to our users. The number of events that we receive depends upon how much text we are generating. Each event is going to contain just a little bit of the overall message that is being generated. So maybe the first event just has the text, quantum, and then the second one says computing, and the third one is, and so on. Now, each event doesn't just contain one word. My contain many words or even an entire sentence. It really just depends upon how much time it takes for Claude to generate each little bit of text. Now, as I mentioned, our server is going to receive these events, and our server can optionally take the text out of each event and immediately send it back down to our web app or mobile app or whatever else where we can display that little chunk of text on the screen. We can then repeat this process for each additional event that we receive on our server. So the net effect is that a user is going to start to see some text, start to appear chunk by chunk in the chat interface. Let's now go back over to our notebook, and we're going to write out a little bit of code to better understand how streaming works. All right, so back inside of my notebook, I still have these three helper functions put together. Now, we are going to ignore the chat function inside of this video because when we start to use streaming, it doesn't work quite so well with the chat function as we have implemented it. So I'm going to instead, down here, make a list of messages and then manually call the client messages.create function. So I'm going to make an empty list of messages. I'll add in a user message to messages, and I'm going to ask Claude to write a one sentence description of a fake database. I'm then going to call client messages create. I will pass in the name of the model. Still need to provide a max tokens. Provide our list of messages. And then finally, we'll put in an additional keyword argument here of stream is true. This is going to give us back not a final answer, but instead we're going to get a stream of different events. We can iterate through this thing because it is a normal iterator. So we can say for event in stream and then print out event. Now, if I run this, we're going to very quickly see a stream of different events up here on screen. So each of these represents a different little chunk of data that is being sent back to us by Claude. You'll notice that we start off with a event named raw message story event. We then get a raw content block start, a raw content block delta. We get several of those as a matter of fact. And then down towards the bottom, we eventually get a content block stop event, a message delta event, any message stop event. So these are all events that are being sent back to us inside of the context of a single request, all coming from Claude. Each of these different events has some meaning in the context of the overall response that we are getting back from Claude. However, there is one event type that we usually care about a little bit more than all the others. And that is the raw content block delta event. This event is what contains the actual text that is being generated by Claude and sent back to us chunk by chunk. In practice, we usually end up getting the same sequence of events over and over. So when we get a response back from Claude, we're almost always going to start off with getting a message start, then a content block start, and then we are going to get a sequence of content block delta. And again, those are what contain the actual text. So we usually want to collect all those different events and extract the text from them and send that text back down to our web app or mobile app or whatever else we are using. Now back inside of our notebook, inside this for loop right here, we could add in a check to take a look and figure out what kind of event we are dealing with. And then if it is one of those raw content block delta events, we could reach into it and get the text we actually care about. But that would require a lot of extra code from us. Thankfully, the Anthropic SDK exposes a different way of creating a stream than what I'm showing to you right here. This alternative way of creating a stream, which I'm going to show you in just one moment, makes it a lot easier to just get the text out of the response. And again, the text is usually the part of the response that we really care about. So let me show you an alternative way of streaming a response. I'm going to go down to the next code cell. So down here, I'm going to again make a list of messages, add a user message with a write a one sentence description of a fake database. And then we're going to call a slightly different function and wrap it inside of a with block. So say with client messages, dot stream. And inside of here, we will again put in our model, our max tokens. And our messages. But we do not need to add in the stream to true argument. We'll then say as stream, colon, all then indent. And inside of here, it will say for text in stream. Text stream like so. So now text is going to be just the text part of those different events. So just the text we actually care about. Again, that's almost always the thing that we actually really care about when we are streaming our response from Claude. Now to show you how this actually works, I'm going to add in a print statement and log out that text. I'm going to add in a end true of empty string and true of empty string. Just make sure that these print statements are not going to add in a new line character to the end of the print statement. So we'll see each bit of text logged out next to each other. Now going to run this and it's going to occur really quickly. But you'll see that now we are getting a response streamed back to us chunk by chunk. So let me do that again. So run again, I'll see chunk, chunk, chunk. There we go. You'll notice that each chunk contains multiple different words. So again, we're not guaranteed to just get back one single word inside of each event. We might get several. There is one last feature here that I want to show you. Now, as I've mentioned, we very often want to stream a response back to a mobile app or a web app so that that a user can see each chunk of text appear on the screen as soon as possible. But something else we very often want to do after completing a stream is take the entire message and maybe store it inside of a database. So we have a record of the entire conversation that was had with a particular user. Let me show you how we can collect all these different events and present them all assembled together inside of one single final message. I'm going to replace this print statement right here with a pass just so we don't have any printing there. And then after it, I'll do a stream dot get final message. And now if I run this again, we are still streaming back a response and we could print it if we wanted to. But we're also going to take all the individual events we get back and assemble them together into one final message, which we could then store inside of a database or do whatever else we need to do with it.

</details>

### 8.1 为什么需要流式输出？

默认情况下，API 会等 Claude 完整生成后才返回响应。对于长回复，用户可能等待几秒甚至几十秒。

流式输出让你**逐步接收** Claude 的回复，实现"打字机效果"，大幅提升用户体验。

### 8.2 基本流式输出

```python
import anthropic

client = anthropic.Anthropic()

# 使用 stream=True 启用流式输出
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a short story about a robot."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()  # 换行
```

### 8.3 流式事件类型

使用底层事件 API 可以获得更细粒度的控制：

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
) as stream:
    for event in stream:
        # 不同事件类型
        if event.type == "message_start":
            print("开始生成...")
        elif event.type == "content_block_start":
            print("内容块开始")
        elif event.type == "content_block_delta":
            # 这里是实际的文本片段
            if hasattr(event.delta, 'text'):
                print(event.delta.text, end="", flush=True)
        elif event.type == "message_stop":
            print("\n生成完成！")
```

### 8.4 获取流式响应的最终消息

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a joke."}]
) as stream:
    # 消费流
    for text in stream.text_stream:
        print(text, end="", flush=True)
    
    # 获取完整的最终消息对象
    final_message = stream.get_final_message()
    print(f"\n\n使用的 token 数: {final_message.usage}")
```

### 8.5 异步流式输出

```python
import asyncio
import anthropic

async def stream_response():
    client = anthropic.AsyncAnthropic()
    
    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Write a poem about coding."}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

# asyncio.run(stream_response())
```

---

## 第 9 课：结构化数据输出

> 📹 视频：Structured Data（6 min）  
> 📓 配套 Notebook：`06_vision.ipynb`


> 🎬 **视频 10**：Structured data  
> 📁 文件：[10. Structured data.mp4](videos/10.%20Structured%20data.mp4)

**核心内容**：讲解如何结合停止序列和助手消息预填充来生成纯净的结构化数据。

**关键要点**：
- Claude 生成结构化数据时倾向于添加额外的标题、说明和评论
- 助手消息预填充：预设回复开头（如 ` ```json `），让 Claude 认为已开始输出结构化内容
- 停止序列：设定触发停止的字符串（如 ` ``` `），在 Claude 试图关闭代码块时立即截断
- 两者配合实现"给我中间的内容"效果——只返回纯净的结构化数据
- 此技术适用于所有结构化数据类型（JSON、代码、列表等），不限于 JSON

<details>
<summary>🇨🇳 查看中文翻译</summary>

停止序列和助手消息预填充可以以非常强大的方式组合在一起使用，这在你需要生成任何类型的结构化数据时可能会经常用到。

为了帮助你理解它们如何协同工作，让我举个例子。假设我们正在构建一个 Web 应用，它会根据用户输入生成 EventBridge 规则。如果你不熟悉的话，EventBridge 规则是在 AWS 中使用的小型 JSON 代码片段。用户输入一些提示然后点击生成。用户体验的关键部分是，我们只想显示生成规则的 JSON，不要其他任何东西。如果我们显示了一个包含头部说明和底部评论的响应，用户就没法直接使用"复制全部"按钮了。

需要明确的是，这不仅限于生成 JSON。实际上，任何时候你使用 Claude 生成结构化数据——无论是 JSON、Python 还是项目符号列表——Claude 都经常会插入标题、页脚或额外的说明性文字。在很多场景中，你不想要那些额外内容，只想要你要求 Claude 创建的原始内容。

为了让 Claude 只给我们需要的原始内容，我们可以结合使用停止序列和预填充助手消息。

回到 notebook 中，我创建消息列表并添加一条用户消息"生成一个简短的 EventBridge 规则，以 JSON 格式"。运行后，我们确实得到了一些 JSON，但不幸的是它有三个反引号和 JSON 标记（Markdown 代码块格式）。对我们来说不需要那些额外字符，只要纯 JSON。

解决方法是同时使用助手消息预填充和停止序列。首先，预填充一条助手消息，内容为 ` ```json `。然后在 chat 调用中添加停止序列：一旦遇到 ` ``` ` 就立即停止生成。

运行后，我们就只得到纯 JSON 了。可能有一些换行符，但这完全没问题——可以通过 `json.loads(text.strip())` 轻松处理。

这是怎么回事呢？Claude 看到用户消息后，自然想写完整规则加上说明。但它遇到了预填充的助手消息，会认为它已经写了那些内容，所以只需要写出实际的 JSON。当它写完 JSON 后，自然想关闭 Markdown 代码块，加上结尾的三个反引号。但一旦这样做，就会触发停止序列，立即停止生成并返回响应。所以本质上我们是在说"以这个开头，以那个结尾，只给我们中间的内容"。

这是一种非常强大的技术，我们会经常使用。任何时候想要生成某种结构化数据并且只获取那些数据而不附带其他内容时，都可以使用助手消息预填充配合停止序列。记住，这种技术不仅限于 JSON，适用于任何结构化数据。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Stop sequences and assistant message prefilling can be combined together in a really powerful way. Something that you're probably going to end up doing rather frequently, anytime you need to generate some kind of structured data. So to help you understand how these things work together, we'll me walk you through a really quick example. Let's imagine that we are building a web app like the one you see on the screen. This is a web app that's going to generate event bridge rules based upon some user input. If you're not familiar with them, event bridge rules are used in AWS the essentially little JSON snippets. So user is going to enter in some prompt like this and then click on generate. In chances are the user is going to want to see some generated rule just up here that they can very easily select right away or click on this little copy button and go use somewhere else. The point there is that part of the critical user experience here is that we want to show just the JSON for the generated rule and nothing else. So if we instead displayed a response that looks like this, it would definitely not be as helpful for our users. We're still generating the rule, but now it also has this header up top and this commentary footer down at the bottom. So now a user can't really use this copy all button. They would have to go in and manually select that JSON right there. So this is an example where we really don't want Claude to be that helpful and explains work. We want just some very particular data and nothing else. Now to be clear, this is not a problem that is just limited to generating JSON. It turns out that anytime you are using Claude to generate any kind of structured data. So it could be JSON or it could be Python or even just a bulleted list of text items. Claude is very often going to try to insert a header or a footer or some additional kind of commentary. And in many of these scenarios, you don't want that additional commentary. You just want the raw content that you asked Claude to create. So to help keep Claude on track here and only give us the raw content we're asking for and no additional header or footer or commentary or anything like that, we can use a stop sequence in combination with a pre-filled assistant message. Let me show you how. I'm going to go back over to my notebook. I'm going to continue on by making a new cell down here. I'm going to again make a list of messages. I'll add in a user message. And I'll say something like generate a very short event, ridge rule as JSON. I'll then pass that off like so. And then let's just see what we get with this kind of initial take. So right away, we can see that we do get back some JSON, but it has unfortunately that little back tick, back tick, back tick, back tick JSON right there. And then a matching closing one over there. And just to make sure it's super clear, these back ticks are in place to format this all as markdown. So it gets formatted very nicely if you were to render it as markdown text. But in our case, we don't want any of those additional characters. We want just the Rob JSON by itself. So to do so, we can do two things. We're going to use both an assistant message and a stop sequence. For right now, we're just going to write out the code to do so. And then I'll show you a diagram that explains how it all works. First, I'm going to pre-fill an assistant message. So let's say add assistant message. And my pre-filled message will be back tick, back tick, back tick, JSON. And then on my chat call, I'll add in stop sequences. And anytime we see a back tick, back tick, back tick, I want to immediately stop generation. So let's now run the cell and see what we get back. Okay, so now we get just the JSON by itself. You will notice that there are some new line characters in here, but that's totally fine. We can very easily remove those extra new lines by just parsing the response as JSON or by doing a strip call. So I could say text is chat, I'll print out text. And then on the next cell down, I might import JSON and do a JSON loads with text and strip on text as well. And if I run that, yes, we definitely get back some very well-formatted JSON here that we can access in any way that we expect. All right, so what exactly is going on with the assistant message and the stop sequence? Well, let me show you diagram just to break it all down and make sure it is super clear. So once again, we are doing our user message. We're providing a pre-filled assistant and a stop sequence. Claude is going to take a look at all the different parts of this request. It's going to initially take a look at that user message content and say, all right, it's very clear that I need to write a full rule. And I should probably also describe it. So maybe put on a header and a footer because that's kind of what Claude naturally wants to do. It wants to explain the work that is doing. But then it's going to encounter that assistant message. And just as we learned in the last video, Claude is going to assume that it already wrote that out in its response. So it's going to say, oh, I've already started the JSON part. So now all I have to do is write out the actual JSON. It's then going to write out all of this JSON in the response. And then as it gets to the very end, it's going to naturally want to close off that markdown code block that it thought it created earlier. So Claude is going to want to put in a closing backtick, backtick, backtick. As soon as it does so, however, it's going to encounter the stop sequence which stops the generation entirely and immediately sends us back the response. So you can really imagine that what's really going on here is we're kind of saying, start with this and with that and just give us everything in between. And that results in us just getting back the part we really care about, just the JSON by itself. And like I mentioned, this is a really powerful technique that we're going to use very often. Anytime we want to generate some kind of structured data and get just that data with nothing else besides it. And remember, this technique can be used for any kind of structured data. It is not limited just being used on JSON. So anytime we have any kind of very specific content we want to generate and get just that content with no additional commentary on it, we're going to take a look at using assistant message prefilling along with stop sequences.

</details>

### 9.1 让 Claude 输出 JSON

通过提示约束，让 Claude 返回结构化数据：

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": """Extract the following information from the text and return as JSON:
- name
- age
- city

Text: "John is 30 years old and lives in New York."

Return ONLY valid JSON, nothing else."""
    }]
)
print(response.content[0].text)
```

### 9.2 Vision（图片理解）

Claude 可以分析和理解图片内容，支持：
- **图片描述**：描述图片中的内容
- **OCR/文本识别**：提取图片中的文字
- **图表解读**：分析图表、数据可视化
- **代码截图**：理解代码截图的内容

**支持格式**：JPEG、PNG、GIF、WebP  
**大小限制**：单张图片最大 5MB，长边不超过 8000px

#### URL 引用

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
                    }
                },
                {
                    "type": "text",
                    "text": "What do you see in this image?"
                }
            ]
        }
    ]
)
print(response.content[0].text)
```

#### Base64 编码

```python
import base64
import mimetypes

def encode_image(image_path):
    """将本地图片编码为 base64"""
    with open(image_path, "rb") as f:
        binary_data = f.read()
    
    base64_string = base64.b64encode(binary_data).decode("utf-8")
    mime_type, _ = mimetypes.guess_type(image_path)
    
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": base64_string
        }
    }

# 使用本地图片
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                encode_image("./my_photo.png"),
                {"type": "text", "text": "Describe this image in detail."}
            ]
        }
    ]
)
```

### 9.3 stop_reason 判断输出完整性

当让 Claude 输出结构化数据时，务必检查 `stop_reason`：
- `end_turn`：正常结束，输出完整
- `max_tokens`：被截断了，JSON 可能不完整

---

## 第 10 课：结构化数据练习

> 📹 视频：Structured Data Exercise（5 min）  
> 本课为动手练习


> 🎬 **视频 11**：Structured data exercise  
> 📁 文件：[11. Structured data exercise.mp4](videos/11.%20Structured%20data%20exercise.mp4)

**核心内容**：停止序列和消息预填充的实战练习——让 Claude 只输出纯净的 CLI 命令。

**关键要点**：
- 练习目标：让 Claude 输出三条 AWS CLI 命令，不含任何注释或说明
- 预填充 ` ```bash ` 来让 Claude 直接进入代码输出模式
- 停止序列设为 ` ``` ` 在代码块结束时截断
- 预填充可以包含描述性文字来引导输出格式（如"以下是所有三个命令，不含注释："）
- 这展示了预填充不仅限于标记字符，还能用自然语言引导输出结构

<details>
<summary>🇨🇳 查看中文翻译</summary>

让我们做一个快速练习，确保停止序列和消息预填充的概念非常清楚。在这个练习中，我希望你写出屏幕上看到的代码。看一下提示，它说"生成三个不同的 AWS CLI 示例命令"。

运行这段代码后，你可能会得到类似这样的输出。它确实给了我们三个不同的示例命令，但周围有很多注释——有标题，然后是列出每个命令的编号。

对于这个练习，我希望你使用消息预填充和停止序列，让所有三个命令在一个响应中紧挨着出现，没有任何额外的注释或解释。而且只使用消息预填充和停止序列，不要调整提示本身。

我给了一个小提示：消息预填充不仅限于使用反引号之类的字符，你可以放入任何类型的预填充回复。建议你暂停视频自己尝试。

来看解决方案。首先，观察没有预填充或停止序列时的输出。我们会注意到每个命令都被三个反引号包裹着。所以一个好的起点是预填充一条助手消息，内容为三个反引号，告诉 Claude 直接开始写命令，跳过任何开头的注释。然后也设置停止序列为三个反引号。

运行后，初始输出看起来还行但不完美——我们得到了三个命令，但开头多了一个 "bash" 字样。这是因为三个反引号表示 Markdown 代码块，Claude 决定加上 bash 作为语言标识符来实现语法高亮。

为了解决这个问题，我们可以在预填充消息中自己加上 "bash"，这样 Claude 就知道它已经在一个 bash 代码块中了。再次运行后效果更好了。

从这里开始，可能还有两个问题需要解决：有时只会得到一个命令（Claude 可能想写三个独立的代码块），以及 Claude 可能插入 bash 格式的注释。为了消除这些问题，可以利用提示中的提示——预填充不仅限于字符标记，还可以用来大幅引导 Claude 的回答方式。比如添加"以下是所有三个命令，在单个代码块中，不含任何注释："然后换行开始 Markdown。

再次运行后，就能得到更可靠的输出了。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Let's go through a very quick exercise, just to make sure the idea of stop sequences and message prefilling are super clear. So in this exercise, I'd like you to write out the exact code I've got right here on the screen. All this code should be really familiar. If you take a look at the prompt, it says generate three different sample AWS CLI commands. Now when you run this code, you're probably gonna get back some output that looks vaguely like this right here. Just make it a little bit easier to read. I rendered it as markdown down here. So here's the sample starting output that I get. You'll notice that it does give us three different sample commands, but it has a lot of commentary around them. So I've got a header and then some numbers listing out each individual command. For this exercise, I would like you to take this code and using all the message prefilling and stop sequences, I want you to get all three different commands in a single response, all right next to each other without any additional comments or explanation or anything like that. And I'd like you to do this using only message prefilling and stop sequences. So no adjusting this prompt at all. So go ahead and give this a shot. I did put a little hint on here, just as a reminder, with message prefilling, it's not limited just to using characters like the back tick, back tick, back tick. You could put any kind of prefil response you want. I would encourage you to pause this video now and give this exercise a shot. Otherwise, I'll go over a solution right away. So here we go. Here's how we're gonna solve this. To solve this, the first thing I recommend you do is take a look at the output without any kind of prefilling or stop sequences or anything like that. So if we take a look at what we have right here, we'll notice that each of our three commands are wrapped in a series of three back ticks. So a good place to get started would probably be to put in a prefilled assessment message of three back ticks to kind of tell a plot, just go right into the command writing right away and skip any initial commentary. And then we might also decide to put in a stop sequence of three back ticks as well. Let's see how far that gets us. So I'll put in a add assistant message and I'll start everything off with three back ticks and I'll put in a stop sequences of closing three back ticks. Let's run this and see how far it gets us. My initial output looks kind of reasonable but it's not perfect just yet. I do get three commands. There's one, two, and three. But you'll notice that I also get the word bash added at the very start. So where's that word coming from exactly? Well, let me show you what plot is really trying to do here. We provided the initial assistant message of those three back ticks. Whenever you put down three back ticks, it's kind of indicating that you are writing out some markdown. And when you are writing a markdown code block with back ticks, you can optionally put in a language identifier right here. If you choose to put one in, that whenever you render this as markdown, the content inside of those back ticks, we rendered using that languages syntax highlighting. So in this case, plot decided to put in bash right here just to say, hey, we should use bash styles syntax highlighting when we render this stuff out. Now for us, we don't want that at all. So one way we could address this would be to adjust our pre-filled message right here and just include bash ourselves. So that's now gonna make it super clear to plot itself that yes, you are inside of a markdown code block and inside this code block, you should be writing out bash formatted commands. So let me try running this again and see how I do now. Okay, so that looks better. Now I will tell you that from this point, there are probably two additional errors that you might want to address. The first is sometimes you will get back a single command, which is kind of an indication that Claude might want to write out three separate markdown code blocks. The other problem that you might run into because we are now using a bash code block, Claude might try to insert some bash formatted comments in there as well. So it might be something like this command does xyz and you might see that repeated. And so we definitely don't want those comments really just because that was one the requirements of this exercise. So to get rid of those comments and to also make sure that we get all three commands more reliably, we can use that hint I gave you. Remember the hint was message refilling isn't just limited to designating characters like backticks or stuff like that. We can also use the message brief fill to dramatically guide cloud in how it's going to answer us. So in this case, we could add in something like here are all three commands in a single block without any comments. And then I'll put in a colon right there and then a new line just so it starts all the markdown stuff on the next line down. So I'm going to try running this and we should now get some much more reliable output. Okay, that looks good. And of course I can keep running all day and we're probably going to see exactly the result we want. Okay, this looks good.

</details>

### 练习：情感分析 + 关键词提取

从非结构化文本中提取情感、关键词和评分：

```python
review = """I bought this wireless keyboard last month. The typing experience is amazing - 
the keys are quiet and responsive. Battery life is incredible, lasting over 3 months. 
However, the Bluetooth connection sometimes drops when my phone is nearby. 
The price of $79 feels fair for the build quality. Would recommend to others."""

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"""Analyze the following product review and return a JSON object with:
- sentiment: "positive", "negative", or "mixed"
- keywords: array of key topics mentioned
- rating_estimate: estimated rating out of 5
- pros: array of positive points
- cons: array of negative points

Review:
{review}

Return ONLY valid JSON."""
    }]
)
print(response.content[0].text)
```

---

## Token 计数与成本（补充知识）

### 理解 Token

- Token 是模型处理文本的基本单位
- 英文约 1 token ≈ 4 个字符（约 0.75 个单词）
- 中文约 1 token ≈ 1-2 个汉字
- 成本 = 输入 token 费用 + 输出 token 费用

### 查看 Token 使用量

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hi!"}]
)

print(f"输入 tokens: {response.usage.input_tokens}")
print(f"输出 tokens: {response.usage.output_tokens}")
print(f"总计 tokens: {response.usage.input_tokens + response.usage.output_tokens}")
```

### 使用 count_tokens 预估

```python
# 在发送请求前预估 token 数
count = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(f"预估输入 tokens: {count.input_tokens}")
```

---

## 练习题

### 练习 1：基础对话

创建一个简单的命令行聊天程序，要求：
- 支持多轮对话
- 设置一个有趣的系统提示（如"你是一位诗人"）
- 显示每轮对话的 token 使用量
- 输入 `quit` 退出

### 练习 2：参数实验

对同一个提示，分别使用 `temperature=0.0` 和 `temperature=1.0`，各运行 3 次，观察输出的差异。

### 练习 3：图片分析

找一张包含文字的图片（如菜单、海报、截图），用 Vision 功能提取其中的文字内容。

### 练习 4：模型对比

对一个复杂问题（如"解释量子纠缠"），分别用 Haiku 和 Sonnet 回答，对比：
- 回答质量
- Token 使用量
- 响应速度

---

## 常见问题

**Q: API Key 泄露了怎么办？**  
A: 立即在 Console 中删除该 Key 并创建新 Key。

**Q: 如何处理 Rate Limit？**  
A: 使用指数退避重试。SDK 内置了自动重试机制。

**Q: 多轮对话越来越慢怎么办？**  
A: 随着对话变长，每次请求的 input tokens 增加。可以定期裁剪对话历史，或使用 Prompt Caching（模块 3 讲解）。

**Q: 图片消耗多少 Token？**  
A: 取决于图片大小。大致估算：小图约 1,000 tokens，大图可达 10,000+ tokens。具体参见 [官方文档](https://docs.anthropic.com/en/docs/build-with-claude/vision)。

---

> **下一模块**：[02_提示工程与评估.md](02_提示工程与评估.md) — 学习提示工程的核心技巧和评估方法
