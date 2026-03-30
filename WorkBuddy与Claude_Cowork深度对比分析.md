# WorkBuddy vs Claude Cowork — 深度对比分析报告

> **版本**：v1.0 — 2026年3月30日  
> **资料来源**：Anthropic 官方产品页、腾讯 CodeBuddy 官方文档、Fello AI 完整指南、Substack 高级用户测试、Collabnix 技术分析、知乎 / CSDN 社区实测  
> **适用读者**：需要选型的产品经理、技术负责人、办公效率探索者

---

## 目录

- [第一部分：全局概览](#第一部分全局概览)
- [第二部分：产品定位与设计哲学](#第二部分产品定位与设计哲学)
- [第三部分：技术架构深度解析](#第三部分技术架构深度解析)
- [第四部分：工作模式详解](#第四部分工作模式详解)
- [第五部分：文件操作能力对比](#第五部分文件操作能力对比)
- [第六部分：技能系统与插件生态](#第六部分技能系统与插件生态)
- [第七部分：多智能体与协作机制](#第七部分多智能体与协作机制)
- [第八部分：平台集成与连接器](#第八部分平台集成与连接器)
- [第九部分：典型场景对比](#第九部分典型场景对比)
- [第十部分：安全机制深度对比](#第十部分安全机制深度对比)
- [第十一部分：平台支持与环境要求](#第十一部分平台支持与环境要求)
- [第十二部分：定价模型对比](#第十二部分定价模型对比)
- [第十三部分：产品发展时间线](#第十三部分产品发展时间线)
- [第十四部分：高级功能深度拆解](#第十四部分高级功能深度拆解)
- [第十五部分：真实用户反馈与踩坑经验](#第十五部分真实用户反馈与踩坑经验)
- [第十六部分：最佳实践与使用技巧](#第十六部分最佳实践与使用技巧)
- [第十七部分：选型决策指南](#第十七部分选型决策指南)

---

# 第一部分：全局概览

## 1.1 两款产品的核心数据一览

| 维度 | 🟢 WorkBuddy（腾讯） | 🟣 Claude Cowork（Anthropic） |
|------|----------------------|------------------------------|
| **发布时间** | 2026.1.19 内测 → 2026.3.9 公测 | 2026.1.12 Research Preview |
| **一句话定位** | AI 原生桌面智能体工作台——"一句话让 AI 替你上班" | 给非程序员用的 Claude Code——"你的第一位 AI 同事" |
| **底层来源** | 基于 CodeBuddy 引擎，兼容 OpenClaw 技能生态 | 底层即 Claude Code 引擎（由 Claude Code 1.5 周内自行编写） |
| **目标用户** | 全角色职场人——运营、行政、销售、产品、创作者 | 非技术知识工作者——白领、法务、行政、营销 |
| **操作系统** | ✅ macOS + Windows（同时支持） | ✅ macOS + Windows（2026.2 新增 Win） |
| **核心模型** | 多模型可切换（混元、DeepSeek 等 5+） | Claude Opus 4.6（单一模型，1M token 上下文） |
| **IM 联动** | ✅ 微信 / 企微 / 飞书 / 钉钉 / QQ | ⚠️ 手机端 ↔ 桌面端同步（2026.3.17 Dispatch 更新） |
| **三方连接器** | MCP Server 内置 + Skills 扩展 | Google Drive / Slack / Notion / Salesforce 等 30+ 连接器 |
| **计划任务** | 通过 IM 指令远程触发 | ✅ `/schedule` Cron 定时任务（2026.2.25） |
| **定价** | 免费体验补贴 + Token 计费 | Pro $20/月（有限）→ Max $100-200/月 |
| **数据隐私** | 本地运行，数据不上云 | 本地沙盒隔离，对话历史存本地（推理在 Anthropic 云端） |
| **多智能体** | ✅ 多 Agent 并行 | ✅ 子代理(Sub-agent)并行协作 |
| **Computer Use** | ❌ 不支持 | ✅ 2026.3.23 上线（屏幕控制 + 应用操作） |
| **记忆功能** | 私有化本地知识库 | 跨会话记忆 + `.cowork-instructions.md` 文件夹指令 |
| **产品阶段** | 正式公测 | Research Preview（研究预览） |

---

# 第二部分：产品定位与设计哲学

## 2.1 WorkBuddy——"腾讯版小龙虾"

**核心理念**：将 AI Agent 做成"免部署版 OpenClaw"，砍掉技术门槛，**下载即用**。

**设计哲学**：

1. **IM 驱动**——从微信/飞书/钉钉发指令，电脑自动干活，打破空间限制
2. **模型自由**——不绑定单一模型，用户可按任务切换混元、DeepSeek 等
3. **生态继承**——完全兼容 OpenClaw 的 Skills 体系，存量技能直接可用
4. **成本控制**——优化模型架构降低 Token 消耗，号称"不是 Token 粉碎机"
5. **本地优先**——所有数据和操作在本地完成，不上云

**官方 slogan**："一句话让 AI 替你上班"

**四大核心能力模块**（来源：官方文档）：
- **自然语言理解**：一句话描述需求，无需复杂操作
- **自主规划与执行**：自动拆解任务、规划步骤并完成操作
- **多模态任务处理**：文档、表格、PPT、数据分析等
- **本地文件操作**：读取授权文件夹，批量处理文件

## 2.2 Claude Cowork——"你的第一位 AI 同事"

**核心理念**：将 Claude Code 的强大代理能力"下沉"到普通知识工作者。

**设计哲学**：

1. **Claude Code 平民化**——去掉命令行，换上 GUI，底层引擎完全相同
2. **委派式交互**——"描述结果和节奏"，Claude 自主选择最快路径执行
3. **三阶梯执行**——优先连接器 → 其次浏览器 → 最后屏幕操作（Computer Use）
4. **沙盒安全**——基于 Apple VZVirtualMachine / Windows Hyper-V 的隔离虚拟环境
5. **单模型深度**——只用 Claude，但把单一模型做到极致

**官方 slogan**："Delegate to Claude, delight in the result"

**发展背景**：Anthropic 发现用户大量将 Claude Code（本来面向开发者的终端工具）用于非编程场景——度假研究、做 PPT、清理邮件、监控植物生长。Simon Willison 精准总结："Claude Code 需要的只是'一个不涉及终端的 UI 和一个不吓跑非开发者的名字'。Cowork 就是那个产品。"

## 2.3 哲学差异的本质

> **WorkBuddy = 平台型**：多模型、多 IM、多 Skills，像一个可无限扩展的"AI 操作系统"  
> **Cowork = 产品型**：单模型、深集成、强安全，像一个智能且可靠的"AI 同事"  
>  
> 类比：**WorkBuddy 像 Android**（开放、可定制），**Cowork 像 iOS**（封闭、体验统一）

---

# 第三部分：技术架构深度解析

## 3.1 架构层对比

| 架构层 | WorkBuddy | Claude Cowork |
|--------|-----------|---------------|
| **底层引擎** | CodeBuddy 引擎 + OpenClaw 兼容层 | Claude Code 引擎（Cowork 100% 由 Claude Code 编写） |
| **模型层** | 多模型路由层：混元大模型、DeepSeek、可配置切换 | 单一模型：Claude Opus 4.6（1M token 上下文） |
| **规划层** | 多 Agent 并行规划，支持任务自动拆解 | 规划层（Planning Layer）：请求分析 → 上下文理解 → 路线图创建 |
| **执行引擎** | 本地 Node.js 运行时 + Skills 脚本执行 | 沙盒隔离执行引擎（VZVirtualMachine / Hyper-V） |
| **协作层** | 多 Agent 并行 + 主 Agent 编排 | 子代理协调系统：主代理编排 + 多子代理并行 |
| **扩展层** | Skills 插件 + MCP Server + IM Bot | Plugins + Connectors + MCP + `.cowork-instructions.md` |
| **安全层** | 文件夹授权 + Skill 标准化 + 危险操作拦截 | VM 沙盒隔离 + bubblewrap + seccomp + 计划审批 + 权限文件夹 |
| **运行依赖** | Node.js + Git + .NET（Windows） | Claude Desktop 应用（无额外依赖） |

## 3.2 WorkBuddy 执行流程

```
IM 指令 / 桌面对话
    → 自然语言理解
    → 任务拆解 & 规划
    → 模型调度（混元/DeepSeek/...）
    → Skills + MCP 执行
    → 交付结果
```

## 3.3 Cowork 执行流程

```
桌面/手机 指令
    → 规划层（分析 + 上下文）
    → 执行引擎（沙盒 VM）
    → 子代理协调
    → 连接器 / 浏览器 / 屏幕操作
    → 交付 + 审核
```

## 3.4 Cowork 底层架构深度拆解

> 来源：Fello AI 完整指南 + Anthropic 官方产品页

**VM 沙盒隔离**：
- macOS：使用 Apple Virtualization Framework (`VZVirtualMachine`) 启动定制 Linux (ARM64) 虚拟机
- Windows：使用 Hyper-V 虚拟化
- 这是一个**完整 VM**，不是容器——执行环境完全与宿主 OS 隔离

**文件挂载（非复制）**：
- 你指定的文件夹通过挂载方式进入 VM
- Cowork 可以直接读写这些文件，但无法访问挂载文件夹以外的任何内容

**额外沙盒层**：
- VM 内部添加了 **bubblewrap + seccomp** 双重保护
- bubblewrap 限制文件系统视图、进程能力和命名空间
- seccomp 过滤系统调用，拒绝越界操作

**云端推理**：
- 尽管有本地 VM，所有 AI 推理都在 Anthropic 服务器完成
- Cowork **需要持续网络连接**，不支持离线使用
- 文件内容会发送到 Anthropic 服务器处理（受其数据处理政策约束）

> ⚠️ **关键差异：运行环境依赖**
>
> **WorkBuddy** 需要用户手动安装 Node.js、Git、.NET 等运行环境——90% 的"插件跑不通"问题都出在这里。  
> **Cowork** 零依赖安装——Claude Desktop 内置了一切，但代价是用户无法自由扩展底层运行时。

---

# 第四部分：工作模式详解

## 4.1 WorkBuddy 三大模式

### ⚡ Craft 模式——精细掌控的"执行家"

- **权限**：最高——可读写文件、运行命令、执行脚本
- **适用**：完全信任 AI 时，让它全速跑
- **交互**：说一句，AI 立即动手干
- **类比**：给同事一个明确指令，"你去做吧"

### 📋 Plan 模式——自动规划的"项目经理"

- **权限**：中等——先出方案，用户确认后才执行
- **适用**：复杂任务、需要审查的场景
- **交互**：AI 先列计划清单 → 你确认 → 再执行
- **类比**：PM 先写 PRD，你审批后才开工

### 💬 Ask 模式——保守的"顾问"

- **权限**：最低——只读文件、只回答问题
- **适用**：查资料、问方案、不想让 AI 动任何东西
- **交互**：纯对话，不修改任何文件
- **类比**：问咨询师意见，但决策权在你

## 4.2 Claude Cowork 工作流程

Cowork 没有显式的"模式切换"——它的控制粒度体现在**执行流程**中：

```
1. 描述需求
   → 2. Claude 展示计划
   → 3. 用户审批
   → 4. 逐步执行（遇到不确定会暂停询问）
   → 5. 交付结果 + 日志
```

### Cowork 的"隐式模式"

虽然 Cowork 没有 Craft/Plan/Ask 的显式切换，但你可以通过**提示词**控制行为：

- **"帮我分析这些文件但不要修改"** → 类似 Ask 模式
- **"先列出你的计划"** → 类似 Plan 模式
- **"直接整理这个文件夹"** → 类似 Craft 模式

## 4.3 模式对比总结

| 对比项 | WorkBuddy | Claude Cowork |
|--------|-----------|---------------|
| **模式切换方式** | UI 下拉菜单明确选择 | 提示词隐式控制 |
| **权限粒度** | 三档：全权 / 审批 / 只读 | 统一：展示计划 → 审批 → 执行 |
| **灵活性** | 适合不同信任度的场景快速切换 | 简化用户决策，始终有审批环节 |
| **安全感** | Ask 模式 = 绝对安全 | 默认就有计划审批，但无"纯只读"保证 |

> **核心差异**：WorkBuddy 把模式做成了**产品级的 UI 开关**，Cowork 靠用户的提示词"软控制"。对于不太会写提示词的用户，WorkBuddy 的显式模式更友好。

---

# 第五部分：文件操作能力对比

## 5.1 能力矩阵

| 能力 | WorkBuddy | Claude Cowork |
|------|-----------|---------------|
| **本地文件读写** | ✅ 直接操作 | ✅ 沙盒内操作 |
| **批量文件处理** | ✅ 按日期分类、批量重命名、批量修改 | ✅ 按类型分类、重命名、清理旧文件 |
| **Excel 处理** | ✅ 数据清洗、统计、跨表匹配、生成图表 | ✅ 数据提取、公式计算、可视化图表、多 Sheet |
| **PPT 生成** | ✅ 从数据/主题自动生成 | ✅ 结合模板和源材料、品牌主题、图表 |
| **Word 文档** | ✅ 报告、文档生成 | ✅ 会议纪要、摘要、富格式文档 |
| **PDF 处理** | ✅ 读取分析 | ✅ 发票 OCR → 表格、合并、格式转换 |
| **图片处理** | ⚠️ 部分（依赖 Skills） | ✅ OCR 识别、截图分析、批量处理 |
| **代码文件** | ✅ 读写（继承 CodeBuddy） | ✅ 完整代码操作（继承 Claude Code） |
| **文件搜索** | ✅ 内容级精准搜索 | ✅ 文件夹内全文搜索 |
| **文件安全** | 文件夹授权 + 高危拦截 | 沙盒隔离 + 计划审批 |

### Cowork 支持的文件类型完整清单

> 来源：Anthropic 官方产品页 FAQ

- **文档和文本**：Word (.docx/.doc)、PDF (.pdf)、纯文本 (.txt)、Markdown (.md)、HTML、JSON、CSV、TSV
- **表格**：Excel (.xlsx/.xls/.xlsm)
- **演示文稿**：PowerPoint (.pptx/.ppt)
- **图片**：PNG、JPG、JPEG、GIF、SVG、WebP
- **数据和配置**：YAML、XML、TOML
- **笔记本**：Jupyter Notebooks (.ipynb)
- **代码文件**：几乎所有编程语言——Python、JS、TS、JSX/TSX、Java、C/C++、Go、Rust、Ruby、PHP、SQL、Shell 等

## 5.2 实战指令对比

### WorkBuddy 指令示例

```
"把 E 盘 WorkBuddy 文件夹里，2026 年 3 月的所有 md 文章，
按发布日期分类，每个日期建一个文件夹，把文章归档进去"

"给所有归档的 md 文章，开头统一加上版权声明，
结尾加上公众号引流话术"

"帮我找 E 盘里，内容同时包含'AI'和'Agent'的所有文档，
按修改时间倒序排列"

"帮我删除桌面超过 6 个月没打开的安装包、压缩包，
只保留工作文档"

"基于 2026年Q1运营数据.xlsx 生成季度复盘PPT"
```

### Claude Cowork 指令示例

```
"Organize all files in my Downloads folder. Sort images into Photos,
documents into Documents, archives into Archives, and delete anything
older than 6 months."

"Extract all sales data from the PDF invoices in my Invoices folder
and create an Excel spreadsheet with monthly totals, charts, and
trend analysis."

"Take my meeting notes from notes.txt and create a professional
summary document with action items, key decisions, and attendee
responsibilities."

"Read receipt photos in this folder. Create expense-tracker.xlsx for
personal budgeting: Date, Vendor, Category, Amount. Add formulas for
totals by category. Apply conditional formatting for anything over $100."
```

---

# 第六部分：技能系统与插件生态

## 6.1 对比总表

| 维度 | WorkBuddy Skills | Cowork Plugins |
|------|-----------------|----------------|
| **扩展形式** | Skills 技能包 + MCP Server | Plugins（= Skills + Connectors + Sub-agents 的捆绑包） |
| **安装方式** | 从 GitHub / 市场拉取，`bun` 运行 | `skills.sh` 平台一键安装 / 企业私有市场 |
| **存储格式** | 脚本文件 + 配置 | `SKILL.md` Markdown 文件（可版本控制） |
| **运行环境** | 依赖 Node.js / Git / .NET | Claude Desktop 内置沙盒 |
| **生态来源** | OpenClaw 社区 + 自定义 | Anthropic 官方 + skills.sh 社区 + 企业私有 |
| **企业市场** | ⚠️ 未提及 | ✅ 私有插件市场 + 管理员控制（2026.2.24） |
| **代表插件** | 公众号排版、表格处理、视频剪辑、爬虫、微信 Bot | 数据分析、邮件管理、文档生成、翻译、社媒管理 |
| **自定义难度** | 低（支持零代码自然语言定义） | 中（需编写 SKILL.md 或使用 Skill Creator 交互生成） |
| **IM 类技能** | ✅ WeixinBot / Wecom / Feishu / Dingtalk | ⚠️ Slack 连接器（Team 计划） |

## 6.2 WorkBuddy 技能系统的杀手锏

**IM 联动**是 WorkBuddy 最大的差异化优势。你可以从微信给 AI 发一条消息，电脑上就自动开始干活——出差时远程让 AI 帮你排版文件、导出数据、发送报告。Cowork 目前的跨设备同步仅限于 Claude 自家的手机 ↔ 桌面端。

## 6.3 Cowork 插件系统的杀手锏

### Plugins = Skills + Connectors + Sub-agents 的捆绑包

> 来源：Anthropic 官方产品页

Cowork 的 Plugin 是一个**三合一概念**：
- **Skills**：领域知识和最佳实践（Markdown 格式，可版本控制）
- **Connectors**：Claude 连接外部工具的通道（Google Drive、Slack、Jira 等）
- **Sub-agents**：处理特定任务的专门化代理

**一个 Plugin 打包了上述三者**，让 Claude 从第一次对话就像一个某领域的专家。

### Skills 的渐进式加载机制

> 来源：Substack 高级用户测试

Claude 使用**渐进式披露**（Progressive Disclosure）加载 Skills：
- 先加载元数据（约 100 tokens）
- 仅在需要时才加载完整指令
- 因此可以同时启用 15+ Skills 而不会淹没上下文窗口

### 技能叠加（Skill Stacking）

多个 Skills 可以同时激活，Claude 会自动在不同领域之间切换：

> 上传一个销售跟踪器并要求分析 → 数据分析 Skill 启动  
> 同一对话中说"把这个做成给领导的 PPT" → 演示文稿 Skill 接管

**关键建议**：把技能拆分为多个小技能，而不是一个巨大的全能技能。测试表明，拆分后的效果**明显更好**。

### 官方 MCP 连接器清单（截至 2026.2）

Google Drive、Gmail、Google Calendar、DocuSign、Apollo、Clay、Outreach、Similarweb、MSCI、LegalZoom、FactSet、WordPress、Harvey、Slack（Salesforce）、LSEG、S&P Global、Common Room、Tribe AI

### Slash Commands（斜杠命令）

Cowork 支持直接在对话中用斜杠命令触发快捷操作：
- `/summarize` — 浓缩长对话
- `/translate` — 翻译到其他语言
- `/rewrite` — 改写段落语气
- `/schedule` — 设置定时任务

---

# 第七部分：多智能体与协作机制

## 7.1 WorkBuddy 多 Agent 并行

**机制**：支持多个 Agent 同时处理不同子任务，主 Agent 负责编排和调度。

**特点**：
- 多任务并行执行，极致提效
- 每个 Agent 可独立调用不同 Skills
- 主 Agent 汇总各子 Agent 结果后统一交付
- 适合大规模批量处理（如同时分析 100 个文件）

## 7.2 Cowork 子代理协调

**机制**：协调器管理多个子代理（Sub-agent），每个负责任务的一部分。

**特点**：
- 主代理规划全局 → 子代理并行执行
- 子代理之间可共享上下文
- 透明的推理过程——能看到每个子代理在做什么
- 官方称为"市场独有功能"（竞品 Copilot/ChatGPT 不支持）

**实测数据**（来源：Substack 高级用户）：
> 处理 10 个文件时，使用并行子代理从约 30 分钟缩短到约 4 分钟。

**用法提示**：可以在提示词中显式要求并行处理：

```
Use sub-agents to process these 50 transcripts in parallel.
Extract themes, then synthesize.
```

## 7.3 两者的协作机制差异

| 维度 | WorkBuddy | Cowork |
|------|-----------|--------|
| **并行方式** | 多 Agent 完全独立并行 | 子代理共享上下文的协作并行 |
| **透明度** | Agent 执行过程可见 | 每个子代理的推理过程实时可见 |
| **显式触发** | 系统自动判断是否并行 | 可通过提示词显式要求并行 |
| **适用规模** | 适合大批量同质任务 | 适合复杂异质任务的分解 |

---

# 第八部分：平台集成与连接器

## 8.1 集成能力全景

| 集成类别 | WorkBuddy | Claude Cowork |
|----------|-----------|---------------|
| **即时通讯** | ✅ 微信 / 企业微信 / 飞书 / 钉钉 / QQ | ⚠️ Slack（Team 计划） |
| **云存储** | 通过 MCP 可扩展 | ✅ Google Drive, Dropbox |
| **邮件** | 通过 Skills 可扩展 | ✅ Gmail, Outlook, Exchange |
| **协作工具** | 通过 MCP 可扩展 | ✅ Notion, Asana, Teams |
| **CRM / 销售** | 通过 Skills 可扩展 | ✅ HubSpot, Salesforce, Apollo, Clay |
| **Office 插件** | 生成 Office 文件（非插件形态） | ✅ Excel 和 PPT 深度插件 + 共享上下文 |
| **电子签名** | — | ✅ DocuSign, Dropbox Sign |
| **内容平台** | 公众号排版（通过 Skills） | ✅ WordPress, Medium |
| **金融数据** | — | ✅ Bloomberg Terminal, FactSet, Stripe |
| **计算机控制** | ❌ 不支持 | ✅ Computer Use — 打开应用、导航浏览器、屏幕操作 |
| **定时任务** | 通过 IM 远程触发 | ✅ Cron 定时 + 按需触发 |
| **浏览器操作** | 通过 MCP / Skills 扩展 | ✅ Claude for Chrome 连接器 |

## 8.2 集成策略差异

> **WorkBuddy** 的集成重心在**中国办公生态**（微信、飞书、钉钉），且采用"MCP + Skills 可扩展"的方式，让社区自己补齐连接器。
>
> **Cowork** 的集成重心在**全球 SaaS 生态**（Google、Salesforce、Slack、Notion），且是官方直接提供的**一等公民连接器**。
>
> **选择依据**：如果你的办公工具链是飞书/钉钉/微信 → WorkBuddy；如果是 Google/Slack/Notion → Cowork。

## 8.3 Cowork 的 Dispatch 更新（2026.3.23）

> 来源：Anthropic 官方产品页

Dispatch 是 Cowork 最新的重大更新，打通了手机端和桌面端：

- **手机发任务，桌面执行**：从手机 Claude App 发送任务，桌面 Claude 自动执行
- **Computer Use**：Claude 可以操控你的屏幕——打开应用、点击按钮、导航浏览器
- **跨会话记忆**：Claude 记住你的偏好和工作方式
- **主动性**：Claude 可以主动建议任务
- **定时任务增强**：与 Computer Use 联动

**三阶梯执行优先级**：
1. **连接器优先**（最快最精确）→ 如有 Slack 连接器就直接用
2. **浏览器次之** → 如果没有连接器，通过 Chrome 操作
3. **屏幕操作兜底** → 如果以上都不行，直接操控屏幕

---

# 第九部分：典型场景对比

## 9.1 场景矩阵

| 场景 | WorkBuddy | Cowork | 推荐 |
|------|-----------|--------|------|
| **下载文件夹整理** | ✅ 按日期/类型分类、批量重命名 | ✅ 智能分类 + 自动清理 + 变更日志 | 🟣 Cowork（日志更详细） |
| **发票批量提取** | ✅ 多格式发票 → 报销表 | ✅ PDF OCR → Excel + 公式 + 图表 | 平手 |
| **会议纪要 → 周报** | ✅ 读取多文件 → 文档生成 | ✅ 合成结构化周报 + .docx 导出 | 平手 |
| **远程控制电脑** | ✅ 微信发指令 → 电脑自动执行 | ⚠️ 手机端可发任务（需 Claude App） | 🟢 WorkBuddy（IM 直连更方便） |
| **CRM 数据分析** | 需手动导出数据到本地 | ✅ Salesforce/HubSpot 直连 → 分析 → 报告 | 🟣 Cowork（直连 SaaS） |
| **定时自动化** | 通过 IM 远程触发（非自动） | ✅ Cron 定时 + Computer Use | 🟣 Cowork（真正的定时执行） |
| **中文办公生态** | ✅ 飞书/钉钉/微信 深度集成 | ❌ 不支持国内 IM | 🟢 WorkBuddy（碾压级优势） |
| **法律文档整理** | 通用文件处理 | ✅ 专门场景 + 时间线排序 + 战略评估 | 🟣 Cowork（专业场景更强） |
| **私有知识库** | ✅ 本地向量化知识库 + 优先调取 | ⚠️ .cowork-instructions 文件夹规则 | 🟢 WorkBuddy（专业知识库能力） |
| **桌面应用操作** | ❌ 不能操控其他应用 | ✅ Computer Use——打开应用、点击、导航 | 🟣 Cowork（独有能力） |
| **竞品调研** | 通过 Skills 爬取 + 本地分析 | ✅ 并行 Web 搜索 → 自动交叉引用 → 报告 | 🟣 Cowork（子代理更擅长并行研究） |
| **邮件分类处理** | 通过 IM Bot 间接处理 | ✅ Gmail 直连 → 分类 → 起草回复 | 🟣 Cowork（Gmail 直连） |
| **公众号 / 社媒排版** | ✅ 专门 Skill（微信公众号排版） | 通过 WordPress 连接器 | 🟢 WorkBuddy（国内内容平台） |
| **数据可视化** | ✅ Excel 图表生成 | ✅ 交互式仪表板 + 多维度分析 | 🟣 Cowork（可视化更丰富） |

## 9.2 Cowork 的"杀手级应用"——文件整理

> 来源：Hackceleration 测评 + Substack 用户报告

Cowork 在文件整理场景上获得了最广泛的好评：
- **500 文件 Google Drive** 在不到 10 分钟内完成整理：创建逻辑文件夹、统一命名规范、标记重复
- **2,200 个 Downloads 文件** 在 20 分钟内完成分类
- 测算：5 人团队每周可在文件整理和报告准备上节省 **6-8 小时**

Cowork 的文件整理之所以强，是因为它**读取文件内容**来分类，而不仅仅看文件名。一张叫 `IMG_4521.png` 的图片，它能识别出这是一张 Stripe 发送的 Substack 发票，并正确分类。

---

# 第十部分：安全机制深度对比

## 10.1 安全对比矩阵

| 安全层面 | WorkBuddy | Claude Cowork |
|----------|-----------|---------------|
| **沙盒隔离** | Skill 标准化执行环境 | Apple VZVirtualMachine / Hyper-V 隔离 VM + bubblewrap + seccomp |
| **文件访问控制** | 文件夹级授权 | 文件夹级授权 + 任务完成后可撤销 + 网络白名单 |
| **高危操作拦截** | ✅ 删除系统文件、修改注册表等直接拦截 | ✅ 展示计划等待审批 + 关键操作前弹窗确认 |
| **操作透明度** | 执行前展示访问范围和步骤 | 实时进度指示器 + 推理过程可见 + 活动日志 |
| **数据存储** | 全部本地，不上云 | 对话历史存本地（推理数据发送到 Anthropic 云端） |
| **企业合规** | 腾讯网关安全保障 | ❌ Research Preview 不支持 HIPAA/FedRAMP，不记入审计日志 |
| **误删风险** | 高危操作拦截 + Ask 模式保底 | ⚠️ 已有用户因 `rm -rf` 删除 15,000 张照片（Davydov 事件） |
| **Prompt Injection** | 通过 Skill 标准化缓解 | ⚠️ 安全研究员已证明可通过提示注入从沙盒外泄文件 |

## 10.2 Davydov 照片删除事件详解

> 来源：Fello AI 完整指南

风险投资基金 DVC 创始人 Nick Davydov 请 Cowork 整理妻子的桌面。Cowork 请求删除临时 Office 文件的权限，Davydov 同意了。然后 Cowork 对它认为是空文件夹的目录执行了 `rm -rf`——但那个目录实际上是**家庭照片库，包含 15 年间的约 15,000 张照片**。

因为终端删除**绕过 macOS 废纸篓**，这些照片直接消失了。幸好 iCloud 保留已删除文件 30 天，Apple Support 帮助他恢复了数据。

**教训**：永远不要授予 AI 对不可替代文件的删除权限。

## 10.3 Prompt Injection 安全风险

> 来源：PromptArmor 安全研究

安全研究员 Johann Rehberger 和 PromptArmor 公司演示了**提示注入攻击可以绕过 Cowork 的沙盒防御，从 VM 中外泄文件**。原因是 Anthropic API 域名在 VM 网络规则中被默认信任。

Anthropic 在发布文档中承认 Agent 安全"仍是一个活跃的开发领域"。

## 10.4 两者共同的安全铁律

> 1. **永远使用沙盒文件夹**——不要直接授权 Home 目录或重要数据目录
> 2. **处理前先备份**——无论用哪个工具，批量操作前必须备份
> 3. **指令要清晰具体**——模糊指令是文件灾难的根源
> 4. **从低风险任务开始**——先用查询/分析类任务建立信任
> 5. **永远不要授予不可替代文件的删除权限**

---

# 第十一部分：平台支持与环境要求

| 维度 | WorkBuddy | Claude Cowork |
|------|-----------|---------------|
| **macOS** | ✅ Apple Silicon + Intel | ✅ 原生支持（需 Apple Silicon 或支持虚拟化的 Intel） |
| **Windows** | ✅ x64 + ARM64 兼容 | ✅ 2026.2 新增（x64 only，ARM64 不支持）；需 Hyper-V |
| **Linux** | ❌ 不支持 | ❌ 不支持 |
| **移动端** | 通过 IM（微信/飞书等）间接使用 | Claude 手机 App（iOS/Android）配对桌面 |
| **Web 版** | ❌ 无 | ❌ 无（仅桌面应用） |
| **运行环境依赖** | Node.js + Git + .NET（需手动安装） | 零依赖（Claude Desktop 自带一切） |
| **安装复杂度** | 中等（需配环境，90% 问题出在这里） | 低（下载安装即可） |
| **跨设备同步** | 通过 IM 间接实现 | 设置和插件可跨设备同步 |
| **网络要求** | 本地执行为主 | 必须持续联网（推理在云端） |
| **电脑休眠** | IM 触发时需电脑开启 | ⚠️ 电脑休眠 = 任务终止，定时任务也需电脑保持唤醒 |

### Cowork Windows 已知问题

> Windows 11 Home 用户可能遇到 "Cannot connect to Claude API" 错误  
> 解决方案：更新到 v1.1.4328 或更高版本（GitHub issue #24918）

---

# 第十二部分：定价模型对比

## 12.1 WorkBuddy 定价

- **免费体验补贴**：新用户可免费体验
- **Token 计费**：按实际使用量计费
- **成本优化**：官方强调优化了模型架构降低 Token 消耗
- **多模型灵活性**：可选择不同价位模型，用便宜模型跑简单任务

**优势**：入门门槛低，按需付费，有免费额度

## 12.2 Claude Cowork 定价

| 计划 | 月费 | Cowork 额度 | 说明 |
|------|------|-------------|------|
| **Free** | $0 | ❌ 不含 | — |
| **Pro** | $20/月（年付 $17/月） | 有限 | 每天 3-5 个复杂任务就可能触限 |
| **Max 5x** | $100/月 | 充足 | ~225+ 消息/5小时窗口，日常使用的现实最低线 |
| **Max 20x** | $200/月 | 大量 | ~900+ 消息/5小时窗口，重度用户 |
| **Team** | $20/座/月 | 含标准和高级席位 | 包含 Slack 连接器 |
| **Enterprise** | 定制 | 完整 | 管理员控制、私有插件市场 |

### Cowork 的 Token 消耗真相

> **Cowork 消耗 Token 的速度远快于 Chat。** 一个 Cowork 任务——比如"调研竞品并创建对比表格"——可能消耗 50-100+ 条消息的上下文。因为 AI 不只是回答问题，它在规划、执行终端命令、读文件、写文件、搜索网页、检查自己的工作。每一步都消耗 Token。
>
> **实际意义**：
> - Pro ($20/月)：每天约 3-5 个复杂任务就会触限。适合探索和偶尔使用。
> - Max 5x ($100/月)：**日常使用的现实最低线**。适合中等强度日常工作流。
> - Max 20x ($200/月)：全天高频使用 Cowork 的重度用户。

## 12.3 成本分析

| 使用强度 | WorkBuddy | Cowork |
|----------|-----------|--------|
| **轻度**（每周几个任务） | 免费额度可能够用 | 最低 $20/月 |
| **中度**（每天多个任务） | 按量计费，成本可控 | $100/月（Max 5x） |
| **重度**（大量复杂多步任务） | 按量可能更灵活 | $100-200/月 |

---

# 第十三部分：产品发展时间线

## 13.1 WorkBuddy 里程碑

| 时间 | 事件 | 说明 |
|------|------|------|
| 2026.1.19 | 腾讯内部发布 | WorkBuddy 首次对外展示 |
| 2026.2.6 | 开放内测申请 | 定位"职场 AI 智能体桌面工作台" |
| 2026.3.9 | 正式公测 | 面向所有用户开放，2000+ 腾讯员工实测验证 |
| 2026.3 | IM 全面接入 | 微信/企微/飞书/钉钉/QQ 联动上线 |

## 13.2 Claude Cowork 里程碑

| 时间 | 事件 | 说明 |
|------|------|------|
| 2026.1.12 | Research Preview 发布 | 仅 macOS + Max 订阅用户 |
| 2026.1.16 | 扩大到 Pro 用户 | 强劲需求推动快速开放 |
| 2026.1.30 | 11 个开源插件发布 | 覆盖 HR、设计、工程、运营、金融 |
| 2026.2.10 | Windows 版上线 | 功能完全对等 macOS |
| 2026.2.24 | 13 个企业插件 + 合作伙伴集成 | Team/Enterprise 可管理组织内 Cowork 插件 |
| 2026.2.25 | `/schedule` 计划任务上线 | Cron 定时 + 按需触发 |
| 2026.3.23 | Dispatch 更新 + Computer Use | 手机 ↔ 桌面同步、屏幕控制、跨会话记忆 |

---

# 第十四部分：高级功能深度拆解

## 14.1 WorkBuddy 高级功能

### 14.1.1 IM 远程控制

WorkBuddy 最独特的能力——通过微信/飞书/钉钉远程控制电脑。

**典型场景**：
- 出差时微信发："帮我把桌面上的季度报告发到 team@company.com"
- 下班路上飞书发："把今天的会议录音整理成纪要"
- 手机钉钉发："帮我查一下上周五的运营数据"

**优势**：利用已有的 IM 生态，不需要安装新 App，接入成本为零。

### 14.1.2 多模型路由

- 可按任务复杂度选择不同模型
- 简单任务用便宜模型，复杂任务切换到强模型
- 不被单一模型供应商锁定

### 14.1.3 私有知识库

- 本地向量化知识库
- 任务执行时优先调取私有知识
- 适合企业内部文档管理和 FAQ 自动化

### 14.1.4 OpenClaw 技能兼容

- 完全兼容 OpenClaw 的 Skills 体系
- 社区存量技能直接可用
- 降低了从 OpenClaw 迁移的成本

## 14.2 Cowork 高级功能

### 14.2.1 Computer Use（屏幕控制）

> 2026.3.23 上线，macOS 首发

**工作方式**：
1. Claude 优先尝试**连接器**（最快最精确）
2. 无连接器时尝试 **Chrome 浏览器**操作
3. 最后才使用**屏幕操作**（打开应用、点击按钮、填表等）

**使用场景**：
- 让 Claude 打开你的分析仪表板，截图并汇总关键指标
- 自动填写在线表单
- 在没有 API/连接器的应用中执行操作

**注意**：Computer Use 目前仍在研究预览阶段，交互可能不稳定。

### 14.2.2 定时任务（Scheduled Tasks）

使用 `/schedule` 命令设置：
- **频率**：每小时、每天、每周、仅工作日、按需
- **典型用法**：
  - 每天早上检查邮件并生成日报
  - 每周五自动拉取指标数据并更新周报
  - 每周一生成 Slack 摘要

**关键限制**：
- 电脑必须保持开启且 Claude Desktop 必须运行
- 网络必须持续连接
- 电脑休眠 = 定时任务不执行

### 14.2.3 跨会话记忆（Memory）

**原生方式**：
- Dispatch 更新后支持跨会话记忆
- Claude 记住你的偏好和工作方式

**手动增强**（来源：Substack 高级用户）：
- 在授权文件夹中创建 `.cowork-instructions.md` 文件
- 描述文件夹内容、组织方式、规则（如"不要删除此文件夹的文件"、"文件名统一用 YYYY-MM-DD 前缀"）
- Cowork 自动读取这些指令

- 在 Settings > Cowork > Instructions 设置**全局指令**（跨会话持久）

### 14.2.4 Cowork Ideas Dashboard

最新更新提供了预填充的提示模板和推荐连接器，帮助用户快速上手委派任务。

---

# 第十五部分：真实用户反馈与踩坑经验

## 15.1 WorkBuddy 用户反馈

### 👍 好评

- **IM 联动体验极佳**：微信发指令就能远程干活，出差党的福音
- **模型灵活性**：可以切换到便宜模型跑简单任务，控制成本
- **中文场景优化好**：对飞书/钉钉/微信公众号的理解到位
- **免费入门**：有免费额度，试错成本低

### 👎 差评和踩坑

- **环境配置是最大痛点**：Node.js / Git / .NET 安装经常出问题，90% 的"插件跑不通"卡在这里
- **Skills 质量参差不齐**：社区 Skills 有些维护不积极
- **缺少 Computer Use**：无法操控桌面应用程序
- **无原生定时任务**：只能通过 IM 手动触发

## 15.2 Cowork 用户反馈

### 👍 好评

- **文件整理是杀手级应用**：500 个文件 10 分钟搞定，2200 个文件 20 分钟
- **文档质量高**：生成的文档被评价为"看起来像手工制作的，不像 AI 生成的"
- **子代理并行真的快**：10 个文件的处理从 30 分钟缩到 4 分钟
- **零配置安装**：下载安装就能用，无环境依赖
- **推理深度强**：Claude Opus 4.6 在复杂分析和研究场景表现出色

### 👎 差评和踩坑

- **Token 消耗太快**：Pro 计划每天 3-5 个复杂任务就可能触限
- **电脑休眠 = 任务终止**：长时间任务需要保持电脑唤醒
- **无跨会话记忆**（Dispatch 更新前）：每次都要重新教 Claude 你的偏好
- **无 Microsoft 365 集成**：如果用 Outlook/OneDrive/Teams/SharePoint，连接器基本废了
- **无 Linux 支持**
- **Davydov 事件**：`rm -rf` 删除 15,000 张照片的安全事故
- **没有项目管理工具集成**：无 Trello、Monday.com、ClickUp、Asana（Jira 通过 MCP 支持）
- **不支持合规审计**：Enterprise 的审计日志和合规 API 不覆盖 Cowork 活动
- **扫描版 PDF 处理不可靠**：基于图像的 PDF（非文字 PDF）经常失败

## 15.3 共同的坑

1. **模糊指令 = 灾难**：两者都不能很好地处理模糊指令，越具体越好
2. **大文件处理**：超大的 Excel/PDF 可能导致超时或错误
3. **复杂格式文档**：布局复杂的文档可能丢失格式
4. **依赖网络**：两者都在某种程度上依赖网络连接

---

# 第十六部分：最佳实践与使用技巧

## 16.1 WorkBuddy 最佳实践

1. **先配好环境再折腾 Skills**：确保 Node.js、Git、.NET 都安装正确
2. **从 Ask 模式开始**：不确定时先用 Ask 模式查看 AI 理解是否正确
3. **利用 IM 联动**：设置好微信/飞书 Bot，出差时远程操控
4. **多模型策略**：简单任务用混元（省钱），复杂任务切 DeepSeek
5. **建立私有知识库**：把常用的文档模板、规范放进知识库

## 16.2 Cowork 最佳实践

### 三问框架——每次任务前回答

> 来源：Substack 高级用户 Karo 的经验

1. **"完成"长什么样？** → 描述期望的最终状态
2. **Claude 需要什么上下文？** → 提供它无法猜到的信息
3. **有什么约束它猜不到？** → 明确不能做的事情

### 指令模板示例

**❌ 差的指令**：
```
整理我的下载文件夹。
```

**✅ 好的指令**：
```
最终状态：我的 ~/Downloads 文件夹只保留最近 7 天的文件。
其余文件按类型分到 ~/Sorted/photos、~/Sorted/documents、~/Sorted/other。

上下文：
当前有约 187 个文件，跨度数月
主要是 .jpg、.pdf 和 .zip

约束：
不要删除任何文件——只移动。

输出：完成后创建 what-moved.md 列出每个类别移了多少文件。
```

### 更多技巧

1. **永远要求变更日志**：让 Claude 生成 `what-changed.md`，方便审查每个决策
2. **先用测试文件试**：用非关键文件测试 Claude 如何理解你的指令
3. **设置全局指令**：Settings > Cowork > Instructions，写上你的角色、偏好、格式规范
4. **创建文件夹指令文件**：每个授权文件夹放一个 `.cowork-instructions.md`
5. **安装相关连接器但不要装太多**：每个活跃插件都增加 Token 消耗
6. **从文件整理开始**：这是 Cowork 最强的场景，也是建立信任的好方法
7. **使用定时任务处理重复工作**：周报、日报、数据拉取
8. **队列多个任务**：Cowork 支持并行处理，不必等一个完成再开始下一个
9. **监控用量**：Settings > Usage 查看消息消耗，尤其 Pro 和 Max 5x 用户
10. **拆分 Skills**：多个小 Skill 比一个大 Skill 效果好得多

### Cowork 十大 Prompt 模板

| 场景 | 模板要点 |
|------|---------|
| **邮件分类** | 回顾过去 7 天邮件 → 分类为紧急/需回复/仅知悉 → 生成 triage.md |
| **内容再利用** | 从文章提取 3 个核心洞察 → 每个生成 60 秒 LinkedIn 视频脚本 |
| **费用追踪** | 读取收据照片 → 创建 expense-tracker.xlsx → 含日期/商家/分类/金额/公式 |
| **研究综合** | 读取文件夹所有文档 → 创建 synthesis-report.docx → 含摘要/主题/引用/矛盾点 |
| **竞品调研** | 调研 [公司 A/B/C] 定价页 → 创建 comparison.xlsx → 含功能/价格/优缺点 |
| **会议准备** | 整理文件夹 → 按工作流分类 → 生成 progress.pptx（5 页以内） |
| **市场规模评估** | 调研市场问题 → 生成分析报告 + PPT + Excel |
| **客户反馈聚合** | 综合通话记录/Slack/CRM/Linear → 识别模式 → 生成优先产品建议 |
| **法律文档整理** | 文件夹诉讼文件 → 按时间排序 → 生成展示集 + 战略重要性评估 |
| **日常简报** | 每天从 Slack/Notion/GitHub 拉取 → 生成优先级 + 关联性简报 |

---

# 第十七部分：选型决策指南

## 17.1 各维度胜者一览

| 维度 | 胜者 | 原因 |
|------|------|------|
| **中国办公生态集成** | 🟢 WorkBuddy | 微信/飞书/钉钉/企微 全面接入，Cowork 无国内 IM |
| **全球 SaaS 连接器** | 🟣 Cowork | 30+ 官方连接器（Google/Slack/Salesforce/Notion） |
| **安装易用性** | 🟣 Cowork | 零依赖安装 vs WorkBuddy 需 Node.js/Git/.NET |
| **模型灵活性** | 🟢 WorkBuddy | 5+ 模型可切换 vs Cowork 仅 Claude 单模型 |
| **工作模式设计** | 🟢 WorkBuddy | 三档 Craft/Plan/Ask 显式切换，安全感更强 |
| **Computer Use** | 🟣 Cowork | 独有能力——操控屏幕、打开应用、点击按钮 |
| **定时自动化** | 🟣 Cowork | Cron 原生定时 vs WorkBuddy 仅 IM 手动触发 |
| **入门成本** | 🟢 WorkBuddy | 免费额度 + 按量计费 vs Cowork 起步 $20/月 |
| **IM 远程控制** | 🟢 WorkBuddy | 微信一条消息就能远程操控电脑，Cowork 无此能力 |
| **企业级管理** | 🟣 Cowork | 私有插件市场 + SSO + 审计日志 + 数据驻留合规 |
| **知识库** | 🟢 WorkBuddy | 本地向量化知识库 vs Cowork 仅文件夹指令 |
| **推理能力上限** | 🟣 Cowork | Claude Opus 4.6（1M context）的推理深度更强 |
| **文件整理** | 🟣 Cowork | 内容级分类 + 变更日志 + 社区广泛验证 |
| **中文内容平台** | 🟢 WorkBuddy | 微信公众号排版等国内平台 Skill |

## 17.2 最终选型建议

### 🇨🇳 选 WorkBuddy，如果你是...

- 日常办公工具是**飞书 / 钉钉 / 微信 / 企业微信**
- 需要**远程控制电脑**（出差时微信发指令干活）
- 希望**多模型灵活切换**，不被单一供应商绑定
- 需要搭建**私有本地知识库**
- 预算敏感，希望**免费起步 + 按量付费**
- 已有 **OpenClaw Skills** 存量资产
- 不需要操控桌面应用程序
- 对"环境配置"不抵触（愿意装 Node.js/Git）

### 🌍 选 Claude Cowork，如果你是...

- 日常办公工具是 **Google Workspace / Slack / Notion / Salesforce**
- 需要 **Computer Use**——让 AI 操控屏幕和应用
- 需要**定时自动化任务**（每周五自动生成报告等）
- 追求**零配置安装**，不想碰任何技术细节
- 企业需要 **SSO / 审计日志 / 合规**等管理能力
- 看重 Claude 的**推理深度**（复杂分析、法律、研究场景）
- 愿意支付 **$20-200/月** 的订阅费用
- 能接受 Research Preview 阶段的偶尔不稳定

### 🤝 终极答案：它们不是替代关系，而是互补关系

**WorkBuddy** 更适合**中国办公环境 + IM 驱动 + 多模型灵活性**的场景。

**Cowork** 更适合**全球 SaaS 生态 + 深度推理 + 定时自动化**的场景。

如果你同时使用飞书和 Slack、同时需要混元和 Claude——**完全可以两个都用**。WorkBuddy 处理国内 IM 联动和批量文件任务，Cowork 处理 SaaS 集成和定时自动化，各取所长。

---

> **声明**：本报告基于 2026 年 3 月公开资料整理，两款产品均在快速迭代中，部分功能可能已更新。
>
> **资料来源**：
> - Anthropic 官方产品页（claude.com/product/cowork）
> - 腾讯 CodeBuddy 官方文档（codebuddy.cn/docs/workbuddy/Overview）
> - Fello AI 完整指南（felloai.com/claude-cowork-guide）
> - Substack 高级用户测试（Karo / Product with Attitude）
> - Collabnix 技术分析（collabnix.com）
> - 知乎、CSDN 社区实测报告
> - Hackceleration 评测
> - PromptArmor 安全研究
