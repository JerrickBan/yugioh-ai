import random
import collections
from enum import Enum
import os
import random
import csv

class Phase(Enum):
    DRAW = 1
    STANBY = 2
    MAIN = 3
    BATTLE = 4
    END = 5

class Face(Enum):
    Up = 1
    Down = 0

class Turn(Enum):
    YOUR = 1
    OPPONENTS = 0


class MonsterCard:
    def __init__(self, name, level, type, attribute, atk, defense):
        self.name = name
        self.level = level
        self.type = type
        self.attribute = attribute
        self.atk = atk
        self.defense = defense
        self.face = Face.Down
    
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
        print(f" {self.name}(ATK:{self.atk},DEF:{self.defense}) ")






class Actions:
    def __init__(self):
        self.num_norm_sum = 0
        self.norm_sum_limit = 1

    def normal_summon():
        pass

    def normal_set():
        pass

    def tribute_summon():
        pass

    def tribute_set():
        pass

    def activate_spell():
        pass

    def set_spell_trap():
        pass

    def check_player_grave():
        pass

    def check_opponent_grave():
        pass


class BoardState:
    def __init__(self):
        self.om = [None,None,None,None,None] # monster zones
        self.ost = [None,None,None,None,None] # spell/trap zones
        self.oh = set() # Opponent hand
        self.og = set() # graveyard
        self.ob = set() # banished
        self.of = None # field spell
        self.pm = [None,None,None,None,None]
        self.pst = [None,None,None,None,None]
        self.ph = set()
        self.pg = set()
        self.pb = set()
        self.pf = None

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
        


class PlayGame:
    def __init__(self, player_deck: Deck, opponent_deck: Deck):
        self.pdeck = player_deck
        self.odeck = opponent_deck
        self.lp = 4000 #life points
        self.olp = 4000
        self.turn = 1
        self.active = Turn.YOUR
        self.phase = Phase.DRAW
        self.b = BoardState()

        def start_game(self):
            self.active = Turn(random.choice([0,1])) # select starting player




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
    
    def print_deck(self):
        print(f'{len(self.cards)} Cards')
        for name, cnt in self.card_count.items():
            print(f'\t{name}  x{cnt}')

    

class Player:
    def __init__(self, deck: Deck):
        self.deck = deck
        self.hand = set()
        self.board = []
        self.MAXBOARDLEN = 3

    
    def start(self):
        for _ in range(5):
            self.hand.add(self.deck.draw())