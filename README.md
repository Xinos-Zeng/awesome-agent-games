# awesome-agent-games

**中文** | [English](README.en.md)

> 一个面向 AI Agent 的游戏 skill 集合：可以是 CoC 跑团，也可以是 Galgame、互动小说，或者任何适合上班摸鱼的可玩内容。

每个游戏都是一个完整、可独立安装的 skill，自带规则提示、剧情数据、运行脚本和存档目录。分类目录只用于整理仓库，真正复制到 Agent skills 目录的是具体游戏目录。

---

## 已收录游戏

### CoC 跑团

| Skill | 系统 | 游戏 | 玩家 | 时长 | 简介 |
|---|---|---|---|---|---|
| [`brenner-apartment`](coc/brenner-apartment/) | 克苏鲁的呼唤 | 布伦纳公寓 | 1 | ~30min | 1923 年波士顿，调查一栋让三名租客接连精神崩溃的公寓。 |

开发规范见 [`coc/tutorial.md`](coc/tutorial.md)。

### Galgame

| Skill | 类型 | 游戏 | 玩家 | 时长 | 简介 |
|---|---|---|---|---|---|
| [`shiomi-academy-seven-days`](galgame/shiomi-academy-seven-days/) | 视觉小说 | 汐見学園の七日間 | 1 | 多周目 | 海边学园、废弃灯塔与七天时间循环中的恋爱冒险。 |

开发规范见 [`galgame/tutorial.md`](galgame/tutorial.md)。

---

## 怎么用

### 1. Clone 仓库

```bash
git clone https://github.com/Xinos-Zeng/awesome-agent-games.git
```

也可以直接对 Agent 说：请从 `https://github.com/Xinos-Zeng/awesome-agent-games` 下载我想玩的游戏 skill，并安装到你的用户级 skills 目录。

### 2. 把想玩的游戏放进 Agent 的 skills 目录

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
cp -r awesome-agent-games/coc/brenner-apartment ~/.claude/skills/
```

例如想玩《汐見学園の七日間》：

```bash
mkdir -p ~/.claude/skills
cp -r awesome-agent-games/galgame/shiomi-academy-seven-days ~/.claude/skills/
```

### 3. 在 Agent 里召唤它

重启 Agent 会话，对它说游戏名就行。比如：

> "我想玩布伦纳公寓"

> "我想玩汐見学園の七日間"

> 如果你是直接把这个 README 链接发给 Agent 的：上面的命令你照着执行即可。默认装到用户级目录，除非用户指定项目级。装完告诉用户重启会话并说出游戏名触发。

---

## 仓库结构

```
awesome-agent-games/
├── README.md
├── coc/
│   ├── tutorial.md
│   └── <game-slug>/
│       ├── SKILL.md
│       ├── data/
│       ├── scripts/
│       ├── schemas/
│       └── saves/
└── galgame/
    ├── tutorial.md
    └── <game-slug>/
        ├── SKILL.md
        ├── data/
        ├── scripts/
        └── saves/
```

---

## 贡献自己的游戏

欢迎 PR 新游戏。为了让多个 skill 共存时不互相抢触发词，请遵守这些约定：

1. 选择合适分类目录，例如 `coc/` 或 `galgame/`。
2. 新建具体游戏目录，目录名使用 kebab-case，并和 `SKILL.md` frontmatter 的 `name` 保持一致。
3. `description` 只触发具体游戏名，不使用“开始游戏”“玩 galgame”“跑团”这类泛词。
4. 保持自包含：所有数据、脚本、schema 和存档都放在自己的游戏目录下。
5. 按分类 tutorial 检查结构和规范。
6. 在 README 的对应分类表格里补一行。
7. 提交 PR，说明游戏类型、触发方式、是否需要外部依赖，以及你测试过的启动流程。

