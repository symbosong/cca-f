# 模块 6：Claude Code 与 Computer Use

> **对应课程**：Building with the Claude API — Module 6: Claude Code & Computer Use  
> **视频数量**：8 个（约 34 分钟）  
> **预计学习时间**：1-2 小时  
> **难度**：⭐⭐

### 📌 原课程地址

| 平台 | 链接 |
|------|------|
| **Skilljar（官方）** | https://anthropic.skilljar.com/claude-with-the-anthropic-api |
| **Coursera（镜像）** | https://www.coursera.org/learn/building-with-the-claude-api |

### 📌 视频课时清单

| # | 视频标题 | 时长 | 核心知识点 |
|:-:|---------|:----:|-----------|
| 1 | Anthropic Applications | 1m | Anthropic 产品矩阵概览 |
| 2 | Claude Code Setup | 2m | 安装配置、首次运行 |
| 3 | Claude Code in Action | 10m | 核心演示：代码理解、生成、重构、调试 |
| 4 | Enhancements with MCP Servers | 3m | 给 Claude Code 接入 MCP 服务器扩展能力 |
| 5 | Parallelizing Claude Code | 8m | 并行子代理、同时执行多个任务 |
| 6 | Automated Debugging | 4m | 自动调试：读取错误→分析→修复→验证 |
| 7 | Computer Use | 3m | Computer Use 概念：像人一样操作桌面 |
| 8 | How to Use Computer Use | 3m | 工作原理：截图→坐标→动作循环 |

> **阅读材料**（2 篇，10 分钟）：Module Introduction / Next Steps

---

## 本模块学习目标

完成本模块后，你将能够：
1. 理解 Claude Code 是什么以及它的核心能力
2. 安装和配置 Claude Code
3. 掌握 Claude Code 的日常工作流
4. 了解 CLAUDE.md 配置文件系统
5. 使用 Hooks 自定义 Claude Code 的行为
6. 理解 Computer Use（桌面操控）的概念和应用

---

## 第 1 课：Anthropic 产品矩阵

> 📹 视频：Anthropic Applications（1 min）


> 🎬 **视频 63**：Anthropic apps  
> 📁 文件：[63. Anthropic apps.mp4](videos/63.%20Anthropic%20apps.mp4)

## 核心内容
本视频介绍了Anthropic构建的两个重要应用——Claude Code和Computer Use，并说明它们是理解Agent概念的完美入口。

## 关键要点
- **Claude Code**：基于终端的编程助手，后续将详细演示设置和使用
- **Computer Use**：一组工具，能极大扩展Claude的能力
- **与Agent的关系**：这两个应用是Agent的典型示例，理解它们有助于学习Agent的构建方法
- 本模块将从Claude Code的设置开始

<details>
<summary>🇨🇳 查看中文翻译</summary>

在本模块中，我们将了解Anthropic构建和部署的两个应用程序：Claude Code和Computer Use。

Claude Code是一个基于终端的编程助手。我将带你完成设置过程，然后我们会在一个非常小的示例项目上使用Claude Code，以理解它的工作原理。

之后，我们将了解Computer Use。Computer Use是一组工具，能够极大地扩展Claude的能力。

Claude Code和Computer Use本身都非常有用，但我们讨论它们还有另一个原因。Claude Code和Computer Use是Agent的完美示例。一旦我们理解了它们的工作方式，我们就能更好地准备理解什么是Agent以及如何构建有效的Agent。

那么让我们在下一个视频中开始Claude Code的设置过程吧。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

In this module, we're going to take a look at two applications that have been built and deployed by Anthropic. They are Claude Code and Computer Use. Claude Code is a terminal-based coding assistant. I'm going to help you go through the setup process and then we're going to use Claude Code on a very small sample project to understand exactly how it works. After that, we're going to take a look at Computer Use. Computer Use is a set of tools that dramatically expands Claude's capabilities. Both Claude Code and Computer Use are extremely useful in their own right, but there's another reason that we're going to discuss them. You see, Claude Code and Computer Use are perfect examples of agents. And once we understand how they work, we'll be much better prepared to understand what agents are and how to build an effective agent. So let's go through the setup process of Claude Code in the next video.

