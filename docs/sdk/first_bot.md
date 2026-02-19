# Build Your First Bot (Custom Logic)

In this guide, we will write a complete bot from scratch. While the `seamaster` library provides powerful **Templates** (see [Writing Your Bot](writing_bots.md)), writing your own logic gives you maximum control.

We will build a **Harvester Bot** that autonomousy manages its energy, harvests algae, and deposits it at a bank.

!!! tip "Copy-Paste Friendly"
    The code blocks in this guide have aligned line numbers. You can copy and paste them sequentially into your file to build the complete bot.

## 1. Imports and Setup
Create a new file `my_first_bot.py`. We start by importing the necessary components from the library.

```python linenums="1"
from seamaster import GameAPI
from seamaster.botbase import BotController
from seamaster.constants import Ability, ABILITY_COSTS, SCRAP_COSTS, Direction
from seamaster.models import EnergyPad, Bank
from seamaster.translate import move, harvest, deposit
from seamaster import utils
import random
```

## 2. Defining the Bot Class
We inherit from `BotController` and define our capabilities.

```python linenums="9" hl_lines="2"
class harvester_bot(BotController):
    ABILITIES = [Ability.HARVEST]  # (1)
    ability_scrap_cost = SCRAP_COSTS[Ability.HARVEST]
    ability_energy_cost = ABILITY_COSTS[Ability.HARVEST] 

    def __init__(self, ctx):
        super().__init__(ctx)
```

1.  **Capabilities**: We declare that this bot needs the `HARVEST` ability. The game engine uses this to calculate spawn costs.

## 3. The Brain (`act`)
The `act()` method is the heart of your bot. It runs every tick. Our logic follows a simple priority system:

1.  **Survival**: If energy is low, find a charger.
2.  **Banking**: If carrying *any* algae, go deposit immediately.
3.  **Work**: Otherwise, find algae and harvest.

```python linenums="17"
    def act(self):
        # 1. Survival: If energy is below 50%, head to recharge ports
        current_energy = self.ctx.get_energy()
        if current_energy < 25:
            nearest_energy_pad : EnergyPad = self.ctx.get_nearest_energy_pad()
            # Calculate path to energy pad
            move_priorities = utils.get_optimal_next_hops(self.ctx.get_location(), nearest_energy_pad.location) # (1)
            if move_priorities:
                return move(move_priorities[0]) # (2)

        # 2. Banking: If I'm carrying algae, deposit it
        if self.ctx.get_algae_held() > 0:
            # Find banks owned by me
            banks: list[Bank] = {
                bank for bank in self.ctx.api.banks() 
                    if bank.is_bank_owner == True
            }
            if banks:
                # Find nearest bank
                nearest_bank: Bank = min(banks, key=lambda bank: utils.manhattan_distance(self.ctx.get_location(), bank.location))
                dist_to_bank = utils.get_shortest_distance_between_points(self.ctx.get_location(), nearest_bank.location)
                
                # If adjacent, deposit. Else, move towards it.
                if not dist_to_bank or dist_to_bank < 2:
                    return deposit(utils.direction_from_point(self.ctx.get_location(), nearest_bank.location)) # (3)
                else:   
                    move_priorities = utils.get_optimal_next_hops(self.ctx.get_location(), nearest_bank.location)
                    if move_priorities:
                        return move(move_priorities[0])

        # 3. Work: Find and harvest algae
        nearest_algae = self.ctx.get_nearest_algae()
        dist_to_algae = utils.manhattan_distance(self.ctx.get_location(), nearest_algae.location)
        
        if dist_to_algae >= 2:
            alg_move_priorities = utils.get_optimal_next_hops(self.ctx.get_location(), nearest_algae.location)
            if alg_move_priorities:
                return move(alg_move_priorities[0])
        elif dist_to_algae < 2 and dist_to_algae > 0:
            return harvest(utils.direction_from_point(self.ctx.get_location(), nearest_algae.location)) # (4)
        else: 
            return harvest(None)
```

1.  **Pathfinding**: `utils.get_optimal_next_hops` helps navigate around obstacles.
2.  **Action**: We execute the move command.
3.  **Deposit**: Uses `direction_from_point` to target the specific bank tile.
4.  **Harvest**: Targeted harvest ensures we grab the specific algae we want.

## 4. The Spawn Policy
Finally, we tell the engine to create our bots.

!!! bug "Spawn Policy" 
    This function must be declared at the top level of the file and named `spawn_policy`. Your code will not run if this is not present.

```python linenums="54" hl_lines="8"
def spawn_policy(gameAPI: GameAPI):
    # Spawn a harvester in every tick
    spawn_rules = [] 

    # spawn a harvester at a random X location
    spawn_x = random.randint(0, gameAPI.view.width-1)
    spawn_rules.append(harvester_bot.spawn(spawn_x)) # (1)
    return spawn_rules
```

1.  **Spawn**: We invoke the `spawn` class method on our custom bot class.

## Next Steps
Congratulations! You've written a custom bot from scratch. 

To go further:

*   Explore **[Writing Your Bot](writing_bots.md)** for detailed API documentation.
*   Learn about **Collision Resolution** in [Resolution Rules](../mechanics/resolution.md).
