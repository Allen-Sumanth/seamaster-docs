# Resolution Rules

The game engine resolves actions in a specific order. Understanding this is key to winning "tie-breaks".

## Turn Order
The Game Loop processes a tick in this order:

1.  **Spawning**: New bots are created.
    *   If a spawn location is occupied, the spawn **fails**.
2.  **Actions**: Existing bots execute their commands.
    *   Iterates through all bots.
3.  **Entity Updates**: Banks and Energy Pads update their timers.
4.  **Win Check**: Victory conditions are checked.

## Action Resolution
The engine resolves actions based on a strict priority system. When multiple bots attempt actions in the same tick, they are processed in the following order:

??? info
    Each bot can only perform one move per tick. Some actions, such as `HARVEST` and `LOCKPICK`, have an option where the bot can move to a location and perform the action, essentially allowing the bot to perform two 'actions' (move and harvest/lockpick) in the same tick.

### 1. Priority Tiers
Actions with higher priority numbers are resolved first.

| Priority | Action |
| :--- | :--- |
| **6** | `SELFDESTRUCT` |
| **5** | `HARVEST` |
| **4** | `POISON` |
| **3** | `DEPOSIT` |
| **2** | `LOCKPICK` |
| **1** | `MOVE` |

### 2. Tie-Breakers
If multiple bots want to perform actions with the **same priority** (e.g., two bots trying to Move into the same tile), the engine resolves the conflict using these tie-breakers, in order:

1.  **Energy**: Bot with **Higher Energy** goes first.
2.  **Age**: Bot that was **Spawned Earlier** (lower Bot ID) goes first.
3.  **Random**: If Energy and Age are identical, it is determined randomly.

## Collision
*   **Bots cannot share a tile.**
*   **Bots cannot move through each other.**
*   **Bots cannot swap places** directly in one tick (head-on collision).

## Timeout & Errors
*   **Time Limit**: Your code has a limited time to respond (e.g., 20ms - 100ms per tick).
*   **Timeout**: If you exceed the limit, your turn is skipped.
*   **Crash**: If your code throws an exception, your turn is skipped.
*   **Disqualification**: Too many consecutive errors/timeouts will disqualify you from the match.