</details>

Anthropic 产品概览：
- **Claude.ai** — 对话界面
- **Claude Code** — 命令行 AI 编程助手
- **Claude API** — 开发者接口
- **Computer Use** — 桌面操控

---

## 第 2 课：Claude Code 安装配置

> 📹 视频：Claude Code Setup（2 min）


> 🎬 **视频 64**：Claude Code setup  
> 📁 文件：[64. Claude Code setup.mp4](videos/64.%20Claude%20Code%20setup.mp4)

## 核心内容
本视频介绍Claude Code的基本概念和安装设置过程。

## 关键要点
- **Claude Code定义**：基于终端的编程助手程序，可帮助完成各种代码相关任务
- **内置工具**：包括文件搜索/读取/编辑等基本工具，以及网页抓取和终端访问等高级工具
- **MCP客户端**：Claude Code内置MCP客户端，可通过添加MCP服务器扩展功能
- **安装步骤**：1）安装Node.js → 2）npm install安装Claude Code → 3）运行`claude`命令并登录Anthropic账户
- **官方文档**：完整设置指南位于docs.anthropic.com

<details>
<summary>🇨🇳 查看中文翻译</summary>

让我们来看看Claude Code。我们将完成一些设置，了解它的工作原理，并看一些高级用例。

Claude Code是一个基于终端的编程助手。这是一个运行在你终端中的程序，可以帮助完成各种与代码相关的任务。

为了帮助你完成编程项目，Claude Code可以访问许多不同的工具。它拥有许多基本工具，比如搜索、读取和编辑文件的能力。但它也有许多高级工具，如网页抓取和终端访问。最后，Claude Code可以作为MCP客户端。你知道这意味着什么——它可以消费MCP服务器提供的工具。因此，我们可以通过添加额外的MCP服务器来轻松扩展Claude Code的能力。

现在让我们完成一些设置，将Claude Code安装到你的机器上。设置很简单：

1. 首先安装Node.js。你的机器上可能已经安装了Node。要确认是否已安装，打开终端并执行命令`npm help`。如果看到返回结果，说明你可能已经安装了Node。
2. 安装Node后，执行npm install命令来安装Claude Code本身。
3. 安装完成后，在终端运行`claude`命令。这将提示你登录Anthropic账户。

完整的设置指南可以在Anthropic官方文档docs.anthropic.com上找到。

我将让你自行完成这个设置过程——就是这三个步骤。完成后，我们将一起进行一个小项目，看看Claude Code真正能为我们做什么。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

Let's take a look at Claude Code. We'll do some setup, learn how it works, and see some advanced use cases. Claude Code is a terminal-based coding assistant. This is a program running in your terminal that can help with a wide variety of code-related tasks. To help you with coding projects, Claude Code has access to many different tools. So it has many basic tools like the ability to search, read, and edit files. But it also has many advanced tools, like web fetching and terminal access. Finally, Claude Code can act as an MCP client. And you know what that means. It means it can consume tools that are provided by MCP servers. So we can easily expand the capabilities of Claude Code by adding in some additional MCP servers. Let's now go through a little bit of setup and install a Claude Code on your machine. Setup is easy. We're going to first install a copy of Node.js. You might already have Node installed on your machine. And to figure out whether or not you do, open up your terminal and execute the command NPM help. If you see a result come back, that means you probably already have Node installed. Once you have Node installed, you'll do a NPM install command that will install Claude Code itself. Once installation is complete, run the command Cloud at your terminal. This will prompt you to log into your Anthropic account. Now a full setup guide can be found at the official Anthropic documentation at docsanthropic.com. Now I'm going to let you go through this setup process on your own, again, just these three steps right here. As soon as you are done, we're going to walk through a little project together and see what Claude Code can really do for us.

</details>

```bash
# 安装 Claude Code（需要 Node.js 18+）
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version

# 在项目目录中启动
cd /path/to/your/project
claude

# 常用启动选项
claude --model claude-sonnet-4-20250514  # 指定模型
claude --verbose                         # 详细输出
```

