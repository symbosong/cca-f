# 模块 4：MCP 模型上下文协议

> **对应课程**：Building with the Claude API — Module 5: Model Context Protocol (MCP)  
> **视频转录**：11 个（视频 52-62，已嵌入文字）  
> **GitHub Notebook**：无（本模块以概念和动手实操为主）  
> **预计学习时间**：2 小时  
> **难度**：⭐⭐

### 📌 原课程地址

| 平台 | 链接 |
|------|------|
| **Skilljar（官方）** | https://anthropic.skilljar.com/claude-with-the-anthropic-api |
| **Coursera（镜像）** | https://www.coursera.org/learn/building-with-the-claude-api |

### 📌 视频课时清单

| # | 视频标题 | 时长 | 核心知识点 |
|:-:|---------|:----:|-----------|
| 1 | Introduction to MCP | 5m | MCP 概念、USB 类比、N×M → N+M 问题 |
| 2 | MCP Clients | 5m | 客户端概念、Claude Desktop/Code 都是 MCP 客户端 |
| 3 | Project Setup | 3m | 安装 MCP SDK、项目结构、配置文件 |
| 4 | Server Inspector | 4m | MCP Inspector 调试工具、查看暴露的工具/资源/提示 |
| 5 | Implementing a Client | 7m | 编写 MCP 客户端、发现和调用工具 |
| 6 | Defining Resources | 10m | 资源定义、为 Claude 提供上下文数据 |
| 7 | Fetching Resources | 5m | 客户端读取资源、URI 模板和参数化 |
| 8 | Defining Prompts | 8m | 预定义提示模板、@mcp.prompt() 装饰器 |
| 9 | Prompts in the Client | 3m | 客户端使用提示模板 |
| 10 | MCP Review | 4m | 全模块总结、与直接工具调用对比 |

> **阅读材料**（3 篇，25 分钟）：Module Introduction / Defining Tools with MCP / Next Steps

---

## 本模块学习目标

完成本模块后，你将能够：
1. 理解 MCP 是什么、为什么需要它
2. 掌握 MCP 的架构和核心概念
3. 了解 MCP 的三大核心能力：Tools、Resources、Prompts
4. 搭建和配置 MCP Server
5. 在 Claude Desktop 和 Claude Code 中使用 MCP
6. 理解 MCP 在 API 中的使用方式
7. 了解 MCP 生态和社区 Server

---

## 第 1 课：MCP 概览

> 📹 视频：Introduction to MCP（5 min）


> 🎬 **视频 52**：Introducing MCP  
> 📁 文件：[52. Introducing MCP.mp4](videos/52.%20Introducing%20MCP.mp4)

**核心内容**
介绍模型上下文协议（MCP）的基本概念，解释MCP如何通过服务器-客户端架构将工具的定义和执行负担从开发者转移到MCP服务器，以GitHub聊天机器人为例说明MCP的实际价值。

**关键要点**
- MCP是一个通信层，为Claude提供上下文和工具，避免开发者编写大量集成代码
- MCP架构包含两个主要元素：客户端（Client）和服务器（Server）
- MCP服务器包含三个核心组件：工具（Tools）、资源（Resources）、提示词（Prompts）
- MCP服务器可看作外部服务的接口，封装了大量功能
- 任何人都可以编写MCP服务器，服务提供商通常会发布官方实现
- MCP与直接API调用的区别：MCP免去了手动编写schema和函数的工作
- MCP和工具使用是互补关系而非相同概念——MCP解决的是"谁来做实际工作"的问题

<details>
<summary>🇨🇳 查看中文翻译</summary>

在本模块中，我们将重点介绍模型上下文协议（MCP）。MCP是一个通信层，旨在为Claude提供上下文和工具，而无需你作为开发者编写大量繁琐的代码。当你初次接触MCP时，你会经常看到类似这样的图表。它展示了MCP的两个主要元素，即客户端和服务器。服务器通常包含多个内部组件，分别称为工具（Tools）、资源（Resources）和提示词（Prompts）。这里有很多术语。为了帮助你理解这一切，我们将假设正在构建一个小型应用，看看MCP如何融入其中。

我们的示例应用将是另一个聊天界面。它将允许用户就其GitHub数据与Claude进行对话。例如，如果用户问"我在所有不同仓库中有哪些开放的拉取请求"，预期Claude可能会使用某个工具来访问GitHub、获取用户账户信息，查看他们有哪些开放的拉取请求、开放的仓库等等。关键点在于，我们可能会通过一组工具来实现这一功能。

我想快速提一下，GitHub拥有大量的功能。有仓库、拉取请求、问题（Issues）、项目等众多内容。因此，要构建一个完整的GitHub聊天机器人，我们确实需要编写大量的工具。如果我们想构建这个示例应用，我们就需要负责编写所有这些schema和所有这些函数。这些都是我们作为开发者需要编写、测试和维护的代码。这需要大量的工作量，给我们带来了很大的负担。

让开发者维护大量集成的这一挑战，正是模型上下文协议旨在解决的主要难题之一。MCP将定义和运行工具的负担从你的服务器转移到另一个叫做MCP服务器的东西上。因此，你和我不再需要编写这些工具。相反，它们将在MCP服务器内部的其他地方被编写和执行。这些MCP服务器可以被视为某个外部服务的接口。例如，我可能有一个GitHub MCP服务器，专门提供GitHub相关的数据和功能访问，本质上是将大量GitHub功能封装到这个MCP服务器中，以一组工具的形式呈现。

现在我们对MCP服务器有了基本了解。它让我们访问一组工具，这些工具公开了与某个外部服务相关的功能。好处是你和我不需要编写所有这些不同的工具schema和函数等。

现在我们有了基本理解，我想回答一些人们初次了解MCP服务器时常见的问题。三个常见问题总是会被提出。

第一个常见问题是：谁来编写这些MCP服务器？答案是任何人都可以制作MCP服务器。但通常你会发现服务提供商会制作自己的官方实现。例如，AWS可能会决定发布他们自己的官方MCP服务器实现，其中可能包含各种不同的工具供你使用。

第二个常见问题是：使用MCP服务器与直接调用服务API有什么不同？如果我们想直接调用API（比如GitHub），我们就需要自己编写工具。而通过添加MCP服务器，我们节省了自己编写schema和函数实现的时间。

最后一个常见问题更多是一种常见的批评。这种批评通常来自那些不太理解MCP本质的人。你经常会看到有人说MCP和工具使用是同一回事。正如我刚才所解释的，MCP服务器和工具使用是互补的。它们是不同的东西，但它们是互补的。MCP背后的理念是你不需要编写工具函数和工具schema。这些由其他人为你完成，并封装在MCP服务器内部。所以在某种程度上，它们是类似的，因为我们在两种情况下都在讨论工具使用。但MCP服务器真正讨论的是谁在做实际的工作。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

In this module, we are going to focus on model context protocol. MCP is a communication layer designed to provide Claude with context and tools without requiring you, the developer, to write a bunch of tedious code. When you first get started with MCP, you will see diagrams that look like this very often. It shows two major elements of MCP, namely the client and the server. The server often contains a number of internal components, named Tools, Resources, and Props. Now, there is a lot of terminology here. So to help you understand all of this, we're going to imagine that we are building a small app and see how MCP fits into it. Our sample app is going to be another chat interface. It's going to allow a user to chat with Claude about their GitHub data. So if a user asks a question like what open pull requests do I have across all my different repositories, the expectation is that Claude is probably going to make use of a tool to reach out to GitHub, access the user's account, and see what open pull requests they have, maybe open repositories or whatever else. The point here is that we would implement this probably by using a set of tools. Now, one thing I want to mention really quickly is that GitHub has a tremendous amount of functionality. There are repositories, pull requests, issues, projects, and tons of other things. So to have a complete GitHub chatbot, we would really have to author a tremendous number of tools. If we wanted to build that sample app, we would be on the hook for authoring all these schemas and all these functions. And this is all code that you and I as developers would have to write, test, and maintain. That's a lot of effort, a lot of burden being placed on us. This challenge of making developers maintain a big set of integrations is one of the primary difficulties that model context aims to solve. MCP shifts the burden of defining and running tools from your server to something else called an MCP server. So no longer would you and I have to author this tool right here. Instead, it would be authored and executed somewhere else inside this MCP server. These MCP servers can really be thought of as like an interface to some outside service. So I might have a GitHub MCP server that provides access to data and functionality provided by specifically GitHub, where essentially wrapping up a ton of functionality around GitHub and placing it into this MCP server in the form of a set of tools. So at this point, we have a very basic understanding of what a MCP server is. It gives us access to a set of tools that exposes functionality related to some outside service. And the benefit here is that you and I do not have to author all these different tool schemas and functions and so on. Now that we have this basic understanding, I want to address some very common questions that a lot of people have when they first learn about MCP servers. So three common questions that seem to always come up. The first common question is who authors these MCP servers? The answer is anyone. Anyone can make an MCP server implementation. But very often you will find that service providers make their own official implementation. So for example, AWS might decide to release their own official MCP server implementation and inside of it, it might have a wide variety of different tools available for you to use. The second common question is how is using a MCP server different than just calling a services API directly? Well, as we just saw, if we wanted to call a API directly, such as GitHub, then we would have to author this tool ourselves. And now we can call GitHub directly. So what did we gain here? Well, all that really changed was we are now having to author the schema ourselves and the function implementation ourselves. So simply by adding in the MCP server, we are saving ourselves a little bit time. The final common question is more of a common criticism that you're going to see people have around MCP. And this criticism is most often coming from people who don't quite understand what MCP is all about. So very often you will see people saying MCP and tool use are the same thing. Well, as I have just laid out to you, MCP servers and tool use, they are complementary. They are different things, but they are complementary. The idea behind MCP is that you do not have to author the tool function and the tool schema. That is something that is done for you by someone else and is being wrapped up inside of this MCP server. So at some level, yeah, they're kind of similar because we are talking about tool use in both cases. But MCP servers are really talking about who is doing the actual work. So if you ever see this criticism, again, it's usually because people don't quite understand what MCP is all about.

</details>

### 什么是 MCP？

**Model Context Protocol（模型上下文协议）** 是 Anthropic 发起的一个**开放标准**，目的是标准化 AI 模型与外部数据源和工具的连接方式。

类比理解：**USB 之于外设** → **MCP 之于 AI 工具集成**

```
传统方式（N×M 问题）：
  3个AI × 3个工具 = 9 个集成

MCP 方式（N+M 问题）：
  3个AI + 3个工具 = 6 个集成
```

### MCP 的三大核心原语

| 原语 | 作用 | 类比 |
|------|------|------|
| **Tools** | 让 AI 调用外部函数 | API 接口 |
| **Resources** | 让 AI 读取外部数据 | 数据库/文件 |
| **Prompts** | 预定义的提示模板 | 操作手册 |

---

## 第 2 课：MCP 客户端

> 📹 视频：MCP Clients（5 min）


> 🎬 **视频 53**：MCP clients  
> 📁 文件：[53. MCP clients.mp4](videos/53.%20MCP%20clients.mp4)

