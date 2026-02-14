# Player View & Perception

Unlike many other strategy games, Seawars provides **Global Vision**. You have access to the entire game state through the `PlayerView` object, with one specific exception (Algae Poison Status).

## The PlayerView Object

Your bot logic receives a `PlayerView` object each tick. This object serves as the single source of truth for the game state.

### Global Fields
*   **tick**: Current game tick (0 to 1000).
*   **scraps**: Your current global currency count.
*   **algae**: Your current score (total permanent algae secured).
*   **bot_id_seed**: The starting ID for your next spawned bot.
*   **bots**: A list of all your own alive bots with full status details.

### Visible Entities (Enemies & Scraps)
The `visible_entities` field contains dynamic objects on the board.

*   **Enemies (`visible_entities.enemies`)**: A list of **ALL** enemy bots currently on the board. You know their ID, Location, Scraps held, and Abilities.
*   **Scraps (`visible_entities.scraps`)**: A list of scraps dropped on the ground from destroyed bots.

### Permanent Entities (Map Features)
The `permanent_entities` field contains static or semi-static map features.

*   **Banks**: Locations of all banks.
*   **Energy Pads**: Locations and status of energy pads.
*   **Walls**: Locations of all wall tiles.
*   **Algae (`permanent_entities.algae`)**: A list of **ALL** algae resource tiles on the board.

### Structure Reference
The `PlayerView` object follows this structure:

```json
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

### Revealing Poison (Scouting)
To reveal the `is_poison` status, you must use the **Scout** ability.

*   **Ability**: `SCOUT`
*   **Range**: 4 tiles (Manhattan Distance).
*   **Effect**: Any algae within **4 tiles** of a bot with the `SCOUT` ability will have its `is_poison` field updated to "TRUE" or "FALSE" in your `PlayerView`.

!!! important
    This is the only "Hidden Information" in the game. Enemy movement and map layout are fully visible.
