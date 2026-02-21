# Win Conditions

There are three ways to end a match.

## 1. Absolute Dominance
If at any point a player has permanently deposited **> 50%** of the total algae on the map:
*   **Result**: Immediate Victory.

## 2. Time Limit
If the game reaches **500 Ticks**:

*   The game ends.
*   **Winner**: Information based on **Permanent Algae** count.
    *   Player with most deposited algae wins.
    *   If tied, it interprets as a Draw.

## 3. Timeout
The Code Runner maintains a **Timeout Score** for each bot.

*   **Timeout Event**: If a bot's code times out or crashes, its Timeout Score increases.
*   **Normal Execution**: If the bot executes successfully, its Timeout Score decreases (or stays at 0).
*   **Disqualification**: If the **Timeout Score reaches 5**, the match ends immediately, and that player loses.

