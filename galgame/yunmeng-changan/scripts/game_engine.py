#!/usr/bin/env python3
"""
云梦长安 — 乙女游戏状态引擎.

Usage:
    python game_engine.py new <save> <name>
    python game_engine.py choose <save> <choice_id>
    python game_engine.py advance <save> <scene_id>
    python game_engine.py flag <save> <flag_name> [true|false]
    python game_engine.py affection <save> <character> <delta>
    python game_engine.py check_route <save>
    python game_engine.py status <save>
    python game_engine.py list_flags <save>
    python game_engine.py get_affection <save> <character>
"""

import json, sys, os, re
from datetime import datetime

# ─── choice definitions ───
# Each choice_id maps to a dict of effects:
#   affection: {character: delta}
#   flags: {flag_name: value}
#   next_scene: scene_id (optional)
CHOICES = {
    # === Chapter 1: 觉醒 (Day 1-2) ===

    # ch1_guqinghan: 第一次遇到顾清寒
    "c1_gu_ask_who": {
        "affection": {},
        "flags": {"asked_gu_identity": True},
    },
    "c1_gu_ask_lingjie": {
        "affection": {},
        "flags": {"asked_about_lingjie": True},
    },
    "c1_gu_silent": {
        "affection": {"guqinghan": 1},
        "flags": {"gu_impressed_by_calm": True},
    },

    # ch1_sumobai: 第一次遇到苏墨白
    "c1_su_ask_who": {
        "affection": {},
        "flags": {"asked_su_identity": True},
    },
    "c1_su_ask_her": {
        "affection": {"sumobai": 1},
        "flags": {"asked_about_her": True},
    },
    "c1_su_stay_alert": {
        "affection": {"sumobai": 2},
        "flags": {"su_impressed_by_courage": True},
    },

    # ch1_peijinzhe: 裴惊蛰回来
    "c1_pei_welcome": {
        "affection": {"peijinzhe": 2},
        "flags": {"pei_welcomed": True},
    },
    "c1_pei_independent": {
        "affection": {},
        "flags": {"pei_hurt_but_understands": True},
    },
    "c1_pei_curious": {
        "affection": {"peijinzhe": 1},
        "flags": {"pei_recognized": True},
    },

    # ch1_lingjie: 灵界入口，选择第一个盟友
    "c1_ling_ally_gu": {
        "affection": {"guqinghan": 2},
        "flags": {"first_ally_gu": True},
    },
    "c1_ling_ally_su": {
        "affection": {"sumobai": 2},
        "flags": {"first_ally_su": True},
    },
    "c1_ling_ally_pei": {
        "affection": {"peijinzhe": 2},
        "flags": {"first_ally_pei": True},
    },

    # === Chapter 2: 羁绊 (Day 3-4) ===

    # ch2_morning: 选择调查方向
    "c2_route_gu": {
        "affection": {},
        "flags": {"ch2_route": "gu"},
        "next_scene": "ch2_guqinghan_route",
    },
    "c2_route_su": {
        "affection": {},
        "flags": {"ch2_route": "su"},
        "next_scene": "ch2_sumobai_route",
    },
    "c2_route_pei": {
        "affection": {},
        "flags": {"ch2_route": "pei"},
        "next_scene": "ch2_peijinzhe_route",
    },

    # ch2_guqinghan_route: 图书馆
    "c2_gu_question": {
        "affection": {"guqinghan": 1},
        "flags": {"questioned_gu": True},
    },
    "c2_gu_thank": {
        "affection": {"guqinghan": 2},
        "flags": {"thanked_gu": True},
    },
    "c2_gu_ask_identity": {
        "affection": {"guqinghan": 1},
        "flags": {"asked_shen_yunmeng": True},
    },

    # ch2_sumobai_route: 狐族领地
    "c2_su_assert_self": {
        "affection": {"sumobai": 2},
        "flags": {"asserted_identity": True},
    },
    "c2_su_empathize": {
        "affection": {"sumobai": 2},
        "flags": {"empathized_with_su": True},
    },
    "c2_su_rational": {
        "affection": {"sumobai": 1},
        "flags": {"asked_about_sacrifice": True},
    },

    # ch2_peijinzhe_route: 道观
    "c2_pei_promise": {
        "affection": {"peijinzhe": 2},
        "flags": {"asked_about_promise": True},
    },
    "c2_pei_direct": {
        "affection": {"peijinzhe": 2},
        "flags": {"asked_why_daoshi": True},
    },
    "c2_pei_thank": {
        "affection": {"peijinzhe": 1},
        "flags": {"thanked_pei": True},
    },

    # ch2_converge: 战斗后关心谁
    "c2_worry_gu": {
        "affection": {"guqinghan": 1},
        "flags": {"worried_gu": True},
    },
    "c2_worry_su": {
        "affection": {"sumobai": 1},
        "flags": {"worried_su": True},
    },
    "c2_worry_pei": {
        "affection": {"peijinzhe": 1},
        "flags": {"worried_pei": True},
    },

    # ch2_evening: 城墙对话
    "c2_eve_sacrifice": {
        "affection": {},
        "flags": {"asked_about_sacrifice_cost": True},
    },
    "c2_eve_identity": {
        "affection": {},
        "flags": {"asked_if_shen_yunmeng": True},
    },
    "c2_eve_moon": {
        "affection": {},
        "flags": {"moonlight_moment": True},
    },

    # === Chapter 3: 真相 (Day 5-6) ===

    # ch3_temple: 古寺分工
    "c3_temple_gu": {
        "affection": {"guqinghan": 1},
        "flags": {"trusted_gu_scout": True},
    },
    "c3_temple_su": {
        "affection": {"sumobai": 1},
        "flags": {"relied_on_su_sense": True},
    },
    "c3_temple_pei": {
        "affection": {"peijinzhe": 1},
        "flags": {"relied_on_pei_guard": True},
    },

    # ch3_memory: 记忆觉醒后的反应
    "c3_mem_accept": {
        "affection": {"guqinghan": 1},
        "flags": {"accepted_identity": True},
    },
    "c3_mem_reject": {
        "affection": {"peijinzhe": 1},
        "flags": {"rejected_identity": True},
    },
    "c3_mem_ask_su": {
        "affection": {"sumobai": 2},
        "flags": {"asked_sumobai_worth": True},
    },

    # ch3_night: 真相揭露
    "c3_night_gu": {
        "affection": {"guqinghan": 1},
        "flags": {"confronted_gu_plan": True},
    },
    "c3_night_su": {
        "affection": {"sumobai": 2},
        "flags": {"asked_su_who_am_i": True},
    },
    "c3_night_pei": {
        "affection": {"peijinzhe": 1},
        "flags": {"thanked_pei_again": True},
    },

    # ch3_crisis: 面对可能的牺牲
    "c3_crisis_determined": {
        "affection": {"guqinghan": 1},
        "flags": {"determined": True},
    },
    "c3_crisis_alternative": {
        "affection": {"sumobai": 1},
        "flags": {"seek_alternative": True},
    },
    "c3_crisis_admit_fear": {
        "affection": {"peijinzhe": 2},
        "flags": {"admitted_fear": True},
    },

    # ch3_route_select: 最终选择
    "c3_route_gu": {
        "affection": {"guqinghan": 3},
        "flags": {"chose_guqinghan": True},
        "next_scene": "ch4_guqinghan",
    },
    "c3_route_su": {
        "affection": {"sumobai": 3},
        "flags": {"chose_sumobai": True},
        "next_scene": "ch4_sumobai",
    },
    "c3_route_pei": {
        "affection": {"peijinzhe": 3},
        "flags": {"chose_peijinzhe": True},
        "next_scene": "ch4_peijinzhe",
    },
    "c3_route_solo": {
        "flags": {"chose_solo": True},
        "next_scene": "ch4_solo",
    },

    # === Chapter 4: 抉择 (Day 7) ===

    # ch4_guqinghan
    "c4_gu_independent": {
        "affection": {"guqinghan": 1},
        "flags": {"gu_independent_response": True},
    },
    "c4_gu_dependent": {
        "affection": {"guqinghan": 2},
        "flags": {"gu_called_by_name": True},
    },

    # ch4_sumobai
    "c4_su_share_burden": {
        "affection": {"sumobai": 1},
        "flags": {"su_share_burden": True},
    },
    "c4_su_beg_live": {
        "affection": {"sumobai": 2},
        "flags": {"su_called_by_name": True},
    },

    # ch4_peijinzhe
    "c4_pei_worried": {
        "affection": {"peijinzhe": 1},
        "flags": {"pei_worried_response": True},
    },
    "c4_pei_hint": {
        "affection": {"peijinzhe": 2},
        "flags": {"pei_hint_confession": True},
    },

    # ch4_solo
    "c4_solo_accept": {
        "flags": {"accepted_duty": True},
        "next_scene": "ending_solo",
    },
    "c4_solo_vulnerable": {
        "flags": {"called_for_help": True},
        "next_scene": "ending_true",
    },
}

