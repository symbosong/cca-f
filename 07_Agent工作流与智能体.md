# 模块 7：Agent 工作流与智能体

> **对应课程**：Building with the Claude API — Module 7: Agents and Workflows  
> **视频数量**：7 个（约 26 分钟）  
> **预计学习时间**：1-2 小时  
> **难度**：⭐⭐⭐

### 📌 原课程地址

| 平台 | 链接 |
|------|------|
| **Skilljar（官方）** | https://anthropic.skilljar.com/claude-with-the-anthropic-api |
| **Coursera（镜像）** | https://www.coursera.org/learn/building-with-the-claude-api |

### 📌 视频课时清单

| # | 视频标题 | 时长 | 核心知识点 |
|:-:|---------|:----:|-----------|
| 1 | AI Workflows | 4m | 工作流 vs Agent 的区别、何时选择哪种 |
| 2 | Parallelization Workflows | 4m | 并行化模式：拆分→并发→汇总 |
| 3 | Chaining Workflows | 5m | 链式模式：前一步输出→下一步输入 |
| 4 | Routing Workflows | 3m | 路由模式：先分类→再交给专业处理 |
| 5 | Agents and Tools | 5m | Agent 循环：stop_reason 驱动的核心 |
| 6 | Environment Inspection | 3m | Agent 如何感知当前环境状态 |
| 7 | Workflows vs Agents | 2m | 总结对比：简单用工作流，复杂用 Agent |

> **阅读材料**（2 篇，10 分钟）：Module Introduction / Next Steps

---

## 本模块学习目标

完成本模块后，你将能够：
1. 理解 Agent 与 Workflow 的区别
2. 掌握三种核心工作流模式：链式、路由、并行
3. 掌握两种 Agent 模式：工具循环 Agent、编排器 Agent
4. 使用 Anthropic Agent SDK 构建 Agent
5. 实现完整的 Agent Loop
6. 理解 Agent 的安全护栏和生产部署

---

## 第 1 课：AI 工作流

> 📹 视频：AI Workflows（4 min）


> 🎬 **视频 67**：Agents and workflows  
> 📁 文件：[67. Agents and workflows.mp4](videos/67.%20Agents%20and%20workflows.mp4)

## 核心内容
介绍工作流与Agent的核心概念和区别，并通过3D建模应用演示"评估器-优化器"工作流模式。

## 关键要点
- **工作流 vs Agent**：知道精确步骤→用工作流；不确定具体步骤→用Agent
- **评估器-优化器模式**：生产者生成输出 → 评分者评估 → 不满足则反馈给生产者改进 → 循环直到通过
- **实际案例**：图片→3D模型应用，Claude描述图片→CadQuery建模→渲染检查→迭代改进
- **工作流模式的价值**：这些模式已被大量工程师验证有效，值得在自己的项目中复用
- **重要认知**：识别工作流模式只是第一步，仍需编写代码实现

<details>
<summary>🇨🇳 查看中文翻译</summary>

在本模块中，我们将聚焦于工作流和Agent。让我们立即深入了解这些概念。

工作流和Agent是我们用来处理那些Claude无法在单次请求中完成的用户任务的策略。信不信由你，你在本课程中已经在创建工作流和Agent了。例如，在学习工具使用时，我们将任务输入Claude，并依赖Claude使用提供的工具来完成任务——那就是一个Agent的例子。

以下是我们在决定创建工作流还是Agent时使用的经验法则：

- **工作流**：如果我们对需要完成的任务有非常精确的了解，并且知道完成任务所需的确切步骤系列，我们就使用工作流
- **Agent**：如果我们对Claude需要解决的任务细节不太确定，我们就使用Agent

在本视频和接下来几个视频中，我们将100%聚焦于工作流。

让我们看第一个例子。假设我们正在构建一个小型Web应用程序：用户可以拖放一张金属零件的图片到屏幕上，然后我们将这张图片转换为3D模型，以STEP文件格式返回给用户（STEP文件是共享3D模型的行业标准格式）。

实现方式：
1. 将用户上传的图片发送给Claude，要求Claude详细描述这个物体
2. 将描述送回Claude，要求Claude使用Python库CadQuery来建模这个物体（CadQuery是一个用于3D实体建模的Python库，可以输出STEP文件）
3. 添加一个错误检查步骤：创建渲染图，将其反馈给Claude，询问渲染结果与原始图片的匹配程度
4. 如果Claude认为渲染存在重大问题，回到第二步让Claude重新尝试渲染
5. 重复这个过程直到得到准确的模型

重要的是，这整个流程的步骤我们可以提前想象出来，可以坐下来设计出整个过程并轻松编写代码实现。因为我们可以提前明确列出和详细说明所有这些步骤，所以我们将其称为**工作流**。

这个建模工作流是**评估器-优化器（Evaluator-Optimizer）**模式的一个例子。其思想是：
- 将输入推送到一个**生产者**（在我们的例子中，是使用CadQuery建模零件并创建渲染图的Claude）
- 输出被送入一个**评分者**，评分者查看输出并决定它是否满足某些标准
- 如果满足标准，工作流结束
- 如果不满足，反馈被送回生产者，生产者有机会改进输出
- 这个循环不断重复，直到评分者接受输出

最后需要澄清一点：识别工作流模式本身并不会自动为我们做任何事情，我们仍然需要编写实际的代码来实现它们。我们讨论工作流的原因是，许多其他工程师已经使用这些完全相同的模式实现了工作流并取得了很大成功。展示这些不同的工作流模式是为了让你在自己的项目中使用它们。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

In this module, we are going to focus on workflows and agents. Let's dive in immediately and understand what these things are. Workflows and agents are strategies that we use to handle the user tasks that can't be completed by cloud in a single request. Believe it or not, you have already been creating workflows and agents throughout this course. For example, when learning about tools, we fed tasks into Claude and relied upon Claude to figure out how to complete them using some provided tools. That was an example of an agent. Now, here's the rule of thumb that we use whenever we are trying to decide whether to create a workflow or an agent. If we have a very precise idea of the task we need to complete and we know the exact series of steps that are used to complete it, we'll use a workflow. Otherwise, if we're not really sure about the details of a task that Claude needs to solve, we'll use an agent. In this video and the next couple, we're going to be 100% focused on workflows. I'm going to show you several examples of workflows, so let's take a look at our first one right now. Let's imagine that we are building a small web application. The goal of this app is to allow a user to drag and drop an image of some metal part onto the screen. We're then going to take that image and then somehow build a 3D model out of it. We're then going to get the user back, something called a step file. Now, if you're not familiar with a step file, toy fine, step file is just an industry standard way of communicating or sharing 3D models. So essentially, we're making a 3D model out of an image. Now, even if you are not very familiar with 3D modeling, with a little bit of help and a little bit of time, I bet you could figure out a way to implement this application. Here's how we might do it. We might take the image that the user uploaded and feed into Claude and ask Claude to describe this object in great detail. Then we could take that description, feed it back into Claude separately, and ask Claude to use a Python library called CAD query to model the object. CAD query is a Python library that allows you to do 3D solid modeling, and then you can output a step file from that process. Now, it's entirely possible that Claude is not going to get this model entirely accurate the first time around. So once we build out this initial model, we might decide to add in a little air checking step, where we could create a rendering as a plain image, and then feed that image back into Claude and ask it how well this image represents the original image that the user uploaded. And if Claude decides that there are major issues in our rendering, we can then go back to the second step and ask Claude to attempt to render the part again. We can then repeat this process over and over again until hopefully we eventually end up with some kind of accurate model of the original part. Now, the important thing to understand here is that this is an entire flow of steps that we can kind of imagine ahead of time. We can sit down and design out this entire process. We could easily write out some code to implement it. As a matter of fact, I have previously implemented something almost exactly like this. Because we can explicitly list out and detail all these steps ahead of time, we would refer to this as a workflow. Remember, we define a workflow as a series of calls off to Claude meant to solve some very specific problem, where we really know exactly what those steps are supposed to be ahead of time. This modeling workflow that I've described is an example of something we call an evaluator optimizer. The idea behind this workflow is that we push some input into something called a producer. In our case, the producer is cloud using the CAD query library to model a part and then creating a rendering out of it. This output, the rendering, is fed into something called a grader. The grader will look at the output and decide if it meets some criteria. If it does, then the workflow ends. Otherwise, if the output doesn't meet some criteria, feedback is given back into the producer, which gets an opportunity to improve the output in some way. This cycle is then going to keep on repeating until eventually the grader accepts the output. Now, at this point in time, you've probably got a somewhat reasonable idea of what this evaluator optimizer thing is all about. But you're probably wondering, okay, what exactly is going on with these workflows? So there's just something I want to clarify here really quickly. Identifying workflows doesn't really inherently do anything for us. We still have to write down and write out the actual code to implement these things. The only reason that we are discussing workflows and the reason that you're going to see workflows as a popular discussion topic is that many other engineers have implemented workflows using these exact same patterns and found a lot of success. So the reason I'm showing you these different workflows is so that you can use these same patterns on your own projects. And hopefully find some success with them because they have worked well for other engineers.

