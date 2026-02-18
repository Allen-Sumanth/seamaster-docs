# Actions & Abilities

Every tick, each of your bots can perform **one** action.

## Energy & Scrap Costs

### Energy Costs
Bots consume energy for movement and actions.

*   **Base Movement Cost**: 2 HP per move.

| Ability | Traversal Modifier (per move) | Action Cost (on use) |
| :--- | :--- | :--- |
| **Harvest** | +0 | 1 |
| **Scout** | +1.5 | 0 |
| **Self-Destruct** | +0.5 | 0 |
| **Speed Boost** | +1 | 0 |
| **Poison** | +0.5 | 2 |
| **Lockpick** | +1.5 | 0 |
| **Shield** | +0.25 | 0 |
| **Deposit** | +0 | 1 |

### Scrap Costs
Base cost to spawn a bot is **10 Scraps**. Adding abilities increases the cost:

| Ability | Scrap Cost |
| :--- | :--- |
| **Harvest** | 8 |
| **Scout** | 8 |
| **Self-Destruct** | 6 |
| **Lockpick** | 6 |
| **Speed Boost** | 8 |
| **Poison** | 7 |
| **Shield** | 7 |

---

## Actions
Your bots can perform the following physical actions on the board:

### Move
Bots can move in cardinal directions: `NORTH`, `SOUTH`, `EAST`, `WEST`.

*   **Cost**: 2 Energy per move.
*   **Speed**: 1 tile per tick.
*   **Associated Ability**: `Speed Boost` (Doubles speed, reduces energy cost).

??? example "Movement Example"
    ```python linenums="1"
    from seamaster.constants import Direction
    from seamaster.translate import move

    def act(self):
        # Move North
        return move(Direction.NORTH)
    ```

### Harvest
*   **Action**: `HARVEST`
*   **Requirement**: Must be on top of an Algae tile.
*   **Effect**: Removes algae from board, adds +1 to inventory.
*   **Energy Cost**: 1 Energy.
*   **Associated Ability**: `Harvest` (Required to perform action).
*   **Warning**: Harvesting **Poisonous Algae** kills the bot instantly.
*   **Move + Harvest**: You can specify a `direction` to move and harvest in the same tick. The bot moves one step in the `direction` and attempts to harvest at the *new* location.

!!! note "Python Library Update"
    The Python library is currently being updated to support the optional `direction` parameter for `harvest`, `lockpick`, and `poison`.

??? example "Harvesting Example"
    ```python linenums="1" hl_lines="9"
    from seamaster.constants import Direction
    from seamaster.translate import harvest

    def act(self):
        # Move + Harvest (Adjacent Tile)
        return harvest(Direction.NORTH)
    ```

### Deposit
*   **Action**: `DEPOSIT`
*   **Requirement**: Must be within range of a **Bank** you own.
*   **Effect**: Starts a deposit timer (100 ticks). If effective, converts inventory to score.
*   **Vulnerability**: While depositing, you are immovable and vulnerable to theft.
*   **Associated Ability**: `Harvest` (implied, as you need to harvest to deposit).

??? example "Banking Example"
    ```python linenums="1"
    from seamaster.translate import deposit

    def act(self):
        # If we are at a bank we own, deposit
        if self.ctx.is_at_bank():
            return deposit(None)
    ```

### Self-Destruct
*   **Action**: `SELFDESTRUCT`
*   **Requirement**: `Ability.SELF_DESTRUCT`
*   **Effect**: The bot explodes, destroying itself and **all bots** (friend or foe) within a **1-tile radius** (3x3 area).
*   **Energy Cost**: 0.5 Energy.
*   **Associated Ability**: `Self-Destruct` (Required to perform action).
*   **Counter**: `Shield` ability.

### Lockpick
*   **Action**: `LOCKPICK`
*   **Requirement**: Must be adjacent to a Bank where an enemy is depositing.
*   **Effect**: Steals the deposit.
*   **Risk**: The Lockpick bot **dies** after the theft is complete (Suicide mission).
*   **Move + Lockpick**: You can initiate a lockpick on a bank from an adjacent tile. The bot moves adjacent to the bank and begins the lockpick in the same tick.
*   **Associated Ability**: `Lockpick` (Required to perform action).

??? example "Lockpick Example"
    ```python linenums="1"
    from seamaster.translate import lockpick
    from seamaster.constants import Direction

    def act(self):
        # Move adjacent to bank and start lockpicking
        return lockpick(direction=Direction.WEST)
    ```

### Poison
*   **Action**: `POISON`
*   **Requirement**: Must be on top of an Algae tile.
*   **Effect**: Turns the algae into **Poisonous Algae**.
*   **Energy Cost**: 2 Energy.
*   **Associated Ability**: `Poison` (Required to perform action).
*   **Move + Poison**: You can specify a `direction` to move and poison in the same tick.

??? example "Poison Example"
    ```python linenums="1"
    from seamaster.constants import Direction
    from seamaster.translate import poison

    def act(self):
        # Move South and poison the algae there
        return poison(Direction.SOUTH)
    ```

---

## Abilities
Abilities are special upgrades or traits that your bots can possess:

### Harvest
*   **Description**: Allows the bot to harvest algae and deposit it at banks.
*   **Note**: Essential for scoring.

### Scout
*   **Description**: Reveals the `is_poison` status of all algae within a **4-tile radius**.
*   **Note**: Without this ability (or proximity), algae status remains "UNKNOWN". Only bots with the **Scout** ability can distinguish Poisonous Algae from Safe Algae. Global vision gives you coordinates, but Scouting gives you safety.



### Self-Destruct
*   **Description**: Allows the bot to self-destruct, dealing area damage.

### Lockpick
*   **Description**: Allows the bot to steal deposits from enemy banks.

### Speed Boost
*   **Description**: Increases movement speed and efficiency.
*   **Effect**: Movement speed doubled (2 tiles per tick).
*   **Energy Cost**: 1 Energy per move (More efficient!).

### Poison
*   **Description**: Allows the bot to poison algae tiles, creating traps for enemy bots.

### Shield
*   **Description**: Passive protection against damage.
*   **Effect**: If hit by a `SelfDestruct` or other damage, the shield breaks instead of the bot dying. The bot loses the Shield ability but survives.
*   **Side Effect**: Shield increases movement energy cost by **0.25**.