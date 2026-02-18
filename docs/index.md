# Welcome to SeaWars!

**Seawars** is a competitive programming game where you write code to control bots in a real-time strategic battle. Your goal is to harvest algae, manage your economy, and outsmart your opponent's algorithm.

## The Objective

You are the commander of a fleet of automated bots. Your mission is to dominate the ocean grid by:

1.  **Harvesting Algae**: Collecting resources to build your economy.
2.  **Banking Resources**: Securely depositing algae to score permanent points.
3.  **Combat**: Destroying enemy bots to deny them resources.

The winner is determined after **500 ticks** (turns) based on who has collected the most algae, or immediately if a player captures (harvests and succefully deposits in their own banks) **>50%** of the total algae on the map. See [Win Conditions](mechanics/win_conditions.md) for more details.

## How It Works

Seawars is a **1v1 turn-based game**.

*   **You write code**: You submit a Python script containing a bot controller class. This code defines your strategy for the entire match and cannot be changed once the game begins. Your bot's logic must autonomously guide its actions across all 500 ticks of the game.
*   **The Engine runs the match**: Your code is executed every tick alongside your opponent's code.
*   **Real-time Logic**: You must make decisions about movement, spawning, and combat within strict time limits.

## Getting Started

1.  Read about [The Board](arena/board.md) and [Game Entities](arena/entities.md) to understand the environment.
2.  Learn the [Rules of Perception](mechanics/perception.md) and [Actions](mechanics/actions_and_abilities.md).
3.  Jump into the [SDK Guide](sdk/writing_bots.md) to write your first bot.
