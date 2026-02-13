this file has 3 snippets which represent how user will write code
these represent different strategies how user code can be

```py
"""
easy level testcase for usercode
just using predefined bots and very basic zone based strategy
"""


# import necessary modules and classes here
from ast import For
from oceanmaster.botbase import BotController
from oceanmaster.templates.flash_scout import FlashScout
from oceanmaster.templates.forager import Forager
from oceanmaster.templates.lurker import Lurker
from oceanmaster.templates.saboteur import Saboteur
#define your custom bot class here
class Custom_Bot_Name(BotController):
    ABILITIES = []

    #set up the bot with any necessary initializations
    def __init__(self, ctx):
        super().__init__(ctx)

    #master strategy for the bot (to be executed at every tick)
    def act(self):
        pass

# define the spawn policy for your bots here (the conditions under which they are spawned)
#return a list/array of bot spawn specifications
def spawn_policy(api):
    policy = []
    tick = api.get_tick()
    it = 0;
    # ZONE 1
    # for the first 50 ticks spawn scouts every 5 ticks ->10 scouts
    if tick < 50 and tick % 5==0:
        policy.append(FlashScout.spawn(location=it))
        it = it+1


    # ZONE 2
    # spawn a forager every 10 ticks and a saboteur every 15 ticks
    if tick > 50 and tick<120:
        if tick%10==0:
            policy.append(Forager.spawn(location=it))
            it=it+1
        if tick%15==0:
            policy.append(Saboteur.spawn(location=it))
            it=it+1


    # ZONE 3
    # spawn less foragers and more saboteurs
    if tick > 120 and tick <200 and tick%10 == 0:
        if tick % 10 ==0:
            policy.append(Saboteur.spawn(location=it))
            it=it+1

        if tick % 20 ==0:
            policy.append(Forager.spawn(location=it))
            it=it+1


    # ZONE 4
    # Harvest more
    if tick>200:
        if tick % 10 == 0:
            policy.append(Forager.spawn(location=it))
            it=it+1

        if tick % 30 == 0:
            policy.append(Saboteur.spawn(location=it))
            it=it+1

    # global lurker policy ->every 30 ticks spawn a lurker

    if tick%30==0:
        policy.append(Lurker.spawn(location=it))
        it=it+1

    return policy```



