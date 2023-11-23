import random
import collections
from enum import Enum
import os
import random
import csv
import time
import sys

PLAYER_WIN = 1
OPPONENT_WIN = 0
NO_RESULT = None

class Phase:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

class Face(Enum):
    Up = 1
    Down = 0

class Turn(Enum):
    YOUR = 1
    OPPONENTS = 0

class Pos(Enum):
    ATK = 1
    DEF = 0


class Phases:
    def __init__(self):
        draw = Phase('Draw')
        standby = Phase('Standby')
        main = Phase('Main')
        battle = Phase('Battle')
        end = Phase('End')
        draw.next = standby
        standby.next = main
        main.next = battle
        battle.next = end
        end.next = draw
        self.phase = draw
        self.turn_num = 1
        self.turn = Turn(random.choice([0,1]))

    def next_phase(self):
        self.phase = self.phase.next
        print(self.phase)

    def switch_turn(self):
        self.turn_num += 1
        if self.turn == Turn.YOUR:
            self.turn = Turn.OPPONENTS
        else:
            self.turn = Turn.YOUR

    def display(self, player, bot):
        bot_hand = ['?' for _ in bot.hand]
        if self.turn == Turn.YOUR: who = 'YOUR TURN' 
        else: who = "OPPONENT'S TURN"
        print(f"OPPONENT'S DECK SIZE: {bot.deck.deck_size()}\n")
        print(f"OPPONENT'S HAND:\n{bot_hand}\n")
        print(f"\n\nOPPONENT'S BOARD\n")
        for c in bot.board:
            if c.face == Face.Up:
                print(f'{c}   ', end="")
            else:
                print(f'?   ', end="")
        print("\n")
        print("------------------------------------------------------------------------")
        print(f'{who} | {self.phase.val} Phase | Turn {self.turn_num} | YOUR LIFE: {player.life} | OPPONENT LIFE: {bot.life}')
        print("------------------------------------------------------------------------")
        print("\n\nYOUR BOARD\n")
        for c in player.board:
            print(f'{c}   ', end="")
        print('\n')
        print(f"YOUR HAND: ")
        for card in player.hand:
            print(card)
        print()
        print(f"YOUR DECK SIZE: {player.deck.deck_size()}\n")
        print("------------------------------------------------------------------------")




#############################################################################################
#############################  IMPLEMENTED  #################################################
#############################################################################################

class CardData:
    def __init__(self):
        self.lines = []
        self.name_map = {}

    def get_data(self):
        with open("card_data.csv") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                self.lines.append(row)

        for n, t, l, r, a, atk, d in self.lines:
            self.name_map[n] = {"Type": t, "Level": l, "Race":r, "Attribute":a, "ATK": atk, "DEF":d}
    
    def filter(self, map, attr, value):
        return {name:val for name, val in map.items() if val[attr] == value}
    
    def dict_to_cards(self, card_dict):
        card_list = [n for n , _ in card_dict.items()]
        return [MonsterCard(card,  card_dict[card]['Level'],card_dict[card]['Race'], card_dict[card]['Attribute'], card_dict[card]['ATK'], card_dict[card]['DEF']) for card in card_list]

    def get_cards_of_attribute(self, info, attr):
        card_pool = self.filter(info, "Race", attr)
        return self.dict_to_cards(card_pool) * 3

class MonsterCard:
    def __init__(self, name, level, type, attribute, atk, defense):
        self.name = name
        self.level = int(level)
        self.type = type
        self.attribute = attribute
        self.atk = int(atk)
        self.defense = int(defense)
        self.face = Face.Down
        self.pos = Pos.ATK
        self.just_summoned = True
        self.current_pos_changes = 0
        self.attacks = 0
    
    def display(self):
        name_level = f'{self.name:7} (lv {self.level})'
        str_atk = f'ATK:{self.atk}'
        str_def = f'DEF:{self.defense}'
        maxlen = max(len(name_level), len(str_atk), len(str_def))
        border = '*' + '-' * maxlen + '*' 
        print(border)
        print(f'|{name_level}{" " * (maxlen - len(name_level))}|')
        print(f'|{str_atk}{" " * (maxlen - len(str_atk))}|')
        print(f'|{str_def}{" " * (maxlen - len(str_def))}|')
        print(border)

    def __str__(self):
        if self.pos == Pos.ATK: position = 'ATK'
        else: position = 'DEF'
        return f"{self.name} ({self.level}*,{self.atk}/{self.defense},POS:{position},Face:{self.face.name})"