</details>

### Workflow vs Agent

| | Workflow（工作流） | Agent（智能体） |
|---|---|---|
| **定义** | 预定义的固定流程 | 动态决策的自主系统 |
| **控制流** | 代码控制，可预测 | 模型控制，灵活 |
| **适用** | 流程固定、需要可靠性 | 流程不确定、需要适应性 |
| **例子** | 数据管道、审批流程 | 客服机器人、研究助手 |

> 📏 **Anthropic 的建议**：如果能用 Workflow 解决，就不要用 Agent。Workflow 更可预测、更容易调试。

### 选择决策树

```
你的任务流程是固定的吗？
├── 是 → 用 Workflow
│   ├── 步骤是串行的？ → 链式（Chaining）
│   ├── 需要根据输入分流？ → 路由（Routing）
│   └── 步骤可以并行？ → 并行化（Parallelization）
│
└── 否 → 需要根据中间结果动态决定下一步？
    ├── 单个 Agent 就够？ → 工具循环 Agent
    └── 需要多个专家协作？ → 编排器-执行器 Agent
```

---

## 第 2 课：并行化工作流

> 📹 视频：Parallelization Workflows（4 min）


> 🎬 **视频 68**：Parallelization workflows  
> 📁 文件：[68. Parallelization workflows.mp4](videos/68.%20Parallelization%20workflows.mp4)

## 核心内容
通过材料分析报告生成的案例，介绍并行化工作流模式及其优势。

## 关键要点
- **问题场景**：单个大提示让Claude同时分析所有材料→效果不佳
- **并行化工作流**：将任务分解为多个并行子任务，每个子任务专注一种材料分析
- **三步流程**：分解任务 → 并行执行子任务 → 聚合器汇总结果
- **三大优势**：
  1. Claude一次专注一个任务，避免注意力分散
  2. 可独立改进和评估每个子任务的提示
  3. 良好的可扩展性，可随时添加新子任务

<details>
<summary>🇨🇳 查看中文翻译</summary>

让我们来看另一个工作流。这次我们稍微改变一下应用程序。我们仍然让用户拖放一张零件图片到屏幕上，但这次我们将返回给用户一份分析报告，告诉用户根据各种标准制造零件的最佳材料。

要实现这个功能，我们可以将用户提供的图片和简短提示一起发送给Claude，询问用金属、聚合物、陶瓷等哪种材料制造最好。这可能有效，但我们真的在这个简单提示中要求Claude做太多了——我们没有告诉Claude在决定使用哪种材料时应考虑的实际因素。

一个自然的改进是回到这个提示中添加更多细节，可能最终得到一个非常大的提示——列出使用金属的标准、使用聚合物的标准、陶瓷、复合材料、弹性体、木材等等。这样一个庞大的提示可能会让Claude感到困惑，因为它必须在一个步骤中完成大量分析和工作。

**更好的方法——并行化工作流：**

当用户提交图片时，我们可以并行地向Claude发出多个不同的请求。每个独立的请求都包含一个专门的提示，询问Claude使用某一种特定材料（金属/聚合物/陶瓷/复合材料等）制造该零件的适用性。

通过这种方式，我们可以为每种材料定制专门的提示，Claude也不需要同时考虑所有不同的材料——它一次只关注一种材料。

当我们得到各个分析结果后，将所有结果反馈给Claude的一个后续请求，要求Claude综合考虑各项分析结果，做出最终材料推荐。现在Claude不需要预先比较所有材料，只需关注看起来最有前景的分析结果。

**这就是并行化工作流的例子。** 其核心思想是：
1. 将一个任务分解为多个子任务
2. 各子任务可以并行运行（同时执行）
3. 将所有子任务的结果合并到最终的**聚合器**步骤中

**并行化工作流的好处：**
- 允许Claude一次专注于一个任务，避免在单个大提示中被不同信息分散注意力
- 可以轻松地改进和评估每个子任务中使用的提示
- 具有良好的可扩展性——可以在任何时候添加额外的子任务，而不影响其他正在执行的子任务

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Let's take a look at another workflow. We're going to change up our application a little bit this time around. We're still going to ask the user to drag and drop an image of a part onto the screen, but this time we're going to give the user back in analysis, a report that's going to tell the user the best material to build their part out of, depending upon some various criteria. To implement this feature, we might take the users supplied image and send it off to Clawed along with a short prompt. In the prompt, we might ask Clawed to decide whether it would be best to make this part out of metal, polymer, ceramic, and so on. Now, this would probably work, but we are really asking a lot out of Clawed in this very simple prompt. For example, we haven't really told Clawed any of the real considerations that it should take into account when deciding which material to use. So even though this might work, we might not get the best results. So a natural improvement here would be probably to go back to this prompt and add in a lot more detail. Maybe it tell Clawed some of the different scenarios in which it should recommend metal or polymer and so on. So we might end up with a really, really large prompt like this. We might give some criteria for deciding when to use metal and then some criteria for deciding when to use polymer and then repeat with ceramic, composite, last mirror, wood, and so on. We would end up with a really, really large prompt that might end up being a little bit confusing to Clawed because it has to do a lot of analysis and a lot of work inside of one single step. So this might not lead to the best results. Let me show you a better way to approach implementing this feature. We could decide to make a series of different requests in parallel off to Clawed whenever a user initially submits an image. Each individual request could then include a specialized prompt asking Clawed if making this given part would be a good idea using metal or polymer or ceramic or composite and so on. So in each separate request, we are asking Clawed for the suitability of building this part in one individual material. With this approach, we could specialize each individual prompt for the given material. And now Clawed doesn't have to worry about all these different materials. It's really just focused on one individual material at a time. Now, when we eventually get some responses back from Clawed, I'm going to change the structure of this diagram just a little bit so I can fit everything on one screen. So we're going to get back these individual analysis results from Clawed. Each one is going to tell us the suitability of building out the given part in say metal, polymer, ceramic, composite, and so on. We can then take each of these analysis results and then feed them back into Clawed in a followed request and ask Clawed to consider each of the different analysis results and decide upon a final material to use. Now Clawed doesn't really have to worry about comparing all these different materials up front. Instead, it can just take a look at the analysis results that seem to be the most promising. This is an example of a parallelization workflow. The idea behind a parallelization workflow is that we're going to take one task and break it up into multiple different subtasks. Each of these subtasks can be ran in parallel, so at the same time. We will then take the results from all those different subtasks and then join them all together in a final aggregator step. In our case, the aggregator was this final step with Clawed right here. So we fed the results of each parallel task into the aggregator and Clawed gave us this final recommendation. There are several benefits to this workflow. First, it allows Clawed to focus on one task at a time. So remember just a moment ago, when I told you that we could feed the original image part into Clawed with a really large prompt that listed out some criteria for many different material types. In this scenario, Clawed might get a little bit confused or distracted as it tried to consider all the different pros and cons of each material simultaneously. The second benefit is that we can very easily improve and evaluate the prompts that are being used inside of each subtask. Finally, this flow can generally scale very well. We can add in additional subtasks at any point if we want to without really subtracting from the other subtasks that are being executed.