---

## 第 3 课：Claude Code 实战演示

> 📹 视频：Claude Code in Action（10 min）


> 🎬 **视频 65**：Claude Code in action  
> 📁 文件：[65. Claude Code in action.mp4](videos/65.%20Claude%20Code%20in%20action.mp4)

## 核心内容
通过实际项目演示Claude Code的使用方式，展示项目设置、init命令、Git集成以及两种高效编码工作流。

## 关键要点
- **核心理念**：将Claude Code视为团队中的另一位工程师，而非简单的代码生成器
- **init命令**：自动扫描代码库，生成CLAUDE.md文件作为后续交互的上下文
- **三种CLAUDE文件**：项目级（project）、本地级（local）、用户级（user）
- **工作流一（分析-规划-实现）**：先让Claude读取相关文件 → 规划方案 → 最后实现
- **工作流二（测试驱动开发）**：先设计测试 → 实现测试 → 编写代码使测试通过
- **效果倍增器**：在指令上多花心思，可以显著提升Claude的输出质量
- **Git集成**：Claude可以自动暂存、编写提交信息并提交代码变更

<details>
<summary>🇨🇳 查看中文翻译</summary>

为了让你获得一些Claude Code的实际操作经验，我创建了一个小项目供我们一起练习。你可以在本课程的附件中找到这个项目的压缩包。我建议你下载这个zip文件，解压内容，然后在新的项目目录中启动代码编辑器。

我已经在编辑器中打开了这个项目。打开项目后，你可能想浏览项目内容或按照ReadMe文件中的说明进行一些设置。但在此之前，有一件重要的事情我想让你了解：

**Claude Code不仅仅是一个为你写代码的工具。** 它当然可以写代码，但这不是Claude Code的全部意义。你真正应该把Claude Code看作是另一个与你一起工作的工程师。你在普通项目中需要完成的每一项任务，都可以完全委托给Claude，包括从项目初始设置、设计新功能、部署到技术支持的全过程。

在本项目中，我们将大量利用Claude来帮助我们完成各种步骤：使用Claude设置项目、规划新功能、编写测试和代码。稍后，在一个稍有不同的项目中，我还会展示如何使用Claude Code自动发现和修复生产环境中的错误。

**项目设置：**
在终端中启动Claude Code，然后让Claude读取ReadMe文件的内容并执行其中列出的设置步骤。Claude会使用各种工具来读取文件，然后执行一系列命令：创建虚拟环境、激活环境并安装依赖。

**init命令：**
完成设置后，我们运行`init`命令。执行此命令时，Claude会自动扫描你的代码库以了解项目的整体架构、编码风格等。完成后，Claude会将所有发现写入一个名为`CLAUDE.md`的特殊文件。将来再运行Claude时，这个文件会自动作为上下文被包含进去。

有三种不同的CLAUDE文件：项目级（project）、本地级（local）和用户级（user）。

运行init命令时，你还可以添加特殊指示，让Claude关注某些特定领域。例如，我让Claude包含关于定义MCP工具的详细说明。生成的CLAUDE.md文件包含了对代码库的总结：顶部列出了可能需要运行的重要命令，还有编码风格信息，以及我特别请求的MCP工具定义信息。

项目会随时间变化。如果编码风格改变或添加了新命令，我们可以手动编辑这个文件，或重新运行init命令来更新。我们还可以用`#`加注释的方式快速追加特定说明到文件中。例如添加"始终为函数参数应用适当的类型"——这将被追加到CLAUDE.md中，影响所有后续请求。

**Git集成：**
项目由Git管理。与其手动暂存和提交文件，我们可以直接让Claude完成。Claude会查看所有代码变更，编写描述性的提交信息并提交文件。

**提高Claude编码效率的技巧：**

我们要为项目添加一个新功能——一个读取Word文档或PDF文件并将内容转换为Markdown的工具。

**工作流一：分析-规划-实现**
1. 识别代码库中与功能相关的文件，让Claude先读取并分析这些文件
2. 告诉Claude要构建的功能，要求它规划解决方案（暂不写代码）
3. 审核计划后，让Claude实际实现方案

