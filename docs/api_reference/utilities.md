# Utilities (`seamaster.utils`)

Collection of helper functions for geometry and pathfinding.

*   `manhattan_distance(p1, p2)`: Returns the Manhattan distance between two `Point`s (int).
*   `next_point(p, direction)`: Returns the next `Point` in a given `Direction`, or `None` if out of bounds.
*   `direction_from_point(p1, p2)`: Returns the primary `Direction` from `p1` to `p2`.
*   `get_direction_in_one_radius(src: Point, trg: Point)`: Returns the direction from `src` to `trg` if it lies in one radius.
*   `get_optimal_next_hops(start, end)`: Returns a list of `Direction`s representing optimal moves from `start` to `end`.
*   `get_shortest_distance_between_points(start, end)`: Returns the shortest path distance (int) between two points using precomputed paths.

#### Example
```python linenums="1"
from seamaster.utils import manhattan_distance, get_optimal_next_hops
from seamaster.constants import Direction

# Calculate distance
dist = manhattan_distance(p1, p2)

# Get path directions
hops: list[Direction] = get_optimal_next_hops(start_pos, end_pos)
if hops:
    next_move = hops[0]
```