**核心内容**
详细介绍MCP客户端的作用和工作机制，通过完整的消息流转图演示用户、服务器、MCP客户端、MCP服务器、GitHub和Claude之间的多步通信过程。

**关键要点**
- MCP客户端是你的服务器与MCP服务器之间的通信桥梁
- MCP是传输无关的（Transport Agnostic），支持stdio、HTTP、WebSocket等多种通信方式
- 核心消息类型：List Tools Request/Result（列出工具）、Call Tool Request/Result（调用工具）
- 完整消息流转：用户→服务器→MCP客户端→MCP服务器→外部服务（如GitHub）→逐层返回
- 服务器不再直接执行工具，而是通过MCP客户端委托给MCP服务器执行
- 同一台机器上的客户端和服务器通常通过标准输入输出（stdio）通信

<details>
<summary>🇨🇳 查看中文翻译</summary>

我们接下来要研究的模型上下文协议的下一部分是客户端。客户端的目的是在你的服务器和MCP服务器之间提供通信手段。这个客户端将是你访问该服务器实现的所有工具的入口点。

MCP是传输无关的（Transport Agnostic）。这个术语只是说客户端和服务器可以通过多种不同的协议进行通信。目前运行MCP服务器的一种非常常见的方式是在与MCP客户端相同的物理机器上运行。如果这两个东西运行在同一台机器上，那么它们可以通过标准输入输出（stdio）进行通信。这就是我们稍后要在本节中设置的内容。然而，还有其他方式可以连接MCP客户端和MCP服务器。它们也可以通过HTTP或WebSocket或其他多种技术进行连接。

一旦客户端和服务器之间建立了连接，它们通过交换消息进行通信。允许的确切消息类型都在MCP规范中定义。我们将重点关注的一些消息类型包括列出工具请求（List Tools Request）和列出工具结果（List Tools Result）。如你所猜，列出工具请求从客户端发送到服务器，要求服务器列出它提供的所有不同工具。服务器随后会用列出工具结果消息进行响应，其中包含它可以提供的所有不同工具的列表。

另外两种常见的消息类型是调用工具请求（Call Tool Request）和调用工具结果（Call Tool Result）。第一个会要求服务器使用某些特定参数运行一个工具。第二个会包含工具运行的结果。

现在让我通过一个完整的示例调用来展示所有这些不同组件如何一起工作。我们将想象用户、我们的服务器、MCP客户端、MCP服务器、GitHub和Claude之间的通信。

首先，用户向我们的服务器提交某种查询，比如"我有哪些仓库"。此时，我们的服务器需要向Claude发出请求。但在该请求中，我们需要列出Claude可以访问的所有不同工具。因此在向Claude发请求之前，服务器会通过MCP客户端和服务器做一个小迂回。服务器意识到它需要获取工具列表，所以会要求MCP客户端获取工具列表。MCP客户端随后向MCP服务器发送列出工具请求。服务器用列出工具结果响应。

现在MCP客户端有了工具列表，它会将列表返回给我们的服务器。现在服务器有了向Claude发送初始请求所需的一切——用户的原始消息和工具列表。Claude查看工具后意识到，为了回答用户的原始问题，它需要调用一个工具。所以Claude会返回一个工具使用消息部分。

此时，我们的服务器意识到Claude想运行一个工具。但我们的服务器不再负责执行任何工具。工具将由MCP服务器执行。因此，为了运行Claude请求的工具，我们的服务器会要求MCP客户端使用Claude提供的特定参数运行工具。MCP客户端实际上不运行工具，它会向MCP服务器发送调用工具请求。MCP服务器接收请求并向GitHub发出后续请求，获取属于该特定用户的仓库列表。GitHub返回仓库列表。然后MCP服务器将数据封装在调用工具结果中发送回MCP客户端。MCP客户端又将结果传递给我们的服务器。

现在我们的服务器有了仓库列表，可以在用户消息中包含工具结果部分向Claude发出后续请求。现在Claude有了所有需要的信息来生成最终响应，它会写出类似"你的仓库有……"的文本，发送回我们的服务器，服务器再发送给用户。

这整个流程确实比较复杂。我展示这个的原因是，当我们稍后开始实现自己的自定义MCP客户端和MCP服务器时，我们将会看到所有这些不同的组件。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

The next portion of ModelContext Protocol that we're going to investigate is the client. The purpose of the client is to provide a means of communication between your server and a MCP server. This client is going to be your access point to all the tools implemented by that server. Now MCP is Transport Agnostic. This is a fancy term that just says that the client and the server can communicate over a variety of different protocols. A very common way to run a MCP server right now is on the same physical machine as the MCP client. If these two things are running on the same machine, then they can communicate over standard input output. And that's what we're going to be setting up later on inside this section. There are, however, other ways we can connect the MCP client with the MCP server. So they can also connect over HTTP or Web Sockets or any of a number of other varieties or techniques. Once a connection has been formed between the client and the server, they communicate by exchanging messages. The exact messages that are allowed are all defined inside of the MCP spec. Some of the message types that you and I are going to be focusing are the List Tools Request and the List Tools Result. As you guessed, List Tools Request is sent from the client to the server and asks the server to list out all the different tools that it provides. The server would then respond with a List Tools Result message, which contains a list of all the different tools that it can provide. Two other common message types that you and I are going to see are the Call Tool Request and Call Tool Result. The first will ask the server to run a tool with some particular arguments. And the second will contain the results of the tool run. Now, at this point in time, we've got this idea of a server and a client, but I suspect it's probably not really clear how all this stuff really works together. So here's what we're going to do in the remainder of this video. We are going to walk through a example call between a lot of different things. So this will be kind of an involved process, but we're going to imagine the communication that goes on between a user, our server that we're putting together, an MCP client, the MCP server, GitHub as some provider that we're trying to access some data from and Claude. So let's get to it. Again, step by step. First thing we would expect to happen is a user to submit some kind of query or question to our server, like what repositories do I have. At this point, it would be up to our server to make a request off to Claude. But in that request, we want to list out all the different tools that Claude has access to. So before our server can make the request off to Claude, it's first going to go through a little side detour through the MCP client and the server. So here's what happens. The server is going to realize that it needs to see a list of tools to send off to Claude along with the user's query. So it's going to ask the MCP client to get a list of tools. The MCP client in turn is going to send a list tools request off to the server. And the server will respond with a list tools result. Now that our MCP client has a list of the tools, it will give that list of tools back to the server. And now our server has everything it needs to make an initial request off to Claude. It has both the original message from the user and a list of tools to include. So our server can make a request off to Claude with that query and the set of tools. Claude is going to take a look at the tools and realize you know what in order to answer the user's original question right here, I really want to call a tool. So Claude would respond with some tool use message part. At this point, our server is going to realize that Claude wants to run a tool. But our server is no longer really in charge of executing any tools. Instead, our tools are going to be executed by the MCP server. So in order to run the tool that Claude is asking for, our server is going to ask the MCP client to run a tool with some particular arguments that are provided by Claude. The MCP client, however, doesn't actually run the tool. It's going to send a call tool request off to the MCP server. The MCP server will receive that request and make a follow request off to GitHub. So this is where we would actually be getting a list of repositories that belong to this particular user. GitHub would respond with that list of repositories. Then the MCP server would wrap up that data inside of a call tool result and send that back to the MCP client. Then the MCP client in turn would hand the result off to our server. Now our server has the list of repositories and it can make a follow up request to Claude with the tool result part inside of a user message. So this tool result would include the list of repositories that Claude was asking for. Now Claude has all the information it needs to formulate a final response. So it will write out some text of something like your repositories are and then send that back to our server and our server would send it on back to our user. All right, so this flow, yes, it is rather complicated. The reason I want to show you this is that we are going to see all these different pieces as you and I start to implement our own custom MCP client and MCP server a little bit later on.

</details>

