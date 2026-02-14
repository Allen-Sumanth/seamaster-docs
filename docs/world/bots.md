# The Bot

The Bot is the fundamental unit of Seawars. You do not control a single character; you control a swarm.

## Stats
Every bot shares the same base statistics:

*   **Energy**: Starts at **50**. Consumed by movement and abilities.
*   **Inventory**: Can hold up to **5 Algae**.

## Construction & Cost
Bots are designed as **modular units**. You start with an **Empty Shell** (chassis) and equip it with **Abilities**.

*   **Construction Cost**: The total cost to spawn a bot.
*   **Formula**: `Total Cost = Base Cost + Sum(Ability Costs)`

Currently, the **Base Cost** for the shell is **0 scraps**, meaning you only pay for the abilities you choose. However, a functional bot typically requires at least **Movement**, enforcing a practical minimum cost (e.g., 10 scraps).

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