对于我们的功能，我让Claude先阅读tools目录中的math.py（现有工具示例）和document.py（包含有用的转换函数）。然后让Claude规划实现方案。最后让Claude实现计划——它更新了Document.py文件、main.py文件，并编写了测试用例，还自动添加了不存在文件或不支持文件类型的错误处理。

**工作流二：测试驱动开发**
1. 让Claude读取相关上下文
2. 在写任何代码之前，让Claude先设计相关测试
3. 选择最相关的测试，让Claude实现它们
4. 测试就绪后，让Claude编写代码直到所有测试通过

对于同一功能，我先运行`/clear`命令清除对话历史，然后让Claude重新阅读相关文件，接着让Claude思考可以编写的测试（暂不写代码）。建议非常好，我选择了测试1-5让Claude实现，然后让Claude编写代码使测试通过。所有测试都通过了。

请记住：Claude Code是一个**效果倍增器**。你可以给出简单指令，Claude会尽力而为，但如果你在指令上多花一点心思，可以显著提升Claude的效果。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

To get you some hands-on experience with Clod Code, I created a small project for us to work on. You should find the source for this project in a zip file attached to this lecture. I would encourage you to download this zip, extract its contents, and then start up your code editor inside of this new project directory. I've already opened up the project inside of my editor. Now once you have the project open, you might be tempted to look through the project contents and maybe go through a little bit of setup, which is described inside the ReadMe file. But before you do, there's something important I would like you to understand about Clod Code. Clod Code is not a tool that is just going to write code for you. Naturally, it absolutely can, but that's not the only thing that Clod Code is about. Instead, you really want to view Clod Code as another engineer who's working on this project alongside you. Every task that you would normally go through on a normal project can really be fully delegated off to Clod. So this includes everything from initially setting up a project to designing new features, to deployment, and to support. As we go through this project, we're going to leverage Clod heavily to aid us in various steps. We will use Clod to set up the project for us, to plan out a new feature, to write tests and code, and then later on, on a slightly different project, I'll show you how we can use Clod Code to automatically discover and fix errors in a production environment. So let's get to it. Back inside my editor, I'm going to open up my terminal, and then launch Clod Code inside there by executing Clod. Then, once I have this open, I'm going to put in my first directive to Clod. I'm going to ask it to read the contents of the ReadMe file, and go through any setup directions that are listed inside of here. I will ask Clod to read the contents of the ReadMe file, and execute these setup directions listed in it. Clod will then use a variety of different tools to read that file, and then execute a series of different commands. It will create a new virtual environment, activate the environment, and install some dependencies. Once that is complete, we are going to run a command that will help Clod get a better understanding of our project. We're going to do so by running the init command. This is a command that we're going to execute inside of Clod Code itself. When you execute this command, Clod will automatically scan your codebase to understand your project's general architecture, coding style, and so on. Once complete, Clod will write all of its findings into a special file named Clod.MD. Whenever we run Clod again in the future, this file will be automatically included as context. Just so you know, there are three different Clod files, project, local, and user. We're going to see some references to these in a minute, so we'll discuss what they're all about then. Whenever you run this init command, you can also actually add in some special directions for some areas for Clod to focus on. So let's try this out right now and see what is generated for our project. I'm going to run the init command, and when I do, I'm going to pass in some special instructions. I'm going to ask Clod to include some detailed notes on defining MCP tools. Once it is all done, I'm going to take a look at the newly generated Clod.MD file. So this is a summary of what Clod thinks of our codebase. At the top, it will list out some important commands that it might need to run in the future. We'll get some listing around our coding style that we've used inside this project. And then as I specially requested, it also included some information around defining MCP tools. As I mentioned a moment ago, this file is going to be included as context for Clod in any follow-up request we make in the future. Now, projects change over time. We might change our coding style or add in some additional commands. So if that ever happens, we can very easily manually edit this file, or we can choose to rerun the init command. If you rerun this command, Clod will update the contents of the Clod MD file. Finally, as a very small shortcut, we can put in a Pound, and then type in some specific note that we want to be appended into the contents of that file. So we can use this as a tool to give very specific small directions to Clod. They will be included in all follow-up requests. So for me, I might add in a direction here that says something like, always apply appropriate types to function arcs. And if I run that, I'll then be asked where I want to add this little note. This is where we see that project memory, local memory, and user memory appear. In my case, this is a note that I want to be shared with everyone who is working on this project. So I will add it to project memory. Once I add that in, I can then check the contents of my Clod.MD file. And either somewhere under Code Style or perhaps at the very bottom, I'll probably see whatever note I just added in. At this point, we have added a new file to our project. And this project is being managed by Git. So normally, we would open up our terminal, stage this new file that we just created into Git, and then commit those changes. We could do all that manually, but it would be a lot faster if we just asked Clod to do it for us. So I will ask Clod to stage and commit all changes. Clod will then take a look at all the different changes we have made to the code base, write a descriptive commit message, and commit those files. Next up, I would like to show you some techniques for increasing Clod's effectiveness when writing code. We are going to add a new feature into this project. As a reminder, this project is a very small, very simple MCP server. We are going to ask Clod to add in a new tool to the server that will read a Word document or a PDF file and convert the contents to Markdown. Now, we absolutely could just type in directions for that to Clod, something like make a Word Doc plus PDF file to Markdown Conversion tool. But before doing that, I want you to know that we can dramatically increase the effectiveness of Clod by putting in a little bit more effort. So let me show you how. Think of Clod Code as being an effort multiplier. If you put a little effort into how you direct Clod, you will get back significantly better results. I'm going to show you two different workflows, two different ways of instructing Clod on how to approach a task. Both of these workflows require a little bit of effort on your side, but they allow Clod to tackle much more complex problems. In this first workflow, we're going to go through three distinct steps. First, we're going to identify some areas of our code base that we know are relevant to a feature that we are trying to work on. We're then going to ask Clod to specifically read and analyze those files. Second, we're going to tell Clod about the feature we want to build and ask it to plan out a solution. So the steps will actually go through to implement whatever feature or problem you're trying to solve. And then finally, after Clod has gone through that planning step, we will ask Clod to actually implement these solution. Let me show you how we would do this for our particular feature of adding in some new document conversion tool. So first, I'm going to go through my code base and identify some different relevant files. You'll notice there is a tools directory and inside there is a math.py file. This is an example of a tool that has already been put together. So this might be some file that is relevant for the feature that we are trying to build, just because it gives Clod a better idea of how to author a tool. Second, we might ask Clod to take a look at the document.py file, which includes a very helpful function, binary document to mark down. So this will take in some amount of binary data and convert it to Markdown. So we can tell Clod to take a look at these files and Clod will get a better idea of how to write a tool in the first place and then how to actually do the conversion. So I'm going to add in some instructions to Clod and ask it to just read the contents of those files. Next, I'm going to ask Clod to plan out the implementation of a new tool called Document Path to Markdown, which will take in a path to a PDF or Word document, read the file, convert the contents to Markdown, and return the results. I'm also going to tell Clod specifically to just plan the feature out and not to write any code just yet. In response, Clod is going to give us a pretty well detailed plan that's going to go through a couple of different steps that will be required to implement this entire thing. Finally, I will ask Clod to implement this plan. It's first going to update the Document.py file, which is definitely correct. It's then going to update the main.py file, which is also good, and then finally, it will author a test around this new tool. It's then going to run the test suite and make sure that the test actually passes. You'll notice that in the summary message, Clod also tells me that added in some air handling for non-existent or unsupported file types, which was definitely appropriate, even though it wasn't something that I actually asked for explicitly inside of my description of this feature. I'd like to show you another way that we could have asked Clod to implement this feature. Before I show you this alternative, I'm going to get Clod to remove all the code that it just wrote by stashing these changes. Now I am back to a clean slate where I don't have anything related to that new feature that was just implemented. The second technique that we are going to explore is a test-driven development workflow. Again, this requires some more effort from you up front, but it dramatically increases Clod's effectiveness. With this workflow, we will again ask Clod to take a look at some relevant context. Then, before writing any code, we're going to ask Clod to think of some different tests it could write related to our feature. Next, we will select the most relevant tests and ask Clod to implement them. Finally, after we have got some working tests put together, we will ask Clod to write out a solution and write code until the tests actually pass. So let me show you how this approach would actually look for the same exact feature, one where we are building a tool that's going to read a document off of our hard drive and convert contents into Markdown. First, I'm going to run the slash clear command. This is going to clear up my conversation history with Clod, essentially reset its context. In this case, I'm doing this just so it doesn't cheat off its previous solution. Then I will ask Clod to read those two relevant files once again. Then, I'm going to add in some very clear instructions to think of some tests that it might write to evaluate this new feature that we want to build. Again, I'm going to ask it specifically to not write any code just yet. The suggestions I get back are really solid. Now, I don't really want to have to worry about tests 6, 7, and 8 because those are a little bit more specialized beyond what we're doing right now. So I'm going to ask Clod to just implement tests 1 through 5. Now we will move on to the last step where we will ask Clod to write out some code to make these tests pass. Very good, all the tests pass. Now, before we move on, I just want to remind you one more time that Clod code really is an effort multiplier. You can put in very simple directions and Clod will do its best, but you can dramatically increase Clod's effectiveness by putting in a little bit of effort on your side as well.

