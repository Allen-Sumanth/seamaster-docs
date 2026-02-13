# The Board

The game is played on a fixed **20x20 grid**.

## Coordinates
The board uses a standard Cartesian coordinate system:
*   **Top-Left**: (0, 0) ? *Wait, engine implementation usually implies 0,0 is bottom-left or top-left depending on iteration order. `incrementLocation` in `engine.md` increments Y for "NORTH" and decrements for "SOUTH". This implies (0,0) is likely **Bottom-Left**.*
*   **X-axis**: 0 to 19 (West to East).
*   **Y-axis**: 0 to 19 (South to North).

> [!NOTE]
> `X` increases towards East. `Y` increases towards North.

## Walls
The board contains static walls that block movement. Bots cannot move into or through walls.

The wall layout is symmetric and predetermined:
*   Walls exist at `x=6` and `x=13`.
*   Walls exist at `y=6` and `y=13`.
*   *(Specific gaps exist in these lines, creating a structured arena).*

## Spawning Zones
*   **Player 1** spawns on the **Left** side (Lower X).
*   **Player 2** spawns on the **Right** side (Higher X, `x=19` is hardcoded for P2 spawns in engine).