</details>

### 多个独立任务同时执行，然后汇总

```
          ┌→ [安全审查] ──┐
输入 ──→  ├→ [性能分析] ──┤→ [汇总报告]
          └→ [代码风格] ──┘
```

```python
import asyncio
import anthropic

async def parallel_workflow(code_to_review):
    """并行工作流：多维度代码审查"""
    async_client = anthropic.AsyncAnthropic()
    
    tasks = {
        "security": {"system": "You are a security expert.", "prompt": f"Review for security:\n\n{code_to_review}"},
        "performance": {"system": "You are a performance engineer.", "prompt": f"Review for performance:\n\n{code_to_review}"},
        "style": {"system": "You are a code quality expert.", "prompt": f"Review for readability:\n\n{code_to_review}"},
    }
    
    async def run_review(name, task):
        response = await async_client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=1024,
            system=task["system"],
            messages=[{"role": "user", "content": task["prompt"]}]
        )
        return name, response.content[0].text
    
    results = await asyncio.gather(*[run_review(n, t) for n, t in tasks.items()])
    reviews = {name: text for name, text in results}
    
    # 汇总
    combined = "\n\n".join([f"=== {n.upper()} ===\n{t}" for n, t in reviews.items()])
    summary = await async_client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1024,
        system="Summarize code review findings into a prioritized action plan.",
        messages=[{"role": "user", "content": combined}]
    )
    return {"reviews": reviews, "summary": summary.content[0].text}
```

**适用场景**：多维度分析、多模型投票、数据并行采集。

---

## 第 3 课：链式工作流

> 📹 视频：Chaining Workflows（5 min）


> 🎬 **视频 69**：Chaining workflows  
> 📁 文件：[69. Chaining workflows.mp4](videos/69.%20Chaining%20workflows.mp4)

## 核心内容
介绍链式工作流模式，特别强调其在解决Claude不遵循大型提示中约束条件这一常见问题时的重要作用。

## 关键要点
- **链式工作流**：将一个大任务分解为多个步骤，每步让Claude专注单一任务
- **社交媒体案例**：搜索热门话题 → 选择话题 → 研究 → 编写脚本 → 生成视频 → 发布
- **重要应用**：解决Claude在大型提示中不遵循约束的问题
- **解决方案**：先用完整提示生成初始结果，再用后续请求专门修正不符合要求的部分
- **核心原则**：每次调用让Claude只聚焦一个特定任务，显著提高输出质量

<details>
<summary>🇨🇳 查看中文翻译</summary>

接下来要看的工作流可能看起来有点简单和明显，但请相信我，它实际上是最有用的工作流之一，特别是在一种你会经常遇到的特定情况下。

让我们再次改变一下应用场景。假设我们正在构建一个社交媒体营销工具。用户输入他们社交媒体账号的主题——也就是账号的关注重点。然后我们的应用目标是为他们的账号生成并发布视频。

**实现方式：**
我们不需要一个带有大量复杂工具的Agent。我们可以构建一个工作流，按照预定义的步骤逐一执行：
1. 获取用户输入的主题，搜索Twitter上的热门话题
2. 将话题列表提供给Claude，让Claude选择最有趣的话题
3. 向Claude发送后续请求，要求对该话题进行网络研究
4. 研究完成后，让Claude为短视频编写脚本
5. 使用AI头像和语音合成程序创建实际视频
6. 将视频发布到社交媒体

**这是链式工作流的例子。** 在链式工作流中，我们将一个大任务分解为一系列不同的步骤，每个步骤让Claude专注于单一任务。

我们本可以在一次调用中让Claude完成所有这些——选择最有趣的话题、研究话题、编写脚本。但通过分解为三个独立的调用，Claude可以一次只专注一个任务。

**这个工作流的重要应用场景——处理大型提示中Claude不遵循约束的问题：**

想象你在使用Claude写一篇文章。你可能先发送一个简单提示，但发现Claude的输出有问题：
- Claude可能提到自己是AI在撰写文章
- 可能过度使用表情符号
- 可能使用陈词滥调的语言

于是你开始在提示中添加一长串"不要做"的列表。但无论你重复多少次这些约束，Claude有时仍然会违反它们。

**解决方案——简单的提示链：**
1. 先用完整的长提示（包含所有约束）发送请求，接受你会得到一个不完全符合要求的初始文章
2. 然后发送后续请求给Claude，提供刚生成的文章，并要求Claude：
   - 找到作者以AI身份自称的地方并删除
   - 找到并删除所有表情符号
   - 以专业技术写作者的风格重写文本

通过这种链式工作流，将任务分解为多个步骤，Claude可以更好地聚焦于每个单独的任务。即使它在原始长提示中未能满足所有要求，后续提示让Claude能够专注于你真正关心的限制条件。

因此，尽管提示链看起来简单明显，但它确实是你会经常使用的方法——每当你给Claude的任务有很多约束，而Claude似乎并不总是遵循这些约束时。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

The next workflow that we're going to take a look at is going to seem a little bit obvious and simple, but trust me, this actually ends up being one of the most useful workflows around, specifically in one particular situation that you're going to run into very often. So let's get to it. Let's change up our application a little bit once again. We'll imagine that we are building a social media marketing tool. Users will be asked to enter a topic for when their social media accounts, kind of what the focus of their account is. Then the goal of our application is to generate and post some videos to their account. So here's how we might actually implement this. We don't really need a fancy agent with a ton of fancy tools to implement this. We can build out a workflow that will just go through a series of predefined steps one by one. So in step one, we might take whatever topic the user entered into that form and do a search for trending topics on Twitter. We could then take the list of topics and feed them all into Claude and ask Claude to select the most interesting topic. But then we could do a followed request to Claude asking it to do some web research on the topic. Then once the research is complete, we could ask Claude to write a script for a short format video. Once we have the script, we could then use an AI avatar and some text to speech program to create an actual video and finally post that video off to social media. This is an example of a chaining workflow. In a chaining workflow, we take one large task, which was initially to generate some videos and post them to social media and we break it up into a series of distinct steps. In our case, the subtasks were the individual calls that we sent off to Claude. We could have attempted to accomplish all three of these tasks inside of a single call off to Claude. So we could have just fed in a list of topics to Claude, asked it to select the most interesting topic and research the topic and write a script inside of a single prompt. But by breaking this up into three separate calls, we allow Claude to focus on just one individual task at a time. Now, like I said, this probably seems like a kind of simple and obvious workflow, maybe not even worth discussing because it might be something you've already implemented in the past. But there's one very particular reason that I point out this workflow in particular because it actually ends up being on the most important workflow to understand to get quality outputs out of Claude consistently when using rather large prompts. So let me walk you through a little scenario. You might not have encountered this before, but I can almost guarantee you that you will at some point in time. Let's imagine that you are making use of Claude to write a article on some given topic. You might initially just send in a very simple prompt to Claude and ask it to write an article, and then you might get back some results. And although it might be OK, there might be some aspects to it that you don't like. So you might initially find that Claude might be mentioning the fact that it is an AI authoring the article, which you probably don't want. It might make excessive use of emojis, which you might not want. And it might use a little bit cliched language all over the place, which, again, you might not want. And so over time, as you start to develop this prompt, you might eventually set up a big long list of things that you tell a Claude to just not do it all. But inevitably, Claude might eventually, no matter how many times you repeat these items, Claude might give you back a response that seems to somehow always use emojis, mention the fact that it has been written by an AI, and just generally have kind of a cringey, non-professional tone to it. And Claude might persist in writing an article like this, no matter how many times you repeat these constraints or things that Claude should not do. So to address this problem, you can use a very simple prompt-chaining workflow. Here's what you might do. You might feed in that initial long prompt that has all these constraints in it, and then just accept that you are going to get back some initial article that doesn't really fit the bill of what you're looking for. Claude might inevitably decide to violate some of the different constraints you laid out. To fix those issues, you could then make a follow-up request back to Claude, providing the article that Claude just wrote. And underneath the article, you could ask Claude to rewrite the article in some particular way. So you could say, find any location where the author identifies as an AI and remove that mention, find and remove all emojis, and then write the text in a way that a professional technical writer would do it. By using this chaining workflow and breaking the task up into multiple steps, you allow Claude to focus much more on each individual task presented to it. So even though it might not really satisfy all the requirements you put into the long prompt originally, the follow-up prompt allows Claude to focus on just the restrictions that you really care about. And it will hopefully rewrite the article in a style that you are really looking for. So once again, even though prompt chaining seems like something kind of obvious and simple, this does end up being something that you're going to use rather often, anytime that you have a task for a cloud with many constraints, and Claude doesn't seem to be always following those constraints as much as you might expect.

