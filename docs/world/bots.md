# The Bot

The Bot is the fundamental unit of Ocean Master. You do not control a single character; you control a swarm.

## Stats
Every bot shares the same base statistics:

*   **Energy**: Starts at **50**. Consumed by movement and abilities.
*   **Vision Radius**: **4 tiles**. Bots can only "see" entities within this range.
*   **Inventory**: Can hold up to **5 Algae**.

## Construction & Cost
Bots are modular. You build them by assigning **Abilities** to a chassis.

*   **Base Cost**: 0 scraps (but effectively determined by abilities).
*   **Minimum Cost**: 10 scraps (Since most functional bots need at least Movement or Vision, usually `Harvest` or `Scout` ability implies the base). *[Engine `validateSpawn` sums `CostDB`. `CostDB` values are e.g. Harvest=10, Scout=10. `game_info.md` mentions "base bots have vision, there’s a 10 scrap minimum cost".]*

The total cost of a bot is the sum of its abilities.

## The Life Cycle
1.  **Spawn**: You request a spawn at your designated spawn zone. Costs scraps.
2.  **Act**: Every tick, your code issues a command (Move, Harvest, etc.).
3.  **Refill**: Bots run out of energy. You must visit an **Energy Pad** to recharge.
4.  **Death**: Bots die if:
    *   They run out of Energy? *(Engine check: `energyCost > bot.Energy` prevents action. It doesn't explicitly `KillBot` on 0 energy, but the bot becomes useless).*
    *   They execute `SelfDestruct`.
    *   They are hit by a `SelfDestruct` explosion.
    *   They harvest **Poisonous Algae**.
    *   They `Lockpick` (Lockpicking is a suicide mission).
