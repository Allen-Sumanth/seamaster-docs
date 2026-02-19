# Actions & Abilities

Every tick, each of your bots can perform upto **one** action and/or **one** movement.

!!! note "Move + Action"
    Action is performed at the final location of the bot after accounting for collisions.

## Energy & Scrap Costs

### Energy Costs
Bots consume energy for movement and actions.

*   **Base Movement Cost**: 2 energy per move.

| Ability | Traversal Modifier (per move) | Action Cost (on use) |
| :--- | :--- | :--- |
| **Harvest** | +0 | 1 |
| **Scout** | +3 | 0 |
| **Self-Destruct** | +0.5 | 0 |
| **Speed Boost** | +0.5 | 1 |
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
Bots can move in cardinal directions: `NORTH`, `SOUTH`, `EAST`, `WEST`. There's an additional `NULL` direction which is especially useful when the bot does not have to move but perform an action.

*   **Energy Cost**: Base cost 2 energy + cumulative ability traversal cost per move.
*   **Speed**: 1 tile per tick.
*   **Associated Ability**: `SPEEDBOOST` (Doubles speed, reduces energy cost).

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
*   **Requirement**: Must be on top of an algae tile or in one block radius.
*   **Effect**: Removes algae from board, adds +1 to inventory.
*   **Energy Cost**: 1 Energy.
*   **Associated Ability**: `HARVEST` (Required to perform action).
*   **Warning**: Harvesting **Poisonous Algae** kills the bot instantly.

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
*   **Effect**: Starts a deposit timer (50 ticks). Upon completition, the algae is permanently deposited to the player owning the deposit.
*   **Vulnerability**: While depositing is instant, the bank is vulnerable to lockpick attempts.
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
*   **Effect**: The bot explodes, destroying itself and **all bots** (friend or foe) within a **1-tile radius** (3x3 area) without an account for the bot movement.
*   **Energy Cost**: 0.5 Energy.
*   **Associated Ability**: `SELFDESTRUCT` (Required to perform action).
*   **Counter**: `Shield` ability.

### Lockpick
*   **Action**: `LOCKPICK`
*   **Requirement**: Must be in **one** block radius of a Bank undergoing deposition for **20** ticks.
*   **Effect**: Steals the deposit.
*   **Associated Ability**: `LOCKPICK` (Required to perform action).

!!! note "Lockpick"
    Lockpick is immediately canceled upon leaving the one bot radius or death.

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
*   **Requirement**: Bot must be within **1** block radius.
*   **Effect**: Turns the algae into **Poisonous Algae**.
*   **Energy Cost**: 2 Energy.
*   **Associated Ability**: `POISON` (Required to perform action).

??? example "Poison Example"
    ```python linenums="1"
    from seamaster.constants import Direction
    from seamaster.translate import poison

    def act(self):
        # Move South and poison the algae there
        return poison(Direction.SOUTH)
    ```

---

## Passive Abilities
Passive Abilities provide permanent boost/upgrades.

### Scout
*   **Description**: Reveals the `is_poison` status of all algae within a **4-tile radius**.
*   **Note**: Without this ability (or proximity), algae status remains "UNKNOWN". Only bots with the **Scout** ability can distinguish Poisonous Algae from Safe Algae. Global vision gives you coordinates, but Scouting gives you safety.

### Shield
*   **Description**: Passive protection against damage.
*   **Effect**: If hit by a `SELFDESTRUCT` or other damage, the shield breaks instead of the bot dying. The bot loses the Shield ability but survives.
*   **Side Effect**: Shield increases movement energy cost by **0.25**.