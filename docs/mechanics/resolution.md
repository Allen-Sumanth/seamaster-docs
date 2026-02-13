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

## Simultaneous Actions
All bot actions for a turn are submitted at once, but processed sequentially by the engine.

> [!WARNING]
> The order in which bots are processed is **non-deterministic**.

If two bots attempt to move into the same empty square on the same tick:
1.  The engine picks one bot (randomly/implementation defined).
2.  That bot moves successfully.
3.  The second bot attempts to move, sees the square is now `Occupied`, and the move **fails**.

## Collision
*   **Bots cannot share a tile.**
*   **Bots cannot move through each other.**
*   **Bots cannot swap places** directly in one tick (head-on collision).

## Timeout & Errors
*   **Time Limit**: Your code has a limited time to respond (e.g., 20ms - 100ms per tick).
*   **Timeout**: If you exceed the limit, your turn is skipped.
*   **Crash**: If your code throws an exception, your turn is skipped.
*   **Disqualification**: Too many consecutive errors/timeouts will disqualify you from the match.
