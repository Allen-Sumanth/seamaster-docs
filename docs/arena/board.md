# The Board

The game is played on a fixed **20x20 grid**.

## Coordinates
The board uses a standard Cartesian coordinate system where **(0,0)** is the corner.

*   **X-axis**: 0 to 19.
*   **Y-axis**: 0 to 19.

!!! note
    `X` is the horizontal axis. `Y` is the vertical axis.

## Walls
The board contains static walls that block movement. Bots cannot move into or through walls.

*   **Symmetry**: The wall layout is **symmetric** and **deterministic**. It is the same for every match (unless the map generation code changes).
*   **Coordinates**: You can find the exact list of wall coordinates in your `PlayerView` object under `permanent_entities.walls`.
*   **Reference**: See [Player View & Perception](../mechanics/perception.md) for data structure details.

## Spawning Zones
Players spawn on **opposite sides** of the board.

*   **Player 1 (You)**: Spawns on the edge where `y=0`.
*   **Player 2 (Opponent)**: Spawns on the edge where `y=19`.

!!! note "Coordinate Flipping"
    To ensure fairness and simplicity, the engine **flips the x-coordinates** for Player 2. This means both players can write logic assuming they are on the "left" (or "right", depending on perspective), but their actual positions on the grid are mirrored.

When you spawn a bot using `spawn(location=x)`, it appears at coordinate `(x, 0)` for Player 1, or `(x, 19)` for Player 2. Valid `location` values are `0` to `19`.
