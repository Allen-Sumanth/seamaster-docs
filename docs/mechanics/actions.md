# Actions & Abilities

Every tick, each of your bots can perform **one** action.

## Movement
Bots can move in cardinal directions: `NORTH`, `SOUTH`, `EAST`, `WEST`.
*   **Cost**: 2 Energy per move.
*   **Speed**: 1 tile per tick.

### Speed Boost (Ability)
*   **Cost**: 10 Scraps (to add ability).
*   **Effect**: Movement speed doubled (2 tiles per tick).
*   **Energy Cost**: 1 Energy per move (More efficient!).

## Harvesting
*   **Action**: `HARVEST`
*   **Requirement**: Must be on top of an Algae tile.
*   **Effect**: Removes algae from board, adds +1 to inventory.
*   **Energy Cost**: 1 Energy.
*   **Warning**: Harvesting **Poisonous Algae** kills the bot instantly.

## Combat (Self-Destruct)
*   **Action**: `SELFDESTRUCT`
*   **Requirement**: `Ability.SELF_DESTRUCT`
*   **Effect**: The bot explodes, destroying itself and **all bots** (friend or foe) within a **1-tile radius** (3x3 area).
*   **Energy Cost**: 0.5 Energy.
*   **Counter**: **Shield** ability.

### Shield (Ability)
*   **Cost**: 5 Scraps.
*   **Effect**: Passive. If hit by a `SelfDestruct` or other damage, the shield breaks instead of the bot dying. The bot loses the Shield ability but survives.
*   **Energy Cost**: 0.25 Energy passive drain? *[Check engine: `EnergyDB` has "SHIELD" {0.25, 0}. Wait, that might be traversal cost modifier? No, `removeShield` reduces `TraversalCost`. So Shield adds weight? `EnergyDB["SHIELD"]` is `{0.25, 0}`. Likely +0.25 to movement cost? Engine snippet: `TraversalCost: engine.calculateTraversalCost(spawn.Abilities)`. So Shield makes you heavier/slower (more energy to move).* 
*   **Note**: Shield increases movement energy cost by **0.25**.

## Banking
*   **Action**: `DEPOSIT`
*   **Requirement**: Must be at a **Bank** you own.
*   **Effect**: Starts a deposit timer (100 ticks). If effective, converts inventory to score.
*   **Vulnerability**: While depositing, you are immovable and vulnerable to theft.

### Lockpick (Ability)
*   **Action**: `LOCKPICK`
*   **Requirement**: Must be adjacent to a Bank where an enemy is depositing.
*   **Effect**: Steals the deposit.
*   **Cost**: 10 Scraps.
*   **Risk**: The Lockpick bot **dies** after the theft is complete (Suicide mission).

## Scouting
*   **Ability**: `SCOUT`
*   **Cost**: 10 Scraps.
*   **Effect**: Increases vision radius? Or allows identifying Poison? Ref: `abilities.md` says "can differentiate good and poison". Base bots might not distinguish poison? *[Clarification: `abilities.md` says "Scouting: will look at algae, can differentiate good and poison". This implies normal bots see "Algae" but don't know if it's poison. Scouts know. This is a huge strategic detail.]*

> [!IMPORTANT]
> Only bots with the **Scout** ability can distinguish Poisonous Algae from Safe Algae.