# ─── route determination ───
ROUTE_THRESHOLDS = {
    "guqinghan": 6,
    "sumobai": 6,
    "peijinzhe": 6,
}

# ─── day mapping for status display ───
SCENE_TO_DAY = {
    "ch1_arrival": 1,
    "ch1_guqinghan": 1,
    "ch1_sumobai": 1,
    "ch1_peijinzhe": 2,
    "ch1_lingjie": 2,
    "ch1_night": 2,
    "ch2_morning": 3,
    "ch2_guqinghan_route": 3,
    "ch2_sumobai_route": 3,
    "ch2_peijinzhe_route": 3,
    "ch2_converge": 4,
    "ch2_evening": 4,
    "ch3_temple": 5,
    "ch3_memory": 5,
    "ch3_night": 5,
    "ch3_crisis": 6,
    "ch3_route_select": 6,
    "ch4_guqinghan": 7,
    "ch4_sumobai": 7,
    "ch4_peijinzhe": 7,
    "ch4_solo": 7,
}

# ─── commands ───
def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(path, state):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    state["updated_at"] = datetime.now().isoformat(timespec="seconds")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return state

def cmd_new(save_path, name):
    state = {
        "protagonist_name": name,
        "current_chapter": 1,
        "current_scene": "ch1_arrival",
        "current_day": 1,
        "affection": {"guqinghan": 0, "sumobai": 0, "peijinzhe": 0},
        "flags": {},
        "route": None,
        "ending": None,
        "choices_made": [],
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": None,
    }
    _save(save_path, state)
    print(json.dumps(state, ensure_ascii=False, indent=2))

