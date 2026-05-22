# tabletop-skills

**🌐 中文** | [English](README.en.md)

> 一个桌游剧本集合，每个剧本都打包成可被 AI Agent 加载的 skill —— 让 Claude / Codex / Gemini 等 Agent 当你的 KP / GM 陪你跑团。

每个一级子目录就是一个完整的剧本，自带规则提示、剧情数据、判定脚本和存档目录，互相独立。

---

## 📚 已收录剧本

| Skill | 系统 | 剧本 | 玩家 | 时长 | 简介 |
|---|---|---|---|---|---|
| [`brenner-apartment`](brenner-apartment/) | 克苏鲁的呼唤 | 布伦纳公寓 | 1 | ~30min | 1923 年波士顿，调查一栋让三名租客接连精神崩溃的公寓。 |

---

## 🚀 怎么用

### 1. Clone 仓库

```bash
git clone https://github.com/Xinos-Zeng/tabletop-skills.git
```

### 2. 把想玩的剧本放进 Agent 的 skills 目录

不同 Agent 平台的 skill 目录位置不一样，按你用的那个工具放：

| Agent | 全局可用 | 仅当前项目 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `<你的项目>/.claude/skills/` |
| Codex CLI | `~/.codex/skills/` | `<你的项目>/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `<你的项目>/.gemini/skills/` |
| 其他 | 参考该 Agent 的 skill 文档 | — |

例如想在 Claude Code 里全局玩布伦纳公寓：

```bash
mkdir -p ~/.claude/skills
cp -r tabletop-skills/brenner-apartment ~/.claude/skills/
```

### 3. 在 Agent 里召唤它

重启 Agent 会话，对它说剧本名就行。比如：

> "我想玩布伦纳公寓"

> 🤖 **如果你是直接把这个 README 链接发给 Agent 的**：上面的命令你照着执行即可。默认装到用户级目录（除非用户指定项目级），装完告诉用户重启会话并说出剧本名触发。

---

## 🧩 仓库结构

```
tabletop-skills/
├── README.md
└── <scenario-name>/             # 一个剧本 = 一个 skill
    ├── SKILL.md                 # 入口：name + description + 规则
    ├── data/                    # 剧情、场景、NPC、道具
    ├── scripts/                 # 骰子、检定、战斗
    ├── schemas/                 # 存档 JSON schema
    └── saves/                   # 玩家存档（运行时生成）
```

---

## ✍️ 想加新剧本？

为了让多个剧本共存时不打架，新增剧本请遵守三条约定：

1. **目录名 = skill 名 = 剧本名（kebab-case）**
   例：`silver-twilight/`、`masks-of-nyarlathotep/`。
2. **`SKILL.md` 的 `description` 只认剧本本身的名字**
   别用「开始游戏」「跑团」「玩克苏鲁」这种泛词，会和其他剧本互抢。
3. **保持自包含**：所有数据、脚本、schema 都放在自己目录下，不跨剧本依赖。

加完别忘了在上面的剧本表格里加一行。