</details>

### 前一步的输出作为后一步的输入

```
输入 → [步骤1: 分析需求] → [步骤2: 生成代码] → [步骤3: 代码审查] → 输出
```

```python
def chain_workflow(user_request):
    """链式工作流：需求分析 → 代码生成 → 代码审查"""
    
    analysis = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1024,
        system="You are a software architect. Create a technical spec.",
        messages=[{"role": "user", "content": f"Analyze: {user_request}"}]
    ).content[0].text
    
    code = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096,
        system="You are an expert Python developer.",
        messages=[{"role": "user", "content": f"Implement based on this spec:\n\n{analysis}"}]
    ).content[0].text
    
    review = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1024,
        system="You are a code reviewer.",
        messages=[{"role": "user", "content": f"Review this code:\n\n{code}"}]
    ).content[0].text
    
    return {"analysis": analysis, "code": code, "review": review}
```

**适用场景**：数据管道、文档生成（大纲→初稿→编辑）、多阶段翻译。

---

## 第 4 课：路由工作流

> 📹 视频：Routing Workflows（3 min）


> 🎬 **视频 70**：Routing workflows  
> 📁 文件：[70. Routing workflows.mp4](videos/70.%20Routing%20workflows.mp4)

## 核心内容
通过社交媒体视频脚本生成案例，介绍路由工作流模式——根据输入类型选择不同处理管道。

## 关键要点
- **问题背景**：不同主题（如编程vs冲浪）需要截然不同的视频脚本风格
- **路由工作流三步**：
  1. 路由步骤：让Claude对用户输入进行分类（教育/娱乐/喜剧等）
  2. 根据分类结果选择对应的专门处理管道
  3. 使用针对性的提示生成最终输出
- **核心价值**：不同类型输入获得专业化处理，而非用通用提示应对所有情况
- **可扩展性**：每个路由选项可以有独立的工作流、提示和工具集

<details>
<summary>🇨🇳 查看中文翻译</summary>

下一个工作流将向我们展示一种改进社交媒体营销工具的方法。我们仍然假设用户输入一个主题，然后我们生成视频并发布到用户的社交媒体账号。

现在，我想让你思考一下脚本生成过程中的一个问题——具体来说是视频中使用的语气和语言。

对于两个不同的主题，比如左边的"编程"和右边的"冲浪"，我们期望得到性质非常不同的视频脚本：
- **编程**：需要大量信息、仔细解释定义，整体上是教育性质的视频
- **冲浪**：可能需要一个不那么教育性的脚本，不需要长篇大论解释什么是冲浪

**路由工作流的实现方式：**

首先，我们坐下来思考用户可能要求我们创建的所有不同视频类型。我们可能决定用户给我们的主题会归入以下六种类型之一：娱乐、教育、喜剧等等。

然后为每种类型编写专门的脚本生成提示：
- **教育类**：要求Claude编写清晰、引人入胜的脚本，包含有趣的例子和引发思考的问题
- **娱乐类**：要求Claude使用流行语言和吸引人的钩子等

**完整流程：**
1. 先向Claude发送一个请求，只包含用户输入的主题（如"Python函数"），要求Claude将其归类到我们预定义的类别中
2. Claude可能将"Python函数"归类为"教育类"
3. 然后我们根据分类结果，使用对应的专门提示向Claude发送后续请求，要求编写具有相应特质和语气的脚本

**这就是路由工作流。** 在路由工作流中：
1. 将用户的原始输入送入**路由步骤**（通常是调用Claude来对输入进行分类）
2. 根据Claude的回答，将用户的输入转发到某个**特定的后续处理管道**
3. 每个路由选项可能有不同的工作流、定制化的提示或专门的工具集

路由工作流的核心价值在于：不同类型的输入可以获得针对性的专业处理，而不是用一个通用提示试图应对所有情况。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Our next workflow is going to show us one way of improving this social media marketing tool. So once again, we'll imagine that a user is going to enter in a topic, we're then going to produce some videos somehow, and post them to a user's social media account. Now, there's something I really want you to think about about the script generation process. In other words, the actual tone and language used in these different videos. Given two different topics, such as programming on the left hand side, and maybe surfing on the right hand side, we would really expect to get video scripts that are very, very different in nature. So on the left hand side with programming, we would want to get a lot of information, carefully explain definitions, and probably just overall a video that is meant to be educational in nature. And if user entered in surfing as a topic, we would probably want to get back a very different video script, probably something that is much less educational in nature and doesn't have a long definition on what surfing is or anything like that. So let me show you a workflow that we could use to make sure that a given topic will result in a video script that fits the nature of that topic really well. First, we would sit down and think about all the different possible genres of videos that users might ask us to create. So we might decide that the topics that users are going to give to us are going to fit into one of six different genres, entertainment, educational, comedy, and so on. So in our example, back over here, programming might be educational and surfing might be entertainment. Then for each of these different genres, we might write out a script generation prompt. So if someone asked for a topic that we categorize as being educational in nature, we would ask Claw to write a script using this prompt right here. And the prompt is asking Claw to make a clear, engaging script that has some interesting examples and interesting questions and so on. If a user gives us a topic of surfing, we might categorize that as being entertainment. So then we would take this prompt right here, put in the topic as surfing and feed the whole prompt into Claw and ask Claw to write a script about surfing that maybe has some trendy language and engaging hooks and so on. So let me show you what this entire flow would look like in practice. We would initially send request off to Claw that contained just the topic the user had entered, maybe something like Python functions and ask Claw to categorize this topic into one of our different categories that we just came up with. In this scenario, Python functions might be most closely related to the category of educational. So then we would take this response from Claw and then make a follow up request asking Claw to write a script that has some clear, engaging information about Python functions that has thought provoking examples. And then presumably, we would get back some script with those different qualities and a tone appropriate for an educational video. This is an example of a routing workflow. In a routing workflow, we're going to take the user's original inputs and feed it into a routing step. This routing step will probably be a call to Claw itself asking Claw to categorize the user input or task in some way. Then depending upon Claw's answer, we're going to forward the user's input onto some very particular follow up processing pipeline. So maybe this one right here or this one right here or this one right here and so on. But probably only one of these different three. Each of these different routing options might have a different workflow implemented inside of it or a customized prompt or a customized set of tools that are specialized for handling the exact task that the user is asking for.

