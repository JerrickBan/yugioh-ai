#!/usr/bin/python3
import csv
import random
import os
from classes import BoardState, Phase, MonsterCard, Deck, Actions, Turn, CardData, PlayGame


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
print("\tPlayers Draw 1 card during the Draw Phase except the first player on the first turn")
print("\tStanby Phase is for effects that specify this phase, but in this game it won't be used for simplicity")
print("\tThe Main Phase is where you do all your actions including summoning, activiating, setting cards")
print("\tThe Battle Phase is where you attack your opponents monsters with your own")
print("\tThe End Phase signals the end of your turn and effects that specific this phase will activate; again not used\n")
print("  3. Each player's board has 3 monster zones, a deck zone, and a graveyard zone\n")
print("  4. The deck goes in the deck zone, and cards that are destroyed are sent to the graveyard. Banished cards are cards that are removed from play\n")
print("  5. Each player starts with 4000 life points\n")
print("  6. To win the game, your opponent's life points must reach 0 must or they run out of cards in their deck\n")


s = input("Type 'n' to continue to Phase Rules: ")
while s != 'n':
    s = input("Type 'n' to continue to Main and Battle Phase Rules: ")

os.system("clear")
print("Main Phase Rules:")
print("  1. You can only normal summon a monster 1 time per turn\n")
print("  2. To normal summon level 5-6 monsters you must sacrifice 1 monster, and for 7+ you must sacrifice 2\n")
print("  3. Monsters can be in face-up attack position (horizontal) or face-up or face-down defense position (horizontal)\n")
print("  4. You can also choose to normal set a monster in face down defense defense position\n")
print("  5. You can change the battle position of each monster max 1 time per turn, except the turn it's summoned.\n    Defense --> Attack and Attack --> Face-Up Defense\n")


s = input("Type 'n' to continue: ")
while s != 'n':
    s = input("Type 'n' to continue: ")

os.system("clear")
print("Battle Phase Rules:")
print("  1. Each attack position monster can attack at most 1 time\n")
print("  2. If opponents have a monster you must attack that monster before attacking the opponent directly\n")
print("  3. If attacking an attack-position monster, the monster with lower attack is sent to graveyard. Both are sent if there's a tie.")
print("    a) The difference in attack is dealt as damage to the losing player's life points\n")
print("  4. If attacking a defense-position monster, that monster is destroyed if yours has higher attack than its defense.")
print("    a) If your monster has lower attack than opponent's defense, then you take difference as damage\n")
print("  5. If attacking a face-down defense monster, flip it to face-up defense and perform calculations\n")
print("  6. You can change the battle position of each monster max 1 time per turn. Defense positions must go to attack and attack must go to face-up defense\n")


s = input("Type 'n' to start: ")
while s != 'n':
    s = input("Type 'n' to start: ")



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
n = input("Type 'n' to continue: ")
while n != 'n':
    n = input("Type 'n' to continue: ")


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
    print("Actions:\nn: next card\np: previous card\na: add card\nr: remove current card\nc: clear history\nf: finished\nb: back\nd: display deck")
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
            deck.add_card(player_cards[index])
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
            print("Actions:\nn: next card\np: previous card\na: add card\nr: remove current card\nc: clear history\nf: finished\nb: back\nd: display deck")
        elif option == 'd':
            deck.print_deck()
        


print("Complete!")
# index = 0
# os.system("clear")
# print(f"Cards with Attribute {t}\nn: next\np: previous\na: add to deck\nr [name] to remove from deck\nr: ready")
# card_pool[card_names[index]].display()
# action = input("Action: ")
# while action != 'q':
#     card_pool[card_names[index]].display()

# print(f'Cards with Attribute {t}:')
# for i, name in enumerate(card_names):
#     print(f'{i}: {name}')



# b = BoardState()
# b.print_board(Phase.DRAW, 1, 4000,4000, Turn(0))