</details>

### 核心能力

- 🔍 **理解代码库**：浏览文件、搜索代码、理解项目结构
- ✏️ **编辑代码**：直接创建、修改、删除文件
- 🖥️ **执行命令**：运行 shell 命令、测试、构建
- 🔄 **Git 操作**：提交、创建 PR、解决冲突

### 日常使用场景

```bash
claude "这个项目的架构是什么？"
claude "给 User 模型添加一个邮箱验证功能"
claude "这个测试失败了，帮我修复"
claude "审查 src/auth/ 目录下的代码，关注安全问题"
claude "提交当前更改，写一个好的 commit message"
```

### 斜杠命令

| 命令 | 功能 |
|------|------|
| `/help` | 查看帮助 |
| `/clear` | 清除对话上下文 |
| `/compact` | 压缩对话历史 |
| `/model` | 切换模型 |
| `/cost` | 查看 token 费用 |
| `/mcp` | 管理 MCP Server |

---

## 第 4 课：MCP 增强

> 📹 视频：Enhancements with MCP Servers（3 min）


> 🎬 **视频 66**：Enhancements with MCP servers  
> 📁 文件：[66. Enhancements with MCP servers.mp4](videos/66.%20Enhancements%20with%20MCP%20servers.mp4)

## 核心内容
演示如何通过MCP服务器扩展Claude Code的功能，将自定义工具集成到Claude Code中。