class Deck:

    def __init__(self): # arr: list of card names, info: dictionary for other data about card
        self.cards = collections.deque([]) # stack where last card is top card
        self.card_count = collections.defaultdict(int)

    def init_deck(self, cards):
        for c in cards:
            self.cards.append(c)
                
    def valid_deck_len(self):
        return len(self.cards) >= 20 and len(self.cards) <= 30

    def add_card(self, card):
        if self.card_count[card.name] < 3:
            self.cards.append(card)
            self.card_count[card.name] += 1
        else:
            print("Only 3 copies per card allowed!")
    
    def remove_card(self, card):
        if self.card_count[card.name] > 0:
            self.cards.remove(card)
            self.card_count[card.name] -= 1
            if self.card_count[card.name] == 0:
                del self.card_count[card.name]
        else:
            print(f"{card.name} not in deck!")
    
    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def peek(self, num): # number of cards to look at from the top of the deck
        if num > len(self.cards): return []
        return [self.cards[i] for i in range(len(self.cards)-1,len(self.cards)-1-num, -1)]

    def put_on_top(self, card: MonsterCard):
        self.arr.append(card)
    
    def put_into_deck(self, card: MonsterCard):
        self.arr.append(card) 
        self.shuffle(self.arr)   

    def put_on_bottom(self, card: MonsterCard):
        self.arr.appendleft(card)

    def search(self, name):
        for i, card in enumerate(self.cards):
            if card.name == name:
                return self.cards.pop(i)
            
        return None

    def deck_size(self):
        return len(self.cards)
    
    def print_deck(self):
        print(f'{len(self.cards)} Cards')
        for name, cnt in self.card_count.items():
            print(f'\t{name}  x{cnt}')

class GraveYard:
    def __init__(self):
        self.cards = []
    
    def add(self, card: MonsterCard):
        self.cards.append(card)

    def display(self):
        print("Top")
        for item in self.cards[::-1]:
            print(item)
        print("Bottom")