```py
"""
medium level testcase for user
Has custom bots -> Vanguard,
"""

# import necessary modules and classes here
from oceanmaster.api.game_api import GameAPI
from oceanmaster.botbase import BotController
from oceanmaster.constants import Ability, Direction
from oceanmaster.translate import move, move_speed, self_destruct
from oceanmaster.templates.forager import Forager
from oceanmaster.templates.saboteur import Saboteur
from oceanmaster.templates.lurker import Lurker

from oceanmaster.utils import manhattan_distance
#define your custom bot class here


class Vanguard(BotController):
    """
    Can scout for more algae +1 life

    """
    ABILITIES = [Ability.SHIELD, Ability.SCOUT]

    #set up the bot with any necessary initializations
    def __init__(self, ctx):
        super().__init__(ctx)


    #master strategy for the bot (to be executed at every tick)
    def act(self):
        ctx = self.ctx
        bot_pos = ctx.get_location()

        radius = 2
        while radius <= 10:
            visible = ctx.sense_algae(radius=radius)
            if visible:
                d = ctx.move_target(bot_pos, visible[0].location)
                if d:
                    return move(d)
            radius += 1
        return move(Direction.NORTH)

class Kamikaze(BotController):
    """
    if a lockpick is happening it goes to the bank and self-destructs
    """
    ABILITIES = [Ability.SELF_DESTRUCT,Ability.SPEED_BOOST]

    def __init__(self,ctx):
        super().__init__(ctx)
        self.target = self.args["target"].location if self.args else None

    def act(self):
        ctx = self.ctx
        loc = ctx.get_location()

        if self.target and manhattan_distance(loc,self.target)<=1:
            return self_destruct()

        if self.target:
            d,steps = ctx.move_target_speed(loc,self.target)
            if d:
                return move_speed(d,steps)

        return move(Direction.NORTH)

# define the spawn policy for your bots here (the conditions under which they are spawned)
#return a list/array of bot spawn specifications
def spawn_policy(api):
    policy = []
    tick = api.get_tick()
    it = 0

    my_bots = api.get_my_bots()
    no_vanguards = sum(1 for b in my_bots if Ability.SHIELD in b.ABILITIES)
    no_foragers = sum(1 for b in my_bots if Ability.HARVEST in b.ABILITIES)
    no_saboteurs = sum(1 for b in my_bots if Ability.SELF_DESTRUCT in b.ABILITIES)

    for bank in api.banks():
        if bank.is_bank_owner and bank.lockpick_occuring:
            if api.can_spawn(Kamikaze.ABILITIES):
                policy.append(
                    Kamikaze.spawn(
                        location=it,
                        args={
                            "target":bank.location
                        }
                    )
                )
                it=it+1

    if tick < 40:
        if tick % 8 == 0 and no_vanguards < 4:
            if api.can_spawn(Vanguard.ABILITIES):
                policy.append(Vanguard.spawn(location=it))
                it += 1

    if 40 <= tick < 120:
        if tick % 15 == 0 and no_foragers < 3:
            if api.can_spawn(Forager.ABILITIES):
                policy.append(Forager.spawn(location=it))
                it += 1

        if tick % 25 == 0 and no_vanguards < 6:
            if api.can_spawn(Vanguard.ABILITIES):
                policy.append(Vanguard.spawn(location=it))
                it += 1

    if 120 <= tick < 200:
        if tick % 20 == 0 and no_saboteurs < 3:
            if api.can_spawn(Saboteur.ABILITIES):
                policy.append(Saboteur.spawn(location=it))
                it += 1

        if tick % 30 == 0:
            if api.can_spawn(Lurker.ABILITIES):
                policy.append(Lurker.spawn(location=it))
                it += 1

    if tick >= 200:
        if tick % 10 == 0:
            if api.can_spawn(Forager.ABILITIES):
                policy.append(Forager.spawn(location=it))
                it += 1

        if tick % 18 == 0:
            if api.can_spawn(Saboteur.ABILITIES):
                policy.append(Saboteur.spawn(location=it))
                it += 1

    return policy
```

