# BotController

Base class for all bot strategies. accessible in `agent/src/seamaster/bot_controller.py`.

To create a new bot strategy, you must inherit from `BotController` and implement the `act` method.
The `act` method is called every tick and must return an `Action` or `None`.

You can access the `BotContext` via `self.ctx` to interact with the game state.

### Example
```python linenums="1"
from seamaster.botbase import BotController
from seamaster.constants import Ability
from seamaster.translate import Action

class MyBot(BotController):
    # Define abilities to equip
    ABILITIES = [Ability.SPEED_BOOST]

    def __init__(self, ctx, args=None):
        super().__init__(ctx, args)
        # Custom initialization

    def act(self) -> Action | None:
        # Main logic loop
        return None 
```

### Methods
*   `act()`: Abstract method. Must be implemented by the subclass. Returns `Action` or `None`.
*   `spawn(location, args)`: Class method to create a spawn specification.

## Actions (`seamaster.translate`)
To perform an action, your `act` method must return an `Action` object. These helper functions in `seamaster.translate` create the appropriate `Action` for you.

*   `move(direction)`: Moves the bot in the given direction.
*   `move_speed(direction)`: Moves the bot 2 steps in the given direction (requires `SPEED_BOOST` ability).
*   `harvest(direction)`: Harvests algae in the given direction.
*   `deposit(direction)`: Deposits resources into a bank or energy pad in the given direction.
*   `self_destruct()`: Destroys the bot and deals damage to surrounding units.

### Example Action Logic
Here is an example of how to use these actions in your bot's logic:

```python linenums="1"
from seamaster.botbase import BotController
from seamaster.translate import move, harvest, deposit
from seamaster import utils

class harvester_bot(BotController):
    def act(self):
        # 1. Deposit Algae if holding any
        if self.ctx.get_algae_held() > 0:
            nearest_bank = self.ctx.get_nearest_bank()
            if nearest_bank:
                dist = utils.manhattan_distance(self.ctx.get_location(), nearest_bank.location)
                
                # If adjacent, deposit
                if dist < 2:
                    return deposit(utils.direction_from_point(self.ctx.get_location(), nearest_bank.location))
                
                # Otherwise move towards bank
                hops = utils.get_optimal_next_hops(self.ctx.get_location(), nearest_bank.location)
                if hops:
                    return move(hops[0])

        # 2. Harvest Algae
        nearest_algae = self.ctx.get_nearest_algae()
        if nearest_algae:
            dist = utils.manhattan_distance(self.ctx.get_location(), nearest_algae.location)
            
            # If adjacent, harvest
            if dist < 2:
                return harvest(utils.direction_from_point(self.ctx.get_location(), nearest_algae.location))
            
            # Move towards algae
            hops = utils.get_optimal_next_hops(self.ctx.get_location(), nearest_algae.location)
            if hops:
                return move(hops[0])
        
        return None
```
