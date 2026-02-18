# The Bot

The Bot is the fundamental unit of Seawars. You do not control a single character; you control a swarm.

## The Bot Object
`Bot` objects are the core data structure representing your units.

```python linenums="1"
class Bot:
    id: int
    location: Point
    energy: float
    scraps: int
    abilities: List[Ability]
    algae_held: int
    traversal_cost: float
    status: str
```

### Attributes

*   **id**: Unique identifier for the bot within the match. Use this to track specific units across ticks.
*   **location**: Current coordinates (`x`, `y`) on the board.
!!! note
    The location of the bot is a Point object, which points to its abosulte position in the board. Refer to [Board Coordinates](../arena/board.md#coordinates) for more details.
*   **energy**: Current energy level. Max 50. Dropping to 0 prevents actions.
*   **scraps**: The amount of scraps this bot is "worth" (the cost to spawn it). This value is used for scoring/rewards when destroyed.
*   **abilities**: List of abilities equipped on this bot (e.g., `["HARVEST", "SPEEDBOOST"]`).
*   **algae_held**: Current number of algae in inventory. Max 5.
*   **traversal_cost**: The energy cost for this bot to move 1 tile. Calculated based on equipped abilities.
*   **status**: Current state of the bot (e.g., "ACTIVE", "DEAD").

## Construction & Cost
Bots are designed as **modular units**. You start with an **Empty Shell** (chassis) and equip it with **Abilities**.

*   **Construction Cost**: The total cost to spawn a bot.
*   **Formula**: `Total Cost = Base Cost + Sum(Ability Costs)`

Currently, the **Base Cost** for the shell is **0 scraps**, meaning you only pay for the abilities you choose. However, a functional bot typically requires at least **Movement**, enforcing a practical minimum cost (e.g., 10 scraps).

## The Life Cycle
1.  **Spawn**: You request a spawn at your designated spawn zone. Costs scraps.
2.  **Act**: Every tick, your code issues a command (Move, Harvest, etc.).
3.  **Refill**: When bots run out of energy, they are unable to execute any actions (movement or abilities) that require energy. To recharge energy before it runs out, bots must visit an **Energy Pad**.
4.  **Death**: Bots die if:
    *   They execute `SelfDestruct`.
    *   They are hit by a `SelfDestruct` explosion.
    *   They harvest **Poisonous Algae**.
