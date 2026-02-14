# Game Entities

Beyond walls and empty space, the grid contains several interactive entities.

## Algae (Resources)
Algae is the primary resource in Seawars. It spawns randomly at the start of the match and does not regrow.
*   **Abundance**: Roughly 15% of the board tiles contain algae (~60 total).
*   **Visibility**: You know the **location** of every algae tile on the board from the start (`PlayerView.permanent_entities.algae`).
*   **Poison Status**: Roughly 5% of algae is **Poisonous**. This status is **Hidden** ("UNKNOWN") until scouted.
    *   **Normal Algae**: Can be harvested for resource points.
    *   **Poisonous Algae**: **Kills** any bot that attempts to harvest it.

!!! warning
    Scout before you harvest! While you can see where the algae is, indiscriminately harvesting "UNKNOWN" algae is a risk.

## Banks
Banks are secure locations where you can deposit harvested algae to make it "Permanent".

*   **Count**: 4 Banks total.
*   **Ownership**: 
    *   2 Banks belong to **Player 1** (South side).
    *   2 Banks belong to **Player 2** (North side).
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
Scraps are the currency used to **construct** new bots. You pay for the bot's chassis and its equipped abilities.

*   **Global Pool**: All scraps belong to you (the player), not individual bots.
*   **Starting Scraps**: 100 per player.
*   **Passive Income**: +1 scrap per tick.
*   **Salvage**: When a bot dies, it drops **50% of its total cost** on the tile where it fell.

!!! note
    Bots with the **Harvest** ability can collect these dropped scraps by moving onto the tile. Collected scraps are immediately added to your global pool.
