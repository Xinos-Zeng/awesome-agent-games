# tabletop-skills

> 一个桌游剧本集合，每个剧本都打包成可被 AI Agent 加载的 skill —— 让 Claude / Codex / Gemini 等 Agent 当你的 KP / GM 陪你跑团。
> A collection of tabletop-RPG scenarios, each packaged as a skill that AI agents can load — let Claude / Codex / Gemini be your Keeper / GM.

每个一级子目录就是一个完整的剧本，自带规则提示、剧情数据、判定脚本和存档目录，互相独立。
Each top-level subdirectory is a complete, self-contained scenario with its own rules, story data, dice scripts, and save folder.

---

## 📚 已收录剧本 / Scenarios

| Skill | 系统 System | 剧本 Scenario | 玩家 Players | 时长 Length | 简介 Pitch |
|---|---|---|---|---|---|
| [`brenner-apartment`](brenner-apartment/) | 克苏鲁的呼唤 / Call of Cthulhu | 布伦纳公寓 / Brenner Apartment | 1 | ~30min | 1923 年波士顿，调查一栋让三名租客接连精神崩溃的公寓。/ Boston, 1923 — investigate an apartment whose last three tenants all went mad. |

---

## 🚀 怎么用 / How to Use

### 1. Clone 仓库 / Clone the repo

```bash
git clone https://github.com/Xinos-Zeng/tabletop-skills.git
```

### 2. 把想玩的剧本放进 Agent 的 skills 目录 / Drop the scenario into your agent's skills folder

不同 Agent 平台的 skill 目录位置不一样，按你用的那个工具放：
The skills folder depends on which agent you use — pick the row that matches yours:

| Agent | 全局可用 / User-level | 仅当前项目 / Project-level |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `<你的项目>/.claude/skills/` |
| Codex CLI | `~/.codex/skills/` | `<你的项目>/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `<你的项目>/.gemini/skills/` |
| 其他 / Other | 参考该 Agent 的 skill 文档 / See your agent's skill docs | — |

例如想在 Claude Code 里全局玩布伦纳公寓：
For example, to make Brenner Apartment globally available in Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -r tabletop-skills/brenner-apartment ~/.claude/skills/
```

> 💡 **只放你想玩的那一个子目录**，别把整个仓库塞进去 —— 否则所有剧本会一次性注册，触发关键词容易打架。
> 💡 **Copy only the scenario you want**, not the whole repo — otherwise every scenario registers at once and their trigger keywords start colliding.

### 3. 在 Agent 里召唤它 / Summon it from your agent

重启 Agent 会话，对它说剧本名就行。比如：
Restart your agent session and just say the scenario's name, e.g.:

> "我想玩布伦纳公寓"
> *"Let's play Brenner Apartment"*

> 🤖 **如果你是直接把这个 README 链接发给 Agent 的**：上面的命令你照着执行即可。默认装到用户级目录（除非用户指定项目级），装完告诉用户重启会话并说出剧本名触发。
> 🤖 **If you're an agent reading this on behalf of a user**: just follow the commands above. Default to the user-level folder unless the user asks for project-level, then tell them to restart the session and say the scenario name to trigger it.

---

## 🧩 仓库结构 / Repository Layout

```
tabletop-skills/
├── README.md
└── <scenario-name>/             # 一个剧本 = 一个 skill / one scenario = one skill
    ├── SKILL.md                 # 入口：name + description + 规则 / entry point
    ├── data/                    # 剧情、场景、NPC、道具 / story, scenes, NPCs, items
    ├── scripts/                 # 骰子、检定、战斗 / dice, checks, combat
    ├── schemas/                 # 存档 JSON schema / save-file schemas
    └── saves/                   # 玩家存档（运行时生成）/ player saves (runtime)
```

---

## ✍️ 想加新剧本？/ Adding a New Scenario

为了让多个剧本共存时不打架，新增剧本请遵守三条约定：
To keep multiple scenarios from stepping on each other, please follow three conventions:

1. **目录名 = skill 名 = 剧本名（kebab-case）** / Directory name = skill name = scenario slug.
   例 / e.g. `silver-twilight/`, `masks-of-nyarlathotep/`.
2. **`SKILL.md` 的 `description` 只认剧本本身的名字** / The `description` should trigger **only** on the scenario's own name.
   别用「开始游戏」「跑团」「玩克苏鲁」这种泛词，会和其他剧本互抢。
   Avoid generic phrases like *"start a game"* or *"play Cthulhu"* — they overlap with other scenarios.
3. **保持自包含** / Keep it self-contained：所有数据、脚本、schema 都放在自己目录下，不跨剧本依赖。
   All data, scripts, and schemas live under the scenario's own folder — no cross-scenario imports.

加完别忘了在上面的剧本表格里加一行。
Don't forget to add a row to the scenario table above.