# HUMAN PLAYER
class Player:
    def __init__(self, deck: Deck):
        self.MAXSUMMON = 1
        self.MAXPOSCHANGE = 1
        self.MAXBOARDLEN = 3
        self.MAXATTACK = 1
        self.deck = deck
        self.hand = []
        self.board = []
        self.grave = GraveYard()
        self.life = 4000
        self.current_summon = 0

    def start(self):
        self.deck.shuffle()
        for _ in range(5):
            self.hand.append(self.deck.draw())

    ## ACTIONS ##

    def lose_lp(self,amnt):
        self.life -= amnt

    def draw(self):
        self.hand.append(self.deck.draw())

    def choose_board_card(self):
        name = input("Enter name of card on board: ")
        for i, c in enumerate(self.board):
            if c.name == name:
                return i, c
        
        return 0, None
            

        
    def choose_hand_card(self):
        if self.current_summon == self.MAXSUMMON:
            print("Already normal summoned/set this turn!")
            time.sleep(2)
            return None, 0
        
        while(1):
            card_name = input("Enter Card Name to Summon (or b to go back): ")
            tribute_flag = False
            if card_name == 'b':
                return None, 0
            for i, card in enumerate(self.hand):
                if card.name == card_name:
                    tribute = 0
                    if card.level > 4 and card.level < 7:
                        tribute = 1
                    elif card.level >= 7:
                        tribute = 2
                    
                    if len(self.board) < tribute:
                        tribute_flag = True
                        break

                    self.current_summon += 1
                    return self.hand.pop(i), tribute
            if tribute_flag:
                print("Not enough monsters for tribute")
                tribute_flag = False
            else:
                print("Card not in Hand")

    def tribute_monsters(self, tribute, phase, player, bot):
        tributed_mons = set()

        while len(tributed_mons) < tribute:
            print("Tribute Monster")
            index, card = self.choose_board_card()

            while card is None:
                print("Card Not On Board")
                index, card = self.choose_board_card()

            tributed_mons.add(self.board.pop(index))

        for c in tributed_mons:
            self.grave.add(c)
    
    def normal(self, card, position, tribute, phase, player, bot): 
        if position == Pos.ATK:
            card.face = Face.Up
            card.pos = Pos.ATK
        else:
            card.face = Face.Down
            card.pos = Pos.DEF
        self.tribute_monsters(tribute, phase, player, bot)
        self.board.append(card)

    def damage_calc(self, attacking: MonsterCard, defending: MonsterCard):
        '''
        Returns 'A' # if attacking is destroyed and minus # from lp
        Returns 'D' # if defending is desetroyed and minus # from lp
        Returns 'Both' 0 if both are destroyed
        Returns None # if nothing is destroyed but damage is taken by attacker
        '''
        if attacking.pos == Pos.DEF:
            return None, -1
        if defending.pos == Pos.ATK:
            if attacking.atk > defending.atk:
                return 'D', attacking.atk - defending.atk
            elif attacking.atk < defending.atk:
                return 'A', defending.atk - attacking.atk
            else:
                return 'Both', 0

        elif defending.pos == Pos.DEF:
            if defending.face == Face.Down:
                defending.face = Face.Up

            if attacking.atk > defending.defense:
                return 'D', 0
            elif attacking.atk < defending.defense:
                return None, defending.defense - attacking.atk
            else: 
                return None, 0

    def destroy(self, card):
        self.board.remove(card)
        self.grave.add(card)


    ## PHASES ##

    def draw_phase(self, phase: Phases, player, bot):
        os.system("clear")
        if self.deck.deck_size() == 0:
            return 0
        self.draw()
        phase.display(player, bot)
        time.sleep(3)
        return 1

    def standby_phase(self, phase: Phases, player, bot):
        phase.next_phase()
        os.system("clear")
        self.current_summon = 0
        for card in self.board:
            card.just_summoned = False
            card.current_pos_changes = 0
            card.attacks = 0
        phase.display(player, bot)
        time.sleep(3)
        
    def main_phase(self, phase: Phases, player, bot):
        phase.next_phase()
        os.system("clear")
        phase.display(player, bot)
        
        while(1):
            print("\nActions: (1) Normal Summon (2) Normal Set (3) Change Position (4) Next Phase")
            action = input("Choice: ")

            if action == '1': # Normal Summon
                if len(self.board) >= self.MAXBOARDLEN:
                    print("Field is full!")
                    continue
                card, tribute = self.choose_hand_card()
                if card:
                    self.normal(card, Pos.ATK, tribute, phase, player, bot)

            elif action == '2': # Normal Set
                if len(self.board) >= self.MAXBOARDLEN:
                    print("Field is full!")
                    continue
                card, tribute = self.choose_hand_card()
                if card:
                    self.normal(card, Pos.DEF, tribute, phase, player, bot)

            elif action == '3': # Change Position
                if len(self.board) == 0:
                    print("No Monsters on Field")
                    time.sleep(2)
                    os.system("clear")
                    phase.display(player, bot)
                    continue

                _, card = self.choose_board_card()

                if not card:
                    print("Card is not board")
                    time.sleep(2)
                    os.system("clear")
                    phase.display(player, bot)
                    continue

                if card.just_summoned:
                    print("Can't change position for card in same turn when it's summoned")
                    time.sleep(2)
                    os.system("clear")
                    phase.display(player, bot)
                    continue
                
                if card.current_pos_changes == self.MAXPOSCHANGE:
                    print("Only can change position max 1 time per card in a turn")
                    time.sleep(2)
                    os.system("clear")
                    phase.display(player, bot)
                    continue
                
                if card.pos == Pos.ATK:
                    card.pos = Pos.DEF
                elif card.pos == Pos.DEF:
                    card.pos = Pos.ATK
                    card.face = Face.Up
                card.current_pos_changes += 1

            elif action == '4': # Next
                break

            os.system("clear")
            phase.display(player, bot)

    def battle_phase(self, phase: Phases, player, bot):
        phase.next_phase()
        os.system("clear")
        phase.display(player, bot)
        while(1):
            print("\nActions: (1) Attack (2) Next Phase")
            action = input("Choice: ")

            if action == '1': # Attack
                print("Choose Attacking Monster")
                i, c = self.choose_board_card()

                ### END GAME EARLY WHEN YOU OR OPPONENT REACHES 0 LP

                if not c:
                    print("Card is not board")
                    time.sleep(2)
                    os.system("clear")
                    phase.display(player, bot)
                    continue

                if c.pos == Pos.DEF:
                    print("Card has to be in ATK position")
                    time.sleep(2)
                    os.system("clear")
                    phase.display(player, bot)
                    continue

                if c.attacks > 0:
                    print("Card already attacked")
                    time.sleep(2)
                    os.system("clear")
                    phase.display(player, bot)
                    continue

                # Choose opponents Monster
                if (len(bot.board) > 0):
                    print("Choose the 1st, 2nd, or 3rd (from the left) Monster to attack")
                    index = int(input("Number[1/2/3]: "))
                    while index > len(bot.board):
                        print("Opponent doesn't have that many cards")
                        index = int(input("Number[1/2/3]: "))
                    
                    i = index - 1
                    target = bot.board[i]
                    destroyed, dmg = self.damage_calc(c, target)

                    # error check (def pos monsters can't attack)
                    if dmg == -1:
                        print("Monster has to be in attack position to attack")
                        time.sleep(2)
                        os.system("clear")
                        phase.display(player, bot)
                        continue

                    c.attacks += 1

                    if destroyed == 'A':
                        player.destroy(c)
                        player.life -= dmg
                        print(f"{c.name} was Destroyed!\nYou took {dmg} Damage")
                    elif destroyed == 'D':
                        bot.destroy(target)
                        bot.life -= dmg
                        print(f"{target.name} was Destroyed!\nOpponent took {dmg} Damage")
                    elif destroyed == 'Both':
                        player.destroy(c)
                        bot.destroy(target)
                        print(f"Both {c.name} and {target.name} were Destroyed")
                    elif not destroyed:
                        player.life -= dmg
                        print(f"Player took {dmg} Damage")
                    
                    time.sleep(2)
                    os.system("clear")
                    phase.display(player, bot)

                # DIRECT ATTACK
                else:
                    bot.life -= c.atk
                    c.attacks += 1
                    print(f"Opponent took {c.atk} Damage")
                    time.sleep(2)
                    os.system("clear")
                    phase.display(player, bot)

            if self.life <= 0:
                return OPPONENT_WIN
            if bot.life <= 0:
                return PLAYER_WIN


            elif action == '2': # Next Phase
                break


    def end_phase(self, phase: Phases, player, bot):
        phase.next_phase()
        os.system("clear")
        # if self.life <= 0:
        #     return OPPONENT_WIN
        # if bot.life <= 0:
            # return PLAYER_WIN
        phase.display(player, bot)
        time.sleep(3)
        phase.next_phase()
        return NO_RESULT
    
        

