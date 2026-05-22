#!/usr/bin/env python3
"""
transition.py — 场景切换与存档更新
用法：
  python transition.py scene <scene_id> <save_path>        # 切换场景
  python transition.py flag <flag_name> <save_path>        # 设置剧情标志为 true
  python transition.py phase <phase_name> <save_path>      # 切换游戏阶段
  python transition.py status <save_path>                  # 查看当前状态摘要
  python transition.py ending <ending_id> <save_path>      # 触发结局
"""

import sys
import json
from pathlib import Path
from datetime import datetime

VALID_SCENES = [
    "scene_street", "scene_lobby", "scene_room207", "scene_police",
    "scene_library", "scene_basement_door", "scene_basement",
    "scene_altar", "scene_hidden_room", "scene_final_confrontation",
    "ending_a", "ending_b", "ending_c"
]

VALID_PHASES = ["character_creation", "act1", "act2", "act3", "ending"]

SCENE_TO_PHASE = {
    "scene_street":            "act1",
    "scene_lobby":             "act1",
    "scene_room207":           "act1",
    "scene_police":            "act1",
    "scene_library":           "act1",
    "scene_basement_door":     "act2",
    "scene_basement":          "act2",
    "scene_altar":             "act2",
    "scene_hidden_room":       "act2",
    "scene_final_confrontation": "act3",
    "ending_a":                "ending",
    "ending_b":                "ending",
    "ending_c":                "ending",
}


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


def switch_scene(scene_id: str, save_path: str):
    if scene_id not in VALID_SCENES:
        print(json.dumps({"error": f"无效场景ID: {scene_id}"}, ensure_ascii=False))
        sys.exit(1)
    
    state = load_state(save_path)
    prev_scene = state["scene"]
    
    # 记录已访问场景
    visited = state.get("visited_scenes", [])
    if prev_scene not in visited:
        visited.append(prev_scene)
    state["visited_scenes"] = visited
    
    state["scene"] = scene_id
    
    # 自动更新阶段
    new_phase = SCENE_TO_PHASE.get(scene_id, state["phase"])
    state["phase"] = new_phase
    
    # 记录时间戳
    state["last_updated"] = datetime.now().isoformat()
    
    save_state(state, save_path)
    print(json.dumps({
        "event": "scene_changed",
        "from": prev_scene,
        "to": scene_id,
        "phase": new_phase,
        "first_visit": scene_id not in visited
    }, ensure_ascii=False))


def set_flag(flag_name: str, save_path: str, value: bool = True):
    state = load_state(save_path)
    flags = state.get("flags", {})
    
    old_value = flags.get(flag_name, False)
    flags[flag_name] = value
    state["flags"] = flags
    
    save_state(state, save_path)
    print(json.dumps({
        "event": "flag_set",
        "flag": flag_name,
        "old_value": old_value,
        "new_value": value
    }, ensure_ascii=False))


def switch_phase(phase_name: str, save_path: str):
    if phase_name not in VALID_PHASES:
        print(json.dumps({"error": f"无效阶段: {phase_name}"}, ensure_ascii=False))
        sys.exit(1)
    
    state = load_state(save_path)
    old_phase = state["phase"]
    state["phase"] = phase_name
    
    save_state(state, save_path)
    print(json.dumps({
        "event": "phase_changed",
        "from": old_phase,
        "to": phase_name
    }, ensure_ascii=False))


def trigger_ending(ending_id: str, save_path: str):
    valid_endings = ["ending_a", "ending_b", "ending_c"]
    if ending_id not in valid_endings:
        print(json.dumps({"error": f"无效结局: {ending_id}"}, ensure_ascii=False))
        sys.exit(1)
    
    state = load_state(save_path)
    state["phase"] = "ending"
    state["scene"] = ending_id
    state["ended_at"] = datetime.now().isoformat()
    
    save_state(state, save_path)
    print(json.dumps({
        "event": "game_ended",
        "ending": ending_id,
        "player_name": state["player"]["name"],
        "final_hp": state["player"]["hp"],
        "final_sanity": state["player"]["sanity"],
        "clues_found": len(state.get("clues", []))
    }, ensure_ascii=False))


