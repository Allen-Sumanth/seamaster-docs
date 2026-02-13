# API Reference

## `GameAPI`
Accessible in `spawn_policy(api)`.

*   `get_tick()`: Returns current game tick (int).
*   `get_my_bots()`: Returns list of your active `Bot` objects.
*   `banks()`: Returns list of `Bank` objects.
*   `can_spawn(abilities)`: Returns `True` if you have enough scraps.

## `BotContext` (`self.ctx`)
Accessible inside `act()`.

### Sensing
*   `get_location()`: Returns `Point(x, y)`.
*   `sense_algae(radius)`: Returns list of `Algae` within radius.
*   `sense_enemies_in_radius(radius)`: Returns list of enemy `Bot`s.
*   `sense_banks()`: Returns observable banks.

### Movement & Actions
*   `move_target(start, end)`: Helper. Returns the `Direction` to move towards target.
*   `move_target_speed(start, end)`: Helper for speed-boosted bots.

## Helpers (`oceanmaster.translate`)
*   `move(direction)`: Returns a move command.
*   `move_speed(direction)`: Returns a double-speed move command.
*   `self_destruct()`: Returns self-destruct command.
*   `harvest()`: Returns harvest command.
