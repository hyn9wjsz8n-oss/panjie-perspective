# 平台安装说明

## 腾讯 WorkBuddy

推荐下载仓库 `dist/panjie-perspective-workbuddy.zip`，在 WorkBuddy 的技能页选择「添加技能 → 上传技能」，上传整个 ZIP，再从已安装列表确认启用。

包内只有一个 `panjie-perspective/` 根文件夹，里面直接包含 `SKILL.md` 与 `references/`。不要把整个 GitHub 源码下载包当作 WorkBuddy 专用技能包；README 中的下载按钮直接指向专用包。

此版本按 WorkBuddy 开放平台的 SKILL.md 结构补齐 `description_zh`、`description_en`、`version`、`author` 等字段。参考资料以平台支持的 `@references/` 提示和相对链接提供。它是本地自定义技能包，没有代为提交 WorkBuddy 官方市场或配置企业下发。

资料依据：[技能导入说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)、[开放平台格式](https://open.workbuddy.cn/en/docs/skill)。企业账号若限制自定义技能，需遵循所在企业的设置。

## Codex

最简单的方法：把仓库链接交给 Codex，并输入：

> 请使用 skill-installer，从 https://github.com/hyn9wjsz8n-oss/panjie-perspective 安装技能；技能入口在仓库根目录。若已存在同名技能，先保留旧版，不覆盖我的私人资料。

也可以下载标准 ZIP，把解压后的完整 `panjie-perspective` 文件夹放到 `~/.agents/skills/`。新版本 Codex 会检测技能变化；未出现时重新打开客户端。已有同名自用版时，先保留旧版，避免同时加载两个同名定义。

本地源码安装方式，需要 Python 3：

```sh
python3 scripts/install.py --target codex
```

脚本默认写入官方个人技能目录，遇到同名目录会停止；它不会修改模型设置或安装额外依赖。旧版或自定义技能目录可通过 `--destination` 明确指定最终技能文件夹。

依据：[OpenAI 技能说明](https://learn.chatgpt.com/docs/build-skills)。

## Claude Code

下载标准 ZIP，把完整技能文件夹放到 `~/.claude/skills/panjie-perspective`，然后在 Claude Code 中输入：

```text
/panjie-perspective 请分析我提供的场景，并写一段模拟回复。
```

或从源码目录运行：

```sh
python3 scripts/install.py --target claude-code
```

依据：[Claude Code 技能说明](https://code.claude.com/docs/en/skills)。

## 普通聊天工具

打开 `dist/panjie-perspective-prompt.md`，将全文粘贴为本次任务指令，再附上你的场景。该文件已合并人物层、应用层、沟通框架和示例，无需读其他文件。

这种方式不安装技能、不提供后台连接，也不保证跨对话记忆；效果和输入长度受所用工具支持范围影响。

## 更新和移除

更新前保留同名旧版本。WorkBuddy 可使用已安装技能页面的管理入口；手动安装的标准包可替换对应技能目录。移除时仅移除本技能目录，不需要清理数据库、登录配置或后台进程。
