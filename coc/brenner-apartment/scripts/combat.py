#!/usr/bin/env python3
"""
combat.py — 战斗结算模块
用法：
  python combat.py start <enemy_id> <save_path>       # 开始战斗
  python combat.py player_attack <weapon> <save_path> # 玩家攻击
  python combat.py player_flee <save_path>            # 玩家逃跑
  python combat.py player_item <item_id> <save_path>  # 使用道具
  python combat.py enemy_turn <save_path>             # 敌人回合
  python combat.py status <save_path>                 # 查看战斗状态

save_path: game_state.json 路径
"""

import sys
import json
import random
from pathlib import Path


# 敌人数据（与 enemies.md 对应）
ENEMIES = {
    "cultist": {
        "name": "邪教徒",
        "hp": 8,
        "attack_types": [
            {"name": "拳打脚踢", "damage": "1d4", "chance": 60},
            {"name": "持刀攻击", "damage": "1d6", "chance": 30},
            {"name": "试图逃跑", "damage": None, "chance": 10}
        ]
    },
    "corbitt_soul": {
        "name": "科比特之魂",
        "hp": 20,
        "immune_to_normal": True,  # 普通武器无效
        "attack_types": [
            {"name": "心灵撕裂", "damage": "1d6", "target": "sanity", "chance": 70},
            {"name": "幽灵之手", "damage": "1d4", "target": "hp", "chance": 30}
        ]
    }
}

# 武器数据
WEAPONS = {
    "unarmed":        {"name": "徒手", "damage": "1d3", "hit_skill": "近战", "normal": True},
    "revolver":       {"name": "左轮手枪", "damage": "1d10", "hit_skill": "射击", "normal": True},
    "ritual_dagger":  {"name": "仪式匕首", "damage": "1d6", "hit_skill": "近战", "normal": False}
}


def roll_dice(dice_str: str) -> int:
    """简单掷骰，格式：NdM"""
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


def start_combat(enemy_id: str, save_path: str):
    """初始化战斗"""
    if enemy_id not in ENEMIES:
        print(json.dumps({"error": f"未知敌人: {enemy_id}"}, ensure_ascii=False))
        sys.exit(1)
    
    state = load_state(save_path)
    enemy = ENEMIES[enemy_id]
    
    state["combat"] = {
        "in_combat": True,
        "enemy_id": enemy_id,
        "enemy_name": enemy["name"],
        "enemy_hp": enemy["hp"],
        "enemy_hp_max": enemy["hp"],
        "round": 1
    }
    
    save_state(state, save_path)
    print(json.dumps({
        "event": "combat_start",
        "enemy": enemy["name"],
        "enemy_hp": enemy["hp"],
        "player_hp": state["player"]["hp"],
        "player_sanity": state["player"]["sanity"],
        "round": 1
    }, ensure_ascii=False))


def player_attack(weapon_id: str, save_path: str):
    """玩家攻击回合"""
    state = load_state(save_path)
    combat = state.get("combat", {})
    
    if not combat.get("in_combat"):
        print(json.dumps({"error": "当前不在战斗中"}, ensure_ascii=False))
        sys.exit(1)
    
    weapon = WEAPONS.get(weapon_id, WEAPONS["unarmed"])
    enemy_id = combat["enemy_id"]
    enemy_data = ENEMIES[enemy_id]
    
    result = {
        "event": "player_attack",
        "weapon": weapon["name"],
        "round": combat["round"]
    }
    
    # 命中检定（d20，>=10 命中，简化规则）
    hit_roll = random.randint(1, 20)
    hit = hit_roll >= 10
    result["hit_roll"] = hit_roll
    result["hit"] = hit
    
    if hit:
        # 检查武器是否对该敌人有效
        if enemy_data.get("immune_to_normal") and weapon.get("normal", True):
            result["effect"] = "无效"
            result["message"] = f"{weapon['name']}对{enemy_data['name']}没有任何效果，它的形态根本无法被普通物品触碰。"
        else:
            damage = roll_dice(weapon["damage"])
            combat["enemy_hp"] = max(0, combat["enemy_hp"] - damage)
            result["damage"] = damage
            result["enemy_hp_remaining"] = combat["enemy_hp"]
            result["enemy_defeated"] = combat["enemy_hp"] <= 0
    else:
        result["message"] = "攻击落空"
    
    # 更新存档
    state["combat"] = combat
    save_state(state, save_path)
    print(json.dumps(result, ensure_ascii=False))


