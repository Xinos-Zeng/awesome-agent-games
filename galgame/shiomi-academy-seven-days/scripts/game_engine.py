#!/usr/bin/env python3
"""
汐見学園 —  galgame state engine.

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
    # === Chapter 1: 始まりの日 (Day 1) ===
    # Scene 1: Morning - where to go before class
    "c1_rooftop": {
        "affection": {"hina": 1},
        "flags": {"visited_rooftop": True},
    },
    "c1_library": {
        "affection": {"shizuku": 1},
        "flags": {"visited_library": True},
    },
    "c1_council": {
        "affection": {"kotone": 1},
        "flags": {"visited_council_room": True},
    },

    # Scene 2: After school - broadcast room mystery
    "c1_go_to_broadcast": {
        "flags": {"found_broadcast_room": True, "heard_static": True},
    },
    "c1_ignore_broadcast": {
        "flags": {"ignored_broadcast": True},
    },

    # Scene 3: Evening - who to ask about the school
    "c1_ask_shizuku": {
        "affection": {"shizuku": 1},
        "flags": {"talked_to_shizuku_ch1": True},
    },
    "c1_ask_kotone": {
        "affection": {"kotone": 1},
        "flags": {"talked_to_kotone_ch1": True},
    },
    "c1_ask_hina": {
        "affection": {"hina": 1},
        "flags": {"talked_to_hina_ch1": True},
    },

    # === Chapter 2: 綻び (Day 2-3) ===
    # Scene 1: Who to investigate with
    "c2_investigate_with_shizuku": {
        "affection": {"shizuku": 2},
        "flags": {"investigated_with_shizuku": True},
    },
    "c2_investigate_with_kotone": {
        "affection": {"kotone": 2},
        "flags": {"investigated_with_kotone": True},
    },
    "c2_investigate_with_hina": {
        "affection": {"hina": 2},
        "flags": {"investigated_with_hina": True},
    },

    # Scene 2: Radio broadcast content
    "c2_trust_radio": {
        "flags": {"trusts_radio": True},
    },
    "c2_doubt_radio": {
        "flags": {"doubts_radio": True},
    },

    # Scene 3: Lighthouse investigation
    "c2_go_lighthouse_shizuku": {
        "affection": {"shizuku": 2},
        "flags": {"visited_lighthouse": True, "found_photograph": True,
                  "lighthouse_with_shizuku": True},
    },
    "c2_go_lighthouse_kotone": {
        "affection": {"kotone": 2},
        "flags": {"visited_lighthouse": True, "found_photograph": True,
                  "lighthouse_with_kotone": True},
    },
    "c2_go_lighthouse_hina": {
        "affection": {"hina": 2},
        "flags": {"visited_lighthouse": True, "found_photograph": True,
                  "lighthouse_with_hina": True},
    },
    "c2_skip_lighthouse": {
        "flags": {"skipped_lighthouse": True},
    },

    # Scene 4: Deeper investigation
    "c2_read_records": {
        "affection": {"kotone": 1},
        "flags": {"read_old_records": True},
    },
    "c2_ask_around": {
        "affection": {"hina": 1},
        "flags": {"asked_teachers": True},
    },
    "c2_search_alone": {
        "affection": {"shizuku": 1},
        "flags": {"searched_alone": True},
    },

    # Scene 5: Night events
    "c2_night_broadcast": {
        "affection": {"shizuku": 2},
        "flags": {"night_broadcast_visited": True, "met_shizuku_night": True},
    },
    "c2_night_council": {
        "affection": {"kotone": 2},
        "flags": {"night_council_visited": True, "saw_kotone_crying": True},
    },
    "c2_night_hina": {
        "affection": {"hina": 2},
        "flags": {"night_hina_visited": True, "hina_confessed_fear": True},
    },

    # === Chapter 3: 真実 (Day 4-5) ===
    # Scene 1: Whose truth to believe
    "c3_believe_shizuku": {
        "affection": {"shizuku": 2},
        "flags": {"believes_shizuku": True},
    },
    "c3_believe_kotone": {
        "affection": {"kotone": 2},
        "flags": {"believes_kotone": True},
    },
    "c3_believe_hina": {
        "affection": {"hina": 2},
        "flags": {"believes_hina": True},
    },

    # Scene 2: Confrontation
    "c3_confront_truth": {
        "flags": {"confronted_truth": True},
    },
    "c3_run_away": {
        "flags": {"ran_away": True},
    },

    # Scene 3: Route selection
    "c3_choose_shizuku": {
        "affection": {"shizuku": 3},
        "flags": {"chose_shizuku": True},
        "next_scene": "route_shizuku_s1",
    },
    "c3_choose_kotone": {
        "affection": {"kotone": 3},
        "flags": {"chose_kotone": True},
        "next_scene": "route_kotone_s1",
    },
    "c3_choose_hina": {
        "affection": {"hina": 3},
        "flags": {"chose_hina": True},
        "next_scene": "route_hina_s1",
    },
    "c3_choose_none": {
        "flags": {"chose_none": True},
        "next_scene": "ending_loop",
    },

    # === Shizuku Route ===
    "rs_accept_loop": {
        "flags": {"accepted_loop": True},
        "next_scene": "ending_eternal",
    },
    "rs_break_loop": {
        "flags": {"broke_loop": True},
        "next_scene": "ending_true_end",
    },
    "rs_find_third_way": {
        "flags": {"found_third_way": True},
        "next_scene": "ending_bittersweet",
    },

    # === Kotone Route ===
    "rk_save_everyone": {
        "affection": {"kotone": 1},
        "flags": {"tried_save_everyone": True},
        "next_scene": "ending_true_end",
    },
    "rk_save_kotone": {
        "affection": {"kotone": 2},
        "flags": {"chose_save_kotone": True},
        "next_scene": "ending_bittersweet",
    },
    "rk_let_go": {
        "flags": {"let_go_kotone": True},
        "next_scene": "ending_normal",
    },

    # === Hina Route ===
    "rh_save_mother": {
        "affection": {"hina": 1},
        "flags": {"tried_save_mother": True},
        "next_scene": "ending_bittersweet",
    },
    "rh_accept_loss": {
        "affection": {"hina": 2},
        "flags": {"accepted_loss": True},
        "next_scene": "ending_true_end",
    },
    "rh_rewrite_fate": {
        "flags": {"rewrote_fate": True},
        "next_scene": "ending_hidden",
    },

    # === Final choices (ending branches) ===
    "end_shizuku_true": {"next_scene": "ending_true_end"},
    "end_shizuku_bittersweet": {"next_scene": "ending_bittersweet"},
    "end_kotone_true": {"next_scene": "ending_true_end"},
    "end_kotone_bittersweet": {"next_scene": "ending_bittersweet"},
    "end_hina_true": {"next_scene": "ending_true_end"},
    "end_hina_bittersweet": {"next_scene": "ending_bittersweet"},
}

# ─── route determination ───
ROUTE_THRESHOLDS = {
    "shizuku": 6,
    "kotone":  6,
    "hina":    6,
}

# ─── commands ───
def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(path, state):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    state["updated_at"] = datetime.now().isoformat(timespec="seconds")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return state

def cmd_new(save_path, name):
    state = {
        "protagonist_name": name,
        "current_chapter": 1,
        "current_scene": "ch1_morning",
        "affection": {"shizuku": 0, "kotone": 0, "hina": 0},
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
    for char, delta in choice.get("affection", {}).items():
        state["affection"][char] = state["affection"].get(char, 0) + delta
    for flag, val in choice.get("flags", {}).items():
        state["flags"][flag] = val
    state["choices_made"].append({
        "choice_id": choice_id,
        "scene": state["current_scene"],
        "chapter": state["current_chapter"],
    })
    if "next_scene" in choice:
        ns = choice["next_scene"]
        state["current_scene"] = ns
        if ns.startswith("route_"):
            state["route"] = ns.replace("route_", "").split("_s")[0]
            state["current_chapter"] = 4
        elif ns.startswith("ending_"):
            state["ending"] = ns.replace("ending_", "")
    _save(save_path, state)
    print(json.dumps({"ok": True, "choice_id": choice_id,
                       "affection": state["affection"],
                       "new_flags": choice.get("flags", {}),
                       "current_scene": state["current_scene"],
                       "route": state["route"],
                       "ending": state["ending"]},
                      ensure_ascii=False, indent=2))

def cmd_advance(save_path, scene_id):
    state = _load(save_path)
    state["current_scene"] = scene_id
    m = re.match(r"ch(\d+)", scene_id)
    if m:
        state["current_chapter"] = int(m.group(1))
    elif scene_id.startswith("route_"):
        state["current_chapter"] = 4
    elif scene_id.startswith("ending_"):
        state["ending"] = scene_id.replace("ending_", "")
    _save(save_path, state)
    print(json.dumps({"ok": True, "current_scene": scene_id,
                       "current_chapter": state["current_chapter"]},
                      ensure_ascii=False, indent=2))

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
        results[route] = {"affection": aff[route], "threshold": threshold,
                          "available": aff[route] >= threshold}
    determined_route = best if best_val >= min(ROUTE_THRESHOLDS.values()) else None
    print(json.dumps({"determined_route": determined_route,
                       "routes": results,
                       "current_route": state.get("route")},
                      ensure_ascii=False, indent=2))

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
