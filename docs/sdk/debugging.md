# Debugging & Logs

## Runtime Logs
The game engine captures standard output (`stdout`) and standard error (`stderr`).

*   **Stdout**: Used for game communication.
*   **Stderr**: Use `sys.stderr` for debugging information.

```python linenums="1"
import sys
print("DEBUG: My bot is stuck!", file=sys.stderr)
```

## Common Errors
1.  **Timeout**: Your `act()` function took too long. Optimize your code.
2.  **Memory Limit**: You allocated too much memory. Avoid large global lists.
3.  **Invalid Move**: You tried to walk into a wall or another bot.

## The Sandwich Strategy
If your bot is behaving strangely, check if it's dead. Dead bots cannot act.
Check if you have Energy. Low energy bots cannot move.