</details>

### 先分类，再交给专业处理

```
输入 → [分类器] → 技术问题 → [技术专家 Prompt]
                 → 账单问题 → [账单专家 Prompt]
                 → 一般咨询 → [通用助手 Prompt]
```

```python
def routing_workflow(user_message):
    """路由工作流：智能客服路由"""
    
    # 用 Haiku 做分类（快且便宜）
    category = client.messages.create(
        model="claude-haiku-4-20250514", max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"Classify as technical/billing/general:\n\n{user_message}\n\nRespond with one word."
        }]
    ).content[0].text.strip().lower()
    
    expert_prompts = {
        "technical": "You are a senior technical support engineer...",
        "billing": "You are a billing specialist...",
        "general": "You are a friendly customer service rep..."
    }
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=2048,
        system=expert_prompts.get(category, expert_prompts["general"]),
        messages=[{"role": "user", "content": user_message}]
    ).content[0].text
    
    return {"category": category, "response": response}
```

**适用场景**：多语言处理、客服系统、内容审核。

---

## 第 5 课：Agent 与工具循环

> 📹 视频：Agents and Tools（5 min）


> 🎬 **视频 71**：Agents and tools  
> 📁 文件：[71. Agents and tools.mp4](videos/71.%20Agents%20and%20tools.mp4)

## 核心内容
深入讲解Agent如何通过组合抽象工具来灵活完成各种任务，以及工具设计的关键原则。

## 关键要点
- **Agent核心能力**：以不同组合方式使用工具，灵活应对各种任务
- **工具组合示例**：3个简单工具（获取时间/添加时长/设置提醒）可以组合解决多种场景
- **工具设计原则——保持抽象**：
  - 提供通用、非超级专业化的工具（如bash、web fetch、write）
  - 不需要提供"重构"或"安装依赖"等超级专业化工具
  - 让Claude自行组合基础工具来完成复杂任务
- **Claude Code作为范例**：只有少量抽象工具，却能完成各种复杂编程任务
- **灵活的用户交互**：Agent可以与用户进行动态多轮交互，而非简单的输入→输出

<details>
<summary>🇨🇳 查看中文翻译</summary>

现在我们已经看了几种不同的工作流，接下来要转向讨论Agent。

理解Agent最简单的方式是回想工作流——具体来说是什么时候使用它们。工作流在我们知道完成给定任务所需的精确步骤系列时最有效。而Agent则在我们不确切知道需要什么步骤时更有效。

在Agent场景中，我们给Claude一个任务和一组工具，然后依赖Claude创建一个计划，使用给定的工具来完成任务。Agent的灵活性使其在构建时非常有吸引力——你可以创建一个Agent，确保它工作良好，然后这个Agent可以解决各种不同的任务。但这种方法也有一些主要缺点，我们稍后会讨论。

**Agent的关键方面是它们以不同组合使用工具的能力。**

回想课程早期的工具示例——我们创建了三个工具：获取当前日期时间、为日期时间添加时长、设置提醒。每个工具都相当简单，但Claude能够以不同且令人惊讶的方式组合它们来完成各种任务：

- "现在几点？" → 直接调用获取当前日期时间
- "11天后是星期几？" → 先获取当前日期时间，然后添加时长
- "下周三设个去健身房的提醒" → 获取当前日期 → 添加时长 → 设置提醒
- "我的90天保修什么时候到期？" → Claude会先询问用户保修开始日期，然后再计算

**关于Agent工具的重要经验——工具应该是合理抽象的。**

看看Claude Code提供的工具就是很好的例子。Claude Code只获得一小组抽象工具：
- **左侧（Claude Code拥有的）**：bash（运行命令）、web fetch（获取URL）、write（创建文件）等——这些是通用的、非超级专业化的工具
- **右侧（Claude Code没有的）**：没有"重构"工具、没有"安装依赖"工具——相反，Claude Code需要自己弄清楚如何使用左侧的工具来完成这些任务

**核心教训：** 当我们创建Agent时，要确保提供合理抽象的工具，让Claude能够想出如何将它们拼接在一起以实现某个目标。

以社交媒体视频创建Agent为例，我们可能提供：
- **bash**：访问FFmpeg（用于生成视频的CLI工具）
- **generate_image**：生成图片
- **text_to_speech**：文本转语音
- **post_media**：将内容发布到社交媒体

Claude可以用这组工具以意想不到的方式工作：
- **场景一**：用户要求创建并发布Python编程视频 → Claude直接完成全流程
- **场景二**：用户先要求生成一个示例封面图 → Claude先生成图片 → 展示给用户 → 获得用户认可 → 再进入视频生成流程

这种灵活的交互方式就是Agent的强大之处。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Now that we have taken a look at several different workflows, we are going to pivot and start to discuss agents. Understanding agents is easiest if you think back to workflows, specifically when we would actually use them. Workflows were most effective when we knew the precise series of steps required to complete a given task. Agents, on the other hand, are more effective when we don't really know exactly what steps are required. So in these scenarios, we give Claude a task and a set of tools. And then we rely upon Claude to create a plan to complete the task using the given tools. This flexibility around agents is what makes them really attractive for building. The thought process is that you can make an agent, make sure it works reasonably well, and then the agent can solve a wide variety of different tasks. However, there are some major drawbacks to this approach, which we will discuss in a little bit. A key aspect of agents is their ability to make use of tools in different combinations. So to help you understand this, I want to think back to an earlier example that we went through earlier on inside this course, where we put together three different tools. We created tools like Git Current Date Time, Adoration to Date Time, and Set Reminder. Each of these tools were rather simple in nature, but Claude was able to combine them in different, kind of surprising ways to achieve a wide variety of different tasks that we might not really have planned out ahead of time. Let me show you some examples. So on the left hand side of this diagram, I've got some example tasks that we could feed into Claude along with those three different tools. And then on the right hand portion is a series of different tool calls that Claude might make to complete the given task. So for example, if we ask Claude what's the given time, easy enough, Claude can just call the Git Current Date Time tool by itself and answer the question. If we ask Claude what day of the week is in 11 days, it could first call Git Current Date Time and then add duration to date time. If we ask Claude to say, Set a reminder to go to the gym next Wednesday, Claude could first figure out the current date of the week, add a duration onto it, and then Set a reminder for that particular day. Finally, Claude can also figure out when it needs some extra information in order to successfully call a tool. So if a user asked, when does my 90 day warranty expire? Well, there's really no guarantee that the user got the warranty today. So Claude might first ask the user for a bit of extra information, particularly when they actually obtain the warranty. The once user gives them that information, then Claude can call Add duration to date time and figure out when the warranty will expire. These are all examples of ways in which Claude can take a set of tools and combine them together in an interesting fashion in order to solve a given task. And this is going to lead us into our first big lesson or understanding around agents. And that is that the set of tools that we provide to an agent need to be a reasonably abstract. And a great example of this and to help you understand what I really mean hereby abstract is to go back and look at Claude code and specifically some of the tools that are provided to it. Claude gets access to a very small set of abstract tools. And when I say abstract, I mean generic or general or kind of vague in purpose, they are not hyper specialized in any way. So Claude code gets access to tools like bash in order to run commands web fetch to fetch URL right to create a file and so on. And Claude code can figure out how to modify and add features to an existing code base in really amazing ways by combining together these different tools. Claude code does not have access to hyper specialized tools that just fulfill one very specific task in one specific scenario. So for example, on the right hand side of this diagram, these are all tools that Claude code notably does not have. So there is no refactor tool that will just magically refactor a file. Instead, Claude code should figure out how to make use of the tools on the left inside in order to refactor something. Likewise, there is no install dependencies tool. Instead, Claude code needs to read files to understand the project configuration and then run the bash tool to run the appropriate command to install the dependencies. The lesson that we can take from this is that whenever we create an agent, we want to make sure that we provide reasonably abstract tools that Claude can somehow figure out how to piece together in order to achieve some goal. So for example, if we go back to our example of building some kind of social media video creation agent, we might provide it for different tools. One might be bash, which would give it access to FF impact. That's a commonly used CLI tool that you can use to generate videos, given some input images or videos or text or audio and so on. We might also give it a generate image tool, a text to speech tool, just to augment the video generation process, and then finally a post media tool so that it can take the generate content, whatever it made and post that content to a social media account. Claude can use that set of tools in rather unexpected ways. So for example, it would enable a flow like what you see on the left-hand side where a user might chat with our agent and ask it to create and post a video on Python programming. But this set of tools might also allow for more dynamic interactions with the user. For example, on the right-hand side, a user might ask for a video, but first ask the agent to generate a sample cover image to use in the video. Then our agent could first generate an image, show it to the user, get the user's approval, and then go into the video generation process.

