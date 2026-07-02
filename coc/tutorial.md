# CoC Skill 开发规范

本目录收录克苏鲁的呼唤或相近调查跑团类游戏。一个游戏对应一个可独立安装的 skill，例如 [`brenner-apartment`](brenner-apartment/)。

## 目录结构

```text
coc/<game-slug>/
├── SKILL.md
├── data/
│   ├── story.md
│   ├── scenes.md
│   ├── npcs.md
│   ├── items.md
│   └── enemies.md
├── scripts/
│   ├── dice.py
│   ├── new_game.py
│   ├── transition.py
│   ├── sanity.py
│   ├── inventory.py
│   └── combat.py
├── schemas/
│   └── game_state.schema.json
└── saves/
```

`saves/` 用于运行时存档，可以保留为空目录或用占位文件确保目录存在。

## 命名与触发

1. 目录名、`SKILL.md` frontmatter 的 `name`、安装后的 skill 名必须一致，并使用 kebab-case。
2. `description` 只触发具体剧本名，例如 `布伦纳公寓` 或 `Brenner Apartment`。
3. 不要使用泛词触发，例如 `跑团`、`玩克苏鲁`、`开始游戏`。这些词会和其他 CoC 剧本互相抢触发。

推荐写法：

```yaml
---
name: brenner-apartment
description: Use ONLY when the user explicitly names the Call of Cthulhu scenario "布伦纳公寓" or "Brenner Apartment".
---
```

## SKILL.md 内容

`SKILL.md` 是 Agent 运行游戏的入口，建议至少包含这些部分：

1. 角色定位：说明 Agent 是 KP、叙述者和裁判。
2. 游戏边界：游戏开始后不能修改规则、跳过检定、直接给成功结果或剧透真相。
3. 新游戏流程：如何创建角色、选择职业和道具、调用建档脚本。
4. 继续游戏流程：如何读取存档、展示当前位置和可行动作。
5. 核心规则：时间推进、一次机会、线索互斥、理智、战斗、结局触发等。
6. 数据速查：说明剧情、场景、NPC、道具、敌人数据分别在哪些文件。
7. 脚本速查：列出每个脚本的命令格式。

## 路径规范

仓库里游戏位于 `coc/<game-slug>/`，但玩家安装时会复制具体游戏目录到 Agent 的 skills 目录。`SKILL.md` 内的运行命令应写成安装后的路径：

```bash
python skills/<game-slug>/scripts/new_game.py skills/<game-slug>/saves/game_state.json
```

不要在 `SKILL.md` 的命令里写 `coc/<game-slug>`，否则复制到 skills 目录后路径会失效。

## 数据与脚本规范

1. `data/story.md` 写背景、真相、关键时间线和结局条件。
2. `data/scenes.md` 写可探索场景、线索、检定难度和转场。
3. `data/npcs.md` 写 NPC 动机、话术边界和可透露信息。
4. `data/items.md` 写道具效果，避免让 Agent 临场发明规则外道具。
5. `scripts/` 只做确定性结算，例如掷骰、建档、扣理智、添加线索、切换结局。
6. `schemas/game_state.schema.json` 约束存档结构，避免多轮游戏后状态漂移。

## PR 自检

提交前请确认：

1. 可以按 README 复制具体游戏目录并触发。
2. `SKILL.md` 的 `name` 与目录名一致。
3. `description` 不含泛用触发词。
4. 新游戏和继续游戏命令可以执行。
5. 存档路径统一为 `skills/<game-slug>/saves/game_state.json`。
6. README 的 CoC 表格已经补充新游戏。
