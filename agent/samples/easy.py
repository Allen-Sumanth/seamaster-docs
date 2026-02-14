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
    
    return policy
