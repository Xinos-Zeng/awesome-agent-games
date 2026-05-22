#!/usr/bin/env python3
"""
inventory.py — 背包与道具管理
用法：
  python inventory.py list <save_path>              # 列出背包
  python inventory.py add <item_id> <save_path>     # 添加道具
  python inventory.py use <item_id> <save_path>     # 使用道具（消耗品）
  python inventory.py has <item_id> <save_path>     # 检查是否持有某道具
  python inventory.py add_clue <clue_id> <save_path> # 添加线索
  python inventory.py clues <save_path>             # 列出已发现的线索
"""

import sys
import json
import random
from pathlib import Path


# 道具数据（与 items.md 对应）
ITEMS = {
    "pocket_watch":       {"name": "怀表",     "type": "tool",       "count": -1},
    "notebook":           {"name": "笔记本",   "type": "tool",       "count": -1},
    "lighter":            {"name": "打火机",   "type": "tool",       "count": -1},
    "first_aid_kit":      {"name": "急救包",   "type": "consumable", "count": 3},
    "flask":              {"name": "酒壶",     "type": "consumable", "count": 1},
    "revolver":           {"name": "左轮手枪", "type": "weapon",     "count": 6},
    "old_key":            {"name": "锈铁钥匙", "type": "plot",       "count": -1},
    "corbitt_diary":      {"name": "科比特日记", "type": "plot",     "count": -1},
    "strange_manuscript": {"name": "奇异手稿", "type": "plot",       "count": -1},
    "ritual_dagger":      {"name": "仪式匕首", "type": "weapon",     "count": -1},
    "library_record":     {"name": "档案记录", "type": "plot",       "count": -1},
}

# 道具使用效果
ITEM_EFFECTS = {
    "first_aid_kit": {
        "skill_required": "急救",
        "skill_value_key": "急救",
        "on_success": {"hp": "1d4"},
        "on_fail": {"hp": 0},
        "message_success": "你稳定地处理了伤口，感觉好多了。",
        "message_fail": "你笨拙地包扎，没有明显效果。"
    },
    "flask": {
        "skill_required": None,
        "on_use": {"sanity": 3},
        "message": "酒液灼烧喉咙，现实感稍微回来了一些。"
    }
}


def roll_dice(dice_str: str) -> int:
    if "d" not in dice_str:
        return int(dice_str)
    parts = dice_str.split("d")
    count = int(parts[0]) if parts[0] else 1
    sides = int(parts[1])
    return sum(random.randint(1, sides) for _ in range(count))


def load_state(save_path: str) -> dict:
    path = Path(save_path)
    if not path.exists():
        print(json.dumps({"error": f"存档文件不存在: {save_path}"}, ensure_ascii=False))
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict, save_path: str):
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def find_item(inventory: list, item_id: str) -> dict | None:
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def list_inventory(save_path: str):
    state = load_state(save_path)
    inventory = state["player"]["inventory"]
    clues = state.get("clues", [])
    
    items_display = []
    for item in inventory:
        item_def = ITEMS.get(item["id"], {})
        count_str = f"x{item['count']}" if item["count"] > 0 else "∞"
        items_display.append({
            "id": item["id"],
            "name": item["name"],
            "count": count_str,
            "type": item_def.get("type", "unknown")
        })
    
    print(json.dumps({
        "inventory": items_display,
        "clue_count": len(clues)
    }, ensure_ascii=False))


def add_item(item_id: str, save_path: str):
    if item_id not in ITEMS:
        print(json.dumps({"error": f"未知道具: {item_id}"}, ensure_ascii=False))
        sys.exit(1)
    
    state = load_state(save_path)
    inventory = state["player"]["inventory"]
    
    existing = find_item(inventory, item_id)
    item_def = ITEMS[item_id]
    
    if existing:
        if existing["count"] > 0:
            existing["count"] += item_def["count"]
        print(json.dumps({"event": "item_added", "item": item_id, "name": item_def["name"], "already_had": True}, ensure_ascii=False))
    else:
        inventory.append({
            "id": item_id,
            "name": item_def["name"],
            "count": item_def["count"]
        })
        print(json.dumps({"event": "item_added", "item": item_id, "name": item_def["name"], "already_had": False}, ensure_ascii=False))
    
    save_state(state, save_path)