def cmd_choose(save_path, choice_id):
    state = _load(save_path)
    if choice_id not in CHOICES:
        print(json.dumps({"error": f"Unknown choice_id: {choice_id}"}, ensure_ascii=False))
        return
    choice = CHOICES[choice_id]
    # Apply affection changes
    for char, delta in choice.get("affection", {}).items():
        state["affection"][char] = state["affection"].get(char, 0) + delta
    # Apply flags
    for flag, val in choice.get("flags", {}).items():
        state["flags"][flag] = val
    # Record choice
    state["choices_made"].append({
        "choice_id": choice_id,
        "scene": state["current_scene"],
        "chapter": state["current_chapter"],
        "day": state.get("current_day", 1),
    })
    # Advance to next scene if specified
    if "next_scene" in choice:
        ns = choice["next_scene"]
        state["current_scene"] = ns
        if ns.startswith("ch4_"):
            state["current_chapter"] = 4
            if ns == "ch4_guqinghan":
                state["route"] = "guqinghan"
            elif ns == "ch4_sumobai":
                state["route"] = "sumobai"
            elif ns == "ch4_peijinzhe":
                state["route"] = "peijinzhe"
            elif ns == "ch4_solo":
                state["route"] = "solo"
        elif ns.startswith("ending_"):
            state["ending"] = ns.replace("ending_", "")
        # Update day
        state["current_day"] = SCENE_TO_DAY.get(ns, state.get("current_day", 1))
    _save(save_path, state)
    print(json.dumps({
        "ok": True,
        "choice_id": choice_id,
        "affection": state["affection"],
        "new_flags": choice.get("flags", {}),
        "current_scene": state["current_scene"],
        "current_day": state.get("current_day", 1),
        "route": state["route"],
        "ending": state["ending"],
    }, ensure_ascii=False, indent=2))