### 架构：Host → Client → Server

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│   MCP Host     │     │   MCP Client   │     │   MCP Server   │
│ (如 Claude     │────▶│ (协议实现层)    │────▶│ (工具提供方)    │
│  Desktop)      │     │               │     │               │
└────────────────┘     └────────────────┘     └────────────────┘
```

| 组件 | 角色 | 示例 |
|------|------|------|
| **Host** | 运行 AI 的应用程序 | Claude Desktop、Claude Code、VS Code |
| **Client** | 管理与 Server 的连接 | 通常由 Host 内置 |
| **Server** | 提供工具、数据、提示模板 | GitHub Server、Filesystem Server |

### 传输方式

| 方式 | 使用场景 | 说明 |
|------|---------|------|
| **stdio** | 本地 Server | Server 作为子进程运行，通过 stdin/stdout 通信 |
| **SSE** | 远程 Server | 通过 HTTP 连接远程 Server |

---

## 第 3 课：项目搭建

> 📹 视频：Project Setup（3 min）


> 🎬 **视频 54**：Project setup  
> 📁 文件：[54. Project setup.mp4](videos/54.%20Project%20setup.mp4)

**核心内容**
开始实现一个基于CLI的MCP聊天机器人项目，包括项目概述、下载起始代码、环境配置和依赖安装。

**关键要点**
- 项目是一个基于CLI的聊天机器人，允许用户操作内存中的假文档
- 初始实现两个工具：读取文档内容和更新文档内容
- 重要说明：正常项目中通常只实现客户端或服务器之一，本项目同时实现两者以便学习
- 项目使用UV包管理器，运行命令为 `uv run main.py`
- 起始代码以zip文件形式附在视频中，包含基本的聊天功能

<details>
<summary>🇨🇳 查看中文翻译</summary>

为了更好地理解MCP的一些方面，我们将开始实现自己的基于CLI的聊天机器人。这将让我们更好地了解客户端和服务器实际上是如何协同工作的。在本视频中，我想做一些项目设置，帮助你准确理解我们将要构建什么。

这是一个基于CLI的聊天机器人。我们将允许用户使用一组文档。这些是假文档，只存储在内存中。我们将构建一个小型MCP客户端，连接到我们自己定义的MCP服务器。目前，服务器中将实现两个工具：一个用于读取文档内容，一个用于更新文档内容。文档都是假的，只在内存中持久化。

有一个非常重要的说明。在正常项目中，通常我们只会实现客户端或MCP服务器中的一个。在真实项目中，我们可能只编写一个MCP服务器来分发给全世界，允许开发者访问我们构建的一些服务。或者，我们可能只构建一个MCP客户端，意图是连接到其他工程师已经实现的外部MCP服务器。在这个项目中，我们同时制作客户端和服务器，这样你能更好地理解这些东西如何实际协同工作。

附带在本视频中，你应该能找到一个名为CLIproject.zip的文件，里面有项目的起始代码。确保下载该zip文件，解压它，然后在该项目目录中打开代码编辑器。项目中有一个readme.md文件，其中放置了设置说明。它会引导你将API密钥放入项目的.env文件中，以及安装依赖项的过程（使用UV或不使用UV）。

设置完成后，可以通过在终端中运行 `uv run main.py`（使用UV）或 `python main.py`（不使用UV）来启动项目。运行后应该会看到聊天提示符出现，可以正常与Claude对话。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

To better understand some aspects of MCK, we are going to start to implement our own CLI-based chatbot. This is going to give us a better idea of how clients and servers actually work together. In this video, I want to do a little bit of project setup and just help you understand exactly what we're going to make. I've got a lot of product description over here of what we're going to build. We're going to go through all this over time. Right now, I just want you to get a high-level understanding. So, as I mentioned, it's going to be a CLI-based chatbot. We're going to allow users to work with a collection of documents. These are going to be fake documents. They're just going to be stored in memory. We're going to build out a small MCP client that is going to connect to our own custom MCP server. For right now, the server is going to have two tools implemented inside of it. One tool to read the contents of a document and one tool to update the contents of a document. Again, these documents are here on the right-hand side. They're all fake, so they are going to be persisted only in memory. That's it. Now, before we go any further, there is a very important note, something I really want you to understand around this entire process. That is, that on a normal project, typically we would be implementing either a client or an MCP server. So, on a real project, we might be authoring just an MCP server to distribute to the world and allow developers to access some services we have built up. Alternatively, we might be building a project where we make only a MCP client. And the intent here would be that we would be connecting to some outside MCP servers that have already been implemented by some other engineers. So, in this project, we are making both a client and a server. And we're just doing that in one project, so you get a better understanding of how this stuff actually works together. All right, now that we have this disclaimer out of the way, let's go through just a little bit of setup. Attached to this video, you should find a file named CLIproject.zip inside there is some starter code for our project. Make sure you download that zip file, extract it, and then open up your code editor inside of that project directory. Just to save a little bit of time, I have already done so. So, I've already got my code editor open inside of that small project. Inside this project, I would encourage you to take a look at the readme.md file. Inside here, I place some setup directions. So, it's going to walk you through the process of making sure you put your API key into the .mv file inside this project. And it's also going to walk you through the process of installing dependencies, either with UV or without UV. Once you have gone through all this setup, you can then run the starter project right away. To do so, inside of your terminal, make sure that you are inside of your project directory. So, I called my project mcp and inside there, I've got all my different project files and folders. To run the project, we will run uv run main.py if you're making use of uv. If you are not making use of uv, then it'll be just python main.py. Now, I'm making use of uv, so I'm going to do a uv run main.py. And then when I run that, I should see a chat prompt appear. And if I ask what's 1 plus 1, I should see a response rather quickly. That is it for our setup. So, now we can start to focus on adding in some new features to this application.

</details>


> 🎬 **视频 55**：Defining tools with MCP  
> 📁 文件：[55. Defining tools with MCP.mp4](videos/55.%20Defining%20tools%20with%20MCP.mp4)

**核心内容**
使用MCP Python SDK在服务器中定义工具，实现读取文档（read_contents）和编辑文档（edit_document）两个工具，展示SDK如何简化工具定义过程。

**关键要点**
- 使用 `@mcp.tool` 装饰器定义工具，SDK自动生成JSON schema
- 使用Pydantic的 `Field` 为参数添加类型和描述
- read_contents工具：接收doc_id，返回文档内容
- edit_document工具：接收doc_id、old_string、new_string，执行查找替换
- 两个工具都包含文档ID存在性检查的错误处理
- 使用MCP SDK定义工具比手动编写JSON schema简单得多

<details>
<summary>🇨🇳 查看中文翻译</summary>

让我们开始为CLI聊天机器人制作MCP服务器。CLI本身已经可以工作，我们可以和Claude聊天，但目前还没有与MCP服务器相关的额外功能。我们将添加一个MCP服务器，其中包含两个工具——一个用于读取文档，一个用于更新文档内容。

服务器的实现放在根项目目录的 `mcp_server.py` 文件中。文件里已经有基本的MCP服务器设置、一组存储在内存中的文档集合，以及一些待完成的TODO项。目前我们只完成前两个：编写两个工具。

**MCP Python SDK 让工具定义变得简单**

之前我们手动定义工具时看到了大量语法——那些庞大的JSON schema。但好消息是，在这个项目中我们使用了**官方MCP Python SDK**（`mcp` 包）。这个SDK只需一行代码就能创建MCP服务器（如文件中那行代码所示），而且定义工具非常简单——只需使用装饰器语法，SDK会在后台自动为我们生成工具的JSON schema，然后可以传递给Claude。

**实现 read_contents 工具**

目标很简单：接收文档名，返回其内容。所有文档都在 `docs` 字典中，键是文档ID/名称，值是内容。

使用 `@mcp.tool` 装饰器，设置名称为 `read_contents`，描述为"读取文档内容并以字符串形式返回"。理想情况下，描述应该非常详尽以确保Claude清楚何时使用此工具，但这里为了简洁先用简短描述。

定义函数 `read_document`，接收 `doc_id: str` 参数，使用 Pydantic 的 `Field` 添加参数描述"ID of the document to read"。需要在文件顶部添加导入：`from pydantic import Field`。

实现逻辑：先处理错误——如果 `doc_id not in docs`，抛出 `ValueError(f"doc with ID {doc_id} not found")`；否则返回 `docs[doc_id]`。

这就是定义一个工具所需的全部。我们指定了工具名称、描述、预期参数、参数类型和描述。所有这些装饰器、Field类型等都会被MCP Python SDK自动整合，生成相应的JSON schema。

**实现 edit_document 工具**

重复相同的流程。`@mcp.tool` 装饰器，名称为 `edit_document`，描述为"通过替换文档内容中的字符串来编辑文档"。

函数 `edit_document` 接收三个参数：
- `doc_id: str` — Field描述"ID of the document that will be edited"
- `old_string: str` — Field描述"the text to replace, must match exactly including whitespace"
- `new_string: str` — Field描述"the new text to insert in place of the old text"

实现逻辑：同样先检查 `doc_id not in docs` 的情况，然后执行 `docs[doc_id] = docs[doc_id].replace(old_string, new_string)`。文档编辑就是简单的查找替换。

就这样，我们非常快速地完成了两个工具实现。使用MCP Python SDK定义工具确实比手动编写schema定义要容易得多。服务器有了一个良好的开端，接下来的步骤就是测试这些工具。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Let's start to make an MCP server for our CLI chatbot. As you saw, the CLI itself already works, and we can already chat with Clawed, but there's no additional functionality around the MCP server tied to it just yet. So we're going to work on adding in this MCP server that is going to have two tools in it for right now. It's going to have one tool to read a document, and one tool to update the contents of a document. The implementation of the server is going to be placed into the MCP server.py file inside the root project directory. Inside of here, I've already gone through a little bit of work to set up a basic MCP server. And then I defined a collection of documents that are going to exist only in memory. And then finally, I put together some different 2DU items. So these are different tasks that you and I are going to complete inside of this file. For right now, as I just mentioned, we're going to be working only on these first two items, writing out two tools. Now we have authored tools in the past, and we saw that, oh, there's a lot of syntax there. There's those big JSON schemas. But I got good news for you here. In this project, we're making use of the official MCP Python SDK. So that's what this MCP packages that we're making use inside of here. This MCP package is going to create our MCP server for us with just one line of code, like what you see right there. This SDK also makes it really easy to define tools. To define a tool, all we have to do is write out what you see on the right-hand side over here. This will make a tool named AddIntegers with this description and two arguments that are going to be required to be passed into it. Once we write out a tool definition like this, behind the scenes, MCP is going to generate a tool JSON schema for us, which we can take and pass off to Claude. So right away, as you can see, it starts to get a lot easier to do some basic things like defined tools. Now, as I mentioned, our first task is going to be to implement these two different tools. So let's go back over to our MCP server.py file right away. Now we're going to start to implement the first tool of reading a document. So the only goal here is to take in the name of some document and return the contents of it. All of our documents are already placed inside of this docs dictionary. The keys are the IDs or essentially names of a document, and the value is a document's contents. So our tool is really simple. We're going to take in one of these strings, look up the appropriate value inside this docs dictionary, and then return it. That's all we need to do. So to implement this, I'm going to find the first to do, and right underneath it, I'm going to define a new tool by writing out at MCP.Tool. I'm going to give this tool a name of read.contents and a description of read the contents of a document and return it as a string. I remember in a perfect world, we put in a really fleshed out description right here to make sure it's super clear to Claude, exactly when to use this tool. But right now, just as usual, to save a little bit of time and keep you from having to type out a bunch of text here, I'm just going to leave in a very simple description. Then I will define my actual tool function. So this is the function to run whenever we decide to run this tool. I will call it read document. It's going to take in a argument of doc ID that is going to be a string. I'm going to set that to a field with a description of ID of the document to read. And then we need to make sure that we import this field class at the top. So I'm going to go up to the top and add an import from PyDanticImportField. Then back down here, inside of the function body, I'm going to put in my actual implementation. The first thing I'm going to do is just make sure I handle the case in which Cloud asks for a document that doesn't actually exist. So I'll say if doc ID not in docs, so in other words, if the provided document ID is not found as a key inside of this dictionary, then I'm going to raise a value error with a estering of doc with ID.id not found. And then if we get past that check, I'll go ahead and return the actual document. So I'll return docs at doc ID. And that's it. That's all it takes to define a tool. So we've specified the name of the tool, its description, the argument that is expected, its type, and a description for that argument as well. All these different decorators and field types and whatnot are all going to be taken together by this Python MCP SDK, and it's going to generate a JSON schema for us. Now that we've implemented this first tool, I'm going to remove the to-do right there, and then we will implement our other tool, the one to edit a document. So we're going to repeat the exact same process. I'll say MCP.tool. I'll give it a name of edit document with a description of edit a document by replacing a string in the documents context or semi-content with a new string. Then for the implementation, I'll call this function edit doc. Or so we'll be consistent call edit document. And then we're going to take in a couple of different arguments here. First is going to be a document ID, and then a old string to find, and then a new string to replace the old string with. So let's write this all out. We're going to have a doc ID. That will be a string with a description of ID, of the document that will be edited. Old string will be a string, with a description of the text to replace, must match exactly, including white space. And then our new string, the new text to insert in place of the old text. So our document editing here is just a very simple, fine and replace. That's it. Once again inside of here, I'm going to make sure that Claude is asking for a document that actually exists. So if doc ID not in docs, raise value error with a f string of doc with ID not found. And then if we do find the correct document, here's how we will do our edit. We'll say docs at doc ID is docs at doc ID, replace old string with the new string. And that's it. All right, so just like that, we have put together two tool implementations really, really quickly. I can't repeat it enough. The finding tools with this MCP Python SDK is a lot easier than writing out the schema definition manually. Now that we've got both tools put together, I'm going to delete the tutu right there. Okay, so this is a good start. We have put together our MCP server and we've implemented two tools inside of it.

</details>

### 安装 MCP SDK

```bash
# Python SDK
pip install mcp

