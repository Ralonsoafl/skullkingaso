# Skull king online
import random
from pdb import set_trace
from itertools import chain
import numpy as np

images = {
    0: 'flag',
    14: 'mermaid',
    15: 'pirate',
    16: 'SK',
    None: 'Flag-pirate'
}
class Card():
    '''
    Class Card
    Create a card with a given type and number.
    Attributes:
        - string type
        - int num
        - bool played
    '''
    def __init__(self, card_type, played=False, num=None):
        self.type = card_type
        self.num = num
        self.played = played
'''
Class Deck
Create a deck of cards to be played in every round.
Attributes:
    - list self
Methods:
    - shuffle(self)
'''
class Deck(list):
    def __init__(self):
        # Add all kind of cards we need to play this game
        # From 1 to 13 numbers of each color
        # for colour in ['red', 'blue', 'yellow', 'black']:
        #     for number in range(1, 14):
        #         new_card = Card(colour, False, number)
        #         self.append(new_card)
        # One skull king card
        sk_card = Card('special', False, 16)
        self.append(sk_card)
        # Two mermaid cards
        mermaid_card = Card('special', False, 14)
        for _ in range(2):
            self.append(mermaid_card)
        # Five pirate cards
        pirate_card = Card('special', False, 15)
        for _ in range(5):
            self.append(pirate_card)
        # One pirate or flag card
        pirate_flag_card = Card('special', False, np.nan)
        self.append(pirate_flag_card)
        # Five flag cards
        flag_card = Card('special', False, 0)
        for _ in range(5):
            self.append(flag_card)

    # Shuffle deck
    def shuffle(self):
        random.shuffle(self)


'''
Class Player
Create a player.
Attributes:
    - string name
    - int points
    - Card[] cards
    - int/nan bet
    - int won_hands
Methods:
    - show_cards(self)
        Print all the cards of the player
    - play_cards(self, nb_cards)
        Set played a card
'''


class Player():
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.points = 0
        self.cards = []
        self.bet = np.nan
        self.won_hands = 0

    def show_cards(self):
        for card in self.cards:
            if card.type == 'special':
                print(images[card.num])
            else:
                print(str(card.num) + 'of' + card.type)

    def play_card(self, nb_card):
        if nb_card < 0 or nb_card >= len(
                self.cards) or self.cards[nb_card].played:
            print('Not possible')
        else:
            if self.cards[nb_card].type == 'special' and np.isnan(
                    self.cards[nb_card].num):
                choice = 'A'
                while (choice != 'P' and choice != 'F'):
                    try:
                        choice = str(input('Flag (F) or pirate (P)?'))
                    except:
                        print('Choose a valid option P/F')

                if choice == 'F':
                    self.cards[nb_card].num = -1
                elif choice == 'P':
                    self.cards[nb_card].num = 15

        self.cards[nb_card].played = True

        return self.cards[nb_card]

    def reset(self):
        self.won_hands = 0
        self.cards = []
        self.bet = np.nan


'''
Class Hand
Create a hand of cards in a round.
Attributes:
    - list self
    - int dominant_col
Methods:
    - add_card(self, card)
        Add a card to the hand
    - locate_best_in_color(self, color)
        Set played a card
    - compute_winner(self)
'''


class Hand(list):
    def __init__(self):
        self.dominant_col = None

    def add_card(self, card):
        self.append(card)

        if card.type != 'special' and not card.type:
            self.dominant_col = card.type

    def show_hand(self):
        for card in self:
            if card.type == 'special':
                print(images[card.num])
            else:
                print(str(card.num) + ' of ' + card.type)

    def locate_best_in_color(self, color):
        types = [c.type for c in self]
        numbers = [c.num for c in self]

        where_color = [i for i, e in enumerate(types) if e == color]

        if len(where_color) > 0:
            color_num = []
            for idx in where_color:
                color_num.append(numbers[idx])
            max_color = np.nanmax(color_num)

            possible_num = np.where(numbers == max_color)

            winner = np.intersect1d(possible_num, where_color)
        else:
            winner = None

        return winner

    def compute_winner(self):
        numbers = np.array([c.num for c in self])
        max_number = np.nanmax(numbers)
        global bonus
        bonus = 0
        set_trace()
        # SK, pirate or mermaid
        if max_number == 16:
            if 14 in numbers:
                winner = np.where(numbers == 14)[0][0]
                bonus = 50
            else:
                winner = np.where(numbers == 16)[0][0]
                bonus = 30 * np.where(numbers == 15)[0].size + 30 * np.where(
                    numbers == -1)[0].size

        elif max_number == 15:
            winner = np.where(numbers == 15)[0][0]

        elif max_number == 14:
            winner = np.where(numbers == 14)[0][0]

        # Color check
        winner = self.locate_best_in_color('black')
        if not winner:
            winner = self.locate_best_in_color(self.dominant_col)
        return winner


class color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


if __name__ == '__main__':

    # Set number of players
    players_list = []
    print('How many players today?')

    nb_players = int(input())
    while (not isinstance(nb_players, int)
           and (nb_players < 2 or nb_players > 6)):
        print('This game is for 2-6 players')
        nb_players = int(input())

    for p in range(nb_players):
        # playername = input('name of player' + str(p))
        playername = 'Player_' + str(p)
        players_list.append(Player(playername, p))
        print(playername + ' joined the game')

    for ronda in range(5, 6):
        deck = Deck()
        deck.shuffle()

        nb_cards = ronda + 1
        print(color.BOLD + 'ROUND ' + str(nb_cards) + color.END)

        start_play = ronda % nb_players

        # Order will determine the order of the players playing
        order = np.append(
            np.arange(start_play, nb_players), np.arange(start_play))

        for card_given in range(nb_cards):
            for i in order:
                player = players_list[i]
                player.cards.append(deck[0])
                deck.remove(deck[0])

        # Bets
        for i in order:
            player = players_list[i]
            while (np.isnan(player.bet) or player.bet > nb_cards
                   or player.bet < 0 or not isinstance(player.bet, int)):
                try:
                    player.bet = int(input('Bet of ' + player.name + ': '))
                except:
                    print('Please introduce a valid value ')

        # Play round
        for c in range(nb_cards):
            hand = Hand()
            print(hand)
            for i in order:
                player = players_list[i]
                player.show_cards()
                card2play = int(input(player.name + ' will play card: '))

                played_card = player.play_card(card2play)

                hand.add_card(played_card)

            set_trace()
            # Winner is the index of the player winning the hand
            print(hand)
            winner = hand.compute_winner()
            print(winner)

            if bonus:
                players_list[winner].points += bonus
            players_list[winner].won_hands += 1

            del hand
            del bonus

        # Once all cards have been played: count points
        # Count points
        for player in players_list:
            if player.bet == 0:
                if player.won_hands == 0:
                    player.points += 10 * nb_cards
                else:
                    player.points -= 10 * nb_cards
            else:
                if player.won_hands == player.bet:
                    player.points += 20 * player.won_hands
                else:
                    player.points -= 10 * abs(player.won_hands - player.bet)

            player.reset()

        del deck