def tick_time(save_path: str, amount: int = 1):
    """推进时间，满10触发黑夜"""
    state = load_state(save_path)
    before = state.get("time_elapsed", 0)
    after = min(before + amount, 20)  # 上限20，防止溢出
    state["time_elapsed"] = after

    night_just_fallen = False
    if after >= 10 and not state.get("night_fallen", False):
        state["night_fallen"] = True
        night_just_fallen = True

    save_state(state, save_path)
    print(json.dumps({
        "event": "time_tick",
        "before": before,
        "after": after,
        "night_fallen": state["night_fallen"],
        "night_just_fallen": night_just_fallen,
        "remaining": max(0, 10 - after) if not state["night_fallen"] else 0
    }, ensure_ascii=False))


def advance_ritual(save_path: str):
    """推进仪式阶段"""
    state = load_state(save_path)
    stage = state.get("ritual_stage", 0)
    stage += 1
    state["ritual_stage"] = stage
    save_state(state, save_path)
    print(json.dumps({
        "event": "ritual_advanced",
        "stage": stage,
        "completed": stage >= 3
    }, ensure_ascii=False))


def get_status(save_path: str):
    state = load_state(save_path)
    player = state["player"]

    sanity = player["sanity"]
    sanity_max = player["sanity_max"]
    bar_len = 15
    filled = round(sanity / sanity_max * bar_len)
    sanity_bar = "#" * filled + "-" * (bar_len - filled)

    hp = player["hp"]
    hp_max = player["hp_max"]
    hp_filled = round(hp / hp_max * bar_len)
    hp_bar = "#" * hp_filled + "-" * (bar_len - hp_filled)

    time_elapsed = state.get("time_elapsed", 0)
    night_fallen = state.get("night_fallen", False)
    time_display = f"{time_elapsed}/10 {'【黑夜已降临】' if night_fallen else f'(还剩{max(0,10-time_elapsed)}点)'}"

    print(json.dumps({
        "phase": state["phase"],
        "scene": state["scene"],
        "time": time_display,
        "night_fallen": night_fallen,
        "ritual_stage": state.get("ritual_stage", 0),
        "player": {
            "name": player["name"],
            "occupation": player["occupation"],
            "hp": f"{hp}/{hp_max}  [{hp_bar}]",
            "sanity": f"{sanity}/{sanity_max}  [{sanity_bar}]",
        },
        "clues": state.get("clues", []),
        "flags": {k: v for k, v in state.get("flags", {}).items() if v is True},
        "inventory": [i["name"] for i in player.get("inventory", [])]
    }, ensure_ascii=False))


def trigger_ending(ending_id: str, save_path: str):
    valid_endings = ["ending_a", "ending_b", "ending_c", "ending_d"]
    if ending_id not in valid_endings:
        print(json.dumps({"error": f"无效结局: {ending_id}"}, ensure_ascii=False))
        sys.exit(1)

    state = load_state(save_path)
    state["phase"] = "ending"
    state["scene"] = ending_id
    state["ended_at"] = datetime.now().isoformat()

    save_state(state, save_path)
    print(json.dumps({
        "event": "game_ended",
        "ending": ending_id,
        "player_name": state["player"]["name"],
        "final_hp": state["player"]["hp"],
        "final_sanity": state["player"]["sanity"],
        "clues_found": len(state.get("clues", [])),
        "time_elapsed": state.get("time_elapsed", 0)
    }, ensure_ascii=False))


def main():
    args = sys.argv[1:]
    if not args:
        print("用法: python transition.py <command> [args...]")
        sys.exit(1)

    cmd = args[0]
    if cmd == "scene" and len(args) >= 3:
        switch_scene(args[1], args[2])
    elif cmd == "flag" and len(args) >= 3:
        set_flag(args[1], args[2])
    elif cmd == "phase" and len(args) >= 3:
        switch_phase(args[1], args[2])
    elif cmd == "ending" and len(args) >= 3:
        trigger_ending(args[1], args[2])
    elif cmd == "tick" and len(args) >= 2:
        amount = int(args[2]) if len(args) >= 3 else 1
        tick_time(args[1], amount)
    elif cmd == "ritual" and len(args) >= 2:
        advance_ritual(args[1])
    elif cmd == "status" and len(args) >= 2:
        get_status(args[1])
    else:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()