## 关键要点
- **内嵌MCP客户端**：Claude Code内置MCP客户端，可连接MCP服务器扩展能力
- **添加MCP服务器**：使用`claude mcp add <名称> <启动命令>`命令
- **实际演示**：将自定义的文档转换MCP服务器连接到Claude Code，成功读取PDF/Word文档
- **实用集成场景**：
  - Sentry：获取生产环境错误详情
  - Jira：查看工单内容
  - Slack：任务完成时发送通知
- **核心价值**：MCP集成为Claude Code提供了极大的灵活性和可扩展性

<details>
<summary>🇨🇳 查看中文翻译</summary>

在这个视频中，我想向你展示Claude Code最有趣的一个方面：Claude Code内嵌了一个MCP客户端。这意味着我们可以将MCP服务器连接到Claude Code，从而极大地扩展其功能。

为了演示这一点，我们将把Claude Code连接到我们一直在开发的MCP服务器。我们刚刚编写了一个名为"Document Path to Markdown"的工具。现在我们可以将这个工具暴露给Claude Code，使其能够读取PDF和Word文档的内容。这样我们就在动态扩展Claude Code的能力。

让我展示如何设置。回到终端中，我先用Ctrl+C结束当前运行的会话。然后通过执行以下命令添加MCP服务器：

```
claude mcp add documents uv run main.py
```