# TypeScript SDK
npm install @modelcontextprotocol/sdk
```

---

## 第 4 课：Server Inspector

> 📹 视频：Server Inspector（4 min）


> 🎬 **视频 56**：The server inspector  
> 📁 文件：[56. The server inspector.mp4](videos/56.%20The%20server%20inspector.mp4)

**核心内容**
介绍MCP Inspector调试工具，演示如何使用浏览器内调试器测试MCP服务器中定义的工具，无需连接实际应用即可验证工具功能。

**关键要点**
- 运行 `mcp dev mcp_server.py` 启动MCP Inspector调试器
- Inspector提供浏览器界面，可以查看和测试工具、资源、提示词
- 可以手动输入参数并运行工具，立即查看返回结果
- 支持测试read_contents和edit_document工具的完整功能
- 是MCP服务器开发过程中的重要调试工具
- Inspector正在积极开发中，界面可能随时间变化

<details>
<summary>🇨🇳 查看中文翻译</summary>

我们在MCP服务器中实现了一些功能，但不知道它是否正常工作。使用Python SDK，我们可以自动访问一个浏览器内调试器来确保服务器按预期工作。

在终端中，确保Python环境已激活，然后运行 `mcp dev mcp_server.py`。运行后会提示服务器监听在6277端口，并给出一个可以访问的地址。在浏览器中打开该地址，就会看到MCP Inspector。

需要注意的是，Inspector正在积极开发中，所以界面可能会有所变化。左侧有一个Connect按钮，点击它会启动MCP服务器。连接后，顶部菜单栏会列出Resources、Prompts、Tools等选项。

点击Tools，然后点击List Tools，就能看到我们刚才定义的工具名称。点击某个工具，右侧面板会变化，可以用来手动调用工具以确保它按预期工作。这就是我们在不将MCP服务器连接到实际应用的情况下进行实时开发的方式。

测试read_contents工具：输入文档ID（如deposition.md），点击Run Tool，就能看到成功结果和文档内容。

测试edit_document工具：输入文档ID、要替换的旧字符串和新字符串，运行工具后显示成功。然后回到read_contents工具重新读取同一文档，可以验证编辑是否正确应用。

MCP Inspector允许我们非常方便地调试正在实现的MCP服务器，无需将服务器连接到实际应用。在构建自己的MCP服务器时，你会经常使用这个Inspector工具。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

We have put together some functionality inside of our MCP server, but we have no idea if it works. So it'd be really great if we could test this out somehow. It turns out that by using this Python SDK, we automatically get access to an in-browser debugger, so we can make sure that this server is working as expected. Let me show you how to use it really quickly. Back inside my terminal, I want to make sure that I have my Python environment activated. Remember the ReadMe document goes into detail on the exact command to run to make sure that you have activated that environment. Once you are sure that it is activated, we'll run MCP, Dev, and then the name of the file that contains our server. In this case, it is MCPServer.py. Once I run that, I'll then be told that I have a server listening on port 6277 and I'll be given a direct act address to actually access it. I'm going to open up that address inside my browser. And once you go there, you'll see something that looks like this. This is the MCP Inspector. Right away, there's something important I want you to understand here. This Inspector is in active development. So by the time you are watching this video, what you see on the screen right now might be very, very different than what I am showing. Nonetheless, it's probably still going to have some very similar functionality. On the left-hand side, you'll see a Connect button. That is going to start up your MCP server, so that file that we just edited. I'm going to click on Connect. And then right away, we'll see a couple of different things on the screen appear. I first want you to notice the top menu bar up here. It lists out resources, prompts, tools, and some other stuff. Again, the UI might change by the time you watch this video. So if you do not see this menu bar up here, all we are really looking for here is some Tools section. Once I click on Tools, I will click on List Tools. And I'll see the name of the tools that we just put together. If I click on one, the right-hand panel is then going to change. And I can use this panel over here to manually invoke one of my tools to make sure that it is working as expected. So this is how we can do some live development on our MCP server without actually having to wire it up to a real application. In order to use the read.contents tool, all we have to do is put in a document ID. If I go back over to my editor and go up to the docs dictionary right here, I can copy one of these document IDs so I will take out deposition.md. I will put it in as the Doc ID and then click on Run Tool. I should then see Run Tool of Success with the contents of the document. And that is it right there. I can verify it. So same exact string is what I see right there. We can use this same exact technique to test out the other tool as well. So I will change over to the Edit Document tool. Now I'll put in my Document ID. My old string that I want to replace how about replace the word deposition? Actually, I have an easier word to type out. How about just this? That'll be a little bit easier. So my old string is this. Remember that is going to be a capital sensitive and I'm going to replace it with a report. And if I run the tool, I'll then be given a success. Remember that tool does not actually return the documents contents. It just edits the document. So now to verify that the edit was done correctly, I can go back over to the Redock contents tool. Run that one again with the same document ID. And I should see a report deposition and then blah, blah, blah. All right, so as you can see, this MCP inspector allows us to very easily debug a MCP server that we are implementing without actually having to wire the server up to an actual application. As you start building your own MCP servers, I expect you'll be using this Inspector tool quite a bit. And we'll probably use it a little bit more inside of this module. Just make sure that our server development is going along pretty well.

</details>

### MCP Inspector：调试 MCP 服务器的可视化工具

Inspector 让你可以直观地查看 MCP Server 暴露的所有工具、资源和提示模板，方便开发调试。

---

## 第 5 课：实现客户端

> 📹 视频：Implementing a Client（7 min）


> 🎬 **视频 57**：Implementing a client  
> 📁 文件：[57. Implementing a client.mp4](videos/57.%20Implementing%20a%20client.mp4)

**核心内容**
实现MCP客户端的list_tools和call_tool两个核心函数，通过客户端会话连接MCP服务器，实现工具列表获取和工具调用功能。

**关键要点**
- MCP客户端类封装client session（与MCP服务器的实际连接），管理资源清理
- list_tools函数：通过session获取服务器定义的所有工具列表
- call_tool函数：通过session调用指定工具，传入名称和参数
- 正常项目中通常只实现客户端或服务器之一
- 客户端将服务器功能暴露给代码库其他部分使用
- 测试验证：可直接运行mcp_client.py查看工具定义，也可通过CLI应用让Claude使用工具

<details>
<summary>🇨🇳 查看中文翻译</summary>

服务器已经准备就绪，现在我们将转向MCP客户端的实现。客户端位于根项目目录的 `mcp_client.py` 文件中。

在动手之前，先提醒一下：通常在典型项目中，我们要么使用客户端，要么实现服务器，只是在这个项目中两者都做，以便你能看到完整的拼图。

**MCP Client 类的结构**

MCP客户端由一个单独的类组成。你会注意到文件中有大量代码，不如服务器那边简洁。让我解释一下这个文件的内容和为什么这么大。

这个类封装了一个叫做**客户端会话（client session）**的东西——它是与MCP服务器的实际连接，是MCP Python SDK的一部分。会话本身需要**资源清理（resource cleanup）**——当我们关闭程序或不再需要服务器时，需要经过清理过程。我已经在MCP客户端类中编写了大量清理代码（你可以在 `connect`、`cleanup`、`__aenter__` 和 `__aexit__` 函数中看到）。这就是这个类存在的原因——用更大的类来管理资源清理是非常常见的做法，而不是直接使用 client session。

**客户端的目的**

在我们的代码中，有些时候需要获取工具列表发送给Claude，之后还需要运行Claude请求的工具。为了访问MCP服务器获取工具列表或运行工具，就需要MCP客户端。客户端本质上是将服务器的功能暴露给代码库的其他部分。

在项目的 `core` 目录中已有其他代码在调用这个类的函数，如 `list_tools`、`call_tool`、`list_prompts`、`get_prompt` 等。

**实现 list_tools**

本视频中我们实现两个函数。首先是 `list_tools`：

```python
result = await self.session.list_tools()
return result.tools
```

就这么简单。通过会话（与MCP服务器的连接）调用内置函数获取服务器定义的所有工具列表。

**实现 call_tool**

```python
return await self.session.call_tool(tool_name, tool_input)
```

通过会话调用特定工具，传入工具名称和Claude提供的输入参数。

**测试**

文件底部有一个测试块，可以直接运行 `mcp_client.py` 文件。注意如果你没有使用 UV，请查看代码中关于修改 `command` 和 `args` 的注释。

在测试块中添加代码：
```python
result = await _client.list_tools()
print(result)
```

运行 `uv run mcp_client.py`（不用UV的话用 `python mcp_client.py`）。它会启动MCP服务器的副本，获取工具列表并打印。可以看到 `read_doc_contents` 工具和 `edit_document` 工具的定义，每个都包含描述和输入schema——这就是最终会传递给Claude的工具定义。

**在CLI应用中测试**

现在两个函数都实现了，项目中其他调用 `list_tools` 和 `call_tool` 的代码也可以工作了。运行CLI应用 `uv run main.py`，询问Claude"report.pdf文档的内容是什么"（确保输入正确的文档名），请求会连同工具列表一起发送给Claude。Claude决定使用 read_document 工具，获取文档内容后回答——文档内容是关于20米冷凝塔的报告。

至此，客户端功能已就绪。客户端允许我们访问MCP服务器实现的功能——列出工具和执行工具。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Now that our server is in a good place, we're going to shift gears a little bit and start working on our MCP client. The client can be found inside the MCP client.py file inside the root project directory. Now before we do anything inside this file, I just want to give you a very quick reminder here. Remember what I told you about earlier. Usually in a typical project, we are either making use of a client or we are implementing a server. It's just in this one particular project that we are working on that we are doing both, again, just so you can see both sides of the puzzle. Now the MCP client itself inside this file is consisting of a single class. You'll notice there is a lot of code inside of here and it doesn't look quite as pretty as some of the code we just wrote out inside of the server. So let me tell you exactly what's going on inside this file and exactly why it is so large. Okay, so inside this file, we are making the MCP client class. This class is going to wrap up something called a client session. The client session is the actual connection to our MCP server. This client session is a part of the MCP Python SDK. So again, this session is what gives us this connection to the outside server. The session itself requires a little bit of resource cleanup. In other words, whenever we close down our program or decide that we don't need the server anymore, we have to go through a little bit of a cleanup process. And I have already written out a lot of that cleanup code inside of the MCP client class. So that's really why this class exists at all. Just to make that cleanup a little bit easier. You can see some of that cleanup code inside of the connect function and down a little bit lower at the cleanup, async enter and async exit functions as well. So it's very common practice to not just make use of this client session directly, instead very common to wrap it up inside of a larger class that's going to manage some of this different resource stuff for you. The next thing I want to clarify is why this client exists at all. So in other words, what is the client really doing for us here? Well, remember this folder we looked at a little bit ago. So we had our code right here, and at certain points in time, we needed say a list of tools to send off to Claude. And then later on after that, we also needed to run a tool that was requested by Claude. In order to reach out to our MCP server and get this list of tools or to run a tool, that's where we are making use of the MCP client. So we can imagine that this client is exposing some functionality that belongs to the server to the rest of our code base. So inside of our code base, inside this project, specifically inside of the core directory, there is a lot of code already inside there that I put together that is making use of this class. So there are some other code that's going to call some of the different functions you see inside of here, like list tools, call tool, list prompts, get prompt, and so on. For right now in this video, we're going to focus on implementing two functions, list tools and call tool. So as you just saw in the diagram, we looked at a moment ago, these two functions are going to be used in different parts of our code base to get a list of tools to provide off to Clawed and then eventually call a tool whenever a Clawed request to call a tool. Implementing these two functions is going to be really simple and straightforward. So let me show you how we're going to do it. We'll first begin with list tools. I'm going to remove the two do inside there and replace it with result is await self.session. I'm going to call that like a function list underscore tools and then I will return result.tools. And that's it. So this is going to get access to our session, which is our actual connection to the MCP server. It's going to call a built in function to get a definition or a list of all the different tools that are implemented by that server. I'm going to get back result and then just return the tools and that's it. Then we can implement call tool right here in a very similar fashion. So this will be return await self.session call tool, tool name and tool input. Once again, getting access to the session, that is our connection to the server and I'm going to attempt to call a very specific tool. The name of the tool we passed in along with the input parameters or input arguments to it that were provided by Clawed. Now this point time, I would like to test out these two functions really quickly. To do so, we're going to go down to the bottom of this file where I put together a very small testing harness for us. So down here, you'll notice I put together this testing block. So we can run this MCP client.py file directly. And if we do so, we're going to form a connection to our MCP server and then we can just run some commands against it and just see what we get back. Notice that in your version of the code, there's a comment in there about changing the command in args right here in case you are not making use of UV. So if you're not using UV, make sure you take a look at that comment. Inside of this width block, I'm going to add in a little bit of testing code. So I'll say result is await, underscore client, list tools, and then I'm going to just print out the result that we get back. So this should start up a copy of our MCP server, then attempt to get a list of all the different tools that are defined by it, and then just print out the result. To test this out, I will flip back over to my terminal and do a UV run, MCP underscore client.py. And as usual, if you are not making use of UV, you'll just do a Python MCP client.py. Okay, so I'll run that. And there is our list of tool definitions. So I can see inside of here that I have the read doc contents tool, which we put together a little bit ago, and our edit document tool as well. Each one has a description and a input schema as well. So this is our tool definition, which will eventually be passed off to Claude. Now before we move on, there's one other thing I want to test. Remember, we just implemented the function that's going to allow us to list out some tools and pass them off to Claude, and the function that's going to allow us to call a tool that is implemented by the MCP server, and then pass the result off to Claude as well. I have already implemented the code that is going to call list tools and call tool for us somewhere else inside this project. So now that we have added in this functionality, now that we have defined these tools and the ability to call a particular tool, we can now run our CLI again and attempt to get Claude to make use of these tools. In other words, we can ask Claude to inspect the contents of some particular document and even edit a document. So let me show you how we do that. Inside of my MCP server, I just want to give you a reminder that there is a document with a ID of report.pdf, and it has some text here of something like a 20 meter condenser tower. I'm going to go back over to my terminal, and I'm going to run my project with a UV run main.py, and then I'm going to ask Claude what is the contents of the report.pdf document, and make sure you put in exactly report.pdf here. And when we run this, we're sending off along with the request our list of tools. Claude is going to decide to use the read document tool, and it's going to get the contents of the document, and then we will see that yes, Claude was able to get the contents of that document. We are told that the report is something about a 20 meter condenser tower. All right, so at this point, we have added in some functionality around our client. Remember, the client is what allows us to access some functionality that is implemented inside of the MCP server. At this point in time, we have been able to list out some tools that are created by the server and execute a tool that has been implemented by the server.

</details>

### 编写 MCP 客户端

连接服务器、发现工具、调用工具：

```python
# 客户端核心操作
# session.list_tools()    — 发现可用工具
# session.call_tool()     — 调用工具
```

---

## 第 6 课：定义资源

> 📹 视频：Defining Resources（10 min）


> 🎬 **视频 58**：Defining resources  
> 📁 文件：[58. Defining resources.mp4](videos/58.%20Defining%20resources.mp4)

**核心内容**
介绍MCP服务器的资源（Resources）概念，实现两个资源——返回文档ID列表和返回单个文档内容，支持@提及文档的自动完成功能。

**关键要点**
- 资源允许MCP服务器向客户端公开数据，每个读操作通常定义一个资源
- 两种资源类型：直接资源（静态URI）和模板资源（URI含参数，如 `{doc_id}`）
- 使用 `@mcp.resource` 装饰器定义资源，指定URI和mime类型
- 第一个资源：`docs://documents`，返回JSON格式的文档ID列表
- 第二个资源：`docs://documents/{doc_id}`，返回纯文本格式的文档内容
- 模板资源的URI参数会自动解析为函数的关键字参数
- MCP SDK自动处理返回值的序列化

