Oceanmaster is a programming game where players write code to control bots that harvest algae and battle for dominance against other players' algorithms in real-time strategic matches.
Format

Users have to write a Python script, using our custom Python library, to control the movement and abilities of the bots.

Players start each match with a fixed amount of scraps (the game's currency) and use them to build different bot types with unique abilities and costs.

The result of the game is decided when a player is able to permanently harvest over 50% of the algae in the game board, or when 1000 ticks (turns) have passed.

Players climb the leaderboard by gaining ELO after winning their matches

The Game Board

Each game is played on the game board, which is 20x20 grid that contains algae in specific, predetermined spots.

The goal of each player is to collect algae, while strategically managing their resources (bots, scraps) and defending against attacks from the opponent.

Players can also attack the bots of other players, using the self-destruct ability, where the bot destroys itself and all bots in a 1-block radius around it.
4 banks exist on the map, 2 on each side.
Bots can deposit algae into a bank, and have to defend it for 100 ticks to deposit it permanently.

Bots with the Lockpick ability can steal from a bank while it’s being deposited.
2 energy refill stations exist on the center of the map
Gameplay

This is a 1v1 turn-based game, where a user’s algorithm is matched with another user’s algorithm that is most evenly matched, based on the matchmaking formula.
Each player starts off with 100 scraps, which can be used to build bots with special abilities (harvesting, self destruction, etc.)

After each tick (turn), each player recieves 1 scrap.

The Bot

Each bot is an empty template, which can carry abilities.

Bots require a certain amount of scraps (10), and energy points (50) and each ability added on to it will further increase the scrap cost of creating the bot.
The movement of the bot is designed by the user - a few template bots will have their movement mechanisms baked in, these can be used as is or as an inspiration to build custom movement logic.
The bot abilities and costs will be specified in the game documentation (to be released soon).