其中"documents"是我们给服务器起的名字（可以是任何名称），`uv run main.py`是启动服务器的命令。

执行完成后，重新启动Claude Code。现在我们可以使用刚才编写的工具了。

在测试目录中，有一个fixtures文件夹，里面有两个示例文件——一个Word文档和一个PDF文档，都包含了关于MCP的简短文档。我让Claude将其中一个文件转换为Markdown。Claude果然使用了我们刚编写的工具，成功提取了文件内容。

这种消费MCP服务器的能力为Claude Code增添了令人难以置信的灵活性，也打开了许多有趣的开发可能：

- 如果你使用**Sentry**进行生产监控，可以添加Sentry MCP服务器让Claude获取生产环境的错误详情
- 如果你使用**Jira**，可以添加MCP服务器让Claude查看特定工单内容
- 如果你使用**Slack**，可以添加Slack让Claude在完成某个问题时通知你

这些只是Claude Code可能增强的一小部分。值得你花时间思考如何增强你自己的特定开发工作流。

</details>

<details>
<summary>📜 查看视频转录原文</summary>

In this video, I want to show you one of the most interesting aspects of Clawed Code. Clawed Code has an MCP client embedded inside of it. That means we can connect MCP servers to Clawed Code and dramatically expand its functionality. To demonstrate this, we are going to connect Clawed Code to the MCP server that we have been working on. We just authored a tool called Document Path to Markdown. We can now expose this tool to Clawed Code, allowing it to read the contents of PDF and Word documents. So we are dynamically expanding the capabilities of Clawed Code. Let me show you how to set this up. Back inside of my terminal, I'm going to end my running session with a Control-C. I'm then going to add in an MCP server to Clawed Code by executing Clawed, MCP, Add, then we're going to put in the name for our MCP server. Now the name can be anything you want it to be. In our case, we are making a server related to documents, so I'm going to call our server documents. And then finally, we're going to put in the command that we used to start up our server, which for us is uvrunmay.py. So uvrunmay.py. And that's it. I'm going to execute that, and I'll start Clawed Code back up with Clawed. And now we can make use of that tool that we just put together. To really test it out inside of our test directory, there's a Fixers folder. Inside there are two demo files, so a WordDoc and a PDFDoc. Both contain just a tiny bit of documentation around MCP itself. So I'm now going to ask Clawed to convert the contents of either one of those files into Markdown. And my expectation is that Clawed will make use of that tool that we just authored a moment ago. And if we scroll up just a little bit here, sure enough it worked. So this actually is the contents of that file. This ability to consume MCP servers adds an incredible amount of flexibility to Clawed Code, and really opens the door to some really interesting development opportunities. For example, you might decide to add in a series of MCP servers related to your particular development flow. For example, if you use Sentry for Production Monitoring, you can add a Sentry MCP server to allow Clawed to fetch details about errors that are occurring in production. If you make use of Gira, you can add in an MCP server that will allow Clawed to view the contents of specific tickets. If you're a Slack user, you can add Slack to message you whenever Clawed is completed working on some particular problem. These are just a small fraction of the possible enhancements that you can add into Clawed Code. So it would definitely worth your time to think about how you can enhance your particular development workflow.

</details>

### 给 Claude Code 接入 MCP 服务器

```bash
claude mcp add github -- npx -y @modelcontextprotocol/server-github
claude mcp add db -- npx -y @modelcontextprotocol/server-postgres postgresql://...
claude mcp list
```

接入后 Claude Code 可以直接查询数据库、操作 GitHub 等。

---

## 第 5 课：并行子代理

> 📹 视频：Parallelizing Claude Code（8 min）

### 让 Claude Code 同时执行多个任务

子代理（sub-agents）概念：Claude Code 可以启动多个并行任务分别处理不同问题，然后汇总结果。显著提升处理复杂任务的效率。

---

## 第 6 课：自动调试

> 📹 视频：Automated Debugging（4 min）

### Claude Code 的自动调试循环

```
读取错误信息 → 分析原因 → 自动修复代码 → 运行测试验证 → 如仍失败则继续迭代
```

---