# AI PROGRAM!!!!
'''
Algorithm:
    My idea for the robot is to implement a Greedy algorithm, where the ai tries to summon it's largest monster to either protect
    itself or destroy the player every turn. 

    Examples:
    If player has monsters that are all greater than bot's hand monsters, bot will normal set it's monster with highest def
    If player has monsters that are all less than a card in bot's hand monsters, bot will summon greatest of them
'''
class Bot(Player):
    def __init__(self, deck: Deck):
        super().__init__(deck)

    def is_summonable(self, card: MonsterCard) -> bool:
        if card.level <= 4 and len(self.board) < self.MAXBOARDLEN: return True
        if card.level > 4 and card.level <=6 and len(self.board) >= 1: return True
        if card.level > 6 and len(self.board) >= 2: return True
        return False
    
    def num_tributes(self, card: MonsterCard) -> int:
        if card.level > 4 and card.level <=6: return 1
        if card.level > 6: return 2
        else: return 0

    def num_tribute_mons_hand(self):
        cnt = 0
        for card in self.hand:
            if card.level > 4:
                cnt+=1
        return cnt

    def num_non_tribute_mons_hand(self):
        cnt = 0
        for card in self.hand:
            if card.level <= 4:
                cnt+=1
        return cnt

    def four_lower_hand(self):
        return len([c for c in self.hand if c.level <= 4]) > 0
    
    def five_above_hand(self):
        return len([c for c in self.hand if (c.level > 4 and self.is_summonable(c))]) > 0

    def greater_atk(self, botcard: MonsterCard, playercard: MonsterCard):
        return True if botcard.atk > playercard.atk else False
    
    def greater_def(self, botcard: MonsterCard, playercard: MonsterCard):
        return True if botcard.defense > playercard.defense else False

    def bot_board_card_with_smallest_atk(self):
        if len(self.board) == 0:
            return None
        smallest = self.board[0]
        for c in self.board:
            if c.atk < smallest.atk:
                smallest = c
        return smallest
    
    def bot_board_card_with_smallest_def(self):
        if len(self.board) == 0:
            return None
        smallest = self.board[0]
        for c in self.board:
            if c.defense < smallest.defense:
                smallest = c
        return smallest

    def bot_board_card_with_largest_atk(self):
        if len(self.board) == 0:
            return None
        largest = self.board[0]
        for c in self.board:
            if c.atk > largest.atk:
                largest = c
        return largest

    def bot_board_card_with_largest_def(self):
        if len(self.board) == 0:
            return None
        largest = self.board[0]
        for c in self.board:
            if c.defense > largest.defense:
                largest = c
        return largest

    def bot_hand_4_lower_with_largest_atk(self):
        h = [c for c in self.hand if c.level <= 4]
        largest = h[0]
        for c in h:
            if c.atk > largest.atk:
                largest = c
        return largest
    
    def bot_hand_4_lower_with_largest_def(self):
        h = [c for c in self.hand if c.level <= 4]
        largest = h[0]
        for c in h:
            if c.defense > largest.defense:
                largest = c
        return largest
    
    def bot_hand_4_lower_with_smallest_def(self):
        h = [c for c in self.hand if c.level <= 4]
        smallest = h[0]
        for c in h:
            if c.defense < smallest.defense:
                smallest = c
        return smallest
    
    def bot_hand_summonable_tribute_with_largest_atk(self):
        summonable_tributes = [c for c in self.hand if c.level > 4 and self.is_summonable(c)]
        max_atk = 0
        card = None
        for c in summonable_tributes:
            if c.atk > max_atk:
                card = c
                max_atk=c.atk
        return card

    def bot_hand_card_with_largest_atk(self):
        if len(self.hand) == 0:
            return None
        largest = self.hand[0]
        for c in self.hand:
            if c.atk > largest.atk:
                largest = c
        return largest

    def bot_hand_card_with_largest_def(self):
        if len(self.hand) == 0:
            return None
        largest = self.hand[0]
        for c in self.hand:
            if c.defense > largest.defense:
                largest = c
        return largest

    def change_to_def(self, botcard: MonsterCard):
        botcard.pos = Pos.DEF

    def change_to_atk(self, botcard: MonsterCard):
        botcard.pos = Pos.ATK

    def strongest_player_card_value(self, player: Player) -> [int, MonsterCard]:
        if len(player.board) == 0:
            return 0, None
        largest = 0
        card = None

        for c in player.board:
            if c.face == Face.Down:
                continue
            if c.pos == Pos.ATK and c.atk > largest: 
                largest = c.atk
                card = c
            elif c.pos == Pos.DEF and c.defense > largest:
                largest = c.defense
                card = c
        return largest, card

    def num_player_mons(self, player: Player):
        return len(player.board)

    def normal_summon(self, card):
        tribute = self.num_tributes(card)
        self.hand.remove(card)
        if tribute == 0:
            card.pos = Pos.ATK
            card.face = Face.Up
            self.board.append(card)
        else:
            tribute_selections = self.find_n_weakes_monsters_atk_board(tribute)
            for c in tribute_selections:
                self.board.remove(c)
                self.grave.add(c)
            self.board.append(card)

    def normal_set(self, card):
        tribute = self.num_tributes(card)
        self.hand.remove(card)
        if tribute == 0:
            card.pos = Pos.DEF
            card.face = Face.Down
            self.board.append(card)
        else:
            tributed_list = set()
            for _ in range(tribute):
                c = self.bot_board_card_with_smallest_def()
                self.board.remove(c)
                tributed_list.add(c)
            for t in tributed_list:
                self.grave.add(t)
            self.board.append(card)

    def change_all_defense(self, exceptions=set()):
        for c in self.board:
            if c not in exceptions and c.pos == Pos.ATK and not c.just_summoned:
                c.pos = Pos.DEF

    def change_all_attack(self, exceptions=set()):
        for c in self.board:
            if c not in exceptions and c.pos == Pos.DEF and not c.just_summoned:
                c.pos = Pos.ATK
                c.face = Face.Up

    def total_atk_on_board(self):
        atk = 0
        for c in self.board:
            atk+=c.atk
        return atk

    def find_n_weakes_monsters_atk_board(self, n):
        board_sorted = sorted(self.board, key=lambda x: x.atk)
        if n > len(board_sorted):
            return []
        return board_sorted[:n+1]

    def total_attack_increase(self, monster):
        tributes = self.num_tributes(monster)
        tribute_candidates = self.find_n_weakes_monsters_atk_board(tributes)
        total_curr_atk = self.total_atk_on_board()
        atk_minus = sum([c.atk for c in tribute_candidates])
        atk_plus = monster.atk
        new_atk = total_curr_atk - atk_minus + atk_plus
        return new_atk > total_curr_atk

    def tribute_set(self, monster):
        pass

    def summonable_mons(self):
        return [c for c in self.hand if self.is_summonable(c)]

    def summonable_monster_with_greater_atk(self, target):
        mons = self.summonable_mons()
        for c in mons:
            if c.atk > target:
                return c
        return None
    
    def summonable_monster_with_greater_def(self, target):
        mons = self.summonable_mons()
        for c in mons:
            if c.defense > target:
                return c
        return None


    # TODO
    def main_phase(self, phase:Phases, player:Player, bot:Player):
        '''
        GOALS:
        - Wipe out player's strongest cards
        - More cards on field better than less but stronger cards on field
        - Play defensively and Protect Life Points
        '''
        phase.next_phase()
        os.system("clear")

        # get player's strongest card
        target, player_strongest = self.strongest_player_card_value(player)
        
        # if player's board has no monsters:
        if len(player.board) == 0:
            # if bot's board not full and bot has a 4* or lower monster 
            if len(self.board) <= self.MAXBOARDLEN and self.four_lower_hand():
                # summon highest attack one
                highest_atk_bot_hand = self.bot_hand_4_lower_with_largest_atk()
                self.normal_summon(highest_atk_bot_hand)
            # else if you have 5* + summonable monster
            elif self.five_above_hand():
                # if the total atk after the strongest one is summoned > total atk before
                strongest_tributed_mon = self.bot_hand_summonable_tribute_with_largest_atk()
                if self.total_attack_increase(strongest_tributed_mon):
                    #summon it by tributing weakest monsters
                    self.normal_summon(strongest_tributed_mon)
            # change all monsters to attack position
            self.change_all_attack()
            # start battle phase
            phase.display(player, bot)
            time.sleep(3)
            return

        # bot strongest atk card on field
        bot_strong_atk =self.bot_board_card_with_largest_atk()

        # if bot board has a higher atk monster on the board:
        if bot_strong_atk and (bot_strong_atk.atk > target):
            # if player board <= 1 monster:
            if len(player.board) <= 1:
                # if board isn't full and you have a 4* or lower in hand:
                if len(self.board) < self.MAXBOARDLEN and self.four_lower_hand():
                    # normal summon a 4* or lower monster with highest atk
                    four_lower_highest_atk = self.bot_hand_4_lower_with_largest_atk()
                    self.normal_summon(four_lower_highest_atk)
                # all to attack position
                self.change_all_attack()
            # else:
            else:
                # if board isn't full and you have a 4* or lower in hand:
                if len(self.board) < self.MAXBOARDLEN and self.four_lower_hand():
                    # normal set a 4* or lower monster with highest def
                    four_lower_highest_def = self.bot_hand_4_lower_with_largest_def()
                    self.normal_set(four_lower_highest_def)
                # change all to def position besides strongest monster
                self.change_all_defense(exceptions={bot_strong_atk})
            # battle phase
            phase.display(player, bot)
            time.sleep(3)
            return

        # if bot board doesn't have a higher atk monster on the board:
        else:
            # filter for summonable monsters in hand (check if board is full too)
            mons = self.summonable_mons()
            # if there is summonable monster with more atk in hand
            stronger_mon = self.summonable_monster_with_greater_atk(target)
            if stronger_mon:
                # normal summon it
                self.normal_summon(stronger_mon)
                # if player board <= 1 monster:
                if len(player.board) <= 1:
                    # change all to atk
                    self.change_all_attack()
                # else
                else:
                    # change rest to def
                    self.change_all_defense(exceptions={stronger_mon})
                # battle
                phase.display(player, bot)
                time.sleep(3)
                return
            # else
            else:
                # if there is monster with more def in hand
                tougher_mon = self.summonable_monster_with_greater_def(target)
                if tougher_mon:
                    # normal set it
                    self.normal_set(tougher_mon)
                # else if there is a 4* or lower in hand
                elif self.four_lower_hand() and len(self.board) < self.MAXBOARDLEN:
                    # normal set the one with lowest def (body block)
                    weakest_def_mon = self.bot_hand_4_lower_with_smallest_def()
                    self.normal_set(weakest_def_mon)
                # change all to def
                self.change_all_defense()
                # end turn
                phase.display(player, bot)
                time.sleep(3)

    # TODO
    def battle_phase(self, phase: Phases, player, bot):
        '''
        1. Sort all attack position monsters by atk value
        2. Sort the monsters on opponent field by attack/defense
        3. Attack using the strongest monster on the strongest opposing monster, and so on
        '''
        phase.next_phase()
        os.system("clear")
        phase.display(player, bot)
        time.sleep(3)
    

