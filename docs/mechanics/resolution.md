# Resolution Rules

The game engine resolves turns in distinct phases. Understanding the order of operations is crucial for predicting game states.

## Turn Order...

The Game Loop processes a tick in the following order:

1.  **Spawning**: New bots are created.
2.  **Movement**: Bot movement is resolved.
3.  **Actions**: Non-movement actions (HARVEST, SELFDESTRUCT, etc.) are validated and executed.
4.  **Entity Updates**: Banks and Energy Pads update their timers.
5.  **Win Check**: Victory conditions are checked.

## Movement Phase

Movement is resolved simultaneously for all bots but calculated iteratively to handle collisions and chains.
If multiple bots attempt to move into the *same* target tile:
*   **Random Winner**: One bot is randomly selected to succeed.
*   **Cancellation**: All other bots attempting to enter that tile will have their moves cancelled and will stay in their current positions.


## Action Phase
Non-movement actions are processed before movement. This includes:
*   `HARVEST`
*   `SELFDESTRUCT`
*   `POISON`
*   `LOCKPICK`
*   `DEPOSIT`

If an action is valid, the energy cost is deducted immediately. If invalid, the bot pays a penalty.

## Energy Costs
*   **Success**: If a move is successful, `TraversalCost` is deducted.
*   **Failure**: If a move is cancelled due to collision or contention, but the bot *attempted* to move, a small penalty is deducted (instead of the full traversal cost).