def use_item(item_id: str, save_path: str):
    state = load_state(save_path)
    inventory = state["player"]["inventory"]
    existing = find_item(inventory, item_id)
    
    if not existing:
        print(json.dumps({"error": f"背包中没有: {item_id}"}, ensure_ascii=False))
        sys.exit(1)
    
    effect_def = ITEM_EFFECTS.get(item_id)
    if not effect_def:
        print(json.dumps({"error": f"该道具不可主动使用: {item_id}"}, ensure_ascii=False))
        sys.exit(1)
    
    result = {"event": "item_used", "item": item_id}
    
    # 需要技能检定的道具（如急救包）
    if effect_def.get("skill_required"):
        skill_key = effect_def["skill_value_key"]
        skill_val = state["player"]["skills"].get(skill_key, 30)
        roll = random.randint(1, 100)
        success = roll <= skill_val
        result["skill_check"] = {"skill": skill_key, "roll": roll, "skill_val": skill_val, "success": success}
        
        if success:
            hp_gain = roll_dice(effect_def["on_success"]["hp"])
            state["player"]["hp"] = min(state["player"]["hp_max"], state["player"]["hp"] + hp_gain)
            result["hp_restored"] = hp_gain
            result["message"] = effect_def["message_success"]
        else:
            result["hp_restored"] = 0
            result["message"] = effect_def["message_fail"]
    
    # 无需检定的道具（如酒壶）
    elif effect_def.get("on_use"):
        effects = effect_def["on_use"]
        if "sanity" in effects:
            restore = effects["sanity"]
            state["player"]["sanity"] = min(state["player"]["sanity_max"], state["player"]["sanity"] + restore)
            result["sanity_restored"] = restore
        result["message"] = effect_def.get("message", "")
    
    # 消耗使用次数
    if existing["count"] > 0:
        existing["count"] -= 1
        if existing["count"] <= 0:
            inventory.remove(existing)
            result["item_consumed"] = True
    
    result["player_hp"] = state["player"]["hp"]
    result["player_sanity"] = state["player"]["sanity"]
    
    save_state(state, save_path)
    print(json.dumps(result, ensure_ascii=False))


def has_item(item_id: str, save_path: str):
    state = load_state(save_path)
    inventory = state["player"]["inventory"]
    existing = find_item(inventory, item_id)
    print(json.dumps({
        "has": existing is not None,
        "item_id": item_id,
        "count": existing["count"] if existing else 0
    }, ensure_ascii=False))


def add_clue(clue_id: str, save_path: str):
    state = load_state(save_path)
    clues = state.get("clues", [])
    already_have = clue_id in clues
    
    if not already_have:
        clues.append(clue_id)
        state["clues"] = clues
        save_state(state, save_path)
    
    print(json.dumps({
        "event": "clue_added",
        "clue_id": clue_id,
        "already_had": already_have,
        "total_clues": len(clues)
    }, ensure_ascii=False))


def list_clues(save_path: str):
    state = load_state(save_path)
    print(json.dumps({
        "clues": state.get("clues", []),
        "total": len(state.get("clues", []))
    }, ensure_ascii=False))


def main():
    args = sys.argv[1:]
    if not args:
        print("用法: python inventory.py <command> [args...]")
        sys.exit(1)
    
    cmd = args[0]
    if cmd == "list" and len(args) >= 2:
        list_inventory(args[1])
    elif cmd == "add" and len(args) >= 3:
        add_item(args[1], args[2])
    elif cmd == "use" and len(args) >= 3:
        use_item(args[1], args[2])
    elif cmd == "has" and len(args) >= 3:
        has_item(args[1], args[2])
    elif cmd == "add_clue" and len(args) >= 3:
        add_clue(args[1], args[2])
    elif cmd == "clues" and len(args) >= 2:
        list_clues(args[1])
    else:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
