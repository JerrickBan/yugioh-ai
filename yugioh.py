#!/usr/bin/python3
import csv
import random
import os
from classes import Deck, CardData, Player, Bot, Game
import copy


################################################################################
#################### GLOBAL VARIABLES ##########################################
################################################################################

types = {
    "Aqua",
    "Beast",
    "Beast-Warrior",
    "Cyberse",
    "Dinosaur",
    "Divine-Beast",
    "Dragon",
    "Fairy",
    "Fiend",
    "Fish",
    "Insect",
    "Machine",
    "Plant",
    "Psychic",
    "Pyro",
    "Reptile",
    "Rock",
    "Sea Serpent",
    "Spellcaster",
    "Thunder",
    "Warrior",
    "Winged Beast",
    "Wyrm",
    "Zombie"
}
type_str = "\n".join(sorted(list(types)))



################################################################################
#################### LOAD CSV DATASET ##########################################
################################################################################
c = CardData()
c.get_data()
info = c.filter(c.name_map,"Type", "Normal Monster" )

os.system("clear")
print("Welcome to the YU-GI-OH! terminal trading card game!")
s = input("Type 's' to start: ")
while s != 's':
    s = input("Type 's' to start: ")


################################################################################
#################### INSTRUCTIONS ##############################################
################################################################################
os.system("clear")
print("Rules:")
print("  1. Players start with 5 cards in their hand\n")
print("  2. There are 5 Phases of play: Draw, Standby, Main, Battle, and End")
print("\tDraw: Draw 1 card except on turn #1")
print("\tStanby Phase: Ignore it for simplicity")
print("\tMain Phase: Do all your actions (more info next page)")
print("\tBattle Phase: Attack your opponent or their monsters. Can't attack on turn #1.")
print("\tEnd Phase: Ignore it for simplicity\n")
print("  3. Each player's board has 3 monster zones\n")
print("  4. Hand sizes for simplicity sake is unlimited\n")
print("  5. Each player starts with 4000 life points\n")
print("  6. To win the game, your opponent's life points must reach 0 must or they run out of cards in their deck\n")


s = input("Type 'n' to continue to Main Phase Rules: ")
while s != 'n':
    s = input("Type 'n' to continue to Main Phase Rules: ")

os.system("clear")
print("Main Phase Rules:\n")
print("Actions:")
print("  1. Normal summon: Place card in face-up attack position (verticle)")
print("  \t1.5. Level 5-6 monsters need 1 monster sacrfice to summon; Level 7+ needs 2\n")
print("  2. Normal set in face-down defense position (horizontal)\n")
print("  3. Switch positions: Change monster battle position\n    Defense --> Face-Up Attack and Attack --> Face-Up Defense\n")
print("Rules:")
print("  1. Can only normal summon/set 1 monster per turn")
print("  2. Cannot change monster's position the turn it's summoned")
print("  3. Each monster can only change position max 1 time per turn\n")

s = input("Type 'n' to continue to Battle Phase Rules: ")
while s != 'n':
    s = input("Type 'n' to continue to Battle Phase Rules: ")

os.system("clear")
print("Battle Phase Rules:")
print("  1. Each ATK-position monster can attack at most 1 time\n")
print("  2. Can attack opponent directly if they don't have monsters")
print("    - Opponent loses Life Points = monster's attack\n")
print("  3. If attacking an ATK-position monster: lower attack is sent to graveyard (both if tie)")
print("    - Losing player takes difference in atk as damage\n")
print("  4. If attacking a DEF-position monster: compare your attack with their defense")
print("    - If your attack = their defense: nothing happens")
print("    - If your attack > their defense: their monster is destroyed. No one takes damage.")
print("    - If your attack < their defense: no one is destroyed. You take damage from the difference.\n")


s = input("Type 'n' to enter Deck Building: ")
while s != 'n':
    s = input("Type 'n' to enter Deck Building: ")



################################################################################
#################### SELECT DECK ###############################################
################################################################################

# Selecting the AI Deck
ai_attribute = random.choice(list(types))
ai_cards = c.get_cards_of_attribute(info, ai_attribute)
while(len(ai_cards) < 20):
    ai_attribute = random.choice(list(types))
    ai_cards = c.get_cards_of_attribute(info, ai_attribute)

ai_deck = Deck()
ai_deck.init_deck(random.sample(ai_cards * 3, 20))
ai_deck.cards[0].display()

os.system("clear")
print("You will now enter Deck Building.\nDecks must be 20-30 cards\nMax 3 duplicates per card")
print("Type:\n\tn -> create your own deck\n\tl -> load deck from file")
n = input("choice: ")
while n != 'n' and n !='l':
    n = input("choice: ")

# CREATE YOUR OWN DECK
if n == 'n':

    # Selecting the User Deck type
    done = False
    while(not done):
        os.system("clear")
        print('Select a Monster Attribute to build your deck around.')
        print(f'All Monster Attributes:\n{type_str}')
        t = input(f'Type for your deck: ')
        while (t not in types or len(c.get_cards_of_attribute(info, t)) < 20):
            t = input(f'Type for your deck: ')
            if len(c.get_cards_of_attribute(info, t)) < 20:
                print(f"\tNot enough cards of type {t} to make a deck!")
                continue

        card_pool = c.filter(info, "Race", t)
        player_cards = c.dict_to_cards(card_pool)

        # Card Selection Menu
        index = 0
        deck = Deck()
        os.system('clear')
        print("Actions:\nn: next card\np: previous card\na: add card\nr: remove current card\nd: display deck\nc: clear history\nb: back\nf: finished\ns: save deck")
        while(True):
            player_cards[index].display()

            #print deck
            option = input("Select Option: ")

            if option == 'b':
                break

            if option == 'f':
                if (deck.valid_deck_len()):
                    done = True
                    break
                else:
                    print("Deck must be 20-30 cards!")
            if option == 'q':
                break
            elif option == 'a':
                deck.add_card(copy.deepcopy(player_cards[index]))
            elif option == 'r':
                deck.remove_card(player_cards[index])
            elif option == 'n':
                if index < len(player_cards) - 1:
                    index+=1
                else: print("At end of cards")
            elif option == 'p':
                if index > 0:
                    index-=1
                else: print("At beginning of cards")
            elif option == 'c':
                os.system('clear')
                print("Actions:\nn: next card\np: previous card\na: add card\nr: remove current card\nd: display deck\nc: clear history\nb: back\nf: finished\ns: save deck")
            elif option == 'd':
                deck.print_deck()
            elif option == 's':
                name = input("Filename: ")
                deck.save_deck(name)

    os.system('clear')
    print("Deck:")
    deck.print_deck()


# LOAD EXISTING DECK
elif n == 'l':
    deck = Deck()
    name = input("Filename: ")
    if not os.path.exists(name):
        print("No such filename")
        raise FileNotFoundError
    deck = c.load_deck(name)
    print("Deck Loaded:")
    deck.print_deck()

################################################################################
#################### START GAME ################################################
################################################################################

player = Player(deck)
bot = Bot(ai_deck)

g = Game(player,bot)
g.countdown(5)
g.start()
g.play()