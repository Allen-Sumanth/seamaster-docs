# GameAPI

Accessible in `spawn_policy(api)`.

### Global Information
*   `get_tick()`: Returns the current tick of the game (int).
*   `get_scraps()`: Returns the total scraps available to you (int).
*   `get_my_bots()`: Returns a list of all bots owned by you (`list[Bot]`).

### Sensing
*   `visible_enemies()`: Returns a list of all visible enemy bots (`list[EnemyBot]`).
*   `visible_scraps()`: Returns a list of all visible scrap entities (`list[Scrap]`).
*   `banks()`: Returns a list of visible banks (`list[Bank]`).
*   `energypads()`: Returns a list of visible energy pads (`list[EnergyPad]`).
*   `visible_walls()`: Returns a list of visible walls (`list[Point]`).
*   `visible_algae()`: Returns a list of visible algae (`list[Algae]`).

### Spawning
*   `can_spawn(abilities)`: Returns `True` if you have enough scraps to spawn a bot with the given abilities (`list[Ability]`).

#### Example
```python linenums="1"
from seamaster import GameAPI, BotController

# Access in spawn_policy
def spawn_policy(api: GameAPI):
    # Check global state
    if api.get_scraps() >= 20:
        return [{"location": 0, "strategy": ...}]

# Access inside a Bot using self.ctx.api
class MyBot(BotController):
    def act(self):
        # You can access the API directly if needed
        all_banks: list[Bank] = self.ctx.api.banks()
```
