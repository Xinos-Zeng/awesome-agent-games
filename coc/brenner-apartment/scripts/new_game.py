#!/usr/bin/env python3
"""
new_game.py — 初始化新游戏存档
用法：
  python new_game.py <save_path> <name> <occupation> <item1> <item2> [skill_points_json]

occupation: 私家侦探 | 记者 | 学者
item1/item2: 初始选择的两件道具 ID（见 items.md）

skill_points_json: 可选，格式为 JSON 字符串，用于额外分配技能点
  例如：'{"调查": 10, "说服": 5}'
  不传则使用职业默认值

职业默认技能值：
  私家侦探: 调查60, 说服50, 潜行45, 近战40, 射击45, 急救35, 神秘学20, 意志50, 敏捷45, 图书馆利用40
  记者:     调查50, 说服60, 潜行35, 近战30, 射击30, 急救30, 神秘学25, 意志45, 敏捷40, 图书馆利用55
  学者:     调查45, 说服40, 潜行25, 近战25, 射击25, 急救40, 神秘学55, 意志55, 敏捷35, 图书馆利用65
"""

import sys
import json
from pathlib import Path
from datetime import datetime

OCCUPATION_SKILLS = {
    "私家侦探": {
        "调查": 60, "说服": 50, "潜行": 45, "近战": 40,
        "射击": 45, "急救": 35, "神秘学": 20,
        "意志": 50, "敏捷": 45, "图书馆利用": 40
    },
    "记者": {
        "调查": 50, "说服": 60, "潜行": 35, "近战": 30,
        "射击": 30, "急救": 30, "神秘学": 25,
        "意志": 45, "敏捷": 40, "图书馆利用": 55
    },
    "学者": {
        "调查": 45, "说服": 40, "潜行": 25, "近战": 25,
        "射击": 25, "急救": 40, "神秘学": 55,
        "意志": 55, "敏捷": 35, "图书馆利用": 65
    }
}

OCCUPATION_SANITY = {
    "私家侦探": 60,
    "记者": 55,
    "学者": 65
}

VALID_ITEMS = [
    "pocket_watch", "notebook", "lighter",
    "first_aid_kit", "flask", "revolver"
]

ITEM_DATA = {
    "pocket_watch":  {"name": "怀表",     "count": -1},
    "notebook":      {"name": "笔记本",   "count": -1},
    "lighter":       {"name": "打火机",   "count": -1},
    "first_aid_kit": {"name": "急救包",   "count": 3},
    "flask":         {"name": "酒壶",     "count": 1},
    "revolver":      {"name": "左轮手枪", "count": 6},
}


def create_save(save_path: str, name: str, occupation: str,
                item1: str, item2: str, extra_skills: dict = None):
    
    if occupation not in OCCUPATION_SKILLS:
        print(json.dumps({"error": f"无效职业: {occupation}，可选: 私家侦探 | 记者 | 学者"}, ensure_ascii=False))
        sys.exit(1)
    
    for item in [item1, item2]:
        if item not in VALID_ITEMS:
            print(json.dumps({"error": f"无效道具: {item}"}, ensure_ascii=False))
            sys.exit(1)
    
    skills = dict(OCCUPATION_SKILLS[occupation])
    if extra_skills:
        for skill, points in extra_skills.items():
            if skill in skills:
                skills[skill] = min(99, skills[skill] + points)
    
    # 构建背包（去重）
    chosen_items = list(dict.fromkeys([item1, item2]))
    inventory = []
    for item_id in chosen_items:
        data = ITEM_DATA[item_id]
        inventory.append({"id": item_id, "name": data["name"], "count": data["count"]})
    
    sanity_max = OCCUPATION_SANITY[occupation]
    
    game_state = {
        "version": "1.1",
        "created_at": datetime.now().isoformat(),
        "phase": "act1",
        "scene": "scene_street",
        "time_elapsed": 0,
        "night_fallen": False,
        "ritual_stage": 0,
        "player": {
            "name": name,
            "occupation": occupation,
            "hp": 10,
            "hp_max": 10,
            "sanity": sanity_max,
            "sanity_max": sanity_max,
            "skills": skills,
            "inventory": inventory
        },
        "flags": {
            "talked_to_mrs_chen": False,
            "talked_to_mrs_chen_deep": False,
            "mrs_chen_closed_door": False,
            "talked_to_officer_riley": False,
            "deep_investigated_police": False,
            "deep_investigated_library": False,
            "visited_library": False,
            "searched_room207_desk": False,
            "searched_room207_wardrobe": False,
            "basement_unlocked": False,
            "cultist_encountered": False,
            "cultist_defeated": False,
            "altar_found": False,
            "altar_symbols_checked": False,
            "altar_searched": False,
            "hidden_room_found": False,
            "hidden_room_read": False,
            "corbitt_appeared": False
        },
        "clues": [],
        "combat": {
            "in_combat": False,
            "enemy_id": "",
            "enemy_name": "",
            "enemy_hp": 0,
            "enemy_hp_max": 0,
            "round": 0
        },
        "visited_scenes": []
    }
    
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(game_state, f, ensure_ascii=False, indent=2)
    
    print(json.dumps({
        "event": "game_created",
        "name": name,
        "occupation": occupation,
        "sanity": sanity_max,
        "hp": 10,
        "skills": skills,
        "inventory": [i["name"] for i in inventory],
        "save_path": save_path
    }, ensure_ascii=False))


def main():
    args = sys.argv[1:]
    if len(args) < 5:
        print("用法: python new_game.py <save_path> <name> <occupation> <item1> <item2> [skill_points_json]")
        sys.exit(1)
    
    save_path = args[0]
    name = args[1]
    occupation = args[2]
    item1 = args[3]
    item2 = args[4]
    extra_skills = json.loads(args[5]) if len(args) > 5 else None
    
    create_save(save_path, name, occupation, item1, item2, extra_skills)


if __name__ == "__main__":
    main()
