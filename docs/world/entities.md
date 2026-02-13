# Game Entities

Beyond walls and empty space, the grid contains several interactive entities.

## Algae (Resources)
Algae is the primary resource in Ocean Master. It spawns randomly at the start of the match and does not regrow.

*   **Abundance**: Roughly 15% of the board tiles contain algae (~60 total).
*   **Poisonous Algae**: About 5% of algae is **poisonous**.
    *   **Normal Algae**: Can be harvested for resource points.
    *   **Poisonous Algae**: **Kills** any bot that attempts to harvest it (unless the bot has specific immunities/abilities, though standard behavior is fatal).

> [!WARNING]
> Scout before you harvest! Indiscriminating harvesting is a quick way to lose bots.

## Banks
Banks are secure locations where you can deposit harvested algae to make it "Permanent".

*   **Count**: 4 Banks total.
*   **Ownership**: 
    *   2 Banks belong to **Player 1** (West side).
    *   2 Banks belong to **Player 2** (East side).
*   **Function**: Bots must stay at a bank for **100 ticks** to deposit their inventory.
*   **Vulnerability**: While depositing, the algae is vulnerable to theft by bots with the **Lockpick** ability.

## Energy Pads
Energy Pads are refill stations for your bots. All bots spawn with limited energy and must recharge to keep moving/acting.

*   **Count**: 2 Energy Pads (Located near the center).
*   **Function**: Moving onto an active pad instantly refills a bot's energy to max (50).
*   **Cooldown**: After use, the pad becomes inactive for a duration.
    *   **Early Game**: 50 ticks cooldown.
    *   **Mid/Late Game**: Cooldown decreases as the match progresses (down to 10 ticks).

## Scraps (Currency)
Scraps are used to spawn new bots and buy abilities.
*   **Starting Scraps**: 100 per player.
*   **Passive Income**: +1 scrap per tick.
*   **Salvage**: +50% of a bot's cost is dropped as scraps when a bot dies (harvestable). *[Note: Engine code implies dropping scraps, need to verify if automatically credited or must be harvested. Engine `KillBot` simply deletes. `game_info.md` says "Can be obtained by harvesting fallen bots". This implies a mechanic not fully detailed in the snippet, possibly a TODO]* 

> [!NOTE]
> Currently, the precise mechanic for harvesting scraps from dead bots is under review. Assume for now you rely on passive income and starting capital.
