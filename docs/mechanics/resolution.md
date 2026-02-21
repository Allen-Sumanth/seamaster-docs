# Resolution Rules

The game engine resolves turns in distinct phases. Understanding the order of operations is crucial for predicting game states.

## Turn Order

The Game Loop processes a tick in the following order:

1.  **Spawning**: New bots are created.
2.  **Action Resolution**: All actions (including movement) submitted by clients are sorted by priority and executed.
3.  **Entity Updates**: Banks and Energy Pads update their timers.
4.  **Win Check**: Victory conditions are checked.

## Action Priority

The current logic sorts all the actions that come to the backend and executes them in the following order (highest number first):

1.  **`SELFDESTRUCT`** (Priority: 6)
2.  **`HARVEST`** (Priority: 5)
3.  **`POISON`** (Priority: 4)
4.  **`DEPOSIT`** (Priority: 3)
5.  **`LOCKPICK`** (Priority: 2)
6.  **`MOVE`** (Priority: 1)

If an action is valid, the energy cost is deducted immediately. If invalid, the bot pays a penalty.

## Movement Resolution

Since `MOVE` has the lowest priority, it is resolved after all other actions. Movement is resolved simultaneously for all bots but calculated iteratively to handle collisions and chains.

If multiple bots attempt to move into the *same* target tile:

*   **Random Winner**: One bot is randomly selected to succeed.
*   **Cancellation**: All other bots attempting to enter that tile will have their moves cancelled and will stay in their current positions.

## Energy Costs
*   **Success**: If a move is successful, `TraversalCost` is deducted.
*   **Failure**: If a move is cancelled due to collision or contention, but the bot *attempted* to move, a small penalty is deducted (instead of the full traversal cost).