def enemy_turn(save_path: str):
    """敌人回合"""
    state = load_state(save_path)
    combat = state.get("combat", {})
    
    if not combat.get("in_combat") or combat.get("enemy_hp", 0) <= 0:
        print(json.dumps({"error": "敌人已失去战斗能力"}, ensure_ascii=False))
        sys.exit(1)
    
    enemy_id = combat["enemy_id"]
    enemy_data = ENEMIES[enemy_id]
    
    # 随机选择攻击方式
    roll = random.randint(1, 100)
    cumulative = 0
    chosen_attack = enemy_data["attack_types"][-1]
    for attack in enemy_data["attack_types"]:
        cumulative += attack["chance"]
        if roll <= cumulative:
            chosen_attack = attack
            break
    
    result = {
        "event": "enemy_turn",
        "enemy_name": enemy_data["name"],
        "action": chosen_attack["name"],
        "round": combat["round"]
    }
    
    if chosen_attack["damage"] is None:
        # 敌人逃跑
        result["enemy_fled"] = True
        combat["in_combat"] = False
    else:
        damage = roll_dice(chosen_attack["damage"])
        target = chosen_attack.get("target", "hp")
        
        if target == "sanity":
            state["player"]["sanity"] = max(0, state["player"]["sanity"] - damage)
            result["sanity_damage"] = damage
            result["player_sanity"] = state["player"]["sanity"]
            result["player_insane"] = state["player"]["sanity"] <= 0
        else:
            state["player"]["hp"] = max(0, state["player"]["hp"] - damage)
            result["hp_damage"] = damage
            result["player_hp"] = state["player"]["hp"]
            result["player_dead"] = state["player"]["hp"] <= 0
    
    # 进入下一回合
    combat["round"] = combat.get("round", 1) + 1
    state["combat"] = combat
    save_state(state, save_path)
    print(json.dumps(result, ensure_ascii=False))


def player_flee(save_path: str):
    """玩家逃跑（敏捷检定，d100 <= 敏捷技能值）"""
    state = load_state(save_path)
    agility = state["player"]["skills"].get("敏捷", 40)
    
    roll = random.randint(1, 100)
    success = roll <= agility
    
    result = {
        "event": "player_flee",
        "roll": roll,
        "agility": agility,
        "success": success
    }
    
    if success:
        state["combat"]["in_combat"] = False
        result["message"] = "成功脱身"
    else:
        # 失败：敌人获得一次免费攻击
        damage = roll_dice("1d4")
        state["player"]["hp"] = max(0, state["player"]["hp"] - damage)
        result["flee_damage"] = damage
        result["player_hp"] = state["player"]["hp"]
        result["message"] = "逃跑失败，受到攻击"
        # 科比特之魂额外心灵攻击
        if state["combat"].get("enemy_id") == "corbitt_soul":
            sanity_damage = roll_dice("1d6")
            state["player"]["sanity"] = max(0, state["player"]["sanity"] - sanity_damage)
            result["sanity_damage"] = sanity_damage
            result["player_sanity"] = state["player"]["sanity"]
    
    save_state(state, save_path)
    print(json.dumps(result, ensure_ascii=False))


def get_status(save_path: str):
    """获取当前战斗状态"""
    state = load_state(save_path)
    combat = state.get("combat", {})
    print(json.dumps({
        "in_combat": combat.get("in_combat", False),
        "round": combat.get("round", 0),
        "enemy_name": combat.get("enemy_name", ""),
        "enemy_hp": combat.get("enemy_hp", 0),
        "enemy_hp_max": combat.get("enemy_hp_max", 0),
        "player_hp": state["player"]["hp"],
        "player_hp_max": state["player"]["hp_max"],
        "player_sanity": state["player"]["sanity"]
    }, ensure_ascii=False))


def main():
    args = sys.argv[1:]
    if not args:
        print("用法: python combat.py <command> [args...]")
        sys.exit(1)
    
    cmd = args[0]
    if cmd == "start" and len(args) >= 3:
        start_combat(args[1], args[2])
    elif cmd == "player_attack" and len(args) >= 3:
        player_attack(args[1], args[2])
    elif cmd == "enemy_turn" and len(args) >= 2:
        enemy_turn(args[1])
    elif cmd == "player_flee" and len(args) >= 2:
        player_flee(args[1])
    elif cmd == "status" and len(args) >= 2:
        get_status(args[1])
    else:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
