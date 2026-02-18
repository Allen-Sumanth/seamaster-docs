from seamaster import GameAPI
from seamaster.botbase import BotController
from seamaster.constants import Ability, ABILITY_COSTS, SCRAP_COSTS, Direction
from seamaster.models import EnergyPad, Bank
from seamaster.translate import move, harvest, deposit
from seamaster import utils
import random

class harvester_bot(BotController):
    ABILITIES = [Ability.HARVEST]
    ability_scrap_cost = SCRAP_COSTS[Ability.HARVEST]
    ability_energy_cost = ABILITY_COSTS[Ability.HARVEST] # {traversal cost, energy cost}

    def _init_(self, ctx):
        super()._init_(ctx)

    def act(self):
        # If energy is below 50%, head to recharge ports
        current_energy = self.ctx.get_energy()
        if current_energy < 25: # magic number, needs to be nuked
            nearest_energy_pad : EnergyPad = self.ctx.get_nearest_energy_pad()
            move_priorities = utils.get_optimal_next_hops(self.ctx.get_location(), nearest_energy_pad.location)
            if move_priorities:
                return move(move_priorities[0])
        # If I'm carrying algae, deposit it before collecting more
        if self.ctx.get_algae_held() > 0:
            banks: list[Bank] = {
                bank for bank in self.ctx.api.banks() 
                    if bank.is_bank_owner == True
            }
            if banks:
                nearest_bank: Bank = min(banks, key=lambda bank: utils.manhattan_distance(self.ctx.get_location(), bank.location))
                dist_to_bank = utils.get_shortest_distance_between_points(self.ctx.get_location(), nearest_bank.location)
                print(f"Bot: {self.ctx.get_location()} is carrying algae, heading to bank at {nearest_bank.location} which is {dist_to_bank} away.")
                if not dist_to_bank or dist_to_bank < 2:
                    return deposit(utils.direction_from_point(self.ctx.get_location(), nearest_bank.location))
                else:   
                    move_priorities = utils.get_optimal_next_hops(self.ctx.get_location(), nearest_bank.location)
                    if move_priorities:
                        return move(move_priorities[0])
        # Otherwise, move to the nearest algae and harvest it
        nearest_algae = self.ctx.get_nearest_algae()
        dist_to_algae = utils.manhattan_distance(self.ctx.get_location(), nearest_algae.location)
        
        if dist_to_algae >= 2:
            alg_move_priorities = utils.get_optimal_next_hops(self.ctx.get_location(), nearest_algae.location)
            if alg_move_priorities:
                return move(alg_move_priorities[0])
        elif dist_to_algae < 2 and dist_to_algae > 0:
            return harvest(utils.direction_from_point(self.ctx.get_location(), nearest_algae.location))
        else: 
            return harvest(None)

def spawn_policy(gameAPI: GameAPI):
    # Spawn a harvester in every tick
    # if my energy goes below 50%, I'll head to recharge ports
    # for every algae that I'll collect, I'll deposit before collectin more
    spawn_rules = [] # list of dicts, each dict has keys "strategy", "abilities", "location", "args" corresponding to a specific bot spawn.

    # spawn a harvester every tick
    spawn_x = random.randint(0, gameAPI.view.width-1)
    spawn_rules.append(harvester_bot.spawn(spawn_x))
    return spawn_rules
