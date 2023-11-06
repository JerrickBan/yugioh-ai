import random
import collections
from enum import Enum
import os
import random
import csv
import time

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
        else: who = 'OPPONENTS TURN'
        print(f"Opponent's Hand: {bot_hand}\n")
        for c in bot.board:
            if c.face == Face.Up:
                print(c, end="")
            else:
                print('?', end="")
        print("\n")
        print(f'{who} | {self.phase.val} Phase | Turn {self.turn_num}\n')
        for c in player.board:
            print(c, end="")
        print()
        print(f"Your Hand: ", end="")
        for card in player.hand:
            print(card, end="")
        print()








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
        self.level = level
        self.type = type
        self.attribute = attribute
        self.atk = atk
        self.defense = defense
        self.face = Face.Down
        self.pos = Pos.ATK
    
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
        return f"{self.name}({self.atk},{self.defense},{position}) "

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
        self.deck = deck
        self.hand = []
        self.board = []
        self.grave = GraveYard()
        self.MAXBOARDLEN = 3
        self.life = 4000

    def start(self):
        for _ in range(5):
            self.hand.append(self.deck.draw())

    ## ACTIONS ##

    def lose_lp(self,amnt):
        self.life -= amnt

    def draw(self):
        self.hand.append(self.deck.draw())

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
        phase.display(player, bot)
        time.sleep(3)
        
    # TODO
    def main_phase(self, phase: Phases, player, bot):
        phase.next_phase()
        os.system("clear")
        phase.display(player, bot)
        time.sleep(3)

    # TODO
    def battle_phase(self, phase: Phases, player, bot):
        phase.next_phase()
        os.system("clear")
        phase.display(player, bot)
        time.sleep(3)

    def end_phase(self, phase: Phases, player, bot):
        phase.next_phase()
        os.system("clear")
        if self.life <= 0:
            return 0
        
        phase.display(player, bot)
        time.sleep(3)
        phase.next_phase()
        return 1
    
        

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

    # TODO
    def main_phase(self, phase: Phases, player, bot):
        phase.next_phase()
        os.system("clear")

    # TODO
    def battle_phase(self, phase: Phases, player, bot):
        phase.next_phase()
        os.system("clear")
    

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
        while(1):
            lose = self.play_turn()
            if lose:
                if self.phase.turn == Turn.YOUR:
                    print("YOU LOSE!!")
                else:
                    print("YOU WIN!!")
            
            self.phase.switch_turn()


    def play_turn(self):
        # Player's Turn
        if self.phase.turn == Turn.YOUR:
            if self.phase.turn_num != 1:
                if not self.player.draw_phase(self.phase, self.player, self.bot):
                    return 1
            else:
                self.phase.display(self.player, self.bot)
                time.sleep(3)
            self.player.standby_phase(self.phase, self.player, self.bot)
            self.player.main_phase(self.phase, self.player, self.bot)
            self.player.battle_phase(self.phase, self.player, self.bot)
            if not self.player.end_phase(self.phase, self.player, self.bot):
                return 1

        # AI's Turn
        else:
            if self.phase.turn_num != 1:
                if not self.bot.draw_phase(self.phase, self.player, self.bot):
                    return 1
            else:
                self.phase.display(self.player, self.bot)
                time.sleep(3)
            self.bot.standby_phase(self.phase, self.player, self.bot)
            self.bot.main_phase(self.phase, self.player, self.bot)
            self.bot.battle_phase(self.phase, self.player, self.bot)
            if not self.bot.end_phase(self.phase, self.player, self.bot):
                return 1

    
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
