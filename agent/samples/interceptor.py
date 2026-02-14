from oceanmaster.botbase import BotController
from oceanmaster.translate import move, move_speed, self_destruct
from oceanmaster.constants import Ability, Direction
from oceanmaster.utils import manhattan_distance


class Interceptor(BotController):
    """
    Interceptor is a reactive counter unit designed to eliminate
    enemy bots possessing the LOCKPICK ability.

    Behavior:
    - Every tick, evaluates all visible enemy bots
    - Selects the nearest enemy with LOCKPICK ability
    - Moves toward it using speed boost
    - Self-destructs when within Manhattan distance 1
    """

    ABILITIES = [Ability.SPEED_BOOST, Ability.SELF_DESTRUCT]

    def __init__(self, ctx):
        super().__init__(ctx)

    def act(self):
        ctx = self.ctx
        loc = ctx.get_location()

        lockpickers = [
            e for e in ctx.api.visible_enemies()
            if Ability.LOCKPICK in e.abilities
        ]

        if lockpickers:
            lockpickers.sort(
                key=lambda e: manhattan_distance(loc, e.location)
            )
            target = lockpickers[0].location

            if manhattan_distance(loc, target) <= 1:
                return self_destruct()

            d, steps = ctx.move_target_speed(loc, target)
            if d:
                return move_speed(d, steps)

        return move(Direction.NORTH)
    
    
LOCKPICK_WINDOW = 20
LOCKPICK_THRESHOLD = 2

lockpick_history = []
prev_pressure = 0

def spawn_policy(api):
    global lockpick_history,prev_pressure
    policy = []
    banks = api.banks()
    it=0
    
    interceptors = [
        b for b in api.get_my_bots()
        if Ability.SPEED_BOOST in b.abilities and Ability.SELF_DESTRUCT in b.abilities
    ]
    
    lockpicks_this_tick = sum(
        1 for b in banks
        if b.is_bank_owner and b.lockpick_occuring
    )

    lockpick_history.append(lockpicks_this_tick)
    if len(lockpick_history) > LOCKPICK_WINDOW:
        lockpick_history.pop(0)

    pressure = sum(lockpick_history)
    pressure_increased = pressure > prev_pressure
    prev_pressure = pressure
    
    if pressure_increased and pressure >= LOCKPICK_THRESHOLD:
        needed = min(2, pressure - len(interceptors))
        for _ in range(max(0, needed)):
            if api.can_spawn(Interceptor.ABILITIES):
                policy.append(
                    Interceptor.spawn(location=it)
                )
                it += 1
    
    return policy