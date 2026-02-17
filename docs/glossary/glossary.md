# Glossary

### Fundamentals
*   **Tick**: A single discrete time unit in the game. The game lasts for a maximum of **500 Ticks**.
*   **Round**: Often used interchangeably with Tick, but technically refers to the full process of both players submitting moves and the engine resolving them.
*   **Arena / Board**: The game world. A **20x20** grid where all gameplay takes place.
*   **Coordinates**: The grid system used to locate entities, ranging from `(0,0)` to `(19,19)`.
*   **SeaMaster**: The game engine that resolves moves and maintains the state.
*   **CodeRunner**: The system that executes player code safely involved in the timeout logic.

### Entities & Resources
*   **Entity**: Any object on the board, including Bots, Algae, Banks, and Energy Pads.
*   **Bot**: The primary unit controlled by players. Bots have Energy, Scraps, and can hold Algae.
*   **Scrap**: The resource used to **spawn** new bots. Scraps are finite and managed at the player level.
*   **Energy**: The fuel for bots. Moving and performing abilities consumes Energy.
*   **Algae**: The primary scoring resource. Harvested from the board and deposited at Banks.
*   **Bank**: A structure where Algae is deposited to earn points.
*   **Energy Pad**: A structure that instantly replenishes a bot's Energy to full.

### Abilities & Actions
*   **Loadout**: The specific set of abilities a bot is spawned with.
*   **Abilities**: Special skills assigned to bots (e.g., Speed Boost, Shield, Poison).
*   **Context (`ctx`)**: The data object containing current game state visible to a bot.
*   **Scout**: Reveals hidden information like Poison within a **4-tile radius**.
*   **Lockpick**: Steals deposits from enemy banks.
*   **Manhattan Distance**: The distance metric used ( |x1-x2| + |y1-y2| ).
