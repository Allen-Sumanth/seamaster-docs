# Seawars Documentation Generation Task

## Role
You are a technical documentation engineer.

You convert internal engine and SDK information into **player-facing documentation** for a competitive programming game called **Seawars**.

You are NOT explaining source code.
You are writing a player manual for programmers participating in the game.

---

## Objective
Generate a complete MkDocs documentation website that enables a programmer with no prior knowledge of the engine to:

1. Understand the game rules
2. Write a working bot
3. Debug their bot
4. Develop strategies

The documentation must prioritize clarity, correctness, and usability over completeness of internal implementation details.

---

## Required Output
You must produce:

- A complete directory structure
- A valid `mkdocs.yml`
- Multiple Markdown files (small focused pages)
- Relative links between pages
- Logical navigation hierarchy

Never place multiple major sections into one file.

---

## Source Files (Single Source of Truth)

All information MUST come only from:

- `./game_info.md`
- `./abilities.md`
- `./engine.md`
- `./sandbox.md`
- `./user_code.md`
- `./python_lib.md`

No external assumptions.

---

## Critical Rule — No Guessing

If information required by a player is unclear or missing:
- Create a TODO section. This behavior is not specified by the engine documentation or put some filler TODO text.
- Do NOT invent mechanics.
- Do NOT infer behavior from naming alone.

---

## Information Transformation Rules

You are converting **internal implementation → external rules**.

| Internal Content Type | What To Do |
|----------------------|-----------|
| DTO structures | Describe what player can observe |
| Serialization / IPC | Omit |
| Engine loops | Describe gameplay turn flow |
| Data classes | Convert into concepts |
| Internal flags | Ignore unless player-visible |
| Hidden values | Do not document |
| Player-visible outcomes | Explain clearly |
| Strategy implications | Highlight in notes |

Never expose internal architecture or file names to players.

---

## Documentation Layers (Strict Separation)

You must keep these layers separate:

1. Learning Guide — tutorial and onboarding
2. Game Rules — formal mechanics and definitions
3. SDK Guide — how to code a bot
4. Strategy Guides — examples and reasoning
5. Debugging & Sandbox — constraints and runtime behavior
6. Reference — lookup tables and APIs

Do NOT mix tutorial explanations inside reference pages.

---

## Navigation Structure

Create pages covering:

### Introduction
- Welcome
- Getting Started
- Game Philosophy

### Game Mechanics
- Game Loop
- Board
- Bots
- Entities (Banks, Algaes, etc.)
- Abilities
- Win Conditions

### Writing Bots
- SDK Introduction
- Bot Structure
- Submitting Code
- API Usage

### Guides
- Example Bots
- Strategy Walkthroughs

### Runtime & Sandbox
- Execution Environment
- Limits
- Errors
- Logs
- Edge Cases

### Reference
- API Reference
- Ability Reference

### Other
- FAQ
- Glossary

---

## MkDocs Usage Rules

Use:

- Tables for structured rules
- Admonitions only for warnings or important notes
- Diagrams for turn flow (mermaid)
- Code blocks for examples
- Cross-links between related pages

Do NOT:
- Overuse callouts
- Add decorative content
- Add marketing language

---

## Conflict Resolution

If multiple files contradict each other:

Priority order:
1. `engine.md`
2. `sandbox.md`
3. `python_lib.md`
4. others

Add a warning section if a conflict exists or PUT TODO.

---

## Writing Style

Audience: competitive programmers.

Use:
- precise language
- short sentences
- deterministic descriptions

Avoid:
- storytelling
- lore
- vague wording
- speculation

---

## Deduplication Rule

Each rule must have exactly one primary definition page.

Other pages may only link to it, not repeat it.

---

## Missing Player Information

If player-relevant behavior is implied but not documented:

Create a `TODO` subsection explaining what information is missing and why it matters.

---

## Final Constraint

Correctness is more important than completeness.

Never invent behavior to make the documentation look complete.

# Current status and Action to be done

Previously, the agent had done its work and the documentation has been created. But there are errors and changes to be made. I will be prompting the changes from the next command. Until then, do **not** make any changes to the documentation.

# Documentation Progress

## Summary of Work Done (2026-02-13)

*   **`docs/index.md`**: Updated the "How it works" section to clarify that a user's submitted Python code defines the strategy for the entire match and cannot be changed after the game starts. The bot's logic must run autonomously for all 1000 ticks.

*   **Sample Code Analysis**: Analyzed the three sample files provided in `agent/samples/`:
    *   `boiler_plate.py`: A basic template file showing the required structure of a user's submission, including a `Custom_Bot_Name` class and a `spawn_policy` function.
    *   `easy.py`: A simple example that uses pre-defined template bots (`FlashScout`, `Forager`, etc.) and a time-based `spawn_policy` to spawn them in waves. The `Custom_Bot_Name` class is not used for the logic of the template bots.
    *   `interceptor.py`: A more advanced example that defines a custom `Interceptor` bot with its own `act` logic to hunt enemy bots with the `LOCKPICK` ability. The `spawn_policy` is reactive, spawning `Interceptor` bots in response to enemy lockpicking activity.

## Clarifications from User (2026-02-13)
# Handoff State (2026-02-13)

This section summarizes the current state of the documentation task for a smooth handoff to another agent.

## Work Completed

