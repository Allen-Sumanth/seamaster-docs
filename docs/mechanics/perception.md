# Player View & Perception

Unlike many other strategy games, Seawars provides **Global Vision**. You have access to the entire game state through the `PlayerView` object, with one specific exception (Algae Poison Status).

## The PlayerView Object

Your bot logic receives a `PlayerView` object each tick. This object serves as the single source of truth for the game state.

??? example "Accessing PlayerView"
    ```python linenums="1"
    def act(self):
        # Access the view via self.ctx.api.view
        playerview = self.ctx.api.view
        
        print(f"Current Tick: {playerview.tick}")
        print(f"My Scraps: {playerview.scraps}")

        # Alternatively, use the helper functions in gameAPI
        print(f"Current Tick: {self.ctx.api.get_tick()}")
        print(f"My Scraps: {self.ctx.api.get_scraps()}")
    ```

!!! note "Indirect Access Preferred"
    In most cases, you do not need to interact with the `PlayerView` object directly. The helper functions provided in [GameAPI](../api_reference/game_api.md), [BotContext](../api_reference/bot_context.md), and [Utilities](../api_reference/utilities.md) cover almost all common use cases (finding nearest entities, pathfinding, checking global stats, etc.). Use the raw `playerview` only when you need custom filtering or data not exposed by the helper methods.

### Global Fields
*   **tick**: Current game tick (0 to 500).
*   **scraps**: Your current global currency count.
*   **algae**: Your current score (total permanent algae secured).
*   **bot_id_seed**: The starting ID for your next spawned bot.
*   **bots**: A list of all your own alive bots with full status details.

### Visible Entities (Enemies & Scraps)
The `visible_entities` field contains dynamic objects on the board.

*   **Enemies (`visible_entities.enemies`)**: A list of **ALL** enemy bots currently on the board. You know their ID, Location, Scraps held, and Abilities.
*   **Scraps (`visible_entities.scraps`)**: A list of scraps dropped on the ground from destroyed bots.

??? example "Filtering Enemies"
    ```python linenums="1"
    from seamaster.constants import Ability
    from seamaster.models import EnemyBot

    def act(self):
        enemies: list[EnemyBot] = self.ctx.api.view.visible_entities.enemies
        
        # Find enemies carrying algae
        rich_enemies = [e for e in enemies if e.algae_held > 0]
        
        # Find enemies with SCOUT ability
        scouts = [e for e in enemies if Ability.SCOUT in e.abilities]
    ```

### Permanent Entities (Map Features)
The `permanent_entities` field contains static or semi-static map features.

*   **Banks**: Locations of all banks.
*   **Energy Pads**: Locations and status of energy pads.
*   **Walls**: Locations of all wall tiles.
*   **Algae (`permanent_entities.algae`)**: A list of **ALL** algae resource tiles on the board.

### Structure Reference
The `PlayerView` object follows this structure:

```json linenums="1"
{
  "tick": "int",
  "scraps": "int",
  "algae": "int",           // Your total score
  "bot_id_seed": "int",     // Next ID for your spawned bot
  "max_bots": "int",
  "width": "int",
  "height": "int",
  
  "bots": {                 // Map of Your_Bot_ID -> Bot Object
    "id": {
      "id": "int",
      "location": {"x": "int", "y": "int"},
      "energy": "float",
      "scraps": "int",
      "abilities": ["str"], // ["HARVEST", "SCOUT", ...]
      "algae_held": "int",
      "status": "str"       // "ALIVE"
    }
  },

  "visible_entities": {
    "enemies": [            // List of ALL enemy bots
      {
        "id": "int",
        "location": {"x": "int", "y": "int"},
        "scraps": "int",
        "abilities": ["str"]
      }
    ],
    "algae": [              // List of ALL algae
       {
         "location": {"x": "int", "y": "int"},
         "is_poison": "str" // "UNKNOWN" | "TRUE" | "FALSE"
       }
    ]
  },

  "permanent_entities": {
     "banks": { "id": { ... } },      // Map of Bank_ID -> Bank Object
     "energy_pads": { "id": { ... } }, // Map of Pad_ID -> Pad Object
     "walls": [{"x": "int", "y": "int"}]
  }
}
```

## The Poison Mechanic (Hidden Info)

While you know the **location** of every algae tile from the start, you do not inherently know if it is safe or poisonous.

### Algae Properties
Each Algae object in `permanent_entities.algae` has an `is_poison` field with three possible values (defined in `AlgaeType`):  
1.  **"UNKNOWN"**: The default state. You know algae is there, but not if it's safe.   
2.  **"TRUE"**: Confirmed Poisonous.   
3.  **"FALSE"**: Confirmed Safe. 

!!! note "Poison ability"
  The algae properties are updated when scouts go near the algae. It does not take into account when the opponent uses their poison ability.

### Revealing Poison (Scouting)
To reveal the `is_poison` status, you must use the **Scout** ability.

*   **Ability**: `SCOUT`
*   **Range**: 2 tiles (Manhattan Distance).
*   **Effect**: Any algae within **2 tiles** of a bot with the `SCOUT` ability will have its `is_poison` field updated to "TRUE" or "FALSE" in your `PlayerView`.

!!! important
    This is the only "Hidden Information" in the game. Enemy movement and map layout are fully visible.

??? example "Safe Harvesting Logic"
    ```python linenums="1"
    from seamaster.constants import AlgaeType
    
    def is_safe_to_harvest(self, algae):
        # Only harvest if CONFIRMED safe
        if algae.is_poison == AlgaeType.FALSE:
            return True
        return False
        
    def act(self):
        # Example: iterate visible algae and check safety
        for algae in self.ctx.api.view.visible_entities.algae:
            if self.is_safe_to_harvest(algae):
                # Go harvest it...
                pass
    ```
