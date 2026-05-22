# tabletop-skills

> 一个面向 AI Agent 的桌游 skill 集合 —— 让 Claude / Codex / Gemini 等带 skill 机制的 Agent 当你的 KP / GM。
> A collection of tabletop-RPG skills for AI agents (Claude, Codex, Gemini, etc.) — let your agent be the Keeper / GM.

每个一级子目录是一个**独立的 skill**，自带 `SKILL.md`、剧本数据、判定脚本和存档目录，互不依赖。
Each top-level subdirectory is a **self-contained skill** with its own `SKILL.md`, scenario data, rule scripts, and save folder — no cross-dependencies.

---

## 📚 已收录剧本 / Available Scenarios

| Skill | 系统 System | 剧本 Scenario | 玩家 Players | 时长 Length | 简介 Pitch |
|---|---|---|---|---|---|
| [`brenner-apartment`](brenner-apartment/) | 克苏鲁的呼唤 / Call of Cthulhu | 布伦纳公寓 / Brenner Apartment | 1 | ~30min | 1923 年波士顿，调查一栋让三名租客接连精神崩溃的公寓。/ Boston, 1923 — investigate an apartment whose last three tenants all went mad. |

> 想加新剧本？看下方[贡献新 skill](#-贡献新-skill--contributing) 章节。
> Want to add a scenario? See [Contributing](#-贡献新-skill--contributing) below.

---

## 🚀 给 Agent 的安装说明 / Installation (for the Agent)

**如果用户把这个仓库链接 (`https://github.com/Xinos-Zeng/tabletop-skills`) 发给你，并希望使用其中某个 skill，按以下步骤执行：**
**If a user hands you this repo URL and asks to use one of its skills, follow these steps:**

### Step 1 — Clone

把仓库 clone 到一个临时位置。Clone the repo to a temporary location.

```bash
git clone https://github.com/Xinos-Zeng/tabletop-skills.git /tmp/tabletop-skills
```

### Step 2 — 识别用户运行环境的 skills 目录 / Identify the host's skills directory

不同 Agent 平台的 skill 安装位置不同，按当前环境选择对应路径。
Different agent platforms store skills in different locations — pick the one matching your runtime:

| 运行环境 / Runtime | 用户级 / User-level | 项目级 / Project-level |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `<project>/.claude/skills/` |
| Codex CLI | `~/.codex/skills/` | `<project>/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `<project>/.gemini/skills/` |
| 其他 / Other | 查阅该 Agent 的 skill 文档 / Check the agent's skill docs | — |

**判断原则 / Rule of thumb：**
- 用户没指定就装到**用户级**目录（全局可用）/ Default to **user-level** unless the user says otherwise (so it's available everywhere).
- 用户级目录不存在时主动创建 / Create the directory if missing：`mkdir -p ~/.claude/skills`

### Step 3 — 只搬用户想要的那个子目录 / Copy only the requested subdirectory

**不要**把整个仓库塞进 skills 目录 —— 那会让所有剧本一次性注册，污染触发空间。
**Do not** dump the whole repo into the skills directory — that would register every scenario at once and pollute the trigger namespace.

```bash
# 例 / Example: 安装布伦纳公寓到 Claude Code 用户级 / Install Brenner Apartment for Claude Code
cp -r /tmp/tabletop-skills/brenner-apartment ~/.claude/skills/
```

### Step 4 — 验证 / Verify

```bash
ls ~/.claude/skills/brenner-apartment/SKILL.md   # 应输出文件路径 / should print the file path
```

随后告诉用户："已安装，重启 Agent 会话后说『玩布伦纳公寓』即可触发。"
Then tell the user: *"Installed. Restart the agent session and say '玩布伦纳公寓' / 'play Brenner Apartment' to trigger it."*

### Step 5 — 清理 / Cleanup

```bash
rm -rf /tmp/tabletop-skills
```

---

## 🧩 仓库结构 / Repository Layout

```
tabletop-skills/
├── README.md                    # 本文件 / this file
└── <scenario-name>/             # 一个剧本 = 一个 skill / one scenario = one skill
    ├── SKILL.md                 # 入口：name + description + 规则提示 / entry point
    ├── data/                    # 剧本数据 / scenario data (story, scenes, NPCs, items…)
    ├── scripts/                 # 判定/骰子/战斗脚本 / dice, checks, combat scripts
    ├── schemas/                 # 存档 JSON schema / save-file schemas
    └── saves/                   # 玩家存档（运行时生成）/ player saves (created at runtime)
```

---

## ✍️ 贡献新 skill / Contributing

新增一个剧本时，遵循下面三条约定，避免触发词互相打架：
When adding a new scenario, follow three conventions so triggers don't collide:

1. **目录名 = skill 名 = 剧本名（kebab-case）** / Directory name = skill name = scenario slug.
   例 / e.g. `silver-twilight/`, `masks-of-nyarlathotep/`.
2. **`SKILL.md` 的 `description` 只认剧本名** / `description` should trigger **only** on the scenario's own name.
   避免用「开始游戏」「跑团」「玩克苏鲁」这类泛词 —— 它们会和其他剧本互抢。
   Avoid generic phrases like *"start a game"* / *"play Cthulhu"* — they overlap with other scenarios.
3. **自包含** / Self-contained：所有数据、脚本、schema 都放在自己的目录下，不跨剧本依赖。
   All data / scripts / schemas live under the scenario's own directory; no cross-scenario imports.