</details>

### Agent 循环：stop_reason 驱动的核心模式

这是所有 Agent 的核心——循环执行工具调用直到 Claude 给出最终回答：

```python
import json

def agent_loop(user_message, tools, process_tool_fn, max_turns=20):
    """通用 Agent Loop"""
    messages = [{"role": "user", "content": user_message}]
    system = "You are a helpful assistant with access to tools."
    
    for turn in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=4096,
            system=system, tools=tools, messages=messages
        )
        
        if response.stop_reason == "end_turn":
            return "".join(b.text for b in response.content if hasattr(b, "text"))
        
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  🔧 {block.name}({json.dumps(block.input, ensure_ascii=False)})")
                    try:
                        result = process_tool_fn(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result", "tool_use_id": block.id,
                            "content": json.dumps(result) if not isinstance(result, str) else result,
                        })
                    except Exception as e:
                        tool_results.append({
                            "type": "tool_result", "tool_use_id": block.id,
                            "content": f"Error: {str(e)}", "is_error": True,
                        })
            messages.append({"role": "user", "content": tool_results})
    
    return "⚠️ 达到最大轮次限制"
```

---

## 第 6 课：环境审查

> 📹 视频：Environment Inspection（3 min）


> 🎬 **视频 72**：Environment inspection  
> 📁 文件：[72. Environment inspection.mp4](videos/72.%20Environment%20inspection.mp4)

## 核心内容
讲解Agent的环境检查能力——Agent需要在采取行动后评估结果，以理解当前状态和进度。

## 关键要点
- **核心原则**：Agent在采取行动后（有时之前）需要评估操作结果，不仅仅依赖工具返回值
- **Computer Use示例**：每次操作后都需要截图来理解新状态
- **Claude Code示例**："写入前先读取"——修改文件前需要先了解文件当前内容
- **实际应用**（社交媒体视频Agent）：
  - 使用WhisperCPP生成字幕文件检查对话时间戳
  - 使用FFmpeg提取视频截图检查视觉效果
- **价值**：帮助Agent更好地评估任务完成进度，处理意外结果和错误

<details>
<summary>🇨🇳 查看中文翻译</summary>

接下来要讨论的Agent相关概念是环境检查。

当我们之前看Computer Use时，你可能注意到一个有趣的现象：在每一个我们看到的操作（如打字或移动鼠标）之后，都会立即出现一张截图。

从Claude的角度来看Computer Use：Claude尝试打字或点击某处，页面可能会发生变化，但Claude并不真正理解会如何变化。点击一个按钮可能导航到新页面，也可能打开一个菜单。为了理解它所采取的任何操作的结果，Claude需要一张截图来理解它所处的新状态或环境。

**同样的思想适用于我们组装的任何Agent。** 在采取行动之后（有时在采取行动之前），Claude确实需要一种方式来评估操作的结果，通常不仅仅是工具返回的内容。通过帮助Claude理解其环境，它可以更好地评估完成任务的进度，并更好地处理意外结果或错误。

**Claude Code中的类似例子：**
当我要求Claude更新main.py文件时，在修改文件之前，Claude需要先了解文件中的当前代码。这看起来显而易见，但我鼓励你在构建自己的Agent时思考这个"写入前先读取"的理念。

**应用到社交媒体视频Agent：**

当我们向Claude发送请求时，可能会在系统提示中提供特殊指令，帮助Claude了解如何在生成视频后检查其环境：

1. **使用WhisperCPP生成字幕文件**：如果我依赖Claude使用FFmpeg生成视频，我预期它有时会在对话放置时间上犯错。我可能会指示Claude使用bash工具运行WhisperCPP程序——这是一个可以自动从视频生成字幕文件的程序，字幕文件包含时间戳，Claude可以用它来确保对话放置正确。

2. **使用FFmpeg提取截图**：我们可能告诉Claude使用bash工具运行FFmpeg从视频的每秒或每10秒提取一张截图，并查看这些截图以确保视频看起来符合预期。

这允许Claude检查其操作的结果——即创建的实际视频——并确保它按预期完成任务。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

The next idea around agents that we are going to discuss is environment inspection. When we were taking a look at computer use previously, you might recall something interesting. After every single action that we saw logged out on the left hand side, like typing or moving the mouse, we always seem to see a screenshot immediately after, and that's what I'm showing you in this diagram right here. Clawed attempted to type out some text, and we see that logged in the first panel up here, and then right after it we saw a screenshot appear immediately. I'd like you to look at computer use from Clawed's perspective. Clawed attempts to type or click somewhere and presumably the page is going to change, but Clawed doesn't really understand how. Clicking on a button might navigate to a new page, or it might open up a menu. In order to understand the result of any action it took, Clawed needed a screenshot to understand the new state or the environment that it was in. This same idea holds for any agent that we assemble. After taking in action, and sometimes before taking in action, Clawed really needs a way of evaluating the result of the action, often beyond whatever just a tool returns. By helping Clawed understand its environment, it can better gauge its progress towards completing a task, and also better deal with unexpected results or errors. We can see a very similar idea when we make use of Clawed code. So in the screenshot at the very top, I've asked Clawed to update the main.py file. Now, the task I've given here of adding in an additional route is really simple, but before we can ever modify that file in any way, this is going to seem really obvious. Well, Clawed needs to understand what the current code is inside the file first. So Clawed needs some way of reading the contents of a file. Now again, I know it seems really obvious, but I would encourage you to think about this idea around reading a file before writing to it anytime you are building an agent of your own. This idea is even applicable to our social media video agent. So whenever we make a request off to Clawed, we might give it a task like create a video on Python and post it to my social media account, along with our list of tools. Then we might provide some special instructions inside of a system prompt, helping Clawed understand how can inspect its environment after generating a video. Personally, if I was relying upon Clawed to use FFimPig to generate a video, I would kind of expect it to maybe sometimes make mistakes around the placement of dialogue. So specifically, when audio clips would play, that it generated using some text-to-speech functionality. To help Clawed better understand its progress around completing a task when making one of these videos, I might give it some instructions to make use of the BASH tool specifically to run a program called specifically WhispersCPP. This is a program we can use to generate caption files automatically out of a video. And those caption files have timestamps inside them. So Clawed could use this program to make sure the dialogue was placed correctly. We might also advise Clawed to use the BASH tool to run FFimPig, which has the ability to extract screenshots out of a video. We might tell Clawed to extract a screenshot from every second or every 10 seconds, and take a look at the screenshots just to make sure that the video looks as it kind of expects it to look. This allows Clawed to inspect the results of its actions, the actual video I created, and make sure that it's completing the task as it should.