# Records Game state and Runs Game
class Game:
    def __init__(self, player: Player, bot: Bot):
        self.player = player
        self.bot = bot
        self.phase = Phases()

    def start(self):
        self.player.start()
        self.bot.start()

    def play(self):
        self.phase.turn = Turn.OPPONENTS
        os.system("clear")
        while(1):
            res = self.play_turn()
            if res == OPPONENT_WIN:
                os.system("clear")
                print("YOU LOSE!!")
                break
            elif res == PLAYER_WIN:
                os.system("clear")
                print("YOU WIN!!")
                break

            self.phase.switch_turn()


    def play_turn(self):
        done = None

        #################
        # Player's Turn #
        #################
        if self.phase.turn == Turn.YOUR:
            # Draw
            if self.phase.turn_num != 1:
                if not self.player.draw_phase(self.phase, self.player, self.bot):
                    return 1
            else:
                self.phase.display(self.player, self.bot)
                time.sleep(3)
            # Standby
            self.player.standby_phase(self.phase, self.player, self.bot)
            # Main
            self.player.main_phase(self.phase, self.player, self.bot)
            # Battle
            if self.phase.turn_num != 1:
                done = self.player.battle_phase(self.phase, self.player, self.bot)
            else:
                self.phase.next_phase()
            if done != None:
                return done
            # End
            self.player.end_phase(self.phase, self.player, self.bot)
    
        #############
        # AI's Turn #
        #############
        else:
            # Draw
            if self.phase.turn_num != 1:
                if not self.bot.draw_phase(self.phase, self.player, self.bot):
                    return 1
            else:
                self.phase.display(self.player, self.bot)
                time.sleep(3)
            # Standby
            self.bot.standby_phase(self.phase, self.player, self.bot)
            # Main
            self.bot.main_phase(self.phase, self.player, self.bot)
            # Battle
            if self.phase.turn_num != 1:
                done = self.bot.battle_phase(self.phase, self.player, self.bot)
            else:
                self.phase.next_phase()
            if done != None:
                return done
            # End
            self.bot.end_phase(self.phase, self.player, self.bot) 




