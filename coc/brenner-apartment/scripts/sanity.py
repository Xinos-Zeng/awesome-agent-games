#!/usr/bin/env python3
"""
sanity.py — 理智值管理模块
用法：
  python sanity.py check <save_path>              # 理智检定（用当前理智值作目标）
  python sanity.py lose <amount> <save_path>      # 直接扣减理智（已经过检定后用）
  python sanity.py restore <amount> <save_path>   # 恢复理智
  python sanity.py roll_loss <dice> <save_path>   # 掷骰扣减（如 1d6）
  python sanity.py status <save_path>             # 查看理智状态

理智状态等级：
  60+    正常
  40-59  轻度不安（Agent可偶尔叙述玩家"感到不安"）
  20-39  中度扭曲（Agent叙述时偶尔加入幻觉片段）
  1-19   严重崩溃（叙述中频繁出现异常感知）
  0      疯狂——游戏结束，触发结局B
"""

import sys
import json
import random
from pathlib import Path


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


def get_sanity_level(sanity: int) -> dict:
    """返回理智状态描述"""
    if sanity >= 60:
        return {"level": "normal", "label": "正常", "hint": ""}
    elif sanity >= 40:
        return {"level": "uneasy", "label": "轻度不安", "hint": "偶尔感到难以名状的不适"}
    elif sanity >= 20:
        return {"level": "disturbed", "label": "中度扭曲", "hint": "现实感开始模糊，偶有幻觉"}
    elif sanity >= 1:
        return {"level": "breaking", "label": "严重崩溃", "hint": "思维频繁混乱，难以集中注意力"}
    else:
        return {"level": "insane", "label": "彻底疯狂", "hint": "游戏结束"}


def sanity_check(save_path: str) -> dict:
    """
    理智检定：掷d100，结果 <= 当前理智值 = 成功
    返回完整检定结果
    """
    state = load_state(save_path)
    current_sanity = state["player"]["sanity"]
    
    roll = random.randint(1, 100)
    success = roll <= current_sanity
    
    result = {
        "event": "sanity_check",
        "roll": roll,
        "sanity": current_sanity,
        "success": success,
        "level": "成功" if success else "失败"
    }
    
    return result, state


def lose_sanity(amount: int, save_path: str, from_roll: bool = False, dice_str: str = ""):
    """扣减理智值"""
    state = load_state(save_path)
    before = state["player"]["sanity"]
    
    actual_loss = roll_dice(dice_str) if from_roll else amount
    state["player"]["sanity"] = max(0, before - actual_loss)
    after = state["player"]["sanity"]
    
    sanity_level = get_sanity_level(after)
    went_insane = after <= 0
    
    result = {
        "event": "sanity_loss",
        "before": before,
        "loss": actual_loss,
        "after": after,
        "dice": dice_str if from_roll else None,
        "sanity_level": sanity_level,
        "went_insane": went_insane
    }
    
    # 若已疯狂，更新游戏阶段
    if went_insane:
        state["phase"] = "ending"
        state["scene"] = "ending_b"
    
    save_state(state, save_path)
    print(json.dumps(result, ensure_ascii=False))


def restore_sanity(amount: int, save_path: str):
    """恢复理智值"""
    state = load_state(save_path)
    before = state["player"]["sanity"]
    max_sanity = state["player"]["sanity_max"]
    
    state["player"]["sanity"] = min(max_sanity, before + amount)
    after = state["player"]["sanity"]
    
    result = {
        "event": "sanity_restore",
        "before": before,
        "restored": amount,
        "after": after,
        "sanity_level": get_sanity_level(after)
    }
    
    save_state(state, save_path)
    print(json.dumps(result, ensure_ascii=False))


def get_status(save_path: str):
    state = load_state(save_path)
    sanity = state["player"]["sanity"]
    max_sanity = state["player"]["sanity_max"]
    level = get_sanity_level(sanity)
    
    # 生成理智条
    bar_length = 20
    filled = round(sanity / max_sanity * bar_length)
    bar = "#" * filled + "-" * (bar_length - filled)
    
    print(json.dumps({
        "sanity": sanity,
        "sanity_max": max_sanity,
        "bar": bar,
        "level": level
    }, ensure_ascii=False))


def main():
    args = sys.argv[1:]
    if not args:
        print("用法: python sanity.py <command> [args...]")
        sys.exit(1)
    
    cmd = args[0]
    
    if cmd == "check" and len(args) >= 2:
        result, state = sanity_check(args[1])
        print(json.dumps(result, ensure_ascii=False))
    
    elif cmd == "lose" and len(args) >= 3:
        lose_sanity(int(args[1]), args[2])
    
    elif cmd == "roll_loss" and len(args) >= 3:
        lose_sanity(0, args[2], from_roll=True, dice_str=args[1])
    
    elif cmd == "restore" and len(args) >= 3:
        restore_sanity(int(args[1]), args[2])
    
    elif cmd == "status" and len(args) >= 2:
        get_status(args[1])
    
    else:
        print(json.dumps({"error": f"未知命令或参数不足: {' '.join(args)}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