## 第 7 课：Computer Use 概念

> 📹 视频：Computer Use（3 min）

### 什么是 Computer Use？

Computer Use 让 Claude 通过**截屏 + 鼠标/键盘操作**来控制桌面应用——就像远程控制一样。

```
用户请求 → Claude 截屏查看桌面 → 决定操作 → 点击/输入 → 再截屏验证 → 继续...
```

---

## 第 8 课：Computer Use 工作原理

> 📹 视频：How to Use Computer Use（3 min）

### 核心工具

| 工具 | 功能 |
|------|------|
| `computer` | 截屏、移动鼠标、点击、输入文字、滚动 |
| `text_editor` | 查看和编辑文件 |
| `bash` | 执行 bash 命令 |

### API 示例

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=[
        {
            "type": "computer_20250124",
            "name": "computer",
            "display_width_px": 1920,
            "display_height_px": 1080,
            "display_number": 0
        },
        {"type": "bash_20250124", "name": "bash"},
        {"type": "text_editor_20250124", "name": "text_editor"}
    ],
    messages=[{
        "role": "user",
        "content": "Open Firefox and search for 'Claude AI' on Google."
    }]
)
```

### 安全考虑

> ⚠️ **Computer Use 仍处于 Beta 阶段**：

1. **在沙箱环境运行**：使用虚拟机或 Docker 容器
2. **限制网络访问**：避免 Claude 访问敏感系统
3. **人工监督**：始终监控 Claude 的操作
4. **避免敏感信息**：不要在可见屏幕上显示密码

```bash
# 推荐：使用 Docker 运行（官方 Demo）
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your-key \
  ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo
```

---

## 补充：CLAUDE.md 配置系统

CLAUDE.md 是 Claude Code 的"项目记忆"。

### 三级配置层次

```
优先级从高到低：
1. ~/.claude/CLAUDE.md          ← 全局配置
2. /project/CLAUDE.md            ← 项目级
3. /project/src/CLAUDE.md        ← 模块级
```

### CLAUDE.md 示例

```markdown
# Project: E-commerce API

## Tech Stack
- Python 3.11 + FastAPI
- PostgreSQL 15 with SQLAlchemy 2.0

## Code Conventions
- Use type hints everywhere
- All database queries must use parameterized queries

## Testing
- Run tests: `pytest tests/ -v`
- Minimum coverage: 80%
```

---

## 补充：Hooks 系统

Hooks 在 Claude Code 的关键节点插入自定义逻辑：

| Hook | 触发时机 | 用途 |
|------|---------|------|
| `PreToolUse` | 工具执行前 | 审批、拦截危险操作 |
| `PostToolUse` | 工具执行后 | 日志、自动格式化 |
| `Notification` | 发出通知时 | 自定义通知方式 |
| `Stop` | 停止时 | 自动运行测试 |

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "write_file",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $CLAUDE_FILE_PATH 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

---

## 补充：CI/CD 集成

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code
      - name: Run AI Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --print "Review the changes in this PR." < <(git diff origin/main...HEAD)
```

---

## 练习题

### 练习 1：Claude Code 上手

安装 Claude Code，创建 CLAUDE.md，用它完成一个小功能。

### 练习 2：Hooks 配置

配置 PostToolUse Hook 自动格式化代码 + Stop Hook 自动运行测试。

### 练习 3：了解 Computer Use

运行官方 Computer Use Demo 容器，体验 Claude 操控桌面。

---

## 扩展阅读

| 资源 | 链接 |
|------|------|
| Claude Code 官方文档 | https://docs.anthropic.com/en/docs/claude-code |
| Claude Code GitHub | https://github.com/anthropics/claude-code |
| Claude Code Hooks | https://docs.anthropic.com/en/docs/claude-code/hooks |
| CLAUDE.md 配置 | https://docs.anthropic.com/en/docs/claude-code/memory |
| Computer Use 文档 | https://docs.anthropic.com/en/docs/build-with-claude/computer-use |

---

> **下一模块**：[07_Agent工作流与智能体.md](07_Agent工作流与智能体.md) — 学习 Agent 循环和工作流模式