<details>
<summary>🇨🇳 查看中文翻译</summary>

本视频将介绍MCP服务器中的下一个主要功能——资源（Resources）。我们将通过在项目中实现另一个特性来帮助理解资源。

**要实现的功能**

允许用户通过输入 `@` 符号加文档名来**提及（mention）**一个文档。用户这样做时，会自动获取该文档的内容并插入到发送给Claude的提示词中。例如用户说"report.pdf文件里有什么？"，我会组装一个提示词包含用户查询和文档内容发送给Claude——这样Claude不需要调用工具就能直接回答。

这个功能有两个方面：
1. 输入 `@` 时自动显示可用文档列表（自动完成）
2. 提交包含提及的消息时自动获取文档内容并插入提示词

**什么是资源？**

这其实是两个独立的功能：获取所有文档名列表，以及获取单个文档内容。为此我们使用**资源（Resources）**。

资源允许MCP服务器向客户端公开一定量的数据。我们通常为每个不同的读操作定义一个资源。在我们的例子中需要两个资源：一个返回文档名列表，一个返回单个文档内容。

**完整的数据流**：当用户输入 `@` 字符时 → 代码通过MCP客户端发送 read resource 请求到MCP服务器 → 请求中包含一个 **URI**（资源地址，在定义资源时确定） → 服务器根据URI运行对应函数 → 将结果通过 read resource result 消息返回 → 客户端取出数据显示在自动完成中。

**两种资源类型**

- **直接资源（Direct/Static）**：静态URI，如 `docs://documents`，永远不变
- **模板资源（Templated）**：URI中包含参数，如 `documents/{doc_id}`。请求时URI中的参数会被MCP Python SDK**自动解析**，作为**同名关键字参数**传递给函数（URI里的 `doc_id` 就是函数的 `doc_id` 参数）。当需要更多选择性或定制化时使用模板资源。

**实现第一个资源：返回所有文档ID**

```python
@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    return list(docs.keys())
```

URI为 `docs://documents`（类似路由处理器），mime类型为 `application/json`——这是给客户端的提示，表示返回的是JSON字符串，客户端需要反序列化。注意我们返回的是列表而非JSON字符串——MCP Python SDK会自动将返回值转换为字符串。

**实现第二个资源：返回单个文档内容**

```python
@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"doc with ID {doc_id} not found")
    return docs[doc_id]
```

这是模板资源，URI中有 `{doc_id}` 通配符。mime类型为 `text/plain`，因为只返回文档的纯文本内容。在实际应用中，读取文档可能会返回完整的文档记录（包含ID、内容、作者名等字典），但这里为了演示纯文本返回就只返回文本内容。如果在URI中添加其他参数（如 `{doc_type}`），它会作为额外的关键字参数出现在函数中。

**在MCP Inspector中测试**

运行 `mcp dev mcp_server.py` 启动Inspector。连接服务器后：
- **列出资源**（Resources → List Resources）：显示静态资源 `docs://documents`
- **列出资源模板**（Resource Templates）：显示 `fetch_doc` 模板
- **运行静态资源**：返回的消息包含 `text` 属性，里面是序列化为JSON字符串的数据，客户端需要从JSON反序列化为可用的字符串列表
- **运行模板资源**：输入 `doc_id`（如 report.pdf），返回 `text/plain` 类型的纯文本文档内容——这提示客户端不要尝试从JSON反序列化

</details>

<details>
<summary>📜 查看视频转录原文</summary>

