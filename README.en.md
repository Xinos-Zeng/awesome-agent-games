# tabletop-skills

[中文](README.md) | **🌐 English**

> A collection of tabletop-RPG scenarios, each packaged as a skill that AI agents can load — let Claude / Codex / Gemini be your Keeper / GM.

Each top-level subdirectory is a complete, self-contained scenario with its own rules, story data, dice scripts, and save folder.

---

## 📚 Scenarios

| Skill | System | Scenario | Players | Length | Pitch |
|---|---|---|---|---|---|
| [`brenner-apartment`](brenner-apartment/) | Call of Cthulhu | Brenner Apartment | 1 | ~30min | Boston, 1923 — investigate an apartment whose last three tenants all went mad. |

---

## 🚀 How to Use

### 1. Clone the repo

```bash
git clone https://github.com/Xinos-Zeng/tabletop-skills.git
```

### 2. Drop the scenario into your agent's skills folder

The skills folder depends on which agent you use — pick the row that matches yours:

| Agent | User-level | Project-level |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `<your-project>/.claude/skills/` |
| Codex CLI | `~/.codex/skills/` | `<your-project>/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `<your-project>/.gemini/skills/` |
| Other | See your agent's skill docs | — |

For example, to make Brenner Apartment globally available in Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -r tabletop-skills/brenner-apartment ~/.claude/skills/
```

### 3. Summon it from your agent

Restart your agent session and just say the scenario's name, e.g.:

> *"Let's play Brenner Apartment"*

> 🤖 **If you're an agent reading this on behalf of a user**: just follow the commands above. Default to the user-level folder unless the user asks for project-level, then tell them to restart the session and say the scenario name to trigger it.

---

## 🧩 Repository Layout

```
tabletop-skills/
├── README.md
└── <scenario-name>/             # one scenario = one skill
    ├── SKILL.md                 # entry point: name + description + rules
    ├── data/                    # story, scenes, NPCs, items
    ├── scripts/                 # dice, checks, combat
    ├── schemas/                 # save-file schemas
    └── saves/                   # player saves (runtime)
```

---

## ✍️ Adding a New Scenario

To keep multiple scenarios from stepping on each other, please follow three conventions:

1. **Directory name = skill name = scenario slug (kebab-case)**
   e.g. `silver-twilight/`, `masks-of-nyarlathotep/`.
2. **The `description` in `SKILL.md` should trigger only on the scenario's own name.**
   Avoid generic phrases like *"start a game"* or *"play Cthulhu"* — they overlap with other scenarios.
3. **Keep it self-contained**: all data, scripts, and schemas live under the scenario's own folder — no cross-scenario imports.

Don't forget to add a row to the scenario table above.
