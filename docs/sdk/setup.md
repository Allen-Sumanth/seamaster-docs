# SDK Setup

To play Ocean Master, you need to write a Python script that uses the `oceanmaster` library.

## Prerequisites
*   Python 3.10+
*   `oceanmaster` library (Provided in the game environment, or installable via `pip install oceanmaster` for local development).

## Project Structure
A typical bot project looks like this:

```
my_bot/
├── main.py            # Entry point (provided by template)
├── my_strategy.py     # Your custom logic
├── submission.py      # The file you submit
```

## The Submission File (`submission.py`)
The game engine expects a specific structure. Your code **must** define:

1.  **Bot Classes**: Classes inheriting from `BotController`.
2.  **Spawn Policy**: A function `spawn_policy(api)` that returns a list of bots to spawn.

> [!TIP]
> Use the [Standard Templates](templates.md) as a starting point.
