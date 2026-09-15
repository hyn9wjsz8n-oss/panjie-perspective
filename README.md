# 盼姐 · 工作判断与表达 Skill

用盼姐的工作判断方式分析问题，用她自然、具体的口语写回复和口播。**安装后直接提问，无需飞书账号、外置知识库或 API 密钥。**

公开版 1.0.0 · 中文 · 指令与参考资料随包提供

## 腾讯 WorkBuddy：下载后导入

**[下载 WorkBuddy 技能包](https://github.com/hyn9wjsz8n-oss/panjie-perspective/raw/refs/heads/main/dist/panjie-perspective-workbuddy.zip)**

1. 下载上面的 ZIP 文件。
2. 在 WorkBuddy 的「专家·技能·连接器 → 技能」中，选择「添加技能 → 上传技能」，导入 ZIP。
3. 确认技能已启用，在对话中选择它，输入你的场景。

例如：

> 用盼姐的工作判断方式分析：一位有木工经验的人想换工作，英语刚开始学，家里比较担心。先说明最该弄清的三件事，再写一段自然口语的模拟回复。

安装入口依据 [WorkBuddy 技能说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。导入包按 [WorkBuddy 开放平台格式](https://open.workbuddy.cn/en/docs/skill) 添加了中英文描述、版本和作者等字段。不同客户端版本的入口文字可能有变化。

## 其他使用方式

| 工具 | 获取方式 | 使用方式 |
| --- | --- | --- |
| Codex | [标准技能包](https://github.com/hyn9wjsz8n-oss/panjie-perspective/raw/refs/heads/main/dist/panjie-perspective.zip)，或让技能安装器读取本仓库 | 选择技能，或输入 `$panjie-perspective` |
| Claude Code | 解压标准包，把完整 `panjie-perspective` 文件夹放到个人技能目录 | 输入 `/panjie-perspective` |
| 能接收长文本指令的聊天工具 | [单文件提示词](dist/panjie-perspective-prompt.md) | 将全文作为本次对话指令，再提供任务 |

完整步骤和本地安装命令见 [平台安装说明](docs/platforms.md)。单文件提示词是文本使用方式，不会自动给聊天工具安装 Skill。

## 两层合在一个入口

- **人物层：**来自原版 `panjie-perspective` 的工作判断与表达框架，重视个人条件、结果与兑现、帮助和责任的边界。
- **应用层：**把框架用于客户分析、方案比较、口播和回复；补齐任务步骤，保留事实缺项。

应用层的新建议会标为推演，不能变成本人过去的观点。WorkBuddy 与标准包共用同一正文和参考资料，只在平台元数据与资源加载提示上做适配。

## 适合直接尝试

> 用盼姐的语气，写一段一分钟口播，解释为什么选择工作不能只看工资数字。例子请明确标为假设。

> 这个客户最在意费用，但还没有具体报价。帮我分析需要先弄清什么，再写一段回复，不编金额。

> 这两种选择分别有什么代价？请按盼姐的判断方式分析，把材料里的事实和你新提出的建议分开。

## 公开版的范围

本版公开工作方法、表达示例和一般客户沟通框架。它不含公司内部 70 问、经营数据、报价和退款口径、原始私人访谈、客户名单、账号凭据或本机路径，也不需要这些资料才能运行。

人物依据截至 2026-09-14；内容不是实时政策或项目数据库。具体报价、资格、合同、工资等结论需要本次适用材料。生成内容属于模拟与草稿，不表示本人已经批准发布或作出承诺。

技能自身没有后台服务、网络请求脚本或自动发送功能。你使用的 AI 工具仍需自己的账号，并按其规则处理输入和产生模型费用。

## 文件与验证

```text
SKILL.md                  统一入口
references/               人物框架、应用流程、沟通框架和示例
agents/openai.yaml        Codex 显示配置
dist/                     标准 ZIP、WorkBuddy ZIP、单文件提示词
docs/                     平台说明、来源与验证范围
scripts/                  安装与发布构建工具（运行技能不需要执行）
```

已做包结构、相对引用、两种包正文一致性、解压和安装脚本检查；本次没有在 WorkBuddy 或 Claude Code 客户端进行实机调用验收。适配状态见 [验证说明](docs/validation.md)。

## 来源与许可

工作风格由已有盼姐模型选编，应用工作流和示例由本项目整理。方法参考花叔的 [女娲 · Skill 造人术](https://github.com/alchaincyf/nuwa-skill)。来源取舍见 [设计说明](docs/design.md)。

本仓库的指令、示例和构建代码按 [MIT License](LICENSE) 提供。许可不代表获得本人背书、代言、肖像或声音使用授权。
