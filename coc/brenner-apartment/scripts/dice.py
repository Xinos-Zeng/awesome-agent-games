#!/usr/bin/env python3
"""
dice.py — 掷骰模块
用法：
  python dice.py d6          # 掷一个6面骰
  python dice.py d100        # 掷百面骰（技能检定用）
  python dice.py 2d6         # 掷两个6面骰求和
  python dice.py d20 +3      # 掷d20加修正值
  python dice.py check 45    # 技能检定：掷d100，目标值45，返回成功/失败
"""

import sys
import random
import re
import json


def roll(dice_str: str) -> dict:
    """解析并掷骰，返回结果字典"""
    dice_str = dice_str.strip().lower()
    
    # 匹配格式：[N]dM 或 dM
    pattern = r'^(\d*)d(\d+)$'
    match = re.match(pattern, dice_str)
    if not match:
        return {"error": f"无法解析骰子格式: {dice_str}"}
    
    count = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    
    if count < 1 or count > 20:
        return {"error": "骰子数量需在1-20之间"}
    if sides < 2 or sides > 100:
        return {"error": "面数需在2-100之间"}
    
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)
    
    return {
        "dice": f"{count}d{sides}",
        "rolls": rolls,
        "total": total
    }


def skill_check(skill_value: int, modifier: int = 0) -> dict:
    """
    技能检定：掷d100，结果 <= (技能值 + 修正) 为成功
    返回结果字典
    """
    d100_result = random.randint(1, 100)
    effective_value = skill_value + modifier
    success = d100_result <= effective_value
    
    # 大成功/大失败判定
    critical_success = d100_result <= max(1, effective_value // 5)
    fumble = d100_result >= 96
    
    level = "大成功" if critical_success else ("成功" if success else ("大失败" if fumble else "失败"))
    
    return {
        "roll": d100_result,
        "skill_value": skill_value,
        "modifier": modifier,
        "effective_value": effective_value,
        "success": success,
        "critical_success": critical_success,
        "fumble": fumble,
        "level": level
    }


def sanity_check(current_sanity: int, difficulty: int = 50) -> dict:
    """
    理智检定：掷d100，结果 <= current_sanity 为成功
    difficulty 用于调整（难度越高，检定越难）
    实际上COC中理智检定是直接用当前理智值作目标
    """
    return skill_check(current_sanity)


def main():
    args = sys.argv[1:]
    
    if not args:
        print(json.dumps({"error": "请提供参数，例如：python dice.py d6"}, ensure_ascii=False))
        sys.exit(1)
    
    # 技能检定模式
    if args[0] == "check":
        if len(args) < 2:
            print(json.dumps({"error": "请提供技能值，例如：python dice.py check 45"}, ensure_ascii=False))
            sys.exit(1)
        skill_val = int(args[1])
        modifier = int(args[2]) if len(args) > 2 else 0
        result = skill_check(skill_val, modifier)
        print(json.dumps(result, ensure_ascii=False))
        return
    
    # 理智检定模式
    if args[0] == "sanity":
        if len(args) < 2:
            print(json.dumps({"error": "请提供当前理智值"}, ensure_ascii=False))
            sys.exit(1)
        sanity_val = int(args[1])
        result = sanity_check(sanity_val)
        print(json.dumps(result, ensure_ascii=False))
        return
    
    # 普通掷骰模式
    dice_str = args[0]
    modifier = int(args[1]) if len(args) > 1 and args[1].lstrip('+-').isdigit() else 0
    
    result = roll(dice_str)
    if modifier != 0:
        result["modifier"] = modifier
        result["final_total"] = result["total"] + modifier
    
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
