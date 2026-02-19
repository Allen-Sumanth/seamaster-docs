# Game Entities

Beyond walls and empty space, the grid contains several interactive entities.

## Algae (Resources)
Algae is the primary resource in Seawars. It spawns randomly at the start of the match and does not regrow.

*   **Abundance**: Roughly 15% of the board tiles contain algae (~60 total).
*   **Visibility**: You know the **location** of every algae tile on the board from the start (`PlayerView.visible_entities.algae`).
*   **Poison Status**: Roughly 5% of algae is **Poisonous**. This status is **Hidden** ("UNKNOWN") until scouted.
*   **Normal Algae**: Can be harvested for resource points.
*   **Poisonous Algae**: **Kills** any bot that attempts to harvest it.

!!! warning
    Scout before you harvest! While you can see where the algae is, indiscriminately harvesting "UNKNOWN" algae is a risk.

??? example "Checking Algae Safety"
    ```python linenums="1"
    from seamaster.constants import AlgaeType

    def act(self):
        # Access list of all algae
        all_algae = self.ctx.api.visible_algae()
        
        for algae in all_algae:
            if algae.is_poison == AlgaeType.FALSE:
                 print(f"Safe algae at {algae.location}!")
    ```

## Banks
Banks are locations where collected algae must be deposited to score points.

*   **Functionality**: Bots with the harvest ability can deposit algae they are carrying into a bank.
*   **Deposit Range**: A bot must be within **2 units** of a bank to deposit.
*   **Deposit Time**: Depositing takes **50 ticks**, during which the bank is susceptible to being lockpicked by a bot with the lockpick ability.

!!! note
    A bot with the lockpick ability can steal the algae which is being deposited into the bank by the enemy player. This action takes 10 ticks (continuously, if the lockpick is interrupted in the middle, it needs to start again for 10 ticks).

*   **Ownership**: There are two banks in each player's half of the map. The two banks closest to you are owned by you, and the two banks closest to your opponent are owned by the opponent. You can **only deposit algae in a bank you own**. Conversely, you can **only lockpick an opponent's bank**.
*   **Coordinates**: You can find the exact list of bank coordinates in your `PlayerView` object under `permanent_entities.banks`.
*   **Reference**: See [Player View & Perception](../mechanics/perception.md) for data structure details.

## Energy Pads
Energy pads are special locations that refill a bot's energy.

*   **Functionality**: When a bot stands on an energy pad, its energy is restored to the spawn energy level.
*   **Cooldown**: After use, an energy pad goes on cooldown for **25 ticks** and cannot be used again until the cooldown expires.
*   **Coordinates**: You can find the exact list of energy pad coordinates in your `PlayerView` object under `permanent_entities.energypads`.
*   **Reference**: See [Player View & Perception](../mechanics/perception.md) for data structure details.

??? example "Checking Energy Pad Availability"
    ```python linenums="1"
    def act(self):
        pads = self.ctx.get_energy_pads()
        
        for pad in pads:
            if pad.available:
                print(f"Pad at {pad.location} is ready!")
            else:
                print(f"Pad at {pad.location} ready in {pad.ticks_left} ticks.")
    ```

## Scraps (Currency)
Scraps are the currency used to **construct** new bots. You pay for the bot's chassis and its equipped abilities.

*   **Global Pool**: All scraps belong to you (the player), not individual bots.
*   **Starting Scraps**: 100 per player.
*   **Passive Income**: +1 scrap per tick.
*   **Salvage**: When a bot dies, it drops **50% of its total cost** on the tile where it fell.

!!! note
    Bots with the **Harvest** ability can collect these dropped scraps by moving onto the tile. Collected scraps are immediately added to your global pool.