######################################################
############## DIRTY CODE ############################
######################################################



# class Actions:
#     def __init__(self):
#         self.num_norm_sum = 0
#         self.norm_sum_limit = 1

#     def normal_summon():
#         pass

#     def normal_set():
#         pass

#     def tribute_summon():
#         pass

#     def tribute_set():
#         pass

#     def activate_spell():
#         pass

#     def set_spell_trap():
#         pass

#     def check_player_grave():
#         pass

#     def check_opponent_grave():
#         pass


# class BoardState:
#     def __init__(self):
#         self.om = [None,None,None,None,None] # monster zones
#         self.ost = [None,None,None,None,None] # spell/trap zones
#         self.oh = set() # Opponent hand
#         self.og = set() # graveyard
#         self.ob = set() # banished
#         self.of = None # field spell
#         self.pm = [None,None,None,None,None]
#         self.pst = [None,None,None,None,None]
#         self.ph = set()
#         self.pg = set()
#         self.pb = set()
#         self.pf = None

    # def print_board_simple(self,)

    # def print_board(self, phase, turn, plp, olp, player):
    #     os.system('clear')
    #     print(f"\n{' ':25}{len(self.oh)} cards in OPPONENT's hand\n")
    #     divider = '|----------|----------|----------|----------|----------|----------|----------|\n'
    #     empty = "|          "
    #     grave = '|   grave  '
    #     deck = '|   deck   '
    #     field = '|   field  '
    #     banish = '|  banish  '

    #     ## OPPONENT SIDE
    #     print(divider)
    #     print(deck, end='')
    #     for card in self.ost:
    #         if card:
    #             print(f"|{card.name:10}", end="")
    #         else:
    #             print(empty, end="")
    #     print(banish,end="")
    #     print('|\n')
    #     print(divider)
    #     print(grave, end='')
    #     for card in self.om:
    #         if card:
    #             print(f"|{card:5}", end="")
    #         else:
    #             print(empty, end="")
    #     print(field, end="")
    #     print('|\n')
    #     print(divider)

    #     print(f"\n{' ':50}OPPONENT'S Life Points: {olp}\n")
    #     print(f'\n{" ":20}{player.name} {phase.name} PHASE {" ":13} Turn: {turn}{" ":13}\n')

    #     print(f"\nYOUR Life Points: {plp}\n")
    #     ## PLAYER SIDE
    #     print(divider)
    #     print(field, end="")
    #     for card in self.pst:
    #         if card:
    #             print(f"|{card:5}", end="")
    #         else:
    #             print(empty, end="")
    #     print(grave, end='')
    #     print('|\n')
    #     print(divider)
    #     print(banish, end="")
    #     for card in self.pm:
    #         if card:
    #             print(f"|{card:5}", end="")
    #         else:
    #             print(empty, end="")
    #     print(deck, end='')
    #     print('|\n')
    #     print(divider)

    #     print(f'\n{" ":10}YOUR hand: {",".join(self.ph)}\n')
        


# class PlayGame:
#     def __init__(self, player_deck: Deck, opponent_deck: Deck):
#         self.pdeck = player_deck
#         self.odeck = opponent_deck
#         self.lp = 4000 #life points
#         self.olp = 4000
#         self.turn = 1
#         self.active = Turn.YOUR
#         self.phase = Phase.DRAW
#         self.b = BoardState()

#         def start_game(self):
#             self.active = Turn(random.choice([0,1])) # select starting player

    
    # def play_turn(self,turn):
    #     if turn == Turn.YOUR:   
    #         self.player.draw_phase()
    #         self.player.standby_phase()
    #         self.player.main_phase()
    #         self.player.standby_phase()
    #         self.turn += 1
    #         return self.player.end_phase(), 'P'

    #     elif turn == Turn.OPPONENTS:
    #         self.bot.draw_phase()
    #         self.bot.standby_phase()
    #         self.bot.main_phase()
    #         self.bot.standby_phase()
    #         self.turn += 1
    #         return self.bot.end_phase(), 'B'
