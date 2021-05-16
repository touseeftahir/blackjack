import random

# keep this into object.py
suits = ('H', 'D', 'S', 'C')
ranks = ('2', '3', '4', '5', '6', '7',
         '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
          '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


# CLASSES

# Card Class
class Card:  # Creates all the cards

    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return self.rank + self.suit


# deck class


class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank, values[rank]))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()
        return 'The deck has: ' + deck_comp

    def shuffle(self):  # shuffle all the cards in the deck
        random.shuffle(self.deck)

    def deal(self):  # pick out a card from the deck
        single_card = self.deck.pop()
        return single_card

# Hand Class


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # keep track of aces

    def add_card(self, card: Card):  # add a card to the player's or dealer's hand
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def total_cards(self):
        return self.cards.count

    def total_points(self):
        return self.value


class Session():
    startTime = None
    stopMoney = None

    def set_start_time(self, startTime):
        self.startTime = startTime

    def get_start_time(self):
        return self.startTime

    def set_stop_money(self, stopMoney):
        self.stopMoney = stopMoney

    def get_stop_money(self):
        return self.stopMoney
