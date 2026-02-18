# BotContext (`self.ctx`)

Accessible inside `act()` via `self.ctx`. Provides a read-only interface to the game state for a specific bot.

### Robot Status
*   `get_id()`: Returns the unique bot ID (int).
*   `get_energy()`: Returns current energy (int).
*   `get_location()`: Returns current `Point` (x, y).
*   `get_abilities()`: Returns list of abilities (`list[str]`).
*   `get_algae_held()`: Returns amount of algae held (int).
*   `get_type()`: Returns list of abilities (alias for `get_abilities`).
*   `spawn_cost(abilities)`: Returns the scrap cost to spawn a bot with given abilities (int).

#### Example
```python linenums="1"
# Check energy and location
if self.ctx.get_energy() < 10:
    print(f"Bot {self.ctx.get_id()} is low on energy at {self.ctx.get_location()}")
```

### Sensing
*   `sense_enemies()`: Returns list of visible `EnemyBot`s.
*   `sense_enemies_in_radius(point, radius)`: Returns list of `EnemyBot`s within radius of a point.
*   `sense_own_bots()`: Returns list of your other `Bot`s.
*   `sense_own_bots_in_radius(point, radius)`: Returns list of your `Bot`s within radius of a point.
*   `sense_algae(radius)`: Returns list of `Algae` within radius of the bot.
*   `sense_algae_in_radius(point, radius)`: Returns list of `Algae` within radius of a point.
*   `sense_unknown_algae(point)`: Returns sorted list of `(distance, Algae)` tuples for algae with unknown poison status.
*   `sense_scraps_in_radius(point, radius)`: Returns list of `Scrap` within radius of a point.
*   `sense_objects()`: Returns a dict containing lists of `scraps`, `banks`, and `energypads`.
*   `sense_walls()`: Returns list of all visible walls (`list[Point]`).
*   `sense_walls_in_radius(point, radius)`: Returns list of walls within radius of a point.

#### Example
```python linenums="1"
# Find enemies nearby
enemies = self.ctx.sense_enemies_in_radius(self.ctx.get_location(), 2)
if enemies:
    # React to enemy
    pass
```

### Pathing & Checks
*   `next_point(pos, direction)`: Returns the next `Point` in direction, or `None` if out of bounds.
*   `next_point_speed(pos, direction, step)`: Returns next `Point` for speed move (step 1 or 2), or `None` if invalid.
*   `run_bfs(start, end)`: Returns a list of points representing the shortest path, or empty list if no path.
*   `can_move(direction)`: Returns `True` if moving in detail direction is within map bounds.
*   `shortest_path(target)`: Returns Manhattan distance to target (int).
*   `check_blocked_point(point)`: Returns `True` if point is blocked by wall, enemy, or own bot.
*   `check_blocked_direction(direction)`: Returns `True` if moving in direction would result in a blocked position.
*   `can_defend()`: Returns `True` if bot has `SHIELD` ability.
*   `can_spawn(abilities)`: Returns `True` if you have enough scraps and bot limit is not reached.

#### Example
```python linenums="1"
from seamaster.constants import Direction

# Check if moving North is possible
if self.ctx.can_move(Direction.NORTH):
    # Check if blocked by obstacle
    if not self.ctx.check_blocked_direction(Direction.NORTH):
        return move(Direction.NORTH)
```

### Nearest Object Helpers
*   `get_nearest_bank()`: Returns the nearest `Bank`.
*   `get_energy_pads()`: Returns list of all `EnergyPad`s.
*   `get_nearest_energy_pad()`: Returns the nearest `EnergyPad`.
*   `get_nearest_scrap()`: Returns the nearest `Scrap`.
*   `get_nearest_algae()`: Returns the nearest `Algae`.
*   `get_nearest_enemy()`: Returns the nearest enemy `Bot`.

#### Example
```python linenums="1"
from seamaster.entities import EnergyPad
from seamaster.models.energy_pad import EnergyPad

# Go to nearest energy pad
pad: EnergyPad = self.ctx.get_nearest_energy_pad()
if pad:
     # Move towards pad...
     pass
```

### Collision Avoidance
*   `move_target(bot_pos, target_pos)`: Returns the best `Direction` to move towards target, avoiding obstacles. Returns `None` if no path.
*   `move_target_speed(bot_pos, target_pos)`: Returns a tuple `(Direction, steps)` for speed-boosted movement. `steps` is 1 or 2.

#### Example
```python linenums="1"
# Safe movement towards target
direction = self.ctx.move_target(self.ctx.get_location(), target_point)
if direction:
    return move(direction)
```