def cmd_advance(save_path, scene_id):
    state = _load(save_path)
    state["current_scene"] = scene_id
    m = re.match(r"ch(\d+)", scene_id)
    if m:
        state["current_chapter"] = int(m.group(1))
    elif scene_id.startswith("ending_"):
        state["ending"] = scene_id.replace("ending_", "")
    # Update day
    state["current_day"] = SCENE_TO_DAY.get(scene_id, state.get("current_day", 1))
    _save(save_path, state)
    print(json.dumps({
        "ok": True,
        "current_scene": scene_id,
        "current_chapter": state["current_chapter"],
        "current_day": state.get("current_day", 1),
    }, ensure_ascii=False, indent=2))

def cmd_flag(save_path, flag_name, value="true"):
    state = _load(save_path)
    state["flags"][flag_name] = value.lower() in ("true", "1", "yes")
    _save(save_path, state)
    print(json.dumps({"ok": True, "flag": flag_name,
                       "value": state["flags"][flag_name]}, ensure_ascii=False))

def cmd_affection(save_path, character, delta):
    state = _load(save_path)
    delta = int(delta)
    if character not in state["affection"]:
        print(json.dumps({"error": f"Unknown character: {character}"}, ensure_ascii=False))
        return
    state["affection"][character] += delta
    _save(save_path, state)
    print(json.dumps({"ok": True, "character": character,
                       "affection": state["affection"]},
                      ensure_ascii=False, indent=2))

def cmd_check_route(save_path):
    state = _load(save_path)
    aff = state["affection"]
    best = max(aff, key=aff.get)
    best_val = aff[best]
    results = {}
    for route, threshold in ROUTE_THRESHOLDS.items():
        results[route] = {
            "affection": aff[route],
            "threshold": threshold,
            "available": aff[route] >= threshold,
        }
    # Check for true ending condition (all >= 5)
    all_high = all(v >= 5 for v in aff.values())
    determined_route = best if best_val >= min(ROUTE_THRESHOLDS.values()) else None
    print(json.dumps({
        "determined_route": determined_route,
        "routes": results,
        "current_route": state.get("route"),
        "true_ending_available": all_high,
    }, ensure_ascii=False, indent=2))

def cmd_status(save_path):
    state = _load(save_path)
    print(json.dumps(state, ensure_ascii=False, indent=2))

def cmd_list_flags(save_path):
    state = _load(save_path)
    print(json.dumps(state["flags"], ensure_ascii=False, indent=2))

def cmd_get_affection(save_path, character):
    state = _load(save_path)
    if character == "all":
        print(json.dumps(state["affection"], ensure_ascii=False, indent=2))
    else:
        print(json.dumps({character: state["affection"].get(character, 0)},
                          ensure_ascii=False))

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    save_path = sys.argv[2]
    handlers = {
        "new":            lambda: cmd_new(save_path, sys.argv[3]),
        "choose":         lambda: cmd_choose(save_path, sys.argv[3]),
        "advance":        lambda: cmd_advance(save_path, sys.argv[3]),
        "flag":           lambda: cmd_flag(save_path, sys.argv[3],
                                           sys.argv[4] if len(sys.argv) > 4 else "true"),
        "affection":      lambda: cmd_affection(save_path, sys.argv[3], sys.argv[4]),
        "check_route":    lambda: cmd_check_route(save_path),
        "status":         lambda: cmd_status(save_path),
        "list_flags":     lambda: cmd_list_flags(save_path),
        "get_affection":  lambda: cmd_get_affection(save_path,
                                           sys.argv[3] if len(sys.argv) > 3 else "all"),
    }
    if cmd not in handlers:
        print(f"Unknown command: {cmd}\n{__doc__}")
        sys.exit(1)
    handlers[cmd]()

if __name__ == "__main__":
    main()
