# Writing Your Bot

A bot consists of two parts: the **Brain** (Logic) and the **Birth** (Spawn Policy).

## 1. The Brain (`BotController`)
You define a class that inherits from `BotController`. The `act()` method is called every tick.

```python
from oceanmaster.botbase import BotController
from oceanmaster.constants import Ability, Direction
from oceanmaster.translate import move

class MyHarvester(BotController):
    # Define abilities this bot needs
    ABILITIES = [Ability.HARVEST]

    def act(self):
        # 1. Get info
        current_loc = self.ctx.get_location()
        
        # 2. Make decision
        if self.ctx.sense_algae(radius=1):
            return move(Direction.NORTH) # Or harvest command
            
        # 3. Return action
        return move(Direction.SOUTH)
```

## 2. The Birth (`spawn_policy`)
You must tell the engine **when** to correct bots.

```python
def spawn_policy(api):
    spawn_list = []
    tick = api.get_tick()
    
    # Simple logic: Spawn a harvester every 10 ticks
    if tick % 10 == 0:
        spawn_list.append(
            MyHarvester.spawn(location=0) # Location is relative offset in spawn zone
        )
        
    return spawn_list
```

## State Management
You can store state in your bot class `__init__`.

```python
class Patroller(BotController):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.direction = Direction.NORTH
        
    def act(self):
        # Use and update self.direction
        pass
```

> [!WARNING]
> Global variables outside the class may reset or behave unexpectedly. Use `self` to store bot-specific memory.
