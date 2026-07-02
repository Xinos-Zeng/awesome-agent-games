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

## 效果预览

这些片段只展示游玩形式，不包含关键线索、真相、路线条件或结局剧透。

### CoC 跑团

```text
玩家：我想玩布伦纳公寓

KP：
🕯️ 布伦纳公寓
— 波士顿雨夜，一栋不愿保持沉默的旧公寓 —

1923 年，波士顿。

雨水沿着红砖墙往下淌，街灯在积水里碎成昏黄的斑点。你站在布伦纳公寓门前，手里攥着房东交给你的钥匙。

传闻里，过去三位租客都在这里住到精神崩溃。有人说是煤气泄漏，有人说是孤独、贫穷和战争留下的阴影。

但当你抬头看向二楼那扇没有亮灯的窗户时，忽然觉得——有什么东西也正在看着你。

你好，调查员。欢迎来到布伦纳公寓。

请先创建你的角色。

请选择职业：
[1] 私家侦探
[2] 记者
[3] 学者

请选择随身携带的 2 件物品：
[A] 打火机  [B] 笔记本  [C] 怀表
[D] 急救包  [E] 酒壶    [F] 左轮手枪
```

### Galgame

```text
玩家：我想玩汐見学園の七日間

Narrator：
🌊 汐見学園の七日間
— 海边的学园，静止的灯塔，永无止境的七天 —

在悬崖之上，有一所名为「汐見学園」的私立高中。

昭和风格的旧校舍，远处灰白色的废弃灯塔， 以及——过于宁静的、仿佛被精心维护的空气。

据说，每到第七天的午夜零点， 一切都会重置回第一天的清晨。

但你什么都不记得了。

你只知道——今天，是你转学的第一天。

你好，玩家。欢迎来到汐見学園的故事 🌙

请问主角叫什么名字？ （直接输入名字即可，留空则使用默认名：長谷川蓮）
```

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