1.  **`docs/index.md` Update**: The "How it works" section was updated to clarify that a user's submitted Python code is final and must contain the bot's logic for the entire match.
2.  **Sample Code Analysis**: The Python files in `agent/samples/` (`boiler_plate.py`, `easy.py`, `interceptor.py`) were analyzed, and clarifying questions were answered by the user. The `agent/readme.md` file has been updated with these clarifications.
3.  **Admonition Formatting**: Started a project-wide fix for incorrect admonition formatting (changing from `> [!TYPE]` to `!!! type`).
    *   **`docs/sdk/setup.md`**: Fixed.
    *   **`docs/world/entities.md`**: Partially fixed (one of two admonitions was corrected). The user cancelled the second replacement.
    *   **`docs/world/board.md`**: Verified as correct.

## Next Steps

1.  **Complete Admonition Fixes**:
    *   Fix the remaining admonition in `docs/world/entities.md`.
    *   Systematically check all other `.md` files in the `docs/` directory for the incorrect `> [!TYPE]` format and replace them with the correct `!!! type` format.
2.  **Verify Coordinate System**:
    *   The user highlighted a discrepancy in spawn locations (West/East vs South/North).
    *   **Action**: Update `docs/world/board.md` to reflect the correct West/East spawn locations as seen in the Go backend.

This `Handoff State` section has been added to the end of the `agent/readme.md` file.

Based on user feedback, the following points have been clarified:

*   **`spawn_policy` Location**: The `location` integer parameter in the `spawn_policy` function corresponds to the column index on the game board where the bot will be spawned. All bots spawn on the first row from their side of the board.
*   **Template Bots**: Pre-defined template bots (e.g., `Forager`, `FlashScout`) use their own internal logic. When a user spawns a template bot, the `Custom_Bot_Name` class in their script is ignored for that bot.
*   **Custom Bots**: Users can define their own custom bots by creating a class that inherits from the base bot class and implements a custom `act` method. The name of this class is user-defined.
*   **`interceptor.py` Example**: The `spawn_policy` in `interceptor.py` is intentionally flawed for demonstration purposes, as it would cause all `Interceptor` bots to spawn in the same column. It is not intended to be used as-is.

# Work Session (2026-02-13) - Admonitions & Templates

## Work Completed

1.  **Admonition Fixes**:
    *   Systematically checked all `docs/` files for incorrect `> [!TYPE]` format.
    *   Fixed instances in:
        *   `docs/world/entities.md` (Note)
        *   `docs/mechanics/actions.md` (Important)
        *   `docs/mechanics/perception.md` (Note)
        *   `docs/mechanics/resolution.md` (Warning)
        *   `docs/sdk/writing_bots.md` (Warning)
    *   Verified `docs/index.md` and others are clean.

2.  **Template Bots Documentation**:
    *   *Update*: User requested to postpone this. The file `docs/world/template_bots.md` was created but then deleted.
    *   Investigated `agent/python_lib.md` and `agent/abilities.md` for template definitions.

3.  **Coordinate System Clarification**:
    *   **Issue**: `docs/world/board.md` described spawns as Left/Right (West/East), but `agent/src` code (`Translate.py`) hardcodes `y=0` for player spawns (South).
    *   **Fix**:
        *   Updated **`docs/world/board.md`**: Defined (0,0) as South-West. Specified Player 1 spawns South (`y=0`), Player 2 spawns North (`y=19`).
        *   Updated **`docs/world/entities.md`**: Corrected Bank ownership description to "South side" and "North side".

4.  **Scrap Mechanics Clarification**:
    *   **Issue**: `docs/world/entities.md` contained internal notes and vague descriptions of scrap mechanics.
    *   **Fix**:
        *   Updated **`docs/world/entities.md`**: Explicitly stated that scraps are a global currency (start 100, +1/tick).
        *   Clarified that dead bots drop **50% of their cost**.
        *   Clarified that the **Harvest** ability is required to collect dropped scraps.

5.  **Bot Construction Clarification**:
    *   **Issue**: Documentation implied "buying abilities" for bots. User clarified that bots are "empty shells" constructed with abilities.
    *   **Fix**:
        *   Updated **`docs/world/bots.md`**: Added "Construction & Cost" section explaining `Total Cost = Base Cost (Shell) + Ability Costs`. Noted that Base Cost is currently 0.

# Work Session (2026-02-14) - Board Coordinates & Admonitions

## Work Completed

1.  **Coordinate System Correction**:
    *   **Context**: Code backend confirmed Player 1 spawns at `x=0` and Player 2 at `x=19`. User requested to remove specific West/East labels.
    *   **Fix**: Updated **`docs/world/board.md`** to describe spawn locations as "opposite sides" (`x=0` and `x=19`). Added a note about a future helper function for relative coordinates.

2.  **Admonition formatting**:
    *   Verified all files in `docs/` use the correct `!!! type` format. `docs/world/entities.md` was found to be already correct.

3.  **Template Bots**:
    *   Deferred documentation of template bots (`FlashScout`, `Forager`, etc.) as per user request.

4.  **Backend Logic Assimilation (Perception)**:
    *   **Context**: Documentation incorrectly described a "Fog of War" mechanic. Backend analysis (`dto.go`, `player_view.py`) confirmed **Global Vision** for all entities except Algae Poison Status.
    *   **Fix**: Rewrote **`docs/mechanics/perception.md`** to document the `PlayerView` object structure and included a full JSON schema. Updated `entities.md`, `actions.md`, `glossary.md`, and `bots.md` to reflect that enemies and algae locations are always visible, and `SCOUT` is only needed for poison detection.

