# Welcome to Ocean Master

**Ocean Master** is a competitive programming game where you write code to control bots in a real-time strategic battle. Your goal is to harvest algae, manage your economy, and outsmart your opponent's algorithm.

## The Objective

You are the commander of a fleet of automated bots. Your mission is to dominate the ocean grid by:

1.  **Harvesting Algae**: Collecting resources to build your economy.
2.  **Banking Resources**: Securely depositing algae to score permanent points.
3.  **Combat**: Destroying enemy bots to deny them resources.

The winner is determined after **1000 ticks** (turns) based on who has collected the most algae, or immediately if a player captures **>50%** of the total algae on the map.

## How It Works

Ocean Master is a **1v1 turn-based game**.

*   **You write code**: You provide a Python class that controls your bots.
*   **The Engine runs the match**: Your code is executed every tick alongside your opponent's code.
*   **Real-time Logic**: You must make decisions about movement, spawning, and combat within strict time limits.

## Getting Started

1.  Read about [The Board](world/board.md) and [Game Entities](world/entities.md) to understand the environment.
2.  Learn the [Rules of Perception](mechanics/perception.md) and [Actions](mechanics/actions.md).
3.  Jump into the [SDK Guide](sdk/writing_bots.md) to write your first bot.