```py
# import necessary modules and classes here
from oceanmaster.botbase import BotController
from oceanmaster.constants import Ability,Direction
from oceanmaster.translate import move,move_speed,self_destruct
from oceanmaster.utils import manhattan_distance
from oceanmaster.models.point import Point
from oceanmaster.templates.saboteur import Saboteur
from oceanmaster.templates.lurker import Lurker
from oceanmaster.templates.flash_scout import FlashScout
from oceanmaster.templates.forager import Forager


class Vanguard(BotController):
    """
    Can scout for more algae +1 life

    """
    ABILITIES = [Ability.SHIELD, Ability.SCOUT]

    def __init__(self, ctx):
        super().__init__(ctx)

    def act(self):
        ctx = self.ctx
        bot_pos = ctx.get_location()

        radius = 2
        while radius <= 10:
            visible = ctx.sense_algae(radius=radius)
            if visible:
                d = ctx.move_target(bot_pos, visible[0].location)
                if d:
                    return move(d)
            radius += 1
        return move(Direction.NORTH)

class Kamikaze(BotController):
    """
    if a lockpick is happening it goes to the bank and self-destructs
    """
    ABILITIES = [Ability.SELF_DESTRUCT,Ability.SPEED_BOOST]

    def __init__(self,ctx,args=None):
        super().__init__(ctx)
        self.target = args["target"].location if args else None

    def act(self):
        ctx = self.ctx
        loc = ctx.get_location()

        if self.target and manhattan_distance(loc,self.target)<=1:
            return self_destruct()

        if self.target:
            d,steps = ctx.move_target_speed(loc,self,self.target)
            if d:
                return move_speed(d,steps)

        return move(Direction.NORTH)

class Guardian(BotController):
    ABILITIES = [Ability.SHIELD, Ability.SELF_DESTRUCT]

    def __init__(self, ctx, args=None):
        super().__init__(ctx)
        self.bank = args["bank"] if args else None
        self.patrol_idx = 0
        self.patrolling = False

        if self.bank:
            x, y = self.bank.location.x, self.bank.location.y
            self.patrol = [
                Point(x, y + 1),
                Point(x + 1, y + 1),
                Point(x + 1, y),
                Point(x + 1, y - 1),
                Point(x, y - 1),
                Point(x - 1, y - 1),
                Point(x - 1, y),
                Point(x - 1, y + 1),
            ]

    def act(self):
        ctx = self.ctx
        loc = ctx.get_location()

        if ctx.sense_enemies_in_radius(loc, radius=1):
            return self_destruct()

        if not self.bank:
            return None

        if not self.patrolling:
            if manhattan_distance(loc, self.bank.location) == 1:
                self.patrolling = True
            else:
                d = ctx.move_target(loc, self.bank.location)
                if d:
                    return move(d)
                return None

        target = self.patrol[self.patrol_idx % 8]

        if loc == target:
            self.patrol_idx += 1
            return None

        dx = target.x - loc.x
        dy = target.y - loc.y

        if dx > 0:
            return move(Direction.SOUTH)
        if dx < 0:
            return move(Direction.NORTH)
        if dy > 0:
            return move(Direction.WEST)
        if dy < 0:
            return move(Direction.EAST)

        return None


def spawn_policy(api):
    policy = []
    tick = api.get_tick()
    it = 0

    my_bots = api.get_my_bots()
    banks = api.banks()

    guardians = [
        b for b in my_bots
        if Ability.SHIELD in b.abilities and Ability.SELF_DESTRUCT in b.abilities
    ]

    foragers = [b for b in my_bots if Ability.HARVEST in b.abilities]

    for bank in banks:
        if not bank.is_bank_owner:
            continue

        guarded = any(
            manhattan_distance(b.location, bank.location) <= 2
            for b in guardians
        )

        if not guarded:
            if api.can_spawn(Guardian.ABILITIES):
                policy.append(
                    Guardian.spawn(
                        location=it,
                        args={"bank": bank},
                    )
                )
                it += 1

        if bank.lockpick_occuring and not guarded:
            if api.can_spawn(Kamikaze.ABILITIES):
                policy.append(
                    Kamikaze.spawn(
                        location=it,
                        args={"target": bank.location},
                    )
                )
                it += 1


    if tick < 80:
        if api.can_spawn(Vanguard.ABILITIES):
            policy.append(Vanguard.spawn(location=it))
            it += 1
        else:
            policy.append(FlashScout.spawn(location=it))
            it += 1

    if 80 <= tick < 200:
        if len(foragers) < 3 and tick % 15 == 0:
            if api.can_spawn(Forager.ABILITIES):
                policy.append(Forager.spawn(location=it))
                it += 1

        if tick % 20 == 0:
            if api.can_spawn(Lurker.ABILITIES):
                policy.append(Lurker.spawn(location=it))
                it += 1

    if 200 <= tick < 350:
        if tick % 15 == 0:
            if api.can_spawn(Saboteur.ABILITIES):
                policy.append(Saboteur.spawn(location=it))
                it += 1

        if tick % 25 == 0:
            if api.can_spawn(Lurker.ABILITIES):
                policy.append(Lurker.spawn(location=it))
                it += 1

    if tick >= 350:
        if tick % 10 == 0:
            if api.can_spawn(Forager.ABILITIES):
                policy.append(Forager.spawn(location=it))
                it += 1

        if tick % 12 == 0:
            if api.can_spawn(Saboteur.ABILITIES):
                policy.append(Saboteur.spawn(location=it))
                it += 1

    return policy```
