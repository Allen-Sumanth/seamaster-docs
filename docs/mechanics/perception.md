# Perception

Bots in Ocean Master are not omniscient. They operate under a "Fog of War".

## Vision Radius
Every bot has a standard **Vision Radius of 4 tiles**.
This is a **Manhattan Distance** (or Chebyshev? *Engine code `VisionRadius = 4` is constant. The exact shape depends on implementation of `sense` functions which are in `ctx` (User code part). `engine.md` doesn't show the `sense` implementation, but typically in grid games it's Manhattan or Square. `user_code.md` uses `manhattan_distance`. I will assume Manhattan or Euclidean radius 4 implies a diamond or circle. The `VisionRadius` constant in engine is just an integer. The `Scout` ability implies "Scouting: will look at algae...". Let's assume standard grid visibility.*).

> [!NOTE]
> For the purpose of strategy, assume you can see any entity within **4 steps** of your bot.

## What You Can See
Within this radius, your bot receives data about:
1.  **Terrain**: Walls and empty tiles.
2.  **Resources**: Locations of **Algae** (and can distinguish **Poisonous** from Good).
3.  **Entities**: Banks and Energy Pads.
4.  **Other Bots**: Enemy and friendly bot locations and their stats (Energy, Scraps).

## Global Knowledge
While bots have limited vision, your **Code** (the `BotController`) has access to some global state via the `GameAPI` or `Context`.
*   [TODO] Clarify exactly what global info is available. *The engine `PlayerViewDTO` likely contains full board state for the player's bots. But usually, competitive games limit this.*
*   **Assumption**: You only know what your aggregated bots can see. If you have no bots in an area, you cannot see algae or enemies there.

## Context Object
Your bot's `act()` method receives a context object providing this sensory data.
```python
visible_algae = ctx.sense_algae(radius=4)
enemies = ctx.sense_enemies_in_radius(radius=4)
```