In this video, we're going to move on to the next major feature inside of MCP servers, which is resources. To help you understand resources, we're going to be implementing another feature inside of our project. Here's what we're going to add in. I want to allow a user to mention a document by putting in an app symbol and then the name of a document. Whenever they do so, I want to automatically fetch the contents of that document and insert it into the prompt that we send off to Claude. So in total, there's going to be kind of two aspects to this feature. Whenever a user types out the app symbol inside of a message, we're going to automatically show a list of all the different documents that they can mention inside of a little auto-complete window. Then whenever a user submits a message with a mention inside of it, we're going to automatically get the contents of that document and insert it into the prompt that we send off to Claude. So for example, if a user says something like what's in the atchreport.pdf file, I would want to assemble a prompt like this and send it to Claude. So we're going to have the query inside there from the user and then we're also going to tell Claude that the user might have referenced some document and here is the contents of the document. So the approach here or the idea here is that we will not have to rely upon Claude to go and make use of some tool to figure out what is inside of the report.pdf file. Instead, the user can just preemptively mention the file and we're going to automatically insert some context ahead of time. Now one thing I want to clarify here is that we're kind of talking about two separate features. The first feature is that whenever a user types in the at symbol, we really need the mcp server to give us a list of all the different documents that the user can possibly mention. And then the second aspect here is that whenever a user submits a message that contains a mention, then we need the mcp server to give us the contents of a single document. To get this information out of our mcp server, we are going to be making use of resources. Resources allow our mcp server to expose some amount of data to the client. We usually define one resource for each distinct read operation. So in our example, we need to get a list of documents and read the contents of a single document. So we would probably end up making two separate resources. One resource would be responsible for returning just a list of document names so we can put them inside the autocomplete. And then we would probably make another resource that will expose the contents of a single document based upon its document ID. When we define these resources, they are going to be accessed through our mcp client. So the entire flow that we're going to eventually put together here, whenever user types in something like what's in the at and then presumably they're going to put in something right there. As soon as they type in that at character, we need to display a list of document names to put in the autocomplete. So our code is going to reach out to the mcp client, which in turn is going to send a read resource request off to the mcp server. Inside of that read resource request, we're going to include something called the URI. That is essentially the address of the resource we want to read. This URI gets defined whenever we put together our resource initially. So the URI is that right there. When we send off this read resource request, the mcp server is going to look at the exact URI that we put inside of here and then run the function we put together right there, take the result and send it back to us inside of a read resource result message. We can then take the data inside there and display it inside of our autocomplete or do whatever else we need to do with it. There are two different types of resources, direct and templated. You'll also sometimes see direct resources referred to as static resources. A direct resource just has a static URI. So it's always going to be the exact same thing, such as docs, colon slash slash documents. A templated resource will have one or more parameters inside of its URI. So for example, we might have documents slash and then kind of a wild card right here. So we can put in any document ID we want to. And whenever we ask for this resource, that document ID right there inside the URI will be automatically parsed by the Python mcp SDK and provided as a keyword argument to our function. The keyword argument will have the exact same name of whatever string you put in right there. So doc ID right there will be doc ID right there. As you can probably guess, we'll make use of templated resources anytime that we want to allow a little bit more selection or variety or customization in what someone is asking for out of our mcp server. Implementing resources is pretty straightforward. So let's go back over to our editor and we're going to add in some resources to our server right away. All right, so back over inside my editor, I will find the mcp server.py file. I'm then going to scroll down a little bit and I'm going to find some comments for writing resource to return all document IDs and writing resource to return the contents of a particular document. Now for this first one right here, I put in the comment document IDs. Remember for us, our document IDs are essentially the name of the document. So for us, we're really just returning these IDs. They're going to serve the purpose of the name. That means we can put them directly into that autocomplete element. All right, so to make our resource, I'm going to delete that to do and then I'll add in a mcp.resource. The first argument is going to be the URI for accessing this thing. Again, it's kind of equivalent to a route handler. So I will use docs, colon slash slash documents. And I'm also going to add in a mime type of application slash JSON. A resource can return any type of data. So it can be plain text, it can be JSON, it can be binary data, anything. It's up to us to kind of give our client a hint as to what kind of data we are returning to do so. We're going to define this mime type. A mime type of application slash JSON is a hint to our client who's eventually going to ask for this resource right here that we're going to be sending back a string that contains some structured JSON data. And so it would be up to our client to de-serialize that data, or essentially turn it into some usable data structure. Underneath that decorator, I'll write out my function of list docs and I'm going to return a list of strings. And then inside there, I'll return list docs keys. So just take all the keys out of that dictionary and turn it into a list and I'm going to return it. Now you'll notice that we are not returning distinct JSON here. In the words we're not actually returning a string. The mcp Python SDK is going to automatically take whatever we return and turn it into a string for us. All right, let's take care of our second resource. So I'm going to delete that comment and then replace it with mcp resource docs colon slash slash documents. And then this time I want a templated resource because I'm putting in this wildcard right here. And then my mime type this time around just for a little bit of variety, I'm going to be returning plain text because it's going to be just the contents of the document. And I'm not going to wrap it up in any kind of structure. Now just so you know in a real application, something like read a document, I would probably return an entire document record. So some kind of dictionary that contains maybe the ID, the content, the author name, the author ID and stuff like that. But just for the sake of an example, I'm going to return just the text at the document to show you how we would normally return plain text. So in this scenario, my mime type would be text plain. And then I will make fetch doc. I'm going to take doc ID, which is going to be a string. And I'm going to return a string. Once again, whatever word you put right there, it's going to show up as a keyword argument inside of your function. If we added in some additional parameters inside of here, such as maybe doc type or something like that, it would just show up as an additional keyword argument like so. Then inside of here, I'm going to first make sure that the ID that this person is asking for actually exists. So if doc ID not in docs, I'm going to raise a value error with the F string that says doc with ID not found. And then if we get past that check, I'll return docs doc ID. And that's it. Now let's try testing this stuff out inside of our MCP inspector once again. So remember at our terminal, we can run the command, you the run MCP dev MCP server.py. That's going to start up a web server at port 6277 or see me 6274 is the default. So I'm going to make sure I open that up inside my browser. Here we go. I'll click connect. I'll then find resources. And then I should build to list out all the different resources that are available. Now when I list out resources, this is going to be specifically static or direct resources. So I'll see only docs slash documents. And then I can separately list out all my different resource templates. And so I'll see that I have one resource template of fetch doc. I can first try to run the slash documents right here. We'll see what we get back. So this is the actual message, the exact structure that gets returned from our MCP server. You'll notice that it has a text property inside there is all the data that we are returning serialized as JSON string. So again, it would be up to us inside of our CLI application to take this text right here and deserialize it from this JSON string into a usable list of strings. Then we can also test out fetch doc. So I'll click on that. I have to enter a doc ID. So I'm going to put it in. I want to read the report.pedia file. And I'll read the resource. And now I should see the contents of that particular document. And you'll notice this I'm around once again, I get a text plane. So that's a hint to me that this is plain text. And I should not attempt to deserialize it from JSON in any way.

</details>

### Resources：为 Claude 提供上下文数据

```python
from mcp.server import Server

server = Server("my-server")

@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="db://users/schema",
            name="Users Table Schema",
            description="Database schema for the users table",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri == "db://users/schema":
        schema = await db.get_schema("users")
        return json.dumps(schema)
```

---

## 第 7 课：读取资源

> 📹 视频：Fetching Resources（5 min）


> 🎬 **视频 59**：Accessing resources  
> 📁 文件：[59. Accessing resources.mp4](videos/59.%20Accessing%20resources.mp4)

**核心内容**
在MCP客户端中实现read_resource函数，根据mime类型正确解析资源内容，实现@提及文档的自动注入功能。

**关键要点**
- 实现客户端的read_resource函数来请求MCP服务器的资源
- 根据mime类型区分处理：`application/json` 用json.loads解析，`text/plain` 直接返回文本
- 使用 `session.read_resource(AnyUrl(uri))` 发送资源请求
- 从 `result.contents[0]` 获取返回的第一个内容元素
- 实现效果：输入@符号时显示文档列表自动完成，选择后自动注入文档内容
- Claude无需调用工具即可直接回答被@提及的文档内容

<details>
<summary>🇨🇳 查看中文翻译</summary>

我们已经在MCP服务器中定义了两个资源，现在客户端需要能够请求这些资源。我们将在MCP客户端中添加一个函数来实现这一点。

打开mcp_client.py文件，找到 `read_resource` 函数。目标是通过向MCP服务器发送请求来读取特定资源，然后根据其mime类型解析返回的内容。

首先在文件顶部添加两个导入：`json` 模块和 `from pydantic import AnyUrl`。

然后实现 `read_resource` 函数：
1. 调用 `result = await self.session.read_resource(AnyUrl(uri))` 获取资源
2. 从 `result.contents[0]` 获取第一个内容元素
3. 检查资源类型和mime类型
4. 如果mime类型是 `application/json`，则使用 `json.loads(resource.text)` 解析并返回
5. 否则直接返回 `resource.text` 作为纯文本

这样客户端就能正确处理两种类型的资源返回——JSON数据（文档列表）和纯文本（文档内容）。

测试：运行 `uv run main.py`，现在输入@符号时会显示可用文档列表，可以用方向键浏览并选择。例如输入"what's in the @report.pdf document"，文档内容会被自动注入到发送给Claude的提示词中，Claude无需使用工具就能直接回答文档内容。

这就是资源的作用——从MCP服务器公开一定量的信息供客户端使用。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

We have defined two separate resources inside of our MCP server. So now our client needs the ability to request these resources. To do so, we're going to add in a single function inside of our MCP client. And remember, this MCP client is going to have some functionality that we're putting together that is going to be used by the rest of our application. And I've already put together that code already. So somewhere else inside this project, something is going to try to make use of this function that we're about to add into the MCP client. To get started, I'm going to open up the MCP client file again. I'm going to scroll down and find read resource right here. So our goal inside of here is to read a particular resource by making a request off to our MCP server and then parse the contents that come back depending upon its mind type and then just return whatever data we get. So you'll notice that a argument to it is the URI. This is going to be the URI of the resource that we want to fetch from the server. In order to make a request, just to get all of our types nicely, we're going to add two imports at the very top of the file. I'm going to add in an import for the JSON module and from PydianTik, I will import any URL. Then I'll go back down to our read resource function. I'm going to clear out the comment and the return statement. Then I'll get a result from calling a wait. Self session, I want to read resource. And then again, this is really just to get the types to work out. We're going to put in a any URL with the input URI. Then I'm going to take from that result. Response or excuse me, result contents at zero. And I want to make this clear right here why we were adding this in. So just a moment ago inside of our inspector, we saw the response we get back. So this is essentially that result variable. Result has a contents list. And there's going to be a list of elements inside there. We really only care about the very first one. So I want to get the first dictionary. I want to access the type property and the mime type. I want specifically the mime type because it's going to help me understand what kind of data we got back. If it is JSON, then I want to make sure I parse the text as JSON and return that result. So let me show you how we're going to do that. I'm going to add in a if is instance. Resource types text resource contents. And inside there, if resource mime type is equal to application JSON. So this is our hint in use. If the server told us that it's giving us back some JSON, we need to make sure that we parse the text content as JSON. So I will return in that case a JSON loads of resource.text. And then otherwise, if we don't fall into that if statement and return early, I want to just return resource.text. So in this scenario, would be returning the text as just plain text, we're not parsing anything. So this would really be the case in which we get back the contents of a single document. All right, so that should really be it. We've got our read resource put together. Now again, I want to remind you, I know I've said this several times, but I just want to remind you because I think it might be a little bit unclear. The code that we're writing inside of the MCP client is being used from several other places inside of this code base. So somewhere else in this code base, we're going to be calling that function that we just put together to get the list of document names and then eventually get the contents of a document to point into a prompt. So at this point, everything should essentially work because the rest of the work has already been done for us. So with that in mind, let's go back over to our terminal and we're going to test out our CLI application again and see if this mention feature works. Okay, so back over here, I'll do a UV run main.py. And now I should be able to say something like what's in the at. And there we go. I see my list of resources and I can use the arrow key to scroll through. Once I am at a resource, I like, I'll just hit space and we'll insert that resource. So what's in the report.pdf document. And now I can tell you that everything is working as expected here. In other words, the contents of this document is being sent off to CLID inside of a prompt. So if I submit this, I should see an immediate response and it's going to tell me what is inside of report.pdf. So this time around, CLID did not have to use a tool to read the contents of the document. All right, so that is resources. Again, we make use of resources to expose some amount of information from our MCP server.

</details>

### 客户端读取资源

```python
# session.list_resources()           — 发现可用资源
# session.read_resource("uri://...")  — 读取资源内容
```

资源支持 URI 模板和参数化。

---

## 第 8 课：定义提示模板

> 📹 视频：Defining Prompts（8 min）


> 🎬 **视频 60**：Defining prompts  
> 📁 文件：[60. Defining prompts.mp4](videos/60.%20Defining%20prompts.mp4)

**核心内容**
介绍MCP服务器的提示词（Prompts）功能，实现一个format命令用于将文档重写为Markdown格式，展示如何定义和测试预制的高质量提示词。

**关键要点**
- 提示词功能允许在MCP服务器中预定义经过优化和评估的高质量提示词
- 提示词的目的：为特定场景提供比用户手动输入更好的结果
- 使用 `@mcp.prompt` 装饰器定义，设置名称和描述
- 函数接收参数（如doc_id），返回消息列表（`base.UserMessage`）
- 提示词中的变量会被自动插值
- 与工具不同，提示词不执行操作，而是返回发送给Claude的消息模板
- 可在MCP Inspector中测试提示词的输出

<details>
<summary>🇨🇳 查看中文翻译</summary>

我们要在MCP服务器中关注的最后一个主要功能是**提示词（Prompts）**。和资源一样，我们将通过在项目中实现一个小功能来理解提示词的用途。

**要实现的功能：斜杠命令**

我们将添加**斜杠命令（slash commands）**支持。例如，输入 `/` 时会列出支持的命令，目前只有一个叫"format"的命令。选择format后，会提示输入文档ID。运行命令后，目标是让Claude使用Markdown语法重新格式化文档。