</details>

### Agent 如何感知当前状态

Agent 可以通过工具来"感知环境"——读取文件、查看目录结构、获取系统信息。这些读取类工具让 Agent 在采取行动前先理解当前状态。

---

## 第 7 课：工作流 vs Agent 总结

> 📹 视频：Workflows vs Agents（2 min）


> 🎬 **视频 73**：Workflows vs agents  
> 📁 文件：[73. Workflows vs agents.mp4](videos/73.%20Workflows%20vs%20agents.mp4)

## 核心内容
系统对比工作流与Agent的优缺点，给出实际项目中的选择建议。

## 关键要点
- **工作流优势**：更高的任务完成准确率、更容易测试和评估、让Claude专注单一任务
- **Agent优势**：更灵活、可创造性解决问题、支持动态用户交互
- **Agent劣势**：任务成功率较低、更难测试和评估
- **核心建议**：优先实现工作流，只在真正需要时才使用Agent
- **关键认知**：用户想要的是可靠工作的产品，而非花哨的Agent

<details>
<summary>🇨🇳 查看中文翻译</summary>

让我们通过比较和对比工作流与Agent的不同方面来做个总结。

**工作流**是对Claude的一系列预定义调用。当我们对完成任务所需的确切步骤系列有很好的了解时，我们通常使用工作流。

**Agent**则不同——我们不确切知道会提供什么任务，所以我们提供一组扎实的基础工具，期望Claude将这些工具组合在一起来完成给定任务。

**工作流的特点：**
- 共同主题是将大任务分成更小的任务，每个小任务更加具体，让Claude一次专注一个领域
- 这种增强的专注力通常导致比Agent更高的任务完成准确率
- 因为我们知道工作流执行的确切步骤系列，所以它们更容易测试和评估

**Agent的特点：**
- 不受固定步骤的约束，Claude可以创造性地解决各种挑战
- 在用户体验上更灵活——工作流期望接收特定的输入集，而Agent可以根据用户查询自行创建输入，也可以在需要时向用户请求更多信息
- **缺点**：任务成功完成率通常低于工作流（因为我们委托了太多工作给Claude）
- 更难测试和评估（因为我们通常不清楚Agent会执行什么步骤系列）

**最终建议：**

Agent确实很有趣，但请记住，作为工程师，你的首要目标是可靠地解决问题。用户可能并不在乎你做了一个多么花哨的Agent——他们真正想要的是一个100%能工作的产品。

因此，通用建议是：**尽可能优先实现工作流，只在真正需要时才使用Agent。**

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Let's wrap up by comparing and contrasting some different aspects of workflows and agents. First, recall that workflows are a predefined series of calls to Claude. We often use workflows when we have a good idea of the exact series of steps that are needed to complete a task. With agents, on the other hand, we don't know exactly what task will be provided, so we instead provide a solid set of basic tools and expect Claude to combine these tools together to complete a given task. You might have noticed that a common theme around workflows is that we take a big task and we divide it up into much smaller tasks. Each of these smaller tasks are much more specific in nature, allowing Claude to focus on a single area at a time. This increased focus generally leads to higher accuracy for completing a task compared to agents. Because we know the exact series of steps that a workflow executes, they're also far easier to test and evaluate. With agents, we aren't constrained to a series of steps etched in stone. Instead, Claude can creatively figure out how to handle a wide variety of challenges. Along with this flexibility, we also get flexibility in the user experience. While workflows expect to receive a very particular set of inputs, agents can create their own inputs based on queries received from the user, and agents can also ask user for more input when it's needed. The downside to agents is that they generally have a lower successful task completion rate compared to workflows because we are delegating so much work to Claude. In addition, they're also harder to test and evaluate, since we often don't have a good idea of what series of steps an agent will execute to complete a given task. At the end of the day, agents are really interesting, but remember, your primary goal as an engineer is to solve problems reliably. Users probably don't care that you've made a fancy agent. They really just want a product that's went to work 100% of the time. So with this in mind, the general recommendation is to always focus on implementing workflows where possible and only resort to agents when they are truly required.

</details>

### 最终对比

| 维度 | Workflow | Agent |
|------|---------|-------|
| 可预测性 | ✅ 高 | ⚠️ 低 |
| 可调试性 | ✅ 容易 | ⚠️ 困难 |
| 灵活性 | ⚠️ 低 | ✅ 高 |
| 适用场景 | 流程固定的任务 | 复杂开放性任务 |

**核心原则**：简单任务用工作流（可预测/可调试），复杂开放任务用 Agent（灵活/自主）。

---

## 补充：编排器-执行器模式

一个"编排器" Agent 分解任务，多个"执行器" Agent 并行处理：

```python
async def orchestrator_agent(user_request):
    """编排器-执行器 Agent"""
    async_client = anthropic.AsyncAnthropic()
    
    # 编排器分解任务
    plan = await async_client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1024,
        system="Break down complex requests into independent subtasks.",
        messages=[{"role": "user", "content": f"Break into subtasks (JSON array):\n{user_request}"}]
    )
    subtasks = json.loads(plan.content[0].text)
    
    # 并行执行子任务
    async def execute(subtask):
        r = await async_client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=2048,
            system=f"You are a {subtask['role']}.",
            messages=[{"role": "user", "content": subtask["task"]}]
        )
        return subtask["id"], r.content[0].text
    
    results = await asyncio.gather(*[execute(t) for t in subtasks])
    
    # 汇总
    results_text = "\n\n".join([f"=== Subtask {id} ===\n{text}" for id, text in results])
    final = await async_client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096,
        system="Synthesize subtask results into a comprehensive response.",
        messages=[{"role": "user", "content": f"Original: {user_request}\n\nResults:\n{results_text}"}]
    )
    return final.content[0].text
```

---

## 补充：Anthropic Agent SDK

```bash
pip install anthropic-agent-sdk
```

```python
from agent_sdk import Agent, tool

agent = Agent(
    name="research-assistant",
    model="claude-sonnet-4-20250514",
    instructions="You are a research assistant.",
)

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"

agent.tools = [search_web]
# result = agent.run("Research quantum computing.")
```

---

## 补充：安全护栏

### 输入/输出过滤

```python
def input_guard(user_message):
    """检查输入是否安全"""
    response = client.messages.create(
        model="claude-haiku-4-20250514", max_tokens=50,
        messages=[{"role": "user", "content": f"Is this safe for a customer service bot?\n\n{user_message}\n\nSAFE or UNSAFE"}]
    )
    return "SAFE" in response.content[0].text.upper()
```

### 升级决策（Human-in-the-Loop）

```python
ESCALATION_TRIGGERS = ["legal action", "speak to manager", "data breach"]

def should_escalate(message):
    for trigger in ESCALATION_TRIGGERS:
        if trigger.lower() in message.lower():
            return True
    return False
```

---

## 补充：生产部署检查清单

```
✅ 架构选择
  □ Workflow 还是 Agent（优先 Workflow）
  □ 选择合适的工作流模式
  □ 确定工具集合和权限

✅ 安全
  □ 输入过滤 / 输出过滤 / 升级机制 / 工具权限最小化 / 审计日志

✅ 可靠性
  □ 错误处理 / 最大轮次限制 / 超时设置 / 降级方案

✅ 成本控制
  □ Prompt Caching / 模型选择 / 监控 token / 预算告警
```

---

## 练习题

### 练习 1：链式工作流

构建"博客生成器"：主题→大纲→初稿→编辑→摘要+SEO标题。

