Each bot can have a combination of the following abilities:
Harvesting: can collect algae in a 1 block radius (4 blocks) around it. Dies if it collects a poison algae. Could experiment with refilling energy on harvest
Poisoning: Poison algae
Scouting: will look at algae, can differentiate good and poison.
Self destruct: Can destroy itself, and all bots in a 1 block radius.
Speed boost: if standard move takes x ticks, it can move in x/2 ticks.
Shield: will take two hits to destroy.
Lockpick: allows breaking bank


Our task is to tabulate the scrap cost and atp usage for all abilities.
Also provide new ability and template ideas (if any)

Templates:
(These should have low synergy by default to encourage player creativity)

Forager: Harvesting and Scouting
Saboteur: Shield & Self-destruct
Flash Scout: Scouting and Speed boost (Example of a good synergy)
Heat seeker. speed boost, self destruct, accepts a location as coordinate, goes there and boom 
Lurker: Lockpick


Algo:
On each tick, every bot’s algorithm is run to return a single action, e.g move 1 block west, mine this block, etc
If for any bot, it takes more than say 10 ms, the turn for that bot is relinquished and next bot algo is run.
Max bot cap - 20
Board:
20x20 grid -> 400 squares
Around 15% algae -> 60 algae in a game 
1000 ticks per round
Energy refill stations, that replenish energy when passed through. Exists in the halfway point in the map. Takes 50 ticks to refill for first 300. 25 ticks at 300 ticks. 10 ticks at 700 ticks.
4 Banks, two in each side. When a player deposits, it takes 100 ticks for the algae to be permanently deposited, until then a theft bot can steal it,(provided more than 20 ticks left to deposit)
Win condition - higher amount of algae at the end of 1000 ticks OR > 50% of algae permanently deposited.


Scraps:
Starting scraps - 100.
Can be obtained by harvesting fallen bots (drops 50 percent of maker’s cost). 
1 scrap given per tick (could also experiment with exponential increase for more bots later in the game)
Since base bots have vision, there’s a 10 scrap minimum cost.
Energy:
Each bot spawns with 50 energy points. 
Base movement cost is 2
Can be refilled by walking over the energy pad in the center of the map, which has a varying cooldown.



How to use scraps during every round:
All decisions about scrap usage must come from an algorithm so the script has access to:
Current scrap count
Current bot count
Current board state (within visibility rules)
Templates the player designed

The OceanMaster can have written code like
if scrap >= cost("HarvesterTemplate"):
    spawn("HarvesterTemplate")

if scrap >= upgrade_cost(bot.id, "Harvest"):
    upgrade(bot.id, "Harvest")


if scrap >= cost("Rebirth") and senseEnemyNearby():
    upgrade(bot.id, "Shield")




Below is a table of abilities row by row

Ability
Scrap cost (SC) 
Energy cost (EC)
---
Harvest
10
0 traversal, 1 mining
---
Scout
10
1.5 traversal, 2 pulse
---
Self destruct
5
 0.5
---
Movement speed x2
10
1
---
Shield
5
0.25
---
Poison
5
0.5 traversal 2 poison
---
Lockpick
10
1.5 traversal. Dies after lockpicking. 20 ticks to steal