**为什么需要这个功能？**

这里有一个有趣之处：用户已经可以直接输入"将report.pdf文件用markdown语法重新格式化"，Claude也能合理完成。那为什么还要做这个功能？

核心思路是：如果我们作为MCP服务器的作者，能够坐下来编写、测试和评估一个专门为**特定场景**（将文档转换为Markdown）定制的高质量提示词，用户会获得比自己随便输入更好的结果。

**这就是MCP服务器中提示词功能的真正目标**——提前定义一组经过优化、经过评估、我们知道在各种场景中都能良好工作的高质量提示词，专门针对服务器的专长领域。当然，我们也可以把这些提示词直接写在CLI代码里，但MCP提示词的理念是：你的MCP服务器可能专注于某些特定任务，它可以暴露一些预制提示词供任何客户端应用使用，用户不需要自己从头开发。

**定义提示词语法**

使用 `@mcp.prompt` 装饰器，添加名称和描述（可选）。当客户端请求这个提示词时，我们返回一个消息列表——这些是实际的用户消息和助手消息，客户端可以直接拿来发送给Claude。

**实现 format 提示词**

回到 `mcp_server.py`，找到关于重写文档的注释位置。

```python
@mcp.prompt(name="format", description="rewrites the contents of the document in markdown format")
def format_document(doc_id: str = Field(description="ID of the document to format")):
    prompt = f"""...精心编写的提示词..."""
    return [base.UserMessage(content=prompt)]
```

需要在顶部添加导入：`from mcp.server.fastmcp.prompts import base`。

提示词内容是一段精心编写的文本，要求Claude：获取指定 `doc_id` 文档的内容（隐式地，我们期望Claude使用 read_document 工具），用Markdown语法重写，然后编辑文档保存更新（使用 edit_document 工具）。`doc_id` 变量会被自动插入到提示词中。

函数返回 `[base.UserMessage(content=prompt)]`——一个包含用户消息的列表。

**在MCP Inspector中测试**

运行 `mcp dev mcp_server.py` 启动Inspector。连接服务器后，找到 **Prompts** 部分，列出所有可用提示词——目前只有一个 `format`。点击format，输入文档ID（如 `outlook.pdf`），点击 **Get Prompt**。

可以看到返回的消息列表：一个消息部分（text part），包含完整的提示词，其中文档ID已被正确插入。拿到这些消息后，就可以发送给Claude，期望得到适当的响应。

再次强调，MCP提示词的核心理念是：这些提示词经过充分测试和评估，专门针对一个特定用例，能提供比用户手动输入更好的结果。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Blast Major Focus we're going to have inside of our MCV server is going to be on prompts. Once again, just like we did with resources, we're going to implement a small feature inside of our project. And we're going to use this feature to understand what prompts are all about, just like we did with resources a moment ago. Let me tell you about the feature we're going to add into our program. We're going to add in support for slash commands. So for example, I want to have a format command. I've got some screenshots over here of how it's going to work. Whenever user types into slash, we're going to list out some number of commands that are supported by our application. For right now, we're going to have just one command called format. So if I type in just slash, I should see a little autocomplete right here, and the only autocomplete option should be format. If I then select format, I should be prompted to add in some document ID after it. So one of our different document names like report.pdf or whatever else. Then whenever user runs this command, the goal is to get Claude to reformat this document using markdown syntax. So in other words, take the plain string that we have without any special formatting tied to it inside of each of our documents right now. Remember inside of our MCP server, our current document content is just plain text. We want to feed this into Claude and somehow get Claude to rewrite it using markdown syntax. So I would expect to see some output like this. Something that says I'll help you reformat the document. Claude is then going to use a tool to read the contents of the document. And then finally, inside the final response, I want to see the content of that document rewritten down here in markdown syntax. Now, there's something interesting about this feature that I want to point out. The real core of this feature, like the real goal here, is to allow a user to reformat a document into markdown syntax. And that is an operation that actually doesn't require you and I, the developers, to write out any code to implement. What do I mean by that? Well, a user can already launch our CLI and say something like reformat the report.pedia file in markdown syntax. A user can already do this. Notice what's so ever. And Claude is going to do a reasonable job of it. It's going to take the contents of our document and reformat it into markdown. And as you can see right here, it worked entirely perfectly. So what are we really doing with this feature? Well, the thought process here is that if we just left this up to users and allowed them to manually type in something like convert this to markdown, they might get a okay result, but they might get much better result if they had a really strong prompt that is custom tailored for this particular scenario of converting a document into markdown. So a user might be a lot happier if you and I sat down as the MCP server authors and wrote out and tested and evelled and went through the entire process of developing a really thorough, fantastic prompts like the one you see on the right hand side. So again, just repeat, yes, a user can execute this entire workflow on their own, but if they use this fancy prompt over here, instead, well, I think they would be all the better. This is the real goal of the prompts feature inside of MCP servers. The thought here is that ahead of time, we can define a set of prompts inside of our server that are custom tailored to whatever our server is really specialized to do. In our case, our server is all about managing documents, reading documents, editing documents, and so on. So we might decide to add in a set of prompts that are very high quality that have been evelled and tested and we know that they work in a wide variety of different scenarios. We can then expose these prompts for use inside of any client application, like the CLI app that we are putting together right now. Now, one thing I want to point out here is that we could develop this prompt and just put it directly into our CLI codebase. That is totally possible. We could do that, obviously, but again, the thought here is that your MCP server that might specialize in some particular task might expose some number of prompts that people can just come and use without having to worry about developing them ahead of time. To define a prompt inside of our MCP server, we're going to write out a little bit of syntax very similar to the tools and resources we have already put together. We will use the prompt decorator. We'll add a name to the prompt and optionally a description as well. Then whenever the client asks for this prompt, we'll send back a list of messages. These are actual user and assistant messages so we can take the messages and send them off to CLI directly. All right, so let's go over to our server and we're going to try putting together our own prompt. And just like you see right here, it's going to be all about taking the contents of a document and somehow rewriting it and mark down format. Okay, so back inside my editor, I'm going to find my MCP server file. I'm going to go down a little bit to the comment about rewriting a document and mark down format. I'll delete that to do and then I'll add in a MCP prompt, the name of format, and a description of rewrites the contents of the document in markdown format. I'll then add in an actual implementation. So format document, I'm going to receive as an argument a doc ID and then optionally we can add in a field description here as well, just like we did with our tool earlier on. So I can optionally add in a field with a description of ID of the document to format. And I'm also going to add in a type annotation of string. Just make sure that's really clear as well. From this function, we are going to return a list of messages. I'm going to make sure I add in an import for this base thing at the top right away. So right underneath the existing MCP server import, I will add in from MCP server fast MCP prompts import base. Then back down at the bottom. Inside of here, we're going to define our very well tested, very well evalued prompt. I wrote a prompt out ahead of time. I'm going to paste it in like so. So this prompt is just asking a plot to take in a document ID. Implicitly, we are kind of asking a plot to fetch the document ID's contents using the re-document tool. And then after getting that document, just go ahead and rewrite it with markdown syntax. And finally, after rewriting it, edit the document as well to save those updates inside of our server. Now, after defining this prompt, we're then going to return a list of messages. So down here, I'm going to return a list with base user message. And I'm going to feed in our prompt that we just wrote out to it like so. Now I'm going to save this file. And then let's go start up our MCP development inspector and test out this prompt from that interface. So at my terminal, I'll run that same command again. And then navigate to that address inside my browser. I'll make sure I connect my server. I'll then find the prompts section. I'm going to list out all the different prompts that are available to us. And at this point in time, we have one prompt just format. So I'll click on format and then I have to enter in a document ID right here. Let's this time around maybe we'll put it in a document ID of how about outlook.pdf. So I'll put that in. And then get prompt. And then here is our list of messages. So these have been put together ahead of time. I've got one message part here. So a text part with our full prompt right there. We could see that the document ID was interpolated into it. Now that we have these messages, we can send them off to Clawed. And hopefully we're going to get back some appropriate kind of response. So once again, the entire idea here behind these prompts we might implement inside of our MCP server is that the prompts we are defining are going to be well tested, well e-valed, really specialized to one particular use case.

</details>

### Prompts：预定义的交互模式

```python
@server.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="code_review",
            description="Review code for bugs and best practices",
            arguments=[
                PromptArgument(name="code", description="The code to review", required=True),
                PromptArgument(name="language", description="Programming language", required=False)
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    if name == "code_review":
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Please review this {arguments.get('language', '')} code:\n\n{arguments['code']}"
                    )
                )
            ]
        )
```

---

## 第 9 课：客户端使用提示

> 📹 视频：Prompts in the Client（3 min）


> 🎬 **视频 61**：Prompts in the client  
> 📁 文件：[61. Prompts in the client.mp4](videos/61.%20Prompts%20in%20the%20client.mp4)

**核心内容**
在MCP客户端中实现list_prompts和get_prompt函数，通过斜杠命令在CLI应用中使用服务器定义的提示词。

**关键要点**
- list_prompts函数：通过session获取所有可用提示词列表
- get_prompt函数：通过session获取特定提示词，传入参数进行变量插值
- get_prompt返回的messages可直接传递给Claude
- CLI中输入 `/` 触发斜杠命令，选择命令后选择文档
- 完整流程：用户选择命令→获取提示词→发送给Claude→Claude执行工具→返回格式化结果
- 提示词是用户控制的，由用户决定何时触发

<details>
<summary>🇨🇳 查看中文翻译</summary>

最后一个主要任务是在MCP客户端中实现一些功能，允许我们列出MCP服务器中定义的所有提示词，以及获取特定提示词并插入变量值。

首先实现 `list_prompts`：`result = await self.session.list_prompts()`，然后 `return result.prompts`。

然后实现 `get_prompt`。获取单个提示词时，会传入一些参数。这些参数最终会出现在服务器端的提示词函数中。例如format_document函数期望接收doc_id，args字典中就应该有doc_id键。实现为：`result = await self.session.get_prompt(prompt_name, arguments)`，然后 `return result.messages`。返回的消息构成某种对话，可以直接传递给Claude。

测试：运行项目，输入斜杠符号时会看到format命令。选择format，然后选择一个文档（如plan.md），按回车。整个提示词（用户消息）直接传递给Claude。Claude收到重新格式化文档的指令和文档ID后，首先使用get_document工具获取文档内容，然后用Markdown语法重写文档。