### 练习 2：路由 + Agent

构建智能助手，根据输入自动路由到计算器/翻译器/搜索/代码助手。

### 练习 3：安全护栏

为练习 2 添加完整的安全护栏：输入过滤+升级决策+输出检查+审计日志。

---

## 扩展阅读

| 资源 | 链接 |
|------|------|
| Anthropic Agent 文档 | https://docs.anthropic.com/en/docs/build-with-claude/agentic |
| Agent SDK | https://github.com/anthropics/agent-sdk |
| Building Effective Agents | https://www.anthropic.com/research/building-effective-agents |
| 安全护栏文档 | https://docs.anthropic.com/en/docs/build-with-claude/safety-guardrails |

---

## 🎓 课程总结


> 🎬 **视频 74**：Course Wrap Up  
> 📁 文件：[74. Course Wrap Up.mp4](videos/74.%20Course%20Wrap%20Up.mp4)

## 核心内容
课程总结与回顾，梳理全部课程要点并推荐后续学习方向。

## 关键要点
- **课程七大模块回顾**：
  1. 模型选择（Haiku快速处理 / Sonnet高智能）
  2. API访问与参数控制（温度、停止序列、预填充等）
  3. 提示评估——**最重要的实践**
  4. 提示工程（清晰直接地告诉Claude期望）
  5. 工具使用（极大扩展Claude能力）
  6. Claude Code和Computer Use
  7. 工作流和Agent
- **推荐后续研究主题**：
  - Agent编排（多Agent协作）
  - Agent性能评估和监控
  - Agentic RAG
  - RAG评估和工具评估

<details>
<summary>🇨🇳 查看中文翻译</summary>

如果你已经完成了整个课程，你付出了巨大的努力，我向你表示祝贺。在结束之前，我想快速回顾一下我们讨论的主要话题，并给你一些推荐的后续研究主题。

**课程回顾：**

1. **模型选择**：我们首先讨论了Anthropic提供的不同模型。Haiku用于快速、较小的请求，Sonnet提供更高的智能。

2. **API访问与参数控制**：我们花了大量时间讨论如何通过API访问Claude，以及可以使用的不同参数来调整响应——温度、停止序列、消息预填充等。这些参数可以引导Claude的方向、控制创造力，确保获得正确的数据格式或预期输出。

3. **提示评估（Prompt Evals）**：我怎么强调都不为过——提示评估是你在自己项目中实施的**最重要的实践**。你可能自己运行提示10次觉得一切正常，但一旦部署到生产环境，用户可能得不到你期望的结果。确保提示有效的唯一方式就是评估它们。记住，提示评估不一定很复杂——你不需要使用花哨的框架或进行复杂的设置。你可以使用Claude来生成提示评估框架。

4. **提示工程**：有一些需要记住的技巧，其中最重要的是清晰地、直接地告诉Claude你对它的期望。

5. **工具使用**：这可能是课程中比较复杂的部分之一，但非常重要，因为它极大地扩展了Claude的能力。

6. **Claude Code和Computer Use**：Anthropic直接发布的两个重要应用。希望你享受了Claude Code的实操体验。个人而言，我使用Claude Code来帮助编写代码和项目——我并不怎么使用编辑器内的花哨助手，而是在终端中运行Claude Code。

7. **工作流和Agent**：记住，Agent确实很有趣，但使用工作流通常会获得更好的结果和更高的准确性。

**推荐的后续研究主题：**

由于时间限制，我们无法在课程中涵盖所有内容。以下是一些重要的后续研究主题：
- **Agent编排**：让多个Agent协同工作
- **Agent性能评估和监控**
- **Agentic RAG**：RAG的一种变体
- **RAG评估**
- **工具评估**：类似于提示评估，确保工具描述以我们期望的方式帮助Claude

就是这些了。希望你享受了这门课程，感谢你花时间完成这些内容。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

If you have made it through this course, you have put in a tremendous amount of effort, and I congratulate you. Before we close things out, I want to very quickly recap some of the major topics we discussed and give you some recommended follow-up topics to research in the future. First, a quick recap of what we have covered. We began this course by discussing some of the different models offered by Anthropic. Remember, we have access to Hikou for fast, smaller requests and Sonnet for greater intelligence. We then spent a lot of time discussing how to access Clawed via the API and different parameters we could feed into Clawed in order to adjust its response. For example, we discussed temperature and stop sequences, message prefilling. All these are parameters we can use to direct Clawed in certain directions, control its creativity, and ensure that we get the correct format of data or output that we expect. We then spent a good amount of time talking about prompt evaluations. I cannot stress it enough. Promp-Devaluations is by far the most important practice for you to implement on your own projects. You might sit down and run a prompt 10 times on your own and think everything is okay, but as soon as you deploy it in production, your users might not get the results that you want them to get. The only way to make sure that you are writing effective prompts is by evaluating them. And remember, prompt devils, they don't have to be hard. You do not have to make use of a fancy framework or do any kind of a big complicated setup. You can use Clawed to generate a prompt evaluation framework on your own. That's kind of what you saw inside this course. The prompt deval framework that we made use of, a lot of that code was written directly by Clawed. We then spent some time discussing prompt engineering. Remember, there's a handful of techniques for you to keep in mind. Chief among them is just simply being clear and directly telling Clawed what you expect of it. After that, we spent a lot of effort on tool use, and that was probably one of the more complicated sections inside the course. This is extremely important because it dramatically expands the capabilities of Clawed. We then spent some time with two important applications that then released by Anthropic Directly, Clawed Code and Computer Use. I hope you enjoyed getting some hands-on experience with Clawed Code. Personally, it is what I use to help me author code and projects. I don't actually use a fancy in-editor assistant that much. I really just run Clawed Code at that terminal, and the exact same style that you saw in those videos. And then finally, we spent a decent amount of time discussing workflows and agents. Now remember, agents are definitely interesting. It's a very exciting topic, but you very often are going to get better results and higher accuracy by the use of workflows. For a lack of time, we were not able to cover every topic inside of this course. There are some big ticket items that I recommend you follow up and do some research on your own. Chief among them is a lot of topics around agents. I'm also trying to get agents to work together with agent orchestration, understanding how to evaluate an agent's performance and monitor it, and a variation on RAG, known as agentic RAG, are all topics that I recommend you spend some time to research on your own. I also recommend you take a look at some different techniques for RAG evaluation and tool evaluation. Tool evaluation is similar to prompt e-vals. We want to make sure that our tool descriptions are helping Clawed in the way we really expect. Well, that's it for now. Like I said, I hope you enjoyed this course and I appreciate your time in working through this content.

</details>

恭喜你完成了所有 7 个模块的学习！

| 模块 | 核心能力 |
|------|---------|
| 1. Claude 入门 | API 调用、消息格式、模型选择、参数 |
| 2. 提示工程与评估 | 提示技巧、思维链、评估管道 |
| 3. 工具使用与高级特性 | 工具调用、Agent Loop、缓存、Extended Thinking |
| 4. MCP 协议 | 标准化工具连接、MCP Server 开发 |
| 5. RAG | 检索增强生成、向量数据库、分块策略 |
| 6. Claude Code & Computer Use | AI 编程助手、桌面操控 |
| 7. Agent 工作流 | 工作流模式、Agent 架构、安全护栏 |

### 下一步

1. **动手实践**：把学到的知识应用到实际项目中
2. **深入文档**：阅读 [Anthropic 官方文档](https://docs.anthropic.com)
3. **关注生态**：关注 MCP 生态和 Agent SDK 的发展
4. **（可选）备考 CCA-F** 验证掌握程度

---

> 📖 返回 [学习大纲](00_学习大纲与资源总览.md)
