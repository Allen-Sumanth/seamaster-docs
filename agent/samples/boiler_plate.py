# import necessary modules and classes here
from oceanmaster.botbase import BotController

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
    return policy
