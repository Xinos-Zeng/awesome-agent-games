# Galgame Skill 开发规范

本目录收录 Galgame、视觉小说和恋爱冒险类游戏。一个游戏对应一个可独立安装的 skill，例如 [`shiomi-academy-seven-days`](shiomi-academy-seven-days/)。

## 目录结构

```text
galgame/<game-slug>/
├── SKILL.md
├── data/
│   ├── story.md
│   ├── characters.md
│   └── scenes.md
├── scripts/
│   └── game_engine.py
└── saves/
```

复杂项目可以继续拆分 `data/routes.md`、`data/endings.md` 或 `schemas/`，但一个游戏内的数据和脚本必须自包含。

## 命名与触发

1. 目录名、`SKILL.md` frontmatter 的 `name`、安装后的 skill 名必须一致，并使用 kebab-case。
2. skill 名应与具体游戏内容关联，例如 `shiomi-academy-seven-days`，不要使用 `galgame` 这种分类名。
3. `description` 只触发具体游戏名，例如 `汐見学園の七日間` 或 `Shiomi Academy Seven Days`。
4. 不要使用泛词触发，例如 `galgame`、`恋爱游戏`、`视觉小说`、`开始游戏`。这些词会和未来其他 Galgame 互相抢触发。

推荐写法：

```yaml
---
name: shiomi-academy-seven-days
description: Use ONLY when the user explicitly names the visual novel "汐見学園の七日間" or "Shiomi Academy Seven Days".
---
```

## SKILL.md 内容

`SKILL.md` 是 Agent 运行游戏的入口，建议至少包含这些部分：

1. 角色定位：说明 Agent 是叙事者，负责第二人称叙述、扮演 NPC、维护好感度和 flag。
2. 游戏边界：游戏开始后不能修改好感度、跳过选择、直接跳结局、查看未触发场景或开上帝视角。
3. 新游戏流程：展示背景、询问主角名、调用脚本创建存档。
4. 继续游戏流程：读取存档，展示当前场景和可用选择。
5. 场景节点系统：区分关键事件、装饰细节和选项节点。
6. 数值系统：说明好感度、flag、路线锁定和结局触发条件。
7. 对话规范：列出主要角色的说话风格、禁忌信息和伏笔边界。
8. 脚本速查：列出 `new`、`choose`、`advance`、`status`、`check_route` 等命令。

## 路径规范

仓库里游戏位于 `galgame/<game-slug>/`，但玩家安装时会复制具体游戏目录到 Agent 的 skills 目录。`SKILL.md` 内的运行命令应写成安装后的路径：

```bash
python skills/<game-slug>/scripts/game_engine.py new skills/<game-slug>/saves/game_state.json "<主角名>"
```

不要在 `SKILL.md` 的命令里写 `galgame/<game-slug>`，否则复制到 skills 目录后路径会失效。

## 数据规范

1. `data/story.md` 写世界观、核心设定、路线主题和真相，不直接暴露给玩家。
2. `data/characters.md` 写角色档案、说话风格、关系推进和关键秘密。
3. `data/scenes.md` 写场景节点、关键事件、选项、路线条件和结局。
4. 关键剧情必须写在数据文件中，Agent 只能补充氛围和过渡，不能临场发明主线。
5. 装饰细节可以允许 Agent 即兴发挥，但必须标明不会影响路线和结局。

## 脚本规范

1. 脚本负责确定性状态变更，例如建档、选择、推进场景、更新好感度和 flag。
2. 选择 ID 应稳定，不要依赖选项显示顺序。
3. 路线锁定和结局条件应由脚本校验，避免 Agent 凭记忆判断。
4. 每次行动前读取存档，每次行动后写回存档并展示状态。
5. 存档路径统一为 `skills/<game-slug>/saves/game_state.json`。

## PR 自检

提交前请确认：

1. 可以按 README 复制具体游戏目录并触发。
2. `SKILL.md` 的 `name` 与目录名一致。
3. `description` 不含泛用触发词。
4. 新游戏、选择、推进和状态查看命令可以执行。
5. 所有脚本命令使用 `skills/<game-slug>/...` 路径。
6. README 的 Galgame 表格已经补充新游戏。
