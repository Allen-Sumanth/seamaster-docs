# Win Conditions

There are three ways to end a match.

## 1. Absolute Dominance
If at any point a player has permanently deposited **> 50%** of the total algae on the map:
*   **Result**: Immediate Victory.

## 2. Time Limit
If the game reaches **1000 Ticks**:
*   The game ends.
*   **Winner**: Information based on **Permanent Algae** count.
    *   Player with most deposited algae wins.
    *   If tied, it interprets as a Draw (or potentially falls back to total assets, but standard rule is Draw).

## 3. Disqualification
If a player's bot code crashes or times out consecutively (e.g., 5 times in a row):
*   **Result**: That player loses immediately.

## Economy Strategy
Winning requires a balance:
*   **Harvesting**: To deny enemy resources.
*   **Banking**: To secure points (Harvested algae in inventory does NOT count for the win until deposited!).
*   **Combat**: To drain enemy scraps and energy.
