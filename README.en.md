# awesome-agent-games

[中文](README.md) | **English**

> A collection of game skills for AI agents: Call of Cthulhu scenarios, galgames, interactive fiction, and other playable distractions.

Each game is a complete, self-contained skill with its own rules prompt, story data, scripts, and save folder. Category folders are only for organizing this repository; copy the concrete game folder into your agent's skills directory.

---

## Included Games

### Call of Cthulhu

| Skill | System | Game | Players | Length | Pitch |
|---|---|---|---|---|---|
| [`brenner-apartment`](coc/brenner-apartment/) | Call of Cthulhu | Brenner Apartment | 1 | ~30min | Boston, 1923. Investigate an apartment whose last three tenants all went mad. |

Development guide: [`coc/tutorial.md`](coc/tutorial.md).

### Galgame

| Skill | Type | Game | Players | Length | Pitch |
|---|---|---|---|---|---|
| [`shiomi-academy-seven-days`](galgame/shiomi-academy-seven-days/) | Visual novel | Shiomi Academy Seven Days | 1 | Multi-route | A seaside academy, an abandoned lighthouse, and romance inside a seven-day time loop. |

Development guide: [`galgame/tutorial.md`](galgame/tutorial.md).

---

## Showcase

These snippets show what play looks like without revealing key clues, truths, route conditions, or endings.

### Call of Cthulhu

```text
Player: Let's play Brenner Apartment.

Keeper:
Brenner Apartment
Boston rain, an old brick building, and rooms that refuse to stay quiet.

Boston, 1923.

Rain runs down the red-brick walls, and the streetlights break into dull yellow fragments across the puddles. You stand before Brenner Apartment with the landlord's key in your hand.

Rumor says the last three tenants all left this place broken. Some blame gas leaks. Some blame loneliness, poverty, or the shadows left behind by the war.

But when you look up at the dark second-floor window, you suddenly feel that something is looking back.

Welcome, investigator. Welcome to Brenner Apartment.

First, create your character.

Choose your occupation:
[1] Private Investigator
[2] Journalist
[3] Scholar

Choose 2 items to carry:
[A] Lighter  [B] Notebook  [C] Pocket Watch
[D] First Aid Kit  [E] Flask  [F] Revolver
```

### Galgame

```text
Player: Let's play Shiomi Academy Seven Days.

Narrator: A sea breeze drifts up from the end of the slope, carrying salt and the smell of summer. Far away, an old lighthouse stands silently by the cliff, its clock stopped at a time you cannot quite read.

Today is your first day transferring into Shiomi Academy.

What is the protagonist's name?
(Default: Hasegawa Ren)
```

---

## How to Use

### 1. Clone the repo

```bash
git clone https://github.com/Xinos-Zeng/awesome-agent-games.git
```

You can also tell your agent: download the game skill I want to play from `https://github.com/Xinos-Zeng/awesome-agent-games` and install it into your user-level skills directory.

### 2. Drop the game into your agent's skills folder

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
cp -r awesome-agent-games/coc/brenner-apartment ~/.claude/skills/
```

For example, to play Shiomi Academy Seven Days:

```bash
mkdir -p ~/.claude/skills
cp -r awesome-agent-games/galgame/shiomi-academy-seven-days ~/.claude/skills/
```

### 3. Summon it from your agent

Restart your agent session and just say the game's name, e.g.:

> *"Let's play Brenner Apartment"*

> *"Let's play Shiomi Academy Seven Days"*

> If you're an agent reading this on behalf of a user: follow the commands above. Default to the user-level folder unless the user asks for project-level, then tell them to restart the session and say the game name to trigger it.

---

## Repository Layout

```
awesome-agent-games/
├── README.md
├── coc/
│   ├── tutorial.md
│   └── <game-slug>/
│       ├── SKILL.md
│       ├── data/
│       ├── scripts/
│       ├── schemas/
│       └── saves/
└── galgame/
    ├── tutorial.md
    └── <game-slug>/
        ├── SKILL.md
        ├── data/
        ├── scripts/
        └── saves/
```

---

## Contributing a Game

PRs for new games are welcome. To keep multiple skills from stealing each other's trigger phrases, follow these conventions:

1. Pick the right category, such as `coc/` or `galgame/`.
2. Create a concrete game folder. Use kebab-case, and keep it identical to the `name` in `SKILL.md` frontmatter.
3. Make `description` trigger only on the concrete game title. Avoid broad phrases like "start a game", "play galgame", or "play Cthulhu".
4. Keep the game self-contained: data, scripts, schemas, and saves stay under its own folder.
5. Check the relevant category tutorial before opening the PR.
6. Add a row to the matching category table in this README.
7. In the PR description, include the game type, trigger phrase, external dependencies if any, and the startup flow you tested.