提示词功能回顾：首先编写和评估与MCP服务器用途相关的提示词；然后在MCP服务器中定义提示词；客户端可以随时请求该提示词；请求时传入的参数会作为关键字参数提供给提示词函数；函数可以在提示词中使用这些参数。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Our last major task is to implement some functionality inside of our MCP client and allow us to list out all the different prompts that are defined inside the MCP server and also get a particular prompt with some variables interpolated into it. So let's first implement list prompts. I will delete the comment and replace it with a result is await, self, session, list prompts, and then I will return result.proms. And that's pretty much it. And then get prompt. Now to be clear, when we get a individual prompt, we're going to be given some number of arguments. These arguments will eventually show up inside of our prompt function. So for example, inside a format document right here, we expect to receive a document ID. Inside of this args dictionary, the expectation is that there will be a document ID key and that will be passed in to the appropriate function over here and then we will get that value interpolated into the prompt itself. So inside the get prompt function, I will get a result from self session, get prompt. I'm going to pass in the prompt name. That's the name of the prompt I want to retrieve and then I'll pass in the arguments. And then I will return result.messages. So those are the messages coming back. They form some kind of conversation that we want to feed directly into Claude. And that's it. That's all we have to do for our client. So now we can test this out inside of the CLI itself. I'll flip back over, run the project again. And now if I put in a slash right here, I'll see that I can access this format command. Now format is really just the name of the prompt that we're going to invoke. So if I select that and then hit space, I'll then be asked to select one of the different documents. And you'll go with plan.md. I'll hit enter. And then we're taking that entire prompt, really just that single user message and finiate directly into Claude. So Claude now has the instructions to go and reformat a document into markdown syntax. And it has also been given the ID of the document that we want to reformat. So the first thing it needs to do here is go and fetch that documents contents. And it will do so by using the get document tool. And then finally, Claude is going to respond with the markdown version of this document. So here is the document with a bunch of markdown syntax inside of it. All right, since it looked like this work just fine, let's do a quick recap on prompts and make sure we understand what they are all about. We begin by writing out and e-vailing a prompt that has some relevancy to our mcp server's purpose. In our case, we were making a document server. So having some functionality or something about rewriting a document in a different style, I think it kind of makes sense. Once we have put our prompt together, we'll define a prompt inside the mcp server. And then our client can ask for that prompt at any point in time. When we ask for the prompt, we will put in some number of arguments that will be provided to this prompting function right here as keyword arguments. And then our function can make use of those keyword arguments inside the prompt itself.

</details>

### 将模板实例化为消息

```python
# session.list_prompts()                           — 发现可用提示模板
# session.get_prompt("code_review", {"code": ...}) — 获取实例化的消息
```

---

## 第 10 课：MCP 总结

> 📹 视频：MCP Review（4 min）


> 🎬 **视频 62**：MCP review  
> 📁 文件：[62. MCP review.mp4](videos/62.%20MCP%20review.mp4)

**核心内容**
回顾MCP服务器的三个核心原语——工具、资源和提示词，重点分析每个原语由谁控制以及适用场景。

**关键要点**
- **工具（Tools）**：模型控制——Claude决定何时调用工具，用于扩展Claude的能力
- **资源（Resources）**：应用控制——应用代码决定何时获取数据，用于UI展示或上下文增强
- **提示词（Prompts）**：用户控制——用户通过UI操作或斜杠命令触发，用于预定义工作流
- 三个原语服务于应用的不同层面：模型层、应用层、用户层
- claude.ai界面中可以看到这三种原语的实际应用
- 选择原语的指导：添加能力→工具，获取数据→资源，预定义流程→提示词

<details>
<summary>🇨🇳 查看中文翻译</summary>

项目已经完成，但在继续之前，我想快速回顾我们学习的三个服务器原语：工具（Tools）、资源（Resources）和提示词（Prompts）。我特别想强调每个原语的一个有趣之处——在典型应用中，谁真正负责运行每个原语，谁从中受益。

工具是模型控制的（Model-controlled）。Claude独自决定何时运行给定的工具。

资源是应用控制的（App-controlled）。应用中运行的某些代码决定需要资源提供的数据。在我们的案例中，我们获取资源用于UI中的自动完成选项列表，也获取资源来增强提示词。这些都是由你和我编写的应用相关代码。

提示词是用户控制的（User-controlled）。用户决定何时运行提示词。用户可以通过点击UI元素（如按钮或菜单选项）或使用斜杠命令来启动提示词。

可以在claude.ai的官方界面中看到这些理念的示例。聊天输入框下方的按钮是用户控制的动作（提示词）；Google Drive文档列表是应用相关的（资源）；Claude在回答问题时自动使用JavaScript执行工具是模型控制的（工具）。

总结：
- 如果需要给Claude添加能力 → 使用工具
- 如果需要将数据获取到应用中用于UI展示 → 使用资源
- 如果需要实现某种预定义的工作流程 → 使用提示词

这三个服务器原语各自服务于应用的不同部分：工具服务于模型，资源服务于应用，提示词服务于用户。这些是高级指导原则，帮助你在构建时理解何时使用每个原语。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

We are all done with our project, but before we move on, I want to do a quick recap on the three server primitives that we learned about. So tools, resources, and prompts. In particular, I want to highlight something interesting about each of these, namely what part of an app is really responsible for running each. In other words, in a typical application, who is really running each of these things and who benefits from them? Well, we would say that tools are model-controlled. This means that Clod alone is really responsible for deciding when to run a given tool. Resources are app-controlled. In other words, some code running inside of your app is going to decide that it needs some data provided by a resource. It will be your app's code that decides to execute a resource and use the return data in some way, maybe by using that data in the UI or something like that. In our case, we fetch a resource and then use that data inside the UI to provide a list of autocomplete options. We also fetch a resource to augment a prompt. Both those things were really application-related code that was authored by you and I to put together. And finally, prompts are really user-controlled. So a user decides when a prompt is going to run. A user might start the invocation of a prompt by clicking on some UI element, like a button or a menu option, or they might make use of a slash command, which is what we did. The reason I highlight what is controlling each of these is to give you some idea of their purpose. So if you ever need to add capabilities to Clod, you're probably going to want to look at implementing some tools inside of your MCP server or consuming some servers' tools through your MCP client. If you ever want to get some data into your app for the purposes of showing content in the UI or something similar, then you probably want to use a resource. And if you ever want to implement some kind of predefined workflow, you probably want to look at prompts. Now you can see examples of all these ideas inside of the official Clod interface at claw.ai. So here's what it currently looks like for me. You'll notice that underneath the main chat input are some buttons right here. If I click on one and then click on one of these examples, you'll see that I immediately died into a chat. So this was a user-controlled action. I, as the user, decided to start up this particular workflow, and I'm making use of a prompt that was probably already written ahead of time and probably has been optimized in some way. So to implement that list of buttons right there, we would probably want to put together a series of different prompts inside of the MCP server. Likewise, if I go back and maybe click on this little tab right here at the plus button, you'll notice that I have a add from Google Drive button. Now I'm not going to click on it because it's going to show some of my internal documents, but if I click on that button, I'm going to see some documents that I can add into this chat as some context. Knowing what documents to actually render in that list, and then whenever I click on one, automatically injecting its contents into the context of this chat, that is all application-related code. So it is solely the application that needs to know the list of documents to render here. And that's, again, specifically UI-related elements. So to implement that listing of documents from Google Drive, I would probably look at implementing a resource inside of an MCP server. And then finally, if I enter in a message to this chat of something like what is Squared 3, use JavaScript to calculate the value and send it off, I'm clearly expecting Claw to somehow execute some JavaScript code, which would likely be done through the use of a tool. In this case, the decision to use a tool was 100% model controlled. It is the model that decided to use some JavaScript tool execution. To implement something like this inside of an MCP server, we likely want to, you guessed it, provide a tool. So in total, that's our three different server primitives. And each one is really intended to be used by a different portion of your overall application. So we got tools which are generally going to serve your model, resources, which are generally going to serve your app and prompts which are going to serve your users. And once again, these are high-level guidelines. And the only reason I mentioned them is to just give you a sense of when you should use each of these primitives, depending upon what you are trying to put together.

</details>

### MCP vs 直接工具调用

| 特性 | 直接 Tool Use (API) | MCP |
|------|---------------------|-----|
| 适用场景 | 自定义应用中嵌入 Claude | 标准化工具生态 |
| 工具定义方式 | 每次请求带 `tools` 参数 | Server 端统一注册 |
| 工具执行 | 你自己写代码执行 | Server 端自动执行 |
| 跨模型兼容 | 仅 Claude | 任何支持 MCP 的模型 |
| 额外能力 | 仅工具调用 | 工具 + 资源 + 提示模板 |

**什么时候用哪个？**
- **构建自己的应用** → 用 API Tool Use
- **增强 Claude Desktop/Code 的能力** → 用 MCP
- **构建可复用的工具服务** → 用 MCP Server
- **两者可以共存**

---

## 补充：完整 MCP Server 示例

### Python SDK

```python
# server.py — 天气 MCP Server
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("weather-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a city.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather":
        weather_data = {"city": arguments["city"], "temperature": "22°C", "conditions": "Sunny"}
        return [TextContent(type="text", text=json.dumps(weather_data, indent=2))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 在 Claude Desktop 中配置

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/weather_server.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Documents"]
    }
  }
}
```

### 在 Claude Code 中配置

```bash
claude mcp add weather -- python /path/to/weather_server.py
claude mcp list
claude mcp remove weather
```

---

## 补充：常用 MCP Server

| Server | 功能 | 安装命令 |
|--------|------|---------|
| **Filesystem** | 读写本地文件 | `npx @modelcontextprotocol/server-filesystem` |
| **GitHub** | 操作 GitHub 仓库 | `npx @modelcontextprotocol/server-github` |
| **Brave Search** | 网页搜索 | `npx @modelcontextprotocol/server-brave-search` |
| **PostgreSQL** | PostgreSQL 数据库 | `npx @modelcontextprotocol/server-postgres` |
| **Memory** | 持久化知识图谱 | `npx @modelcontextprotocol/server-memory` |

**发现更多**：[MCP Server 目录](https://github.com/modelcontextprotocol/servers) / [Smithery 社区市场](https://smithery.ai/)

---

## 补充：MCP 安全最佳实践

1. **最小权限原则**：只给 MCP Server 必要的权限
2. **审查 Server 代码**：使用社区 Server 前检查其源码
3. **环境变量管理**：不要在配置文件中硬编码敏感信息
4. **网络隔离**：远程 MCP Server 应使用 HTTPS
5. **日志监控**：在生产环境中记录所有工具调用

---

## 练习题

### 练习 1：搭建 MCP Server

用 Python 构建一个 MCP Server，提供待办事项管理工具（get_todos / add_todo / complete_todo）。

### 练习 2：使用社区 Server

安装 Filesystem 和 GitHub Server，在 Claude Desktop 中测试。

### 练习 3：资源与提示模板

扩展练习 1 的 Server，添加一个 Resource（返回统计信息）和一个 Prompt 模板（生成日报）。

---

## 扩展阅读

| 资源 | 链接 |
|------|------|
| MCP 官方文档 | https://modelcontextprotocol.io/ |
| MCP 规范 | https://github.com/modelcontextprotocol/specification |
| Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk |
| 官方 Server 集合 | https://github.com/modelcontextprotocol/servers |
| Anthropic MCP 文档 | https://docs.anthropic.com/en/docs/agents-and-tools/mcp |

---

> **下一模块**：[05_RAG检索增强生成.md](05_RAG检索增强生成.md) — 学习如何让 Claude 基于你的数据生成精准回答
